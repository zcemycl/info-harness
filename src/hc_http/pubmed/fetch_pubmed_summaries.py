"""Fetch PubMed article summaries via NCBI E-utilities esummary."""

from __future__ import annotations

from typing import Any

from hc_http.pubmed.pubmed_request import pubmed_request_json


def run_fetch_pubmed_summaries(pmids: list[str]) -> dict[str, Any]:
    """GET esummary.fcgi for PubMed IDs and return the JSON payload."""
    if not pmids:
        return {"result": {}}
    data = pubmed_request_json(
        "/esummary.fcgi",
        params={"db": "pubmed", "id": ",".join(pmids)},
    )
    if not isinstance(data, dict):
        raise RuntimeError(f"Unexpected PubMed response type: {type(data).__name__}")
    return data
