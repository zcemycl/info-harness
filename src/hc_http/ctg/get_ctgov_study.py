"""Fetch one ClinicalTrials.gov API v2 study by NCT id."""

from __future__ import annotations

from hc_http.ctg.ctgov_request import ctgov_request_json
from hc_http.ctg.project_ctgov_study import project_ctgov_study
from model.ctg.ctgov_study_hit import CtgovStudyHit
from model.ctg.is_placeholder_nct import is_placeholder_nct

_FIELDS = "NCTId,BriefTitle,OfficialTitle,OverallStatus,Acronym,OrgStudyId"


def run_get_ctgov_study(nctid: str) -> CtgovStudyHit:
    """GET /studies/{nctId} and return a projected study hit."""
    nid = nctid.strip().upper()
    if not nid.startswith("NCT"):
        raise ValueError(f"invalid NCT id: {nctid!r}")
    if is_placeholder_nct(nid):
        raise ValueError(f"placeholder/demo NCT id rejected: {nctid!r}")
    data = ctgov_request_json(
        f"/studies/{nid}",
        params={"fields": _FIELDS},
    )
    if not isinstance(data, dict):
        raise RuntimeError(f"Unexpected CT.gov type: {type(data).__name__}")
    return project_ctgov_study(data)
