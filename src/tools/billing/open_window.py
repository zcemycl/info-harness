"""Monthly window anchored to the user's first seen date."""

from __future__ import annotations

import calendar
from datetime import date


def open_window(anchor: date, today: date) -> tuple[date, date]:
    """Return the window start and end that contains ``today``."""
    start = anchor
    while True:
        nxt = _add_month(anchor.day, start)
        if nxt > today:
            return start, nxt
        start = nxt


def _add_month(day_of_month: int, cursor: date) -> date:
    month = cursor.month + 1
    year = cursor.year + (month - 1) // 12
    month = (month - 1) % 12 + 1
    return date(year, month, min(day_of_month, calendar.monthrange(year, month)[1]))
