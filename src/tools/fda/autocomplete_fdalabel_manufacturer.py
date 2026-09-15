"""Tool: autocomplete FDA manufacturers."""

from __future__ import annotations

from hc_http.fda._cache_key import DEFAULT_CACHE_KEY
from hc_http.fda.search_manufacturer import run_autocomplete_fdalabel_manufacturer
from model.fda_scrape_versions import FdaScrapeVersions


def autocomplete_fdalabel_manufacturer(
    manufacturer: str,
    *,
    versions: FdaScrapeVersions | None = None,
    cache_key: str = DEFAULT_CACHE_KEY,
) -> list[str]:
    """Autocomplete FDA manufacturer names."""
    return run_autocomplete_fdalabel_manufacturer(
        manufacturer, versions=versions, cache_key=cache_key
    )
