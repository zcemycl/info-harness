"""Tool: search CT.gov API v2 by study title / acronym."""

from __future__ import annotations

from hc_http.ctg.search_ctgov_by_titles import run_search_ctgov_by_titles
from model.ctg.ctgov_study_hit import CtgovStudyHit


def search_ctgov_by_titles(name: str, *, page_size: int = 10) -> list[CtgovStudyHit]:
    """Search ClinicalTrials.gov by titles / acronym."""
    return run_search_ctgov_by_titles(name, page_size=page_size)
