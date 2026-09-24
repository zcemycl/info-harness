"""Project a raw CT.gov API v2 study object into CtgovStudyHit."""

from __future__ import annotations

from typing import Any

from model.ctg.ctgov_study_hit import CtgovStudyHit

_STUDY_URL = "https://clinicaltrials.gov/study"


def project_ctgov_study(raw: dict[str, Any]) -> CtgovStudyHit:
    """Map protocolSection identification/status modules to a hit."""
    protocol = raw.get("protocolSection") or {}
    ident = protocol.get("identificationModule") or {}
    status = protocol.get("statusModule") or {}
    nctid = str(ident.get("nctId") or "").strip()
    if not nctid:
        raise RuntimeError("CT.gov study missing nctId")
    return CtgovStudyHit(
        nctid=nctid,
        brief_title=ident.get("briefTitle"),
        official_title=ident.get("officialTitle"),
        acronym=ident.get("acronym"),
        org_study_id=(ident.get("orgStudyIdInfo") or {}).get("id"),
        overall_status=status.get("overallStatus"),
        ctg_url=f"{_STUDY_URL}/{nctid}",
    )
