"""Thread-local Cognito access token for HC calls during a chat run."""

from __future__ import annotations

from collections.abc import Iterator
from contextlib import contextmanager
from contextvars import ContextVar

_token: ContextVar[str | None] = ContextVar("hc_access_token", default=None)


def current_access_token() -> str | None:
    """Return the token bound for this run, if any."""
    return _token.get()


@contextmanager
def bind_access_token(token: str) -> Iterator[None]:
    """Use ``token`` for HC calls until the block exits."""
    marker = _token.set(token)
    try:
        yield
    finally:
        _token.reset(marker)
