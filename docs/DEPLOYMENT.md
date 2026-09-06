# Deployment guide

## Local portfolio

The default configuration is free: SQLite, deterministic provider, the Python API, and the React website. Add Ollama for local Qwen inference and Phoenix for local trace inspection.

## Container deployment

`docker compose up --build` starts PostgreSQL/pgvector, the API, and Phoenix. Add `--profile local-model` for Ollama. Pull `qwen3:4b-instruct` before selecting `PROVIDER_MODE=ollama`.

## Production deployment

1. Deploy the Python container to a service that supports Python 3.12 and HTTPS.
2. Use managed PostgreSQL with encrypted backups and point-in-time recovery.
3. Configure only rights-cleared race connectors.
4. Add provider secrets through the host secret manager, never repository variables.
5. Set `APPROVAL_API_KEY` or replace it with organization SSO before editor use.
6. Set `NEXT_PUBLIC_ULTRAMEDIA_API_URL` on the website to the HTTPS API origin.
7. Run Ruff, pytest, deterministic evals, and provider-backed shadow evals before release.
8. Publish the website only after API health, CORS, approval, and rollback checks pass.

## CommonGroundAI secret reuse

The existing CommonGroundAI deployment contains Fireworks, Mistral, Pinecone, and LangSmith secrets, but secret managers correctly prevent reading those values back. Copy or re-enter them through a secure administrator workflow. Use `ultramedia-public-v1` rather than the CommonGround namespace and `ultramedia-production` rather than the CommonGround LangSmith project.

