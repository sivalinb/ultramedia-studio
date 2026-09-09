# Demo and submission kit

The handout states **Sunday September 13, 2026, 11:59 p.m. PT** for Builder of the Week consideration. It specifies pass/fail and no individual feedback. [Submission form](https://forms.gle/7Hpa2Pkd8ZaWUomm6). No form submission is claimed.

## Three-to-four-minute walkthrough script

| Time | Show | Say |
|---|---|---|
| 0:00–0:30 | Week5 flow and a source pack | “An editor receives scattered race updates. Can a small model prepare a cited draft and know when the evidence is insufficient?” |
| 0:30–1:00 | One labeled example and400/80/120 split | “Facts stay in the request. Fine-tuning teaches the response behavior. Race groups are isolated across splits.” |
| 1:00–1:35 | Actual final loss curve and training receipt | “We trained LoRA adapters over a frozen4-bit Qwen base, selected checkpoint 100 using validation loss, then merged the adapter for local inference.” |
| 1:35–2:10 | Local classification and all-check results | “Decision accuracy rose83.3% to90.8%. Passing all nine checks rose63.3% to90.8%. Both variants had identical JSON constraints.” |
| 2:10–2:45 | Actual adapter recording and one failure | “These are real local model outputs. The UI checks passed, but the model still makes mistakes. An editor stays responsible for the final wording.” |
| 2:45–3:20 | Rules comparison and business decision | “Rules already solve this engineered structured task. We need measured editorial benefit to justify using the learned model in production.” |
| 3:20–3:45 | GitHub folder and reproducible assets | “The dataset, training configuration, raw results, failure cases and diagrams are all linked here. Here is what remains unmeasured.” |

Duration is a recommendation, not a course rule. Use the actual recorded evidence, never stage a successful notebook output or describe a static replay as live hosted inference.

## Ready assets

- [Visual workflow](https://github.com/sivalinb/ultramedia-studio/blob/codex/week5-handout-alignment/week5/diagrams/week5-flow.svg), [training curve](https://github.com/sivalinb/ultramedia-studio/blob/codex/week5-handout-alignment/week5/reports/data/final-training/training-loss.png), and [actual run manifest](https://github.com/sivalinb/ultramedia-studio/blob/codex/week5-handout-alignment/week5/reports/data/final-training/training-run.json).
- [Actual adapted application recording](https://github.com/sivalinb/ultramedia-studio/blob/codex/week5-handout-alignment/week5/evidence/adapter-serving/adapter-demo.webm).
- [Five smoke probes and outcomes](https://github.com/sivalinb/ultramedia-studio/blob/codex/week5-handout-alignment/week5/reports/HANDOUT_SMOKE_RESULTS.md).
- [Classification report](https://github.com/sivalinb/ultramedia-studio/blob/codex/week5-handout-alignment/week5/reports/DISPOSITION_RESULTS.md) and [complete fine-tuning reports](https://github.com/sivalinb/ultramedia-studio/blob/codex/week5-handout-alignment/week5/reports/README.md).
- [Public evidence page](https://ultramedia-studio.siva-babu.chatgpt.site/week5).

- [Silent recorded project walkthrough](https://github.com/sivalinb/ultramedia-studio/blob/codex/week5-handout-alignment/week5/evidence/handout-page/project-walkthrough.webm): actual page interactions, not a Loom upload or narrated presentation.

## Remaining external actions

- Record or upload this walkthrough to Loom and place its accessible URL in `week5/project/submission-status.json`. No Loom account/upload is available in this execution, and a local video is not a Loom submission.
- A real editor completes the blind pilot. This strengthens the custom project and is required by our production gate, not by the PDF for every submission.
- Submit the final GitHub URL plus Loom through the form. Verify anonymous access. No submission or reviewer contact occurs automatically.

A separate PR contains these handout-alignment changes; the original evidence PR retains its own outstanding GPU comparison. Merge/release status must be read from the actual PRs, not inferred from this checklist.
