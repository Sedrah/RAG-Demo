from agent.graph import graph


def run_agent_pipeline(query):

    state = graph.invoke({
        "user_query": query
    })

    # Rebuild "results" structure for UI compatibility
    results = {
        "documents": [state["retrieved_docs"]],
        "metadatas": [state["metadatas"]],
        "distances": [state["distances"]],
    }

    return {
        "answer": state["final_answer"],
        "results": results,
        "confidence_score": state["confidence_score"],
        "confidence_label": state["confidence_label"]
    }
