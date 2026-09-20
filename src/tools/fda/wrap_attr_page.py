"""Wrap projected hits into an FdaLabelAttrPage with next_offset."""

from __future__ import annotations

from typing import TypeVar

from model.fda.fda_label_attr_page import FdaLabelAttrPage
from tools.fda.next_page_offset import next_page_offset

T = TypeVar("T")


def wrap_attr_page(items: list[T], *, offset: int, limit: int) -> FdaLabelAttrPage[T]:
    """Attach pagination metadata to a list of slim hits."""
    return FdaLabelAttrPage(
        items=items,
        offset=offset,
        limit=limit,
        next_offset=next_page_offset(offset, limit, len(items)),
    )
