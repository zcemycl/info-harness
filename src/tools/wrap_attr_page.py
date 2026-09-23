"""Wrap projected hits into an AttrPage with next_offset."""

from __future__ import annotations

from typing import TypeVar

from model.attr_page import AttrPage
from tools.next_page_offset import next_page_offset

T = TypeVar("T")


def wrap_attr_page(items: list[T], *, offset: int, limit: int) -> AttrPage[T]:
    """Attach pagination metadata to a list of slim hits."""
    return AttrPage(
        items=items,
        offset=offset,
        limit=limit,
        next_offset=next_page_offset(offset, limit, len(items)),
    )
