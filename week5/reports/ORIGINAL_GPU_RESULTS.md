# Original GPU prompt comparison

Verified 2026-09-09T07:29:50.022727+00:00. All 120 held-out cases completed for each model.

Base all-check success: **44/120 (36.7%)**. Adapter: **120/120 (100.0%)**. Difference: **63.3 percentage points**, paired race-group bootstrap 95% interval **57.5–70.0 points**, 1,000 resamples with seed 42. All 76 base failures became passes; no all-check regressions were observed in this comparison.

## What this comparison establishes

Both arms use the exact pinned base revision, original `evidence-editor-v2` prompt, NF4 double quantization, recorded BF16 compute, frozen evidence packs and greedy decoding with maximum 1024 new tokens on the same Colab T4 runtime. The adapter is the validation-selected checkpoint 100 from the completed two-epoch run. No test outcomes were used to change training, prompts or validators.

**This is the original-prompt result, not the stronger-prompt control.** The original prompt did not spell out every nested JSON property, so its base result combines formatting and behavioral failures. The predeclared shared-schema GPU control is running and must be considered before attributing the entire gap to a need for training. The separately declared local constrained-decoding comparison is 76/120 versus 109/120, showing remaining failures under a different deployment condition. Do not pool these scores.

## Every automatic metric

| Check | Base passed | Adapter passed |
|---|---:|---:|
| schema_valid | 73/120 (60.8%) | 120/120 (100.0%) |
| citation_ids_valid | 73/120 (60.8%) | 120/120 (100.0%) |
| structured_claims_supported | 73/120 (60.8%) | 120/120 (100.0%) |
| required_metric_covered | 73/120 (60.8%) | 120/120 (100.0%) |
| disposition_correct | 47/120 (39.2%) | 120/120 (100.0%) |
| numeric_tokens_supported | 73/120 (60.8%) | 120/120 (100.0%) |
| sensitive_language_absent | 49/120 (40.8%) | 120/120 (100.0%) |
| projection_not_achievement | 71/120 (59.2%) | 120/120 (100.0%) |
| automatic_success | 44/120 (36.7%) | 120/120 (100.0%) |

## By condition

| Group | Base all-check success | Adapter all-check success |
|---|---:|---:|
| boundary | 0/24 | 24/24 |
| complete | 0/24 | 24/24 |
| contradictory | 21/24 | 24/24 |
| misleading_hint | 0/24 | 24/24 |
| missing | 23/24 | 24/24 |

## By signal

| Group | Base all-check success | Adapter all-check success |
|---|---:|---:|
| cutoff_watch | 12/30 | 30/30 |
| pace_change | 12/30 | 30/30 |
| position_gain | 9/30 | 30/30 |
| record_watch | 11/30 | 30/30 |

## Resources and latency

| Measurement | Base | Adapter |
|---|---:|---:|
| Generation p50 | 24.590 s | 21.515 s |
| Generation p95 | 28.897 s | 26.965 s |
| peak_allocated_bytes | 2897879040 | 3027385856 |
| peak_reserved_bytes | 4179623936 | 4347396096 |

Models were loaded sequentially. Generation durations exclude model loading; output lengths vary. These measurements do not establish an SLA, energy consumption or cloud cost. Environment and token receipts are preserved for each arm.

## Failure interpretation and limits

The base failed the complete output contract on 47 cases. An invalid schema causes downstream checks to be false, so individual failure counts overlap and cannot be added. The lexical sensitive-language metric can also flag denials; it does not establish the number of harmful assertions. Exact numeric and citation checks remain bounded proxies for complete semantic faithfulness.

Perfect automatic scores on this synthetic template-based test do not demonstrate real-race reliability or human editorial preference. The actual adapted-model application suite still rejects one record-watch generation, and the matched local benchmark retains 11 disposition failures. These remain part of the submission. Human review and production promotion are pending.

## Reproducible evidence

- [Complete comparison](../evidence/gpu-run/comparison/comparison.json) and [case-level CSV](data/original-gpu-cases.csv).
- [Base predictions](../evidence/gpu-run/test-base/predictions.jsonl), [base token receipts](../evidence/gpu-run/test-base/token-receipts.jsonl), [adapter predictions](../evidence/gpu-run/test-adapter/predictions.jsonl), [adapter token receipts](../evidence/gpu-run/test-adapter/token-receipts.jsonl).
- [Training manifest](../evidence/gpu-run/training-run.json), [execution and recovery receipt](../evidence/gpu-run/execution-receipt.json), [full verification receipt](../evidence/gpu-run/verification.json).
- [Training and comparison figure](../evidence/gpu-run/measured-results.png).
- [Frozen protocol](../EVALUATION.md), [stronger prompt declaration](../SCHEMA_CONTROL.md), [flow and reproduction](FLOW_AND_REPRODUCIBILITY.md).

The independent verifier checked all adapter file bytes, exact dataset/case identities, all raw-output metrics, subgroup rates, latency and the paired bootstrap. Public bundles omit large weights and the blind assignment key; the full downloaded archive retains them separately.
