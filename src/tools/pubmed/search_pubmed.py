"""Tool: search PubMed via NCBI E-utilities."""

from __future__ import annotations

from hc_http.pubmed.search_pubmed import run_search_pubmed
from model.pubmed.pubmed_search_response import PubmedSearchResponse


def search_pubmed(
    query: str,
    *,
    retmax: int = 20,
    retstart: int = 0,
    sort: str = "relevance",
) -> PubmedSearchResponse:
    """Search PubMed and return a typed esearch payload."""
    return run_search_pubmed(query, retmax=retmax, retstart=retstart, sort=sort)
