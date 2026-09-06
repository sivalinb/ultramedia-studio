import json

from sqlalchemy import delete, func, select

from .database import Database, KnowledgeChunk, Race, TimingEvent
from .providers import hash_embedding


def seed_sample(database: Database, data_path, *, replace: bool = False) -> dict[str, int | str]:
    payload = json.loads(data_path.read_text())
    race_data = payload["race"]
    with database.session() as db:
        existing = db.scalar(select(func.count()).select_from(Race).where(Race.id == race_data["id"]))
        if existing and not replace:
            timings = db.scalar(
                select(func.count()).select_from(TimingEvent).where(TimingEvent.race_id == race_data["id"])
            )
            chunks = db.scalar(
                select(func.count()).select_from(KnowledgeChunk).where(KnowledgeChunk.race_id == race_data["id"])
            )
            return {"race_id": race_data["id"], "timing_events": timings or 0, "knowledge_chunks": chunks or 0}
        if replace:
            db.execute(delete(TimingEvent).where(TimingEvent.race_id == race_data["id"]))
            db.execute(delete(KnowledgeChunk).where(KnowledgeChunk.race_id == race_data["id"]))
            db.execute(delete(Race).where(Race.id == race_data["id"]))
        db.add(Race(**race_data))
        for event in payload["timing_events"]:
            db.add(TimingEvent(race_id=race_data["id"], **event))
        for chunk in payload["knowledge_chunks"]:
            db.add(
                KnowledgeChunk(
                    race_id=race_data["id"],
                    embedding=hash_embedding(chunk["text"]),
                    **chunk,
                )
            )
    return {
        "race_id": race_data["id"],
        "timing_events": len(payload["timing_events"]),
        "knowledge_chunks": len(payload["knowledge_chunks"]),
    }
