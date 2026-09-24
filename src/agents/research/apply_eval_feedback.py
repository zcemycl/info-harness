"""Merge evaluator next_* directives into a ResearchPlan."""

from __future__ import annotations

from agents.research.ensure_workstream_ids import ensure_workstream_ids
from model.research.research_eval_result import ResearchEvalResult
from model.research.research_plan import ResearchPlan
from model.research.specialist_brief import SpecialistBrief


def apply_eval_feedback(
    plan: ResearchPlan,
    eval_feedback: ResearchEvalResult | None,
) -> ResearchPlan:
    """Ensure next_briefs / next_specialists land in the plan (not broadcast)."""
    if eval_feedback is None:
        return plan

    by_id: dict[str, SpecialistBrief] = {}
    order: list[str] = []
    for brief in ensure_workstream_ids(plan.selected):
        wid = brief.workstream_id or ""
        if wid not in by_id:
            order.append(wid)
        by_id[wid] = brief

    for brief in ensure_workstream_ids(list(eval_feedback.next_briefs)):
        wid = brief.workstream_id or ""
        if wid not in by_id:
            order.append(wid)
        by_id[wid] = brief

    # If evaluator named specialists without briefs, add stub focuses.
    existing_kinds = {b.specialist for b in by_id.values()}
    for kind in eval_feedback.next_specialists:
        if kind in existing_kinds:
            continue
        action = (
            eval_feedback.recommended_next_actions[0]
            if eval_feedback.recommended_next_actions
            else f"Investigate using {kind.value}"
        )
        stub = ensure_workstream_ids([SpecialistBrief(specialist=kind, focus=action)])[
            0
        ]
        wid = stub.workstream_id or kind.value
        order.append(wid)
        by_id[wid] = stub
        existing_kinds.add(kind)

    return plan.model_copy(update={"selected": [by_id[k] for k in order if k in by_id]})
