"""Detect demo / placeholder PubMed PMIDs."""

from __future__ import annotations

_FORBIDDEN = frozenset(
    {
        "00000000",
        "00000001",
        "01234567",
        "01234568",
        "01234569",
        "12345678",
        "12345679",
        "23456789",
        "11111111",
        "22222222",
        "30512345",
        "31500000",
    }
)


def is_placeholder_pmid(value: str) -> bool:
    """True for invented demo PMIDs (sequential / repeating / known fakes)."""
    digits = value.strip()
    if not digits.isdigit() or not (5 <= len(digits) <= 9):
        return True
    if digits in _FORBIDDEN:
        return True
    if len(set(digits)) == 1:
        return True
    if digits.endswith("00000") or digits.endswith("0000"):
        return True
    if digits.startswith("012345") or digits.startswith("123456"):
        return True
    return False
