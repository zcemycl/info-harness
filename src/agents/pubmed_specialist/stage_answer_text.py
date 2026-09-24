"""Format PubMed PEWE stage answers as text for the next agent."""

from __future__ import annotations

from typing import Any

from model.pubmed.pubmed_attr_name import PubmedAttrName
from model.pubmed.pubmed_attr_page import PubmedAttrPage
from model.pubmed.pubmed_evidence_note import PubmedEvidenceNote
from model.pubmed.pubmed_planner_output import PubmedPlannerOutput
from model.pubmed.pubmed_worker_plan import PubmedWorkerPlan
from model.research.diary_entry import DiaryEntry


def planner_answer_text(planned: PubmedPlannerOutput) -> str:
    """Human/next-agent text summarizing the planner output."""
    lines = [
        f"Rationale: {planned.rationale}",
        f"Tasks ({len(planned.tasks)}):",
    ]
    for task in planned.tasks:
        lines.append(
            f"- worker=id query={task.query!r} "
            f"attrs={[a.value for a in task.attrs]} "
            f"offset={task.offset} limit={task.limit}"
        )
    return "\n".join(lines)


def executor_answer_text(
    triples: list[tuple[PubmedWorkerPlan, PubmedAttrName, PubmedAttrPage[Any]]],
    failures: list[str],
) -> str:
    """Human/next-agent text summarizing executor results and failures."""
    lines = [f"Fetched {len(triples)} result set(s)."]
    for plan, attr, page in triples:
        lines.append(
            f"- id/{attr.value} query={plan.query!r} "
            f"items={len(page.items)} next_offset={page.next_offset}"
        )
    if failures:
        lines.append(f"Failures ({len(failures)}):")
        lines.extend(f"- {item}" for item in failures)
    return "\n".join(lines)


def writer_answer_text(
    notes: list[PubmedEvidenceNote], evidence: list[PubmedEvidenceNote]
) -> str:
    """Human/next-agent text summarizing writer ledger updates."""
    pmids = sorted({n.pmid for n in notes if n.pmid})
    joined = ", ".join(pmids) if pmids else "(none)"
    return (
        f"Appended {len(notes)} evidence note(s); ledger size={len(evidence)}. "
        f"PMIDs this pass: {joined}."
    )


def evaluator_answer_text(entry: DiaryEntry) -> str:
    """Human/next-agent text summarizing the evaluator decision."""
    actions = "; ".join(entry.recommended_next_actions) or "(none)"
    gaps = "; ".join(entry.evidence_gaps) or "(none)"
    return f"Decision: {entry.decision.value}. Next: {actions}. Gaps: {gaps}."
