"""Tool: compare FDA adverse-effects tables across setids."""

from __future__ import annotations

from typing import Any

from hc_http.fda.compare_adverse_effects import run_compare_fdalabel_adverse_effects
from model.fda_scrape_versions import FdaScrapeVersions


def compare_fdalabel_adverse_effects(
    setids: list[str],
    *,
    versions: FdaScrapeVersions | None = None,
) -> dict[str, Any]:
    """Compare adverse-effects matrices for the given setids."""
    return run_compare_fdalabel_adverse_effects(setids, versions=versions)
