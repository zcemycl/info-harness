"""Search PubMed via NCBI E-utilities esearch."""

from __future__ import annotations

from hc_http.pubmed.pubmed_request import pubmed_request_json
from model.parse_model import parse_model
from model.pubmed.pubmed_search_response import PubmedSearchResponse


def run_search_pubmed(
    query: str,
    *,
    retmax: int = 20,
    retstart: int = 0,
    sort: str = "relevance",
) -> PubmedSearchResponse:
    """GET esearch.fcgi for PubMed and return a typed payload."""
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
    return parse_model(PubmedSearchResponse, data)
