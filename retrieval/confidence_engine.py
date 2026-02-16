def compute_confidence(results):

    metadatas = results["metadatas"][0]
    distances = results["distances"][0]

    sources = set()
    draft_penalty = False

    for meta in metadatas:
        sources.add(meta.get("source_doc", "unknown"))

        if meta.get("confidence_tag") == "draft":
            draft_penalty = True

    # Agreement score
    source_count = len(sources)

    if source_count >= 3:
        agreement = 1.0
    elif source_count == 2:
        agreement = 0.8
    else:
        agreement = 0.6

    # Retrieval strength
    avg_distance = sum(distances) / len(distances)

    if avg_distance < 0.3:
        retrieval = 1.0
    elif avg_distance < 0.6:
        retrieval = 0.7
    else:
        retrieval = 0.4

    penalty = 0.6 if draft_penalty else 1.0

    score = agreement * retrieval * penalty

    if score > 0.8:
        label = "High"
    elif score > 0.5:
        label = "Medium"
    else:
        label = "Low"

    return score, label
