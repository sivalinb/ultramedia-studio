"""Publish a bounded evidence snapshot; never synthesize model performance."""
import json
import hashlib
import shutil
import subprocess
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
manifest = json.loads((ROOT / 'week5/data/synthetic/manifest.json').read_text())
rows = [json.loads(line) for line in (ROOT / 'week5/data/synthetic/train.jsonl').read_text().splitlines()]
examples = [next(row for row in rows if row['inputs']['moment']['signal_type'] == signal and row['provenance']['condition'] == condition)
            for signal in ['position_gain', 'record_watch', 'cutoff_watch', 'pace_change']
            for condition in ['complete', 'missing', 'contradictory', 'misleading_hint', 'boundary']]
report_path = ROOT / 'week5/evidence/deterministic-test/report.json'
report = json.loads(report_path.read_text()) if report_path.exists() else None
if report and report['dataset_sha256'] != manifest['dataset_sha256']:
    raise ValueError('Deterministic evidence is stale; rerun it against the current data')
snapshot = {'manifest': manifest, 'examples': examples, 'deterministic': report,
            'model_comparison': {'status': 'not_run', 'base_model_score': None, 'adapter_score': None,
                                 'human_review': 'pending', 'production_promoted': False}}
snapshot['comparisons'] = []
test_rows = [json.loads(line) for line in (ROOT / 'week5/data/synthetic/test.jsonl').read_text().splitlines()]
selected_test = [next(row for row in test_rows if row['inputs']['moment']['signal_type'] == signal and row['provenance']['condition'] == condition)
                 for signal in ['position_gain', 'record_watch', 'cutoff_watch', 'pace_change']
                 for condition in ['complete', 'missing', 'contradictory', 'misleading_hint', 'boundary']]


def add_comparison(directory, identifier, title, description, download):
    results = json.loads((directory / 'comparison/comparison.json').read_text())
    predictions = {variant: {row['id']: row for row in map(json.loads, (directory / f'test-{variant}/predictions.jsonl').read_text().splitlines())}
                   for variant in ['base', 'adapter']}
    snapshot['comparisons'].append({'id': identifier, 'title': title, 'description': description,
        'download': download, 'results': results, 'examples': [
            {'id': row['id'], 'signal': row['inputs']['moment']['signal_type'], 'condition': row['provenance']['condition'],
             'inputs': row['inputs'], **{variant: predictions[variant][row['id']] for variant in predictions}}
            for row in selected_test]})


gpu = ROOT / 'week5/evidence/gpu-run'
local = ROOT / 'week5/evidence/local-serving'
local_comparison = ROOT / 'week5/evidence/local-comparison'
adapter_serving = ROOT / 'week5/evidence/adapter-serving'
if adapter_serving.exists():
    adapter_summary = json.loads((adapter_serving / 'summary.json').read_text())
    browser = json.loads((adapter_serving / 'e2e-report.json').read_text())
    assert browser['passed'] and all(step['passed'] for step in browser['steps'])
    assert len(browser['steps']) == adapter_summary['browser_checks_passed']
    assert not adapter_summary['human_review_complete'] and not adapter_summary['production_promoted']
    for name, expected in json.loads((adapter_serving / 'artifact-sha256.json').read_text()).items():
        path = (adapter_serving / name).resolve()
        assert path.is_relative_to(adapter_serving.resolve())
        assert hashlib.sha256(path.read_bytes()).hexdigest() == expected, name
    snapshot['adapter_serving'] = adapter_summary
training_report = ROOT / 'week5/reports/data/final-training/training-run.json'
if training_report.exists():
    training = json.loads(training_report.read_text())
    assert training['status'] == 'trained' and training['dataset_sha256'] == manifest['dataset_sha256']
    snapshot['training_completed'] = True
if local_comparison.exists():
    subprocess.run([sys.executable, str(ROOT / 'week5/scripts/verify_local_comparison.py'),
                    str(local_comparison), '--metadata-only'], check=True)
    add_comparison(local_comparison, 'local-deployment-comparison', 'Matched local deployment: base versus fine-tuned model',
        'Both models use the same pinned Qwen revision, Q4_K_M conversion, Apple M1 Max runtime, explicit serving prompt and JSON-schema constrained decoding. Each was evaluated on the same 120 held-out synthetic cases. These results are separate from the GPU prompt controls and the earlier unadapted browser demo.',
        '/week5/local-comparison-evidence.zip')
if local.exists():
    local_summary = json.loads((local / 'summary.json').read_text())
    local_report = json.loads((local / 'e2e-report.json').read_text())
    assert local_summary['status'] == 'verified' and local_report['passed']
    assert local_summary['browser_checks_passed'] == len(local_report['steps'])
    assert all(step['passed'] for step in local_report['steps'])
    for name, digest in json.loads((local / 'artifact-sha256.json').read_text()).items():
        path = local / name
        assert path.resolve().is_relative_to(local.resolve())
        assert hashlib.sha256(path.read_bytes()).hexdigest() == digest, name
    snapshot['local_serving'] = local_summary
if gpu.exists():
    subprocess.run([sys.executable, str(ROOT / 'week5/scripts/verify_gpu_run.py'),
                    str(gpu), '--metadata-only'], check=True)
    training = json.loads((gpu / 'training-run.json').read_text())
    comparison = json.loads((gpu / 'comparison/comparison.json').read_text())
    if training['status'] != 'trained' or training['dataset_sha256'] != manifest['dataset_sha256']:
        raise ValueError('GPU training evidence does not match the current dataset')
    for variant in ['base', 'adapter']:
        result = comparison[variant]
        if result['dataset_sha256'] != manifest['dataset_sha256'] or result['cases'] != manifest['audit']['counts']['test']:
            raise ValueError('GPU comparison evidence is incomplete or stale')
        if result['identity']['kind'] != 'model_inference' or result['identity']['revision'] != training['revision']:
            raise ValueError('GPU comparison model identity mismatch')
    snapshot['model_comparison'].update({
        'status': 'completed',
        'base_model_score': comparison['base']['metrics']['automatic_success'],
        'adapter_score': comparison['adapter']['metrics']['automatic_success'],
        'training': {key: training[key] for key in ['base_model', 'revision', 'training_seconds',
            'trainable_parameters', 'peak_allocated_vram_bytes', 'environment', 'history']},
        'results': comparison,
    })
    add_comparison(gpu, 'original-gpu-comparison', 'Original GPU comparison',
        'Same base revision, NF4 quantization, original training prompt and greedy decoding for both models. Interpret this alongside the stronger shared-prompt control: the original prompt did not spell out every nested JSON key.', '/week5/gpu-evidence.zip')
    if (gpu / 'schema-control/comparison/comparison.json').exists():
        subprocess.run([sys.executable, str(ROOT / 'week5/scripts/verify_gpu_run.py'),
                        str(gpu), '--metadata-only', '--schema-control'], check=True)
        add_comparison(gpu / 'schema-control', 'stronger-prompt-control', 'Stronger shared prompt: the main GPU control',
            'The same exact JSON schema is supplied to both the base and fine-tuned model. The adapter, 120 held-out cases, NF4 quantization and greedy decoding are unchanged. Decoding is unconstrained. This control tests whether a clearer prompt closes the fine-tuning gap.', '/week5/gpu-evidence.zip')
serialized = json.dumps(snapshot, indent=2) + '\n'
(ROOT / 'public/data/week5-evidence.json').write_text(serialized)
(ROOT / 'week5/evidence/site-snapshot.json').write_text(serialized)
public = ROOT / 'public/week5'
public.mkdir(parents=True, exist_ok=True)
if adapter_serving.exists():
    with zipfile.ZipFile(public / 'adapter-serving-evidence.zip', 'w', zipfile.ZIP_DEFLATED) as bundle:
        for path in sorted(adapter_serving.rglob('*')):
            if path.is_file() and path.suffix in {'.json', '.png', '.md'}:
                bundle.write(path, path.relative_to(adapter_serving))
    shutil.copyfile(adapter_serving / 'adapter-demo.webm', public / 'adapter-demo.webm')
    shutil.copyfile(adapter_serving / '01-generated-desktop.png', public / 'adapter-demo-poster.png')
if local_comparison.exists():
    with zipfile.ZipFile(public / 'local-comparison-evidence.zip', 'w', zipfile.ZIP_DEFLATED) as bundle:
        for path in sorted(local_comparison.rglob('*')):
            if path.is_file() and path.name != 'review-key.json' and path.suffix in {'.json', '.jsonl', '.py', '.md'}:
                bundle.write(path, path.relative_to(local_comparison))
reports = ROOT / 'week5/reports'
if reports.exists():
    with zipfile.ZipFile(public / 'fine-tuning-reports.zip', 'w', zipfile.ZIP_DEFLATED) as bundle:
        for path in sorted(reports.rglob('*')):
            if path.is_file() and path.suffix in {'.json', '.jsonl', '.csv', '.md', '.png', '.py'}:
                bundle.write(path, path.relative_to(reports))
if local.exists():
    with zipfile.ZipFile(public / 'local-serving-evidence.zip', 'w', zipfile.ZIP_DEFLATED) as bundle:
        for path in sorted(local.rglob('*')):
            if path.is_file() and path.suffix in {'.json', '.png', '.md'}:
                bundle.write(path, path.relative_to(local))
    shutil.copyfile(local / 'local-demo.webm', public / 'local-demo.webm')
    shutil.copyfile(local / '01-generated-desktop.png', public / 'local-demo-poster.png')
if gpu.exists():
    with zipfile.ZipFile(public / 'gpu-evidence.zip', 'w', zipfile.ZIP_DEFLATED) as bundle:
        for path in sorted(gpu.rglob('*')):
            relative = path.relative_to(gpu)
            if (path.is_file() and path.name != 'review-key.json'
                    and path.suffix in {'.json', '.jsonl', '.log', '.md', '.png'}
                    and not {'adapter', 'checkpoints', 'merged'}.intersection(relative.parts)):
                bundle.write(path, path.relative_to(gpu))
    shutil.copyfile(gpu / 'measured-results.png', public / 'measured-results.png')
else:
    for stale in ['gpu-evidence.zip', 'measured-results.png']:
        (public / stale).unlink(missing_ok=True)
shutil.copyfile(ROOT / 'week5/notebooks/UltraMedia_Week5_QLoRA.ipynb', public / 'UltraMedia_Week5_QLoRA.ipynb')
for name in ['SUBMISSION.md', 'DATA_CARD.md', 'EVALUATION.md', 'SERVING.md', 'SCHEMA_CONTROL.md', 'END_TO_END.md', 'COMPUTE_OPTIONS.md']:
    source = ROOT / 'week5' / name
    if source.exists():
        shutil.copyfile(source, public / name)
with zipfile.ZipFile(public / 'synthetic-dataset.zip', 'w', zipfile.ZIP_DEFLATED) as bundle:
    for path in sorted((ROOT / 'week5/data/synthetic').iterdir()):
        bundle.write(path, path.name)
