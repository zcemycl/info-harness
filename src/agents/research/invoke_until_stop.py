"""Keep calling the chat model until it stops or the continuation budget ends."""

from __future__ import annotations

from typing import Any

from openai import LengthFinishReasonError

_MAX_EXTRA_CALLS = 3
_CONTINUE = (
    "Continue from the exact cutoff. Do not repeat text already written. "
    "Do not add a preface."
)


def invoke_until_stop(llm: Any, messages: list[dict[str, str]]) -> str:
    """Return the full text, requesting more when the model stops for length."""
    thread = list(messages)
    parts: list[str] = []
    for turn in range(_MAX_EXTRA_CALLS + 1):
        try:
            response = llm.invoke(thread)
        except LengthFinishReasonError as exc:
            partial = _partial_text(exc)
            if partial:
                parts.append(partial)
            break
        text = _content(response)
        parts.append(text)
        if not _hit_length(response) or turn == _MAX_EXTRA_CALLS:
            break
        thread.extend(
            [
                {"role": "assistant", "content": text},
                {"role": "user", "content": _CONTINUE},
            ]
        )
    return "".join(parts)


def _hit_length(response: object) -> bool:
    meta = getattr(response, "response_metadata", None)
    if not isinstance(meta, dict):
        return False
    return meta.get("finish_reason") == "length"


def _content(response: object) -> str:
    content = getattr(response, "content", "")
    return content if isinstance(content, str) else str(content)


def _partial_text(exc: LengthFinishReasonError) -> str:
    try:
        content = exc.completion.choices[0].message.content
    except (AttributeError, IndexError):
        return ""
    return content or ""
