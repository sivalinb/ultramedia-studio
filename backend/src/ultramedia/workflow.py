from typing import TypedDict
from uuid import uuid4

from langgraph.graph import END, START, StateGraph
from sqlalchemy import select

from .database import Database, StoryDraft
from .observability import TraceRecorder
from .providers import GeneratedStory, StoryProvider
from .retrieval import HybridRetriever
from .schemas import StoryGenerateRequest


class StoryState(TypedDict, total=False):
    race_id: str
    moment: dict
    timing: list[dict]
    evidence: list[dict]
    generated: dict
    confidence: float
    safety_passed: bool
    story_id: str
    trace_id: str


class StoryWorkflow:
    def __init__(self, database: Database, provider: StoryProvider, retriever: HybridRetriever):
        self.database = database
        self.provider = provider
        self.retriever = retriever
        self._active_trace: TraceRecorder | None = None
        builder = StateGraph(StoryState)
        builder.add_node("moment_detector", self._moment_detector)
        builder.add_node("evidence_retriever", self._evidence_retriever)
        builder.add_node("story_writer", self._story_writer)
        builder.add_node("fact_verifier", self._fact_verifier)
        builder.add_node("safety_editor", self._safety_editor)
        builder.add_node("human_review_queue", self._persist_for_review)
        builder.add_edge(START, "moment_detector")
        builder.add_edge("moment_detector", "evidence_retriever")
        builder.add_edge("evidence_retriever", "story_writer")
        builder.add_edge("story_writer", "fact_verifier")
        builder.add_edge("fact_verifier", "safety_editor")
        builder.add_edge("safety_editor", "human_review_queue")
        builder.add_edge("human_review_queue", END)
        self.graph = builder.compile()

    @property
    def trace(self) -> TraceRecorder:
        if self._active_trace is None:
            raise RuntimeError("Workflow trace is unavailable")
        return self._active_trace

    def _moment_detector(self, state: StoryState) -> dict:
        with self.trace.stage("moment_detector", "Validated race signal and athlete reference"):
            moment = state["moment"]
            if not moment.get("athlete_bib") or not moment.get("headline_hint"):
                raise ValueError("Moment requires athlete_bib and headline_hint")
            return {"moment": moment}

    def _evidence_retriever(self, state: StoryState) -> dict:
        with self.trace.stage("evidence_retriever", "Hybrid retrieval over timing and course context"):
            query = f"{state['moment']['headline_hint']} {state['moment']['signal_type']}"
            with self.database.session() as db:
                timing = self.retriever.timing_context(db, state["race_id"], state["moment"]["athlete_bib"])
                evidence = self.retriever.search(db, state["race_id"], query)
            if not timing:
                raise ValueError("No timing evidence found for athlete")
            latest = timing[0]
            previous = timing[1] if len(timing) > 1 else timing[0]
            timing_citation = {
                "id": f"timing-{latest['id']}",
                "title": f"Timing comparison · {latest['checkpoint']}",
                "source_url": f"ultramedia://timing/{latest['id']}",
                "excerpt": (
                    f"Synthetic timing: {latest['athlete_name']} moved from position "
                    f"{previous['position_overall']} at {previous['checkpoint']} to position "
                    f"{latest['position_overall']} at {latest['checkpoint']}."
                ),
                "score": 1.0,
            }
            return {"timing": timing, "evidence": [timing_citation, *evidence]}

    def _story_writer(self, state: StoryState) -> dict:
        with self.trace.stage("story_writer", f"Generated structured draft with {self.provider.name}"):
            generated = self.provider.generate(state["moment"], state["evidence"], state["timing"])
            return {"generated": generated.model_dump()}

    def _fact_verifier(self, state: StoryState) -> dict:
        with self.trace.stage("fact_verifier", "Checked citations and claim support"):
            generated = GeneratedStory.model_validate(state["generated"])
            allowed = {item["id"] for item in state["evidence"]}
            valid = [citation for citation in generated.citation_ids if citation in allowed]
            if not valid:
                raise ValueError("Draft has no valid evidence citations")
            generated.citation_ids = valid
            confidence = min(0.99, 0.78 + 0.04 * len(valid))
            return {"generated": generated.model_dump(), "confidence": confidence}

    def _safety_editor(self, state: StoryState) -> dict:
        with self.trace.stage("safety_editor", "Blocked unsupported health and intent inferences"):
            text = f"{state['generated']['headline']} {state['generated']['body']}".lower()
            evidence_text = " ".join(item["excerpt"] for item in state["evidence"]).lower()
            sensitive_terms = ("injury", "injured", "dehydrated", "collapsed", "medical condition")
            unsupported = [term for term in sensitive_terms if term in text and term not in evidence_text]
            if unsupported:
                raise ValueError(f"Unsupported sensitive inference: {unsupported[0]}")
            return {"safety_passed": True}

    def _persist_for_review(self, state: StoryState) -> dict:
        with self.trace.stage("human_review_queue", "Stored draft as pending; no automatic publication"):
            generated = GeneratedStory.model_validate(state["generated"])
            citation_map = {item["id"]: item for item in state["evidence"]}
            citations = [citation_map[citation] for citation in generated.citation_ids]
            story = StoryDraft(
                race_id=state["race_id"],
                athlete_bib=state["moment"]["athlete_bib"],
                signal_type=state["moment"]["signal_type"],
                eyebrow=generated.eyebrow,
                headline=generated.headline,
                body=generated.body,
                social_caption=generated.social_caption,
                confidence=state["confidence"],
                status="pending_review",
                citations=citations,
                trace_id=state["trace_id"],
            )
            with self.database.session() as db:
                db.add(story)
                db.flush()
                story_id = story.id
            return {"story_id": story_id}

    def run(self, request: StoryGenerateRequest) -> StoryDraft:
        trace = TraceRecorder(self.database, str(uuid4()))
        self._active_trace = trace
        try:
            result = self.graph.invoke(
                {
                    "race_id": request.race_id,
                    "moment": request.moment.model_dump(),
                    "trace_id": trace.trace_id,
                }
            )
        finally:
            self._active_trace = None
        with self.database.session() as db:
            story = db.scalar(select(StoryDraft).where(StoryDraft.id == result["story_id"]))
            if story is None:
                raise RuntimeError("Story draft was not persisted")
            db.expunge(story)
            return story
