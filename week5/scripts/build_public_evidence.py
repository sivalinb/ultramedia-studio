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
gpu = ROOT / 'week5/evidence/gpu-run'
local = ROOT / 'week5/evidence/local-serving'
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
serialized = json.dumps(snapshot, indent=2) + '\n'
(ROOT / 'public/data/week5-evidence.json').write_text(serialized)
(ROOT / 'week5/evidence/site-snapshot.json').write_text(serialized)
public = ROOT / 'public/week5'
public.mkdir(parents=True, exist_ok=True)
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
