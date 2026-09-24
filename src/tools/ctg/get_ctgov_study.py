"""Tool: fetch one CT.gov API v2 study by NCT id."""

from __future__ import annotations

from hc_http.ctg.get_ctgov_study import run_get_ctgov_study
from model.ctg.ctgov_study_hit import CtgovStudyHit


def get_ctgov_study(nctid: str) -> CtgovStudyHit:
    """GET a single ClinicalTrials.gov study by NCT id."""
    return run_get_ctgov_study(nctid)
