# Fine-tuning reports and evidence

Report snapshot: **2026-09-09T05:30:20.711121+00:00**. This is an interim report: training is represented by verified checkpoint **90/100**. Final comparison scores are pending. Update the interpretation after all declared comparisons have been independently verified; preserve this progress snapshot as historical evidence.

| Report | Contents |
|---|---|
| [Fine-tuning report](FINE_TUNING_REPORT.md) | Research question, actual configuration, loss curve, experiment controls, recovery history, results status and limitations |
| [Data report](DATA_REPORT.md) | All 600 examples, split/condition/signal counts, token lengths, hashes, provenance, targets and leakage limits |
| [Flow and reproduction](FLOW_AND_REPRODUCIBILITY.md) | Training, evaluation, deployment and editorial-flow diagrams; runnable commands and artifact verification |

[Verified local-base results](LOCAL_BASE_RESULTS.md): all 120 cases completed; adapter comparison pending.

Machine-readable evidence: [600-row inventory](data/dataset-inventory.csv), [distribution table](data/dataset-distribution.csv), [dataset summary](data/dataset-summary.json), [training history CSV](data/training-history.csv), [verified interim checkpoint receipt](data/training-progress.json), and [five training examples](data/annotated-training-examples.json). Original inputs and targets remain in [the versioned dataset](../data/synthetic/).

These reports distinguish synthetic reference targets, deterministic checks, teacher-forced losses, real model generation, automated browser tests, and human editorial review. They are not interchangeable measures of success.
