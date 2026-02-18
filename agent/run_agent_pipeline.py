from retrieval.query_chroma import query_collection
from retrieval.confidence_engine import compute_confidence
from rag.generate_answer import generate_answer
from rag.build_context import build_context
from rag.build_prompt import build_prompt


def run_agent_pipeline(query):
    

    execution_trace = []
    state = {
        "query": query,
        "results": [],
        "answer": "",
        "confidence_score": 0,
        "confidence_label": "",
        "execution_trace": [],
        "escalation_required": False
    }

    # --------------------------
    # NODE 1 — Retrieval
    # --------------------------
    state["execution_trace"].append("Retrieval")

    results = query_collection(query)
    state["results"] = results

    # --------------------------
    # NODE 2 — Confidence
    # --------------------------
    state["execution_trace"].append("Confidence Evaluation")

    score, label = compute_confidence(results)

    state["confidence_score"] = score
    state["confidence_label"] = label

    # --------------------------
    # NODE 3 — Escalation Logic
    # --------------------------
    if score < 0.4:
        state["execution_trace"].append("Escalation Triggered")
        state["escalation_required"] = True

    # --------------------------
    # NODE 4 — Answer Generation
    # --------------------------
    state["execution_trace"].append("Answer Generation")

    context = build_context(results)

    prompt = build_prompt(context, query, state["confidence_label"])

    answer = generate_answer(prompt)
    state["answer"] = answer

    return state
