# Five task-level smoke probes

Authored September 9, 2026 after the original benchmark. Freeze these five inputs and this protocol before their inference. They are synthetic smoke probes, not independent human labels or an untouched broad benchmark. No tuning or retries selected for score. Preserve every first attempt and error.

Use the already verified pinned base and adapted Q4_K_M artifacts, the same local llama.cpp runtime, serving prompt v1, constrained JSON, greedy temperature 0, seed 42 and max 1024 tokens. Run rules, base and adapter separately. Score exact draft/abstain choice plus the original automatic contract; inspect prose separately through blind review. The signal type is an input, not a predicted class. Do not update the original frozen data, prompts, adapter or validators from these outcomes.

Cases: a position loss, a projected record, missing cutoff evidence, contradictory pace evidence, and a misleading hint despite sufficient position evidence. Human review and model promotion remain pending regardless of count. See `scripts/run_handout_smoke.py` for portable reproduction.
