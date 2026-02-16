import os
import streamlit as st
from openai import OpenAI


def get_secret(key):
    # Try local env first
    value = os.getenv(key)

    # Fallback to Streamlit secrets
    if not value:
        value = st.secrets.get(key)

    return value


def get_openai_client():
    api_key = get_secret("OPENAI_API_KEY")

    if not api_key:
        raise ValueError("Missing OPENAI_API_KEY")

    return OpenAI(api_key=api_key)
