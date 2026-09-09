# Actual fine-tuned model application evidence

All 13 software checks passed with the actual checksum-verified adapter, including browser-to-model generation, citations, six workflow spans, protected review, unsupported-edit rejection, revision persistence, stale-write rejection and mobile/download behavior.

The first saved draft took 4.585 seconds in this one browser measurement. Do not treat that as a latency benchmark or directly compare it with another demonstration's timing.

The independent six-case workflow quality suite reports **FAIL**: four retrieval checks and the position-gain generation passed, but record-watch generation failed. Its raw output covered latest position and omitted the requested projection metric. Independent assessment reports `required_metric_covered=false` and `disposition_correct=false`. The application rejected it rather than silently substituting a draft. Other suite metric failures reflect the invalid generation's denominator treatment, not independently established citation or medical-language violations.

The recording, raw model requests/responses (without authentication headers), trace, saved draft and simulated revision history are retained. Review actions were explicitly labeled automated synthetic QA, with training consent false. Human editorial review and production promotion remain pending. The 120-case matched local benchmark is a separate evaluation.
