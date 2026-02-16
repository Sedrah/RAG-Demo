def build_context(results):
    documents = results.get("documents", [])
    distances = results.get("distances", [])

    # Handle nested lists safely
    documents = documents[0] if documents else []
    distances = distances[0] if distances else []

    context_parts = []

    for i, doc in enumerate(documents):
        score = distances[i] if i < len(distances) else None
        context_parts.append(f"{doc} (score={score})")

    return "\n".join(context_parts)
