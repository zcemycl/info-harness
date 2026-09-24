"""Force continue when pack has CTG PMIDs but pubmed never fetched them."""

from __future__ import annotations

from model.research.diary_entry import DiaryDecision
from model.research.research_eval_result import ResearchEvalResult
from model.research.research_pack import ResearchPack
from model.research.specialist_brief import SpecialistBrief
from model.research.specialist_kind import SpecialistKind
from tools.research.collect_pmids import collect_pmids
from tools.research.collect_pmids_from_pack import collect_pmids_from_pack


def enforce_pubmed_pmid_coverage(
    evaluation: ResearchEvalResult,
    pack: ResearchPack,
) -> ResearchEvalResult:
    """If upstream PMIDs exist but pubmed omitted them, force pubmed follow-up."""
    known = collect_pmids_from_pack(pack)
    if not known:
        return evaluation

    covered: set[str] = set()
    pubmed_ran = False
    for outcome in pack.outcomes:
        if outcome.specialist is not SpecialistKind.PUBMED:
            continue
        pubmed_ran = True
        covered |= set(collect_pmids(outcome.answer.answer))
        dump = outcome.specialist_result or {}
        for note in dump.get("evidence") or []:
            if isinstance(note, dict) and note.get("pmid"):
                covered.add(str(note["pmid"]).strip())
    missing = [p for p in known if p not in covered]
    if not missing and pubmed_ran:
        return evaluation
    if not missing:
        missing = known

    gap = "PubMed has not fetched upstream PMIDs: " + ", ".join(missing[:12])
    focus = (
        "Fetch MEDLINE sections (abstract + citation) for these PMIDs only: "
        f"{', '.join(missing[:12])}. Do not invent other PMIDs."
    )
    next_brief = SpecialistBrief(
        specialist=SpecialistKind.PUBMED,
        focus=focus,
        seed_queries=missing[:12],
        workstream_id="pubmed-known-pmids",
    )
    next_briefs = list(evaluation.next_briefs)
    if not any(b.workstream_id == "pubmed-known-pmids" for b in next_briefs):
        next_briefs.append(next_brief)
    return evaluation.model_copy(
        update={
            "decision": DiaryDecision.CONTINUE,
            "evidence_gaps": list(dict.fromkeys([*evaluation.evidence_gaps, gap])),
            "recommended_next_actions": list(
                dict.fromkeys(
                    [
                        *evaluation.recommended_next_actions,
                        f"PubMed id for {', '.join(missing[:8])}",
                    ]
                )
            ),
            "next_briefs": next_briefs,
            "next_specialists": list(
                dict.fromkeys([*evaluation.next_specialists, SpecialistKind.PUBMED])
            ),
            "lessons": list(
                dict.fromkeys(
                    [
                        *evaluation.lessons,
                        "Known PMIDs: " + ", ".join(known[:20]),
                        "Spawn pubmed only with PMIDs from CTG references "
                        "or the user brief — never invent PMIDs.",
                    ]
                )
            ),
        }
    )
