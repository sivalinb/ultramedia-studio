import json

import pytest

from ultramedia.training import validate_saved_evaluation


def test_resume_rejects_changed_decoding_and_missing_receipts(tmp_path):
    selected = [{"id": "case-1", "content_sha256": "case-digest"}]
    expected = {"max_new_tokens": 1024, "compute_dtype": "torch.float16"}
    (tmp_path / "report.json").write_text(
        json.dumps({"identity": expected, "dataset_sha256": "dataset-digest", "cases": 1})
    )
    (tmp_path / "predictions.jsonl").write_text(json.dumps(selected[0]) + "\n")
    (tmp_path / "token-receipts.jsonl").write_text('{"id":"case-1"}\n')
    (tmp_path / "gpu-memory.json").write_text("{}")
    validate_saved_evaluation(tmp_path, selected, "dataset-digest", expected)
    with pytest.raises(ValueError, match="decoding settings"):
        validate_saved_evaluation(tmp_path, selected, "dataset-digest", {**expected, "max_new_tokens": 512})
    with pytest.raises(ValueError, match="different test data"):
        validate_saved_evaluation(tmp_path, selected, "changed-dataset", expected)
    (tmp_path / "token-receipts.jsonl").write_text("")
    with pytest.raises(ValueError, match="receipts are incomplete"):
        validate_saved_evaluation(tmp_path, selected, "dataset-digest", expected)
