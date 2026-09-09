# UltraMedia data sources and provenance

Companion to the eleven-page illustrated brochure. Reviewed 9 September 2026. This note distinguishes the research corpus, demonstration fixture, external context and actual execution receipts. All repository links below pin the reviewed source snapshot `cc8f42cbc73f6efe92c49d21437f4e4b16fd1089`. The brochure artwork illustrates concepts; it is not a screenshot, race result, customer testimonial or measurement.

## 1. What the training data actually is

UltraMedia authored all **600 research examples** programmatically in [dataset.py](https://github.com/sivalinb/ultramedia-studio/blob/cc8f42cbc73f6efe92c49d21437f4e4b16fd1089/backend/src/ultramedia/dataset.py). The deterministic generator seed is **20260908**, separate from training/evaluation seed **42**. It constructs 150 fictional race episodes and athlete identities, produces synthetic timing and evidence, and writes reference responses from programmed rules.

The version is `ultramedia-synthetic-research-v1`, prompt `evidence-editor-v2`, and contract `ultramedia-story-v2`. The provenance for each row identifies an authored synthetic generator, `synthetic=true`, `human_approved=false` and `CC0-1.0`. That license applies to these newly authored records; it does not relicense official race websites or the model weights.

The corpus did **not** use real athlete results, scraped articles, private customer prompts, human-approved editorial targets or teacher-model outputs. A `synthetic://fictional-race-...` source URL is an internal provenance identifier, not an external website. Programmatic synthetic targets are not teacher-model distillation. Automatic checks are not human approval.

| Split | Examples | Race groups | Draft targets | Hold targets | Use |
|---|---:|---:|---:|---:|---|
| Train | 400 | 100 | 240 | 160 | Parameter updates |
| Validation | 80 | 20 | 48 | 32 | Loss review and checkpoint selection |
| Test | 120 | 30 | 72 | 48 | Frozen generation comparisons |

There are no shared race groups or exact message-payload overlaps across splits. Templates, vocabulary and task structure remain shared, so this does not prove broad semantic independence or real-race generalization. Source: [manifest and audit](https://github.com/sivalinb/ultramedia-studio/blob/cc8f42cbc73f6efe92c49d21437f4e4b16fd1089/week5/data/synthetic/manifest.json), [600-row inventory](https://github.com/sivalinb/ultramedia-studio/blob/cc8f42cbc73f6efe92c49d21437f4e4b16fd1089/week5/reports/data/dataset-inventory.csv).

## 2. Fields and factors considered

Each model request has three input sections. The reference response is withheld from inference.

| Section | Fields | Purpose |
|---|---|---|
| Moment | `athlete_bib`, `signal_type`, `headline_hint` | Identify the requested race moment; the hint is untrusted and cannot override facts. |
| Timing | Athlete name/bib, checkpoint, mile, elapsed seconds, overall position | Supply the timing context. In research and the demo, these values are fictional. |
| Evidence | ID, title, source URL, excerpt, optional score and structured metric/value facts | Preserve traceable support for a claim. A retrieval score is not a calibrated factual-confidence probability. |

The response contract contains disposition, eyebrow, headline, body, social caption, citation IDs, structured claims and a reason. Each claim carries a metric, signed numeric value and citation ID. Drafts need support; holds must state a reason and contain no factual claims. The social caption limit is 280 characters. Source: [contracts.py](https://github.com/sivalinb/ultramedia-studio/blob/cc8f42cbc73f6efe92c49d21437f4e4b16fd1089/backend/src/ultramedia/contracts.py).

### Four signal types

| Signal | Generator range | Unit and interpretation |
|---|---|---|
| Position change | -8 to +19 | Places; positive means gained, negative means lost. |
| Record projection | -180 to +240 | Seconds; positive means ahead of projected target, not an achieved record. |
| Cutoff buffer | -12 to +42 | Minutes; positive means time remaining, negative means beyond cutoff. |
| Pace change | -35 to +50 | Seconds per mile; negative means faster, positive means slower. |

These are programmed ranges, not measured population bounds. Boundary cases use zero. For position cases, timing rows are adjusted to match the reference gain. Other signal measurements are supplied synthetically, not predicted by a validated race-performance model. The model cannot infer medical condition, emotion, intent or misconduct from these fields.

### Five evidence conditions

- **Complete:** consistent support is available; target a draft.
- **Missing:** required facts are removed; target a hold.
- **Contradictory:** a second measurement differs by 7 in the metric's unit; target a hold.
- **Misleading hint:** the hint asks for an unsupported injury/record claim; the target follows the facts instead.
- **Boundary:** zero-valued metrics test direction and neutral wording.

Each signal has 150 records and each condition 120. Every signal/condition combination has 20 train, 4 validation and 6 test records. This balance is deliberate experimental design, not the expected frequency of live-race situations. The [annotated training examples](https://github.com/sivalinb/ultramedia-studio/blob/cc8f42cbc73f6efe92c49d21437f4e4b16fd1089/week5/reports/data/annotated-training-examples.json) show the exact evidence, prompt, reference and hashes for one example per condition, selected from training without inspecting test success.

## 3. What the application demo uses

The local seed fixture [sample_race.json](https://github.com/sivalinb/ultramedia-studio/blob/cc8f42cbc73f6efe92c49d21437f4e4b16fd1089/backend/data/sample_race.json) labels the race **Western States 100 - Simulation**. It contains **7 timing events for 2 fictional athletes** and **5 knowledge chunks**. The names and timing values are invented; checkpoint/course labels provide demonstration context.

Four knowledge chunks attribute context to official Western States pages. One additional chunk is the project's simulation policy.

| Demo chunk | Source publisher and location | Role in the demo |
|---|---|---|
| `wser-course-profile` | Western States Endurance Run, [official homepage](https://www.wser.org/) | Course profile context. |
| `wser-canyons` | Western States Endurance Run, [official homepage](https://www.wser.org/) | Canyon/river geographic context. |
| `wser-finish-window` | Western States Endurance Run, [participant guide](https://www.wser.org/participant-guide/) | Finish-window context; current organizer communications remain authoritative. |
| `wser-history` | Western States Endurance Run, [year-by-year archive](https://www.wser.org/year-by-year/) | Historical background, not current timing. |
| `simulation-policy` | UltraMedia, [product site](https://ultramedia-studio.siva-babu.chatgpt.site/) | Internal simulation and editorial-review policy. |

The three official URLs were opened and checked on 9 September 2026 for this source review. Their current pages support the type of context attributed in the fixture. The repository does not retain the original date each summary was authored, an archived copy of each webpage or a third-party license grant. This review date must not be presented as an original collection timestamp. No official partnership or endorsement is claimed.

[seed.py](https://github.com/sivalinb/ultramedia-studio/blob/cc8f42cbc73f6efe92c49d21437f4e4b16fd1089/backend/src/ultramedia/seed.py) loads that static JSON into local storage. It does not fetch a live race feed. [retrieval.py](https://github.com/sivalinb/ultramedia-studio/blob/cc8f42cbc73f6efe92c49d21437f4e4b16fd1089/backend/src/ultramedia/retrieval.py) ranks stored context with a blend of hash-vector cosine similarity (0.58) and lexical overlap (0.42), returning up to five chunks and four timing rows for the selected athlete. These are implementation settings, not tuned accuracy claims or a pretrained embedding-model experiment.

The current [workflow](https://github.com/sivalinb/ultramedia-studio/blob/cc8f42cbc73f6efe92c49d21437f4e4b16fd1089/backend/src/ultramedia/workflow.py) derives position gain and latest position from stored timing and adds an internal `ultramedia://timing/...` citation. It does not establish an operational calculator for all four research signals. Research coverage must not be confused with complete live-demo signal coverage.

## 4. Where the model and measured results come from

The pretrained weights are published by Qwen as [Qwen3-4B-Instruct-2507](https://huggingface.co/Qwen/Qwen3-4B-Instruct-2507), whose model card lists Apache 2.0. UltraMedia pins revision `cdbee75f17c01a7cc42f958dc650907174af0554`. The model is a software/model input, not the source of race facts; this report does not claim to audit its entire pretraining corpus.

The project produced the [training receipts](https://github.com/sivalinb/ultramedia-studio/tree/cc8f42cbc73f6efe92c49d21437f4e4b16fd1089/week5/reports/data/final-training) on a Colab T4 and the [matched local comparison](https://github.com/sivalinb/ultramedia-studio/blob/cc8f42cbc73f6efe92c49d21437f4e4b16fd1089/week5/reports/LOCAL_COMPARISON_RESULTS.md) on an Apple M1 Max with 64 GiB RAM. Saved raw predictions, checks, token receipts and conversion hashes support the comparison. These are actual execution outputs on synthetic test inputs.

The brochure chart reads the saved comparison JSON: 76/120 versus 109/120 automatic success, +27.5 percentage points. Its paired 95% interval is +20 to +35 points from 1,000 resamples of 30 race groups, seed 42. All failures remain in the denominator. Neither this measure, the loss curve nor passing software checks establishes human editorial usefulness. The original GPU experiment and incomplete explicit-schema GPU control are separate comparisons and are not pooled into the local chart.

## 5. Identity, integrity and future external sources

The [dataset manifest](https://github.com/sivalinb/ultramedia-studio/blob/cc8f42cbc73f6efe92c49d21437f4e4b16fd1089/week5/data/synthetic/manifest.json) records the dataset SHA-256:

`5c148b3d1e57a989e38c55e73f1d46ae0b5b17227be154457953bac2dcaef8cf`

| File | SHA-256 |
|---|---|
| train.jsonl | `0ae633ce602b8fba856b2b9ed7f255b6047c0960ac83c85594d7d416320ea754` |
| validation.jsonl | `5313d54852954cdcce8f40dde1c2fe54071e80c83c90102db45e62414304c6e0` |
| test.jsonl | `69995179a6268fe60b1f7b62945f921311ba6c38faa4da3c70fd8a5325d65ffc` |

A [timing CSV importer](https://github.com/sivalinb/ultramedia-studio/blob/cc8f42cbc73f6efe92c49d21437f4e4b16fd1089/backend/src/ultramedia/ingestion.py) exists. It requires bib, name, checkpoint, mile, elapsed seconds and overall position for an existing race. The implementation's stated scope is a rights-cleared export; it is not evidence of a connected vendor, executed external import or automatic rights verification.

For future editorial data, the export path requires approved revisions, explicit training consent and a nonempty rights basis. The current corpus has zero human-approved examples. A real pilot should record data-owner permission, source version and collection date, transformations, reviewer consent and split membership before including external material. Weather, physiology, multilingual vendor feeds and independently judged real-race writing are outside the current training evidence.

## 6. Visual provenance

All eleven illustrations were generated or edited using the built-in image tool, with the user-provided portrait as a likeness reference and the approved sales illustration as a style reference. The original personal photographs are not distributed. The characters show the same creator in different illustrative roles. Exact chart values, report captions, links and QR codes are composed programmatically; decorative books, maps and paper stacks do not establish additional data sources. The final prompts and workspace artwork are retained in the brochure's `art/` folder.
