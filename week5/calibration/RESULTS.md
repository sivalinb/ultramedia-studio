# Week 4 feedback applied to Week 5

Date: September 12, 2026. Declaration commit: `9902a78`. This is a new diagnostic, not a replacement for the original benchmark or evidence that independent calibration has finished.

**Finding:** misleading hints trigger additional abstention in these controlled cases, but the adapter also fails on neutral record projections and invents citations when evidence is missing. The next change must address these separately. No model is promoted.

## What was actually done

- Prepared evidence-only reference-label packets and separate output-judge packets with blank response templates; proposed answers and automatic scores are withheld from those packets.
- Ran ten author-designed evaluator challenges against the unchanged validator.
- Froze eight new fictional source groups across four signals, each crossed with complete/missing/contradictory evidence and neutral/misleading hints: **48 cases per variant**.
- Executed the existing pinned local base, merged adapter and rules: **144 saved first-attempt outputs**, including every failure. Model/runner/dataset/server-binary hashes and Git declaration are in each receipt. No retraining, cloud upload or new GPU purchase.
- Recomputed every saved decision and check, and every paired hint transition from raw outputs.

Human reference-label review: **0 completed**. Independent judge calibration: **0 completed**. Model runs are exploratory author-labeled diagnostics. Repeat the frozen design after independent labels and judge decisions are locked before confirmatory claims.

## Paired interaction results

Each cell contains eight source groups. Hint-only pairs have identical evidence and timing. A hold is considered unnecessary here against the author-proposed label, not independently adjudicated truth.

| Measure | Rules | Base | Adapter |
|---|---:|---:|---:|
| Holds on complete evidence, neutral hint | 0/8 | 0/8 | 2/8 |
| Holds on complete evidence, misleading hint | 0/8 | 8/8 | 8/8 |
| Additional holds when only hint changes | 0 | 8 | 6 |
| Unsupported drafts on missing/contradictory evidence, both hint conditions | 0/32 | 0/32 | 0/32 |
| Correct draft/hold decision across all cases | 48/48 | 40/48 | 38/48 |
| All existing automatic checks pass | 48/48 | 27/48 | 22/48 |
| Invalid/error outcomes | 0/48 | 0/48 | 0/48 |

The adapter does **not** beat the base on this diagnostic. Its 22/48 all-check score must not be hidden behind the earlier 109/120 score: these are different datasets and protocols, so they are not a before/after trend. This sample supports a hint-related effect under these inputs; it does not identify an internal neural mechanism, establish a retrieval failure, or prove broad generalization. Source packs were supplied directly; retrieval was not varied.

## Failures that guide the next experiment

1. **Hint-related over-abstention:** base switches draft to hold in 8/8 complete-evidence pairs; adapter in 6/8. Test one new policy instruction to reject the unsupported hint while retaining usable facts, after human label/judge calibration. Preserve the existing policy as the control.
2. **Record-projection weakness independent of the hint:** the adapter's other two complete-evidence cases already hold under neutral hints, despite an explicit sign convention. Investigate supported projection interpretation separately; a hint-only fix cannot explain this.
3. **Missing-evidence citation behavior:** all 16 adapted missing-evidence outputs choose hold but invent the citation `timing`. A correct disposition does not make the whole response valid. Validate empty-evidence citation handling independently of abstention choice.
4. **Evaluator limits:** two semantic reversals pass existing checks. A sentence denying injury fails the lexical sensitive-word policy. Calibrate factual correctness and publication-style policy as separate dimensions.

No runtime or training changes were made from these findings. Reports preserve the existing validator and all original artifacts.

## Judge challenge results are not human calibration

| Challenge | Existing automatic decision | Author expectation |
|---|---|---|
| Wrong position direction with matching number | Accept | Unacceptable |
| Wrong projected ahead/behind direction | Accept | Unacceptable |
| Explicit denial that injury is established | Reject | Semantically acceptable; publication policy may still reject |

The other seven challenges agree with the author expectations. Against the author's six unacceptable and four acceptable examples, this is two false accepts and one false reject. Those denominators are deliberately constructed and **not estimates of production judge accuracy**. Actual independent reviewers must confirm or challenge the proposed labels. The denial example especially requires a clearly defined factual-versus-style rubric.

## Independent review and next-change gate

Use two separately completed copies of each template. Do not give reviewers `judge-probes.json`, `interaction-cases.json`, these results or other reviewers' answers before they lock their judgments. Public availability does not make a review blind; the operator must verify the review procedure. Keep filled responses and identities outside Git.

`collect_independent.py` rejects incomplete responses, duplicate/missing case IDs, duplicate reviewers and founder/other feedback in an independent pair. It reports agreement, ambiguity and adjudication needs without public identities or rationales. Completeness and self-reported roles are not proof of independence or truth. A human must adjudicate disagreements and approve reference labels; the script does not manufacture consensus.

Proceed in this order: **independent labels → independent judge calibration → adjudication → frozen evaluator → repeated interaction tests → one targeted change → fresh evaluation → editorial release review**. Keep ambiguous cases separate. Define acceptable false-accept/false-reject and model-error thresholds before the confirmatory run with the domain reviewer; no arbitrary numeric threshold is asserted here.

The label packet complements the earlier five-case editorial packet. The earlier packet assesses usefulness and editing effort; this new packet checks whether the reference decision and judge are trustworthy. Neither has completed human responses yet.

## Reproduce and inspect

- [Frozen protocol](PROTOCOL.md), [input manifest](manifest.json), [interaction cases](interaction-cases.json).
- [Evidence-only label packet](independent-label-packet.json), [label template](independent-label-template.json).
- [Judge packet](judge-review-packet.json), [judge template](judge-review-template.json), [author-only judge diagnostics](judge-diagnostic.json).
- [Rules results](runs/rules/summary.json), [base results](runs/base/summary.json), [adapter results](runs/adapter/summary.json). Each folder includes raw predictions and the receipt.
- Run `PYTHONPATH=backend/src python week5/calibration/analyze.py week5/calibration/runs/base --output /tmp/base-summary.json` (likewise adapter/rules) to verify without model calls.
- Run `PYTHONPATH=backend/src python -m unittest discover -s week5/calibration -p 'test_*.py'` for protocol/review-tool checks.
- Collect private responses using `python week5/calibration/collect_independent.py --kind labels /private/reviewer-a.json /private/reviewer-b.json --output /private/label-agreement.json`; use `--kind judge` for judge responses.

The paired tests used the same Mac with overlapping runs. Request times are retained for diagnostics only; this is not a latency or speed comparison. Eight source groups and one misleading-hint wording limit the strength of inference. All data remains fictional; no permissioned historical replay or human-calibrated benchmark is claimed.
