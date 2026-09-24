"""LangChain tools for the CTG condition autocomplete worker."""

from __future__ import annotations

from langchain_core.tools import StructuredTool

from agents.dump_tool_result import dump_tool_result
from tools.ctg.search_ctg_condition import search_ctg_condition


def condition_worker_tools() -> list[StructuredTool]:
    """Build the single search_ctg_condition tool."""
    return [
        StructuredTool.from_function(
            name="search_ctg_condition",
            description=(
                "Autocomplete CTG condition names. "
                "both_sides=false (default): SQL LIKE q% (prefix only). "
                "both_sides=true: SQL LIKE %q% (substring on either side). "
                "Returns a JSON list of matching condition name strings."
            ),
            func=_search,
        )
    ]


def _search(q: str, both_sides: bool = False) -> str:
    names = search_ctg_condition(q, both_sides=both_sides)
    return dump_tool_result(names)
