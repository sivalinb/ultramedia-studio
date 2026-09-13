# UltraMedia Week 5 Agenda Coverage

Audit date: 9 September 2026. Reference: the supplied agenda screenshot, including both class columns and both demo items. Project evidence snapshot: `e37de759155ee0b350f25ce1d124962452d8d2b2`. The separate four-page project handout defines the custom submission route; the agenda lists a wider set of teaching topics.

**Finding:** the project demonstrates the central SFT/QLoRA lifecycle, but it does not demonstrate every agenda topic. This supplement explains all listed topics and connects them to evidence or a clearly unexecuted extension. Conceptual coverage is not execution evidence. No percentage of “agenda completion” is assigned because the agenda gives no weighting or requirement to execute every method.

## 12 Previous class topics and their evidence

| Agenda topic | Evidence and justification | Assessment |
|---|---|---|
| Building intuition about neural net architecture | The project uses a pretrained transformer and adapts its attention and feed-forward projections. Section 14 explains token representations, attention, next-token prediction and adapter placement. We did not build or pretrain a network. | Concept explained; pretrained architecture used |
| What is fine-tuning | The actual run updates 33,030,144 adapter parameters on labeled assistant completions. Two epochs and 100 optimizer steps are recorded. | Demonstrated |
| Decision framework prompting versus RAG versus fine-tuning | The serving prompt specifies the task; retrieval supplies race facts; SFT teaches response behavior. Rules/base/adapter results inform the systems decision. No isolated prompting-versus-RAG ablation was run. | Applied and explained; no full ablation |
| Critical distinction behavior versus knowledge | Citation structure, restraint and draft/hold behavior are learned; current timing facts stay in retrieved/request evidence. The 600 synthetic examples do not update live race knowledge. | Applied and explained |
| LoRA and QLoRA breakdown | Rank 16, alpha 32, dropout .05, frozen NF4 double-quantized base, seven projection targets and actual memory receipt. Section 14 separates adapter learning from quantization. | Demonstrated |
| Fine-tuning methods | SFT is the executed objective; LoRA is the parameter-efficient update method and QLoRA adds quantization. Full tuning, preference optimization and RFT are compared conceptually below. | SFT demonstrated; other methods not run |
| Fine-tuning failure modes | Retained misleading-hint failures, invented citation, semantic sign ambiguity, template dependence, prompt sensitivity and interrupted compute. Loss and contract checks do not prove editor quality. | Demonstrated and analyzed |

Evidence: [final training manifests](https://github.com/sivalinb/ultramedia-studio/tree/e37de759155ee0b350f25ce1d124962452d8d2b2/week5/reports/data/final-training), [application workflow](https://github.com/sivalinb/ultramedia-studio/blob/e37de759155ee0b350f25ce1d124962452d8d2b2/backend/src/ultramedia/workflow.py), [matched local comparison](https://github.com/sivalinb/ultramedia-studio/blob/e37de759155ee0b350f25ce1d124962452d8d2b2/week5/reports/LOCAL_COMPARISON_RESULTS.md), and [smoke failures](https://github.com/sivalinb/ultramedia-studio/blob/e37de759155ee0b350f25ce1d124962452d8d2b2/week5/reports/HANDOUT_SMOKE_RESULTS.md).

The distinction matters for the submission story: UltraMedia can show a real learned change and explain why fine-tuning was considered, while still concluding that deterministic handling currently wins for the engineered structured task. Choosing not to promote a model is a defensible systems decision.

<!-- pagebreak -->

## 13 Current class topics and demos

| Agenda topic | Evidence and justification | Assessment |
|---|---|---|
| Merging and deploying custom models | Adapter merged with pinned base, converted to GGUF and served locally; actual adapted browser/API evidence exists. Public page is recorded evidence, not a hosted model API. | Local deployment demonstrated; cloud pending |
| Reinforcement Fine-Tuning | Existing checks can inform a future reward design, but no reward-driven optimizer, rollout training or RFT checkpoint exists. Section 14 explains the distinction. | Concept only; not executed |
| Synthetic data and distillation | All 600 examples were generated programmatically from fictional race rules. No teacher-model outputs or logits trained the student. | Synthetic data demonstrated; teacher distillation not run |
| The cost math | Actual local request latency and training memory/time are recorded. Section 15 adds explicit hypothetical break-even arithmetic. Editor labor, accepted-brief cost and real ROI are unmeasured. | Measured resources plus illustrative economics |
| Why local cost privacy and no-internet access | Actual local inference avoids a hosted inference dependency for the measured model path. Downloads/setup need connectivity; a disconnected full-app test has not been recorded. | Local execution demonstrated; offline proof pending |
| Running models locally with Ollama | Verified runtime is llama.cpp bundled with Ollama 0.33.3. An Ollama provider and import instructions exist, but they do not establish a successful native Ollama API run. | Partial tool-specific coverage |
| Privacy cost and compliance benefits of local inference | Loopback model serving, isolated QA data, revision controls and consent gates are implemented. Local execution alone proves neither complete network isolation nor legal compliance. | Controls demonstrated; broader assurances unproven |
| Demo Ollama | No separate recorded `ollama create` / `ollama run` / `/api/chat` demonstration of the adapted artifact was found in the reviewed evidence. | Specific demo pending |
| Demo RFT Fireworks AI | Fireworks inference-provider code is not RFT. No Fireworks RFT job, reward curve, checkpoint or deployment receipt exists. | Not executed |

The two demo rows overlap agenda topics but are listed separately so every visible item is accounted for. The supplied project handout does not demand a Fireworks RFT run, teacher distillation, a disconnected demo or every training method as conditions of the custom GitHub-plus-Loom route. That is why this audit distinguishes course breadth from the narrower submission task.

The SQL example uses execution as a strong correctness signal. UltraMedia's validators are weaker: valid JSON and matching numeric tokens can coexist with incorrect prose. We should not copy the SQL example's reward claims or label our existing evaluation an RFT loop.

Evidence: [serving guide](https://github.com/sivalinb/ultramedia-studio/blob/e37de759155ee0b350f25ce1d124962452d8d2b2/week5/SERVING.md), [historical local runtime evidence](https://github.com/sivalinb/ultramedia-studio/blob/e37de759155ee0b350f25ce1d124962452d8d2b2/week5/END_TO_END.md), [actual adapted application receipts](https://github.com/sivalinb/ultramedia-studio/tree/e37de759155ee0b350f25ce1d124962452d8d2b2/week5/evidence/adapter-serving), [provider implementations](https://github.com/sivalinb/ultramedia-studio/blob/e37de759155ee0b350f25ce1d124962452d8d2b2/backend/src/ultramedia/providers.py).

<!-- pagebreak -->

## 14 Architecture methods and the RFT distinction

A transformer represents input tokens as vectors. Attention mixes information from preceding tokens, while feed-forward layers transform those representations. Repeated layers and the output head produce next-token scores. In UltraMedia, the prompt contains the task and race evidence; generated tokens form the structured story. The small network icons in the illustration are explanatory symbols, not a literal architecture diagram or evidence of pretraining.

LoRA freezes a pretrained weight matrix and learns a low-rank update through two smaller matrices. Merging adds the learned update to the corresponding base weights. QLoRA trains those adapters while storing the base in a quantized representation; gradients still train the adapters. UltraMedia's NF4 training and Q4_K_M serving are different quantization choices, so the project compares each runtime separately. [LoRA paper](https://arxiv.org/abs/2106.09685), [QLoRA paper](https://arxiv.org/abs/2305.14314).

| Choice | Learning signal or purpose | UltraMedia state |
|---|---|---|
| Prompting | Instructions and examples in the current request; no weight updates | Used by both baseline and adapted model |
| Retrieval augmented generation | Retrieve relevant facts into the request | Local evidence retrieval implemented |
| SFT | Learn reference completions with supervised loss | Executed using QLoRA |
| Full-parameter tuning | Update all selected base parameters | Not executed |
| Preference optimization | Learn from preferred versus rejected responses | Not executed; human review packet is unfilled |
| RFT | Generate outputs, score rollouts, update a policy toward higher reward | Not executed |
| Teacher distillation | Train a student using a teacher model's behavior or probability targets | Not executed; rules generated this corpus |

The objective and parameter-update method are separate choices. “SFT versus RFT” concerns the learning signal; “full tuning versus LoRA” concerns which parameters are updated. Synthetic data is a provenance category, not proof of distillation. Quantizing or merging a model also does not constitute distillation. [Foundational distillation paper](https://arxiv.org/abs/1503.02531).

For a future RFT experiment, prompts would produce candidate outputs, a reviewed evaluator would assign reward, and training would update the model using those rewards. Our current automatic scores are calculated after SFT for evaluation; they are not fed into a reinforcement-learning optimizer. Fireworks documents prompts plus an evaluator as the basis of its RFT workflow. [Official Fireworks RFT documentation](https://docs.fireworks.ai/fine-tuning/reinforcement-fine-tuning-models).

A future reward must test unsupported drafts, wrong abstentions, fabricated citations, malformed output and semantic meaning. Otherwise a model might maximize reward by holding every request or producing superficially valid text. First test the evaluator against those counterexamples, freeze a new validation/test set, and compare both models under one protocol. This is an extension design, not a completed RFT experiment or a promise that the current Qwen artifact is supported by a Fireworks training configuration.

<!-- pagebreak -->

## 15 Cost privacy and local execution

Local execution gives control over the inference endpoint and removes the per-request need to call a hosted model for that path. It still consumes hardware, electricity, storage and maintenance. UltraMedia measured model-request p50 latency of 4.622 seconds for the base and 1.801 seconds for the adapter, with different generated lengths. It did not measure total editor productivity or paid serving cost per accepted story.

### Worked cost example with hypothetical inputs

Assume a one-time adaptation cost of **$30**, a base workflow cost of **$0.05 per accepted brief**, and an adapted workflow cost of **$0.02 per accepted brief**. Assume these recurring amounts already include serving, failures, retries and equal editorial labor. These are invented scenario inputs for teaching the arithmetic, not actual project spend or provider prices.

| Hypothetical calculation | Result |
|---|---|
| Recurring saving per accepted brief | $0.05 minus $0.02 = $0.03 |
| Break-even volume | $30 divided by $0.03 = 1,000 accepted briefs |
| Base total at 1,000 accepted briefs | 1,000 times $0.05 = $50 |
| Adapted total at 1,000 accepted briefs | $30 plus 1,000 times $0.02 = $50 |

If adapted outputs instead require **30 extra seconds of review at $30 per hour**, they add **$0.25 per accepted brief**. Recurring adapted cost becomes $0.27, above the base's $0.05, so there is no positive break-even under those assumptions. If there are no accepted briefs, cost per accepted brief is undefined. This sensitivity explains why a faster model request alone does not establish a cheaper workflow.

### Local privacy and offline boundaries

The recorded local model server binds to loopback, and browser testing uses an isolated synthetic database and a private reviewer credential. Review updates reject unsupported numeric edits and require explicit training consent and a rights basis. Those controls are observed software behavior; they do not establish compliance with a specific law, certification or organization policy.

A full disconnected demonstration would cache model files and application dependencies, explicitly select the local provider, disable cloud features/fallbacks, block outbound connectivity, restart the app, and verify generation, retrieval and revision persistence. It would also check that errors cannot silently switch to a cloud provider. No such complete network-isolation test is claimed here. Ollama documents local-only configuration, but configuration guidance is not evidence that this project's whole stack passed an offline test. [Ollama FAQ](https://docs.ollama.com/faq).

For exact Ollama demo coverage, a future run should import the pinned merged GGUF under a new model name, retain model/template settings, call the native API, and save actual output and validation receipts. Import and template compatibility must be checked; an arbitrary model tag is not the trained artifact. [Ollama model import documentation](https://docs.ollama.com/import).

<!-- pagebreak -->

## 16 Illustrated end to end project flow

![UltraMedia illustrated end to end training inference validation and editorial flow](../diagrams/week5-end-to-end-illustrated.png)

The training strip follows labeled synthetic examples through the train/validation/test split, QLoRA and merge. The five main panels follow a race evidence request through the base/adapted comparison, structured output, validation and measured results. The final editor panel keeps source inspection and approval visible. The output card describes fields; it is not a fabricated model prediction.

The green result card reports automatic contract success on the frozen local test set. Decision accuracy is shown separately. The amber smoke-test card refers to the two learned models, each 3/5; the rules baseline passed 5/5. Those results are evaluations, not RFT rewards. The validator panel lists examples of the eight constituent checks; their aggregate is the ninth reported metric.

The lower editor panel shows the intended human workflow and labels human quality review pending. Recorded automated browser approvals do not satisfy that review. No held-out score arrow feeds back to the training strip, because no RFT loop was executed.

### Defensible agenda summary

We can demonstrate SFT with QLoRA, synthetic-data preparation, loss review, adapter merge, matched local serving, measured classification results and failure analysis. We can explain the remaining agenda concepts and why they matter to this project. We cannot claim completed teacher distillation, reinforcement fine-tuning, a Fireworks RFT demo, a native Ollama demo or a fully disconnected application test.

That distinction strengthens the report's credibility. The core handout gaps remain the five-probe quality failures and final Loom/form submission. Human editorial validation strengthens the project and governs production promotion. The interrupted explicit-schema GPU control is an additional research commitment. None of these open items is closed by creating this visual or supplement.

The illustration was generated with the built-in image tool and checked against the recorded project facts. It is an explanatory visual, not a screenshot of a training run or an independently generated experiment result.


## September 12 feedback follow-up

[Independent calibration and abstention diagnosis](../calibration/RESULTS.md) adds 144 saved diagnostic outputs, ten author-designed judge challenges, evidence-only label packets, judge packets, validation tools and an evidence-led next-change gate. Human calibration is still pending. The new negative result is preserved separately from the original benchmark.
