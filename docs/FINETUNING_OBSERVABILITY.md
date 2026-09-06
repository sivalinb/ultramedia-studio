# Fine-tuning and observability status

## Honest status

The repository implements the complete QLoRA path, but it does not contain a trained adapter. The training-data preparation step accepts only human-approved story drafts and exits unless at least 20 examples exist. The current local fixture has zero approved examples, so training is correctly blocked.

The current release candidate is the deterministic local provider with hybrid retrieval. On September 6, 2026, `ultramedia-release-v1` ran six fixture cases and passed all four gates: retrieval recall at 3, citation validity, the mandatory human-review gate, and zero unsupported sensitive inferences. The Python test suite also passed 6 of 6 tests. These are smoke-test results and must not be represented as fine-tuned-model results.

## Implemented fine-tuning method

- Base: `Qwen/Qwen3-4B-Instruct-2507`
- Method: supervised fine-tuning with TRL and PEFT LoRA adapters
- Quantization: 4-bit NF4, double quantization, bfloat16 compute
- LoRA: rank 16, alpha 32, dropout 0.05
- Targets: `q_proj`, `k_proj`, `v_proj`, `o_proj`, `gate_proj`, `up_proj`, `down_proj`
- Training: 2 epochs, learning rate `2e-4`, warmup ratio `0.05`, maximum length 2,048
- Batching: per-device batch 2 with gradient accumulation 8, effective batch 16
- Data: 90/10 train-validation split with seed 42

Fine-tuning is intended to learn editorial voice, response structure, citation placement, and abstention behavior. Current race facts remain in RAG.

## Required experiment before adapter release

1. Accumulate a rights-cleared, diverse set of human-approved stories.
2. Freeze a held-out test set before training.
3. Benchmark prompt only, prompt plus RAG, and QLoRA plus RAG on the same cases.
4. Measure grounding, numeric exactness, style, safety, fairness, latency, and cost.
5. Ship the adapter only if it beats prompt plus RAG on predeclared thresholds.
