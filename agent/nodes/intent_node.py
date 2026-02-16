def intent_node(state):

    query = state["user_query"].lower()

    if "risk" in query or "pricing" in query:
        state["intent"] = "pricing_analysis"
    else:
        state["intent"] = "general"

    return state
