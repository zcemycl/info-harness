"""Tool: fetch FDA label history by setid."""

from __future__ import annotations

from typing import Any

from hc_http.fda.history_by_id import run_fdalabel_history_by_id
from model.fda_scrape_versions import FdaScrapeVersions


def fdalabel_history_by_id(
    setid: str,
    *,
    versions: FdaScrapeVersions | None = None,
) -> dict[str, Any]:
    """Fetch FDA label history for a setid."""
    return run_fdalabel_history_by_id(setid, versions=versions)
