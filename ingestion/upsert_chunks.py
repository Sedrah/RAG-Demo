from infrastructure.collections import get_collection
import uuid


def upsert_chunks(chunks, metadatas):

    collection = get_collection()

    ids = [str(uuid.uuid4()) for _ in chunks]

    collection.upsert(
        ids=ids,
        documents=chunks,
        metadatas=metadatas
    )

    return len(ids)
