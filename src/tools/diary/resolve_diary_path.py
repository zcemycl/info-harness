"""Resolve a diary file path that must stay under ``diary_dir``."""

from __future__ import annotations

from pathlib import Path

from tools.diary.default_diary_dir import DEFAULT_DIARY_DIR


def resolve_diary_path(
    path: str,
    *,
    diary_dir: Path = DEFAULT_DIARY_DIR,
) -> Path:
    """Resolve ``path`` to an existing diary file under ``diary_dir``."""
    if not path.strip():
        raise ValueError("path must be non-empty")

    root = diary_dir.expanduser().resolve()
    raw = Path(path).expanduser()
    candidates: list[Path] = []
    if raw.is_absolute():
        candidates.append(raw.resolve())
    else:
        candidates.append((Path.cwd() / raw).resolve())
        candidates.append((root / raw).resolve())
        candidates.append((root / raw.name).resolve())

    for resolved in candidates:
        if resolved.is_relative_to(root) and resolved.is_file():
            return resolved

    if any(not candidate.is_relative_to(root) for candidate in candidates):
        raise ValueError(f"path escapes diary_dir: {path!r}")
    raise FileNotFoundError(f"Diary file not found: {path}")
