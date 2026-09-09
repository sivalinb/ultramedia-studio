# Week 5 project: UltraMedia Race Desk

**Teach a small model when to draft and when to ask for evidence.** During a live race, an editor receives scattered timing updates. UltraMedia turns supported evidence into a cited draft and flags insufficient evidence for review. Current facts come from supplied evidence; training specializes response behavior.

![Data, fine-tuning, evaluation and editorial flow](../diagrams/week5-flow.svg)

## Read in five minutes

1. [Exact handout mapping](HANDOUT_MAPPING.md): all six lab phases and deliberate custom choices.
2. [Disposition classification report](../reports/DISPOSITION_RESULTS.md): precision, recall, F1 and confusion matrices from all 120 saved local cases per model.
3. [Five fresh task-level probes](../reports/HANDOUT_SMOKE_RESULTS.md): actual rules/base/adapter outputs; failures stay visible.
4. [Business decision](BUSINESS_CASE.md): what rules already solve, measured model latency, explicit cost assumptions and why production promotion is pending.
5. [Demo and submission](DEMO_AND_SUBMISSION.md): a timed script, the exact deadline, assets and remaining human actions.

[Gap closure register](GAP_STATUS.md): completed work and remaining external evidence.

## What is implemented

A versioned synthetic dataset; actual QLoRA training; completion-only masking; held-out base/adapted comparisons; checksummed adapters; merge and local inference; a review workflow; raw outputs and reproducible verification. These are implemented and evidenced. A model response is never an automatic publication.

## Where everything lives

| Folder | Contents |
|---|---|
| `week5/project/` | Handout mapping, decision record, submission script, smoke inputs and reviewer protocol |
| `week5/diagrams/` | Standalone SVG and text flow |
| `week5/data/` | Frozen 600-example training/validation/test corpus |
| `week5/notebooks/` | Portable Colab/Kaggle training notebook |
| `week5/evidence/` | Actual raw training, model comparisons, browser tests and new task probes |
| `week5/reports/` | Methodology, data, loss curves, classification, failures and CSVs |
| `week5/scripts/` | Runners, metric derivation, artifact builders and independent verification |

The original benchmark remains frozen. New smoke probes are explicitly post-training author-authored diagnostics, not an independent human-validated benchmark. The four race signal types are inputs; the predicted decision has two classes: `draft` and `insufficient_evidence`.
