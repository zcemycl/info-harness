"""Tool: search CT.gov API v2 by study id (OrgStudyId / SecondaryId / NCT)."""

from __future__ import annotations

from hc_http.ctg.search_ctgov_by_id import run_search_ctgov_by_id
from model.ctg.ctgov_study_hit import CtgovStudyHit


def search_ctgov_by_id(study_id: str, *, page_size: int = 10) -> list[CtgovStudyHit]:
    """Search ClinicalTrials.gov by study / org / secondary id."""
    return run_search_ctgov_by_id(study_id, page_size=page_size)
