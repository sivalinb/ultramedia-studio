"""Validate pinned TRL/PEFT plumbing using a tiny random CPU model, not Qwen weights."""
import json
from pathlib import Path
import torch
from datasets import Dataset
from peft import LoraConfig
from transformers import AutoModelForCausalLM, AutoTokenizer, Qwen3Config
from trl import SFTConfig, SFTTrainer
from ultramedia.contracts import MODEL_ID, MODEL_REVISION
from ultramedia.dataset import load_dataset_records
from ultramedia.training import training_records
from tempfile import TemporaryDirectory

ROOT = Path(__file__).resolve().parents[2]
rows, manifest = load_dataset_records(ROOT / 'week5/data/synthetic')
tokenizer = AutoTokenizer.from_pretrained(MODEL_ID, revision=MODEL_REVISION, local_files_only=True)
tokenizer.pad_token = tokenizer.eos_token
config = Qwen3Config(vocab_size=len(tokenizer), hidden_size=32, intermediate_size=64, num_hidden_layers=1,
                    num_attention_heads=2, num_key_value_heads=1, head_dim=16, max_position_embeddings=2048)
model = AutoModelForCausalLM.from_config(config)
with TemporaryDirectory() as directory:
    trainer = SFTTrainer(model=model, processing_class=tokenizer,
        train_dataset=Dataset.from_list(training_records(rows, 'train')[:4]),
        eval_dataset=Dataset.from_list(training_records(rows, 'validation')[:2]),
        args=SFTConfig(output_dir=directory, max_length=2048, completion_only_loss=True,
                       eval_strategy='epoch', save_strategy='epoch', load_best_model_at_end=True,
                       metric_for_best_model='eval_loss', greater_is_better=False, use_cpu=True,
                       bf16=False, fp16=False, report_to='none', packing=False),
        peft_config=LoraConfig(r=16, lora_alpha=32, lora_dropout=.05, task_type='CAUSAL_LM',
            target_modules=['q_proj','k_proj','v_proj','o_proj','gate_proj','up_proj','down_proj']))
    feature = trainer.train_dataset[0]
    batch = trainer.data_collator([feature])
    labels = batch['labels'][0]
    masked, supervised = int((labels == -100).sum()), int((labels != -100).sum())
    assert masked > 0 and supervised > 0
    completion_mask = torch.tensor(feature['completion_mask'], dtype=torch.bool)
    assert torch.all(labels[:len(completion_mask)][~completion_mask] == -100)
    result = {'status':'passed', 'dataset_sha256':manifest['dataset_sha256'], 'device':'cpu',
              'model':'random tiny Qwen3 architecture; not pretrained target weights',
              'training_executed':False, 'masked_tokens':masked, 'supervised_tokens':supervised,
              'prompt_positions_all_masked':True, 'validation_schedule':'epoch',
              'scope':'Pinned API, PEFT target modules, dataset formatting, and actual TRL collator only'}
    (ROOT/'week5/evidence/training-api-validation.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))
