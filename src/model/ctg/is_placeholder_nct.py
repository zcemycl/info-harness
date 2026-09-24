"""Detect demo / placeholder ClinicalTrials.gov NCT ids."""

from __future__ import annotations

import re

_NCT_RE = re.compile(r"^NCT[-\s]?(\d{8})$", re.IGNORECASE)

# Explicit demos + ascending / repeating patterns models invent.
_FORBIDDEN_DIGITS = frozenset(
    {
        "00000000",
        "00000001",
        "00123456",
        "00123457",
        "00123458",
        "00123459",
        "01234567",
        "01234568",
        "01234569",
        "11111111",
        "12345678",
        "12345679",
    }
)


def nct_digits(value: str) -> str | None:
    """Return 8 NCT digits if ``value`` looks like NCT########, else None."""
    match = _NCT_RE.fullmatch(value.strip())
    return match.group(1) if match else None


def is_placeholder_nct(value: str) -> bool:
    """True for invented demo NCTs (sequential / repeating / known fakes)."""
    digits = nct_digits(value)
    if digits is None:
        return False
    if digits in _FORBIDDEN_DIGITS:
        return True
    if len(set(digits)) == 1:
        return True
    if digits.startswith("0012345") or digits.startswith("012345"):
        return True
    return False
