"""Build FDA scrape-versions JSON body for HC requests."""

from __future__ import annotations

from model.fda_scrape_versions import FdaScrapeVersions


def _versions_body(
    versions: FdaScrapeVersions | None,
) -> dict[str, str | None]:
    """Return a versions map, defaulting to `FdaScrapeVersions()`."""
    return (versions or FdaScrapeVersions()).model_dump()
