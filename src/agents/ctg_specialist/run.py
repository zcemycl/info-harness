"""Run the CTG specialist PEWE loop (planner→executor→writer→evaluator)."""

from __future__ import annotations

import os
import uuid

from agents.ctg_specialist.pewe_stages import (
    run_evaluator_stage,
    run_executor_stage,
    run_planner_stage,
    run_writer_stage,
)
from agents.ctg_specialist.synthesize_answer import synthesize_ctg_answer
from model.ctg.ctg_evidence_note import CtgEvidenceNote
from model.ctg.ctg_specialist_result import CtgSpecialistResult
from model.research.agent_answer import (
    AgentAnswer,
    AnswerAudience,
    AnswerStatus,
)
from model.research.diary_entry import DiaryDecision, DiaryEntry
from tools.diary.write_agent_answer import write_agent_answer
from tools.diary.write_ctg_specialist_result import write_ctg_specialist_result
from tools.trace_call import trace_info, trace_span


def run_ctg_specialist(
    brief: str,
    *,
    max_loops: int | None = None,
    run_id: str | None = None,
) -> CtgSpecialistResult:
    """PEWE loop dispatching CTG nctid / condition / resolve_trial workers."""
    limit = max_loops or int(os.getenv("CTG_SPECIALIST_MAX_LOOPS", "3"))
    rid = run_id or uuid.uuid4().hex[:12]
    diary: list[DiaryEntry] = []
    evidence: list[CtgEvidenceNote] = []
    stage_answers: list[AgentAnswer] = []
    loops_run = 0

    with trace_span("agent", "ctg_specialist", run_id=rid, max_loops=limit):
        for loop in range(1, limit + 1):
            loops_run = loop
            loop_failures: list[str] = []
            with trace_span("loop", f"{loop}/{limit}"):
                planned = run_planner_stage(
                    brief,
                    loop=loop,
                    diary=diary,
                    evidence=evidence,
                    run_id=rid,
                    stage_answers=stage_answers,
                )
                if planned.tasks:
                    (
                        nctid_triples,
                        condition_pairs,
                        resolve_pairs,
                        loop_failures,
                    ) = run_executor_stage(
                        brief,
                        loop=loop,
                        tasks=planned.tasks,
                        run_id=rid,
                        stage_answers=stage_answers,
                    )
                    run_writer_stage(
                        brief,
                        loop=loop,
                        nctid_triples=nctid_triples,
                        condition_pairs=condition_pairs,
                        resolve_pairs=resolve_pairs,
                        evidence=evidence,
                        run_id=rid,
                        stage_answers=stage_answers,
                    )
                entry = run_evaluator_stage(
                    brief,
                    loop=loop,
                    evidence=evidence,
                    failures=loop_failures,
                    run_id=rid,
                    diary=diary,
                    stage_answers=stage_answers,
                )
            if entry.decision is DiaryDecision.COMPLETE:
                break
            if entry.decision is DiaryDecision.REPLAN and not planned.tasks:
                continue

        final_answer = _finalize_answer(brief, evidence, rid, loops_run, stage_answers)

    result = CtgSpecialistResult(
        answer=final_answer,
        stage_answers=stage_answers,
        evidence=evidence,
        diary=diary,
        loops=loops_run,
    )
    path = write_ctg_specialist_result(result, name_prefix=f"{rid}/ctg")
    trace_info("final written", path=path)
    return result


def _finalize_answer(
    brief: str,
    evidence: list[CtgEvidenceNote],
    rid: str,
    loops_run: int,
    stage_answers: list[AgentAnswer],
) -> AgentAnswer:
    with trace_span("stage", "synthesize"):
        text = synthesize_ctg_answer(brief, evidence).strip()
        status = AnswerStatus.OK if text and evidence else AnswerStatus.INCOMPLETE
        if not text:
            text = "No evidence collected; unable to answer the brief."
        final_answer = write_agent_answer(
            AgentAnswer(
                agent="ctg_specialist",
                audience=AnswerAudience.BOTH,
                brief=brief,
                answer=text,
                status=status,
                run_id=rid,
                loop=loops_run or None,
                extras={"loops": loops_run, "evidence": len(evidence)},
            ),
            name_prefix=f"{rid}/ctg",
            filename_stem="answer",
        )
        stage_answers.append(final_answer)
        trace_info("answer ready", chars=len(final_answer.answer))
        return final_answer
