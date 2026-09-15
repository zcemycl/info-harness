"""Tool: list FDA scrape versions."""

from __future__ import annotations

from hc_http.fda.get_scrape_version import run_get_fdalabel_scrape_versions


def get_fdalabel_scrape_versions() -> list[str]:
    """List available FDA scrape versions."""
    return run_get_fdalabel_scrape_versions()
