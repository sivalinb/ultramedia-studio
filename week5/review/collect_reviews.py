"""Validate human-completed PDFs and write anonymous pilot aggregates. No model unblinding."""
import argparse
import hashlib
import json
import math
from collections import Counter
from pathlib import Path
from pypdf import PdfReader

ROLES={'independent_editor','race_volunteer','founder','other'}


def validate(fields):
    def value(key):
        v=str(fields.get(key,'')).strip()
        if not v:
            raise ValueError(f'Missing required answer: {key}')
        return v
    def choice(key, options):
        v=value(key)
        if v not in options:
            raise ValueError(f'Invalid {key}: expected {sorted(options)}')
        return v
    reviewer=value('reviewer_id')
    role=choice('reviewer_role',ROLES)
    consent=str(fields.get('training_consent','')).strip() or 'false'
    if consent not in {'true','false'}:
        raise ValueError('training_consent must be true or false')
    rows=[];preferences=[]
    for i in range(1,6):
        preferences.append({'case':i,'preferred':choice(f'{i}.preferred',{'A','B','C','tie','neither'}),
                            'reason':value(f'{i}.preference_reason')})
        for label in 'ABC':
            prefix=f'{i}.{label}.'
            readability=choice(prefix+'readability',set('12345'))
            minutes=float(value(prefix+'minutes'))
            if not math.isfinite(minutes) or minutes<0:
                raise ValueError('Correction minutes must be finite and nonnegative')
            rows.append({'case':i,'candidate':label,
                         'meaning':choice(prefix+'meaning',{'supported','unsupported','unclear'}),
                         'readability':int(readability),
                         'usable':choice(prefix+'usable',{'yes','no'}),
                         'minutes':minutes,'rationale':value(prefix+'rationale')})
    return {'reviewer':reviewer,'role':role,'training_consent':consent=='true',
            'rows':rows,'preferences':preferences}


def collect(paths, output):
    reviews=[]; hashes=[]
    for path in paths:
        reader=PdfReader(path)
        fields=reader.get_fields() or {}
        review=validate({k:v.get('/V','') for k,v in fields.items()})
        digest=hashlib.sha256(path.read_bytes()).hexdigest()
        if digest in hashes or any(r['reviewer'].casefold()==review['reviewer'].casefold() for r in reviews):
            raise ValueError('Duplicate file or reviewer ID; provide one locked response per reviewer')
        hashes.append(digest);reviews.append(review)
    if not reviews:
        raise ValueError('No reviews supplied')
    groups={}
    for role in sorted({r['role'] for r in reviews}):
        subset=[r for r in reviews if r['role']==role]
        rows=[row for r in subset for row in r['rows']]
        groups[role]={'reviewers':len(subset),'candidate_judgments':len(rows),
                      'meaning_counts':dict(Counter(r['meaning'] for r in rows)),
                      'usable_count':sum(r['usable']=='yes' for r in rows),
                      'mean_readability':sum(r['readability'] for r in rows)/len(rows),
                      'mean_reported_correction_minutes':sum(r['minutes'] for r in rows)/len(rows)}
    disagreements=[]
    for i in range(1,6):
        counts=Counter(r['preferences'][i-1]['preferred'] for r in reviews)
        disagreements.append({'case':i,'preference_counts':dict(counts),'disagreement':len(counts)>1})
    result={'status':'human_responses_validated_not_independently_authenticated',
            'reviewers':len(reviews),'cases':5,'source':'handout-smoke/blind-review.json',
            'source_sha256':hashlib.sha256((Path(__file__).resolve().parents[1]/'evidence/handout-smoke/blind-review.json').read_bytes()).hexdigest(),
            'groups':groups,'case_preferences':disagreements,
            'limitations':['Five synthetic authored cases; exploratory only.',
                          'Role and timing are self-reported; owner must verify actual human completion.',
                          'A/B/C assignments vary by case; do not pool letters as model identities.',
                          'No identities, free-text rationales, or consent grants published. Keep originals private.',
                          'No model winner or production readiness inferred.']}
    output.write_text(json.dumps(result,indent=2)+'\n')
    return result


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('pdfs',nargs='+',type=Path)
    parser.add_argument('--output',required=True,type=Path)
    args=parser.parse_args()
    try:
        result=collect(args.pdfs,args.output)
    except (ValueError,TypeError) as exc:
        parser.exit(2,f'Review rejected: {exc}\n')
    print(f"Validated {result['reviewers']} reviewer response(s); owner verification still required.")
