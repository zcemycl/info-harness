"""Wrap projected CTG hits into a CtgAttrPage with next_offset."""

from __future__ import annotations

from typing import TypeVar

from model.ctg.ctg_attr_page import CtgAttrPage
from tools.ctg.next_page_offset import next_page_offset

T = TypeVar("T")


def wrap_attr_page(items: list[T], *, offset: int, limit: int) -> CtgAttrPage[T]:
    """Attach pagination metadata to a list of slim hits."""
    return CtgAttrPage(
        items=items,
        offset=offset,
        limit=limit,
        next_offset=next_page_offset(offset, limit, len(items)),
    )
