"""Tool: list FDA section scrape versions for a parent version."""

from __future__ import annotations

from typing import Any

from hc_http.fda.get_section_scrape_version import (
    run_get_fdalabel_section_scrape_versions,
)
from model.fda_scrape_versions import DEFAULT_SCRAPE_VERSION


def get_fdalabel_section_scrape_versions(
    version: str = DEFAULT_SCRAPE_VERSION,
) -> dict[str, Any]:
    """List section scrape versions for a parent FDA scrape version."""
    return run_get_fdalabel_section_scrape_versions(version)
