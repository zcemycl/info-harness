"""Tool loop that may read diary files, then emits a schema."""

from __future__ import annotations

import json
from typing import Any, TypeVar

from langchain_core.messages import AIMessage, HumanMessage, SystemMessage, ToolMessage
from pydantic import BaseModel, ValidationError

from agents.shared.read_evidence_artifact_tool import read_evidence_artifact_tool

T = TypeVar("T", bound=BaseModel)

_HINT = (
    "If total_chars is larger than the summary, or a path / artifact_path is "
    "present, call read_evidence_artifact before you decide. Continue with "
    "next_offset until the window is enough. Then reply with only a JSON "
    "object for your schema. Do not paste the full prior text into that JSON."
)


def invoke_schema_with_reader(
    llm: Any,
    schema: type[T],
    *,
    system: str,
    user: str,
    max_turns: int = 4,
) -> T:
    """Let the model read diary paths, then parse ``schema`` from the last text."""
    tool = read_evidence_artifact_tool()
    bound = llm.bind_tools([tool])
    messages: list[Any] = [
        SystemMessage(content=f"{system}\n\n{_HINT}"),
        HumanMessage(content=user),
    ]
    for _turn in range(max_turns):
        response = bound.invoke(messages)
        messages.append(response)
        if not isinstance(response, AIMessage) or not response.tool_calls:
            parsed = _parse(schema, response)
            if parsed is not None:
                return parsed
            messages.append(
                HumanMessage(content="Reply with only the JSON object. No preamble.")
            )
            continue
        for call in response.tool_calls:
            result = tool.invoke(call["args"])
            messages.append(ToolMessage(content=str(result), tool_call_id=call["id"]))
    fallback = llm.with_structured_output(schema)
    result = fallback.invoke(messages)
    if isinstance(result, schema):
        return result
    return schema.model_validate(result)


def _parse(schema: type[T], response: object) -> T | None:
    text = getattr(response, "content", "")
    raw = text if isinstance(text, str) else str(text)
    start = raw.find("{")
    end = raw.rfind("}")
    if start < 0 or end <= start:
        return None
    try:
        data: Any = json.loads(raw[start : end + 1])
    except json.JSONDecodeError:
        return None
    try:
        return schema.model_validate(data)
    except ValidationError:
        return None
