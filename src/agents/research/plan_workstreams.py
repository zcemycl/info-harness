"""Planner step for the research outer loop."""

from __future__ import annotations

from agents.chat_model import chat_model
from agents.invoke_schema_with_reader import invoke_schema_with_reader
from agents.research.apply_eval_feedback import apply_eval_feedback
from agents.research.build_planner_input import build_planner_input
from agents.research.ensure_workstream_ids import ensure_workstream_ids
from agents.research.restrict_plan_to_open import restrict_plan_to_open
from model.research.diary_entry import DiaryEntry
from model.research.research_eval_result import ResearchEvalResult
from model.research.research_memory import ResearchMemory
from model.research.research_plan import ResearchPlan
from prompt.load_prompt import load_prompt
from tools.research.annotate_ctg_for_references import annotate_ctg_for_references
from tools.research.collect_nct_ids_from_memory import collect_nct_ids_from_memory
from tools.research.collect_pmids import collect_pmids
from tools.research.collect_pmids_from_memory import collect_pmids_from_memory
from tools.research.enrich_ctg_briefs import enrich_ctg_briefs
from tools.research.enrich_pubmed_briefs import enrich_pubmed_briefs
from tools.research.gate_pubmed_briefs import gate_pubmed_briefs


def plan_workstreams(
    brief: str,
    *,
    loop: int,
    diary: list[DiaryEntry],
    memory: ResearchMemory,
    eval_feedback: ResearchEvalResult | None = None,
) -> ResearchPlan:
    """Ask the planner LLM for workstreams; apply memory guards."""
    llm = chat_model(model_env="OPENROUTER_RESEARCH_PLANNER_MODEL")
    result = invoke_schema_with_reader(
        llm,
        ResearchPlan,
        system=load_prompt("research", "planner.md"),
        user=build_planner_input(
            brief,
            loop=loop,
            diary=diary,
            memory=memory,
            eval_feedback=eval_feedback,
        ),
    )
    plan = (
        result
        if isinstance(result, ResearchPlan)
        else ResearchPlan.model_validate(result)
    )
    plan = plan.model_copy(update={"selected": ensure_workstream_ids(plan.selected)})
    plan = apply_eval_feedback(plan, eval_feedback)
    plan = restrict_plan_to_open(plan, memory, eval_feedback)
    known_ncts = collect_nct_ids_from_memory(memory)
    known_pmids = list(
        dict.fromkeys([*collect_pmids_from_memory(memory), *collect_pmids(brief)])
    )
    selected = enrich_ctg_briefs(ensure_workstream_ids(plan.selected), known_ncts)
    selected = enrich_pubmed_briefs(selected, known_pmids)
    selected = gate_pubmed_briefs(selected, user_brief=brief)
    selected = annotate_ctg_for_references(selected, user_brief=brief)
    return plan.model_copy(update={"selected": selected})
