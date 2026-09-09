"""Post-hoc descriptive analysis of saved predictions; does not run or tune models.

Usage: python derive_week5_disposition_metrics.py /path/to/ultramedia-studio /path/to/output
"""
import csv
import hashlib
import json
import subprocess
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

repo, destination = map(Path, sys.argv[1:])
destination.mkdir(parents=True, exist_ok=True)
target_file = repo / "week5/data/synthetic/test.jsonl"
targets = [json.loads(line) for line in target_file.read_text().splitlines()]
assert len(targets) == len({row['id'] for row in targets}) == 120
labels = ["draft", "insufficient_evidence"]
result = {
    "analysis": "Post-hoc disposition classification, separate from frozen nine-check evaluation",
    "created_at": datetime.now(timezone.utc).isoformat(),
    "source_commit": subprocess.check_output(["git", "-C", str(repo), "rev-parse", "HEAD"], text=True).strip(),
    "scope": "120 synthetic test cases, 30 race groups; no new inference, training or human review",
    "matrix_rows": labels,
    "matrix_columns": labels + ["invalid"],
    "hashes": {str(target_file.relative_to(repo)): hashlib.sha256(target_file.read_bytes()).hexdigest()},
    "variants": {},
}
cases = []
for variant in ["base", "adapter"]:
    path = repo / f"week5/evidence/local-comparison/test-{variant}/predictions.jsonl"
    predictions = [json.loads(line) for line in path.read_text().splitlines()]
    assert len(predictions) == 120
    counts = Counter()
    for target, prediction in zip(targets, predictions):
        for key in ["id", "content_sha256", "group_id"]:
            assert target[key] == prediction[key]
        truth = target["output"]["disposition"]
        parsed = prediction.get("output") or {}
        predicted = parsed.get("disposition", "invalid")
        if predicted not in labels:
            predicted = "invalid"
        if predicted != "invalid":
            assert json.loads(prediction["raw_output"])["disposition"] == predicted
        assert bool(prediction["metrics"]["disposition_correct"]) == (truth == predicted)
        counts[truth, predicted] += 1
        cases.append({"variant": variant, "id": target["id"], "group_id": target["group_id"],
                      "content_sha256": target["content_sha256"],
                      "signal_supplied_in_input": prediction["signal"], "condition": prediction["condition"],
                      "reference": truth, "prediction": predicted, "correct": truth == predicted})
    classes = {}
    for label in labels:
        tp = counts[label, label]
        support = sum(n for (actual, predicted), n in counts.items() if actual == label)
        predicted_count = sum(n for (actual, predicted), n in counts.items() if predicted == label)
        precision = tp / predicted_count if predicted_count else 0.0
        recall = tp / support if support else 0.0
        f1 = 2 * precision * recall / (precision + recall) if precision + recall else 0.0
        classes[label] = {"precision": precision, "recall": recall, "f1": f1, "support": support}
    result["variants"][variant] = {
        "cases": len(predictions), "classes": classes,
        "accuracy": sum(counts[label, label] for label in labels) / len(predictions),
        "macro_f1": sum(row["f1"] for row in classes.values()) / len(labels),
        "confusion_matrix": [[counts[actual, predicted] for predicted in labels + ["invalid"]] for actual in labels],
    }
    result["hashes"][str(path.relative_to(repo))] = hashlib.sha256(path.read_bytes()).hexdigest()
(destination / "UltraMedia-Week5-Disposition-Analysis.json").write_text(json.dumps(result, indent=2) + "\n")
with (destination / "UltraMedia-Week5-Disposition-Cases.csv").open("w", newline="") as stream:
    writer = csv.DictWriter(stream, fieldnames=list(cases[0]), lineterminator="\n")
    writer.writeheader()
    writer.writerows(cases)
print(json.dumps(result["variants"], indent=2))
