# Week 5 submission package

Start with [SUBMISSION.md](SUBMISSION.md). Run [the Colab/Kaggle notebook](notebooks/UltraMedia_Week5_QLoRA.ipynb) with the supplied source ZIP to produce an actual adapter and measured comparison.

The 600 supplied examples are synthetic and unapproved by humans. Local data, software, deterministic checks, and actual open-source model serving are recorded. The browser run passed 13 software checks; the separate local-model workflow check failed both generation cases. GPU training is in progress; comparative GPU model quality and editor preference remain unmeasured until their evaluation and review are complete.

- [Data card](DATA_CARD.md)
- [Evaluation protocol](EVALUATION.md)
- [Serving and rollback](SERVING.md)
- [Dataset manifest](data/synthetic/manifest.json)
- [Local evidence](evidence/)

- [End-to-end recording and verification](END_TO_END.md)
- [Predeclared stronger prompt control](SCHEMA_CONTROL.md)
- [Compute options and recovery](COMPUTE_OPTIONS.md)

- [Detailed fine-tuning, data and flow reports](reports/README.md)
