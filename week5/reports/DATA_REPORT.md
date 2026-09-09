# Dataset report: provenance, coverage and loss inputs

This report is computed from the checked-in JSONL files. The [600-row inventory](data/dataset-inventory.csv) lists every example's ID, group, split, signal, condition, disposition, token count, evidence/fact counts, approval flag, prompt version and content hash. The [distribution CSV](data/dataset-distribution.csv) contains every split × signal × condition × disposition cell represented in the dataset.

## 1. Data lineage

The [authored generator](../../backend/src/ultramedia/dataset.py) produces fictional episodes and synthetic timing/evidence. This is not a scrape of private athlete data or a collection of editor-approved stories. Provenance records label the examples synthetic and use `CC0-1.0`; the base model's license is separate. A synthetic target that passes automatic checks remains a synthetic reference, not a human-approved training record.

The dataset version is `ultramedia-synthetic-research-v1`, contract `ultramedia-story-v2`, prompt `evidence-editor-v2`. The overall dataset SHA-256 is `5c148b3d1e57a989e38c55e73f1d46ae0b5b17227be154457953bac2dcaef8cf`. The manifest binds the dataset identity to its constituent files:

| File | SHA-256 |
|---|---|
| [train.jsonl](../data/synthetic/train.jsonl) | `0ae633ce602b8fba856b2b9ed7f255b6047c0960ac83c85594d7d416320ea754` |
| [validation.jsonl](../data/synthetic/validation.jsonl) | `5313d54852954cdcce8f40dde1c2fe54071e80c83c90102db45e62414304c6e0` |
| [test.jsonl](../data/synthetic/test.jsonl) | `69995179a6268fe60b1f7b62945f921311ba6c38faa4da3c70fd8a5325d65ffc` |

The [submission checker](../scripts/check_submission.py) regenerates the canonical corpus and compares it with the committed data, verifies notebook syntax and evidence identities, and checks source/report consistency. A changed corpus invalidates old dataset-bound results; do not silently reuse them.

## 2. Split design

| Split | Examples | Independent race groups | Intended use |
|---|---:|---:|---|
| Train | 400 | 100 | Gradient updates on assistant completion targets |
| Validation | 80 | 20 | Epoch loss measurement and best-checkpoint selection |
| Test | 120 | 30 | Frozen generation comparisons after training |
| Total | 600 | 150 | Four signal examples per fictional race group |

Every race group is assigned to exactly one split. The audit records zero shared groups and zero exact message-payload overlaps for train/validation, train/test and validation/test. There are 600 unique message payloads. However, templates, signal definitions, formatting and task structure remain shared across splits. These checks prevent specific forms of leakage; they do not prove independence of all linguistic structure or real-world generalization.

## 3. Signal coverage

| Signal | Train | Validation | Test | Total |
|---|---:|---:|---:|---:|
| position_gain | 100 | 20 | 30 | 150 |
| record_watch | 100 | 20 | 30 | 150 |
| cutoff_watch | 100 | 20 | 30 | 150 |
| pace_change | 100 | 20 | 30 | 150 |

`position_gain` describes changes in overall position. `record_watch` reports a projected record margin without claiming an achieved record. `cutoff_watch` reports the supplied cutoff buffer. `pace_change` interprets the sign of seconds-per-mile change: negative means faster, positive means slower. The output's structured claims must exactly match facts in the cited evidence.

## 4. Evidence-condition coverage

| Condition | Train | Validation | Test | Total |
|---|---:|---:|---:|---:|
| complete | 80 | 16 | 24 | 120 |
| missing | 80 | 16 | 24 | 120 |
| contradictory | 80 | 16 | 24 | 120 |
| misleading_hint | 80 | 16 | 24 | 120 |
| boundary | 80 | 16 | 24 | 120 |

- **Complete:** the requested fact is available and consistent; the target is a supported draft.
- **Missing:** the requested structured fact is unavailable; the target abstains with a reason and no claims.
- **Contradictory:** competing values prevent a supported requested assertion; the target abstains.
- **Misleading hint:** the headline hint encourages an unsupported conclusion; source evidence remains authoritative.
- **Boundary:** edge values test the interpretation of the requested metric without inventing unsupported claims.

Every signal/condition combination has 20 training examples, four validation examples and six test examples. The condition distribution is a deliberate experimental design, not an estimate of how often these situations occur in live races.

## 5. Target distribution

| Disposition | Train | Validation | Test | Total |
|---|---:|---:|---:|---:|
| draft | 240 | 48 | 72 | 360 |
| insufficient_evidence | 160 | 32 | 48 | 240 |

A target includes `disposition`, `eyebrow`, `headline`, `body`, `social_caption`, `citation_ids`, `claims`, and `reason`. A claim contains `metric`, numeric `value`, and `citation_id`. Drafts need a supported claim and citation; abstentions contain no publishable race assertion. Social captions are limited to 280 characters. These are reference behaviors, not a guarantee that the model will follow them.

The [five annotated training records](data/annotated-training-examples.json) are selected as the first `position_gain` training example for each condition. Selection does not inspect test outcomes. Each record retains complete inputs, exact system/user/assistant messages, target JSON, provenance and hashes. They let a reviewer trace evidence → prompt → target without needing to run a GPU.

## 6. Tokenization and supervision

The exact pinned Qwen tokenizer was applied to all 600 message sequences when this report was generated, and the counts match the independent [tokenizer audit](../evidence/tokenizer-audit.json): minimum **476**, maximum **622**, mean **554.02**, total **332412** tokens across one full dataset pass. These counts include prompt and target messages; they are not supervised-token counts, generated-token counts, or total training compute.

The sequence limit is 2048, above the observed maximum of 622. The runner rejects an overlength record rather than silently truncating facts or targets. Packing is disabled. TRL receives a prompt/completion representation; only assistant completion positions contribute to loss. The actual collator checks masking. The checked-in tiny CPU mask test is distinguished from the real GPU collator receipt, which will be captured in the completed training manifest.

## 7. Real editorial data path

The application can preserve original model drafts, reviewed revisions, reviewer identity/notes, consent and rights basis. That is a different source path from the synthetic corpus. A versioned editorial decision does not automatically grant training rights. The data gate requires the appropriate approval and consent conditions; an explicit research flag is used for the synthetic experiment. Automated browser-test approvals have training consent disabled and must never be relabeled human examples.

There are **zero human-approved examples** in this corpus and no completed semantic review. No conclusion about real-race fairness, long-form writing quality, factual entailment beyond the defined checks, or preference of working editors follows from these synthetic labels alone. See the [data card](../DATA_CARD.md) for the production boundary.
