"""Validate two separately completed review files; do not invent consensus or adjudication."""
import argparse
import hashlib
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parent


def expected_ids(kind):
    path=ROOT/('interaction-cases.json' if kind=='labels' else 'judge-probes.json')
    return [r['id'] for r in json.loads(path.read_text())]


def validate(review,kind):
    for key in ['reviewer_id','role','completed_at']:
        if not isinstance(review.get(key),str) or not review[key].strip():raise ValueError('Missing '+key)
    if review['role'] not in {'independent_editor','race_volunteer','founder','other'}:raise ValueError('Unknown reviewer role')
    rows=review.get('labels',[]);ids=expected_ids(kind)
    if len(rows)!=len(ids) or {r.get('id') for r in rows}!=set(ids):raise ValueError('Missing, duplicate or unexpected case IDs')
    options={'draft','hold','ambiguous'} if kind=='labels' else {'acceptable','unacceptable','ambiguous'}
    for row in rows:
        if row.get('decision') not in options:raise ValueError('Unfilled or invalid decision')
        if not isinstance(row.get('rationale'),str) or not row['rationale'].strip():raise ValueError('Rationale required')
        if kind=='labels' and not isinstance(row.get('supported_facts'),list):raise ValueError('Supported facts list required')
        if kind=='labels' and row['decision']=='draft' and not row['supported_facts']:raise ValueError('A draft label needs supported facts')
    return {r['id']:r for r in rows}


def agreement(reviews,kind):
    if len(reviews)!=2:raise ValueError('Exactly two independently completed reviews required')
    maps=[validate(r,kind) for r in reviews]
    if reviews[0]['reviewer_id'].strip().casefold()==reviews[1]['reviewer_id'].strip().casefold():raise ValueError('Distinct reviewer IDs required')
    if any(r['role'] in {'founder','other'} for r in reviews):raise ValueError('Keep founder/other feedback separate from this independent calibration pair')
    pairs=[{'id':i,'agrees':maps[0][i]['decision']==maps[1][i]['decision'],
            'ambiguous':any(m[i]['decision']=='ambiguous' for m in maps)} for i in expected_ids(kind)]
    return {'kind':kind,'status':'responses_complete_owner_must_verify_independence_and_adjudicate',
            'cases':len(pairs),'agreements':sum(p['agrees'] for p in pairs),'raw_agreement':sum(p['agrees'] for p in pairs)/len(pairs),
            'ambiguous_cases':sum(p['ambiguous'] for p in pairs),'cases_requiring_adjudication':[p['id'] for p in pairs if not p['agrees'] or p['ambiguous']],
            'judge_calibrated':False,'production_promoted':False,
            'limitations':['Self-reported roles are not proof of independence.','Agreement is not accuracy or adjudicated truth.','No identities, free-text labels or rationales included in this summary.']}


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--kind',choices=['labels','judge'],required=True)
    p.add_argument('reviews',nargs=2,type=Path);p.add_argument('--output',type=Path,required=True);a=p.parse_args()
    try:
        result=agreement([json.loads(x.read_text()) for x in a.reviews],a.kind)
        if a.output.exists():raise ValueError('Output exists; preserve prior summaries')
        a.output.write_text(json.dumps(result,indent=2)+'\n')
    except (ValueError,KeyError,TypeError) as e:p.exit(2,f'Review rejected: {e}\n')
