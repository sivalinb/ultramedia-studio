"""Five new authored task probes. Preserve failures; never modify training or prompts."""
import argparse
import hashlib
import json
import platform
import time
from datetime import datetime, timezone
from pathlib import Path

import httpx
from ultramedia.contracts import GeneratedStory, MODEL_ID, MODEL_REVISION, assess_story
from ultramedia.prompt_controls import SERVING_PROMPT_VERSION, serving_messages_for
from ultramedia.providers import LocalStoryProvider

ROOT = Path(__file__).resolve().parents[2]


def run():
    parser = argparse.ArgumentParser()
    parser.add_argument('--variant', choices=['base', 'adapter', 'rules'], required=True)
    parser.add_argument('--url', default='http://127.0.0.1:8081')
    parser.add_argument('--model', default='ultramedia-smoke')
    parser.add_argument('--artifact', type=Path)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    if args.output.exists():
        raise ValueError('Output already exists; preserve the previous run and use a new directory')
    dataset = ROOT / 'week5/project/smoke-cases.json'
    rows = json.loads(dataset.read_text())
    if args.variant != 'rules' and not args.artifact:
        parser.error('--artifact is required for model lineage verification')
    digest = None
    if args.artifact:
        with args.artifact.open('rb') as stream:
            digest = hashlib.file_digest(stream, 'sha256').hexdigest()
        lineage = json.loads((ROOT / 'week5/evidence/local-comparison/lineage.json').read_text())
        # The exact previously verified identities are recorded explicitly for these new probes.
        expected = {'base': '39ccbecc6b48c63cbb57b789f558e66d15a9e9d65272ade7e9e0b81b2153fbc2',
                    'adapter': 'ac3d4d36947c9412e5dbd884a705b2223315bef9cb19028209b2c263743a6b24'}
        assert digest == expected[args.variant]
    args.output.mkdir(parents=True)
    results = []
    for row in rows:
        start = time.perf_counter()
        result = {'id': row['id'], 'inputs': row['inputs'], 'expected': row['expected'],
                  'raw_output': None, 'output': None, 'passed': False, 'usage': None}
        try:
            if args.variant == 'rules':
                story = LocalStoryProvider().generate(row['inputs']['moment'], row['inputs']['evidence'], row['inputs']['timing'])
                raw = story.model_dump_json()
            else:
                response = httpx.post(args.url.rstrip('/') + '/v1/chat/completions', timeout=120,
                    json={'model': args.model, 'messages': serving_messages_for(row['inputs']),
                          'temperature': 0, 'seed': 42, 'max_tokens': 1024,
                          'response_format': {'type': 'json_schema', 'json_schema': {
                              'name': 'GeneratedStory', 'strict': True, 'schema': GeneratedStory.model_json_schema()}}})
                response.raise_for_status()
                data = response.json()
                raw = data['choices'][0]['message']['content']
                result['usage'] = data.get('usage')
                result['finish_reason'] = data['choices'][0]['finish_reason']
            result['raw_output'] = raw
            story = GeneratedStory.model_validate_json(raw)
            result['output'] = story.model_dump()
            result['checks'] = assess_story(story, row['inputs'])
            result['decision_correct'] = story.disposition == row['expected']['disposition']
            result['passed'] = result['decision_correct'] and result['checks']['automatic_checks_passed']
        except Exception as error:
            result['error_type'] = type(error).__name__
        result['duration_seconds'] = time.perf_counter() - start
        results.append(result)
        with (args.output / 'predictions.jsonl').open('a') as stream:
            stream.write(json.dumps(result) + '\n')
        print(json.dumps({'variant': args.variant, 'completed': len(results), 'passed': result['passed']}), flush=True)
    report = {'kind': 'post_training_authored_smoke_probe', 'created_at': datetime.now(timezone.utc).isoformat(),
              'variant': args.variant, 'cases': len(rows), 'passed': sum(r['passed'] for r in results),
              'dataset_sha256': hashlib.sha256(dataset.read_bytes()).hexdigest(),
              'runner_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
              'model': MODEL_ID if args.variant != 'rules' else 'local-deterministic-v2',
              'revision': MODEL_REVISION if args.variant != 'rules' else None,
              'model_sha256': digest, 'prompt_version': SERVING_PROMPT_VERSION if args.variant != 'rules' else None,
              'temperature': 0, 'seed': 42, 'max_tokens': 1024,
              'platform': platform.platform(), 'python': platform.python_version(),
              'human_review_complete': False, 'production_promoted': False,
              'scope': 'Five authored synthetic examples; descriptive smoke test, not independent human validation or a new generalization benchmark.'}
    (args.output / 'report.json').write_text(json.dumps(report, indent=2) + '\n')


if __name__ == '__main__':
    run()
