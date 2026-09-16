"""Resolve a diary subfolder under the diary root without path escape."""

from __future__ import annotations

from pathlib import Path


def diary_folder(root: Path, name_prefix: str | None) -> Path:
    """Return ``root`` or ``root / name_prefix``, rejecting ``..`` escapes."""
    if not name_prefix or not name_prefix.strip():
        return root
    rel = Path(name_prefix.strip())
    if rel.is_absolute() or ".." in rel.parts:
        raise ValueError(f"name_prefix must stay under diary_dir: {name_prefix!r}")
    folder = (root / rel).resolve()
    if not folder.is_relative_to(root):
        raise ValueError(f"name_prefix escapes diary_dir: {name_prefix!r}")
    return folder
