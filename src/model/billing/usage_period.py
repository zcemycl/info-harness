"""One free-plan usage window."""

from __future__ import annotations

from datetime import date

from pydantic import BaseModel


class UsagePeriod(BaseModel):
    """Window start, end, and the DynamoDB range key."""

    start: date
    end: date
    key: str
