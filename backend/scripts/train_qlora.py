import argparse
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser(description="QLoRA fine-tune Qwen3 for UltraMedia's editorial style")
    parser.add_argument("--model", default="Qwen/Qwen3-4B-Instruct-2507")
    parser.add_argument("--train", type=Path, default=Path("training_data/train.jsonl"))
    parser.add_argument("--validation", type=Path, default=Path("training_data/validation.jsonl"))
    parser.add_argument("--output", type=Path, default=Path("artifacts/qwen3-ultramedia-lora"))
    args = parser.parse_args()
    try:
        import torch
        from datasets import load_dataset
        from peft import LoraConfig
        from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig
        from trl import SFTConfig, SFTTrainer
    except ImportError as error:
        raise SystemExit("Install the fine-tuning extra: pip install -e '.[finetune]'") from error

    quantization = BitsAndBytesConfig(
        load_in_4bit=True,
        bnb_4bit_quant_type="nf4",
        bnb_4bit_compute_dtype=torch.bfloat16,
        bnb_4bit_use_double_quant=True,
    )
    model = AutoModelForCausalLM.from_pretrained(
        args.model,
        device_map="auto",
        quantization_config=quantization,
        trust_remote_code=False,
    )
    tokenizer = AutoTokenizer.from_pretrained(args.model, trust_remote_code=False)
    dataset = load_dataset(
        "json",
        data_files={"train": str(args.train), "validation": str(args.validation)},
    )
    peft_config = LoraConfig(
        r=16,
        lora_alpha=32,
        lora_dropout=0.05,
        target_modules=["q_proj", "k_proj", "v_proj", "o_proj", "gate_proj", "up_proj", "down_proj"],
        task_type="CAUSAL_LM",
    )
    training_config = SFTConfig(
        output_dir=str(args.output),
        num_train_epochs=2,
        per_device_train_batch_size=2,
        gradient_accumulation_steps=8,
        learning_rate=2e-4,
        warmup_ratio=0.05,
        eval_strategy="steps",
        eval_steps=50,
        save_steps=50,
        logging_steps=10,
        bf16=True,
        max_length=2048,
        report_to="none",
        seed=42,
    )
    trainer = SFTTrainer(
        model=model,
        args=training_config,
        train_dataset=dataset["train"],
        eval_dataset=dataset["validation"],
        peft_config=peft_config,
        processing_class=tokenizer,
    )
    trainer.train()
    trainer.save_model(str(args.output))
    tokenizer.save_pretrained(str(args.output))


if __name__ == "__main__":
    main()
