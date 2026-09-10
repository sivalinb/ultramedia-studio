# Draft-versus-abstain classification

Post-hoc descriptive analysis of the saved matched-local 120-case predictions per model. No new inference or tuning. This supplements the frozen nine-check report; signal type is supplied in the input, not classified.

| Metric | Base | Adapter |
|---|---:|---:|
| accuracy | 0.8333 | 0.9083 |
| macro_f1 | 0.8326 | 0.9072 |
| draft: precision | 0.9643 | 1.0000 |
| draft: recall | 0.7500 | 0.8472 |
| draft: f1 | 0.8437 | 0.9173 |
| draft: support | 72.0000 | 72.0000 |
| insufficient_evidence: precision | 0.7188 | 0.8136 |
| insufficient_evidence: recall | 0.9583 | 1.0000 |
| insufficient_evidence: f1 | 0.8214 | 0.8972 |
| insufficient_evidence: support | 48.0000 | 48.0000 |

## Confusion matrices

Rows are reference classes. Columns are predicted classes. Neither local arm has invalid outputs; other experiments must retain an invalid category.

| Reference | Base draft | Base hold | Adapter draft | Adapter hold |
|---|---:|---:|---:|---:|
| Draft |54|18|61|11|
| Insufficient evidence |2|46|0|48|

The adapted model eliminates two unsupported draft decisions in this sample and reduces unnecessary holds from 18 to 11. All 11 remaining disposition errors involve misleading hints. Observed 0/48 unsupported drafts is not a zero-risk guarantee.

**Decision accuracy rises 7.5 percentage points; all-nine-check success rises 27.5 points. These are different measures.** Human usefulness and semantic quality remain unmeasured.

[Analysis and source hashes](https://github.com/sivalinb/ultramedia-studio/blob/codex/week5-handout-alignment/week5/reports/data/handout/UltraMedia-Week5-Disposition-Analysis.json) · [all 240 case rows](https://github.com/sivalinb/ultramedia-studio/blob/codex/week5-handout-alignment/week5/reports/data/handout/UltraMedia-Week5-Disposition-Cases.csv) · [reproduction script](https://github.com/sivalinb/ultramedia-studio/blob/codex/week5-handout-alignment/week5/scripts/derive_disposition_metrics.py) · [original local comparison](https://github.com/sivalinb/ultramedia-studio/blob/codex/week5-handout-alignment/week5/reports/LOCAL_COMPARISON_RESULTS.md)
