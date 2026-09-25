"""Bind the signed-in Cognito user for chat storage keys."""

from __future__ import annotations

from collections.abc import Iterator
from contextlib import contextmanager
from contextvars import ContextVar

_owner: ContextVar[str | None] = ContextVar("chat_owner_sub", default=None)


def current_chat_owner() -> str:
    """Return the Cognito ``sub`` for this request or chat run."""
    owner = _owner.get()
    if not owner:
        raise RuntimeError("chat owner is not bound")
    return owner


@contextmanager
def bind_chat_owner(owner_sub: str) -> Iterator[None]:
    """Scope chat reads and writes to ``owner_sub`` until the block exits."""
    sub = owner_sub.strip()
    if not sub or "/" in sub or ".." in sub:
        raise ValueError(f"unsafe chat owner: {owner_sub}")
    marker = _owner.set(sub)
    try:
        yield
    finally:
        _owner.reset(marker)
