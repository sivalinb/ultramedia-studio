from fastapi import Depends, FastAPI, Header, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import select

from .config import Settings, get_settings
from .database import Approval, Database, Race, StoryDraft, TraceSpan
from .evals import run_eval_suite
from .observability import configure_telemetry
from .providers import select_provider
from .retrieval import HybridRetriever
from .schemas import (
    Citation,
    EvalReport,
    IngestResult,
    RaceOut,
    ReviewRequest,
    StoryGenerateRequest,
    StoryOut,
    TraceOut,
    TraceSpanOut,
)
from .seed import seed_sample
from .workflow import StoryWorkflow


def story_out(story: StoryDraft) -> StoryOut:
    return StoryOut(
        id=story.id,
        race_id=story.race_id,
        athlete_bib=story.athlete_bib,
        eyebrow=story.eyebrow,
        headline=story.headline,
        body=story.body,
        social_caption=story.social_caption,
        confidence=story.confidence,
        status=story.status,
        citations=[Citation.model_validate(item) for item in story.citations],
        trace_id=story.trace_id,
        created_at=story.created_at,
    )


def create_app(settings: Settings | None = None) -> FastAPI:
    settings = settings or get_settings()
    configure_telemetry(settings.otel_exporter_otlp_endpoint, settings.environment)
    database = Database(settings.database_url)
    database.create_all()
    seed_sample(database, settings.data_dir / "sample_race.json")
    provider = select_provider(settings)
    retriever = HybridRetriever(settings.embedding_dimensions)
    workflow = StoryWorkflow(database, provider, retriever)

    app = FastAPI(
        title=settings.app_name,
        version="0.1.0",
        description="Evidence-grounded ultramarathon newsroom API with a mandatory human review gate.",
    )
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.allowed_origins,
        allow_credentials=False,
        allow_methods=["GET", "POST"],
        allow_headers=["Content-Type", "X-Reviewer-Key"],
    )
    app.state.settings = settings
    app.state.database = database
    app.state.provider = provider
    app.state.workflow = workflow

    def require_reviewer_key(x_reviewer_key: str | None = Header(default=None)) -> None:
        if settings.approval_api_key and x_reviewer_key != settings.approval_api_key:
            raise HTTPException(status_code=401, detail="Valid reviewer key required")

    @app.get("/health")
    def health() -> dict:
        return {
            "status": "ok",
            "service": "ultramedia-api",
            "provider": provider.name,
            "publication_mode": "human-gated",
        }

    @app.get("/api/v1/races", response_model=list[RaceOut])
    def list_races() -> list[RaceOut]:
        with database.session() as db:
            races = list(db.scalars(select(Race).order_by(Race.name)))
            return [
                RaceOut(
                    id=race.id,
                    name=race.name,
                    distance_miles=race.distance_miles,
                    location=race.location,
                    status=race.status,
                )
                for race in races
            ]

    @app.post("/api/v1/races/{race_id}/ingest", response_model=IngestResult)
    def ingest_demo(race_id: str, replace: bool = Query(default=False)) -> IngestResult:
        if race_id != "wser-demo":
            raise HTTPException(status_code=404, detail="Only the governed demo connector is enabled")
        result = seed_sample(database, settings.data_dir / "sample_race.json", replace=replace)
        return IngestResult(**result, source_mode="governed-fixture")

    @app.post("/api/v1/stories/generate", response_model=StoryOut, status_code=201)
    def generate_story(request: StoryGenerateRequest) -> StoryOut:
        try:
            return story_out(workflow.run(request))
        except ValueError as error:
            raise HTTPException(status_code=422, detail=str(error)) from error

    @app.get("/api/v1/stories", response_model=list[StoryOut])
    def list_stories(limit: int = Query(default=20, ge=1, le=100)) -> list[StoryOut]:
        with database.session() as db:
            stories = list(db.scalars(select(StoryDraft).order_by(StoryDraft.created_at.desc()).limit(limit)))
            return [story_out(story) for story in stories]

    @app.post(
        "/api/v1/stories/{story_id}/review",
        response_model=StoryOut,
        dependencies=[Depends(require_reviewer_key)],
    )
    def review_story(story_id: str, request: ReviewRequest) -> StoryOut:
        with database.session() as db:
            story = db.get(StoryDraft, story_id)
            if story is None:
                raise HTTPException(status_code=404, detail="Story not found")
            db.add(
                Approval(
                    story_id=story_id,
                    decision=request.decision,
                    reviewer=request.reviewer,
                    rationale=request.rationale,
                )
            )
            story.status = request.decision
            db.flush()
            db.refresh(story)
            return story_out(story)

    @app.get("/api/v1/traces/{trace_id}", response_model=TraceOut)
    def get_trace(trace_id: str) -> TraceOut:
        with database.session() as db:
            spans = list(
                db.scalars(select(TraceSpan).where(TraceSpan.trace_id == trace_id).order_by(TraceSpan.created_at))
            )
            if not spans:
                raise HTTPException(status_code=404, detail="Trace not found")
            return TraceOut(
                trace_id=trace_id,
                total_duration_ms=sum(span.duration_ms for span in spans),
                spans=[
                    TraceSpanOut(
                        stage=span.stage,
                        status=span.status,
                        duration_ms=span.duration_ms,
                        detail=span.detail,
                    )
                    for span in spans
                ],
            )

    @app.post("/api/v1/evals/run", response_model=EvalReport)
    def run_evals() -> EvalReport:
        return run_eval_suite(database, settings.embedding_dimensions)

    return app


app = create_app()


def run() -> None:
    import uvicorn

    uvicorn.run("ultramedia.main:app", host="0.0.0.0", port=8000, reload=False)


if __name__ == "__main__":
    run()
