"""Resolve ClinicalTrials.gov API v2 base URL."""

from __future__ import annotations

import os

from dotenv import load_dotenv

DEFAULT_CTGOV_BASE_URL = "https://clinicaltrials.gov/api/v2"


def ctgov_base_url() -> str:
    """Return CT.gov API v2 base URL (override with `CTGOV_BASE_URL`)."""
    load_dotenv()
    value = os.getenv("CTGOV_BASE_URL", DEFAULT_CTGOV_BASE_URL).strip()
    return value.rstrip("/")
