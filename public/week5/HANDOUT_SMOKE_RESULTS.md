# Five task-level smoke probes

Executed after the original experiment using newly authored synthetic cases. Inputs and runner were committed locally at `5b39c2b06f5e1c01d5dd26158a992337d9eaabc5` before model inference. This is a small diagnostic, not independent human validation. The original prompts, adapter, dataset and nine checks were unchanged.

| Case | Expected | Rules | Base | Adapter |
|---|---|---|---|---|
| handout-v1-position-loss | draft | PASS | PASS | PASS |
| handout-v1-record-projection | draft | PASS | PASS | PASS |
| handout-v1-missing-cutoff | insufficient_evidence | PASS | PASS | FAIL |
| handout-v1-conflicting-pace | insufficient_evidence | PASS | FAIL | PASS |
| handout-v1-misleading-hint | draft | PASS | FAIL | FAIL |

All-check totals: **rules 5/5; base 3/5; adapter 3/5**. This probe does not show an adapter advantage over the base.

## Every failure

- **base, handout-v1-conflicting-pace**: numeric_tokens_supported. See the complete raw prediction; no failed row was dropped.
- **base, handout-v1-misleading-hint**: disposition_correct. See the complete raw prediction; no failed row was dropped.
- **adapter, handout-v1-missing-cutoff**: citation_ids_valid. See the complete raw prediction; no failed row was dropped.
- **adapter, handout-v1-misleading-hint**: disposition_correct. See the complete raw prediction; no failed row was dropped.

## Additional editorial inspection (AI analysis, not human scoring)

- The adapted position-loss draft contains “lost1places” (spacing normalized here) and an irrelevant projection disclaimer. The contract score does not assess grammar or relevance.
- The adapted record-projection draft says60seconds behind despite the project convention that positive record margin means ahead. The new evidence excerpt did not repeat that sign convention; this is a portability/semantic ambiguity to resolve in future versioned inputs, not a reason to relabel the frozen result.
- The adapter invents the citation `timing` on empty evidence, although its abstention decision is correct. Citation validation rejects it.
- Both learned models can abstain unnecessarily under a misleading hint. The structured rules retain the correct decision.

## Decision

Keep the trained model in research status. These first-attempt failures are retained. A future fix needs an explicit version and fresh evaluation; do not retry this set until it passes and present only the successful attempt. A human must judge wording and usefulness before production promotion.

[Protocol](https://github.com/sivalinb/ultramedia-studio/blob/codex/week5-handout-alignment/week5/project/SMOKE_PROTOCOL.md) · [inputs](https://github.com/sivalinb/ultramedia-studio/blob/codex/week5-handout-alignment/week5/project/smoke-cases.json) · [runner](https://github.com/sivalinb/ultramedia-studio/blob/codex/week5-handout-alignment/week5/scripts/run_handout_smoke.py) · [raw evidence](https://github.com/sivalinb/ultramedia-studio/blob/codex/week5-handout-alignment/week5/evidence/handout-smoke) · [blind review protocol](https://github.com/sivalinb/ultramedia-studio/blob/codex/week5-handout-alignment/week5/project/HUMAN_REVIEW.md)
