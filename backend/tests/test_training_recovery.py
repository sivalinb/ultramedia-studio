"""Recovery archives must retain both optimizer state and the selected best adapter."""

import json
import zipfile
from types import SimpleNamespace

import pytest

pytest.importorskip("transformers")

from ultramedia.training import recovery_callback


def test_recovery_archive_can_resume_without_losing_best_checkpoint(tmp_path):
    run = tmp_path / "run"
    for step in [50, 55]:
        checkpoint = run / "checkpoints" / f"checkpoint-{step}"
        checkpoint.mkdir(parents=True)
        (checkpoint / "adapter_model.safetensors").write_bytes(f"adapter-{step}".encode())
        (checkpoint / "optimizer.pt").write_bytes(f"optimizer-{step}".encode())
        (checkpoint / "trainer_state.json").write_text(json.dumps({"global_step": step}))
    (run / "experiment.json").write_text('{"seed":42}')
    state = SimpleNamespace(
        global_step=55,
        max_steps=100,
        epoch=1.1,
        log_history=[{"loss": 0.5}],
        best_model_checkpoint=str(run / "checkpoints/checkpoint-50"),
    )
    args = SimpleNamespace(output_dir=str(run / "checkpoints"))
    control = SimpleNamespace(should_save=False)
    callback = recovery_callback(run, 5)
    callback.on_step_end(args, state, control)
    assert control.should_save
    callback.on_log(args, state, control, logs={"loss": 0.5})
    callback.on_save(args, state, control)
    with zipfile.ZipFile(tmp_path / "run-recovery.zip") as bundle:
        assert bundle.testzip() is None
        assert bundle.read("checkpoints/checkpoint-55/optimizer.pt") == b"optimizer-55"
        assert bundle.read("checkpoints/checkpoint-50/adapter_model.safetensors") == b"adapter-50"
        assert json.loads(bundle.read("progress.json"))["global_step"] == 55
        assert json.loads(bundle.read("experiment.json"))["seed"] == 42
    assert not list(tmp_path.glob("*.tmp"))
