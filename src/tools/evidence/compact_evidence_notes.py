"""Compact evidence notes for planner/evaluator/synth LLM payloads."""

from __future__ import annotations

from typing import Any

_EVIDENCE_TAIL = 30


def compact_evidence_notes(
    notes: list[Any],
    *,
    tail: int | None = _EVIDENCE_TAIL,
) -> list[dict[str, Any]]:
    """Map notes to slim dicts; keep only the last ``tail`` (None = all)."""
    selected = notes if tail is None else notes[-max(1, tail) :]
    slim: list[dict[str, Any]] = []
    for note in selected:
        if hasattr(note, "model_dump"):
            raw = note.model_dump(mode="json")  # type: ignore[union-attr]
        elif isinstance(note, dict):
            raw = note
        else:
            continue
        slim.append(
            {
                "worker": raw.get("worker"),
                "query": raw.get("query"),
                "attr": raw.get("attr"),
                "nctid": raw.get("nctid"),
                "pmid": raw.get("pmid"),
                "setid": raw.get("setid"),
                "tradename": raw.get("tradename"),
                "label_id": raw.get("label_id"),
                "names": raw.get("names") or [],
                "summary": raw.get("summary") or "",
                "artifact_path": raw.get("artifact_path"),
                "total_chars": raw.get("total_chars"),
                "offset": raw.get("offset"),
                "next_offset": raw.get("next_offset"),
                "both_sides": raw.get("both_sides"),
            }
        )
    return slim
