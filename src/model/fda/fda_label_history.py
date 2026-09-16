"""FDA label history payload for a setid."""

from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field, field_validator


def _split_or_list(value: Any) -> list[str]:
    if value is None:
        return []
    if isinstance(value, list):
        return [str(item) for item in value]
    if isinstance(value, str):
        return value.split("<*>") if value else []
    raise TypeError(f"Expected str or list, got {type(value).__name__}")


def _split_timestamps(value: Any) -> list[datetime]:
    if value is None:
        return []
    if isinstance(value, list):
        out: list[datetime] = []
        for item in value:
            if isinstance(item, datetime):
                out.append(item)
            else:
                out.append(datetime.fromtimestamp(int(item)))
        return out
    if isinstance(value, str):
        return [
            datetime.fromtimestamp(int(part)) for part in value.split("<*>") if part
        ]
    raise TypeError(f"Expected str or list, got {type(value).__name__}")


class FdaLabelHistory(BaseModel):
    """Historical SPL versions / manufacturers for a trade name lineage."""

    tradename: str = Field(description="Normalized trade name")
    setids: list[str] = Field(description="Historical setids for the lineage")
    manufacturers: list[str] = Field(description="Historical manufacturer names")
    spl_earliest_dates: list[datetime] = Field(
        description="Earliest SPL dates aligned with setids"
    )
    spl_effective_dates: list[datetime] = Field(
        description="Effective SPL dates aligned with setids"
    )

    @field_validator("setids", "manufacturers", mode="before")
    @classmethod
    def _coerce_string_lists(cls, value: Any) -> list[str]:
        return _split_or_list(value)

    @field_validator("spl_earliest_dates", "spl_effective_dates", mode="before")
    @classmethod
    def _coerce_dates(cls, value: Any) -> list[datetime]:
        return _split_timestamps(value)
