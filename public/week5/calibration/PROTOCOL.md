# Independent calibration and abstention diagnosis

Version: calibration-interactions-v1. This applies the Week 4 feedback to Week 5. Preserve negative results, validate labels and judges independently, then test interactions before choosing a mechanism-specific change.

## Status and separation

The original 120-case comparisons, five smoke probes, production validator, training data and prompts remain frozen. New cases are authored synthetic diagnostics with **proposed labels, not independent human truth**. Model runs before human calibration are exploratory; repeat the frozen protocol after independent labels are locked before making confirmatory claims. No human review is fabricated and no model is promoted by these diagnostics.

## Independent reference labels

Give two reviewers only `independent-label-packet.json` and separate copies of `independent-label-template.json`. Keep proposed labels, model outputs, judge diagnostics and other reviewers' answers withheld. Reviewers choose draft / hold / ambiguous, identify supported facts and explain missing evidence or conflicts. The project owner verifies reviewer independence and locks timestamped responses privately before revealing results. Report raw agreement and disagreements; adjudicate without consulting model identity. Preserve ambiguous cases as a separate stratum rather than forcing a label. Founder feedback is separate from independent labels.

## Judge calibration

Give the same or separate independent reviewers `judge-review-packet.json`, which contains inputs and outputs but no automatic scores or author answers. Record acceptable / unacceptable / ambiguous and a rationale per output. Distinguish semantic correctness from an editorial policy forbidding sensitive words even in denials. An independent factual reviewer may accept a denial while a publication style policy rejects it; publish both dimensions rather than silently changing the definition.

The ten author challenges cover correct and reversed direction, supported projection versus achieved record, fabricated citations, appropriate and inappropriate holds, and sensitive assertions versus denials. `judge-diagnostic.json` measures disagreement with author expectations only. It is not an independently measured evaluator accuracy. After adjudication, report false accepts / human-unacceptable outputs and false rejects / human-acceptable outputs, including counts, denominators and error types; ambiguous labels remain separate. Use a distinct fresh check set to validate any revised evaluator, then freeze that evaluator before evaluating a model revision.

## Paired interaction design, frozen before model inference

Eight fictional source episodes (two per signal) each have six cells: complete, missing or contradictory evidence crossed with neutral or misleading hint. Total 48 cases per variant. The hint-only pair has byte-identical evidence and timing; evidence changes are explicit interventions. Metric sign conventions are stated in evidence to reduce the known projection ambiguity. All prompts receive source packs directly: this experiment does not manipulate a retrieval system and cannot establish a retrieval mechanism.

Run the exact previously verified local base, adapter and deterministic rules. Use existing serving prompt v1, JSON-schema constraints, temperature 0, seed 42 and max 1024 tokens. Freeze input/runner hashes and Git commit before inference. Preserve first attempts, errors and truncated responses. No retries chosen for score. Runs on the same Mac may overlap, so latency is diagnostic only and must not be used as a speed comparison.

Report unnecessary holds on complete evidence, unsupported drafts on missing/contradictory evidence, invalid/error outcomes separately, paired hint-induced decision flips and all-check pass counts. A changed answer can be from draft to invalid as well as draft to hold; preserve all transitions. The primary hint effect is the difference in unnecessary-hold counts between misleading and neutral hints on complete evidence. Also report per-signal and source-group cells. Eight groups are a small authored pilot, not population generalization or independent calibration.

## Evidence-led next change

Hypothesis, not conclusion: misleading hints may cause over-abstention. If paired results show that effect without changing evidence, test one versioned instruction to reject unsupported hints while retaining supported source facts. If neutral complete cases also fail, investigate schema/task interpretation or learned abstention behavior rather than assuming a hint mechanism. If labels or judge calibration disagree, resolve those before claiming model improvement. Do not retrain or change the production policy from aggregate score alone.

After independent calibration, repeat interaction tests under the frozen protocol. Any prompt or training change requires a new version and fresh evaluation cases. Release remains blocked until independent label/judge review, acceptable semantic quality and the project's editorial gate are satisfied. No numerical release threshold is invented here; agree on it before the confirmatory run.
