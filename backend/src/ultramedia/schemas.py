from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field


class RaceOut(BaseModel):
    id: str
    name: str
    distance_miles: float
    location: str
    status: str


class IngestResult(BaseModel):
    race_id: str
    timing_events: int
    knowledge_chunks: int
    source_mode: str


class MomentInput(BaseModel):
    athlete_bib: str = Field(min_length=1, max_length=16)
    signal_type: Literal["position_gain", "record_watch", "cutoff_watch", "pace_change"]
    headline_hint: str = Field(min_length=3, max_length=240)


class StoryGenerateRequest(BaseModel):
    race_id: str = "wser-demo"
    moment: MomentInput


class Citation(BaseModel):
    id: str
    title: str
    source_url: str
    excerpt: str
    score: float


class StoryOut(BaseModel):
    id: str
    race_id: str
    athlete_bib: str
    eyebrow: str
    headline: str
    body: str
    social_caption: str
    confidence: float
    status: str
    citations: list[Citation]
    trace_id: str
    created_at: datetime


class ReviewRequest(BaseModel):
    decision: Literal["approved", "revision_requested", "rejected"]
    reviewer: str = Field(min_length=2, max_length=80)
    rationale: str = Field(default="", max_length=500)


class TraceSpanOut(BaseModel):
    stage: str
    status: str
    duration_ms: int
    detail: str


class TraceOut(BaseModel):
    trace_id: str
    spans: list[TraceSpanOut]
    total_duration_ms: int


class EvalMetric(BaseModel):
    name: str
    score: float
    target: float
    passed: bool


class EvalReport(BaseModel):
    suite: str
    cases: int
    release_decision: Literal["PASS", "FAIL"]
    metrics: list[EvalMetric]
