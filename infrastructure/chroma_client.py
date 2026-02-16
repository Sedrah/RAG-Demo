import chromadb
from infrastructure.secrets import get_secret

def get_chroma_client():
    """
    Returns a CloudClient for Chroma Cloud.
    Works locally (.env) and on Streamlit Cloud.
    """
    api_key = get_secret("CHROMA_API_KEY")
    tenant = get_secret("CHROMA_TENANT")
    database = get_secret("CHROMA_DATABASE")

    if not api_key:
        raise ValueError("Missing CHROMA_API_KEY")

    return chromadb.CloudClient(
        api_key=api_key,
        tenant=tenant,
        database=database
    )
