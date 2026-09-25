"""Writer tool loop: read specialist answer paths, then continue if cut off."""

from __future__ import annotations

from typing import Any

from langchain_core.messages import AIMessage, HumanMessage, SystemMessage, ToolMessage

from agents.research.invoke_until_stop import invoke_until_stop
from agents.shared.read_evidence_artifact_tool import read_evidence_artifact_tool

_HINT = (
    "Outcomes list answer_path and total_chars, not the full text. "
    "Call read_evidence_artifact on each path you need, using next_offset "
    "when the window is short. Then write the synthesis. Do not repeat a path "
    "you already read in full."
)
_CONTINUE = (
    "Continue from the exact cutoff. Do not repeat text already written. "
    "Do not add a preface."
)


def invoke_text_with_reader(
    llm: Any,
    *,
    system: str,
    user: str,
    max_reads: int = 6,
) -> str:
    """Read diary paths, then keep writing if the model stops for length."""
    tool = read_evidence_artifact_tool()
    bound = llm.bind_tools([tool])
    messages: list[Any] = [
        SystemMessage(content=f"{system}\n\n{_HINT}"),
        HumanMessage(content=user),
    ]
    for _turn in range(max_reads):
        response = bound.invoke(messages)
        messages.append(response)
        if not isinstance(response, AIMessage) or not response.tool_calls:
            return _finish(llm, system, user, response)
        for call in response.tool_calls:
            result = tool.invoke(call["args"])
            messages.append(ToolMessage(content=str(result), tool_call_id=call["id"]))
    return invoke_until_stop(
        llm,
        [
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ],
    )


def _finish(llm: Any, system: str, user: str, response: object) -> str:
    text = _content(response)
    if not _hit_length(response):
        return text
    more = invoke_until_stop(
        llm,
        [
            {"role": "system", "content": system},
            {"role": "user", "content": user},
            {"role": "assistant", "content": text},
            {"role": "user", "content": _CONTINUE},
        ],
    )
    return text + more


def _hit_length(response: object) -> bool:
    meta = getattr(response, "response_metadata", None)
    return isinstance(meta, dict) and meta.get("finish_reason") == "length"


def _content(response: object) -> str:
    content = getattr(response, "content", "")
    return content if isinstance(content, str) else str(content)
