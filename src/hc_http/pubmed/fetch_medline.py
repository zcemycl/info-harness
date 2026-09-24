"""Fetch PubMed MEDLINE records as plain text via NCBI efetch."""

from __future__ import annotations

from typing import Any

import httpx

from hc_http.pubmed.pubmed_env import pubmed_api_key, pubmed_base_url


def run_fetch_medline(pmids: list[str], *, timeout: float = 60.0) -> str:
    """GET efetch.fcgi medline text for PubMed IDs (SI / abstract fields)."""
    if not pmids:
        return ""
    params: dict[str, Any] = {
        "db": "pubmed",
        "id": ",".join(pmids),
        "rettype": "medline",
        "retmode": "text",
    }
    api_key = pubmed_api_key()
    if api_key:
        params["api_key"] = api_key
    url = f"{pubmed_base_url()}/efetch.fcgi"
    try:
        with httpx.Client(timeout=timeout) as client:
            response = client.get(url, params=params)
    except httpx.RequestError as exc:
        raise RuntimeError(f"PubMed efetch failed: {exc}") from exc
    if response.status_code >= 400:
        raise RuntimeError(
            f"PubMed efetch failed ({response.status_code}): {response.text}"
        )
    return str(response.text)
