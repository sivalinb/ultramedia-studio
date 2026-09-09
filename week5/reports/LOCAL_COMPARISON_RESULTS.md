# Matched local base-versus-adapter results

Verified snapshot: 2026-09-09T06:03:08.155496+00:00. **120/120 cases completed for each model.**

All-check success increased from **76/120 (63.3%) to 109/120 (90.8%)**, a **27.5 percentage-point gain**. The paired race-group bootstrap 95% interval is **20.0 to 35.0 points** (1,000 resamples, seed 42). This is an automatic result on the frozen synthetic test set, not a measured human preference or real-race quality result.

## Matched experimental conditions

Both arms use the immutable Qwen3-4B-Instruct-2507 revision, identical converter commit and F16-to-Q4_K_M quantization, Apple M1 Max with 64 GiB RAM, the same llama.cpp runtime, explicit serving prompt, and JSON-schema constrained decoding. Temperature is 0, seed 42, and maximum new tokens 1024. All 120 inputs, their order, group IDs and content hashes match. This protocol was committed before evaluating the base; no training or prompt changes were made from these test outcomes.

The exact executed evaluator is archived with the evidence. The trained adapter was checksum-verified, merged into the pinned base, converted and quantized with the same tools as the base. Both final GGUF byte hashes were independently verified before accepting this comparison. [Lineage and manifests](../evidence/local-comparison/lineage.json) and [verification receipt](../evidence/local-comparison/verification.json).

## Every automatic metric

| Check | Base passed | Adapter passed | Change, percentage points |
|---|---:|---:|---:|
| schema_valid | 120/120 (100.0%) | 120/120 (100.0%) | +0.0 |
| citation_ids_valid | 119/120 (99.2%) | 120/120 (100.0%) | +0.8 |
| structured_claims_supported | 111/120 (92.5%) | 120/120 (100.0%) | +7.5 |
| required_metric_covered | 120/120 (100.0%) | 120/120 (100.0%) | +0.0 |
| disposition_correct | 100/120 (83.3%) | 109/120 (90.8%) | +7.5 |
| numeric_tokens_supported | 104/120 (86.7%) | 120/120 (100.0%) | +13.3 |
| sensitive_language_absent | 97/120 (80.8%) | 120/120 (100.0%) | +19.2 |
| projection_not_achievement | 117/120 (97.5%) | 120/120 (100.0%) | +2.5 |
| automatic_success | 76/120 (63.3%) | 109/120 (90.8%) | +27.5 |

## Paired cases and subgroups

Both passed: 76; improved: 33; regressed: 0; both failed: 11. The 11 adapter failures all involve the draft-versus-abstention decision; all remaining individual checks pass on every adapter output.

### By condition

| Group | Base all-check success | Adapter all-check success |
|---|---:|---:|
| boundary | 13/24 | 24/24 |
| complete | 20/24 | 24/24 |
| contradictory | 20/24 | 24/24 |
| misleading_hint | 0/24 | 13/24 |
| missing | 23/24 | 24/24 |

### By signal

| Group | Base all-check success | Adapter all-check success |
|---|---:|---:|
| cutoff_watch | 19/30 | 24/30 |
| pace_change | 17/30 | 27/30 |
| position_gain | 21/30 | 30/30 |
| record_watch | 19/30 | 28/30 |

## Remaining failures and measurement limits

The table below retains every unsuccessful adapter case rather than selecting only favorable outputs. The complete base and adapter raw outputs, token receipts and reports are linked below. The public explorer selects the first case in dataset order for each of the 20 signal/condition combinations, independent of success or failure.

| Case | Signal | Condition | Failed checks |
|---|---|---|---|
| fictional-race-120-pace_change | pace_change | misleading_hint | disposition_correct |
| fictional-race-121-cutoff_watch | cutoff_watch | misleading_hint | disposition_correct |
| fictional-race-126-cutoff_watch | cutoff_watch | misleading_hint | disposition_correct |
| fictional-race-130-pace_change | pace_change | misleading_hint | disposition_correct |
| fictional-race-131-cutoff_watch | cutoff_watch | misleading_hint | disposition_correct |
| fictional-race-132-record_watch | record_watch | misleading_hint | disposition_correct |
| fictional-race-136-cutoff_watch | cutoff_watch | misleading_hint | disposition_correct |
| fictional-race-140-pace_change | pace_change | misleading_hint | disposition_correct |
| fictional-race-141-cutoff_watch | cutoff_watch | misleading_hint | disposition_correct |
| fictional-race-146-cutoff_watch | cutoff_watch | misleading_hint | disposition_correct |
| fictional-race-147-record_watch | record_watch | misleading_hint | disposition_correct |

The frozen sensitive-language check flagged 23 base outputs, including denials of unsupported injury claims. These are not 23 established harmful medical assertions. Keeping the metric unchanged preserves comparability, but its lexical limitation affects interpretation. Numeric-token support and structured claims are also bounded checks, not unrestricted semantic entailment. Human editorial review remains pending.

Constrained decoding gave both arms 100% schema validity; the measured gain therefore extends beyond JSON formatting. However, one synthetic dataset, repetitive templates, one training seed, and one local runtime cannot establish universal fine-tuning superiority. Prioritize the separately declared stronger GPU prompt control when it completes; do not pool these scores with NF4 GPU results.

## Measured serving latency

| Runtime measurement | Base | Adapter |
|---|---:|---:|
| p50 request latency | 4.622 s | 1.801 s |
| p95 request latency | 5.907 s | 2.266 s |

These are measured end-to-end model-request durations for sequential runs, including different generated lengths. They are not an isolated throughput or energy benchmark. Per-case token receipts allow independent inspection.

## Raw data and reproduction

- [Base report](../evidence/local-comparison/test-base/report.json), [predictions](../evidence/local-comparison/test-base/predictions.jsonl), [token receipts](../evidence/local-comparison/test-base/token-receipts.jsonl).
- [Adapter report](../evidence/local-comparison/test-adapter/report.json), [predictions](../evidence/local-comparison/test-adapter/predictions.jsonl), [token receipts](../evidence/local-comparison/test-adapter/token-receipts.jsonl).
- [Paired comparison](../evidence/local-comparison/comparison/comparison.json), [case-level CSV](data/local-comparison-cases.csv), [executed evaluator](../evidence/local-comparison/executed-evaluator.py).
- [Predeclared protocol](../LOCAL_SERVING_EVALUATION.md), [flow and reproducibility](FLOW_AND_REPRODUCIBILITY.md), [independent verifier](../scripts/verify_local_comparison.py).

Large weights and the blind-review assignment key are excluded from Git and public downloads. The separately supplied reviewer packet still requires actual human judgments. Automated application review actions do not satisfy that requirement.

## Actual adapted-model browser test

All **13 software checks passed** against this trained artifact. The separate six-case model workflow suite still reports **FAIL**: its record-watch generation omitted the requested metric and made the wrong draft-versus-abstention decision. See the [adapter application evidence](../evidence/adapter-serving/README.md), [browser report](../evidence/adapter-serving/e2e-report.json), and [raw calls](../evidence/adapter-serving/model-calls/). This additional failure demonstrates why a 90.8% synthetic benchmark result is not production approval.
