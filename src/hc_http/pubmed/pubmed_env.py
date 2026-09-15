"""Resolve NCBI E-utilities base URL and optional API key."""

from __future__ import annotations

import os

from dotenv import load_dotenv

DEFAULT_PUBMED_BASE_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"


def pubmed_base_url() -> str:
    """Return PubMed E-utilities base URL (override with `PUBMED_BASE_URL`)."""
    load_dotenv()
    value = os.getenv("PUBMED_BASE_URL", DEFAULT_PUBMED_BASE_URL).strip()
    return value.rstrip("/")


def pubmed_api_key() -> str | None:
    """Return optional `NCBI_API_KEY` from the environment."""
    load_dotenv()
    value = os.getenv("NCBI_API_KEY", "").strip()
    return value or None
