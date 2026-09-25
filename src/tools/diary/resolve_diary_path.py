"""Resolve a diary file path that must stay under ``diary_dir``."""

from __future__ import annotations

from pathlib import Path

from tools.diary.default_diary_dir import diary_root


def resolve_diary_path(
    path: str,
    *,
    diary_dir: Path | None = None,
) -> Path:
    """Resolve ``path`` to an existing diary file under ``diary_dir``."""
    if not path.strip():
        raise ValueError("path must be non-empty")

    root = diary_root(diary_dir)
    raw = Path(path).expanduser()
    if raw.is_absolute():
        return _existing(_contained(raw.resolve(), root, path), path)

    anchored = _contained((root / raw).resolve(), root, path)
    for candidate in (
        anchored,
        (root / raw.name).resolve(),
        (Path.cwd() / raw).resolve(),
    ):
        if _inside(candidate, root) and candidate.is_file():
            return candidate
    raise FileNotFoundError(f"Diary file not found: {path}")


def _contained(resolved: Path, root: Path, path: str) -> Path:
    if not _inside(resolved, root):
        raise ValueError(f"path escapes diary_dir: {path!r}")
    return resolved


def _existing(resolved: Path, path: str) -> Path:
    if not resolved.is_file():
        raise FileNotFoundError(f"Diary file not found: {path}")
    return resolved


def _inside(resolved: Path, root: Path) -> bool:
    return resolved.is_relative_to(root)
