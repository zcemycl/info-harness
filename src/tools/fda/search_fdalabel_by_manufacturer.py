"""Tool: fetch FDA labels for an exact manufacturer."""

from __future__ import annotations

from typing import Any

from hc_http.fda.search_by_manufacturer import run_search_fdalabel_by_manufacturer
from model.fda_scrape_versions import FdaScrapeVersions


def search_fdalabel_by_manufacturer(
    manufacturer: str,
    *,
    versions: FdaScrapeVersions | None = None,
) -> dict[str, Any]:
    """Fetch FDA labels for an exact manufacturer name."""
    return run_search_fdalabel_by_manufacturer(manufacturer, versions=versions)
