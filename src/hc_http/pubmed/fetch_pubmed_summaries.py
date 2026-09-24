"""Fetch PubMed article summaries via NCBI E-utilities esummary."""

from __future__ import annotations

from hc_http.pubmed.pubmed_request import pubmed_request_json
from model.parse_model import parse_model
from model.pubmed.pubmed_summary_response import PubmedSummaryResponse


def run_fetch_pubmed_summaries(pmids: list[str]) -> PubmedSummaryResponse:
    """GET esummary.fcgi for PubMed IDs and return a typed payload."""
    if not pmids:
        return PubmedSummaryResponse()
    data = pubmed_request_json(
        "/esummary.fcgi",
        params={"db": "pubmed", "id": ",".join(pmids)},
    )
    return parse_model(PubmedSummaryResponse, data)
