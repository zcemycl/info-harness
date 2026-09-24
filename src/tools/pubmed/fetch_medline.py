"""Tool: fetch PubMed MEDLINE text for PMIDs."""

from __future__ import annotations

from hc_http.pubmed.fetch_medline import run_fetch_medline


def fetch_medline(pmids: list[str]) -> str:
    """Return MEDLINE text (includes SI ClinicalTrials.gov lines when present)."""
    return run_fetch_medline(pmids)
