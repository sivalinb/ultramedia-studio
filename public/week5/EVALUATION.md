# Frozen evaluation protocol

## Question and controls

Compare base Qwen3-4B-Instruct-2507 against its QLoRA adapter on the same frozen evidence packs. Pin revision `cdbee75f17c01a7cc42f958dc650907174af0554`, optimized prompt version, NF4 double quantization, hardware, greedy decoding and maximum new tokens. Base and adapted models are loaded sequentially; their generation time excludes model loading. The rule baseline is a separate software check, never a substitute for base-model results. A prompting-only ablation or LoRA-vs-QLoRA comparison would be a separate explicitly controlled experiment, not an existing claim.

## Metrics

Every attempted example stays in the denominator, including API exceptions, malformed JSON and unsupported outputs. Save raw outputs and parsed predictions per case. Report structured checks individually and their conjunction:

- Schema compliance, including the complete response fields and valid draft/abstention contract.
- Citation-ID validity and exact support for structured numeric claims in the cited evidence.
- Coverage of the requested signal metric.
- Correct draft versus abstention decision given missing or conflicting facts.
- Numeric-token support in all text fields. This checks values, not whether each number modifies the right noun.
- Absence of selected sensitive-language patterns across all text fields.
- No achieved-record assertion inferred from a projection.

These are automatic contract measures. Full claim support, editorial quality, and semantic faithfulness require independent human review. No language model judge is silently substituted for an editor.

Report per-signal and per-condition results, output lengths, truncation/termination reason, latency p50/p95, and GPU peak allocated/reserved memory. VRAM is not host RAM. These are measured when the notebook runs; unavailable values remain absent. Sample p95 over 120 cases is descriptive, not an SLA. The comparison generates a paired 95% bootstrap interval by resampling race groups, preserving within-group dependence.

## Predeclared interpretation

Use the optimized base as the main control. Do not tune from the final test results and reuse them as untouched evidence. Training selects its best checkpoint by validation loss. Report all chosen hyperparameters and any reruns.

For a proposed promotion, require no regression on citation/structured-fact/sensitive-language checks, no automated publication, and a meaningful editorial benefit established by blind comparison. Suggested practical target: editor preference for the adapter above 60% of decided pairs with uncertainty reported, plus reduced correction effort. This is a proposed product criterion, not a course rubric or a promised result. Tie/neither choices and factual failures must remain visible. If the base already performs well or adaptation harms factuality, keep the base.

The software deliberately leaves promotion blocked pending human review. Even a favorable synthetic comparison does not authorize production without representative, rights-cleared editor-reviewed evidence.

## Blind review

The notebook emits `blind-review.json`, `review-inputs.jsonl`, and a separate `review-key.json`. Give the reviewer the first two only. Evaluate every pair against the source pack, record A/B/tie/neither, reviewer identity, claim support, and rationale. Do not infer preferences from the generator's target or mark rows approved automatically. Retain factual failures even when prose is more attractive. The response pair key is for analysis after the review.

## Evidence provenance

The checked-in deterministic report contains actual local rule execution and all 120 predictions. It is expected to score highly on the engineered contract and says nothing about an unrun model. The tokenizer audit downloads only the pinned tokenizer. The notebook has no prefilled execution outputs. Actual model evidence must include `training-run.json`, adapter checksums, base/adapted predictions, token receipts, memory receipts, comparison, and completed human reviews.
