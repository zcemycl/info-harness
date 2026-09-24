"""LangChain tools for the therapeutic-area search worker (all FdaLabel attrs)."""

from __future__ import annotations

from langchain_core.tools import StructuredTool

from agents.dump_tool_result import dump_tool_result
from agents.fda_shared.extract_ctg_nct_links_tool import extract_ctg_nct_links_tool
from agents.fda_shared.extract_study_mentions_tool import extract_study_mentions_tool
from model.fda.fda_attr_name import FdaAttrName
from tools.fda.search_fdalabel_therapeutic_area.attr_registry import (
    THERAPEUTIC_AREA_ATTR_SEARCH,
)


def therapeutic_area_worker_tools() -> list[StructuredTool]:
    """Build one langchain tool per FdaLabel attribute plus NCT/mention extract."""
    tools: list[StructuredTool] = []
    for attr, search in THERAPEUTIC_AREA_ATTR_SEARCH.items():
        tools.append(_tool_for(attr, search))
    tools.append(extract_ctg_nct_links_tool())
    tools.append(extract_study_mentions_tool())
    return tools


def _tool_for(attr: FdaAttrName, search: object) -> StructuredTool:
    name = f"search_fdalabel_therapeutic_area_{attr.value}"

    def _call(
        ta_description: str,
        offset: int = 0,
        limit: int = 5,
        maxn: int = 30,
    ) -> str:
        page = search(  # type: ignore[operator]
            ta_description, offset=offset, limit=limit, maxn=maxn
        )
        return dump_tool_result(page)

    _call.__name__ = name
    _call.__doc__ = (
        f"Search FDA labels by therapeutic area; returns id, setid, tradename, "
        f"{attr.value}, plus offset/limit/next_offset pagination."
    )
    return StructuredTool.from_function(
        name=name,
        description=_call.__doc__,
        func=_call,
    )
