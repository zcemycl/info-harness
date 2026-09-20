"""LLM-as-judge scoring for worker and inner eval runs."""

from __future__ import annotations

import json
import os

from agents.chat_model import chat_model
from model.eval.judge_score import JudgeScore
from model.research.agent_answer import AgentAnswer
from model.research.fda_specialist_result import FdaSpecialistResult
from prompt.load_prompt import load_prompt


def score_worker_judge(
    *,
    brief: str,
    answer: AgentAnswer,
    pass_threshold: float,
) -> JudgeScore:
    """Judge a worker answer; set passed from threshold."""
    payload = {
        "brief": brief,
        "answer": answer.answer,
        "status": answer.status.value,
        "tools_called": answer.extras.get("tools_called") or [],
    }
    return _invoke_judge(
        system=load_prompt("eval", "worker_judge.md"),
        payload=payload,
        pass_threshold=pass_threshold,
    )


def score_inner_judge(
    *,
    brief: str,
    result: FdaSpecialistResult,
    pass_threshold: float,
) -> JudgeScore:
    """Judge a specialist result; set passed from threshold."""
    planner = next((a for a in result.stage_answers if a.agent == "planner"), None)
    payload = {
        "brief": brief,
        "final_answer": result.answer.answer,
        "final_status": result.answer.status.value,
        "loops": result.loops,
        "planner_tasks": (planner.extras.get("tasks") if planner else []) or [],
        "evidence_summaries": [n.summary for n in result.evidence[:30]],
        "diary_decisions": [d.decision.value for d in result.diary],
    }
    return _invoke_judge(
        system=load_prompt("eval", "inner_judge.md"),
        payload=payload,
        pass_threshold=pass_threshold,
    )


def resolve_pass_threshold(override: float | None) -> float:
    """Use case override or FDA_EVAL_PASS_THRESHOLD (default 3.5)."""
    if override is not None:
        return override
    return float(os.getenv("FDA_EVAL_PASS_THRESHOLD", "3.5"))


def _invoke_judge(
    *,
    system: str,
    payload: dict[str, object],
    pass_threshold: float,
) -> JudgeScore:
    llm = chat_model()
    structured = llm.with_structured_output(JudgeScore)
    raw = structured.invoke(
        [
            {"role": "system", "content": system},
            {
                "role": "user",
                "content": json.dumps(payload, indent=2, default=str),
            },
        ]
    )
    score = raw if isinstance(raw, JudgeScore) else JudgeScore.model_validate(raw)
    score.passed = score.score >= pass_threshold
    return score
