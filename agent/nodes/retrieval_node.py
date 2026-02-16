from retrieval.query_chroma import query_collection


def retrieval_node(state):

    results = query_collection(state["user_query"])

    state["retrieved_docs"] = results["documents"][0]
    state["metadatas"] = results["metadatas"][0]
    state["distances"] = results["distances"][0]

    return state
