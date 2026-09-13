# Business decision: where a learned model earns its place

## Decision supported by current evidence

**Keep deterministic handling for the fully structured decision; retain the adapted model as an editorial research candidate.** Do not claim production savings or promote it from these results. Fine-tuning improves the local base on this synthetic task, but usefulness beyond rules remains unproven.

The existing rule implementation passes 120/120 engineered cases. It shares the task definition with the synthetic generator, so this is not independent generalization evidence. It does show that structured evidence sufficiency does not need a language model. The learned opportunity is useful wording and lower editor correction effort when inputs become varied; actual editors have not assessed that benefit.

| Evidence | Rules | Local base | Local adapter |
|---|---:|---:|---:|
| All nine checks, frozen 120 | 120/120 | 76/120 | 109/120 |
| Draft/hold accuracy | 120/120 | 100/120 | 109/120 |
| Saved p50 latency | .062ms in-process | 4.622s model request | 1.801s model request |
| Independent human preference | Not measured | Not measured | Not measured |

Rule in-process timing and model HTTP request timing have different boundaries. Neither includes editor correction or publication. Model output lengths differ; do not advertise an isolated speedup or zero operating cost.

## Cost accounting without invented prices

For each candidate record: actual training spend, serving price or machine-hour assumption, request durations and generated lengths, attempts, accepted briefs, and human review minutes. Use:

`cost per accepted brief = (amortized training + serving for every attempt + editor labor + retries) / accepted briefs`

`break-even briefs = additional training cost / positive recurring saving per accepted brief`

If recurring savings are zero or negative, there is no break-even. If acceptance or labor is unmeasured, cost per accepted brief is unknown. Free Colab and an existing Mac do not imply no energy, maintenance or opportunity cost. The public calculator is an explicit hypothetical scenario, not measured ROI or provider pricing.

## Evidence needed to reconsider

The [new interaction diagnostic](../calibration/RESULTS.md) strengthens the research-only decision: the adapter scores 22/48 all-check passes versus the base's 27/48 and rules' 48/48 on new authored cases. Misleading hints increase holds, but neutral projection and empty-evidence citation failures also persist. Complete independent reference-label and judge calibration, repeat controlled interactions, then choose a targeted change. The new sample does not measure editorial labor or justify model promotion.

Use the [blind editorial protocol](HUMAN_REVIEW.md) on new, rights-cleared examples authored independently of training. Compare rules, prompted base and adapter under the same user task. Collect factual-meaning errors, usefulness, correction time, ties and neither choices. Keep the current frozen scores and failures intact. Any training or prompt revision needs a new version and a fresh evaluation set.
