"""Force CTG fetch references when literature is needed but PMIDs missing."""

from __future__ import annotations

from model.research.diary_entry import DiaryDecision
from model.research.research_eval_result import ResearchEvalResult
from model.research.research_pack import ResearchPack
from model.research.specialist_brief import SpecialistBrief
from model.research.specialist_kind import SpecialistKind
from tools.research.brief_wants_literature import brief_wants_literature
from tools.research.collect_nct_ids_from_pack import collect_nct_ids_from_pack
from tools.research.collect_pmids_from_pack import collect_pmids_from_pack


def enforce_ctg_references(
    evaluation: ResearchEvalResult,
    pack: ResearchPack,
    *,
    user_brief: str,
) -> ResearchEvalResult:
    """If literature brief has NCTs but no PMIDs, force CTG worker=fetch references."""
    lit_texts = [
        user_brief,
        *[o.brief.focus for o in pack.outcomes],
        *[b.focus for b in evaluation.next_briefs],
    ]
    if not brief_wants_literature(*lit_texts):
        return evaluation
    if collect_pmids_from_pack(pack):
        return evaluation
    known = collect_nct_ids_from_pack(pack)
    if not known:
        return evaluation

    gap = (
        "Literature requested but CTG did not return PMIDs — need "
        f"worker=fetch attrs=[references] for {', '.join(known[:8])}."
    )
    focus = (
        "Literature / PubMed handoff: for each NCT use worker=fetch with "
        f"attrs=[references] (limit=20): {', '.join(known)}. "
        "Do not use worker=nctid alone — references is fetch-only."
    )
    next_brief = SpecialistBrief(
        specialist=SpecialistKind.CTG,
        focus=focus,
        seed_queries=known,
        workstream_id="ctg-fetch-references",
    )
    next_briefs = list(evaluation.next_briefs)
    if not any(b.workstream_id == "ctg-fetch-references" for b in next_briefs):
        next_briefs.append(next_brief)
    ctg_ids = [
        o.workstream_id for o in pack.outcomes if o.specialist is SpecialistKind.CTG
    ]
    return evaluation.model_copy(
        update={
            "decision": DiaryDecision.CONTINUE,
            "evidence_gaps": list(dict.fromkeys([*evaluation.evidence_gaps, gap])),
            "recommended_next_actions": list(
                dict.fromkeys(
                    [
                        *evaluation.recommended_next_actions,
                        f"CTG fetch references for {', '.join(known[:6])}",
                    ]
                )
            ),
            "next_briefs": next_briefs,
            "next_specialists": list(
                dict.fromkeys([*evaluation.next_specialists, SpecialistKind.CTG])
            ),
            "force_rerun_workstream_ids": list(
                dict.fromkeys([*evaluation.force_rerun_workstream_ids, *ctg_ids])
            ),
            "lessons": list(
                dict.fromkeys(
                    [
                        *evaluation.lessons,
                        "PubMed PMIDs come from CTG worker=fetch "
                        "references — not from worker=nctid.",
                    ]
                )
            ),
        }
    )
