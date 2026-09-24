"""Shared LangChain tool: extract NCT ids / CTG URLs from clinical_trials text."""

from __future__ import annotations

from langchain_core.tools import StructuredTool

from agents.dump_tool_result import dump_tool_result
from tools.fda.extract_ctg_nct_links import extract_ctg_nct_links


def extract_ctg_nct_links_tool() -> StructuredTool:
    """Build the extract_ctg_nct_links tool for FDA search workers."""

    def _call(text: str) -> str:
        return dump_tool_result(extract_ctg_nct_links(text))

    _call.__name__ = "extract_ctg_nct_links"
    _call.__doc__ = (
        "Extract NCT######## ids and ClinicalTrials.gov study URLs from text. "
        "Pass clinical_trials section content (or any blob that may contain "
        "NCT ids). Returns nctid + ctg_url found in the text only — never "
        "invents placeholders like NCT01234567."
    )
    return StructuredTool.from_function(
        name="extract_ctg_nct_links",
        description=_call.__doc__,
        func=_call,
    )
