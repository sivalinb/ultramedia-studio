"""Verify the new diagnostics and review status without inference or human-score fabrication."""
import hashlib
import json
from pathlib import Path
from analyze import analyze
from prepare import cases,judge_probes
from ultramedia.contracts import GeneratedStory,assess_story

ROOT=Path(__file__).resolve().parent
manifest=json.loads((ROOT/'manifest.json').read_text())
assert manifest['independent_human_labels']==0
for name,sha in manifest['sha256'].items():assert hashlib.sha256((ROOT/name).read_bytes()).hexdigest()==sha,name
assert cases()==json.loads((ROOT/'interaction-cases.json').read_text())
assert judge_probes(cases())==json.loads((ROOT/'judge-probes.json').read_text())
judge=json.loads((ROOT/'judge-diagnostic.json').read_text())
for source,result in zip(judge_probes(cases()),judge['results'],strict=True):
    checks=assess_story(GeneratedStory.model_validate(source['output']),source['inputs'])
    assert result['id']==source['id'] and result['checks']==checks
    assert result['author_expected_acceptable']==source['author_expected_acceptable']
    assert result['automatic_accept']==checks['automatic_checks_passed']
    assert result['disagrees_with_author']==(result['automatic_accept']!=result['author_expected_acceptable'])
for variant in ['rules','base','adapter']:
    folder=ROOT/'runs'/variant
    assert analyze(folder)==json.loads((folder/'summary.json').read_text())
    receipt=json.loads((folder/'receipt.json').read_text())
    assert receipt['runner_sha256']==hashlib.sha256((ROOT/'run_interactions.py').read_bytes()).hexdigest()
    assert receipt['independent_labels']==0 and not receipt['human_judge_calibrated'] and not receipt['production_promoted']
print(json.dumps({'verified':True,'variants':3,'predictions_recomputed':144,'judge_challenges':10,'independent_human_reviews':0}))
