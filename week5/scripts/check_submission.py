"""Offline reproducibility checks; does not claim GPU execution."""
import ast
import json
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
assert snapshot['model_comparison']['base_model_score'] is None
assert snapshot['model_comparison']['adapter_score'] is None
for name in ['tokenizer-audit.json', 'training-api-validation.json']:
    extra = json.loads((ROOT / 'week5/evidence' / name).read_text())
    assert extra['dataset_sha256'] == manifest['dataset_sha256'], f'Stale evidence: {name}'
print(json.dumps({'dataset_rows': len(rows), 'group_overlap': report['group_overlap'],
                  'exact_payload_overlap': report['exact_payload_overlap'],
                  'notebook_code_cells_checked': len(code_cells), 'generator_reproducible': True,
                  'recorded_evidence_matches_dataset': True, 'gpu_execution': 'not_run'}, indent=2))
