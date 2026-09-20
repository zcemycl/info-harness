"""Paginated wrapper for slim FDA label attribute hits."""

from __future__ import annotations

from typing import Generic, TypeVar

from pydantic import BaseModel, Field

T = TypeVar("T")


class FdaLabelAttrPage(BaseModel, Generic[T]):
    """One page of slim attribute hits with next-offset hint."""

    items: list[T] = Field(description="Hits for this page")
    offset: int = Field(ge=0, description="Request offset")
    limit: int = Field(ge=1, description="Request page size")
    next_offset: int | None = Field(
        default=None,
        description="Pass as offset to fetch the next page; null when done",
    )
