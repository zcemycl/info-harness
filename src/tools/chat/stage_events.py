"""Optional listener for diary stage writes during a chat run."""

from __future__ import annotations

from collections.abc import Callable, Iterator
from contextlib import contextmanager
from contextvars import ContextVar

from loguru import logger

from model.research.agent_answer import AgentAnswer

_listener: ContextVar[Callable[[AgentAnswer], None] | None] = ContextVar(
    "chat_stage_listener",
    default=None,
)


def notify_stage(entry: AgentAnswer) -> None:
    """Forward a persisted stage answer. No listener means CLI no-op."""
    callback = _listener.get()
    if callback is None:
        return
    try:
        callback(entry)
    except Exception:
        logger.exception("stage event listener failed")


@contextmanager
def bind_stage_events(
    callback: Callable[[AgentAnswer], None],
) -> Iterator[None]:
    """Bind ``callback`` for nested specialist threads in this context."""
    token = _listener.set(callback)
    try:
        yield
    finally:
        _listener.reset(token)
