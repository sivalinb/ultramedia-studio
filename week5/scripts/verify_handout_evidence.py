"""Recompute new task evidence from saved inputs and raw outputs, without inference."""
import hashlib
import json
from collections import Counter
from pathlib import Path

from ultramedia.contracts import GeneratedStory, assess_story

ROOT = Path(__file__).resolve().parents[2]


def verify():
    classification = json.loads((ROOT / 'week5/reports/data/handout/UltraMedia-Week5-Disposition-Analysis.json').read_text())
    for name, digest in classification['hashes'].items():
        path = (ROOT / name).resolve()
        assert path.is_relative_to(ROOT)
        assert hashlib.sha256(path.read_bytes()).hexdigest() == digest
    targets = [json.loads(line) for line in (ROOT / 'week5/data/synthetic/test.jsonl').read_text().splitlines()]
    labels = ['draft', 'insufficient_evidence']
    for variant in ['base', 'adapter']:
        predictions = [json.loads(line) for line in (ROOT / f'week5/evidence/local-comparison/test-{variant}/predictions.jsonl').read_text().splitlines()]
        counts = Counter()
        assert len(targets) == len(predictions) == 120
        for target, prediction in zip(targets, predictions, strict=True):
            assert all(target[k] == prediction[k] for k in ['id', 'content_sha256', 'group_id'])
            story = GeneratedStory.model_validate_json(prediction['raw_output'])
            counts[target['output']['disposition'], story.disposition] += 1
        actual = classification['variants'][variant]
        assert actual['confusion_matrix'] == [[counts[a, b] for b in labels + ['invalid']] for a in labels]
        assert actual['accuracy'] == sum(counts[a, a] for a in labels) / 120
        f1s = []
        for label in labels:
            tp = counts[label, label]
            support = sum(n for (a, b), n in counts.items() if a == label)
            predicted = sum(n for (a, b), n in counts.items() if b == label)
            precision = tp / predicted if predicted else 0
            recall = tp / support if support else 0
            f1 = 2 * precision * recall / (precision + recall) if precision + recall else 0
            assert actual['classes'][label] == {'precision': precision, 'recall': recall, 'f1': f1, 'support': support}
            f1s.append(f1)
        assert actual['macro_f1'] == sum(f1s) / 2
    folder = ROOT / 'week5/evidence/handout-smoke'
    for name, digest in json.loads((folder / 'artifact-sha256.json').read_text()).items():
        path = (folder / name).resolve()
        assert path.is_relative_to(folder)
        assert hashlib.sha256(path.read_bytes()).hexdigest() == digest, name
    dataset = ROOT / 'week5/project/smoke-cases.json'
    cases = json.loads(dataset.read_text())
    summary = json.loads((folder / 'summary.json').read_text())
    for variant in ['rules', 'base', 'adapter']:
        report = json.loads((folder / variant / 'report.json').read_text())
        assert report == summary['reports'][variant]
        assert report['dataset_sha256'] == hashlib.sha256(dataset.read_bytes()).hexdigest()
        assert report['runner_sha256'] == hashlib.sha256((ROOT / 'week5/scripts/run_handout_smoke.py').read_bytes()).hexdigest()
        rows = [json.loads(line) for line in (folder / variant / 'predictions.jsonl').read_text().splitlines()]
        assert len(rows) == len(cases) == 5
        for row, case in zip(rows, cases, strict=True):
            assert row['id'] == case['id'] and row['inputs'] == case['inputs'] and row['expected'] == case['expected']
            story = GeneratedStory.model_validate_json(row['raw_output'])
            assert story.model_dump() == row['output']
            checks = assess_story(story, case['inputs'])
            assert checks == row['checks']
            assert row['passed'] == (checks['automatic_checks_passed'] and story.disposition == case['expected']['disposition'])
        assert report['cases'] == 5 and report['passed'] == sum(row['passed'] for row in rows)
        assert report['human_review_complete'] is False and report['production_promoted'] is False
    packet = json.loads((folder / 'blind-review.json').read_text())
    assert len(packet) == 5 and all(p['reviewer'] is None and p['preferred'] is None for p in packet)
    assert not (folder / 'review-key.json').exists()
    print(json.dumps({'classification_cases_verified': 240, 'smoke_outputs_verified': 15, 'human_review': 'pending'}))


if __name__ == '__main__':
    verify()
