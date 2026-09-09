"""Recompute saved GPU results without loading a model.

The default additionally verifies the downloaded adapter's bytes. Use
--metadata-only for the public evidence bundle, which excludes model weights.
"""
import argparse
import hashlib
import json
import math
import statistics
import tempfile
from pathlib import Path

from ultramedia.benchmark import METRICS, compare_runs, percentile
from ultramedia.contracts import GeneratedStory, MODEL_ID, MODEL_REVISION, PROMPT_VERSION, assess_story, canonical
from ultramedia.dataset import load_dataset_records, sha
from ultramedia.prompt_controls import SCHEMA_PROMPT_VERSION

parser = argparse.ArgumentParser()
parser.add_argument('run', type=Path)
parser.add_argument('--dataset', type=Path, default=Path(__file__).resolve().parents[1] / 'data/synthetic')
parser.add_argument('--metadata-only', action='store_true', help='Skip model-weight byte verification; still recompute every metric')
parser.add_argument('--schema-control', action='store_true')
args = parser.parse_args()
run = args.run
evaluation_dir = run / 'schema-control' if args.schema_control else run
rows, manifest = load_dataset_records(args.dataset)
test = {r['id']: r for r in rows if r['split'] == 'test'}
training = json.loads((run/'training-run.json').read_text())
assert training['status'] == 'trained'
assert training['base_model'] == MODEL_ID and training['revision'] == MODEL_REVISION
assert training['prompt_version'] == PROMPT_VERSION
assert training['dataset_sha256'] == manifest['dataset_sha256']
assert training['trainable_parameters'] > 0 and training['training_seconds'] > 0
assert not training['production_promoted']
assert len([x for x in training['history'] if 'eval_loss' in x]) == 2
assert all(math.isfinite(x['eval_loss']) for x in training['history'] if 'eval_loss' in x)
for name, expected in training['adapter_files_sha256'].items():
    assert Path(name).name == name
    assert len(expected) == 64 and all(c in '0123456789abcdef' for c in expected)
    if not args.metadata_only:
        assert hashlib.sha256((run/'adapter'/name).read_bytes()).hexdigest() == expected, name
assert 'adapter_model.safetensors' in training['adapter_files_sha256']
for variant in ['base', 'adapter']:
    directory = evaluation_dir/('test-'+variant)
    predictions = [json.loads(s) for s in (directory/'predictions.jsonl').read_text().splitlines()]
    report = json.loads((directory/'report.json').read_text())
    receipts = [json.loads(s) for s in (directory/'token-receipts.jsonl').read_text().splitlines()]
    assert report['cases'] == len(test) == len(predictions) == len(receipts)
    assert [p['id'] for p in predictions] == list(test)
    assert report['identity']['kind'] == 'model_inference'
    assert report['identity']['variant'] == variant
    for field in ['base_model', 'revision', 'quantization', 'compute_dtype']:
        assert report['identity'][field] == training[field], field
    assert report['identity']['prompt_version'] == (SCHEMA_PROMPT_VERSION if args.schema_control else PROMPT_VERSION)
    assert report['identity']['split'] == 'test'
    assert report['identity']['adapter_files_sha256'] == (training['adapter_files_sha256'] if variant == 'adapter' else None)
    assert report['dataset_sha256'] == manifest['dataset_sha256']
    assert report['case_set_sha256'] == sha(canonical(list(test)))
    memory = json.loads((directory/'gpu-memory.json').read_text())
    assert 0 < memory['peak_allocated_bytes'] <= memory['peak_reserved_bytes']
    for p, receipt in zip(predictions, receipts, strict=True):
        row = test[p['id']]
        assert receipt['id'] == p['id']
        assert p['content_sha256'] == row['content_sha256']
        assert p['group_id'] == row['group_id']
        assert p['signal'] == row['inputs']['moment']['signal_type']
        assert p['condition'] == row['provenance']['condition']
        assert receipt['finish_reason'] in {'eos', 'length', 'error'}
        if receipt['finish_reason'] != 'error':
            assert receipt['input_tokens'] > 0
            assert 0 < receipt['output_tokens'] <= report['identity']['max_new_tokens']
        checks = {m: False for m in METRICS}
        try:
            story = GeneratedStory.model_validate_json(p['raw_output'])
            assessed = assess_story(story, row['inputs'])
            checks.update({m: bool(assessed.get(m, False)) for m in METRICS})
            checks['schema_valid'] = True
            checks['automatic_success'] = assessed['automatic_checks_passed']
        except Exception:
            pass
        assert p['metrics'] == checks, p['id']
        assert math.isfinite(p['duration_ms']) and p['duration_ms'] >= 0
    for metric in METRICS:
        actual = sum(p['metrics'][metric] for p in predictions)/len(predictions)
        assert actual == report['metrics'][metric], (variant, metric)
    for field in ['signal', 'condition']:
        expected_groups = {p[field] for p in predictions}
        assert set(report['by_'+field]) == expected_groups
        for group in expected_groups:
            selected = [p for p in predictions if p[field] == group]
            recorded_group = report['by_'+field][group]
            assert recorded_group['cases'] == len(selected)
            for metric in METRICS:
                assert recorded_group[metric] == sum(p['metrics'][metric] for p in selected)/len(selected)
    durations = [p['duration_ms'] for p in predictions]
    assert report['latency_ms'] == {'p50': statistics.median(durations), 'p95': percentile(durations, 0.95)}
with tempfile.TemporaryDirectory() as temporary:
    recomputed = compare_runs(evaluation_dir/'test-base', evaluation_dir/'test-adapter', Path(temporary)/'comparison')
    recorded = json.loads((evaluation_dir/'comparison/comparison.json').read_text())
    assert recomputed == recorded
print(json.dumps({'verified': True, 'test_cases_per_model': len(test),
                  'adapter_bytes_verified': not args.metadata_only, 'all_metrics_recomputed': True,
                  'paired_comparison_reproduced': True, 'human_review_complete': False}, indent=2))
