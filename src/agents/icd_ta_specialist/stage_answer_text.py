"""Format ICD PEWE stage answers as text for the next agent."""

from __future__ import annotations

from model.research.diary_entry import DiaryEntry
from model.therapeutic_area.icd_evidence_note import IcdEvidenceNote
from model.therapeutic_area.icd_planner_output import IcdPlannerOutput
from model.therapeutic_area.icd_worker_plan import IcdWorkerPlan


def planner_answer_text(planned: IcdPlannerOutput) -> str:
    """Human/next-agent text summarizing the planner output."""
    lines = [
        f"Rationale: {planned.rationale}",
        f"Tasks ({len(planned.tasks)}):",
    ]
    for task in planned.tasks:
        like = "%q%" if task.both_sides else "q%"
        lines.append(f"- q={task.q!r} both_sides={task.both_sides} ({like})")
    return "\n".join(lines)


def executor_answer_text(
    pairs: list[tuple[IcdWorkerPlan, list[str]]],
    failures: list[str],
) -> str:
    """Human/next-agent text summarizing search results and failures."""
    lines = [f"Fetched {len(pairs)} search result set(s)."]
    for plan, names in pairs:
        like = "%q%" if plan.both_sides else "q%"
        preview = ", ".join(names[:5])
        more = f" (+{len(names) - 5} more)" if len(names) > 5 else ""
        lines.append(f"- q={plan.q!r} {like} hits={len(names)}: {preview}{more}")
    if failures:
        lines.append(f"Failures ({len(failures)}):")
        lines.extend(f"- {item}" for item in failures)
    return "\n".join(lines)


def writer_answer_text(
    notes: list[IcdEvidenceNote], evidence: list[IcdEvidenceNote]
) -> str:
    """Human/next-agent text summarizing writer ledger updates."""
    n_names = sum(len(n.names) for n in notes)
    return (
        f"Appended {len(notes)} evidence note(s) covering {n_names} name(s); "
        f"ledger size={len(evidence)}."
    )


def evaluator_answer_text(entry: DiaryEntry) -> str:
    """Human/next-agent text summarizing the evaluator decision."""
    actions = "; ".join(entry.recommended_next_actions) or "(none)"
    gaps = "; ".join(entry.evidence_gaps) or "(none)"
    return f"Decision: {entry.decision.value}. Next: {actions}. Gaps: {gaps}."
