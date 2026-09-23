"""Format CTG PEWE stage answers as text for the next agent."""

from __future__ import annotations

from typing import Any

from model.ctg.ctg_attr_name import CtgAttrName
from model.ctg.ctg_attr_page import CtgAttrPage
from model.ctg.ctg_evidence_note import CtgEvidenceNote
from model.ctg.ctg_planner_output import CtgPlannerOutput
from model.ctg.ctg_worker_plan import CtgWorkerName, CtgWorkerPlan
from model.research.diary_entry import DiaryEntry


def planner_answer_text(planned: CtgPlannerOutput) -> str:
    """Human/next-agent text summarizing the planner output."""
    lines = [
        f"Rationale: {planned.rationale}",
        f"Tasks ({len(planned.tasks)}):",
    ]
    for task in planned.tasks:
        if task.worker is CtgWorkerName.CONDITION:
            like = "%q%" if task.both_sides else "q%"
            lines.append(
                f"- worker=condition query={task.query!r} "
                f"both_sides={task.both_sides} ({like})"
            )
        else:
            lines.append(
                f"- worker=nctid query={task.query!r} "
                f"attrs={[a.value for a in task.attrs]} "
                f"offset={task.offset} limit={task.limit}"
            )
    return "\n".join(lines)


def executor_answer_text(
    nctid_triples: list[tuple[CtgWorkerPlan, CtgAttrName, CtgAttrPage[Any]]],
    condition_pairs: list[tuple[CtgWorkerPlan, list[str]]],
    failures: list[str],
) -> str:
    """Human/next-agent text summarizing executor results and failures."""
    total = len(nctid_triples) + len(condition_pairs)
    lines = [f"Fetched {total} result set(s)."]
    for plan, attr, page in nctid_triples:
        lines.append(
            f"- nctid/{attr.value} query={plan.query!r} "
            f"items={len(page.items)} next_offset={page.next_offset}"
        )
    for plan, names in condition_pairs:
        like = "%q%" if plan.both_sides else "q%"
        preview = ", ".join(names[:5])
        more = f" (+{len(names) - 5} more)" if len(names) > 5 else ""
        lines.append(
            f"- condition q={plan.query!r} {like} "
            f"hits={len(names)}: {preview}{more}"
        )
    if failures:
        lines.append(f"Failures ({len(failures)}):")
        lines.extend(f"- {item}" for item in failures)
    return "\n".join(lines)


def writer_answer_text(
    notes: list[CtgEvidenceNote], evidence: list[CtgEvidenceNote]
) -> str:
    """Human/next-agent text summarizing writer ledger updates."""
    nctids = sorted({n.nctid for n in notes if n.nctid})
    joined = ", ".join(nctids) if nctids else "(none)"
    return (
        f"Appended {len(notes)} evidence note(s); ledger size={len(evidence)}. "
        f"NCT ids this pass: {joined}."
    )


def evaluator_answer_text(entry: DiaryEntry) -> str:
    """Human/next-agent text summarizing the evaluator decision."""
    actions = "; ".join(entry.recommended_next_actions) or "(none)"
    gaps = "; ".join(entry.evidence_gaps) or "(none)"
    return f"Decision: {entry.decision.value}. Next: {actions}. Gaps: {gaps}."
