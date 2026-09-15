"""Tool: autocomplete therapeutic area names."""

from __future__ import annotations

from hc_http.therapeutic_area.search_therapeutic_area import (
    run_search_therapeutic_area,
)


def search_therapeutic_area(q: str, *, both_sides: bool = False) -> list[str]:
    """Autocomplete therapeutic area names."""
    return run_search_therapeutic_area(q, both_sides=both_sides)
