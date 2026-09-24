"""Search ClinicalTrials.gov API v2 by study title / acronym."""

from __future__ import annotations

from typing import Any

from hc_http.ctg.ctgov_request import ctgov_request_json
from hc_http.ctg.project_ctgov_study import project_ctgov_study
from model.ctg.ctgov_study_hit import CtgovStudyHit

_FIELDS = "NCTId,BriefTitle,OfficialTitle,OverallStatus,Acronym,OrgStudyId"


def run_search_ctgov_by_titles(
    name: str,
    *,
    page_size: int = 10,
) -> list[CtgovStudyHit]:
    """GET /studies with query.titles; return projected hits."""
    q = name.strip()
    if not q:
        raise ValueError("study name must be non-empty")
    size = max(1, min(int(page_size), 100))
    data = ctgov_request_json(
        "/studies",
        params={"query.titles": q, "pageSize": size, "fields": _FIELDS},
    )
    return _project_studies(data)


def _project_studies(data: Any) -> list[CtgovStudyHit]:
    if not isinstance(data, dict):
        raise RuntimeError(f"Unexpected CT.gov type: {type(data).__name__}")
    raw = data.get("studies") or []
    if not isinstance(raw, list):
        raise RuntimeError("CT.gov studies field is not a list")
    return [project_ctgov_study(item) for item in raw if isinstance(item, dict)]
