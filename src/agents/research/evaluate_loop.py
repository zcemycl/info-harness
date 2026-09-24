"""Evaluator step for the research outer loop."""

from __future__ import annotations

import json

from agents.chat_model import chat_model
from model.research.research_eval_result import ResearchEvalResult
from model.research.research_memory import ResearchMemory
from model.research.research_pack import ResearchPack
from model.research.research_plan import ResearchPlan
from prompt.load_prompt import load_prompt


def evaluate_research_loop(
    brief: str,
    *,
    loop: int,
    plan: ResearchPlan,
    pack: ResearchPack,
    answer_text: str,
    memory: ResearchMemory,
) -> ResearchEvalResult:
    """Ask the evaluator LLM for ResearchEvalResult (diary + next_*)."""
    llm = chat_model(model_env="OPENROUTER_RESEARCH_EVALUATOR_MODEL")
    structured = llm.with_structured_output(ResearchEvalResult)
    payload = {
        "brief": brief,
        "loop": loop,
        "plan": plan.model_dump(mode="json"),
        "answer": answer_text,
        "outcomes": [
            {
                "workstream_id": o.workstream_id,
                "specialist": o.specialist.value,
                "focus": o.brief.focus,
                "fingerprint": o.idea_fingerprint,
                "status": o.status.value,
                "answer": o.answer.answer[:800],
                "error": o.error,
            }
            for o in pack.outcomes
        ],
        "memory": memory.model_dump(mode="json"),
    }
    result = structured.invoke(
        [
            {"role": "system", "content": load_prompt("research", "evaluator.md")},
            {
                "role": "user",
                "content": json.dumps(payload, indent=2, default=str),
            },
        ]
    )
    evaluation = (
        result
        if isinstance(result, ResearchEvalResult)
        else ResearchEvalResult.model_validate(result)
    )
    return evaluation.model_copy(update={"loop": loop})
