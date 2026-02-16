import os
import streamlit as st

def get_secret(key, default=None):
    """
    Returns a secret from environment variables or Streamlit secrets.
    """
    # Try OS environment first (local dev / Codespaces)
    value = os.getenv(key)

    # Fallback to Streamlit secrets (Cloud)
    if not value:
        value = st.secrets.get(key, default)

    return value
