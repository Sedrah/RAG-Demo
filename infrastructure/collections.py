from infrastructure.chroma_client import get_chroma_client
from config.settings import settings


def get_collection():

    client = get_chroma_client()

    return client.get_collection(name=settings.COLLECTION_NAME)
