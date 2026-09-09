import argparse
import json
from pathlib import Path

from ultramedia.contracts import MODEL_ID, MODEL_REVISION
from ultramedia.training import sha_bytes


def main() -> None:
    parser = argparse.ArgumentParser(description="Merge an UltraMedia LoRA adapter into the base model")
    parser.add_argument("--model", default=MODEL_ID)
    parser.add_argument("--adapter", type=Path, default=Path("artifacts/qwen3-ultramedia-lora"))
    parser.add_argument("--output", type=Path, default=Path("artifacts/qwen3-ultramedia-merged"))
    args = parser.parse_args()
    try:
        from peft import PeftModel
        from transformers import AutoModelForCausalLM, AutoTokenizer
    except ImportError as error:
        raise SystemExit("Install the fine-tuning extra: pip install -e '.[finetune]'") from error
    if args.output.exists():
        raise ValueError("Merge output exists; choose a new directory")
    run = json.loads((args.adapter.parent / "training-run.json").read_text())
    if run["base_model"] != args.model or run["revision"] != MODEL_REVISION:
        raise ValueError("Adapter/base model lineage mismatch")
    for name, digest in run["adapter_files_sha256"].items():
        if sha_bytes(args.adapter / name) != digest:
            raise ValueError(f"Adapter checksum mismatch: {name}")
    base = AutoModelForCausalLM.from_pretrained(
        args.model, revision=MODEL_REVISION, device_map="cpu", torch_dtype="auto"
    )
    merged = PeftModel.from_pretrained(base, str(args.adapter)).merge_and_unload()
    merged.save_pretrained(str(args.output), safe_serialization=True)
    AutoTokenizer.from_pretrained(str(args.adapter)).save_pretrained(str(args.output))
    (args.output / "merge-manifest.json").write_text(
        json.dumps(
            {
                "base_model": args.model,
                "revision": MODEL_REVISION,
                "dataset_sha256": run["dataset_sha256"],
                "source_adapter_sha256": run["adapter_files_sha256"],
                "production_promoted": False,
                "note": "Re-evaluate after conversion/quantization before selecting this model.",
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
