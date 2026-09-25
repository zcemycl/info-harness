"""Resolve the on-disk root for research diaries."""

from __future__ import annotations

import os
from pathlib import Path

DEFAULT_DIARY_DIR = Path("data/diary")


def diary_root(diary_dir: Path | None = None) -> Path:
    """Resolved diary directory for this call.

    An explicit ``diary_dir`` wins. Otherwise ``DIARY_DIR``, then ``/tmp/diary``
    on Lambda, then ``data/diary``. Lambda ``/tmp`` disappears with the environment.
    """
    chosen = diary_dir if diary_dir is not None else _default_dir()
    return chosen.expanduser().resolve()


def _default_dir() -> Path:
    configured = os.getenv("DIARY_DIR", "").strip()
    if configured:
        return Path(configured)
    if os.getenv("AWS_LAMBDA_FUNCTION_NAME", "").strip():
        return Path("/tmp/diary")
    return DEFAULT_DIARY_DIR
