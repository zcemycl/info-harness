"""Tool: autocomplete FDA setids."""

from __future__ import annotations

from hc_http.fda._cache_key import DEFAULT_CACHE_KEY
from hc_http.fda.search_setid import run_autocomplete_fdalabel_setid
from model.fda_scrape_versions import FdaScrapeVersions


def autocomplete_fdalabel_setid(
    setid: str,
    *,
    versions: FdaScrapeVersions | None = None,
    cache_key: str = DEFAULT_CACHE_KEY,
) -> list[str]:
    """Autocomplete FDA setids."""
    return run_autocomplete_fdalabel_setid(
        setid, versions=versions, cache_key=cache_key
    )
