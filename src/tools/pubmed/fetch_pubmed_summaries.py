"""Tool: fetch PubMed article summaries by PMID."""

from __future__ import annotations

from typing import Any

from hc_http.pubmed.fetch_pubmed_summaries import run_fetch_pubmed_summaries


def fetch_pubmed_summaries(pmids: list[str]) -> dict[str, Any]:
    """Fetch PubMed esummary payloads for PMIDs."""
    return run_fetch_pubmed_summaries(pmids)
