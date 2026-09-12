"""First-attempt local diagnostics. No training, prompt edits, cloud requests or human labels."""
import argparse
import hashlib
import json
import platform
import subprocess
import time
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlparse
import httpx
from ultramedia.contracts import GeneratedStory, MODEL_ID, MODEL_REVISION, assess_story
from ultramedia.prompt_controls import serving_messages_for, SERVING_PROMPT_VERSION
from ultramedia.providers import LocalStoryProvider

ROOT=Path(__file__).resolve().parent
HASHES={'base':'39ccbecc6b48c63cbb57b789f558e66d15a9e9d65272ade7e9e0b81b2153fbc2',
        'adapter':'ac3d4d36947c9412e5dbd884a705b2223315bef9cb19028209b2c263743a6b24'}


def digest(path):
    with path.open('rb') as f:return hashlib.file_digest(f,'sha256').hexdigest()


def run():
    p=argparse.ArgumentParser();p.add_argument('--variant',choices=['rules','base','adapter'],required=True)
    p.add_argument('--url');p.add_argument('--artifact',type=Path);p.add_argument('--server-binary',type=Path)
    p.add_argument('--output',required=True,type=Path);args=p.parse_args()
    if args.output.exists():raise ValueError('Preserve existing results; select a new output path')
    model_hash=None;server_hash=None
    if args.variant!='rules':
        if not args.url or urlparse(args.url).hostname not in {'127.0.0.1','localhost'}:p.error('Local loopback endpoint required')
        if not args.artifact or not args.server_binary:p.error('Model artifact and server binary required')
        model_hash=digest(args.artifact);assert model_hash==HASHES[args.variant]
        server_hash=digest(args.server_binary)
        props=httpx.get(args.url+'/props',timeout=20);props.raise_for_status()
        live=props.json()
        assert Path(live['model_path']).resolve()==args.artifact.resolve(), 'Server loaded a different model'
    manifest=json.loads((ROOT/'manifest.json').read_text())
    assert digest(ROOT/'interaction-cases.json')==manifest['sha256']['interaction-cases.json']
    rows=json.loads((ROOT/'interaction-cases.json').read_text())
    args.output.mkdir(parents=True)
    receipt={'variant':args.variant,'model':MODEL_ID if model_hash else 'local-deterministic-v2',
        'revision':MODEL_REVISION if model_hash else None,'model_sha256':model_hash,'server_binary_sha256':server_hash,
        'cases':len(rows),'dataset_sha256':digest(ROOT/'interaction-cases.json'),'runner_sha256':digest(Path(__file__)),
        'git_commit':subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),
        'prompt_version':SERVING_PROMPT_VERSION,'temperature':0,'seed':42,'max_tokens':1024,
        'platform':platform.platform(),'started_at':datetime.now(timezone.utc).isoformat(),
        'status':'running','independent_labels':0,'human_judge_calibrated':False,'production_promoted':False,
        'scope':'Exploratory authored interaction diagnostic, not confirmatory calibrated evaluation; latency not comparable.'}
    (args.output/'receipt.json').write_text(json.dumps(receipt,indent=2)+'\n')
    for row in rows:
        out={'id':row['id'],'group_id':row['group_id'],'condition':row['condition'],'hint':row['hint'],
             'expected':row['expected'],'raw_output':None,'decision':'invalid','checks':None,'error':None}
        start=time.perf_counter()
        try:
            if args.variant=='rules':
                story=LocalStoryProvider().generate(**row['inputs']);raw=story.model_dump_json()
            else:
                response=httpx.post(args.url+'/v1/chat/completions',timeout=120,json={
                    'model':'ultramedia-interactions-'+args.variant,'messages':serving_messages_for(row['inputs']),
                    'temperature':0,'seed':42,'max_tokens':1024,
                    'response_format':{'type':'json_schema','json_schema':{'name':'GeneratedStory','strict':True,'schema':GeneratedStory.model_json_schema()}}})
                response.raise_for_status();data=response.json();raw=data['choices'][0]['message']['content']
                out.update(usage=data.get('usage'),finish_reason=data['choices'][0]['finish_reason'])
            out['raw_output']=raw;story=GeneratedStory.model_validate_json(raw)
            out['decision']=story.disposition;out['checks']=assess_story(story,row['inputs'])
        except Exception as exc:out['error']=type(exc).__name__
        out['duration_seconds']=time.perf_counter()-start
        with (args.output/'predictions.jsonl').open('a') as f:f.write(json.dumps(out)+'\n')
        print(json.dumps({'variant':args.variant,'id':row['id'],'decision':out['decision']}),flush=True)
    receipt.update(status='completed',completed_at=datetime.now(timezone.utc).isoformat())
    (args.output/'receipt.json').write_text(json.dumps(receipt,indent=2)+'\n')


if __name__=='__main__':run()
