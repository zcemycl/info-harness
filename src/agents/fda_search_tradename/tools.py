"""LangChain tools for the tradename search worker."""

from __future__ import annotations

from langchain_core.tools import StructuredTool

from agents.dump_tool_result import dump_tool_result
from tools.fda.search_fdalabel_tradename.adverse_effects import (
    search_fdalabel_tradename_adverse_effects,
)
from tools.fda.search_fdalabel_tradename.indication import (
    search_fdalabel_tradename_indication,
)


def tradename_worker_tools() -> list[StructuredTool]:
    """Build langchain tools bound to tradename attr search functions."""
    return [
        StructuredTool.from_function(
            name="search_fdalabel_tradename_indication",
            description=(
                "Search FDA labels by tradename; returns id, setid, tradename, "
                "indication, plus offset/limit/next_offset pagination."
            ),
            func=_indication,
        ),
        StructuredTool.from_function(
            name="search_fdalabel_tradename_adverse_effects",
            description=(
                "Search FDA labels by tradename; returns id, setid, tradename, "
                "adverse_effects, plus offset/limit/next_offset pagination."
            ),
            func=_adverse_effects,
        ),
    ]


def _indication(tradename: str, offset: int = 0, limit: int = 5, maxn: int = 30) -> str:
    page = search_fdalabel_tradename_indication(
        tradename, offset=offset, limit=limit, maxn=maxn
    )
    return dump_tool_result(page)


def _adverse_effects(
    tradename: str, offset: int = 0, limit: int = 5, maxn: int = 30
) -> str:
    page = search_fdalabel_tradename_adverse_effects(
        tradename, offset=offset, limit=limit, maxn=maxn
    )
    return dump_tool_result(page)
