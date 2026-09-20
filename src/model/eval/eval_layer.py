"""Eval layer discriminator for suite selection."""

from __future__ import annotations

from enum import StrEnum


class EvalLayer(StrEnum):
    """Which agent layer a case exercises."""

    WORKER = "worker"
    INNER = "inner"
