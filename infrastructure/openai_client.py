from openai import OpenAI
from infrastructure.secrets import get_secret

def get_openai_client():
    """
    Returns an OpenAI client using environment or Streamlit secrets.
    """
    api_key = get_secret("OPENAI_API_KEY")

    if not api_key:
        raise ValueError("Missing OPENAI_API_KEY")

    return OpenAI(api_key=api_key)
