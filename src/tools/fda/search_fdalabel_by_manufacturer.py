"""Tool: fetch FDA labels for an exact manufacturer."""

from __future__ import annotations

from hc_http.fda.search_by_manufacturer import run_search_fdalabel_by_manufacturer
from model.fda.manufacturer import Manufacturer
from model.fda_scrape_versions import FdaScrapeVersions


def search_fdalabel_by_manufacturer(
    manufacturer: str,
    *,
    versions: FdaScrapeVersions | None = None,
) -> Manufacturer:
    """Fetch FDA labels for an exact manufacturer name."""
    return run_search_fdalabel_by_manufacturer(manufacturer, versions=versions)
