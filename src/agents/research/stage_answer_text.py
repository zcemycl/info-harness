"""Format research PEWE stage answers as text for the next agent."""

from __future__ import annotations

from model.research.diary_entry import DiaryEntry
from model.research.research_eval_result import ResearchEvalResult
from model.research.research_pack import ResearchPack
from model.research.research_plan import ResearchPlan


def planner_answer_text(planned: ResearchPlan) -> str:
    """Summarize planner workstreams."""
    lines = [
        f"Rationale: {planned.rationale}",
        f"Directions: {'; '.join(planned.general_directions) or '(none)'}",
        f"Workstreams ({len(planned.selected)}):",
    ]
    for brief in planned.selected:
        lines.append(
            f"- id={brief.workstream_id} specialist={brief.specialist.value} "
            f"focus={brief.focus!r} seeds={brief.seed_queries}"
        )
    return "\n".join(lines)


def executor_answer_text(pack: ResearchPack) -> str:
    """Summarize spawn outcomes."""
    lines = [f"Spawned {len(pack.outcomes)} workstream(s)."]
    for item in pack.outcomes:
        lines.append(
            f"- {item.workstream_id} {item.specialist.value} "
            f"status={item.status.value} err={item.error or '-'}"
        )
    return "\n".join(lines)


def writer_answer_text(answer: str) -> str:
    """Summarize writer synthesis."""
    preview = answer.strip().replace("\n", " ")
    if len(preview) > 240:
        preview = preview[:237] + "..."
    return f"Synthesis ready ({len(answer)} chars): {preview}"


def evaluator_answer_text(entry: DiaryEntry | ResearchEvalResult) -> str:
    """Summarize evaluator decision."""
    actions = "; ".join(entry.recommended_next_actions) or "(none)"
    gaps = "; ".join(entry.evidence_gaps) or "(none)"
    return f"Decision: {entry.decision.value}. Next: {actions}. Gaps: {gaps}."
