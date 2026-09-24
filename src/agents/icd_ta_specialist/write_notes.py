"""Writer step: compress ICD search results into evidence notes."""

from __future__ import annotations

from model.therapeutic_area.icd_evidence_note import IcdEvidenceNote
from model.therapeutic_area.icd_worker_plan import IcdWorkerPlan


def write_icd_evidence_notes(
    pairs: list[tuple[IcdWorkerPlan, list[str]]],
) -> list[IcdEvidenceNote]:
    """Turn executed searches into compact ledger notes (deterministic)."""
    notes: list[IcdEvidenceNote] = []
    for plan, names in pairs:
        like = "%q%" if plan.both_sides else "q%"
        preview = ", ".join(names[:8])
        more = f" (+{len(names) - 8} more)" if len(names) > 8 else ""
        notes.append(
            IcdEvidenceNote(
                query=plan.q,
                both_sides=plan.both_sides,
                names=names,
                summary=f"{like} q={plan.q!r} → {len(names)} hit(s): {preview}{more}",
            )
        )
    return notes
