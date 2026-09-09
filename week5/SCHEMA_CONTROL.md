# Predeclared explicit-schema prompt control

Declared 2026-09-09 at 04:23 UTC, while the QLoRA run was still training (step35/100) and before either GPU test evaluation was available.

The first separate local GGUF serving probe returned `numeric_value` in its claims instead of the required `value` key. The existing frozen prompt describes a "numeric value" without spelling out the nested JSON schema. This is a prompting weakness that could exaggerate the apparent benefit of learning a fixed output format through SFT.

We therefore retain the original experiment unchanged and add a second paired comparison. Both the unadapted base and the same trained adapter receive the original prompt plus the exact output JSON schema. The new prompt version is `evidence-editor-v2-explicit-schema-v1`; its implementation is `backend/src/ultramedia/prompt_controls.py`. No few-shot answers or test labels are added. Training data, training settings, validation checkpoint selection, test cases, model revision, quantization, greedy decoding and maximum output length remain unchanged. No retraining or tuning from final test predictions is permitted.

Run after the original comparison:

```bash
PYTHONPATH=backend/src python -m ultramedia.training evaluate \
  --run week5/runs/<run> --dataset week5/data/synthetic \
  --schema-control --resume-evaluation --max-new-tokens 1024
```

The second comparison is saved beneath `schema-control/`, preserving the original reports and predictions. It covers the same120 held-out cases per model, retaining invalid outputs and errors in the denominator. Report all nine automatic metrics, the paired group-bootstrap interval, per-condition and per-signal results, latency, token counts and memory for each arm.

The key interpretation is the adapter's benefit **under the stronger shared prompt**, with the original comparison shown as context. If the prompted base closes the gap, say that prompting is sufficient for this contract. If the adapter still improves automatic checks, that is evidence for this synthetic task only; editorial benefit and real-race generalization still require human evaluation. Lower training loss alone is not proof of value.

The local llama.cpp demonstration additionally uses schema-constrained decoding. That serving safeguard is separate from this GPU prompt-only control, which does not constrain decoding. Do not combine scores from different runtimes or quantizations into a controlled comparison.

No outcome is claimed in this declaration.
