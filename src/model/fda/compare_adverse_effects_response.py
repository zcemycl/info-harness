"""Adverse-effects compare matrix response."""

from __future__ import annotations

from typing import Any

from pydantic import RootModel


class CompareAdverseEffectsResponse(RootModel[dict[str, list[list[Any]]]]):
    """AE compare matrices keyed by table type (heads, N totals, AE rows, …)."""
