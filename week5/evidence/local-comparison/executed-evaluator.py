"""Predeclared same-runtime GGUF evaluation; never changes frozen training or GPU outputs."""
import argparse,hashlib,json,sys
from pathlib import Path
import httpx
root=Path(__file__).resolve().parent
repo=root/'ultramedia-studio'
sys.path.insert(0,str(repo/'backend/src'))
from ultramedia.benchmark import evaluate,compare_runs
from ultramedia.dataset import load_dataset_records
from ultramedia.contracts import MODEL_ID,MODEL_REVISION,GeneratedStory
from ultramedia.prompt_controls import serving_messages_for,SERVING_PROMPT_VERSION
p=argparse.ArgumentParser();p.add_argument('--variant',choices=['base','adapter'],required=True);p.add_argument('--model',required=True);p.add_argument('--port',type=int,default=8081);p.add_argument('--artifact',type=Path,required=True);args=p.parse_args()
rows,manifest=load_dataset_records(repo/'week5/data/synthetic');selected=[r for r in rows if r['split']=='test']
h=hashlib.sha256()
with args.artifact.open('rb') as f:
 for chunk in iter(lambda:f.read(8*1024*1024),b''):h.update(chunk)
identity={'kind':'model_inference','variant':args.variant,'base_model':MODEL_ID,'revision':MODEL_REVISION,'quantization':'GGUF Q4_K_M','prompt_version':SERVING_PROMPT_VERSION,'max_new_tokens':1024,'temperature':0,'seed':42,'decoding':'JSON-schema constrained','hardware':'Apple M1 Max, 64 GiB','runtime':'llama.cpp 0.3.0-dev build1 commit0f3a71be1','converter_commit':'30b6a755e29692e8bc8e072885325716a2fee70f','model_sha256':h.hexdigest(),'declaration_commit':'31c7c0df2b585a5df1ecf38e7e280f6081174099'}
output=root/'local-gguf-evaluation'/('test-'+args.variant)
receipts=[]
progress=root/'local-gguf-evaluation'/('progress-'+args.variant+'.jsonl');progress.parent.mkdir(exist_ok=True)
if output.exists() or progress.exists():raise ValueError('Local evaluation already started; inspect retained evidence before rerunning')
client=httpx.Client(timeout=120)
def generate(inputs):
 receipt={'case_index':len(receipts),'usage':None,'finish_reason':'error'};receipts.append(receipt)
 try:
  response=client.post(f'http://127.0.0.1:{args.port}/v1/chat/completions',json={'model':args.model,'messages':serving_messages_for(inputs),'temperature':0,'seed':42,'max_tokens':1024,'response_format':{'type':'json_schema','json_schema':{'name':'GeneratedStory','strict':True,'schema':GeneratedStory.model_json_schema()}}})
  response.raise_for_status();data=response.json();receipt['usage']=data.get('usage');receipt['finish_reason']=data['choices'][0]['finish_reason'];raw=data['choices'][0]['message']['content'];receipt['raw_output']=raw;return raw
 except Exception as e:
  receipt['error_type']=type(e).__name__;raise
 finally:
  with progress.open('a') as f:f.write(json.dumps(receipt)+'\n')
  print(json.dumps({'variant':args.variant,'completed':len(receipts),'total':len(selected),'finish_reason':receipt['finish_reason']}),flush=True)
report,predictions=evaluate(selected,generate,identity,manifest,output)
(output/'token-receipts.jsonl').write_text(''.join(json.dumps({'id':row['id'],**receipt})+'\n' for row,receipt in zip(selected,receipts,strict=True)))
print(json.dumps({'variant':args.variant,'cases':report['cases'],'metrics':report['metrics']}),flush=True)
