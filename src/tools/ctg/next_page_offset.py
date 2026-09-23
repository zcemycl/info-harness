"""Compute next pagination offset from a filled page."""

from __future__ import annotations


def next_page_offset(offset: int, limit: int, item_count: int) -> int | None:
    """Return the next offset when the page looks full; else None."""
    if item_count >= limit:
        return offset + item_count
    return None
