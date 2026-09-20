"""LangChain tools for the indication search worker."""

from __future__ import annotations

from langchain_core.tools import StructuredTool

from agents.dump_tool_result import dump_tool_result
from tools.fda.search_fdalabel_indication.adverse_effects import (
    search_fdalabel_indication_adverse_effects,
)
from tools.fda.search_fdalabel_indication.indication import (
    search_fdalabel_indication_indication,
)


def indication_worker_tools() -> list[StructuredTool]:
    """Build langchain tools bound to indication attr search functions."""
    return [
        StructuredTool.from_function(
            name="search_fdalabel_indication_indication",
            description=(
                "Search FDA labels by indication text; returns id, setid, "
                "tradename, indication, plus offset/limit/next_offset."
            ),
            func=_indication,
        ),
        StructuredTool.from_function(
            name="search_fdalabel_indication_adverse_effects",
            description=(
                "Search FDA labels by indication text; returns id, setid, "
                "tradename, adverse_effects, plus offset/limit/next_offset."
            ),
            func=_adverse_effects,
        ),
    ]


def _indication(
    indication: str, offset: int = 0, limit: int = 5, maxn: int = 30
) -> str:
    page = search_fdalabel_indication_indication(
        indication, offset=offset, limit=limit, maxn=maxn
    )
    return dump_tool_result(page)


def _adverse_effects(
    indication: str, offset: int = 0, limit: int = 5, maxn: int = 30
) -> str:
    page = search_fdalabel_indication_adverse_effects(
        indication, offset=offset, limit=limit, maxn=maxn
    )
    return dump_tool_result(page)
