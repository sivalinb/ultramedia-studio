# Week 5 handout → custom implementation → evidence

Source: all four pages of **Week 5 Project Handout (Aug 2026).pdf**, reviewed September 9, 2026. The PDF explicitly allows custom projects with GitHub assets and a Loom video. It specifies pass/fail, not a numerical award rubric. This is a custom implementation, not a claim of executing the exact standard notebook.

| Phase / handout page | Standard lab | UltraMedia | Inspect |
|---|---|---|---|
| Business task, 1–2 | Ticket → resolver queue; no customer response | Evidence → cited draft or evidence hold → human editor | [Project guide](README.md), [flow](../diagrams/week5-flow.svg) |
| 1. Install, 2 | Free T4; LLaMA-Factory | Actual Colab T4; pinned TRL/PEFT/bitsandbytes | [Training report](../reports/FINE_TUNING_REPORT.md) |
| 2. Data, 2–3 | CSV, stratified 80/20, ShareGPT and dataset_info.json | 600 chat examples; group-isolated 400/80/120; explicit manifests | [Data report](../reports/DATA_REPORT.md) |
| 3. Train, 2–3 | LLaMA Board, Qwen3-1.7B-Base, LoRA | Qwen3-4B-Instruct-2507; QLoRA rank 16; completion-only SFT | [Notebook](../notebooks/UltraMedia_Week5_QLoRA.ipynb) |
| Settings, 3 | Understand LR, epochs, batch, rank | LR .0002; 2 epochs; batch 1 × accumulation 8; rank 16 | [Configuration and receipts](../reports/FINE_TUNING_REPORT.md) |
| 4. Review, 2–3 | Inspect loss | 100 steps; two validation losses; selected checkpoint 100 | [Final loss curve](../reports/data/final-training/training-loss.png) |
| 5. Merge, 2–4 | ADAPTER_DIR, merge, classify(), five smoke tickets | Hash-verified merge to standalone GGUF; five new task probes | [Serving](../SERVING.md), [smoke results](../reports/HANDOUT_SMOKE_RESULTS.md) |
| 6. Evaluate, 3–4 | Class precision/recall/F1/support, confusion matrix, same-base accuracy | Binary draft/hold report plus nine separate structured checks | [Classification](../reports/DISPOSITION_RESULTS.md) |
| Fair baseline, 4 | Constrained letter-choice prompt | Both local variants use identical JSON-schema constraints | [Matched local report](../reports/LOCAL_COMPARISON_RESULTS.md) |
| Business value, 1 | Faster/cheaper useful model | Actual latency and explicit rules/base/adapter decision; human effort unmeasured | [Business case](BUSINESS_CASE.md) |
| Submit, 4 | Google Doc + run screenshot; custom alternative GitHub + Loom | Git reports, actual loss/run evidence, browser video, walkthrough script; Loom remains pending | [Submission checklist](DEMO_AND_SUBMISSION.md) |

## Deliberate custom choices

- **Task:** structured editorial drafting plus a binary abstention decision instead of seven-way IT routing. Do not report the four supplied signal types as model-predicted categories.
- **Model:** 4B Instruct supports structured generation; no evidence shows it is superior to the lab's 1.7B model. The larger resource footprint is a tradeoff.
- **Tooling:** a scripted TRL/PEFT workflow replaces the Board UI and records exact settings/recovery. No LLaMA Board screenshot or execution is claimed.
- **Data format:** versioned chat JSONL replaces CSV registration; the extra frozen test set prevents using checkpoint-selection validation as the final comparison.
- **Quantization:** QLoRA trains a small adapter over a frozen NF4 base. Local GGUF serving is a separately matched quantization/runtime experiment.

The PDF's custom allowance supports a custom project; it does not explicitly enumerate exceptions for every lab setting. These differences are transparent for the reviewer. No extra GPU model, live hosting, DPO, RLHF, or three-comparison requirement is stated in the handout. Three comparisons are our own research commitment.
