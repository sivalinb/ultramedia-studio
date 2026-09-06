import math
import re
from collections import Counter

from sqlalchemy import select
from sqlalchemy.orm import Session

from .database import KnowledgeChunk, TimingEvent
from .providers import hash_embedding

STOP_WORDS = {"the", "and", "for", "with", "from", "that", "this", "into", "was", "are"}


def tokenize(text: str) -> list[str]:
    return [token for token in re.findall(r"[a-z0-9]+", text.lower()) if len(token) > 2 and token not in STOP_WORDS]


def cosine(a: list[float], b: list[float]) -> float:
    if not a or not b or len(a) != len(b):
        return 0.0
    denominator = math.sqrt(sum(x * x for x in a)) * math.sqrt(sum(y * y for y in b))
    return sum(x * y for x, y in zip(a, b, strict=True)) / denominator if denominator else 0.0


class HybridRetriever:
    def __init__(self, dimensions: int = 256):
        self.dimensions = dimensions

    def search(self, db: Session, race_id: str, query: str, top_k: int = 5) -> list[dict]:
        documents = list(db.scalars(select(KnowledgeChunk).where(KnowledgeChunk.race_id == race_id)))
        query_tokens = Counter(tokenize(query))
        query_vector = hash_embedding(query, self.dimensions)
        ranked: list[tuple[float, KnowledgeChunk]] = []
        for document in documents:
            doc_tokens = Counter(tokenize(document.text))
            overlap = sum(min(count, doc_tokens[token]) for token, count in query_tokens.items())
            lexical = overlap / max(1, sum(query_tokens.values()))
            dense = cosine(query_vector, document.embedding or [])
            score = 0.58 * max(0.0, dense) + 0.42 * lexical
            ranked.append((score, document))
        ranked.sort(key=lambda item: item[0], reverse=True)
        return [
            {
                "id": document.id,
                "title": document.title,
                "source_url": document.source_url,
                "excerpt": document.text[:420],
                "score": round(score, 4),
            }
            for score, document in ranked[:top_k]
        ]

    def timing_context(self, db: Session, race_id: str, athlete_bib: str) -> list[dict]:
        events = list(
            db.scalars(
                select(TimingEvent)
                .where(TimingEvent.race_id == race_id, TimingEvent.athlete_bib == athlete_bib)
                .order_by(TimingEvent.mile.desc())
                .limit(4)
            )
        )
        return [
            {
                "id": event.id,
                "athlete_bib": event.athlete_bib,
                "athlete_name": event.athlete_name,
                "checkpoint": event.checkpoint,
                "mile": event.mile,
                "elapsed_seconds": event.elapsed_seconds,
                "position_overall": event.position_overall,
            }
            for event in events
        ]
