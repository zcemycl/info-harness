"""LangChain tool: read a diary evidence artifact in char windows."""

from __future__ import annotations

from langchain_core.tools import StructuredTool

from agents.dump_tool_result import dump_tool_result
from tools.diary.read_evidence_artifact import read_evidence_artifact


def read_evidence_artifact_tool() -> StructuredTool:
    """Build the read_evidence_artifact tool for specialist workers."""

    def _call(
        path: str,
        offset: int = 0,
        limit_chars: int = 4000,
    ) -> str:
        return dump_tool_result(
            read_evidence_artifact(path, offset=offset, limit_chars=limit_chars)
        )

    _call.__name__ = "read_evidence_artifact"
    _call.__doc__ = (
        "Read a diary evidence artifact by path (from evidence note "
        "artifact_path). Optional offset/limit_chars for chunked reads "
        "(default limit 4000). Use when a capped summary is not enough."
    )
    return StructuredTool.from_function(
        name="read_evidence_artifact",
        description=_call.__doc__,
        func=_call,
    )
