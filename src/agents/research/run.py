"""Run the research outer PEWE loop (planner→executor→writer→evaluator)."""

from __future__ import annotations

import os
import uuid

from agents.research.enforce_continue_on_gaps import enforce_continue_on_gaps
from agents.research.merge_prior_pack import merge_prior_pack
from agents.research.pewe_stages import (
    run_evaluator_stage,
    run_executor_stage,
    run_planner_stage,
    run_writer_stage,
)
from agents.research.update_memory import update_research_memory
from model.research.agent_answer import (
    AgentAnswer,
    AnswerAudience,
    AnswerStatus,
)
from model.research.diary_entry import DiaryDecision, DiaryEntry
from model.research.research_eval_result import ResearchEvalResult
from model.research.research_memory import ResearchMemory
from model.research.research_pack import ResearchPack
from model.research.research_plan import ResearchPlan
from model.research.research_result import ResearchResult
from tools.diary.write_agent_answer import write_agent_answer
from tools.diary.write_research_memory import write_research_memory
from tools.diary.write_research_result import write_research_result
from tools.trace_call import trace_info, trace_span

DEFAULT_MAX_LOOPS = int(os.getenv("RESEARCH_MAX_LOOPS", "2"))
DEFAULT_CONCURRENCY = int(os.getenv("RESEARCH_SPECIALIST_CONCURRENCY", "3"))


async def run_research(
    brief: str,
    *,
    max_loops: int | None = None,
    run_id: str | None = None,
    concurrency: int | None = None,
    specialist_max_loops: int | None = None,
) -> ResearchResult:
    """Outer PEWE loop with durable memory across loops."""
    limit = max_loops if max_loops is not None else DEFAULT_MAX_LOOPS
    if limit < 1:
        raise ValueError(f"max_loops must be >= 1, got {limit}")
    rid = run_id or uuid.uuid4().hex[:12]
    conc = concurrency if concurrency is not None else DEFAULT_CONCURRENCY

    diary: list[DiaryEntry] = []
    stage_answers: list[AgentAnswer] = []
    memory = ResearchMemory()
    prior_pack: ResearchPack | None = None
    eval_feedback: ResearchEvalResult | None = None
    plan: ResearchPlan | None = None
    pack = ResearchPack()
    answer_text = ""
    evaluation: ResearchEvalResult | None = None
    loops_run = 0

    with trace_span("agent", "research", run_id=rid, max_loops=limit):
        for loop in range(1, limit + 1):
            loops_run = loop
            with trace_span("loop", f"{loop}/{limit}"):
                plan = run_planner_stage(
                    brief,
                    loop=loop,
                    diary=diary,
                    memory=memory,
                    eval_feedback=eval_feedback,
                    run_id=rid,
                    stage_answers=stage_answers,
                )
                pack = await run_executor_stage(
                    brief,
                    loop=loop,
                    plan=plan,
                    run_id=rid,
                    stage_answers=stage_answers,
                    concurrency=conc,
                    specialist_max_loops=specialist_max_loops,
                )
                pack = merge_prior_pack(pack, prior_pack)
                answer_text = run_writer_stage(
                    brief,
                    loop=loop,
                    plan=plan,
                    pack=pack,
                    run_id=rid,
                    stage_answers=stage_answers,
                )
                evaluation = run_evaluator_stage(
                    brief,
                    loop=loop,
                    plan=plan,
                    pack=pack,
                    answer_text=answer_text,
                    memory=memory,
                    diary=diary,
                    run_id=rid,
                    stage_answers=stage_answers,
                )
                evaluation = enforce_continue_on_gaps(evaluation, pack)
                memory = update_research_memory(memory, pack, evaluation, loop=loop)
                write_research_memory(memory, name_prefix=f"{rid}/research/loop-{loop}")
                prior_pack = pack
                eval_feedback = evaluation
            if evaluation.decision is DiaryDecision.COMPLETE:
                break

        final = _finalize_answer(brief, answer_text, pack, rid, loops_run)

    result = ResearchResult(
        answer=final,
        stage_answers=stage_answers,
        plan=plan,
        pack=pack,
        diary=diary,
        evaluation=evaluation,
        memory=memory,
        loops=loops_run,
        run_id=rid,
    )
    path = write_research_result(result, name_prefix=f"{rid}/research")
    trace_info("final written", path=path)
    return result


def _finalize_answer(
    brief: str,
    answer_text: str,
    pack: ResearchPack,
    rid: str,
    loops_run: int,
) -> AgentAnswer:
    text = answer_text.strip() or "No synthesis produced; unable to answer the brief."
    ok_any = any(o.status is AnswerStatus.OK for o in pack.outcomes)
    status = AnswerStatus.OK if text and ok_any else AnswerStatus.INCOMPLETE
    return write_agent_answer(
        AgentAnswer(
            agent="research",
            audience=AnswerAudience.BOTH,
            brief=brief,
            answer=text,
            status=status,
            run_id=rid,
            loop=loops_run or None,
            extras={
                "loops": loops_run,
                "outcomes": len(pack.outcomes),
                "settled": [
                    o.workstream_id
                    for o in pack.outcomes
                    if o.status is AnswerStatus.OK
                ],
            },
        ),
        name_prefix=f"{rid}/research",
        filename_stem="answer",
    )
