"""Tool: fetch CTG studies by NCT IDs."""

from __future__ import annotations

from hc_http.ctg.get_by_nctids import DEFAULT_CACHE_KEY, run_get_ctg_by_nctids
from model.ctg.ctg_by_nctid_row import CtgByNctidRow
from model.fda_scrape_versions import DEFAULT_SCRAPE_VERSION


def get_ctg_by_nctids(
    nctids: list[str],
    *,
    version: str = DEFAULT_SCRAPE_VERSION,
    cache_key: str = DEFAULT_CACHE_KEY,
) -> list[CtgByNctidRow]:
    """Fetch clinical trials by NCT ID list."""
    return run_get_ctg_by_nctids(nctids, version=version, cache_key=cache_key)
