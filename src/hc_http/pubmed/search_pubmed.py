"""Search PubMed via NCBI E-utilities esearch."""

from __future__ import annotations

from typing import Any

from hc_http.pubmed.pubmed_request import pubmed_request_json


def run_search_pubmed(
    query: str,
    *,
    retmax: int = 20,
    retstart: int = 0,
    sort: str = "relevance",
) -> dict[str, Any]:
    """GET esearch.fcgi for PubMed and return the JSON payload."""
    data = pubmed_request_json(
        "/esearch.fcgi",
        params={
            "db": "pubmed",
            "term": query,
            "retmax": retmax,
            "retstart": retstart,
            "sort": sort,
        },
    )
    if not isinstance(data, dict):
        raise RuntimeError(f"Unexpected PubMed response type: {type(data).__name__}")
    return data
