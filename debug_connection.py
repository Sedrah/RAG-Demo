from infrastructure.chroma_client import get_chroma_client

client = get_chroma_client()

print(client.list_collections())
