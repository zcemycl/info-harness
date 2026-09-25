"""LangChain tool: read a diary evidence artifact in char windows."""

from __future__ import annotations

import json

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
        try:
            return dump_tool_result(
                read_evidence_artifact(path, offset=offset, limit_chars=limit_chars)
            )
        except (ValueError, FileNotFoundError, OSError, json.JSONDecodeError) as exc:
            return json.dumps({"error": f"{type(exc).__name__}: {exc}"})

    _call.__name__ = "read_evidence_artifact"
    _call.__doc__ = (
        "Read a diary evidence artifact or a stage-answer JSON by path "
        "(artifact_path or AgentAnswer.path). Optional offset/limit_chars "
        "windows the text (default limit 4000). Use next_offset to continue. "
        "Call this when total_chars is larger than the summary. "
        "A missing path returns an error object; do not invent paths."
    )
    return StructuredTool.from_function(
        name="read_evidence_artifact",
        description=_call.__doc__,
        func=_call,
    )
