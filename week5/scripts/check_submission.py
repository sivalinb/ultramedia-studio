"""Offline reproducibility checks; does not claim GPU execution."""
import ast
import hashlib
import json
import subprocess
import sys
from pathlib import Path
from ultramedia.dataset import audit, canonical, load_dataset_records, synthetic_examples

ROOT = Path(__file__).resolve().parents[2]
rows, manifest = load_dataset_records(ROOT / 'week5/data/synthetic')
assert canonical(rows) == canonical(synthetic_examples()), 'Generator does not reproduce checked-in corpus'
report = audit(rows)
notebook = json.loads((ROOT / 'week5/notebooks/UltraMedia_Week5_QLoRA.ipynb').read_text())
code_cells = [cell for cell in notebook['cells'] if cell['cell_type'] == 'code']
for cell in code_cells:
    ast.parse(''.join(cell['source']))
    assert cell['execution_count'] is None and not cell['outputs'], 'Notebook must not contain claimed GPU outputs'
recorded = json.loads((ROOT / 'week5/evidence/deterministic-test/report.json').read_text())
assert recorded['dataset_sha256'] == manifest['dataset_sha256']
assert recorded['identity']['kind'] == 'deterministic_rules'
assert recorded['cases'] == report['counts']['test']
snapshot = json.loads((ROOT / 'public/data/week5-evidence.json').read_text())
assert snapshot['manifest'] == manifest
assert snapshot == json.loads((ROOT / 'week5/evidence/site-snapshot.json').read_text())
model = snapshot['model_comparison']
if model['status'] == 'not_run':
    assert model['base_model_score'] is None and model['adapter_score'] is None
else:
    assert model['status'] == 'completed'
    subprocess.run([sys.executable, str(ROOT / 'week5/scripts/verify_gpu_run.py'),
                    str(ROOT / 'week5/evidence/gpu-run'), '--metadata-only'], check=True)
    comparison = json.loads((ROOT / 'week5/evidence/gpu-run/comparison/comparison.json').read_text())
    assert model['results'] == comparison
    for variant, field in [('base', 'base_model_score'), ('adapter', 'adapter_score')]:
        assert model[field] == comparison[variant]['metrics']['automatic_success']
        assert comparison[variant]['cases'] == report['counts']['test']
        assert comparison[variant]['dataset_sha256'] == manifest['dataset_sha256']
assert model['human_review'] == 'pending' and not model['production_promoted']
for comparison in snapshot.get('comparisons', []):
    if comparison['id'] == 'local-deployment-comparison':
        directory = ROOT / 'week5/evidence/local-comparison'
        subprocess.run([sys.executable, str(ROOT / 'week5/scripts/verify_local_comparison.py'),
                        str(directory), '--metadata-only'], check=True)
    elif comparison['id'] == 'stronger-prompt-control':
        directory = ROOT / 'week5/evidence/gpu-run/schema-control'
        subprocess.run([sys.executable, str(ROOT / 'week5/scripts/verify_gpu_run.py'),
                        str(directory.parent), '--schema-control', '--metadata-only'], check=True)
    else:
        assert comparison['id'] == 'original-gpu-comparison'
        directory = ROOT / 'week5/evidence/gpu-run'
    assert comparison['results'] == json.loads((directory / 'comparison/comparison.json').read_text())
    for variant in ['base', 'adapter']:
        predictions = {p['id']: p for p in map(json.loads, (directory / f'test-{variant}/predictions.jsonl').read_text().splitlines())}
        for example in comparison['examples']:
            assert example[variant] == predictions[example['id']]
    assert len(comparison['examples']) == 20
subprocess.run([sys.executable, str(ROOT / 'week5/scripts/verify_handout_evidence.py')], check=True)
reports = ROOT / 'week5/reports'
for name, expected in json.loads((reports / 'artifact-sha256.json').read_text()).items():
    path = (reports / name).resolve()
    assert path.is_relative_to(reports.resolve())
    assert hashlib.sha256(path.read_bytes()).hexdigest() == expected, name
adapter_demo = snapshot.get('adapter_serving')
if adapter_demo:
    directory = ROOT / 'week5/evidence/adapter-serving'
    assert adapter_demo == json.loads((directory / 'summary.json').read_text())
    for name, expected in json.loads((directory / 'artifact-sha256.json').read_text()).items():
        path = (directory / name).resolve()
        assert path.is_relative_to(directory.resolve())
        assert hashlib.sha256(path.read_bytes()).hexdigest() == expected, name
    quality = json.loads((directory / 'workflow-check.json').read_text())
    assert quality['release_decision'] == adapter_demo['model_workflow_decision']
    assert sum(not case['passed'] for case in quality['case_results'] if case['kind'] == 'generation') == adapter_demo['failed_model_cases']
local = snapshot.get('local_serving')
if local:
    folder = ROOT / 'week5/evidence/local-serving'
    assert local == json.loads((folder / 'summary.json').read_text())
    hashes = json.loads((folder / 'artifact-sha256.json').read_text())
    for name, expected in hashes.items():
        path = (folder / name).resolve()
        assert path.is_relative_to(folder.resolve()), 'Unsafe evidence path'
        assert hashlib.sha256(path.read_bytes()).hexdigest() == expected, name
    browser = json.loads((folder / 'e2e-report.json').read_text())
    assert browser['passed'] and all(step['passed'] for step in browser['steps'])
    assert len(browser['steps']) == local['browser_checks_passed']
    quality = json.loads((folder / 'workflow-check.json').read_text())
    assert quality['release_decision'] == local['model_workflow_decision']
    assert sum(not case['passed'] for case in quality['case_results']) == local['failed_model_cases']
    assert not local['human_review_complete'] and not local['production_promoted']
for name in ['tokenizer-audit.json', 'training-api-validation.json']:
    extra = json.loads((ROOT / 'week5/evidence' / name).read_text())
    assert extra['dataset_sha256'] == manifest['dataset_sha256'], f'Stale evidence: {name}'
print(json.dumps({'dataset_rows': len(rows), 'group_overlap': report['group_overlap'],
                  'exact_payload_overlap': report['exact_payload_overlap'],
                  'notebook_code_cells_checked': len(code_cells), 'generator_reproducible': True,
                  'recorded_evidence_matches_dataset': True, 'gpu_execution': model['status']}, indent=2))
