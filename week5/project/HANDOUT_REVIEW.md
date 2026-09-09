# UltraMedia: Week 5 handout mapping and gap review

Reviewed September 9, 2026. Source: all four pages of **Week 5 Project Handout (Aug 2026).pdf**, including the tables and highlighted deadline, extracted and visually inspected. Project evidence snapshot: Git commit `9e544998e91a097ef0ac5ce016eb4f0f5fbd15c1`, public version 14, and the recovery status last checked at 13:26 UTC. This is an assessment, not a claim that the remaining changes have been implemented or submitted.

## Assessment

UltraMedia is a credible **custom Week 5 fine-tuning project**. It already demonstrates actual parameter-efficient training, controlled comparisons, model merging, and application inference. The handout explicitly permits custom ideas with a GitHub link containing assets and a Loom video (page 4). Rebuilding the project as an IT ticket router is unnecessary for the custom route.

The strongest gaps are the explanation of why fine-tuning is useful beyond deterministic rules, task-level classification reporting, semantic editorial evaluation, and a clear narrated submission video. The remaining GPU comparison is an outstanding self-declared experiment; it is not an explicit requirement that the handout asks every participant to run three comparisons.

The handout describes a pass/fail evaluation and provides no scored Builder of the Week rubric. This review identifies evidence and presentation strengths; it cannot establish award eligibility beyond the stated submission instructions or guarantee selection.

## What the handout actually asks

The standard lab trains `Qwen/Qwen3-1.7B-Base` to assign one of seven ticket labels: Active Directory, Computer-Services, EOL, Fileservice, O365, Software, and Support general. The prediction determines a downstream queue; the model does not write a customer response. Its business motivation is a useful smaller model rather than repeated expensive general-model routing.

The six phases are installation on a free T4, labeled-data preparation, LoRA training in LLaMA Board, loss review, adapter merge and smoke testing, and held-out evaluation against the unadapted base. The specified evaluation views include precision, recall, F1, support, a confusion matrix, five obvious smoke-test tickets, and a baseline prompt constrained to avoid label-format failures.

The PDF states a deadline of **Sunday, September 13, 2026, 11:59 p.m. PT**, with submission through [the linked form](https://forms.gle/7Hpa2Pkd8ZaWUomm6). The standard submission is a Google Doc with a screenshot of a successful notebook run; the custom alternative is GitHub assets and a Loom video. The PDF says completion is not required for the certificate and individual feedback will not be provided.

The project-notebook repository linked in the PDF could not be retrieved during this review (web fetch failed and the GitHub README request returned 404). Therefore the mapping below relies on the fully inspected PDF, not an assertion that the linked notebook was read.

## Requirement-to-evidence mapping

| Handout item | UltraMedia evidence | Assessment and remaining gap |
|---|---|---|
| Practical narrow task and downstream action, pp. 1-2 | Given race evidence, produce a cited draft or `insufficient_evidence`; drafts require editor review | Good custom analogue. Explain the editorial decision before showing architecture. Signal type is supplied in the input; do not claim the model learns four-way signal routing. |
| Free T4 and dependency installation, p. 2 | Actual Colab T4 training, pinned requirements, environment and recovery manifests | Demonstrated. Current capacity prevents recovery of the last control arm; it does not invalidate completed training. |
| LLaMA-Factory and LLaMA Board, pp. 2-3 | Custom TRL/PEFT/bitsandbytes training runner and notebook | Deliberate tooling departure. Document the conceptual correspondence. No executed LLaMA Board run is present; do not claim one. The custom allowance supports a custom approach, but the PDF does not explicitly waive each individual lab choice. |
| Qwen3-1.7B-Base, pp. 2-3 | Pinned Qwen3-4B-Instruct-2507 | Deliberate model departure. Explain instruction-following structured generation versus label-only routing and the larger model's resource tradeoff. No 1.7B comparison was performed. |
| `support_tickets.csv`, stratified 80/20 split, ShareGPT JSON, `dataset_info.json`, pp. 2-3 | 600 versioned chat examples, 400/80/120 train/validation/test, race-group isolation, balanced signals and conditions, hashes and provenance | Equivalent data-preparation learning with an additional test split. It is not the exact 80/20 or LLaMA-Factory registration workflow. Keep the stronger group isolation; do not re-split the completed experiment to mimic the lab. |
| LoRA and meaningful training settings, p. 3 | QLoRA rank 16, alpha 32, dropout .05, learning rate .0002, two epochs, batch 1 and accumulation 8 | Demonstrated. Explain QLoRA as LoRA over a quantized frozen base, and effective batch size. No hyperparameter sweep is required or claimed. |
| Loss curve and review, pp. 2-3 | 100 steps, both epoch validation losses, selected checkpoint 100, logs, historical checkpoint-90 and final curves | Demonstrated. Make final results the first view; keep interim material clearly historical. Low template loss is not editorial quality. |
| Adapter merge and standalone inference, pp. 2-3 | Adapter checksums, pinned-base merge, GGUF conversion lineage, actual local application inference | Demonstrated. Quantization is an additional serving step; base and adapted local variants used matching conversion tooling. Large model files are retained separately from Git. |
| Five obvious smoke tests, p. 4 | 13 browser software checks and a separate six-case workflow suite | Partial. The six-case suite contains four retrieval and two generation cases; it is not five successful task-level model smoke tests. Record five clear custom-task cases and show actual expected/observed decisions. |
| Precision/recall/F1/support and confusion matrix, pp. 3-4 | Nine automatic checks and subgroup rates; saved disposition predictions | Reporting gap. This review derives the binary disposition classification report below without new inference. Integrate it into the Git reports and public evidence. Keep writing-quality checks alongside it. |
| Same-base comparison, p. 4 | Original GPU 44/120 versus 120/120; matched local 76/120 versus 109/120 all-check success | Demonstrated with limits. Lead with the matched local comparison because both variants have 100% schema validity; it avoids attributing the whole gain to formatting failures. |
| Format-resistant baseline, p. 4 | Identical local JSON-schema constraints for base and adapter; separate explicit-schema GPU control | Local comparison provides a strong analogous control. Merely appending a schema to the GPU prompt is not constrained decoding. Its base arm is 36/120 all-check success; the adapter arm is pending. Do not describe that prompt as empirically stronger. |
| Class confusions and asymmetric error costs, p. 4 | Missing/contradictory inputs should abstain; misleading hints reveal over-abstention | Partial. Report unsupported draft decisions separately from unnecessary abstentions and relate each to the editor's work. |
| Faster/cheaper systems decision, p. 1 | Local p50 4.622s base versus 1.801s adapter; GPU time/memory receipts | Partial. Output lengths differ. No end-to-end editor time, cost per accepted brief, representative workload, or measured break-even analysis exists. Free compute is not proof of zero total operating cost. |
| Custom GitHub assets plus Loom, p. 4 | Detailed reports, raw predictions, notebook, datasets, browser recordings, public evidence page | Git assets are strong. No Loom link was found in reviewed project materials; browser `.webm` recordings are not evidence of a submitted Loom. PR #2 remains draft. |
| Submission by deadline, pp. 1, 4 | Submission guide and public page exist | Actual form submission is not evidenced. This review does not submit anything. |

## Classification results recoverable now

This is a **post-hoc descriptive analysis** of the already saved matched-local predictions, not a newly predeclared experiment or replacement for the frozen nine-check metric. The script verifies all 120 case identities, group IDs, input hashes, saved raw dispositions and consistency with the existing disposition check. There are 72 reference drafts and 48 reference abstentions.

| Metric | Base | Adapted |
|---|---:|---:|
| Disposition accuracy | 83.33% | 90.83% |
| Macro F1 | 0.8326 | 0.9072 |
| Draft precision | 96.43% | 100.00% |
| Draft recall | 75.00% | 84.72% |
| Draft F1; support 72 | 0.8438 | 0.9173 |
| Abstain precision | 71.88% | 81.36% |
| Abstain recall | 95.83% | 100.00% |
| Abstain F1; support 48 | 0.8214 | 0.8972 |

Confusion matrices use true classes as rows and predictions as columns:

| Reference | Base: draft | Base: abstain | Adapter: draft | Adapter: abstain |
|---|---:|---:|---:|---:|
| Draft | 54 | 18 | 61 | 11 |
| Insufficient evidence | 2 | 46 | 0 | 48 |

Neither local arm has invalid-schema outputs. Other comparisons must keep invalid outputs in an explicit failure category rather than silently dropping them.

The adapted model eliminates the two unsupported draft decisions in this sample and reduces unnecessary abstentions from 18 to 11. All 11 remaining adapter decision errors occur under misleading hints. This is bounded synthetic evidence; 0/48 observed failures is not a guarantee of zero risk.

**Do not conflate the metrics:** disposition accuracy improves by **7.5 percentage points**, while the conjunction of nine checks improves by **27.5 percentage points**. The latter is not classification accuracy, semantic accuracy, or an editor-preference score.

Reproduction files supplied with this review:

- [Analysis JSON](../reports/data/handout/UltraMedia-Week5-Disposition-Analysis.json), including source hashes.
- [All 240 model-case rows](../reports/data/handout/UltraMedia-Week5-Disposition-Cases.csv).
- [Derivation script](../scripts/derive_disposition_metrics.py); run with the repository path and desired output directory.

## Highest-impact gaps, in priority order

### 1. Make the fine-tuning value case defensible

The deterministic provider already passes **120/120** cases on the engineered contract. Its implementation shares task rules with the synthetic targets, so this is not independent evidence of general editorial ability. Nevertheless, a reviewer can reasonably ask why an LLM is needed when rules suffice for these cases.

Retain deterministic evidence and explicitly separate **evidence sufficiency/routing**, which rules can often handle, from **useful wording and editorial effort**, where learned behavior might add value. Measure editor corrections, acceptance, readability and factual meaning on a new, independently authored, rights-cleared evaluation set. Compare rules, prompted base and adapter. Freeze the new evaluation before evaluating it; do not train or prompt-tune on the old held-out failures and call a rerun untouched evidence.

Acceptance evidence: a documented keep-rules/keep-base/use-adapter decision based on observed quality and cost. A negative result is valid. A second model or paid GPU alone does not close this gap.

### 2. Integrate the classification view

Add the report and confusion matrices above to the Git evidence and public learning map. Use `draft` versus `insufficient_evidence` as the predicted task classes. The four race signal types are input strata, not four learned output classes. Introduce no fictional routing component or invented seven-class metric.

Acceptance evidence: every reported count traces to saved predictions; class errors, malformed outputs and denominators remain inspectable.

### 3. Demonstrate semantic quality and five real model smoke tests

All-check success is narrower than correct prose. In `fictional-race-120-position_gain`, the local base describes movement from 34th to 35th as gaining a place, while its structured numeric claim is -1; all automatic checks still pass. The adapted output correctly says lost but includes the grammatical error “lost 1 places.” These are concrete reasons to inspect meaning and language separately.

The application also retains a failed adapted record-watch case that omits the required projection metric and chooses the wrong disposition. Diagnose it without hiding or replacing the recorded failure. Any future prompt/model repair should have a separate version and fresh evaluation.

Recommended five smoke scenarios: supported position change, supported projected record with no achievement claim, missing metric, contradictory evidence, and a misleading hint with sufficient evidence. Require observed outputs and decisions, not screenshots of a UI alone. Human review is a valuable custom-project strength and a project-defined production gate; the PDF does not make it a universal submission prerequisite.

### 4. Make the story understandable and record the Loom

Recommended title: **UltraMedia Race Desk: teach a small model when to draft and when to ask for evidence.**

Suggested opening: “During a live race, an editor receives scattered timing updates. UltraMedia turns supported evidence into a cited draft, flags missing evidence, and keeps the editor in control.” This describes the intended use; it does not assert measured staffing savings.

Suggested 3-4 minute Loom structure (duration is a recommendation, not a handout rule):

1. Show the editor's problem and one before/after example in plain language.
2. Trace one labeled training example through LoRA training, the real final loss curve, merge and inference.
3. Show the matched base/adapted comparison and disposition confusion matrix; define the metric.
4. Show one remaining failure and how the app rejects or holds it for review.
5. End at the GitHub report index, reproduction path and explicit research release status.

Give viewers three clear choices on the public page: **Watch the walkthrough**, **Inspect a recorded example**, and **Reproduce the experiment**. Preserve recorded replay labeling; the public evidence site currently does not host the Python model endpoint. Live GPU hosting is not stated as a handout requirement and is lower priority than a clear walkthrough and reliable artifacts.

### 5. Close the experiment and release bookkeeping

Complete the interrupted explicit-schema adapter arm when compatible capacity returns, preserving trained weights, settings, saved base outputs, and any cross-session timing limitation. The original GPU and matched local comparisons already exist; do not misrepresent the pending control as a handout demand for three experiments.

Current Git documents still contain snapshot text saying the control is running; recovery state says interrupted awaiting T4 capacity. Separate current status from historical logs, make final training the lead view, and rename “stronger” to “explicit-schema” where empirical strength is not established. Refresh Git reports, checksums, model card, public downloads and current-state labels, then pass final checks and merge PR #2 under the existing authorization. Preserve historical snapshots.

### 6. Make compute and data claims realistic

Document measured latency with generated lengths and workload conditions. Build an explicitly labeled cost scenario only with sourced rates or actual spend; include amortized training, serving, failures and editor rework. Do not claim “cheaper than frontier models” without a relevant measured or transparently assumed comparator.

All 600 existing examples are synthetic and use repeated structure; zero are human-approved. Add independent editor review and a fresh challenge set to support usefulness claims. Do not erase the synthetic provenance or silently change the frozen corpus. The handout does not require a particular extra dataset size, additional model family, DPO, RLHF, or a LoRA-versus-QLoRA ablation.

## Recommended completion order

1. Incorporate this handout-specific map and the derived classification report; make the custom model/tool/split substitutions explicit.
2. Correct current status labels, show five task-level smoke tests, and prepare the plain-language walkthrough using actual evidence.
3. Obtain independent editorial assessment of new examples to test usefulness beyond the rules baseline; retain failures and measured uncertainty.
4. Finish the already declared GPU control when feasible; do not let extra experiments displace the required submission packaging.
5. Record and link the Loom, finalize evidence, merge and publish, check anonymous access, and submit through the stated form before the handout deadline.

The engineering work is substantial. The most valuable next improvement is making its task, comparison, limitations and user benefit immediately clear, with evidence that answers why this model should be used.

## Existing project evidence

- [Git report index](https://github.com/sivalinb/ultramedia-studio/tree/codex/week5-submission/week5/reports)
- [Matched local results](https://github.com/sivalinb/ultramedia-studio/blob/codex/week5-submission/week5/reports/LOCAL_COMPARISON_RESULTS.md)
- [Dataset report](https://github.com/sivalinb/ultramedia-studio/blob/codex/week5-submission/week5/reports/DATA_REPORT.md)
- [Deterministic report](https://github.com/sivalinb/ultramedia-studio/blob/codex/week5-submission/week5/evidence/deterministic-test/report.json)
- [Local base predictions](https://github.com/sivalinb/ultramedia-studio/blob/codex/week5-submission/week5/evidence/local-comparison/test-base/predictions.jsonl)
- [Application evidence](https://github.com/sivalinb/ultramedia-studio/tree/codex/week5-submission/week5/evidence/adapter-serving)
- [Public Week 5 evidence](https://ultramedia-studio.siva-babu.chatgpt.site/week5)
- [PR #2](https://github.com/sivalinb/ultramedia-studio/pull/2)
