"""LangChain tools for the PubMed PMID id-sections worker."""

from __future__ import annotations

from langchain_core.tools import StructuredTool

from agents.dump_tool_result import dump_tool_result
from model.pubmed.pubmed_attr_name import PubmedAttrName
from tools.pubmed.id_sections.attr_registry import ID_ATTR_SECTIONS


def id_sections_worker_tools() -> list[StructuredTool]:
    """Build one langchain tool per MEDLINE section."""
    tools: list[StructuredTool] = []
    for attr, fetch in ID_ATTR_SECTIONS.items():
        tools.append(_tool_for(attr, fetch))
    return tools


def _tool_for(attr: PubmedAttrName, fetch: object) -> StructuredTool:
    name = f"pubmed_id_{attr.value}"

    def _call(pmid: str, offset: int = 0, limit: int = 20) -> str:
        page = fetch(pmid, offset=offset, limit=limit)  # type: ignore[operator]
        return dump_tool_result(page)

    _call.__name__ = name
    _call.__doc__ = (
        f"Fetch PubMed MEDLINE by PMID; returns pmid, {attr.value}, "
        f"plus offset/limit/next_offset pagination over split units."
    )
    return StructuredTool.from_function(
        name=name,
        description=_call.__doc__,
        func=_call,
    )
