# UltraMedia Studio — Week 5 submission

**Project:** Evidence-grounded editorial specialization with QLoRA.

**Question:** Can a small adapted model write more consistent, useful race briefs than the same base model with a strong prompt and frozen evidence, while preserving facts and appropriate abstention?

## Submission status

The application, dataset, experiment runner, notebook, and local evidence are implemented. GPU training and the base-versus-adapter model comparison are **not run**. The owner requested a Colab/Kaggle notebook to execute those steps. No trained adapter, human-approved example, editor preference, or model-quality improvement is claimed in this source package.

This is a runnable research submission with measured software/data evidence. It becomes a completed fine-tuning experiment only when the notebook produces an actual adapter and held-out results. An honest negative result is acceptable: retain the base model if the adapter adds no value.

## What the project demonstrates

| Week 5 concept | Concrete implementation | Evidence |
|---|---|---|
| Behavior versus knowledge | Writing behavior in the adapter; current facts in supplied timing/evidence | Shared input/output contract and saved evidence snapshots |
| SFT | Chat prompt plus assistant-only completion target | 600 versioned synthetic examples; shared prompt formatter |
| LoRA / QLoRA | Rank 16, alpha 32, attention and MLP projections; NF4 double quantization | GPU runner and pinned notebook; actual run pending |
| Dataset governance | Provenance, original evidence, opt-in corrected revisions, independent race groups | Data card, manifest, audit, editor API tests |
| Evaluation | Frozen base/adapted comparison, failed outputs retained, paired group bootstrap | Deterministic evidence now; model predictions after notebook |
| Overfitting and leakage | Separate train/validation/test groups and validation checkpoint selection | Split hashes, overlap checks, training curves after notebook |
| Serving | Adapter checksums, lineage-aware merge, GGUF comparison protocol and rollback | Merge script and serving guide; merged artifact pending |
| Model card / release decision | Unmeasured fields stay null; no automatic production promotion | Evidence snapshot, model card, comparison gate |

The teaching lab's intent-classification pattern becomes a structured drafting/abstention task. This is QLoRA SFT, not pretraining, RLHF, DPO, or an unperformed LoRA-vs-QLoRA ablation.

## Files to submit

- `week5/notebooks/UltraMedia_Week5_QLoRA.ipynb`: portable Colab/Kaggle workflow with no fabricated outputs.
- `week5/data/synthetic/`: 400 train, 80 validation, 120 test examples and SHA-256 manifest.
- `week5/evidence/`: executed local checks, complete deterministic predictions and tokenization audit.
- `week5/DATA_CARD.md`, `EVALUATION.md`, `SERVING.md`: provenance, limitations, protocol and reproducibility.
- `backend/src/ultramedia/`: shared contract, dataset audit, real-model experiment runner and application implementation.
- `backend/tests/`: behavior tests including editorial revisions, tampering, unsupported claims, and abstention.
- `week5/runs/<run>/`: **add after running the notebook** — adapter, training manifest, curves, base/adapted predictions, measured memory/tokens, comparison and completed editorial reviews.

## Run the notebook

1. Open the notebook in Colab or Kaggle and enable a CUDA GPU and Internet.
2. Upload `ultramedia-week5-source.zip`; on Kaggle attach it as an input dataset. The setup cell finds the archive and installs the exact direct training dependencies.
3. Inspect the data and predeclared settings, run training, then the held-out comparison. The trainer checks the real loss mask, avoids silent sequence truncation, evaluates every epoch and saves the best validation-loss adapter.
4. Download the generated result ZIP before the session ends. Retain failures and the full environment manifest.
5. Complete blind editorial review using the supplied response pairs and source inputs. Keep the answer key separate until the review is complete.
6. Update the submission with observed results and a reasoned keep-base/promote decision. A synthetic-only run cannot authorize production.

The direct dependencies are pinned; `training-run.json` records every relevant resolved version and CUDA/GPU details. The Qwen model revision is immutable. A target-model GPU run is not claimed to have been validated locally. Hosted runtime availability and memory sufficiency must be checked in the notebook.

## Reproduce local checks

From the repository root, using Python 3.11 or 3.12:

```bash
python -m venv .venv
.venv/bin/python -m pip install -e 'backend[dev]'
.venv/bin/python -m pytest backend/tests
PYTHONPATH=backend/src .venv/bin/python week5/scripts/check_submission.py
PYTHONPATH=backend/src .venv/bin/python -m ultramedia.benchmark --output week5/runs/rules-recheck
npm ci --registry=https://registry.npmjs.org
npm run build
```

The checked-in npm lockfile was truncated in the starting repository; it was regenerated from the existing pinned package manifest. No dependency registry configuration on the host was changed.

## Demonstration narrative

1. Open `/week5`: show the dataset counts, evidence conditions, provenance and the explicit untrained state.
2. Inspect a supported signal, then a conflicting or missing signal. Show why abstention is the correct target.
3. Open `/studio` with the Python API configured: generate a draft, correct wording, enter reviewer identity and notes, and save a versioned review. Training consent and rights basis are separate explicit fields.
4. Show the model notebook and, when available, its actual adapter, validation curve and paired held-out results.
5. Explain one improvement and one failure with source evidence. Close with the release decision and the base-model rollback path.

The hosted web interface cannot execute Python or GPU training. It displays recorded evidence and calls the separately configured Python API. Its preview never pretends to have saved reviews or run a model.

## Boundaries

All supplied race episodes and athletes are fictional. The automatic checks verify the structured numeric facts, allowed citations, required signal, selected unsafe-language patterns, and abstention contract. They do not establish general semantic entailment, calibrated confidence, fairness across real athletes, or medical safety. Human approval means editorial review, not automatic publication. No race result is officially adjudicated by this application.
