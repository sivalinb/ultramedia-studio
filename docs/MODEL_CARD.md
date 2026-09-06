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

## Training-data gate

Only rights-cleared, human-approved drafts may enter training. The preparation script refuses fewer than 20 approved examples. A credible release should use hundreds to thousands of diverse examples, with race, geography, gender, performance tier, channel, and failure-mode coverage documented.

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

