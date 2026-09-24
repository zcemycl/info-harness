"""Shared FDA label table section (hc-backend BaseSectionTable)."""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class FdaLabelTableContent(BaseModel):
    """Parsed table payload nested under AE/CT table sections."""

    model_config = ConfigDict(extra="allow")

    table: list[list[str]] | None = Field(
        default=None, description="2D string grid of table cells"
    )
    fifo: dict[int, list[str]] | None = Field(
        default=None, description="FIFO leftover column map when present"
    )
    isEmptyFifo: bool | None = Field(
        default=None, description="Whether FIFO leftovers are empty"
    )
    isTransposeable: bool | None = Field(
        default=None, description="Whether the table can be transposed"
    )
    max_leftover_nrows: int | None = Field(
        default=None, description="Max leftover rows after FIFO handling"
    )


class FdaLabelTable(BaseModel):
    """Adverse-effect or clinical-trial table section."""

    model_config = ConfigDict(extra="allow")

    id: int = Field(description="Table section row id")
    content: FdaLabelTableContent | None = Field(
        default=None, description="Parsed table content payload"
    )
    version: str = Field(description="Table scrape/cache version pin")
    caption: str = Field(description="Table caption text")
    # Keep room for annotation extras from API without failing validation.
    annotation: Any | None = Field(
        default=None, description="Optional annotation payload if present"
    )
