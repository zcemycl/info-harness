"""Evaluator step for the research outer loop."""

from __future__ import annotations

import json
from typing import Any

from openai import LengthFinishReasonError

from agents.chat_model import chat_model
from agents.invoke_schema_with_reader import invoke_schema_with_reader
from model.research.diary_entry import DiaryDecision
from model.research.research_eval_result import ResearchEvalResult
from model.research.research_memory import ResearchMemory
from model.research.research_pack import ResearchPack
from model.research.research_plan import ResearchPlan
from prompt.load_prompt import load_prompt

_ANSWER_CAP = 4000
_FIELD_CAP = 500


def evaluate_research_loop(
    brief: str,
    *,
    loop: int,
    plan: ResearchPlan,
    pack: ResearchPack,
    answer_text: str,
    memory: ResearchMemory,
    synthesis_path: str | None = None,
) -> ResearchEvalResult:
    """Ask the evaluator LLM for ResearchEvalResult (diary + next_*)."""
    llm = chat_model(model_env="OPENROUTER_RESEARCH_EVALUATOR_MODEL")
    try:
        result = invoke_schema_with_reader(
            llm,
            ResearchEvalResult,
            system=load_prompt("research", "evaluator.md"),
            user=json.dumps(
                _payload(
                    brief,
                    loop,
                    plan,
                    pack,
                    answer_text,
                    memory,
                    synthesis_path,
                ),
                indent=2,
                default=str,
            ),
        )
    except LengthFinishReasonError:
        return _truncated(loop)
    evaluation = (
        result
        if isinstance(result, ResearchEvalResult)
        else ResearchEvalResult.model_validate(result)
    )
    return evaluation.model_copy(update={"loop": loop})


def _truncated(loop: int) -> ResearchEvalResult:
    return ResearchEvalResult(
        loop=loop,
        observations=[
            "Evaluator reply hit the model output limit; kept the synthesis."
        ],
        decision=DiaryDecision.CONTINUE,
    )


def _payload(
    brief: str,
    loop: int,
    plan: ResearchPlan,
    pack: ResearchPack,
    answer_text: str,
    memory: ResearchMemory,
    synthesis_path: str | None,
) -> dict[str, Any]:
    return {
        "brief": _clip(brief, _ANSWER_CAP),
        "loop": loop,
        "plan": _clip_value(plan.model_dump(mode="json")),
        "answer": _clip(answer_text, _ANSWER_CAP),
        "answer_chars": len(answer_text),
        "answer_path": synthesis_path,
        "outcomes": [
            {
                "workstream_id": item.workstream_id,
                "specialist": item.specialist.value,
                "focus": _clip(item.brief.focus, _FIELD_CAP),
                "fingerprint": item.idea_fingerprint,
                "status": item.status.value,
                "answer": _clip(item.answer.answer, 800),
                "answer_path": item.answer.path,
                "total_chars": len(item.answer.answer or ""),
                "error": item.error,
            }
            for item in pack.outcomes
        ],
        "memory": _clip_value(memory.model_dump(mode="json")),
    }


def _clip_value(value: Any) -> Any:
    if isinstance(value, str):
        return _clip(value, _FIELD_CAP)
    if isinstance(value, list):
        return [_clip_value(item) for item in value]
    if isinstance(value, dict):
        return {str(key): _clip_value(item) for key, item in value.items()}
    return value


def _clip(text: str, limit: int) -> str:
    if len(text) <= limit:
        return text
    return text[: limit - 1] + "…"
