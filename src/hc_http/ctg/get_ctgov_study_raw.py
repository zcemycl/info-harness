"""Fetch full ClinicalTrials.gov API v2 study JSON by NCT id."""

from __future__ import annotations

from typing import Any

from hc_http.ctg.ctgov_request import ctgov_request_json


def run_get_ctgov_study_raw(nctid: str) -> dict[str, Any]:
    """GET /studies/{nctId} with no fields filter (full study payload)."""
    nid = nctid.strip().upper()
    if not nid.startswith("NCT"):
        raise ValueError(f"invalid NCT id: {nctid!r}")
    data = ctgov_request_json(f"/studies/{nid}")
    if not isinstance(data, dict):
        raise RuntimeError(f"Unexpected CT.gov type: {type(data).__name__}")
    return data
