"""LangChain tools for the ICD therapeutic-area worker."""

from __future__ import annotations

from langchain_core.tools import StructuredTool

from agents.dump_tool_result import dump_tool_result
from tools.therapeutic_area.search_therapeutic_area import search_therapeutic_area


def icd_ta_worker_tools() -> list[StructuredTool]:
    """Build the single search_therapeutic_area tool."""
    return [
        StructuredTool.from_function(
            name="search_therapeutic_area",
            description=(
                "Autocomplete ICD therapeutic area names. "
                "both_sides=false (default): SQL LIKE q% (prefix only). "
                "both_sides=true: SQL LIKE %q% (substring on either side). "
                "Returns a JSON list of matching TA name strings (no ids)."
            ),
            func=_search,
        )
    ]


def _search(q: str, both_sides: bool = False) -> str:
    names = search_therapeutic_area(q, both_sides=both_sides)
    return dump_tool_result(names)
