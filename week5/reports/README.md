# Fine-tuning reports and evidence

Report snapshot: **2026-09-09T07:31:52.453945+00:00**. Training has now completed all 100 steps; the verified completion update is in the fine-tuning report. The checkpoint **90/100** snapshot is retained as historical evidence. The matched local comparison is complete: 76/120 base versus 109/120 adapter (27.5 percentage points; paired 95% interval 20.0–35.0). The stronger GPU prompt control remains pending. Update the interpretation after all declared comparisons have been independently verified; preserve this progress snapshot as historical evidence.

| Report | Contents |
|---|---|
| [Fine-tuning report](FINE_TUNING_REPORT.md) | Research question, actual configuration, loss curve, experiment controls, recovery history, results status and limitations |
| [Data report](DATA_REPORT.md) | All 600 examples, split/condition/signal counts, token lengths, hashes, provenance, targets and leakage limits |
| [Flow and reproduction](FLOW_AND_REPRODUCIBILITY.md) | Training, evaluation, deployment and editorial-flow diagrams; runnable commands and artifact verification |

[Verified local comparison](LOCAL_COMPARISON_RESULTS.md): all 120 cases per model, all nine metrics, subgroup results, remaining failures, raw predictions and conversion lineage. The earlier [local-base report](LOCAL_BASE_RESULTS.md) is preserved as an interim snapshot.

Machine-readable evidence: [600-row inventory](data/dataset-inventory.csv), [distribution table](data/dataset-distribution.csv), [dataset summary](data/dataset-summary.json), [training history CSV](data/training-history.csv), [verified interim checkpoint receipt](data/training-progress.json), and [five training examples](data/annotated-training-examples.json). Original inputs and targets remain in [the versioned dataset](../data/synthetic/).

These reports distinguish synthetic reference targets, deterministic checks, teacher-forced losses, real model generation, automated browser tests, and human editorial review. They are not interchangeable measures of success.

## Original GPU comparison completed

The original-prompt NF4 comparison is now fully verified: **44/120 base versus 120/120 adapter**, a **63.3 percentage-point difference** (paired 95% group-bootstrap interval 57.5–70.0). The [complete report](ORIGINAL_GPU_RESULTS.md) retains all raw outputs, subgroup rates, timing, memory and failure interpretation. The stronger shared-schema GPU control is running; interpret the original result with its formatting ambiguity and do not treat 100% synthetic automatic success as human approval.
