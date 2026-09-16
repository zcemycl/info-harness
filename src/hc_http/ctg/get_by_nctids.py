"""Fetch CTG studies by NCT IDs via the HC platform API."""

from __future__ import annotations

from hc_http.hc_request import hc_request_json
from model.ctg.ctg_by_nctid_row import CtgByNctidRow
from model.fda_scrape_versions import DEFAULT_SCRAPE_VERSION
from model.parse_model_list import parse_model_list

DEFAULT_CACHE_KEY = "2026-03-02"


def run_get_ctg_by_nctids(
    nctids: list[str],
    *,
    version: str = DEFAULT_SCRAPE_VERSION,
    cache_key: str = DEFAULT_CACHE_KEY,
) -> list[CtgByNctidRow]:
    """GET /ctg/get_by_nctids and return clinical trial rows."""
    data = hc_request_json(
        "GET",
        "/ctg/get_by_nctids",
        params={"id": nctids, "version": version, "cache_key": cache_key},
    )
    return parse_model_list(CtgByNctidRow, data)
