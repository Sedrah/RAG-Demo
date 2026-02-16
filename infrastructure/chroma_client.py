import os
import streamlit as st
import chromadb
from config.settings import settings


def get_secret(key, fallback=None):
    # 1. Try environment variable (.env / system)
    value = os.getenv(key)

    # 2. Try Streamlit secrets (cloud deployment)
    if not value:
        value = st.secrets.get(key, fallback)

    return value


def get_chroma_client():
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
