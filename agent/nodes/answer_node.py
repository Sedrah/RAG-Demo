from rag.build_context import build_context
from rag.build_prompt import build_prompt
from rag.generate_answer import generate_answer


def answer_node(state):

    results = {
        "documents": [state["retrieved_docs"]],
        "metadatas": [state["metadatas"]],
    }

    context = build_context(results)

    prompt = build_prompt(
        context,
        state["user_query"],
        state["confidence_label"]
    )

    answer = generate_answer(prompt)

    state["final_answer"] = answer

    return state
