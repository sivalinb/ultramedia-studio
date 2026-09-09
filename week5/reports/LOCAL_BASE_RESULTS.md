# Verified pinned local-base results — adapter comparison pending

This report describes the **unadapted base arm only**, completed under the [predeclared local-serving protocol](../LOCAL_SERVING_EVALUATION.md). It is not a measurement of fine-tuning gain. The adapted arm and paired comparison remain pending.

## Execution identity

- Model: `Qwen/Qwen3-4B-Instruct-2507`, revision `cdbee75f17c01a7cc42f958dc650907174af0554`.
- Quantization: F16 conversion followed by Q4_K_M; exact output SHA-256 `39ccbecc6b48c63cbb57b789f558e66d15a9e9d65272ade7e9e0b81b2153fbc2`.
- Runtime: llama.cpp 0.3.0-dev, build 1, commit `0f3a71be1`; Apple M1 Max with 64 GiB RAM.
- Prompt: `evidence-editor-v2-local-serving-v1` with strict JSON-schema constrained decoding; temperature 0, seed 42, maximum 1024 output tokens.
- Cases: all 120 frozen test examples from 30 race groups. Source dataset identity matches the manifest.
- Conversion source: pinned llama.cpp commit `30b6a755e29692e8bc8e072885325716a2fee70f`. See [conversion lineage](data/local-base/conversion-lineage.json).

The independent verification recomputed every metric and subgroup from raw outputs, checked exact IDs, group/content/dataset hashes and token receipts, recomputed latency, and rehashed the actual model file. See [verification receipt](data/local-base/verification.json). The archived [executed evaluator](data/local-base/executed-evaluator.py) is the exact workspace wrapper used for this run; its relative workspace paths are preserved as execution evidence, not presented as a portable repository command.

## Results

| Automatic check | Passing cases | Rate |
|---|---:|---:|
| `schema_valid` | 120 / 120 | 100.0% |
| `citation_ids_valid` | 119 / 120 | 99.2% |
| `structured_claims_supported` | 111 / 120 | 92.5% |
| `required_metric_covered` | 120 / 120 | 100.0% |
| `disposition_correct` | 100 / 120 | 83.3% |
| `numeric_tokens_supported` | 104 / 120 | 86.7% |
| `sensitive_language_absent` | 97 / 120 | 80.8% |
| `projection_not_achievement` | 117 / 120 | 97.5% |
| `automatic_success` | 76 / 120 | 63.3% |

**All automatic checks: 76/120, or 63.3%.** These are contract checks, not human judgments of factuality or overall editorial quality. Some checks are conditional on disposition or can pass when an abstention has no claims; inspect the conjunction and disposition check together. Valid JSON in every case is expected from constrained decoding and does not prove supported content.

| Evidence condition | Passing all checks | Rate |
|---|---:|---:|
| boundary | 13 / 24 | 54.2% |
| complete | 20 / 24 | 83.3% |
| contradictory | 20 / 24 | 83.3% |
| misleading_hint | 0 / 24 | 0.0% |
| missing | 23 / 24 | 95.8% |

Measured per-request latency was p50 **4.622 seconds** and p95 **5.907 seconds** in this local run. These values include the measured request path, are hardware/workload specific, and are not a production latency guarantee. GPU NF4 timings are a separate condition.

## Failure inspection and metric limitations

The complete [case-check matrix](data/local-base/case-checks.csv), [raw predictions](data/local-base/predictions.jsonl), and [token receipts](data/local-base/token-receipts.jsonl) are retained. The examples below are the first failures encountered for the named checks in stored case order, not a selected sample used to compute a new score.

1. **Misleading hint and unnecessary abstention:** `fictional-race-120-pace_change` had a supported pace fact, but the model focused on rejecting a misleading injury/record hint and returned `insufficient_evidence`. The contract expected it to ignore the hint and draft the supported requested fact. This failed the disposition check.
2. **Lexical safety metric limitation:** the same output said an injury claim was unsupported. The selected sensitive-language check flags the occurrence of that vocabulary even in a denial. Therefore, the 23 sensitive-language failures do **not** establish 23 harmful medical assertions. This is an explicit limitation of the frozen automatic metric; it has not been loosened after seeing test results. A future negation-aware metric needs its own version and separate validation.
3. **Derived claim without a supporting structured fact:** `fictional-race-122-pace_change` added a position-gain claim derived from timing positions while citing an evidence item whose structured fact supported pace delta. The strict claim-support contract rejects that extra claim. A mathematically derivable number is not automatically an allowed structured claim under this contract.

All 24 misleading-hint examples failed the combined automatic contract. That points to a useful area for the adapter comparison, but the metric's lexical limitations and the model's frequent rejection of the bad hint must be considered when interpreting the result. Do not translate a contract failure rate directly into a hallucination or safety-incident rate.

No training, prompt, validator or case-selection changes were made from these test outcomes. The adapted model must receive the same serving conditions, and the full paired result must be reported even if it shows no advantage. Human editorial review remains pending.
