"""LangChain tools for the CTG resolve_trial worker."""

from __future__ import annotations

from langchain_core.tools import StructuredTool

from agents.dump_tool_result import dump_tool_result
from tools.ctg.resolve_trial_mention import resolve_trial_mention


def resolve_trial_worker_tools() -> list[StructuredTool]:
    """Build the single resolve_trial_mention tool."""
    return [
        StructuredTool.from_function(
            name="resolve_trial_mention",
            description=(
                "Resolve a study name, acronym, or sponsor protocol id to an "
                "NCT via CT.gov + PubMed. Returns resolved/unresolved status, "
                "nctid when found, sources tried, and pmids. Never invents NCTs."
            ),
            func=_resolve,
        )
    ]


def _resolve(query: str, page_size: int = 10) -> str:
    result = resolve_trial_mention(query, page_size=page_size)
    return dump_tool_result(result)
