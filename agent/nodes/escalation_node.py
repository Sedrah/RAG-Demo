def escalation_node(state):

    score = state["confidence_score"]

    state["escalation_required"] = score < 0.5

    return state
