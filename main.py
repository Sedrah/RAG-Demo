from retrieval.query_chroma import query_collection
from retrieval.confidence_engine import compute_confidence
from rag.build_context import build_context
from rag.build_prompt import build_prompt
from rag.generate_answer import generate_answer


def run():

    query = input("Ask pricing question: ")

    results = query_collection(query)

    context = build_context(results)

    score, label = compute_confidence(results)

    prompt = build_prompt(context, query, label)

    answer = generate_answer(prompt)

    print("\n--- AI Answer ---")
    print(answer)

    print("\nConfidence:", label, round(score, 2))


if __name__ == "__main__":
    run()
