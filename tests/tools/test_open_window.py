"""Free-window date math."""

from __future__ import annotations

from datetime import date

from tools.billing.open_window import open_window


def test_window_steps_to_the_next_anniversary() -> None:
    start, end = open_window(date(2026, 9, 1), date(2026, 10, 2))
    assert start == date(2026, 10, 1)
    assert end == date(2026, 11, 1)
