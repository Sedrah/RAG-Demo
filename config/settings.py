import os
from dotenv import load_dotenv

load_dotenv()

class Settings:

    CHROMA_API_KEY = os.getenv("CHROMA_API_KEY")
    CHROMA_TENANT = os.getenv("CHROMA_TENANT")
    CHROMA_DATABASE = os.getenv("CHROMA_DATABASE")

    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

    COLLECTION_NAME = "pricing_chunks"


settings = Settings()