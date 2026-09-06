import hashlib
import json
import re
from typing import Protocol

import httpx
from pydantic import BaseModel, Field

from .config import Settings


class GeneratedStory(BaseModel):
    eyebrow: str
    headline: str
    body: str
    social_caption: str
    citation_ids: list[str] = Field(min_length=1)


class StoryProvider(Protocol):
    name: str

    def generate(self, moment: dict, evidence: list[dict], timing: list[dict]) -> GeneratedStory: ...


def hash_embedding(text: str, dimensions: int = 256) -> list[float]:
    vector = [0.0] * dimensions
    tokens = re.findall(r"[a-z0-9]+", text.lower())
    for token in tokens:
        digest = hashlib.sha256(token.encode()).digest()
        index = int.from_bytes(digest[:4], "big") % dimensions
        vector[index] += 1.0 if digest[4] % 2 else -1.0
    magnitude = sum(value * value for value in vector) ** 0.5 or 1.0
    return [value / magnitude for value in vector]


class LocalStoryProvider:
    """Deterministic local provider used for tests and zero-cost development."""

    name = "local-deterministic"

    def generate(self, moment: dict, evidence: list[dict], timing: list[dict]) -> GeneratedStory:
        athlete = timing[0]["athlete_name"] if timing else f"Bib {moment['athlete_bib']}"
        latest = timing[0] if timing else None
        previous = timing[1] if len(timing) > 1 else None
        position_gain = 0
        if latest and previous:
            position_gain = max(0, previous["position_overall"] - latest["position_overall"])
        citations = [item["id"] for item in evidence[:3]]
        signal = moment["signal_type"]
        if signal == "position_gain":
            eyebrow = "Turning point detected"
            headline = f"{athlete} just changed the shape of the race."
            detail = (
                f"gained {position_gain} positions from {previous['checkpoint']} to {latest['checkpoint']}"
                if latest and previous
                else "produced a sustained position gain"
            )
        elif signal == "record_watch":
            eyebrow = "Course record watch"
            headline = f"{athlete} is carrying historic pace into the next sector."
            detail = "remains on the modeled record trajectory"
        elif signal == "cutoff_watch":
            eyebrow = "Cutoff watch"
            headline = "The final finish window is tightening."
            detail = "is approaching the next checkpoint inside the modeled cutoff window"
        else:
            eyebrow = "Pace change"
            headline = f"A measured shift from {athlete} is worth watching."
            detail = "changed pace while maintaining forward position"
        body = (
            f"{athlete} {detail}. UltraMedia matched the timing signal "
            "with course context and historical race notes; an editor must approve this draft before publication."
        )
        return GeneratedStory(
            eyebrow=eyebrow,
            headline=headline,
            body=body,
            social_caption=f"{eyebrow}: {headline} Verified race context attached. #UltraMedia",
            citation_ids=citations or ["timing-simulation"],
        )


class FireworksStoryProvider:
    name = "fireworks-qwen"

    def __init__(self, settings: Settings):
        self.settings = settings

    def generate(self, moment: dict, evidence: list[dict], timing: list[dict]) -> GeneratedStory:
        allowed_ids = [item["id"] for item in evidence]
        response = httpx.post(
            "https://api.fireworks.ai/inference/v1/chat/completions",
            headers={"Authorization": f"Bearer {self.settings.fireworks_api_key}"},
            json={
                "model": self.settings.fireworks_chat_model,
                "temperature": 0.1,
                "max_tokens": 500,
                "response_format": {"type": "json_object"},
                "messages": [
                    {
                        "role": "system",
                        "content": (
                            "You are an ultramarathon newsroom editor. Return JSON with eyebrow, headline, body, "
                            "social_caption, and citation_ids. Use only supplied evidence. Never infer health, injury, "
                            "intent, or emotion. Keep the draft factual and vivid. citation_ids must be selected from: "
                            + ", ".join(allowed_ids)
                        ),
                    },
                    {
                        "role": "user",
                        "content": json.dumps({"moment": moment, "timing": timing, "evidence": evidence}),
                    },
                ],
            },
            timeout=25,
        )
        response.raise_for_status()
        payload = response.json()
        parsed = json.loads(payload["choices"][0]["message"]["content"])
        story = GeneratedStory.model_validate(parsed)
        story.citation_ids = [citation for citation in story.citation_ids if citation in allowed_ids]
        if not story.citation_ids:
            raise ValueError("Provider returned no valid citations")
        return story


class OllamaStoryProvider:
    name = "ollama-qwen3"

    def __init__(self, settings: Settings):
        self.settings = settings

    def generate(self, moment: dict, evidence: list[dict], timing: list[dict]) -> GeneratedStory:
        allowed_ids = [item["id"] for item in evidence]
        prompt = (
            "Return compact JSON with eyebrow, headline, body, social_caption, citation_ids. "
            "Use only the evidence; do not infer medical condition or emotion.\n"
            + json.dumps({"moment": moment, "timing": timing, "evidence": evidence})
        )
        response = httpx.post(
            f"{self.settings.ollama_base_url.rstrip('/')}/api/chat",
            json={
                "model": self.settings.ollama_model,
                "stream": False,
                "format": "json",
                "messages": [{"role": "user", "content": prompt}],
                "options": {"temperature": 0.1},
            },
            timeout=60,
        )
        response.raise_for_status()
        story = GeneratedStory.model_validate_json(response.json()["message"]["content"])
        story.citation_ids = [citation for citation in story.citation_ids if citation in allowed_ids]
        if not story.citation_ids:
            raise ValueError("Local model returned no valid citations")
        return story


def select_provider(settings: Settings) -> StoryProvider:
    if settings.provider_mode == "fireworks" or (settings.provider_mode == "auto" and settings.fireworks_api_key):
        return FireworksStoryProvider(settings)
    if settings.provider_mode == "ollama":
        return OllamaStoryProvider(settings)
    return LocalStoryProvider()
