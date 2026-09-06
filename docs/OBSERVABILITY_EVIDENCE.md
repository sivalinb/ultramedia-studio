# Observability evidence register

This register connects every claim shown in the UltraMedia Model Ops dashboard to inspectable implementation or run evidence. It distinguishes configured behavior from measured results and from work that has not run.

## Verification snapshot

- Captured: 2026-09-06
- Release candidate: local deterministic provider + hybrid RAG
- Evaluation suite: `ultramedia-release-v1`
- Evaluation result: `PASS` across 6 deterministic cases
- Python tests: 6 passed, 0 failed
- Human-approved training examples: 0
- Minimum training gate: 20
- Latest recorded workflow trace: 6 spans, 0 failed

Commands executed from the repository root:

```text
backend/.venv/bin/pytest -q
6 passed, 1 warning in 0.59s

backend/.venv/bin/ultramedia-eval
suite: ultramedia-release-v1
cases: 6
release_decision: PASS
retrieval_recall_at_3: 1.0 (target 0.75)
citation_validity: 1.0 (target 1.0)
human_review_gate: 1.0 (target 1.0)
unsupported_sensitive_inference: 0.0 (target 0.0)

SQLite verification against backend/ultramedia.db
approved_examples: 0
trace_spans: 6
```

## Claim-to-evidence matrix

| Dashboard claim | State | Primary evidence |
| --- | --- | --- |
| Training is blocked at 0 / 20 approved examples | Measured gate | [`prepare_training_data.py`](../backend/scripts/prepare_training_data.py#L14-L69) queries only approved drafts and refuses fewer than 20; the verification snapshot above records the current approved count as 0. |
| Qwen3-4B QLoRA path exists | Implemented, not executed | [`train_qlora.py`](../backend/scripts/train_qlora.py#L5-L71) defines the base model, 4-bit NF4 loading, LoRA targets, and supervised training configuration. |
| Training split is 90 / 10 with seed 42 | Implemented | [`prepare_training_data.py`](../backend/scripts/prepare_training_data.py#L57-L69) shuffles with seed 42 and writes a 90 / 10 split. |
| Adapter merge exists | Implemented, not executed | [`merge_adapter.py`](../backend/scripts/merge_adapter.py#L5-L19) loads a PEFT adapter, merges it into the base model, and saves safe tensors. |
| Ollama packaging exists | Documented, no adapter artifact | [`backend/Modelfile`](../backend/Modelfile#L1-L4) defines the local runtime contract; [`docs/DEPLOYMENT.md`](DEPLOYMENT.md#local-portfolio) describes the Ollama deployment path. |
| Prompt + RAG remains selected | Decision | No adapter exists and no provider benchmark has run; the [model card](MODEL_CARD.md#evaluation-before-release) requires QLoRA to beat prompt + RAG before release. |
| Four evaluation gates passed | Measured | [`evals.py`](../backend/src/ultramedia/evals.py#L10-L75) defines and calculates the four metrics. The verification snapshot above records the observed result. |
| Six Python tests passed | Measured | [`tests/test_api.py`](../backend/tests/test_api.py#L1-L85) covers the health contract, fixture race, citations, review gate, failure behavior, trace sequence, and release eval. |
| Six workflow stages executed | Measured fixture trace | [`workflow.py`](../backend/src/ultramedia/workflow.py#L26-L152) defines the six-stage LangGraph and records each stage; the verification snapshot records six stored spans. |
| Trace durations total 7 ms | Measured fixture trace | The [machine-readable snapshot](../public/data/model-observability.json) contains stage durations 1, 2, 1, 1, 1, and 1 ms. These are deterministic local fixture timings, not production LLM latency. |
| Raw prompts and story bodies are excluded from trace rows | Implemented | [`observability.py`](../backend/src/ultramedia/observability.py#L27-L59) stores only trace ID, stage, status, duration, and operational detail. |
| No fine-tuned quality result is claimed | Verified absence | The [machine-readable snapshot](../public/data/model-observability.json) records the unmet data gate and null adapter artifact; the dashboard labels QLoRA as not trained. |
| Cloud latency, cost, fairness, and long-tail coverage remain unmeasured | Not run | They are explicitly listed as pre-release evaluation requirements in the [model card](MODEL_CARD.md#evaluation-before-release) and are not present in the measured smoke suite. |

## Evidence boundaries

The dashboard is an evidence console for a portfolio implementation, not a production model-monitoring claim. “Implemented” means code or configuration exists. “Measured” means the result was produced by the local deterministic fixture and is reproduced above. “Not run,” “not trained,” and “not produced” are deliberate negative evidence and must remain visible until artifacts exist.

## Visual system flow

The dashboard’s cinematic system map intentionally separates two operating modes:

1. The online lane follows moment detection → hybrid RAG → story generation → fact and safety verification → human review. The green observability rail records privacy-minimized spans across this request path.
2. The offline lane follows approved edits → minimum dataset gate → QLoRA training → challenger evaluation → adapter merge and local serving. It is visibly stopped at the 0 / 20 dataset gate.
3. The only bridge from online inference to offline learning is an editor-approved, evidence-linked draft. A trained adapter may return to the live lane only after it beats the prompt + RAG baseline on the model card’s release criteria.

The same structure is available in machine-readable form in [`public/data/model-observability.json`](../public/data/model-observability.json).
