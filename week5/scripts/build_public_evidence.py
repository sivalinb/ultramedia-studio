"""Publish a bounded evidence snapshot; never synthesize model performance."""
import json
import shutil
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
(ROOT / 'public/data/week5-evidence.json').write_text(json.dumps(snapshot, indent=2) + '\n')
public = ROOT / 'public/week5'
public.mkdir(parents=True, exist_ok=True)
shutil.copyfile(ROOT / 'week5/notebooks/UltraMedia_Week5_QLoRA.ipynb', public / 'UltraMedia_Week5_QLoRA.ipynb')
for name in ['SUBMISSION.md', 'DATA_CARD.md', 'EVALUATION.md', 'SERVING.md']:
    source = ROOT / 'week5' / name
    if source.exists():
        shutil.copyfile(source, public / name)
with zipfile.ZipFile(public / 'synthetic-dataset.zip', 'w', zipfile.ZIP_DEFLATED) as bundle:
    for path in sorted((ROOT / 'week5/data/synthetic').iterdir()):
        bundle.write(path, path.name)
