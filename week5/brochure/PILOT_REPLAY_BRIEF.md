# UltraMedia supervised replay: proposed participation brief

Status: protocol proposal, 9 September 2026. No race export has been obtained for this pilot, no reviewers recruited, and no pilot results collected. This document does not authorize a live publication or a new paid compute allocation. The existing frozen Week 5 results remain unchanged.

## First customer and decision

The initial customer hypothesis is a race organizer with a small media team. The daily user is the editor reconciling timing and context while preparing a reviewed update. Validate the hypothesis in interviews before assuming demand. A runner's support crew is a distinct later audience; navigation, pacing instructions, medical interpretation and race-control decisions are outside this editorial pilot.

Ask organizers and editors to describe their last event: where updates arrived, which records needed correction, who approved stories, and how much time verification and drafting took. Request examples and existing workflow evidence rather than hypothetical enthusiasm. Record actual responses only after consent. No interviews have been completed.

The pilot asks whether the adapted model reduces effort to produce a correct, useful brief compared with rules and a prompted base model. If rules are equally useful or cheaper after review, retain rules for that task.

## Participation checklist

- A data owner willing to provide one historical timing export with permission for this evaluation and clearly stated redistribution limits.
- Source owner, event/version, collection date, timezone, timing methodology and correction history. Preserve an original-file hash and transformation log.
- Two independent reviewers with race-media experience, separate from the model-building role. Obtain consent for recording judgments and review time.
- Agreement on the input contract, selection procedure, factual-error rubric, freshness policy, candidate versions and decision gates before generation.
- A replay only: no external posting, live runner decisions or implied organizer endorsement. Redact unnecessary identifiers; keep restricted source records and reviewer identities out of public artifacts.

## Candidate design to freeze before execution

Use 30 new cases from one historical event, with five cases in each condition: normal, delayed, corrected, duplicate, conflicting and missing updates. Select cases before seeing model outcomes. Document how cases were selected; these balanced conditions are a stress test, not an estimate of real event frequencies. Where the export lacks a condition, inject a clearly labeled perturbation into a copy and retain the original. Never describe an injected fault as an observed event.

Have a domain reviewer establish expected facts and whether the evidence supports a draft, independently of model outputs. Separate this adjudication role from blinded output review where feasible. Preserve a frozen reference snapshot, case IDs, athlete/event groups and hashes. Use additional disjoint practice examples for reviewer familiarization; do not train or tune on these 30 evaluation cases. Later revisions require a new evaluation version and fresh cases.

Compare three frozen candidates: deterministic rules/templates, the prompted base model and the adapted model. Provide the same available evidence and task. Record prompts, source selection, model/runtime/quantization, decoding settings, validator version and generation failures. Do not substitute the existing 120-case scores for this replay. The unfinished GPU comparison is a separate experiment.

Each of two reviewers assesses all 90 candidate outputs, giving 180 planned judgments. Anonymize model identity, randomize order and counterbalance candidate order across reviewers. Separate repeated presentations of the same case across sessions to reduce recognition effects. Some carryover remains; disclose it. Record factuality, usefulness, correction time, acceptance, ties and neither-acceptable choices. Keep generation failures and holds in the denominator.

## Required freshness and correction behavior

These are proposed readiness requirements, not capabilities demonstrated by the current brochure screenshot:

| Field or behavior | Requirement |
|---|---|
| Time | Separate event time from received time, include timezone, show last confirmed update and data age. Define race-specific freshness thresholds before replay; there is no universal threshold asserted here. |
| Authority | Preserve source owner, original record ID, record version and evidence link. Distinguish organizer-confirmed, provisional, estimated and corrected values. |
| Corrections | Link superseded records, retain history, invalidate affected candidate claims and require a new review. Do not silently overwrite already approved evidence. |
| Identity | Match event, bib and category; do not confuse overall/category positions or checkpoint IN/OUT times. |
| Delivery faults | Deduplicate repeated events and handle out-of-order arrival. A delayed message must not replace a newer confirmed state. |
| Missing data | State no confirmed update; do not infer that a runner stopped, was injured or withdrew. |
| Projections | Label estimates and their assumptions; do not announce a record achieved from projected pace. |

Western States' [webcast procedures](https://www.wser.org/webcast/) describe manual timer sheets, variable internet access and radio fallback. Reviewed 9 September 2026. This source motivates delivery-fault testing; it is not a connected feed, permission grant or evidence that the project has implemented those mechanisms.

## Measurements and proposed gates

Freeze the final thresholds with participants before collecting outcomes. The values below are proposed product gates, not established standards or measured achievements.

| Measure | Definition and proposed criterion |
|---|---|
| Critical factual errors | False identity, direction of position change, unsupported status/medical assertion, falsely achieved record, or materially wrong cutoff assertion. Proposed gate: zero such assertions in generated drafts before correction. An observed zero in 30 cases is not proof of zero future risk. |
| Other major factual errors | Reviewer-adjudicated materially wrong claims per candidate across all cases. No worse rate than rules. Record both pre-edit errors and any errors remaining in accepted text. |
| Acceptance | Cases ending with a reviewer-accepted brief divided by all cases, including failures and unnecessary holds. Acceptance must be no lower than rules. A justified hold is assessed separately and does not count as an accepted brief. |
| Unnecessary holds | Holds on independently adjudicated draftable cases; report count, denominator and affected condition. Do not reward a model for refusing every case. |
| Review effort | Time from opening evidence/output to accept/reject; include all attempts in totals. Proposed gate: at least 20% lower median review time against the fastest eligible comparator (rules or prompted base) on the shared subset both accept. Also report total review time and coverage over all cases so selective abstention cannot hide work. |
| Cost per accepted brief | (Amortized training + all serving attempts + reviewer labor + retries) / accepted briefs. Include correction labor and declared hardware/spend assumptions. Proposed gate: no higher than the lowest-cost comparator meeting the factuality/acceptance gates. Undefined if no briefs are accepted. |
| Usefulness | Blind ordinal ratings and preference, ties and neither choices; report reviewer disagreement. Treat as exploratory support, not a substituted factuality score. |

Agree an error rubric before review. Adjudicate disagreements without revealing candidate identity if feasible; retain both original judgments and the adjudicated record. Report all cases and per-condition results, paired differences and appropriate uncertainty with group structure. One event and 30 cases cannot validate performance across races. No production promotion is implied even if every pilot gate passes.

## Decision and next steps

If factuality or acceptance gates fail, revise the appropriate source handling, rules, prompt or model behavior and test fresh cases. If no editor-effort benefit appears, keep deterministic handling and investigate a narrower writing task. Only after benefit appears should the team assess broader timing integrations, team access or hosting. RFT requires a validated reward; the current automatic checks miss semantic errors and should not be treated as a complete reward.

To prepare a replay, supply the participation checklist to the project owner and agree the frozen protocol. This is a participation brief, not a working signup form or booked pilot. Expected next evidence: permission record, frozen case manifest, candidate versions, reviewer judgments, timing/cost ledger and an honest go/revise decision.
