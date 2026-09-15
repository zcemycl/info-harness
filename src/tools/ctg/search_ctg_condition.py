"""Tool: autocomplete CTG condition names."""

from __future__ import annotations

from hc_http.ctg.search_condition import run_search_ctg_condition


def search_ctg_condition(q: str, *, both_sides: bool = False) -> list[str]:
    """Autocomplete CTG condition names."""
    return run_search_ctg_condition(q, both_sides=both_sides)
