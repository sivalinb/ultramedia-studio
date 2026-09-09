from collections.abc import Iterator
from contextlib import contextmanager
from datetime import UTC, datetime
from uuid import uuid4

from sqlalchemy import JSON, DateTime, Float, ForeignKey, Integer, String, Text, create_engine
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    Session,
    mapped_column,
    relationship,
    sessionmaker,
)
from sqlalchemy.pool import StaticPool


def utcnow() -> datetime:
    return datetime.now(UTC)


class Base(DeclarativeBase):
    pass


class Race(Base):
    __tablename__ = "races"
    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    name: Mapped[str] = mapped_column(String(160))
    distance_miles: Mapped[float] = mapped_column(Float)
    location: Mapped[str] = mapped_column(String(200))
    status: Mapped[str] = mapped_column(String(32), default="simulation")


class TimingEvent(Base):
    __tablename__ = "timing_events"
    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid4()))
    race_id: Mapped[str] = mapped_column(ForeignKey("races.id"), index=True)
    athlete_bib: Mapped[str] = mapped_column(String(16), index=True)
    athlete_name: Mapped[str] = mapped_column(String(120))
    checkpoint: Mapped[str] = mapped_column(String(120))
    mile: Mapped[float] = mapped_column(Float)
    elapsed_seconds: Mapped[int] = mapped_column(Integer)
    position_overall: Mapped[int] = mapped_column(Integer)
    recorded_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)


class KnowledgeChunk(Base):
    __tablename__ = "knowledge_chunks"
    id: Mapped[str] = mapped_column(String(80), primary_key=True)
    race_id: Mapped[str] = mapped_column(String(64), index=True)
    title: Mapped[str] = mapped_column(String(240))
    text: Mapped[str] = mapped_column(Text)
    source_url: Mapped[str] = mapped_column(String(600))
    source_type: Mapped[str] = mapped_column(String(40))
    embedding: Mapped[list[float]] = mapped_column(JSON, default=list)


class StoryDraft(Base):
    __tablename__ = "story_drafts"
    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid4()))
    race_id: Mapped[str] = mapped_column(ForeignKey("races.id"), index=True)
    athlete_bib: Mapped[str] = mapped_column(String(16), index=True)
    signal_type: Mapped[str] = mapped_column(String(40))
    eyebrow: Mapped[str] = mapped_column(String(120))
    headline: Mapped[str] = mapped_column(String(300))
    body: Mapped[str] = mapped_column(Text)
    social_caption: Mapped[str] = mapped_column(Text)
    confidence: Mapped[float] = mapped_column(Float)
    status: Mapped[str] = mapped_column(String(32), default="pending_review")
    citations: Mapped[list[dict]] = mapped_column(JSON, default=list)
    trace_id: Mapped[str] = mapped_column(String(36), index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)
    approvals: Mapped[list["Approval"]] = relationship(back_populates="story")


class Approval(Base):
    __tablename__ = "approvals"
    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid4()))
    story_id: Mapped[str] = mapped_column(ForeignKey("story_drafts.id"), index=True)
    decision: Mapped[str] = mapped_column(String(32))
    reviewer: Mapped[str] = mapped_column(String(80))
    rationale: Mapped[str] = mapped_column(Text, default="")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)
    story: Mapped[StoryDraft] = relationship(back_populates="approvals")


class TraceSpan(Base):
    __tablename__ = "trace_spans"
    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid4()))
    trace_id: Mapped[str] = mapped_column(String(36), index=True)
    stage: Mapped[str] = mapped_column(String(80))
    status: Mapped[str] = mapped_column(String(24))
    duration_ms: Mapped[int] = mapped_column(Integer)
    detail: Mapped[str] = mapped_column(String(500))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)


class GenerationRecord(Base):
    """Additive table: legacy databases retain their stories without ALTER/DROP."""

    __tablename__ = "generation_records"
    story_id: Mapped[str] = mapped_column(ForeignKey("story_drafts.id"), primary_key=True)
    contract_version: Mapped[str] = mapped_column(String(80))
    prompt_version: Mapped[str] = mapped_column(String(80))
    provider: Mapped[str] = mapped_column(String(240))
    inputs: Mapped[dict] = mapped_column(JSON)
    output: Mapped[dict] = mapped_column(JSON)
    checks: Mapped[dict] = mapped_column(JSON)
    revision: Mapped[int] = mapped_column(Integer, default=0)
    provenance: Mapped[dict] = mapped_column(JSON, default=dict)
    __mapper_args__ = {"version_id_col": revision, "version_id_generator": False}


class EditorialRevision(Base):
    __tablename__ = "editorial_revisions"
    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid4()))
    story_id: Mapped[str] = mapped_column(ForeignKey("story_drafts.id"), index=True)
    revision: Mapped[int] = mapped_column(Integer)
    reviewer: Mapped[str] = mapped_column(String(80))
    decision: Mapped[str] = mapped_column(String(32))
    rationale: Mapped[str] = mapped_column(Text)
    before: Mapped[dict] = mapped_column(JSON)
    after: Mapped[dict] = mapped_column(JSON)
    training_consent: Mapped[bool] = mapped_column(default=False)
    rights_basis: Mapped[str] = mapped_column(Text, default="")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)


class Database:
    def __init__(self, url: str):
        options: dict = {"future": True}
        if url.startswith("sqlite"):
            options["connect_args"] = {"check_same_thread": False}
            if url in {"sqlite://", "sqlite:///:memory:"}:
                options["poolclass"] = StaticPool
        self.engine = create_engine(url, **options)
        self.session_factory = sessionmaker(self.engine, expire_on_commit=False, class_=Session)

    def create_all(self) -> None:
        Base.metadata.create_all(self.engine)

    @contextmanager
    def session(self) -> Iterator[Session]:
        db = self.session_factory()
        try:
            yield db
            db.commit()
        except Exception:
            db.rollback()
            raise
        finally:
            db.close()
