"""Shared LangChain tool: extract non-NCT study mentions from label text."""

from __future__ import annotations

from langchain_core.tools import StructuredTool

from agents.dump_tool_result import dump_tool_result
from tools.fda.extract_study_mentions import extract_study_mentions


def extract_study_mentions_tool() -> StructuredTool:
    """Build the extract_study_mentions tool for FDA search workers."""

    def _call(text: str) -> str:
        return dump_tool_result(extract_study_mentions(text))

    _call.__name__ = "extract_study_mentions"
    _call.__doc__ = (
        "Extract non-NCT study mentions (sponsor protocol ids like CNA3006, "
        "acronyms like INO-VATE) from clinical_trials text. Returns raw, "
        "kind, and known aliases. Does not invent NCT ids."
    )
    return StructuredTool.from_function(
        name="extract_study_mentions",
        description=_call.__doc__,
        func=_call,
    )
