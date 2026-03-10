# AI Study Helper Agent

A Python-based AI Study Helper agent backend, designed for **learning, testing, and exploring AI agent patterns**.

This project implements an **MCP-inspired agent architecture** with **tool-based execution**, structured `Planner` flow, and **LLM abstraction** for easy switching between **FakeLLM** (offline) and **OpenAI / Azure LLM** (online).

---

## Key Features

- **Agent-based reasoning** – orchestrates multiple tools in a deterministic flow
- **Tool architecture** – summary, key points, question generation, answer generation
- **LLM abstraction** – supports FakeLLM for offline dev/testing and OpenAI LLM for real AI responses
- **RAG (Retrieval Augmented Generation)** – optional FAISS knowledge base integration for context-aware answers
- **PDF Export** – structured study materials (summary, key points, Q&A) exportable to PDF
- **Testable core** – fully unit-testable architecture
- **Future-ready** – designed to easily add FastAPI endpoints, more tools, embeddings, or multi-agent orchestration

---

## Current Status

- Core Agent, Planner, Tools fully implemented
- CLI interface for testing and PDF export
- FakeLLM functional; OpenAI integration ready (requires API key)
- RAG/FAISS knowledge base implemented for context-aware material
- PDF export tool available via CLI

---

## .env file configuration

- `USE_OPENAI`=true/false (true if you use, false if you use fake llm)
- `OPENAI_API_KEY`=sk-xxxxxxxx (API key)
- `OPENAI_MODEL`=xyz (example model: gpt-3.5-turbo)

## Requirements
```bash
poetry install
```

## Running app
```bash
poetry run python -m app.main
```