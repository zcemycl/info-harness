"""UTC timestamps for chat records."""

from __future__ import annotations

from datetime import UTC, datetime


def utc_now() -> str:
    """Return an ISO-8601 UTC timestamp."""
    return datetime.now(UTC).isoformat()
