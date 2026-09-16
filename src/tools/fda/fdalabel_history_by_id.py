"""Tool: fetch FDA label history by setid."""

from __future__ import annotations

from hc_http.fda.history_by_id import run_fdalabel_history_by_id
from model.fda.fda_label_history import FdaLabelHistory
from model.fda_scrape_versions import FdaScrapeVersions


def fdalabel_history_by_id(
    setid: str,
    *,
    versions: FdaScrapeVersions | None = None,
) -> FdaLabelHistory:
    """Fetch FDA label history for a setid."""
    return run_fdalabel_history_by_id(setid, versions=versions)
