"""Extract Table N + tableplaceholder refs from FDA section prose."""

from __future__ import annotations

import re

from model.fda.fda_table_placeholder_ref import FdaTablePlaceholderRef

_PLACEHOLDER_RE = re.compile(r"<tableplaceholder\s*/>-(\d+)", re.IGNORECASE)
_TABLE_NUM_RE = re.compile(r"Table\s+(\d+)\b", re.IGNORECASE)


def extract_table_placeholders(text: str) -> list[FdaTablePlaceholderRef]:
    """Parse ``<tableplaceholder/>-i`` markers and nearby ``Table N`` labels."""
    if not text:
        return []
    refs: list[FdaTablePlaceholderRef] = []
    seen: set[int] = set()
    for match in _PLACEHOLDER_RE.finditer(text):
        index = int(match.group(1))
        if index in seen:
            continue
        seen.add(index)
        start = max(0, match.start() - 200)
        window = text[start : match.start()]
        nums = _TABLE_NUM_RE.findall(window)
        table_number = int(nums[-1]) if nums else None
        snippet = " ".join(window.split())[-120:]
        refs.append(
            FdaTablePlaceholderRef(
                placeholder_index=index,
                table_number=table_number,
                context_snippet=snippet,
            )
        )
    return refs
