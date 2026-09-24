"""Force continue when pack has NCT ids but CTG never fetched them."""

from __future__ import annotations

from model.research.diary_entry import DiaryDecision
from model.research.research_eval_result import ResearchEvalResult
from model.research.research_pack import ResearchPack
from model.research.specialist_brief import SpecialistBrief
from model.research.specialist_kind import SpecialistKind
from tools.research.collect_nct_ids import collect_nct_ids
from tools.research.collect_nct_ids_from_pack import collect_nct_ids_from_pack


def enforce_ctg_nct_coverage(
    evaluation: ResearchEvalResult,
    pack: ResearchPack,
) -> ResearchEvalResult:
    """If FDA/other pack text has NCTs CTG answers omit, force CTG follow-up."""
    known = collect_nct_ids_from_pack(pack)
    if not known:
        return evaluation

    ctg_text = " ".join(
        (o.answer.answer or "")
        for o in pack.outcomes
        if o.specialist is SpecialistKind.CTG
    )
    covered = set(collect_nct_ids(ctg_text))
    missing = [n for n in known if n not in covered]
    if not missing:
        return evaluation

    gap = "CTG has not reported study sections for known NCT ids: " + ", ".join(missing)
    focus = (
        "Fetch ClinicalTrials.gov sections for these NCT ids: "
        f"{', '.join(missing)}. Prefer worker=nctid or fetch with "
        "attrs basic_info, outcomes, adverse_events, demographics, "
        "conditions, locations; add references when results are thin."
    )
    next_brief = SpecialistBrief(
        specialist=SpecialistKind.CTG,
        focus=focus,
        seed_queries=missing,
        workstream_id="ctg-known-ncts",
    )
    next_briefs = list(evaluation.next_briefs)
    if not any(b.workstream_id == "ctg-known-ncts" for b in next_briefs):
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
                        f"CTG nctid/fetch for {', '.join(missing)}",
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
                        "When FDA (or brief) lists NCT ids, CTG must fetch "
                        "those ids — do not only search by drug/condition name.",
                    ]
                )
            ),
        }
    )
