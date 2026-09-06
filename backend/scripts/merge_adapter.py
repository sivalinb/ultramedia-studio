import argparse
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser(description="Merge an UltraMedia LoRA adapter into the base model")
    parser.add_argument("--model", default="Qwen/Qwen3-4B-Instruct-2507")
    parser.add_argument("--adapter", type=Path, default=Path("artifacts/qwen3-ultramedia-lora"))
    parser.add_argument("--output", type=Path, default=Path("artifacts/qwen3-ultramedia-merged"))
    args = parser.parse_args()
    try:
        from peft import PeftModel
        from transformers import AutoModelForCausalLM, AutoTokenizer
    except ImportError as error:
        raise SystemExit("Install the fine-tuning extra: pip install -e '.[finetune]'") from error
    base = AutoModelForCausalLM.from_pretrained(args.model, device_map="cpu", torch_dtype="auto")
    merged = PeftModel.from_pretrained(base, str(args.adapter)).merge_and_unload()
    merged.save_pretrained(str(args.output), safe_serialization=True)
    AutoTokenizer.from_pretrained(args.model).save_pretrained(str(args.output))


if __name__ == "__main__":
    main()
