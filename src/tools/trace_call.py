"""Indented loguru tracing for agent / worker / tool / loop calls."""

from __future__ import annotations

from collections.abc import Iterator
from contextlib import contextmanager
from contextvars import ContextVar
from typing import Any

from loguru import logger

_depth: ContextVar[int] = ContextVar("trace_call_depth", default=0)


def trace_info(message: str, **fields: Any) -> None:
    """Log one line at the current nest depth."""
    logger.info(_format(message, fields))


@contextmanager
def trace_span(kind: str, name: str, **fields: Any) -> Iterator[None]:
    """Enter/leave a nested call; children indent two spaces further."""
    depth = _depth.get()
    trace_info(f"→ {kind} {name}", **fields)
    token = _depth.set(depth + 1)
    try:
        yield
    except Exception as exc:
        logger.opt(exception=False).error(
            _format(f"✗ {kind} {name}", {"error": f"{type(exc).__name__}: {exc}"})
        )
        raise
    finally:
        _depth.reset(token)
        # Leave line at the same depth as the enter line.
        logger.info(_format(f"← {kind} {name}", {}))


def _format(message: str, fields: dict[str, Any]) -> str:
    indent = "  " * _depth.get()
    extras = " ".join(
        f"{key}={value!r}" for key, value in fields.items() if value is not None
    )
    if extras:
        return f"{indent}{message}  {extras}"
    return f"{indent}{message}"
