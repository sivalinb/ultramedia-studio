# ADR-001: Use the web application as the primary product interface

## Status

Accepted — September 10, 2026

## Decision

Keep the React/Vinext website as UltraMedia Studio's public product and portfolio interface. Do not add a separate Streamlit application now.

Python remains the main language for ingestion, RAG, agents, fine-tuning, evaluation, observability, and API contracts. The web application owns the customer experience and calls the Python FastAPI service.

## Why

- Race directors, editors, sponsors, commentators, and fans need a branded, responsive product—not an ML experiment console.
- The current website already joins the race atlas, newsroom, human review, model observability, Week 5 evidence, downloadable artifacts, and public portfolio narrative.
- A second Streamlit surface would duplicate authentication, state, review behavior, deployment, accessibility work, and screenshots without strengthening the model evidence.
- The FastAPI boundary keeps the Python intelligence layer reusable from the website, notebooks, batch jobs, and a future internal tool.

## When Streamlit would become useful

Add a private Streamlit workbench only if the team needs a fast internal interface for dataset upload, annotation, training-job launch, prompt comparison, or interactive error slicing and the notebook plus `/week5` dashboard no longer meet that need. It should consume the same Python packages and evidence contracts rather than become a second product implementation.

## Consequences

- Public experience: React 19, TypeScript, Vinext, Tailwind, and OpenAI Sites.
- Intelligence and control plane: Python 3.12, FastAPI, LangGraph, retrieval, evaluation, and QLoRA tooling.
- Experiment execution: reproducible Colab/Kaggle notebook and Python CLI.
- Evidence: `/week5`, repository reports, frozen predictions, run receipts, and observability artifacts.

