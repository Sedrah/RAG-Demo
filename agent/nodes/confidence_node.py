from retrieval.confidence_engine import compute_confidence


def confidence_node(state):

    results = {
        "documents": [state["retrieved_docs"]],
        "metadatas": [state["metadatas"]],
        "distances": [state["distances"]],
    }

    score, label = compute_confidence(results)

    state["confidence_score"] = score
    state["confidence_label"] = label

    return state
