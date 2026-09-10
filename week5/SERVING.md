# Serving and rollback

## Keep model lineage intact

Training uses Qwen/Qwen3-4B-Instruct-2507 at revision `cdbee75f17c01a7cc42f958dc650907174af0554`. The run records dataset hash, prompt version, adapter file hashes and tokenizer. Merging checks those hashes and the base revision. An arbitrary Ollama `qwen3` tag or a different cloud model is not an equivalent baseline.

```bash
PYTHONPATH=backend/src python backend/scripts/merge_adapter.py --adapter week5/runs/RUN/adapter --output week5/runs/RUN/merged
```

This needs RAM and disk for full weights. It is optional and is not performed by the default notebook.

## Convert and compare

Use an installed, compatible llama.cpp checkout. Choose and record its actual commit; do not invent a pin or describe an untested command as verified. Conversion commands depend on the selected llama.cpp build:

```bash
python /path/to/llama.cpp/convert_hf_to_gguf.py week5/runs/RUN/merged --outfile week5/runs/RUN/ultramedia-f16.gguf --outtype f16
/path/to/llama.cpp/build/bin/llama-quantize week5/runs/RUN/ultramedia-f16.gguf week5/runs/RUN/ultramedia-q4_k_m.gguf Q4_K_M
```

Repeat conversion at the same precision for the exact original base-model revision. Record the converter revision, GGUF SHA-256, flags, runtime version and hardware. Re-run the same held-out requests through the chosen runtime for both artifacts before claiming deployment quality or speed. NF4 GPU training/evaluation and Q4_K_M CPU serving are distinct comparisons.

For Ollama, create a new model name from the generated GGUF using a Modelfile whose `FROM` points to that file. Verify that the runtime uses the tokenizer's chat template; the application supplies its shared system/user messages. Keep maximum output tokens and temperature equal across candidates. Do not overwrite the known base model.

```text
FROM /absolute/path/to/ultramedia-q4_k_m.gguf
PARAMETER temperature 0
PARAMETER num_predict 1024
```

Then configure `PROVIDER_MODE=ollama` and `OLLAMA_MODEL=<the new model name>`, and start the Python API. `NEXT_PUBLIC_ULTRAMEDIA_API_URL` connects the web race desk to that API. Production reviewers should use the configured reviewer key or an organization authentication layer. Public evidence pages do not require access to a model or private review records.

## Failures and rollback

The API rejects unsupported corrections and invalid generated contracts; provider failures must not be relabeled as successful drafts. Keep the original base model and its configuration. Roll back by restoring its recorded model name and revision, retaining candidate evidence for diagnosis. Publication remains a separate human action regardless of adapter quality.

## Executed local demonstration

The separate unadapted Qwen 4B Q4_K_M model was served on an Apple M1 Max through `PROVIDER_MODE=llamacpp`. The browser-to-API demonstration passed 13 software checks and produced a real draft in 7.623 seconds. This single-request measurement is not a latency guarantee. Both generation cases in the independent workflow quality check failed and remain in the evidence. See [END_TO_END.md](END_TO_END.md) for exact model hashes, commands, recording, and limitations.

Current status as of September 9, 2026: training, adapter merge, conversion and the matched local comparison are complete. The actual adapted model also passed 13 browser software checks, while its separate workflow quality suite failed one generation case. See [matched local results](reports/LOCAL_COMPARISON_RESULTS.md). The preceding unadapted demonstration is retained as historical evidence. Native Ollama API execution and Fireworks deployment have not been demonstrated; verified serving used llama.cpp bundled with Ollama. The explicit-schema GPU adapter control remains interrupted awaiting capacity.
