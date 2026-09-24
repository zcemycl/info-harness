"""Load a prompt markdown file from src/prompt/."""

from __future__ import annotations

from pathlib import Path

_PROMPT_ROOT = Path(__file__).resolve().parents[1] / "prompt"


def load_prompt(*parts: str) -> str:
    """Read ``src/prompt/<parts...>`` as UTF-8 text."""
    path = _PROMPT_ROOT.joinpath(*parts)
    return path.read_text(encoding="utf-8")
