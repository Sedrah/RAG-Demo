import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


import streamlit as st
from services.rag_service import run_rag_pipeline
from agent.run_agent_pipeline import run_agent_pipeline


# ---------- Page Config ----------
st.set_page_config(
    page_title="Pricing Decision Assistant",
    page_icon="💰",
    layout="wide"
)

st.title("💰 AI Pricing Decision Assistant")

# ---------- Sidebar ----------
st.sidebar.header("About")
st.sidebar.write(
    """
    This assistant answers pricing risk questions using internal policy documents.
    
    Features:
    - Retrieval Augmented Generation
    - Source Transparency
    - Confidence Scoring
    """
)

st.sidebar.header("Example Questions")
examples = [
    "What are pricing risks for EU enterprise customers?",
    "What discount limits apply to enterprise deals?",
    "Are long contracts risky in EU?"
]

for ex in examples:
    if st.sidebar.button(ex):
        st.session_state["query"] = ex


# ---------- Query Input ----------
query = st.text_input(
    "Ask a pricing question:",
    value=st.session_state.get("query", "")
)

# ---------- Run Pipeline ----------
if st.button("Ask AI") and query:

    with st.spinner("Retrieving knowledge and generating answer..."):

        rag_output = run_agent_pipeline(query)

        answer = rag_output["answer"]
        results = rag_output["results"]
        score = rag_output["confidence_score"]
        label = rag_output["confidence_label"]

    # ---------- Display Answer ----------
    st.subheader("🤖 AI Answer")
    st.write(answer)

    # ---------- Confidence Badge ----------
    if label == "High":
        st.success(f"Confidence: {label} ({round(score,2)})")

    elif label == "Medium":
        st.warning(f"Confidence: {label} ({round(score,2)})")

    else:
        st.error(f"Confidence: {label} ({round(score,2)})")

    # ---------- Source Transparency ----------
    st.subheader("📚 Retrieved Sources")

    docs = results["documents"][0]
    metas = results["metadatas"][0]
    distances = results["distances"][0]

    for i, (doc, meta, dist) in enumerate(zip(docs, metas, distances)):

        similarity = round(1 - dist, 2)

        with st.expander(f"Source {i+1} — Similarity {similarity}"):

            st.write("**Content:**")
            st.write(doc)

            st.write("**Source Document:**", meta.get("source_doc", "Unknown"))
            st.write("**Page:**", meta.get("page_number", "N/A"))
            st.write("**Confidence Tag:**", meta.get("confidence_tag", "Unknown"))
