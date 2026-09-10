# Compute options and recovery

These statuses describe actual execution, not a promise of quota or an award.

| Option | Verified status | Role and limits |
|---|---|---|
| Google Colab T4, 15,360 MiB | QLoRA training is running with checkpoint backups | Primary frozen experiment. Runtime loss requires restoration of the same dataset, settings, and checkpoint. A100 and L4 requests were unavailable under the current quota. |
| Apple M1 Max, 64 GiB | Actual Qwen 4B Q4_K_M inference, browser recording, 13 software checks | No GPU account needed for the demonstrated local inference. This is a separate unadapted model; both independent generation quality cases failed. |
| Kaggle GPU notebook | Portable notebook prepared; not executed on Kaggle | Alternate CUDA environment when an account has GPU quota and Internet enabled. Verify the pinned dependencies and available memory before starting. |
| Runpod GPU Pod | Documentation reviewed; no Pod purchased or provisioned | Paid fallback if hosted notebook quota blocks completion. Use an on-demand CUDA Pod, persistent storage, the same source archive and training settings, and explicit spend limits. |

The Colab run saves recoverable checkpoints containing adapter, optimizer, scheduler, RNG state and trainer state. Local backups verify ZIP integrity and the experiment identity. Completed training and evaluation stages are downloaded independently. Interrupted attempts remain in the execution receipt; elapsed training time from a resumed invocation must not be presented as total project compute time.

For a fresh run use the checked-in notebook. To resume a verified checkpoint with the same configuration:

```bash
PYTHONPATH=backend/src python -m ultramedia.training train \
  --dataset week5/data/synthetic --output week5/runs/RUN \
  --research-synthetic --epochs 2 --max-length 2048 \
  --resume-from-checkpoint week5/runs/RUN/checkpoints/checkpoint-N
```

After original evaluation, run the predeclared [schema control](SCHEMA_CONTROL.md) using the same trained adapter. Retain both comparisons. A changed prompt or quantization must be labeled as a different condition.

Official references: [Colab availability and runtime limits](https://research.google.com/colaboratory/faq.html), [Kaggle notebooks](https://www.kaggle.com/docs/notebooks), [Runpod Pods](https://docs.runpod.io/pods/overview), [Ollama Qwen 4B model](https://ollama.com/library/qwen3:4b-instruct), and [llama.cpp server](https://github.com/ggml-org/llama.cpp/tree/master/tools/server). No additional paid capacity was purchased for this submission.
