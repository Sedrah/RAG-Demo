from retrieval.query_chroma import query_collection
from retrieval.confidence_engine import compute_confidence
from rag.build_context import build_context
from rag.build_prompt import build_prompt
from rag.generate_answer import generate_answer


def run_rag_pipeline(query: str):

    # Retrieval
    results = query_collection(query)

    # Context building
    context = build_context(results)

    # Confidence scoring
    score, label = compute_confidence(results)

    # Prompt creation
    prompt = build_prompt(context, query, label)

    # LLM generation
    answer = generate_answer(prompt)

    return {
        "answer": answer,
        "results": results,
        "confidence_score": score,
        "confidence_label": label
    }
