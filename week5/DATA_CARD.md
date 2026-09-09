# UltraMedia synthetic research data card

**Version:** `ultramedia-synthetic-research-v1` · **License:** CC0-1.0 for the newly authored synthetic records.

**Provenance:** Programmatically authored fictional race episodes and target briefs. No real athlete data, private customer prompts, scraped article text, or third-party model outputs were used to produce this corpus. The original application's attributed course references are separate from this dataset. Human-approved examples: **0**. Automatic validation is not human review.

## Composition

600 examples, 150 fictional race episodes and athletes, four signal types per episode. Each type has 150 examples: position gain, record watch, cutoff watch, and pace change. Five conditions have 120 examples each: complete evidence, missing evidence, conflicting evidence, a misleading instruction in the headline hint, and a zero/boundary measurement. Drafting and abstention are both supervised. Claims retain signed values; prose explains the direction.

| Split | Examples | Race groups | Use |
|---|---:|---:|---|
| Train | 400 | 100 | Gradient updates |
| Validation | 80 | 20 | Checkpoint selection and development |
| Test | 120 | 30 | Frozen final base/adapted comparison |

Each group stays in one split. Athlete identities are disjoint by construction. Content checksums cover the complete messages. The manifest records each file hash and the dataset hash. The audit rejects shared groups, duplicate IDs, exact cross-split payload matches, altered files and input/target format mismatches. It validates every reference response against the same bounded contract used at runtime.

## Record schema

Each JSONL row contains `id`, `group_id`, `split`, `contract_version`, `prompt_version`, `inputs`, `output`, `messages`, `content_sha256`, `provenance`, and `human_approved`. `inputs` contains exactly `moment`, `timing`, and `evidence`; `messages` is produced by the runtime formatter. No gold disposition or output is passed to the inference function.

Targets contain `disposition`, `eyebrow`, `headline`, `body`, `social_caption`, `citation_ids`, `claims`, and `reason`. Each structured claim has a metric, signed numeric value, and citation ID. An insufficient-evidence target has no factual claims and states its reason.

## Important limitations

Templates, task structure, vocabulary, and metric definitions are shared across splits. Exact/group decontamination does not establish semantic independence. The tests are intentionally a controlled synthetic research environment. The corpus does not contain realistic noisy vendor timing feeds, multilingual reports, genuinely independent editor styles, or enough evidence to infer population-level fairness. Record-watch margins and pace deltas are supplied fictional measurements, not predictions from a validated race model. A near-duplicate semantic detector or human sample review is still appropriate before adding external data.

Do not interpret high rule-baseline performance as learned writing or generalization. The generator and automatic checker share the declared contract. An expert-authored challenge set using independently sourced, rights-cleared evidence should be added before real use.

## Editor-reviewed production corpus

The application stores the exact generation input and output in an additive generation table. Every review preserves before/after responses, reviewer, rationale, revision number, and optional training consent/rights basis. Exports include only the currently approved revision with consent and a nonempty rights basis; legacy stories without original evidence cannot enter training.

```bash
PYTHONPATH=backend/src python backend/scripts/prepare_training_data.py --database-url sqlite:///backend/ultramedia.db --output week5/data/reviewed
```

Export requires at least 20 consenting examples from three independent race groups. Production-mode training separately requires at least 200 approved train/validation examples and an approved test split. These are implementation gates, not claims of statistical adequacy. The synthetic notebook uses an explicit research-only flag and cannot turn synthetic records into human-approved data.

Only the latest corrected target enters an export. Earlier revisions remain audit evidence; they must not be scattered across train and test. Reviewer identity and permissions may be sensitive in real data: review exports before sharing. The supplied public research corpus contains no actual reviewers.
