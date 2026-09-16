"""Tool: fetch PubMed article summaries by PMID."""

from __future__ import annotations

from hc_http.pubmed.fetch_pubmed_summaries import run_fetch_pubmed_summaries
from model.pubmed.pubmed_summary_response import PubmedSummaryResponse


def fetch_pubmed_summaries(pmids: list[str]) -> PubmedSummaryResponse:
    """Fetch typed PubMed esummary payloads for PMIDs."""
    return run_fetch_pubmed_summaries(pmids)
