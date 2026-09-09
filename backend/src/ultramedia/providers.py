import hashlib
import json
import re
from typing import Protocol

import httpx

from .config import Settings
from .contracts import (
    METRICS,
    Claim,
    GeneratedStory,
    evidence_facts,
    evidence_sufficient,
    generation_input,
    messages_for,
    required_metric,
    validate_story,
)


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
    """Rule baseline; a passing run does not measure LLM quality."""

    name = "local-deterministic-v2"

    def generate(self, moment: dict, evidence: list[dict], timing: list[dict]) -> GeneratedStory:
        inputs = generation_input(moment, evidence, timing)
        if not evidence_sufficient(inputs):
            return GeneratedStory(
                disposition="insufficient_evidence",
                eyebrow="Evidence needed",
                headline="Hold this race update for verification.",
                body="The supplied evidence is incomplete or conflicting. An editor must verify the signal.",
                social_caption="",
                citation_ids=[],
                claims=[],
                reason="Missing or contradictory signal facts.",
            )
        metric = required_metric(moment["signal_type"])
        value, cid = evidence_facts(inputs)[metric][0]
        athlete = timing[0]["athlete_name"] if timing else "The athlete"
        number = f"{value:g}"
        details = {
            "position_gain": f"a position change of {number} places (positive means gained)",
            "record_margin_seconds": f"a projected record margin of {number} seconds (positive means ahead)",
            "cutoff_buffer_minutes": f"a cutoff buffer of {number} minutes (negative means late)",
            "pace_delta_seconds_per_mile": f"a pace change of {number} seconds per mile (negative means faster)",
        }
        return GeneratedStory(
            disposition="draft",
            eyebrow="Verified signal",
            headline=f"A timing update for {athlete}.",
            body=f"{athlete} has {details[metric]}. This is a synthetic race update awaiting editorial review.",
            social_caption=f"Timing update: {athlete}; {number} {METRICS[metric]}. Awaiting editorial review.",
            citation_ids=[cid],
            claims=[Claim(metric=metric, value=value, citation_id=cid)],
            reason="",
        )


class FireworksStoryProvider:
    name = "fireworks-qwen"

    def __init__(self, settings: Settings):
        self.settings = settings
        self.name = f"fireworks:{settings.fireworks_chat_model}"

    def generate(self, moment: dict, evidence: list[dict], timing: list[dict]) -> GeneratedStory:
        response = httpx.post(
            "https://api.fireworks.ai/inference/v1/chat/completions",
            headers={"Authorization": f"Bearer {self.settings.fireworks_api_key}"},
            json={
                "model": self.settings.fireworks_chat_model,
                "temperature": 0,
                "max_tokens": self.settings.generation_max_tokens,
                "response_format": {"type": "json_object"},
                "messages": messages_for(generation_input(moment, evidence, timing)),
            },
            timeout=25,
        )
        response.raise_for_status()
        payload = response.json()
        parsed = json.loads(payload["choices"][0]["message"]["content"])
        story = GeneratedStory.model_validate(parsed)
        validate_story(story, generation_input(moment, evidence, timing))
        return story


class OllamaStoryProvider:
    name = "ollama-qwen3"

    def __init__(self, settings: Settings):
        self.settings = settings
        self.name = f"ollama:{settings.ollama_model}"

    def generate(self, moment: dict, evidence: list[dict], timing: list[dict]) -> GeneratedStory:
        response = httpx.post(
            f"{self.settings.ollama_base_url.rstrip('/')}/api/chat",
            json={
                "model": self.settings.ollama_model,
                "stream": False,
                "format": "json",
                "messages": messages_for(generation_input(moment, evidence, timing)),
                "options": {"temperature": 0, "num_predict": self.settings.generation_max_tokens},
            },
            timeout=60,
        )
        response.raise_for_status()
        story = GeneratedStory.model_validate_json(response.json()["message"]["content"])
        validate_story(story, generation_input(moment, evidence, timing))
        return story


def select_provider(settings: Settings) -> StoryProvider:
    if settings.provider_mode == "fireworks" or (settings.provider_mode == "auto" and settings.fireworks_api_key):
        return FireworksStoryProvider(settings)
    if settings.provider_mode == "ollama":
        return OllamaStoryProvider(settings)
    return LocalStoryProvider()
