"""Tool: autocomplete FDA tradenames."""

from __future__ import annotations

from hc_http.fda._cache_key import DEFAULT_CACHE_KEY
from hc_http.fda.search_tradename import run_autocomplete_fdalabel_tradename
from model.fda_scrape_versions import FdaScrapeVersions


def autocomplete_fdalabel_tradename(
    tradename: str,
    *,
    versions: FdaScrapeVersions | None = None,
    cache_key: str = DEFAULT_CACHE_KEY,
) -> list[str]:
    """Autocomplete FDA tradenames."""
    return run_autocomplete_fdalabel_tradename(
        tradename, versions=versions, cache_key=cache_key
    )
