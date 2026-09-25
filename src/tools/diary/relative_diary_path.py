"""Path of a diary file relative to the diary root."""

from __future__ import annotations

from pathlib import Path


def relative_diary_path(path: Path, root: Path) -> str:
    """Return ``path`` relative to ``root`` so readers can join it later."""
    return path.resolve().relative_to(root.resolve()).as_posix()
