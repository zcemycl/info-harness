"""Tool: search PubMed via NCBI E-utilities."""

from __future__ import annotations

from typing import Any

from hc_http.pubmed.search_pubmed import run_search_pubmed


def search_pubmed(
    query: str,
    *,
    retmax: int = 20,
    retstart: int = 0,
    sort: str = "relevance",
) -> dict[str, Any]:
    """Search PubMed and return the esearch JSON payload."""
    return run_search_pubmed(query, retmax=retmax, retstart=retstart, sort=sort)
