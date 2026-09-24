"""Planner step for the research outer loop."""

from __future__ import annotations

from agents.chat_model import chat_model
from agents.research.apply_eval_feedback import apply_eval_feedback
from agents.research.build_planner_input import build_planner_input
from agents.research.ensure_workstream_ids import ensure_workstream_ids
from agents.research.restrict_plan_to_open import restrict_plan_to_open
from model.research.diary_entry import DiaryEntry
from model.research.research_eval_result import ResearchEvalResult
from model.research.research_memory import ResearchMemory
from model.research.research_plan import ResearchPlan
from prompt.load_prompt import load_prompt
from tools.research.collect_nct_ids_from_memory import collect_nct_ids_from_memory
from tools.research.enrich_ctg_briefs import enrich_ctg_briefs


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
    structured = llm.with_structured_output(ResearchPlan)
    result = structured.invoke(
        [
            {"role": "system", "content": load_prompt("research", "planner.md")},
            {
                "role": "user",
                "content": build_planner_input(
                    brief,
                    loop=loop,
                    diary=diary,
                    memory=memory,
                    eval_feedback=eval_feedback,
                ),
            },
        ]
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
    selected = enrich_ctg_briefs(ensure_workstream_ids(plan.selected), known_ncts)
    return plan.model_copy(update={"selected": selected})
