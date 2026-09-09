# Week 5: UltraMedia Race Desk

**Start with the [handout-aligned project guide](project/README.md).** It maps each lab phase to measured evidence, includes a visual flow, classification metrics, five task-level model probes, a business decision and a Loom submission script.

![Week 5 flow](diagrams/week5-flow.svg)

# Week 5 submission package

Start with [SUBMISSION.md](SUBMISSION.md). Run [the Colab/Kaggle notebook](notebooks/UltraMedia_Week5_QLoRA.ipynb) with the supplied source ZIP to produce an actual adapter and measured comparison.

The 600 supplied examples are synthetic and unapproved by humans. Training completed 100 steps. The original GPU comparison is 44/120 base versus 120/120 adapter; the matched local comparison is 76/120 versus 109/120. The explicit-schema GPU control was interrupted during its adapter arm and awaits compatible Colab capacity; its completed base outputs are retained. All scores are automatic checks on 120 synthetic cases per model, not human editorial preference. The actual adapter passed 13 browser software checks; its separate application quality suite still fails one generation case. Human review and production promotion remain pending.

- [Data card](DATA_CARD.md)
- [Evaluation protocol](EVALUATION.md)
- [Serving and rollback](SERVING.md)
- [Dataset manifest](data/synthetic/manifest.json)
- [Local evidence](evidence/)

- [End-to-end recording and verification](END_TO_END.md)
- [Predeclared stronger prompt control](SCHEMA_CONTROL.md)
- [Compute options and recovery](COMPUTE_OPTIONS.md)

- [Detailed fine-tuning, data and flow reports](reports/README.md)
