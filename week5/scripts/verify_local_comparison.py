"""Recompute the separately declared local GGUF comparison and verify lineage."""
import argparse
import hashlib
import json
import math
import statistics
import tempfile
from pathlib import Path
from ultramedia.benchmark import METRICS, compare_runs, percentile
from ultramedia.contracts import MODEL_ID, MODEL_REVISION, GeneratedStory, assess_story, canonical
from ultramedia.dataset import load_dataset_records, sha
from ultramedia.prompt_controls import SERVING_PROMPT_VERSION

parser = argparse.ArgumentParser()
parser.add_argument('run', type=Path)
parser.add_argument('--dataset', type=Path, default=Path(__file__).resolve().parents[1]/'data/synthetic')
parser.add_argument('--metadata-only', action='store_true')
parser.add_argument('--base-model', type=Path)
parser.add_argument('--adapter-model', type=Path)
args = parser.parse_args()
if not args.metadata_only and (not args.base_model or not args.adapter_model):
    parser.error('Provide both model paths for byte verification, or explicitly use --metadata-only')
rows, manifest = load_dataset_records(args.dataset)
rows = [r for r in rows if r['split'] == 'test']
lineage = json.loads((args.run/'lineage.json').read_text())
training = lineage['adapter']['training_manifest']
assert training['status'] == 'trained' and training['base_model'] == MODEL_ID
assert training['revision'] == MODEL_REVISION and training['dataset_sha256'] == manifest['dataset_sha256']
assert training['adapter_files_sha256'] == lineage['adapter']['merge_manifest']['source_adapter_sha256']
for variant, model_path in [('base', args.base_model), ('adapter', args.adapter_model)]:
    folder = args.run/('test-'+variant)
    report = json.loads((folder/'report.json').read_text())
    predictions = [json.loads(s) for s in (folder/'predictions.jsonl').read_text().splitlines()]
    receipts = [json.loads(s) for s in (folder/'token-receipts.jsonl').read_text().splitlines()]
    assert len(rows) == len(predictions) == len(receipts) == report['cases'] == 120
    identity = report['identity']
    assert identity['variant'] == variant and identity['kind'] == 'model_inference'
    assert identity['base_model'] == MODEL_ID and identity['revision'] == MODEL_REVISION
    assert identity['prompt_version'] == SERVING_PROMPT_VERSION and identity['quantization'] == 'GGUF Q4_K_M'
    assert identity['temperature'] == 0 and identity['seed'] == 42 and identity['max_new_tokens'] == 1024
    assert identity['decoding'] == 'JSON-schema constrained'
    assert identity['converter_commit'] == lineage[variant]['converter_commit']
    expected_hash = lineage[variant]['artifacts'][f'qwen-{ "pinned-base" if variant == "base" else "adapter" }-q4_k_m.gguf']['sha256']
    assert identity['model_sha256'] == expected_hash
    if not args.metadata_only:
        digest = hashlib.sha256()
        with model_path.open('rb') as stream:
            for chunk in iter(lambda: stream.read(8*1024*1024), b''):
                digest.update(chunk)
        assert digest.hexdigest() == expected_hash
    assert report['dataset_sha256'] == manifest['dataset_sha256']
    assert report['case_set_sha256'] == sha(canonical([r['id'] for r in rows]))
    for row, prediction, receipt in zip(rows, predictions, receipts, strict=True):
        assert row['id'] == prediction['id'] == receipt['id']
        assert row['content_sha256'] == prediction['content_sha256']
        assert row['group_id'] == prediction['group_id']
        assert row['inputs']['moment']['signal_type'] == prediction['signal']
        assert row['provenance']['condition'] == prediction['condition']
        metrics = {key: False for key in METRICS}
        try:
            story = GeneratedStory.model_validate_json(prediction['raw_output'])
            checks = assess_story(story, row['inputs'])
            metrics.update({key: bool(checks.get(key, False)) for key in METRICS})
            metrics['schema_valid'] = True
            metrics['automatic_success'] = checks['automatic_checks_passed']
        except Exception:
            pass
        assert metrics == prediction['metrics'], row['id']
        if receipt['finish_reason'] != 'error':
            assert receipt['raw_output'] == prediction['raw_output']
            assert receipt['finish_reason'] in ['stop', 'length']
            assert 0 < receipt['usage']['completion_tokens'] <= 1024
            assert receipt['usage']['prompt_tokens'] > 0
    for metric in METRICS:
        assert report['metrics'][metric] == sum(p['metrics'][metric] for p in predictions)/120
    for field in ['signal', 'condition']:
        groups = {p[field] for p in predictions}
        assert set(report['by_'+field]) == groups
        for group in groups:
            selected = [p for p in predictions if p[field] == group]
            saved = report['by_'+field][group]
            assert saved['cases'] == len(selected)
            for metric in METRICS:
                assert saved[metric] == sum(p['metrics'][metric] for p in selected)/len(selected)
    durations = [p['duration_ms'] for p in predictions]
    assert all(math.isfinite(value) and value >= 0 for value in durations)
    assert report['latency_ms'] == {'p50': statistics.median(durations), 'p95': percentile(durations, .95)}
base = json.loads((args.run/'test-base/report.json').read_text())['identity']
adapter = json.loads((args.run/'test-adapter/report.json').read_text())['identity']
for key in ['runtime', 'converter_commit', 'hardware', 'temperature', 'seed', 'decoding']:
    assert base[key] == adapter[key], key
with tempfile.TemporaryDirectory() as directory:
    result = compare_runs(args.run/'test-base', args.run/'test-adapter', Path(directory)/'comparison')
    assert result == json.loads((args.run/'comparison/comparison.json').read_text())
print(json.dumps({'verified': True, 'cases_per_model': 120, 'all_metrics_recomputed': True,
                  'paired_comparison_reproduced': True, 'model_bytes_verified': not args.metadata_only,
                  'human_review_complete': False}, indent=2))
