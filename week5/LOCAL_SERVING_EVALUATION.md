# Secondary evaluation after deployment conversion

Declared 2026-09-09 at 05:15:00 UTC, before testing the newly converted pinned-base GGUF or the trained-adapter GGUF. This is a deployment check in addition to the two GPU prompt comparisons.

Convert the exact Qwen/Qwen3-4B-Instruct-2507 revision `cdbee75f17c01a7cc42f958dc650907174af0554` and the adapter merged into that same revision to F16, then Q4_K_M with the same converter and quantizer. Record source hashes, converter commit, runtime version, model hashes and hardware. The base has been converted with llama.cpp converter commit `30b6a755e29692e8bc8e072885325716a2fee70f`; the quantizer is the llama.cpp 0.3.0-dev build bundled with official Ollama 0.33.3, commit `0f3a71be1`. The adapter must use the identical conversion path.

Evaluate all 120 frozen test cases for each artifact on the same Apple M1 Max. Use the versioned local-serving prompt `evidence-editor-v2-local-serving-v1`, strict JSON-schema constrained decoding, temperature zero, seed 42 and maximum 1024 output tokens. Preserve complete raw outputs, token receipts and errors. Report all nine structured checks, signal/condition breakdowns, measured latency and the paired group-bootstrap interval. Do not tune training, prompts or validators from these final-test outputs.

This comparison uses stronger decoding constraints and a different quantization/runtime from GPU NF4 evaluation. Keep its results separate. The earlier Ollama-tag browser recording remains an independent unadapted serving demonstration; it cannot establish exact base lineage. A successful software workflow does not imply successful model quality. Human editorial review and production promotion remain pending regardless of automatic scores.
