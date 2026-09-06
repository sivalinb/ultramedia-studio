# UltraMedia Studio

UltraMedia Studio is an AI newsroom for ultramarathons. It converts race timing, GPS, course, weather, and historical data into evidence-linked story drafts, commentator briefs, social content, and finisher recaps while keeping publication behind a human approval gate.

- **Product:** [ultramedia-studio.siva-babu.chatgpt.site](https://ultramedia-studio.siva-babu.chatgpt.site)
- **Working newsroom:** `/studio`
- **API docs:** `http://localhost:8000/docs` when the Python service is running
- **System design:** [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md)

All athlete names and live timing values in the public portfolio are synthetic. Official course pages are used only as attributed context. Production use requires data rights, athlete privacy, editorial, accessibility, and security review with each race organizer.

## What is implemented

- Governed race/timing ingestion from local fixtures and rights-cleared CSV exports
- Hybrid dense-plus-lexical retrieval over timing and course evidence
- Six-stage LangGraph workflow: moment detection, evidence retrieval, story writing, fact verification, safety editing, and human review queue
- Qwen-compatible provider routing: zero-cost deterministic mode, local Ollama, or Fireworks
- Claim/citation validation and a guard against unsupported health or intent inferences
- Persistent race, story, approval, and trace records
- Human approve/revise/reject endpoint—generation never publishes directly
- Release evaluation endpoint and pytest suite covering the safe-stop paths
- QLoRA data preparation, training, adapter merge, and Ollama packaging scripts
- Responsive React/Vinext newsroom connected to the Python API when configured
- Privacy-minimized traces ready for OpenTelemetry/Phoenix and LangSmith

## Free-first technology choices

| Layer | Default | Production path |
| --- | --- | --- |
| Main language | Python 3.12 | Python 3.12 |
| API | FastAPI + Pydantic | FastAPI behind a managed container runtime |
| Workflow | LangGraph | LangGraph with durable PostgreSQL checkpointing |
| Database | SQLite | PostgreSQL 16 + pgvector |
| Retrieval | Local hybrid hashing + lexical search | Fireworks embeddings/rerank or pgvector/Pinecone |
| Generation | Deterministic local provider | Qwen3-4B through Ollama or Fireworks |
| Fine-tuning | Reproducible scripts only | QLoRA on an on-demand GPU, then local inference |
| Observability | SQLite traces + OpenTelemetry | Phoenix self-hosted; LangSmith optional |
| Web | React 19, TypeScript, Vinext, Tailwind | OpenAI Sites / Cloudflare Workers |
| Testing | pytest, Ruff, deterministic evals | Same suite plus provider-backed shadow evals |

The model target is [Qwen3-4B-Instruct-2507](https://huggingface.co/Qwen/Qwen3-4B-Instruct-2507), an Apache-2.0 model that is small enough for a portfolio-scale QLoRA experiment. Ollama provides the no-token local serving path. Fine-tuning teaches editorial format and voice; current race facts remain in RAG.

## Local quick start

Use Python 3.11 or newer.

```bash
cp .env.example .env.local
cd backend
python -m venv .venv
.venv/bin/pip install -e '.[dev]'
.venv/bin/uvicorn ultramedia.main:app --reload
```

In a second terminal:

```bash
npm install
NEXT_PUBLIC_ULTRAMEDIA_API_URL=http://localhost:8000 npm run dev
```

Open the website and choose **Open newsroom**. The API also exposes interactive OpenAPI documentation at `http://localhost:8000/docs`.

## Test and evaluate

```bash
cd backend
.venv/bin/ruff check src tests scripts
.venv/bin/pytest --cov=ultramedia
.venv/bin/ultramedia-eval
```

The release gate currently measures retrieval recall, citation validity, mandatory human review, and unsupported sensitive inference. The checked-in fixture is deliberately small and synthetic; provider-backed and large-corpus results must be labeled separately from local deterministic results.

## Local model and fine-tuning

Run the base model without an API bill:

```bash
ollama run qwen3:4b-instruct
PROVIDER_MODE=ollama .venv/bin/uvicorn ultramedia.main:app --reload
```

Prepare training examples only from human-approved drafts:

```bash
.venv/bin/python scripts/prepare_training_data.py --database ultramedia.db
.venv/bin/pip install -e '.[finetune]'
.venv/bin/python scripts/train_qlora.py
.venv/bin/python scripts/merge_adapter.py
```

Convert the merged model to GGUF with llama.cpp, place it at `backend/artifacts/qwen3-ultramedia.gguf`, then run `ollama create ultramedia-qwen3 -f Modelfile`.

## Reusing CommonGroundAI integrations

UltraMedia intentionally uses the same environment variable contracts for Fireworks, Mistral, Pinecone, and LangSmith. Real secret values are never copied into this repository. Re-enter or securely clone those secrets in the target deployment secret manager, and use an UltraMedia-specific Pinecone namespace and LangSmith project to prevent cross-product data mixing.

## API journey

1. `POST /api/v1/races/wser-demo/ingest` loads the governed demo source.
2. `POST /api/v1/stories/generate` runs the six-agent workflow.
3. `GET /api/v1/traces/{trace_id}` explains the run without exposing raw prompts.
4. `POST /api/v1/stories/{story_id}/review` records the human decision.
5. `POST /api/v1/evals/run` runs the deterministic release gate.

## Repository map

```text
app/                     React product and working newsroom
backend/src/ultramedia/  Python API, retrieval, agents, persistence, evals
backend/scripts/         QLoRA preparation, training, and model merge
backend/data/            Governed synthetic portfolio fixture
docs/                    Architecture, governance, deployment, model card
docker-compose.yml       PostgreSQL, API, Phoenix, optional Ollama
```

