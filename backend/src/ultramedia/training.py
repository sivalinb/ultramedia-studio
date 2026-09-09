"""GPU-only reproducible PEFT experiment; imported without GPU dependencies by tests."""

import argparse
import importlib.metadata
import json
import platform
import time
import zipfile
from pathlib import Path

from .contracts import MODEL_ID, MODEL_REVISION, PROMPT_VERSION, canonical, messages_for
from .dataset import check_training_gate, load_dataset_records


def training_records(rows, split):
    return [
        {"prompt": row["messages"][:-1], "completion": row["messages"][-1:]} for row in rows if row["split"] == split
    ]


def check_sequence_lengths(rows, tokenizer, max_length):
    lengths = [len(tokenizer.apply_chat_template(row["messages"], tokenize=True)) for row in rows]
    if max(lengths) > max_length:
        raise ValueError(
            f"Longest example has {max(lengths)} tokens, exceeding {max_length}; do not silently truncate targets"
        )
    return {
        "examples": len(lengths),
        "min_tokens": min(lengths),
        "max_tokens": max(lengths),
        "mean_tokens": sum(lengths) / len(lengths),
    }


def environment(torch):
    names = ("torch", "transformers", "trl", "peft", "datasets", "accelerate", "bitsandbytes")
    return {
        "python": platform.python_version(),
        "packages": {n: importlib.metadata.version(n) for n in names},
        "gpu": torch.cuda.get_device_name(0),
        "cuda": torch.version.cuda,
        "vram_bytes": torch.cuda.get_device_properties(0).total_memory,
    }


def recovery_callback(run_dir, every_steps):
    """Preserve resumable checkpoints without changing epoch validation selection."""
    from transformers import TrainerCallback

    class Recovery(TrainerCallback):
        def on_step_end(self, args, state, control, **kwargs):
            if every_steps and state.global_step % every_steps == 0:
                control.should_save = True
            return control

        def on_log(self, args, state, control, logs=None, **kwargs):
            progress = {
                "global_step": state.global_step,
                "max_steps": state.max_steps,
                "epoch": state.epoch,
                "history": state.log_history,
            }
            temporary = run_dir / "progress.json.tmp"
            temporary.write_text(json.dumps(progress, indent=2, default=str) + "\n")
            temporary.replace(run_dir / "progress.json")
            print(json.dumps({"training_progress": state.global_step, "metrics": logs}), flush=True)

        def on_save(self, args, state, control, **kwargs):
            checkpoint = Path(args.output_dir) / f"checkpoint-{state.global_step}"
            checkpoints = {checkpoint}
            if state.best_model_checkpoint:
                checkpoints.add(Path(state.best_model_checkpoint))
            destination = run_dir.parent / (run_dir.name + "-recovery.zip")
            temporary = destination.with_suffix(".zip.tmp")
            with zipfile.ZipFile(temporary, "w", zipfile.ZIP_DEFLATED) as bundle:
                for directory in sorted(checkpoints):
                    for path in sorted(directory.rglob("*")):
                        if path.is_file():
                            bundle.write(path, path.relative_to(run_dir))
                for name in ["experiment.json", "progress.json"]:
                    if (run_dir / name).exists():
                        bundle.write(run_dir / name, name)
            temporary.replace(destination)
            print(
                json.dumps(
                    {
                        "recovery_checkpoint": state.global_step,
                        "archive": str(destination),
                        "bytes": destination.stat().st_size,
                    }
                ),
                flush=True,
            )

    return Recovery()


def run(args):
    if args.epochs < 1 or args.max_length < 256:
        raise ValueError("Use at least one epoch and a sequence limit of at least 256 tokens")
    if getattr(args, "checkpoint_steps", 5) < 0:
        raise ValueError("Checkpoint interval must be non-negative")
    rows, manifest = load_dataset_records(args.dataset)
    check_training_gate(rows, manifest, args.research_synthetic)
    import torch
    from datasets import Dataset
    from peft import LoraConfig
    from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig, set_seed
    from trl import SFTConfig, SFTTrainer

    if not torch.cuda.is_available():
        raise RuntimeError("CUDA GPU required. Run the supplied notebook on Colab/Kaggle with GPU enabled.")
    identity = {
        "base_model": MODEL_ID,
        "revision": MODEL_REVISION,
        "dataset_sha256": manifest["dataset_sha256"],
        "epochs": args.epochs,
        "max_length": args.max_length,
        "seed": 42,
        "prompt_version": PROMPT_VERSION,
    }
    resume = getattr(args, "resume_from_checkpoint", None)
    if resume:
        resume = resume.resolve()
        if resume.parent != (args.output / "checkpoints").resolve() or not (resume / "trainer_state.json").is_file():
            raise ValueError("Resume from a complete checkpoint inside this run's checkpoints directory")
        if json.loads((args.output / "experiment.json").read_text()) != identity:
            raise ValueError("Resume configuration or dataset differs from the original experiment")
    elif args.output.exists():
        raise ValueError("Run directory exists. Choose a new output name to preserve previous evidence.")
    else:
        args.output.mkdir(parents=True)
        (args.output / "experiment.json").write_text(json.dumps(identity, indent=2) + "\n")
    set_seed(42)
    bf16 = torch.cuda.is_bf16_supported()
    dtype = torch.bfloat16 if bf16 else torch.float16
    tokenizer = AutoTokenizer.from_pretrained(MODEL_ID, revision=MODEL_REVISION)
    tokenizer.pad_token = tokenizer.eos_token
    lengths = check_sequence_lengths(rows, tokenizer, args.max_length)
    quant = BitsAndBytesConfig(
        load_in_4bit=True, bnb_4bit_quant_type="nf4", bnb_4bit_use_double_quant=True, bnb_4bit_compute_dtype=dtype
    )
    model = AutoModelForCausalLM.from_pretrained(
        MODEL_ID, revision=MODEL_REVISION, quantization_config=quant, torch_dtype=dtype, device_map={"": 0}
    )
    model.config.use_cache = False
    config = SFTConfig(
        output_dir=str(args.output / "checkpoints"),
        num_train_epochs=args.epochs,
        per_device_train_batch_size=1,
        per_device_eval_batch_size=1,
        gradient_accumulation_steps=8,
        learning_rate=2e-4,
        warmup_ratio=0.05,
        lr_scheduler_type="cosine",
        max_length=args.max_length,
        eval_strategy="epoch",
        save_strategy="epoch",
        logging_steps=5,
        save_total_limit=2,
        load_best_model_at_end=True,
        metric_for_best_model="eval_loss",
        greater_is_better=False,
        bf16=bf16,
        fp16=not bf16,
        gradient_checkpointing=True,
        gradient_checkpointing_kwargs={"use_reentrant": False},
        optim="paged_adamw_8bit",
        completion_only_loss=True,
        packing=False,
        seed=42,
        data_seed=42,
        report_to="none",
    )
    trainer = SFTTrainer(
        model=model,
        processing_class=tokenizer,
        args=config,
        train_dataset=Dataset.from_list(training_records(rows, "train")),
        eval_dataset=Dataset.from_list(training_records(rows, "validation")),
        peft_config=LoraConfig(
            r=16,
            lora_alpha=32,
            lora_dropout=0.05,
            bias="none",
            task_type="CAUSAL_LM",
            target_modules=["q_proj", "k_proj", "v_proj", "o_proj", "gate_proj", "up_proj", "down_proj"],
        ),
        callbacks=[recovery_callback(args.output, getattr(args, "checkpoint_steps", 5))],
    )
    # Check the actual trainer collator, not just a configuration flag.
    batch = trainer.data_collator([trainer.train_dataset[0]])
    labels = batch["labels"][0]
    masked, supervised = int((labels == -100).sum()), int((labels != -100).sum())
    if not masked or not supervised:
        raise ValueError("Expected both masked prompt tokens and supervised assistant tokens")
    env = environment(torch)
    trainable = sum(p.numel() for p in trainer.model.parameters() if p.requires_grad)
    torch.cuda.reset_peak_memory_stats()
    start = time.perf_counter()
    trainer.train(resume_from_checkpoint=str(resume) if resume else None)
    torch.cuda.synchronize()
    training_seconds = time.perf_counter() - start
    adapter = args.output / "adapter"
    trainer.save_model(str(adapter))
    tokenizer.save_pretrained(str(adapter))
    result = {
        "status": "trained",
        "base_model": MODEL_ID,
        "revision": MODEL_REVISION,
        "dataset_sha256": manifest["dataset_sha256"],
        "dataset_kind": manifest["kind"],
        "prompt_version": PROMPT_VERSION,
        "quantization": "NF4 double-quant",
        "seed": 42,
        "compute_dtype": str(dtype),
        "trainable_parameters": trainable,
        "training_seconds": training_seconds,
        "training_seconds_scope": "this invocation; excludes any earlier interrupted attempts",
        "resume_from_checkpoint": str(resume) if resume else None,
        "peak_allocated_vram_bytes": torch.cuda.max_memory_allocated(),
        "peak_reserved_vram_bytes": torch.cuda.max_memory_reserved(),
        "sequence_audit": lengths,
        "first_example_loss_mask": {"masked_tokens": masked, "supervised_tokens": supervised},
        "environment": env,
        "config": config.to_dict(),
        "history": trainer.state.log_history,
        "adapter_files_sha256": {p.name: sha_bytes(p) for p in adapter.iterdir() if p.is_file()},
        "production_promoted": False,
    }
    (args.output / "training-run.json").write_text(json.dumps(result, indent=2, default=str) + "\n")
    return result


def sha_bytes(path):
    import hashlib

    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def validate_saved_evaluation(directory, selected, dataset_sha256, expected):
    required = ["report.json", "predictions.jsonl", "token-receipts.jsonl", "gpu-memory.json"]
    if not all((directory / name).is_file() for name in required):
        raise ValueError(f"Incomplete saved evaluation; preserve it before retrying: {directory}")
    prior = json.loads((directory / "report.json").read_text())
    if any(prior["identity"].get(key) != value for key, value in expected.items()):
        raise ValueError("Saved evaluation has different model or decoding settings")
    if prior["dataset_sha256"] != dataset_sha256 or prior["cases"] != len(selected):
        raise ValueError("Saved evaluation has different test data")
    predictions = [json.loads(line) for line in (directory / "predictions.jsonl").read_text().splitlines()]
    if [(p["id"], p["content_sha256"]) for p in predictions] != [(r["id"], r["content_sha256"]) for r in selected]:
        raise ValueError("Saved evaluation predictions do not cover the exact test split")
    receipts = [json.loads(line) for line in (directory / "token-receipts.jsonl").read_text().splitlines()]
    if [r["id"] for r in receipts] != [r["id"] for r in selected]:
        raise ValueError("Saved token receipts are incomplete")
    json.loads((directory / "gpu-memory.json").read_text())


def evaluate_models(args):
    import gc

    import torch
    from peft import PeftModel
    from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig

    from .benchmark import compare_runs, evaluate

    rows, manifest = load_dataset_records(args.dataset)
    run_record = json.loads((args.run / "training-run.json").read_text())
    if run_record["dataset_sha256"] != manifest["dataset_sha256"]:
        raise ValueError("Training/evaluation dataset mismatch")
    for name, digest in run_record["adapter_files_sha256"].items():
        if sha_bytes(args.run / "adapter" / name) != digest:
            raise ValueError(f"Adapter checksum mismatch: {name}")
    selected = [row for row in rows if row["split"] == "test"]
    dtype = torch.bfloat16 if torch.cuda.is_bf16_supported() else torch.float16
    tokenizer = AutoTokenizer.from_pretrained(args.run / "adapter")
    for variant in ("base", "adapter"):
        directory = args.run / f"test-{variant}"
        if directory.exists() and getattr(args, "resume_evaluation", False):
            expected = {
                "base_model": MODEL_ID,
                "revision": MODEL_REVISION,
                "quantization": "NF4 double-quant",
                "compute_dtype": str(dtype),
                "prompt_version": PROMPT_VERSION,
                "max_new_tokens": args.max_new_tokens,
                "variant": variant,
                "kind": "model_inference",
                "split": "test",
                "adapter_files_sha256": run_record["adapter_files_sha256"] if variant == "adapter" else None,
            }
            validate_saved_evaluation(directory, selected, manifest["dataset_sha256"], expected)
            print(json.dumps({"reused_completed_evaluation": variant, "cases": len(selected)}), flush=True)
            continue
        quant = BitsAndBytesConfig(
            load_in_4bit=True, bnb_4bit_quant_type="nf4", bnb_4bit_use_double_quant=True, bnb_4bit_compute_dtype=dtype
        )
        model = AutoModelForCausalLM.from_pretrained(
            MODEL_ID, revision=MODEL_REVISION, quantization_config=quant, torch_dtype=dtype, device_map={"": 0}
        )
        if variant == "adapter":
            model = PeftModel.from_pretrained(model, args.run / "adapter")
        model.eval()
        torch.cuda.reset_peak_memory_stats()

        receipts = []

        def generate(inputs, active_model=model, active_receipts=receipts):
            active_receipts.append({"input_tokens": None, "output_tokens": None, "finish_reason": "error"})
            text = tokenizer.apply_chat_template(messages_for(inputs), tokenize=False, add_generation_prompt=True)
            batch = tokenizer(text, return_tensors="pt", add_special_tokens=False).to("cuda")
            with torch.inference_mode():
                generated = active_model.generate(
                    **batch, max_new_tokens=args.max_new_tokens, do_sample=False, pad_token_id=tokenizer.eos_token_id
                )
            torch.cuda.synchronize()
            completion = generated[0, batch["input_ids"].shape[1] :]
            active_receipts[-1].update(
                {
                    "input_tokens": int(batch["input_ids"].shape[1]),
                    "output_tokens": int(completion.shape[0]),
                    "finish_reason": "eos" if int(completion[-1]) == tokenizer.eos_token_id else "length",
                }
            )
            return tokenizer.decode(completion, skip_special_tokens=True)

        identity = {
            "kind": "model_inference",
            "variant": variant,
            "base_model": MODEL_ID,
            "revision": MODEL_REVISION,
            "quantization": "NF4 double-quant",
            "compute_dtype": str(dtype),
            "prompt_version": PROMPT_VERSION,
            "max_new_tokens": args.max_new_tokens,
            "adapter_files_sha256": run_record["adapter_files_sha256"] if variant == "adapter" else None,
            "environment": environment(torch),
            "split": "test",
            "retrieval": "frozen evidence packs",
        }
        evaluate(selected, generate, identity, manifest, directory)
        (directory / "token-receipts.jsonl").write_text(
            "".join(
                canonical({"id": row["id"], **receipt}) + "\n" for row, receipt in zip(selected, receipts, strict=True)
            )
        )
        (directory / "gpu-memory.json").write_text(
            json.dumps(
                {
                    "peak_allocated_bytes": torch.cuda.max_memory_allocated(),
                    "peak_reserved_bytes": torch.cuda.max_memory_reserved(),
                },
                indent=2,
            )
        )
        del generate, model
        gc.collect()
        torch.cuda.empty_cache()
    comparison_path = args.run / "comparison" / "comparison.json"
    if comparison_path.exists() and getattr(args, "resume_evaluation", False):
        result = json.loads(comparison_path.read_text())
        for variant in ["base", "adapter"]:
            if result[variant] != json.loads((args.run / f"test-{variant}" / "report.json").read_text()):
                raise ValueError("Saved comparison differs from its evaluation reports")
    else:
        result = compare_runs(args.run / "test-base", args.run / "test-adapter", args.run / "comparison")
    (args.run / "comparison" / "review-inputs.jsonl").write_text(
        "".join(canonical({"id": r["id"], "inputs": r["inputs"]}) + "\n" for r in selected)
    )
    return result


def main():
    parser = argparse.ArgumentParser()
    commands = parser.add_subparsers(dest="command", required=True)
    train = commands.add_parser("train")
    train.add_argument("--dataset", type=Path, default=Path("week5/data/synthetic"))
    train.add_argument("--output", type=Path, required=True)
    train.add_argument("--research-synthetic", action="store_true")
    train.add_argument("--epochs", type=int, default=2)
    train.add_argument("--max-length", type=int, default=2048)
    train.add_argument("--checkpoint-steps", type=int, default=5)
    train.add_argument("--resume-from-checkpoint", type=Path)
    evaluate = commands.add_parser("evaluate")
    evaluate.add_argument("--dataset", type=Path, default=Path("week5/data/synthetic"))
    evaluate.add_argument("--run", type=Path, required=True)
    evaluate.add_argument("--max-new-tokens", type=int, default=1024)
    evaluate.add_argument("--resume-evaluation", action="store_true")
    args = parser.parse_args()
    result = run(args) if args.command == "train" else evaluate_models(args)
    print(json.dumps({k: v for k, v in result.items() if k not in {"history", "config", "base", "adapter"}}, indent=2))


if __name__ == "__main__":
    main()
