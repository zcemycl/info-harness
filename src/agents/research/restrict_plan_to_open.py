"""Drop locked / already-tried workstreams from later research plans."""

from __future__ import annotations

from agents.research.fingerprint_idea import fingerprint_brief
from model.research.research_eval_result import ResearchEvalResult
from model.research.research_memory import ResearchMemory
from model.research.research_plan import ResearchPlan
from model.research.specialist_brief import SpecialistBrief


def restrict_plan_to_open(
    plan: ResearchPlan,
    memory: ResearchMemory,
    eval_feedback: ResearchEvalResult | None,
) -> ResearchPlan:
    """Keep only unlocked, non-duplicate briefs on later outer loops.

    Improvements over FDE criterion-only locking:
    - Lock by workstream_id (multi-brief per specialist allowed)
    - Drop identical idea fingerprints already tried successfully
    - Drop focuses that match rejected/failed approaches unless forced
    """
    forced_ids = set(eval_feedback.force_rerun_workstream_ids if eval_feedback else [])
    forced_briefs = list(eval_feedback.next_briefs if eval_feedback else [])
    settled = memory.settled_ids()
    ok_fps = {
        item.fingerprint
        for item in memory.tried_ideas
        if item.status == "ok" and item.workstream_id in settled
    }
    rejected = {_norm(x) for x in memory.rejected_directions}

    kept: list[SpecialistBrief] = []
    skipped: list[str] = []
    for brief in plan.selected:
        wid = (brief.workstream_id or "").strip()
        fp = fingerprint_brief(brief)
        if wid and wid in settled and wid not in forced_ids:
            skipped.append(f"locked:{wid}")
            continue
        if fp in ok_fps and wid not in forced_ids:
            skipped.append(f"tried-ok:{fp}")
            continue
        focus_n = _norm(brief.focus)
        if any(focus_n and focus_n in r for r in rejected):
            skipped.append(f"rejected-direction:{brief.specialist.value}")
            continue
        kept.append(brief)

    if not kept and (forced_briefs or memory.open_gaps):
        kept = list(forced_briefs) or [
            SpecialistBrief(
                specialist=item.specialist,
                focus=f"Revisit gap: {gap}",
                workstream_id=f"gap-{item.workstream_id}",
            )
            for item, gap in zip(memory.tried_ideas[-3:], memory.open_gaps[:3])
        ]

    rationale = plan.rationale
    if skipped:
        note = f"Skipped remembered work ({len(skipped)}): {', '.join(skipped[:8])}."
        rationale = f"{rationale.rstrip()} {note}".strip()
    return plan.model_copy(update={"selected": kept, "rationale": rationale})


def _norm(text: str) -> str:
    return " ".join(text.strip().lower().split())
