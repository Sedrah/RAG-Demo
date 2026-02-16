from openai import OpenAI
from config.settings import settings


def get_openai_client():
    return OpenAI(api_key=settings.OPENAI_API_KEY)
