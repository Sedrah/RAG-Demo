# Pricing Decision Assistant

A **Retrieval-Augmented Generation (RAG)** system that answers pricing questions using multi-source document retrieval, confidence scoring, escalation logic, and a LangGraph-based agent pipeline with a Streamlit web interface.

---

## Overview

This project demonstrates a production-style RAG pipeline where pricing questions are answered by:
1. Retrieving relevant documents from a vector store (Chroma)
2. Scoring confidence based on source agreement and retrieval quality
3. Escalating low-confidence answers for human review
4. Generating a final answer with GPT-4o-mini, grounded in retrieved context

---

## Tech Stack

| Layer | Technology |
|---|---|
| Agent Orchestration | [LangGraph](https://github.com/langchain-ai/langgraph) |
| Vector Store | [ChromaDB (Chroma Cloud)](https://www.trychroma.com/) |
| LLM | OpenAI GPT-4o-mini |
| Web UI | [Streamlit](https://streamlit.io/) |
| Environment | python-dotenv / Streamlit secrets |
| Runtime | Python 3.11 |

---

## Project Structure

```
RAG-Demo/
├── agent/                        # LangGraph agent pipeline
│   ├── graph.py                  # 5-node state machine
│   ├── state.py                  # PricingAgentState TypedDict
│   ├── run_agent_pipeline.py     # Pipeline entry point with trace logging
│   └── nodes/
│       ├── intent_node.py        # Classify query intent
│       ├── retrieval_node.py     # Semantic search against Chroma
│       ├── confidence_node.py    # Compute confidence score
│       ├── escalation_node.py    # Flag low-confidence results
│       └── answer_node.py        # Generate final answer
├── config/
│   └── settings.py               # Loads env vars, defines collection name
├── infrastructure/
│   ├── chroma_client.py          # Chroma Cloud client
│   ├── openai_client.py          # OpenAI client
│   ├── collections.py            # Chroma collection accessor
│   └── secrets.py                # Unified secrets getter (local + Streamlit Cloud)
├── ingestion/
│   ├── chunking.py               # 300-word chunks with 50-word overlap
│   ├── metadata_builder.py       # Chunk metadata schema
│   └── upsert_chunks.py          # UUID generation and Chroma upsert
├── rag/
│   ├── build_context.py          # Format retrieved docs into context string
│   ├── build_prompt.py           # System + context + question prompt template
│   └── generate_answer.py        # GPT-4o-mini call
├── retrieval/
│   ├── query_chroma.py           # Top-5 semantic search
│   └── confidence_engine.py      # Multi-factor confidence scoring
├── scripts/
│   └── ingest_demo.py            # Ingest sample pricing documents
├── services/
│   ├── rag_service.py            # Linear RAG pipeline wrapper
│   └── ingestion_service.py      # Chunking + upsert orchestration
├── ui/
│   └── streamlit_app.py          # Web interface (port 8501)
├── docs/
│   ├── architecture.md
│   └── workflow_design.md
└── main.py                       # CLI entry point
```

---

## Agent Pipeline

The core pipeline is a **5-node LangGraph state machine** defined in [agent/graph.py](agent/graph.py):

```
Intent → Retrieval → Confidence → Escalation → Answer
```

| Node | What it does |
|---|---|
| **Intent** | Classifies query as `pricing_analysis` or `general` |
| **Retrieval** | Queries Chroma for the top 5 semantically similar chunks |
| **Confidence** | Scores result quality using multi-factor scoring |
| **Escalation** | Sets `escalation_required = True` when confidence < 0.5 |
| **Answer** | Builds prompt and calls GPT-4o-mini to generate the response |

State is tracked in `PricingAgentState` — a TypedDict with optional fields populated as the graph progresses.

---

## Confidence Scoring

Defined in [retrieval/confidence_engine.py](retrieval/confidence_engine.py):

| Factor | Logic |
|---|---|
| **Agreement Score** | 1 source → 0.6 · 2 sources → 0.8 · 3+ sources → 1.0 |
| **Retrieval Strength** | distance < 0.3 → 1.0 · 0.3–0.6 → 0.7 · > 0.6 → 0.4 |
| **Draft Penalty** | Multiplied by 0.6 if any source is marked draft |

**Final score** = agreement × retrieval × draft penalty

| Label | Range |
|---|---|
| High | > 0.8 |
| Medium | 0.5 – 0.8 |
| Low (escalated) | < 0.5 |

---

## Document Metadata Schema

Each ingested chunk includes:

```python
{
    "region": str,
    "customer_segment": str,
    "source_doc": str,
    "page_number": int,
    "draft": bool
}
```

Chunking uses 300-word windows with 50-word overlap ([ingestion/chunking.py](ingestion/chunking.py)).

---

## Getting Started

### 1. Prerequisites

- Python 3.11
- A [Chroma Cloud](https://www.trychroma.com/) account
- An OpenAI API key

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure environment

Create a `.env` file in the project root:

```env
CHROMA_API_KEY=...
CHROMA_TENANT=...
CHROMA_DATABASE=...
OPENAI_API_KEY=...
```

> For Streamlit Cloud deployment, use `.streamlit/secrets.toml` instead — the secrets module handles both automatically.

### 4. Ingest demo documents

```bash
python scripts/ingest_demo.py
```

### 5. Run the web app

```bash
streamlit run ui/streamlit_app.py
```

Open [http://localhost:8501](http://localhost:8501) in your browser.

### 6. Run via CLI

```bash
python main.py
```

---

## Streamlit UI Features

- Natural language input for pricing questions
- Sidebar with example queries and system capabilities
- Color-coded confidence badge (green / yellow / red)
- Escalation warning for low-confidence answers
- Source transparency panel with retrieved documents, similarity scores, and metadata
- Agent execution trace visualization

---

## Deployment

This project is Streamlit Cloud-ready. Set secrets in `.streamlit/secrets.toml` using the same keys as the `.env` file. The `infrastructure/secrets.py` module detects the environment automatically.

---

## Development Notes

- Do not commit `.env` or `.streamlit/secrets.toml` — both are gitignored
- Manage dependencies via `requirements.txt`; keep it updated when adding packages
- The devcontainer uses Python 3.11 and auto-launches the Streamlit app on port 8501
- The Chroma collection name is `pricing_chunks` (configured in `config/settings.py`)
