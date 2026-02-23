# CLAUDE.md

Instructions and context for Claude Code when working in this repository.

## Project Overview

This is a **Pricing Decision Assistant** — a Retrieval-Augmented Generation (RAG) system that answers pricing questions using multi-source document retrieval, confidence scoring, escalation logic, and a LangGraph-based agent pipeline with a Streamlit web interface.

## Tech Stack

- **Python 3.11**
- **LangGraph** — multi-node agent orchestration
- **ChromaDB (Chroma Cloud)** — vector store for semantic search
- **OpenAI (gpt-4o-mini)** — LLM for answer generation
- **Streamlit** — web UI
- **python-dotenv** — environment variable management

## Project Structure

```
RAG-Demo/
├── agent/               # LangGraph agent graph and nodes
│   ├── graph.py         # 5-node pipeline: Intent → Retrieval → Confidence → Escalation → Answer
│   ├── run_agent_pipeline.py  # Entry point for agent execution
│   └── nodes/           # Individual node implementations
├── config/
│   └── settings.py      # Settings class loading from .env
├── infrastructure/
│   ├── clients.py        # Chroma and OpenAI client initialization
│   └── secrets.py        # Unified secrets getter (.env + Streamlit Cloud)
├── ingestion/           # Document chunking, metadata, upserting
├── rag/                 # Context building, prompt engineering, answer generation
├── retrieval/
│   └── confidence_engine.py  # Multi-factor confidence scoring
├── scripts/
│   └── ingest_demo.py   # Demo ingestion script
├── services/
│   ├── rag_service.py        # Linear RAG pipeline
│   └── ingestion_service.py  # Wraps chunking and upserting
├── ui/
│   └── streamlit_app.py # Main web interface (port 8501)
└── main.py              # CLI entry point
```

## Running the Project

### Web App
```bash
streamlit run ui/streamlit_app.py
```

### CLI
```bash
python main.py
```

### Ingest Demo Documents
```bash
python scripts/ingest_demo.py
```

## Environment Setup

Create a `.env` file in the project root with:
```
CHROMA_API_KEY=...
CHROMA_TENANT=...
CHROMA_DATABASE=...
OPENAI_API_KEY=...
```

The Chroma collection name is `pricing_chunks` (defined in `config/settings.py`).

For Streamlit Cloud deployment, use `.streamlit/secrets.toml` instead — the secrets module handles both automatically.

## Key Architectural Patterns

### Agent Pipeline (LangGraph)
Sequential 5-node graph in `agent/graph.py`:
1. **Intent** — classify and extract the query intent
2. **Retrieval** — semantic search against Chroma (top 5 results)
3. **Confidence** — multi-factor scoring
4. **Escalation** — flag low-confidence results
5. **Answer** — generate response with GPT-4o-mini

State type is `PricingAgentState` with optional fields populated as the pipeline runs.

### Confidence Scoring (`retrieval/confidence_engine.py`)
Three factors combined:
- **Agreement Score**: 1 source → 0.6, 2 → 0.8, 3+ → 1.0
- **Retrieval Strength**: embedding distance < 0.3 → 1.0, 0.3–0.6 → 0.7, > 0.6 → 0.4
- **Draft Penalty**: multiply by 0.6 if document is marked draft

Labels: **High** > 0.8, **Medium** 0.5–0.8, **Low** < 0.5
**Escalation** is triggered when confidence < 0.5.

### Document Metadata Schema
Ingested chunks include: `region`, `customer_segment`, `source_doc`, `page_number`, `draft`

### Secrets Management
`infrastructure/secrets.py` provides a unified getter that works both locally (`.env`) and on Streamlit Cloud (`.streamlit/secrets.toml`). Always use this for accessing secrets — do not read env vars directly.

## Development Notes

- Do not commit `.env` or `.streamlit/secrets.toml` — both are gitignored
- The `venv/` directory is also gitignored; manage dependencies via `requirements.txt`
- Keep `requirements.txt` up to date when adding new packages
- The devcontainer uses Python 3.11 and opens `ui/streamlit_app.py` by default on port 8501
