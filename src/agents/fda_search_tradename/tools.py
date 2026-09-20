"""LangChain tools for the tradename search worker (all FdaLabel attrs)."""

from __future__ import annotations

from langchain_core.tools import StructuredTool

from agents.dump_tool_result import dump_tool_result
from model.fda.fda_attr_name import FdaAttrName
from tools.fda.search_fdalabel_tradename.attr_registry import TRADENAME_ATTR_SEARCH


def tradename_worker_tools() -> list[StructuredTool]:
    """Build one langchain tool per FdaLabel attribute."""
    tools: list[StructuredTool] = []
    for attr, search in TRADENAME_ATTR_SEARCH.items():
        tools.append(_tool_for(attr, search))
    return tools


def _tool_for(attr: FdaAttrName, search: object) -> StructuredTool:
    name = f"search_fdalabel_tradename_{attr.value}"

    def _call(tradename: str, offset: int = 0, limit: int = 5, maxn: int = 30) -> str:
        page = search(  # type: ignore[operator]
            tradename, offset=offset, limit=limit, maxn=maxn
        )
        return dump_tool_result(page)

    _call.__name__ = name
    _call.__doc__ = (
        f"Search FDA labels by tradename; returns id, setid, tradename, "
        f"{attr.value}, plus offset/limit/next_offset pagination."
    )
    return StructuredTool.from_function(
        name=name,
        description=_call.__doc__,
        func=_call,
    )
