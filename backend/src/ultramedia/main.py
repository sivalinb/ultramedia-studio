import httpx
from fastapi import Depends, FastAPI, Header, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import select
from sqlalchemy.orm.exc import StaleDataError

from .config import Settings, get_settings
from .contracts import GeneratedStory, validate_story
from .database import Approval, Database, EditorialRevision, GenerationRecord, Race, StoryDraft, TraceSpan
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


def story_out(story: StoryDraft, record: GenerationRecord | None = None) -> StoryOut:
    return StoryOut(
        id=story.id,
        race_id=story.race_id,
        athlete_bib=story.athlete_bib,
        eyebrow=story.eyebrow,
        headline=story.headline,
        body=story.body,
        social_caption=story.social_caption,
        confidence=None,
        disposition=record.output["disposition"] if record else "legacy_unverified",
        claims=record.output["claims"] if record else [],
        reason=record.output["reason"] if record else "Original generation evidence was not retained.",
        review_revision=record.revision if record else 0,
        quality_checks=record.checks if record else {},
        provider=record.provider if record else "legacy-unrecorded",
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
            story = workflow.run(request)
            with database.session() as db:
                return story_out(story, db.get(GenerationRecord, story.id))
        except ValueError as error:
            raise HTTPException(status_code=422, detail=str(error)) from error
        except httpx.HTTPError as error:
            raise HTTPException(status_code=502, detail="Story provider unavailable; no draft was saved") from error

    @app.get("/api/v1/stories", response_model=list[StoryOut])
    def list_stories(limit: int = Query(default=20, ge=1, le=100)) -> list[StoryOut]:
        with database.session() as db:
            stories = list(db.scalars(select(StoryDraft).order_by(StoryDraft.created_at.desc()).limit(limit)))
            return [story_out(story, db.get(GenerationRecord, story.id)) for story in stories]

    @app.post(
        "/api/v1/stories/{story_id}/review",
        response_model=StoryOut,
        dependencies=[Depends(require_reviewer_key)],
    )
    def review_story(story_id: str, request: ReviewRequest) -> StoryOut:
        try:
            with database.session() as db:
                story = db.get(StoryDraft, story_id)
                if story is None:
                    raise HTTPException(status_code=404, detail="Story not found")
                record = db.get(GenerationRecord, story_id)
                if request.edited_story and (not record or request.expected_revision is None):
                    raise HTTPException(status_code=409, detail="Edits require retained evidence and expected_revision")
                if record and request.expected_revision is not None and record.revision != request.expected_revision:
                    raise HTTPException(status_code=409, detail="A newer editorial revision exists; reload the draft")
                if request.training_consent and (not request.rights_basis.strip() or request.decision != "approved"):
                    raise HTTPException(status_code=422, detail="Training consent requires approval and a rights basis")
                if record:
                    before = record.output
                    after = request.edited_story or GeneratedStory.model_validate(before)
                    checks = validate_story(after, record.inputs)
                    record.output = after.model_dump()
                    record.checks = checks
                    record.revision += 1
                    for field in ("eyebrow", "headline", "body", "social_caption"):
                        setattr(story, field, getattr(after, field))
                    cited = set(after.citation_ids)
                    story.citations = [e for e in record.inputs["evidence"] if e["id"] in cited]
                    db.add(
                        EditorialRevision(
                            story_id=story_id,
                            revision=record.revision,
                            reviewer=request.reviewer,
                            decision=request.decision,
                            rationale=request.rationale,
                            before=before,
                            after=record.output,
                            training_consent=request.training_consent,
                            rights_basis=request.rights_basis,
                        )
                    )
                elif request.training_consent:
                    raise HTTPException(
                        status_code=422, detail="Legacy draft cannot enter training without original evidence"
                    )
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
                return story_out(story, record)
        except StaleDataError as error:
            raise HTTPException(
                status_code=409, detail="A newer editorial revision exists; reload the draft"
            ) from error
        except ValueError as error:
            raise HTTPException(status_code=422, detail=str(error)) from error

    @app.get("/api/v1/stories/{story_id}/revisions", dependencies=[Depends(require_reviewer_key)])
    def revisions(story_id: str) -> list[dict]:
        with database.session() as db:
            rows = db.scalars(
                select(EditorialRevision)
                .where(EditorialRevision.story_id == story_id)
                .order_by(EditorialRevision.revision)
            )
            return [
                {
                    "revision": row.revision,
                    "reviewer": row.reviewer,
                    "decision": row.decision,
                    "rationale": row.rationale,
                    "before": row.before,
                    "after": row.after,
                    "training_consent": row.training_consent,
                    "rights_basis": row.rights_basis,
                }
                for row in rows
            ]

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
        return run_eval_suite(database, settings.embedding_dimensions, provider)

    return app


app = create_app()


def run() -> None:
    import uvicorn

    uvicorn.run("ultramedia.main:app", host="0.0.0.0", port=8000, reload=False)


if __name__ == "__main__":
    run()
