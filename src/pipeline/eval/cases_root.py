"""Resolve paths under src/examples/eval/."""

from __future__ import annotations

from pathlib import Path

_EVAL_ROOT = Path(__file__).resolve().parents[2] / "examples" / "eval"


def eval_cases_root() -> Path:
    """Return ``src/examples/eval`` (created on demand by callers)."""
    return _EVAL_ROOT
