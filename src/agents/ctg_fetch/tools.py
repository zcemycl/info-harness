"""LangChain tools for the CTG live NCT-id fetch worker (all study sections)."""

from __future__ import annotations

from langchain_core.tools import StructuredTool

from agents.dump_tool_result import dump_tool_result
from agents.shared.read_evidence_artifact_tool import read_evidence_artifact_tool
from model.ctg.ctg_attr_name import CtgAttrName
from tools.ctg.fetch_ctg_nctid.attr_registry import NCTID_ATTR_FETCH


def fetch_nctid_worker_tools() -> list[StructuredTool]:
    """Build one langchain tool per live CT.gov study section."""
    tools: list[StructuredTool] = []
    for attr, fetch in NCTID_ATTR_FETCH.items():
        tools.append(_tool_for(attr, fetch))
    tools.append(read_evidence_artifact_tool())
    return tools


def _tool_for(attr: CtgAttrName, fetch: object) -> StructuredTool:
    name = f"fetch_ctg_nctid_{attr.value}"

    def _call(nctid: str, offset: int = 0, limit: int = 5) -> str:
        page = fetch(nctid, offset=offset, limit=limit)  # type: ignore[operator]
        return dump_tool_result(page)

    _call.__name__ = name
    _call.__doc__ = (
        f"Fetch live CT.gov study by NCT id; returns nctid, "
        f"{attr.value}, plus offset/limit/next_offset pagination."
    )
    return StructuredTool.from_function(
        name=name,
        description=_call.__doc__,
        func=_call,
    )
