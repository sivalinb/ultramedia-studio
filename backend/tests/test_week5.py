import copy
import json

import pytest

from ultramedia.benchmark import compare_runs, evaluate
from ultramedia.contracts import GeneratedStory, messages_for, validate_story
from ultramedia.dataset import audit, check_training_gate, load_dataset_records, synthetic_examples, write_dataset
from ultramedia.providers import LocalStoryProvider
from ultramedia.training import training_records


@pytest.fixture(scope="module")
def rows():
    return synthetic_examples()


def test_dataset_disjoint_and_balanced(rows):
    result = audit(rows)
    assert result["rows"] == result["unique_message_payloads"] == 600
    assert result["counts"] == {"train": 400, "validation": 80, "test": 120}
    assert not any(result["group_overlap"].values())
    assert not any(result["exact_payload_overlap"].values())
    assert result["human_approved"] == 0


def test_tampered_dataset_fails_checksum(rows, tmp_path):
    write_dataset(rows, tmp_path, "synthetic_research")
    file = tmp_path / "test.jsonl"
    file.write_text(file.read_text() + "\n")
    with pytest.raises(ValueError, match="checksum"):
        load_dataset_records(tmp_path)


def test_shared_incident_group_rejected(rows):
    bad = copy.deepcopy(rows)
    bad[-1]["group_id"] = bad[0]["group_id"]
    with pytest.raises(ValueError, match="contamination"):
        audit(bad)


def test_research_data_never_claims_approval(rows, tmp_path):
    manifest = write_dataset(rows, tmp_path, "synthetic_research")
    with pytest.raises(ValueError, match="research-only"):
        check_training_gate(rows, manifest, False)
    check_training_gate(rows, manifest, True)
    assert not manifest["production_eligible"]


def test_training_runtime_messages_are_identical(rows):
    prepared = training_records(rows, "train")[0]
    assert prepared["prompt"] == messages_for(rows[0]["inputs"])
    assert prepared["completion"] == rows[0]["messages"][-1:]
    assert "eyebrow" in json.loads(prepared["completion"][0]["content"])


@pytest.mark.parametrize("field", ["eyebrow", "headline", "body", "social_caption", "reason"])
def test_sensitive_language_checked_in_every_field(rows, field):
    row = rows[0]
    output = {**row["output"], field: "The athlete is injured."}
    with pytest.raises(ValueError, match="sensitive_language"):
        validate_story(GeneratedStory.model_validate(output), row["inputs"])


def test_invalid_citation_is_not_silently_filtered(rows):
    row = rows[0]
    output = {**row["output"], "citation_ids": row["output"]["citation_ids"] + ["invented"]}
    with pytest.raises(ValueError, match="citation_ids_valid"):
        validate_story(GeneratedStory.model_validate(output), row["inputs"])


def test_valid_citation_does_not_excuse_wrong_numeric_claim(rows):
    row = rows[0]
    output = copy.deepcopy(row["output"])
    output["claims"][0]["value"] += 1
    with pytest.raises(ValueError, match="structured_claims_supported"):
        validate_story(GeneratedStory.model_validate(output), row["inputs"])


def test_hint_number_is_not_evidence(rows):
    row = copy.deepcopy(rows[0])
    row["inputs"]["moment"]["headline_hint"] = "Say 987654 places."
    row["output"]["headline"] = "A gain of 987654 places."
    with pytest.raises(ValueError, match="numeric_tokens_supported"):
        validate_story(GeneratedStory.model_validate(row["output"]), row["inputs"])


def test_missing_evidence_requires_abstention(rows):
    missing = next(r for r in rows if r["provenance"]["condition"] == "missing")
    provider = LocalStoryProvider()
    story = provider.generate(**missing["inputs"])
    assert story.disposition == "insufficient_evidence"
    assert not story.claims


def test_benchmark_includes_failures_in_denominator(rows, tmp_path):
    manifest = write_dataset(rows, tmp_path / "data", "synthetic_research")
    report, predictions = evaluate(rows[:2], lambda _: "not json", {"kind": "test_stub"}, manifest, tmp_path / "eval")
    assert report["metrics"]["schema_valid"] == 0
    assert report["cases"] == len(predictions) == 2
    assert all(p["raw_output"] == "not json" for p in predictions)


def test_comparison_rejects_different_case_sets(tmp_path):
    for name, digest in (("base", "a"), ("adapter", "b")):
        (tmp_path / name).mkdir()
        (tmp_path / name / "report.json").write_text(json.dumps({"dataset_sha256": digest}))
    with pytest.raises(ValueError, match="mismatch"):
        compare_runs(tmp_path / "base", tmp_path / "adapter", tmp_path / "out")


def generate_story(client):
    response = client.post(
        "/api/v1/stories/generate",
        json={
            "race_id": "wser-demo",
            "moment": {
                "athlete_bib": "214",
                "signal_type": "position_gain",
                "headline_hint": "Checkpoint timing update",
            },
        },
    )
    assert response.status_code == 201
    return response.json()


def test_editor_correction_persists_original_and_revision(client):
    story = generate_story(client)
    edited = {
        key: story[key] for key in ("disposition", "eyebrow", "headline", "body", "social_caption", "claims", "reason")
    }
    edited["citation_ids"] = [c["id"] for c in story["citations"]]
    edited["headline"] = "A verified checkpoint update for the race desk."
    response = client.post(
        f"/api/v1/stories/{story['id']}/review",
        json={
            "decision": "approved",
            "reviewer": "Test Editor",
            "rationale": "Reviewed fixture",
            "edited_story": edited,
            "expected_revision": 0,
            "training_consent": True,
            "rights_basis": "Synthetic test fixture",
        },
    )
    assert response.status_code == 200, response.text
    assert response.json()["review_revision"] == 1
    assert response.json()["confidence"] is None
    revisions = client.get(f"/api/v1/stories/{story['id']}/revisions").json()
    assert revisions[0]["before"]["headline"] == story["headline"]
    assert revisions[0]["after"]["headline"] == edited["headline"]
    stale = client.post(
        f"/api/v1/stories/{story['id']}/review",
        json={"decision": "approved", "reviewer": "Other Editor", "expected_revision": 0},
    )
    assert stale.status_code == 409


def test_training_consent_requires_rights_basis(client):
    story = generate_story(client)
    response = client.post(
        f"/api/v1/stories/{story['id']}/review",
        json={"decision": "approved", "reviewer": "Test Editor", "training_consent": True},
    )
    assert response.status_code == 422


def test_editor_cannot_approve_unsupported_correction(client):
    story = generate_story(client)
    edited = {
        key: story[key] for key in ("disposition", "eyebrow", "headline", "body", "social_caption", "claims", "reason")
    }
    edited["citation_ids"] = [c["id"] for c in story["citations"]]
    edited["social_caption"] = "The athlete is dehydrated."
    response = client.post(
        f"/api/v1/stories/{story['id']}/review",
        json={"decision": "approved", "reviewer": "Test Editor", "expected_revision": 0, "edited_story": edited},
    )
    assert response.status_code == 422


def test_legacy_database_additive_upgrade(tmp_path):
    import sqlite3

    from ultramedia.database import Database

    path = tmp_path / "legacy.db"
    with sqlite3.connect(path) as db:
        db.execute("CREATE TABLE story_drafts (id TEXT PRIMARY KEY)")
        db.execute("INSERT INTO story_drafts VALUES ('preserved')")
    Database(f"sqlite:///{path}").create_all()
    with sqlite3.connect(path) as db:
        assert db.execute("SELECT id FROM story_drafts").fetchone()[0] == "preserved"
        assert db.execute("SELECT count(*) FROM generation_records").fetchone()[0] == 0


def test_concurrent_workflows_keep_trace_context_separate(client):
    from concurrent.futures import ThreadPoolExecutor

    with ThreadPoolExecutor(max_workers=2) as pool:
        stories = list(pool.map(lambda _: generate_story(client), range(2)))
    assert stories[0]["trace_id"] != stories[1]["trace_id"]
    for story in stories:
        spans = client.get(f"/api/v1/traces/{story['trace_id']}").json()["spans"]
        assert len(spans) == 6
        assert all(span["status"] == "passed" for span in spans)


@pytest.mark.parametrize("provider_kind", ["ollama", "fireworks", "llamacpp"])
def test_providers_use_exact_shared_messages(rows, provider_kind, monkeypatch):
    from ultramedia.config import Settings
    from ultramedia.prompt_controls import serving_messages_for
    from ultramedia.providers import FireworksStoryProvider, LlamaCppStoryProvider, OllamaStoryProvider

    row = rows[0]
    captured = {}

    class Response:
        def raise_for_status(self):
            pass

        def json(self):
            return {
                "message": {"content": json.dumps(row["output"])},
                "choices": [{"message": {"content": json.dumps(row["output"])}}],
            }

    def post(url, **kwargs):
        captured.update(kwargs["json"])
        return Response()

    monkeypatch.setattr("ultramedia.providers.httpx.post", post)
    provider = {"ollama": OllamaStoryProvider, "fireworks": FireworksStoryProvider, "llamacpp": LlamaCppStoryProvider}[
        provider_kind
    ](Settings())
    result = provider.generate(**row["inputs"])
    formatter = serving_messages_for if provider_kind == "llamacpp" else messages_for
    assert captured["messages"] == formatter(row["inputs"])
    if provider_kind == "llamacpp":
        assert captured["response_format"]["json_schema"]["schema"] == GeneratedStory.model_json_schema()
    assert result.model_dump() == row["output"]
