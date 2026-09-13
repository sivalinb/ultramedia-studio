"""Recompute all saved interaction decisions/checks and paired effects, without model calls."""
import argparse
import collections
import hashlib
import json
from pathlib import Path
from ultramedia.contracts import GeneratedStory, assess_story

ROOT=Path(__file__).resolve().parent


def analyze(folder):
    cases=json.loads((ROOT/'interaction-cases.json').read_text())
    rows=[json.loads(x) for x in (folder/'predictions.jsonl').read_text().splitlines()]
    receipt=json.loads((folder/'receipt.json').read_text())
    assert receipt['status']=='completed' and receipt['dataset_sha256']==hashlib.sha256((ROOT/'interaction-cases.json').read_bytes()).hexdigest()
    assert [r['id'] for r in rows]==[c['id'] for c in cases]
    for row,case in zip(rows,cases,strict=True):
        for key in ['group_id','condition','hint','expected']:assert row[key]==case[key]
        try:
            story=GeneratedStory.model_validate_json(row['raw_output'])
        except Exception:
            assert row['decision']=='invalid' and row['checks'] is None
        else:
            assert row['decision']==story.disposition and row['checks']==assess_story(story,case['inputs'])
    cells={}
    for condition in ['complete','missing','contradictory']:
        for hint in ['neutral','misleading']:
            subset=[r for r in rows if r['condition']==condition and r['hint']==hint]
            cells[condition+'_'+hint]={'cases':len(subset),'decisions':dict(collections.Counter(r['decision'] for r in subset)),
                'unnecessary_holds':sum(r['decision']=='insufficient_evidence' for r in subset) if condition=='complete' else None,
                'unsupported_drafts':sum(r['decision']=='draft' for r in subset) if condition!='complete' else None,
                'invalid':sum(r['decision']=='invalid' for r in subset),
                'all_checks_pass':sum(bool(r['checks'] and r['checks']['automatic_checks_passed']) for r in subset)}
    pairs=[]
    for group in sorted({r['group_id'] for r in rows}):
        for condition in ['complete','missing','contradictory']:
            pair={r['hint']:r for r in rows if r['group_id']==group and r['condition']==condition}
            a,b=pair['neutral'],pair['misleading']
            pairs.append({'group_id':group,'condition':condition,'neutral':a['decision'],'misleading':b['decision'],
                          'decision_changed':a['decision']!=b['decision']})
    return {'variant':receipt['variant'],'cases':len(rows),'source_groups':8,'cells':cells,'pairs':pairs,
            'hint_effect_complete_hold_count':cells['complete_misleading']['unnecessary_holds']-cells['complete_neutral']['unnecessary_holds'],
            'independent_human_labels':0,'human_judge_calibrated':False,'production_promoted':False,
            'scope':'Counts against author-proposed labels; no causal claim about retrieval, no population generalization.'}


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('folder',type=Path);p.add_argument('--output',type=Path,required=True);args=p.parse_args()
    args.output.write_text(json.dumps(analyze(args.folder),indent=2)+'\n')
