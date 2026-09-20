"""Format PEWE stage answers as text for the next agent."""

from __future__ import annotations

from typing import Any

from model.fda.fda_label_attr_page import FdaLabelAttrPage
from model.research.diary_entry import DiaryEntry
from model.research.evidence_note import EvidenceNote
from model.research.planner_output import PlannerOutput
from model.research.worker_plan import FdaAttrName, WorkerPlan


def planner_answer_text(planned: PlannerOutput) -> str:
    """Human/next-agent text summarizing the planner output."""
    lines = [
        f"Rationale: {planned.rationale}",
        f"Tasks ({len(planned.tasks)}):",
    ]
    for task in planned.tasks:
        lines.append(
            f"- worker={task.worker.value} query={task.query!r} "
            f"attrs={[a.value for a in task.attrs]} "
            f"offset={task.offset} limit={task.limit}"
        )
    return "\n".join(lines)


def executor_answer_text(
    pairs: list[tuple[WorkerPlan, FdaAttrName, FdaLabelAttrPage[Any]]],
    failures: list[str],
) -> str:
    """Human/next-agent text summarizing executor pages and failures."""
    lines = [f"Fetched {len(pairs)} page(s)."]
    for plan, attr, page in pairs:
        lines.append(
            f"- {plan.worker.value}/{attr.value} query={plan.query!r} "
            f"items={len(page.items)} next_offset={page.next_offset}"
        )
    if failures:
        lines.append(f"Failures ({len(failures)}):")
        lines.extend(f"- {item}" for item in failures)
    return "\n".join(lines)


def writer_answer_text(notes: list[EvidenceNote], evidence: list[EvidenceNote]) -> str:
    """Human/next-agent text summarizing writer ledger updates."""
    names = sorted({note.tradename for note in notes})
    joined = ", ".join(names) if names else "(none)"
    return (
        f"Appended {len(notes)} evidence note(s); ledger size={len(evidence)}. "
        f"Tradenames this pass: {joined}."
    )


def evaluator_answer_text(entry: DiaryEntry) -> str:
    """Human/next-agent text summarizing the evaluator decision."""
    actions = "; ".join(entry.recommended_next_actions) or "(none)"
    gaps = "; ".join(entry.evidence_gaps) or "(none)"
    return f"Decision: {entry.decision.value}. Next: {actions}. Gaps: {gaps}."
