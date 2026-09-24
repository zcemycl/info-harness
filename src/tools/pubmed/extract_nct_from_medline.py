"""Extract NCT ids from PubMed MEDLINE text."""

from __future__ import annotations

from model.fda.ctg_nct_link import CtgNctLink
from tools.fda.extract_ctg_nct_links import extract_ctg_nct_links


def extract_nct_from_medline(medline: str) -> list[CtgNctLink]:
    """Pull unique NCT######## ids from MEDLINE (SI lines and free text)."""
    return extract_ctg_nct_links(medline)
