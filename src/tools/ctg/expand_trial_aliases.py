"""Expand a study mention with curated alternate spellings."""

from __future__ import annotations

import json
from functools import lru_cache
from pathlib import Path

_ALIASES_PATH = (
    Path(__file__).resolve().parents[2] / "examples" / "trial_aliases" / "aliases.json"
)


def expand_trial_aliases(query: str) -> list[str]:
    """Return query plus known aliases (original first, unique)."""
    q = query.strip()
    if not q:
        return []
    out: list[str] = [q]
    seen = {q.casefold()}
    for alt in _load_aliases().get(q.casefold(), []):
        token = alt.strip()
        key = token.casefold()
        if not token or key in seen:
            continue
        seen.add(key)
        out.append(token)
    return out


@lru_cache(maxsize=1)
def _load_aliases() -> dict[str, list[str]]:
    """Map casefolded key → list of alternate spellings."""
    if not _ALIASES_PATH.is_file():
        return {}
    data = json.loads(_ALIASES_PATH.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        return {}
    out: dict[str, list[str]] = {}
    for key, value in data.items():
        if not isinstance(key, str) or not isinstance(value, list):
            continue
        out[key.casefold()] = [str(v) for v in value if isinstance(v, str)]
    return out
