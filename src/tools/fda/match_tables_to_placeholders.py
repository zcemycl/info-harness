"""Match FdaLabelTable rows to placeholder Table N refs by caption."""

from __future__ import annotations

import re
from typing import Any

from model.fda.fda_label_table import FdaLabelTable
from model.fda.fda_table_placeholder_ref import FdaTablePlaceholderRef

_CAPTION_TABLE_RE = re.compile(r"^Table\s+(\d+)\b", re.IGNORECASE)


def match_tables_to_placeholders(
    refs: list[FdaTablePlaceholderRef],
    tables: list[Any],
) -> tuple[
    list[tuple[FdaTablePlaceholderRef, FdaLabelTable]],
    list[FdaTablePlaceholderRef],
]:
    """Pair refs to tables by caption ``Table N``; return matches + unmatched."""
    by_num: dict[int, FdaLabelTable] = {}
    for raw in tables:
        table = _as_table(raw)
        if table is None:
            continue
        match = _CAPTION_TABLE_RE.match(table.caption or "")
        if not match:
            continue
        num = int(match.group(1))
        by_num.setdefault(num, table)

    matched: list[tuple[FdaTablePlaceholderRef, FdaLabelTable]] = []
    unmatched: list[FdaTablePlaceholderRef] = []
    seen_nums: set[int] = set()
    for ref in refs:
        if ref.table_number is None or ref.table_number not in by_num:
            unmatched.append(ref)
            continue
        if ref.table_number in seen_nums:
            continue
        seen_nums.add(ref.table_number)
        matched.append((ref, by_num[ref.table_number]))
    return matched, unmatched


def _as_table(raw: Any) -> FdaLabelTable | None:
    if isinstance(raw, FdaLabelTable):
        return raw
    if hasattr(raw, "model_dump"):
        try:
            return FdaLabelTable.model_validate(raw.model_dump(mode="json"))
        except Exception:  # noqa: BLE001
            return None
    if isinstance(raw, dict):
        try:
            return FdaLabelTable.model_validate(raw)
        except Exception:  # noqa: BLE001
            return None
    return None
