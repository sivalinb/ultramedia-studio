def test_health_reports_human_gate(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["publication_mode"] == "human-gated"


def test_demo_race_is_available(client):
    response = client.get("/api/v1/races")
    assert response.status_code == 200
    assert response.json()[0]["id"] == "wser-demo"
    assert response.json()[0]["status"] == "simulation"


def test_story_generation_is_cited_and_pending(client):
    response = client.post(
        "/api/v1/stories/generate",
        json={
            "race_id": "wser-demo",
            "moment": {
                "athlete_bib": "214",
                "signal_type": "position_gain",
                "headline_hint": "Mara moved through the field in the canyon sector",
            },
        },
    )
    assert response.status_code == 201
    story = response.json()
    assert story["status"] == "pending_review"
    assert story["citations"]
    assert story["trace_id"]

    trace = client.get(f"/api/v1/traces/{story['trace_id']}")
    assert trace.status_code == 200
    assert [span["stage"] for span in trace.json()["spans"]] == [
        "moment_detector",
        "evidence_retriever",
        "story_writer",
        "fact_verifier",
        "safety_editor",
        "human_review_queue",
    ]


def test_human_can_approve_but_generation_cannot(client):
    story = client.post(
        "/api/v1/stories/generate",
        json={
            "race_id": "wser-demo",
            "moment": {
                "athlete_bib": "101",
                "signal_type": "record_watch",
                "headline_hint": "Leader maintains strong pace into Foresthill",
            },
        },
    ).json()
    reviewed = client.post(
        f"/api/v1/stories/{story['id']}/review",
        json={"decision": "approved", "reviewer": "Demo Editor", "rationale": "Facts checked"},
    )
    assert reviewed.status_code == 200
    assert reviewed.json()["status"] == "approved"


def test_unknown_athlete_fails_closed(client):
    response = client.post(
        "/api/v1/stories/generate",
        json={
            "race_id": "wser-demo",
            "moment": {
                "athlete_bib": "999",
                "signal_type": "pace_change",
                "headline_hint": "Unknown runner signal",
            },
        },
    )
    assert response.status_code == 422
    assert "No timing evidence" in response.json()["detail"]


def test_release_eval_suite_passes(client):
    response = client.post("/api/v1/evals/run")
    assert response.status_code == 200
    report = response.json()
    assert report["release_decision"] == "PASS"
    assert report["cases"] == 6
