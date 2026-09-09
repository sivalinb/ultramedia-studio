import json

from .database import Database, GenerationRecord
from .providers import LocalStoryProvider
from .retrieval import HybridRetriever
from .schemas import EvalMetric, EvalReport, MomentInput, StoryGenerateRequest
from .workflow import StoryWorkflow


def run_eval_suite(database: Database, dimensions: int = 256, provider=None) -> EvalReport:
    retriever = HybridRetriever(dimensions)
    retrieval_cases = [
        ("course climbing and descending profile", "wser-course-profile"),
        ("official finish cutoff award deadline", "wser-finish-window"),
        ("canyons and river crossing", "wser-canyons"),
        ("synthetic athlete timing demonstration", "simulation-policy"),
    ]
    retrieval_hits = 0
    case_results = []
    with database.session() as db:
        for query, target in retrieval_cases:
            ids = {item["id"] for item in retriever.search(db, "wser-demo", query, top_k=3)}
            retrieval_hits += int(target in ids)
            case_results.append({"kind": "retrieval", "id": target, "passed": target in ids})

    provider = provider or LocalStoryProvider()
    workflow = StoryWorkflow(database, provider, retriever)
    generation_cases = [
        MomentInput(
            athlete_bib="214",
            signal_type="position_gain",
            headline_hint="large position gain through the canyon sector",
        ),
        MomentInput(
            athlete_bib="101",
            signal_type="record_watch",
            headline_hint="leader pace at Foresthill with historical context",
        ),
    ]
    stories = []
    for moment in generation_cases:
        try:
            story = workflow.run(StoryGenerateRequest(race_id="wser-demo", moment=moment))
            stories.append(story)
            case_results.append(
                {
                    "kind": "generation",
                    "id": moment.signal_type,
                    "passed": True,
                    "story_id": story.id,
                    "trace_id": story.trace_id,
                }
            )
        except Exception as error:
            # An invalid model output is a failed eval case, never an omitted denominator or HTTP500.
            # Exception bodies can contain provider URLs/credentials; retain only the error class.
            case_results.append(
                {"kind": "generation", "id": moment.signal_type, "passed": False, "error_type": type(error).__name__}
            )
    attempted = len(generation_cases)
    with database.session() as db:
        citations_valid = (
            sum(db.get(GenerationRecord, story.id).checks["citation_ids_valid"] for story in stories) / attempted
        )
        sensitive_pass_rate = (
            sum(db.get(GenerationRecord, story.id).checks["sensitive_language_absent"] for story in stories) / attempted
        )
    human_gate = sum(story.status == "pending_review" for story in stories) / attempted

    metrics = [
        EvalMetric(
            name="generation_contract_pass_rate",
            score=len(stories) / attempted,
            target=1.0,
            passed=len(stories) == attempted,
        ),
        EvalMetric(
            name="retrieval_recall_at_3",
            score=retrieval_hits / len(retrieval_cases),
            target=0.75,
            passed=retrieval_hits / len(retrieval_cases) >= 0.75,
        ),
        EvalMetric(
            name="citation_validity",
            score=citations_valid,
            target=1.0,
            passed=citations_valid >= 1.0,
        ),
        EvalMetric(
            name="human_review_gate",
            score=human_gate,
            target=1.0,
            passed=human_gate >= 1.0,
        ),
        EvalMetric(
            name="sensitive_language_check_pass_rate",
            score=sensitive_pass_rate,
            target=1.0,
            passed=sensitive_pass_rate == 1.0,
        ),
    ]
    return EvalReport(
        suite=f"ultramedia-workflow-v2:{provider.name}",
        cases=len(retrieval_cases) + len(generation_cases),
        release_decision="PASS" if all(metric.passed for metric in metrics) else "FAIL",
        metrics=metrics,
        case_results=case_results,
    )


def main() -> None:
    from .config import get_settings
    from .seed import seed_sample

    settings = get_settings()
    database = Database(settings.database_url)
    database.create_all()
    seed_sample(database, settings.data_dir / "sample_race.json")
    print(json.dumps(run_eval_suite(database, settings.embedding_dimensions).model_dump(), indent=2))


if __name__ == "__main__":
    main()
