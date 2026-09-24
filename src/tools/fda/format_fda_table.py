"""Render an FdaLabelTable as caption + TSV grid for LLM context."""

from __future__ import annotations

from typing import Any

from model.fda.fda_label_table import FdaLabelTable, FdaLabelTableContent


def format_fda_table(table: Any) -> str:
    """Return ``caption`` plus tab-separated ``content.table`` rows."""
    parsed = _as_table(table)
    if parsed is None:
        return str(table)
    lines: list[str] = []
    if parsed.caption:
        lines.append(parsed.caption.strip())
    grid = _grid(parsed.content)
    if grid:
        lines.append(_tsv(grid))
    elif parsed.content is not None:
        lines.append("(empty table grid)")
    return "\n".join(lines).strip()


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


def _grid(content: FdaLabelTableContent | dict[str, Any] | None) -> list[list[str]]:
    if content is None:
        return []
    if isinstance(content, FdaLabelTableContent):
        rows = content.table or []
    elif isinstance(content, dict):
        rows = content.get("table") or []
    else:
        return []
    out: list[list[str]] = []
    for row in rows:
        if isinstance(row, list):
            out.append([_cell(c) for c in row])
        else:
            out.append([_cell(row)])
    return out


def _cell(value: object) -> str:
    text = " ".join(str(value).split())
    return text.replace("\t", " ")


def _tsv(grid: list[list[str]]) -> str:
    return "\n".join("\t".join(row) for row in grid)
