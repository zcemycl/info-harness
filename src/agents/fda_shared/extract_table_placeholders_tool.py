"""Shared LangChain tool: extract table placeholders from FDA section text."""

from __future__ import annotations

from langchain_core.tools import StructuredTool

from agents.dump_tool_result import dump_tool_result
from tools.fda.extract_table_placeholders import extract_table_placeholders


def extract_table_placeholders_tool() -> StructuredTool:
    """Build the extract_table_placeholders tool for FDA search workers."""

    def _call(text: str) -> str:
        return dump_tool_result(extract_table_placeholders(text))

    _call.__name__ = "extract_table_placeholders"
    _call.__doc__ = (
        "Extract <tableplaceholder/>-N markers and nearby Table N labels "
        "from adverse_effects or clinical_trials section content. Use the "
        "Table N values to fetch the paired adverse_effect_tables or "
        "clinical_trial_tables for the same setid and match by caption."
    )
    return StructuredTool.from_function(
        name="extract_table_placeholders",
        description=_call.__doc__,
        func=_call,
    )
