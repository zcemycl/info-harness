"""LangChain tools for the CTG NCT-id search worker (all study sections)."""

from __future__ import annotations

from langchain_core.tools import StructuredTool

from agents.dump_tool_result import dump_tool_result
from model.ctg.ctg_attr_name import CtgAttrName
from tools.ctg.search_ctg_nctid.attr_registry import NCTID_ATTR_SEARCH


def nctid_worker_tools() -> list[StructuredTool]:
    """Build one langchain tool per CtgByNctidRow section."""
    tools: list[StructuredTool] = []
    for attr, search in NCTID_ATTR_SEARCH.items():
        tools.append(_tool_for(attr, search))
    return tools


def _tool_for(attr: CtgAttrName, search: object) -> StructuredTool:
    name = f"search_ctg_nctid_{attr.value}"

    def _call(nctid: str, offset: int = 0, limit: int = 5) -> str:
        page = search(nctid, offset=offset, limit=limit)  # type: ignore[operator]
        return dump_tool_result(page)

    _call.__name__ = name
    _call.__doc__ = (
        f"Search CTG studies by NCT id; returns id, setid, nctid, "
        f"{attr.value}, plus offset/limit/next_offset pagination."
    )
    return StructuredTool.from_function(
        name=name,
        description=_call.__doc__,
        func=_call,
    )
