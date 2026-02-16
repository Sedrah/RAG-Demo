from ingestion.chunking import chunk_document
from ingestion.metadata_builder import build_metadata
from ingestion.upsert_chunks import upsert_chunks


def ingest_document(
    text,
    region,
    segment,
    source,
    page
):

    chunks = chunk_document(text)

    metadatas = [
        build_metadata(region, segment, source, page)
        for _ in chunks
    ]

    inserted = upsert_chunks(chunks, metadatas)

    return inserted
