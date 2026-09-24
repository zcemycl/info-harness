"""Resolve the HC platform API base URL from `.env`."""

from __future__ import annotations

import os

from dotenv import load_dotenv


def hc_api_base_url() -> str:
    """Return required `HC_API_BASE_URL` from the environment."""
    load_dotenv()
    value = os.getenv("HC_API_BASE_URL", "").strip()
    if not value:
        raise ValueError("Missing required env var: HC_API_BASE_URL")
    return value.rstrip("/")
