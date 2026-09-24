"""Research PEWE stage runners that always emit an AgentAnswer."""

from __future__ import annotations

from agents.research.emit_stage_answer import emit_stage_answer
from agents.research.eval_to_diary_entry import eval_to_diary_entry
from agents.research.evaluate_loop import evaluate_research_loop
from agents.research.execute_workstreams import execute_workstreams
from agents.research.plan_workstreams import plan_workstreams
from agents.research.stage_answer_text import (
    evaluator_answer_text,
    executor_answer_text,
    planner_answer_text,
    writer_answer_text,
)
from agents.research.write_synthesis import write_synthesis
from model.research.agent_answer import AgentAnswer, AnswerStatus
from model.research.diary_entry import DiaryEntry
from model.research.research_eval_result import ResearchEvalResult
from model.research.research_memory import ResearchMemory
from model.research.research_pack import ResearchPack
from model.research.research_plan import ResearchPlan
from tools.diary.write_diary import write_diary
from tools.trace_call import trace_info, trace_span


def run_planner_stage(
    brief: str,
    *,
    loop: int,
    diary: list[DiaryEntry],
    memory: ResearchMemory,
    eval_feedback: ResearchEvalResult | None,
    run_id: str,
    stage_answers: list[AgentAnswer],
) -> ResearchPlan:
    """Plan workstreams and emit a next-agent answer."""
    with trace_span("stage", "planner"):
        planned = plan_workstreams(
            brief,
            loop=loop,
            diary=diary,
            memory=memory,
            eval_feedback=eval_feedback,
        )
        stage_answers.append(
            emit_stage_answer(
                agent="planner",
                brief=brief,
                answer=planner_answer_text(planned),
                run_id=run_id,
                loop=loop,
                extras=planned.model_dump(mode="json"),
            )
        )
        trace_info("plan ready", workstreams=len(planned.selected))
        return planned


async def run_executor_stage(
    brief: str,
    *,
    loop: int,
    plan: ResearchPlan,
    run_id: str,
    stage_answers: list[AgentAnswer],
    concurrency: int,
    specialist_max_loops: int | None,
) -> ResearchPack:
    """Spawn specialists and emit a next-agent answer."""
    with trace_span("stage", "executor", workstreams=len(plan.selected)):
        pack = await execute_workstreams(
            plan,
            run_id=run_id,
            concurrency=concurrency,
            specialist_max_loops=specialist_max_loops,
        )
        bad = sum(1 for o in pack.outcomes if o.status is not AnswerStatus.OK)
        all_bad = bool(pack.outcomes) and bad == len(pack.outcomes)
        status = AnswerStatus.ERROR if all_bad else AnswerStatus.OK
        stage_answers.append(
            emit_stage_answer(
                agent="executor",
                brief=brief,
                answer=executor_answer_text(pack),
                run_id=run_id,
                loop=loop,
                status=status,
                extras={"outcomes": len(pack.outcomes), "failed": bad},
            )
        )
        return pack


def run_writer_stage(
    brief: str,
    *,
    loop: int,
    plan: ResearchPlan,
    pack: ResearchPack,
    run_id: str,
    stage_answers: list[AgentAnswer],
) -> str:
    """Synthesize answer text and emit a next-agent answer."""
    with trace_span("stage", "writer"):
        text = write_synthesis(brief, plan, pack).strip()
        stage_answers.append(
            emit_stage_answer(
                agent="writer",
                brief=brief,
                answer=writer_answer_text(text),
                run_id=run_id,
                loop=loop,
                extras={"chars": len(text)},
            )
        )
        trace_info("synthesis ready", chars=len(text))
        return text


def run_evaluator_stage(
    brief: str,
    *,
    loop: int,
    plan: ResearchPlan,
    pack: ResearchPack,
    answer_text: str,
    memory: ResearchMemory,
    diary: list[DiaryEntry],
    run_id: str,
    stage_answers: list[AgentAnswer],
) -> ResearchEvalResult:
    """Evaluate the loop, write DiaryEntry, emit stage answer."""
    with trace_span("stage", "evaluator"):
        evaluation = evaluate_research_loop(
            brief,
            loop=loop,
            plan=plan,
            pack=pack,
            answer_text=answer_text,
            memory=memory,
        )
        entry = eval_to_diary_entry(evaluation)
        write_diary(entry, name_prefix=f"{run_id}/research")
        diary.append(entry)
        stage_answers.append(
            emit_stage_answer(
                agent="evaluator",
                brief=brief,
                answer=evaluator_answer_text(evaluation),
                run_id=run_id,
                loop=loop,
                extras=evaluation.model_dump(mode="json"),
            )
        )
        trace_info("decision", decision=evaluation.decision.value)
        return evaluation
