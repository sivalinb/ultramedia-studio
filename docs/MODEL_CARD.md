# Model card: UltraMedia Qwen3 adapter

## Base model

Qwen/Qwen3-4B-Instruct-2507, Apache-2.0. The local demo can use the Ollama `qwen3:4b-instruct` package. The fine-tuning scripts use 4-bit NF4 QLoRA with targeted attention and MLP projection modules.

## Intended use

- Structured ultramarathon story drafts
- Broadcast briefs and social captions
- Citation-aware editorial formatting
- Abstention and human-handoff behavior

## Out of scope

- Medical or safety diagnosis
- Athlete intent, emotion, credibility, or misconduct inference
- Official rankings or timing adjudication
- Automated publication
- Personalized training or nutrition advice

## Week 5 research status

The runnable experiment and current evidence live in [`../week5/SUBMISSION.md`](../week5/SUBMISSION.md). The 600 synthetic examples are a separately flagged research corpus, not human-approved production data. Training completed 100 steps. The original GPU comparison is 44/120 base versus 120/120 adapter; the matched local comparison is 76/120 versus 109/120. The explicit-schema GPU control was interrupted during its adapter arm and awaits compatible Colab capacity; its completed base outputs are retained. All scores are automatic checks on 120 synthetic cases per model, not human editorial preference. The actual adapter passed 13 browser software checks; its separate application quality suite still fails one generation case. Human review and production promotion remain pending. The corrected output contract includes explicit abstention and structured numeric claims.

## Training-data gate

Only rights-cleared, human-approved drafts may enter training. The preparation script requires 20 consenting approved examples from three independent race groups. Production-mode training requires 200 approved train/validation examples and an approved test split. A credible release should use hundreds to thousands of diverse examples, with race, geography, gender, performance tier, channel, and failure-mode coverage documented.

## Evaluation before release

- Retrieval recall and expected-source coverage
- Claim-level citation validity and faithfulness
- Numeric exactness for ranks, splits, cutoffs, and elevation
- Unsupported sensitive inference rate: zero tolerance
- Human-review-gate enforcement: 100%
- Channel style and length adherence
- Counterfactual fairness across synthetic identity attributes
- P95 latency and provider failure behavior

QLoRA should ship only when it beats prompt-plus-RAG on predeclared thresholds. Otherwise the simpler system remains the production candidate.


## Measured evidence and limitations

See the [detailed fine-tuning reports](../week5/reports/README.md), [original GPU results](../week5/reports/ORIGINAL_GPU_RESULTS.md), and [matched local results](../week5/reports/LOCAL_COMPARISON_RESULTS.md). Original-prompt formatting failures inflate the apparent training gap; prioritize the stronger shared-prompt control once complete. Synthetic template repetition, a single training seed, bounded lexical checks and unmeasured editorial preference limit generalization. Final model-byte checksums, conversion lineage and actual serving failures are preserved.
