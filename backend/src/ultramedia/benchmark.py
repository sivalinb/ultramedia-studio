"""Model-agnostic held-out evaluation. Preserve failures and complete predictions."""

import argparse
import json
import platform
import statistics
import time
from collections import defaultdict
from datetime import UTC, datetime
from pathlib import Path
from random import Random

from .contracts import GeneratedStory, assess_story, canonical
from .dataset import load_dataset_records, sha

METRICS = (
    "schema_valid",
    "citation_ids_valid",
    "structured_claims_supported",
    "required_metric_covered",
    "disposition_correct",
    "numeric_tokens_supported",
    "sensitive_language_absent",
    "projection_not_achievement",
    "automatic_success",
)


def percentile(values, q):
    return sorted(values)[min(len(values) - 1, max(0, int(len(values) * q + 0.999999) - 1))] if values else None


def evaluate(rows, generate, identity, dataset_manifest, output: Path):
    if output.exists():
        raise ValueError(f"Evidence directory already exists; use a new run name: {output}")
    predictions = []
    started = time.perf_counter()
    for row in rows:
        begin = time.perf_counter()
        prediction = {
            "id": row["id"],
            "group_id": row["group_id"],
            "content_sha256": row["content_sha256"],
            "signal": row["inputs"]["moment"]["signal_type"],
            "condition": row["provenance"].get("condition"),
            "metrics": {key: False for key in METRICS},
            "raw_output": None,
            "output": None,
        }
        try:
            raw = generate(row["inputs"])
            prediction["raw_output"] = raw
            story = (
                GeneratedStory.model_validate_json(raw) if isinstance(raw, str) else GeneratedStory.model_validate(raw)
            )
            checks = assess_story(story, row["inputs"])
            prediction["output"] = story.model_dump()
            prediction["metrics"] = {key: bool(checks.get(key, False)) for key in METRICS}
            prediction["metrics"]["schema_valid"] = True
            prediction["metrics"]["automatic_success"] = checks["automatic_checks_passed"]
        except Exception as error:
            prediction["error_type"] = type(error).__name__
            # Dataset is explicitly curated/public; arbitrary provider exception bodies stay excluded.
        prediction["duration_ms"] = round((time.perf_counter() - begin) * 1000, 3)
        predictions.append(prediction)
    if not predictions:
        raise ValueError("No evaluation cases")

    def rates(items):
        return {key: sum(p["metrics"][key] for p in items) / len(items) for key in METRICS}

    duration = time.perf_counter() - started
    report = {
        "schema_version": "week5-evaluation-v1",
        "created_at": datetime.now(UTC).isoformat(),
        "identity": identity,
        "dataset_sha256": dataset_manifest["dataset_sha256"],
        "cases": len(predictions),
        "case_set_sha256": sha(canonical([p["id"] for p in predictions])),
        "metrics": rates(predictions),
        "by_signal": {},
        "by_condition": {},
        "latency_ms": {
            "p50": statistics.median(p["duration_ms"] for p in predictions),
            "p95": percentile([p["duration_ms"] for p in predictions], 0.95),
        },
        "wall_seconds": duration,
        "environment": {"platform": platform.platform(), "python": platform.python_version()},
        "semantic_faithfulness": None,
        "editor_preference": None,
        "quality_scope": "Structured evidence checks; not human semantic accuracy or real-race generalization",
        "release_decision": "not_a_promotion_test",
    }
    for field in ("signal", "condition"):
        for value in sorted({p[field] or "unspecified" for p in predictions}):
            selected = [p for p in predictions if (p[field] or "unspecified") == value]
            report[f"by_{field}"][value] = {"cases": len(selected), **rates(selected)}
    output.mkdir(parents=True)
    (output / "predictions.jsonl").write_text("".join(canonical(p) + "\n" for p in predictions), encoding="utf-8")
    (output / "report.json").write_text(json.dumps(report, indent=2) + "\n")
    return report, predictions


def compare_runs(base_dir: Path, adapter_dir: Path, output: Path):
    reports = [json.loads((d / "report.json").read_text()) for d in (base_dir, adapter_dir)]
    for field in ("dataset_sha256", "case_set_sha256"):
        if reports[0][field] != reports[1][field]:
            raise ValueError(f"Comparison mismatch: {field}")
    for field in ("base_model", "revision", "quantization", "prompt_version", "max_new_tokens"):
        if reports[0]["identity"].get(field) != reports[1]["identity"].get(field):
            raise ValueError(f"Uncontrolled comparison: {field}")
    predictions = [
        [json.loads(line) for line in (d / "predictions.jsonl").read_text().splitlines()]
        for d in (base_dir, adapter_dir)
    ]
    groups = defaultdict(list)
    blind = []
    key = []
    rng = Random(42)
    for base, adapter in zip(*predictions, strict=True):
        if base["id"] != adapter["id"] or base["content_sha256"] != adapter["content_sha256"]:
            raise ValueError("Prediction alignment mismatch")
        delta = int(adapter["metrics"]["automatic_success"]) - int(base["metrics"]["automatic_success"])
        groups[base["group_id"]].append(delta)
        flipped = rng.choice([True, False])
        candidates = [base["output"], adapter["output"]]
        if flipped:
            candidates.reverse()
        blind.append(
            {
                "id": base["id"],
                "A": candidates[0],
                "B": candidates[1],
                "preferred": None,
                "reviewer": None,
                "claim_support": None,
                "rationale": None,
            }
        )
        key.append({"id": base["id"], "A": "adapter" if flipped else "base"})
    group_values = list(groups.values())
    boot = []
    for _ in range(1000):
        sample = [v for _ in group_values for v in rng.choice(group_values)]
        boot.append(statistics.mean(sample))
    result = {
        "base": reports[0],
        "adapter": reports[1],
        "automatic_success_delta": reports[1]["metrics"]["automatic_success"]
        - reports[0]["metrics"]["automatic_success"],
        "paired_group_bootstrap_95_interval": [percentile(boot, 0.025), percentile(boot, 0.975)],
        "human_review_complete": False,
        "release_decision": "blocked_pending_human_review",
        "note": "Synthetic experiment cannot authorize production. Inspect all regressions and blind editor review.",
    }
    output.mkdir(parents=True, exist_ok=False)
    for name, content in (("comparison.json", result), ("blind-review.json", blind), ("review-key.json", key)):
        (output / name).write_text(json.dumps(content, indent=2) + "\n")
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dataset", type=Path, default=Path("week5/data/synthetic"))
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--split", choices=["validation", "test"], default="test")
    args = parser.parse_args()
    rows, manifest = load_dataset_records(args.dataset)
    from .providers import LocalStoryProvider

    provider = LocalStoryProvider()
    report, _ = evaluate(
        [r for r in rows if r["split"] == args.split],
        lambda inputs: provider.generate(**inputs).model_dump(),
        {"provider": provider.name, "kind": "deterministic_rules", "split": args.split},
        manifest,
        args.output,
    )
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
