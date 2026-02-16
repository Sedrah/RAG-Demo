import chromadb
from config.settings import settings


def get_chroma_client():

    if not settings.CHROMA_API_KEY:
        raise ValueError("Missing CHROMA_API_KEY")

    return chromadb.CloudClient(
        api_key=settings.CHROMA_API_KEY,
        tenant=settings.CHROMA_TENANT,
        database=settings.CHROMA_DATABASE
    )
