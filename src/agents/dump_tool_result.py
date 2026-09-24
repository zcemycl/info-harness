"""Serialize tool results to JSON capped by FDA_AGENT_TOOL_MAX_CHARS."""

from __future__ import annotations

import json
import os
from typing import Any

from pydantic import BaseModel


def dump_tool_result(value: Any) -> str:
    """JSON-serialize a tool return value and truncate for the LLM context."""
    max_chars = int(os.getenv("FDA_AGENT_TOOL_MAX_CHARS", "8000"))
    if isinstance(value, BaseModel):
        payload: Any = value.model_dump(mode="json")
    elif isinstance(value, list) and value and isinstance(value[0], BaseModel):
        payload = [item.model_dump(mode="json") for item in value]
    else:
        payload = value
    text = json.dumps(payload, indent=2, default=str)
    if len(text) <= max_chars:
        return text
    return text[: max_chars - 20] + "\n...[truncated]"
