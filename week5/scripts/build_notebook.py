"""Regenerate the portable notebook; no stored outputs or invented training results."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
cells = []
def md(text):
    cells.append({'cell_type': 'markdown', 'metadata': {}, 'source': text.splitlines(True)})
def code(text):
    cells.append({'cell_type': 'code', 'metadata': {}, 'source': text.splitlines(True), 'execution_count': None, 'outputs': []})

md('''# UltraMedia · Week 5 QLoRA experiment

**Research question:** does a specialized Qwen3-4B model produce more consistent, evidence-supported race briefs than the same base model with an optimized prompt and frozen retrieval?

This notebook runs on **Colab or Kaggle with a CUDA GPU** and internet enabled. It downloads model weights and trains an actual adapter. The bundled 600 examples are **synthetic, automatically checked, and not human-approved**. Their shared templates limit generalization. Training does not authorize production use. No GPU result has been prefilled.

Start with a fresh Python 3.11/3.12 runtime. In Colab choose Runtime → Change runtime type → GPU. In Kaggle enable GPU and Internet. Upload `ultramedia-week5-source.zip` (or attach it as a Kaggle dataset). Run cells in order. Save the result archive before the session ends; hosted sessions and accelerator quotas are not guaranteed.
''')
code('''from pathlib import Path
import sys, zipfile, subprocess, os, json, datetime
ZIP_PATH = ""  # Optional: exact path to the supplied source archive.
if ZIP_PATH:
    archive = Path(ZIP_PATH)
else:
    candidates = list(Path('/kaggle/input').rglob('ultramedia-week5-source.zip')) if Path('/kaggle/input').exists() else []
    if candidates:
        archive = candidates[0]
    else:
        from google.colab import files
        uploaded = files.upload()
        archive = Path(next(name for name in uploaded if name.endswith('.zip')))
work = Path('/kaggle/working' if Path('/kaggle/working').exists() else '/content') / 'ultramedia-week5'
work.mkdir(parents=True, exist_ok=True)
with zipfile.ZipFile(archive) as bundle:
    for member in bundle.infolist():
        if not (work / member.filename).resolve().is_relative_to(work.resolve()):
            raise ValueError('Unsafe archive path')
    bundle.extractall(work)
ROOT = work / 'ultramedia-studio'
assert (ROOT / 'week5/requirements-gpu.txt').exists(), 'Select the supplied UltraMedia source archive.'
os.chdir(ROOT)
subprocess.run([sys.executable, '-m', 'pip', 'install', '-r', 'week5/requirements-gpu.txt'], check=True)
sys.path.insert(0, str(ROOT / 'backend/src'))
os.environ['PYTHONPATH'] = str(ROOT / 'backend/src')
print('Source ready:', ROOT)
''')
md('''## Verify the GPU, data, and frozen experiment settings

The code selects BF16 only when supported, otherwise FP16. A T4 commonly needs FP16. If memory is insufficient, first reduce sequence length only after the token audit; do not silently cut target responses. The default microbatch is one with eight accumulation steps. Choose training settings before viewing test results.
''')
code('''import torch
from ultramedia.dataset import load_dataset_records, check_training_gate
from ultramedia.contracts import MODEL_ID, MODEL_REVISION
from ultramedia.training import check_sequence_lengths
from transformers import AutoTokenizer
assert torch.cuda.is_available(), 'Enable a CUDA GPU runtime before continuing.'
DATASET = ROOT / 'week5/data/synthetic'
rows, manifest = load_dataset_records(DATASET)
check_training_gate(rows, manifest, research=True)
print(torch.cuda.get_device_name(0), 'VRAM GiB:', round(torch.cuda.get_device_properties(0).total_memory / 2**30, 2))
print(json.dumps(manifest['audit'], indent=2))
tokenizer = AutoTokenizer.from_pretrained(MODEL_ID, revision=MODEL_REVISION)
print(check_sequence_lengths(rows, tokenizer, 2048))
CONFIG = {'epochs': 2, 'max_length': 2048, 'max_new_tokens': 1024, 'seed': 42}
RUN = ROOT / 'week5/runs' / datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%SZ')
print('Run:', RUN, '\\nSettings:', CONFIG)
''')
md('''## Inspect training examples and the controls

Review only training examples here. The 120 test examples are grouped into 30 unseen fictional race episodes. No race group crosses splits. This does not make the shared templates or vocabulary independent. An additional expert-authored real-world test set remains necessary for a production claim.

The strongest control is the **same Qwen model, revision, NF4 quantization, optimized system prompt, evidence, token limit, and greedy decoding** with the adapter absent. The rule baseline is separately labeled. Primary model evidence is structured correctness and paired editor preference, not similarity to a synthetic target sentence.
''')
code('''for condition in ['complete', 'missing', 'contradictory', 'misleading_hint', 'boundary']:
    row = next(r for r in rows if r['split'] == 'train' and r['provenance']['condition'] == condition)
    print(condition, json.dumps({'input': row['inputs'], 'target': row['output']}, indent=2))
''')
md('''## Train QLoRA

This cell performs real training. It checks completion-only loss masking, evaluates each epoch, selects the best validation-loss checkpoint, and saves weights, tokenizer, exact configuration, package versions, curves, dataset hash, training duration, and peak VRAM. Checkpoints may consume several GB. Keep the results even when quality does not improve.
''')
code('''subprocess.run([sys.executable, '-m', 'ultramedia.training', 'train', '--dataset', str(DATASET),
                '--output', str(RUN), '--research-synthetic', '--epochs', str(CONFIG['epochs']),
                '--max-length', str(CONFIG['max_length'])], check=True)
training = json.loads((RUN / 'training-run.json').read_text())
print({k: training[k] for k in ['status', 'trainable_parameters', 'training_seconds', 'peak_allocated_vram_bytes', 'first_example_loss_mask']})
''')
md('''## Run the frozen held-out comparison

This loads the base and adapted models sequentially to avoid holding both in GPU memory. All 120 test cases are run for each. Invalid JSON, unsupported claims, bad citations and generation errors stay in the denominator. Full predictions, token counts, termination reason, latency and GPU memory are saved. Do not use the resulting test errors to tune and re-report the same test as untouched.
''')
code('''subprocess.run([sys.executable, '-m', 'ultramedia.training', 'evaluate', '--dataset', str(DATASET),
                '--run', str(RUN), '--max-new-tokens', str(CONFIG['max_new_tokens'])], check=True)
comparison = json.loads((RUN / 'comparison/comparison.json').read_text())
for variant in ['base', 'adapter']:
    print(variant, json.dumps(comparison[variant]['metrics'], indent=2))
print('Paired delta:', comparison['automatic_success_delta'])
print('Group-bootstrap interval:', comparison['paired_group_bootstrap_95_interval'])
print('Release decision:', comparison['release_decision'])
''')
md('''## Plot measured results and conduct blind editorial review

Compare full factual support, clarity, useful brevity, and revision effort. Give the reviewer `blind-review.json` and `review-inputs.jsonl`, keeping `review-key.json` separate until review is complete. Complete preferred=A/B/tie/neither, reviewer, claim_support, and rationale for every case. Do not invent reviews or treat automated checks as human judgment. A syntactically valid number can still modify the wrong noun.
''')
code('''import matplotlib.pyplot as plt
history = training['history']
fig, axes = plt.subplots(1, 2, figsize=(12, 4))
for metric in ['loss', 'eval_loss']:
    points = [(r.get('epoch', 0), r[metric]) for r in history if metric in r]
    if points:
        axes[0].plot(*zip(*points), marker='o', label=metric)
axes[0].set(xlabel='Epoch', ylabel='Loss', title='Measured training and validation loss')
axes[0].legend()
metrics = ['schema_valid', 'structured_claims_supported', 'disposition_correct', 'automatic_success']
for i, variant in enumerate(['base', 'adapter']):
    axes[1].bar([n + i * .4 for n in range(len(metrics))], [comparison[variant]['metrics'][m] for m in metrics], width=.4, label=variant)
axes[1].set_xticks([n + .2 for n in range(len(metrics))], metrics, rotation=25, ha='right')
axes[1].set(ylim=(0, 1.05), ylabel='Fraction of all test cases', title='Automatic checks; semantic review pending')
axes[1].legend(); fig.tight_layout(); fig.savefig(RUN / 'measured-results.png', dpi=160)
plt.show()
''')
md('''## Optional: merge and export for local serving

Run this separately after downloading your adapter. Merging full weights needs substantial system RAM and disk. Follow `week5/SERVING.md` to convert both base and adapted weights with the same pinned llama.cpp revision and quantization, then re-evaluate them. NF4 training comparison and GGUF serving comparison are different experiments. Keep the base model available for rollback.

```bash
PYTHONPATH=backend/src python backend/scripts/merge_adapter.py --adapter week5/runs/RUN/adapter --output week5/runs/RUN/merged
```
''')
md('''## Download your evidence

The compact archive contains the adapter, metrics, raw predictions, configuration, curves and review forms. Intermediate checkpoints are excluded. It is an actual-run artifact only after the training and evaluation cells succeed. The source submission package alone is not proof that the model was trained.
''')
code('''destination = RUN.parent / (RUN.name + '-results.zip')
with zipfile.ZipFile(destination, 'w', zipfile.ZIP_DEFLATED) as bundle:
    for path in RUN.rglob('*'):
        if path.is_file() and 'checkpoints' not in path.relative_to(RUN).parts and 'merged' not in path.relative_to(RUN).parts:
            bundle.write(path, Path(RUN.name) / path.relative_to(RUN))
print('Saved:', destination)
try:
    from google.colab import files
    files.download(str(destination))
except ImportError:
    from IPython.display import FileLink, display
    display(FileLink(str(destination)))
''')
notebook = {'cells': cells, 'metadata': {'kernelspec': {'display_name': 'Python 3', 'language': 'python', 'name': 'python3'},
    'language_info': {'name': 'python', 'version': '3.12'}, 'accelerator': 'GPU'}, 'nbformat': 4, 'nbformat_minor': 5}
for i, cell in enumerate(cells):
    cell['id'] = f'week5-{i:02d}'
(ROOT / 'week5/notebooks/UltraMedia_Week5_QLoRA.ipynb').write_text(json.dumps(notebook, indent=2) + '\n')
