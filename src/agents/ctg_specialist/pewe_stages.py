"""PEWE stage runners for the CTG specialist."""

from __future__ import annotations

from typing import Any

from agents.ctg_specialist.emit_stage_answer import emit_stage_answer
from agents.ctg_specialist.evaluate_loop import evaluate_ctg_loop
from agents.ctg_specialist.execute_tasks import execute_ctg_tasks
from agents.ctg_specialist.plan_tasks import plan_ctg_tasks
from agents.ctg_specialist.stage_answer_text import (
    evaluator_answer_text,
    executor_answer_text,
    planner_answer_text,
    writer_answer_text,
)
from agents.ctg_specialist.write_notes import write_ctg_evidence_notes
from model.ctg.ctg_attr_name import CtgAttrName
from model.ctg.ctg_attr_page import CtgAttrPage
from model.ctg.ctg_evidence_note import CtgEvidenceNote
from model.ctg.ctg_planner_output import CtgPlannerOutput
from model.ctg.ctg_worker_plan import CtgWorkerPlan
from model.research.agent_answer import AgentAnswer, AnswerStatus
from model.research.diary_entry import DiaryEntry
from tools.diary.write_diary import write_diary
from tools.trace_call import trace_info, trace_span

NctidTriple = tuple[CtgWorkerPlan, CtgAttrName, CtgAttrPage[Any]]
ConditionPair = tuple[CtgWorkerPlan, list[str]]


def run_planner_stage(
    brief: str,
    *,
    loop: int,
    diary: list[DiaryEntry],
    evidence: list[CtgEvidenceNote],
    run_id: str,
    stage_answers: list[AgentAnswer],
) -> CtgPlannerOutput:
    """Plan CTG tasks and emit a next-agent answer."""
    with trace_span("stage", "planner"):
        planned = plan_ctg_tasks(brief, loop=loop, diary=diary, evidence=evidence)
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
        trace_info(
            "plan ready",
            tasks=len(planned.tasks),
            rationale=planned.rationale[:120],
        )
        return planned


def run_executor_stage(
    brief: str,
    *,
    loop: int,
    tasks: list[CtgWorkerPlan],
    run_id: str,
    stage_answers: list[AgentAnswer],
) -> tuple[list[NctidTriple], list[ConditionPair], list[str]]:
    """Execute tasks and emit a next-agent answer."""
    with trace_span("stage", "executor", tasks=len(tasks)):
        nctid_triples, condition_pairs, failures = execute_ctg_tasks(tasks)
        if failures:
            trace_info("failures", count=len(failures))
        has_hits = bool(nctid_triples or condition_pairs)
        status = AnswerStatus.ERROR if failures and not has_hits else AnswerStatus.OK
        stage_answers.append(
            emit_stage_answer(
                agent="executor",
                brief=brief,
                answer=executor_answer_text(nctid_triples, condition_pairs, failures),
                run_id=run_id,
                loop=loop,
                status=status,
                extras={
                    "nctid_pages": len(nctid_triples),
                    "condition_searches": len(condition_pairs),
                    "failures": failures,
                },
            )
        )
        return nctid_triples, condition_pairs, failures


def run_writer_stage(
    brief: str,
    *,
    loop: int,
    nctid_triples: list[NctidTriple],
    condition_pairs: list[ConditionPair],
    evidence: list[CtgEvidenceNote],
    run_id: str,
    stage_answers: list[AgentAnswer],
) -> list[CtgEvidenceNote]:
    """Write evidence notes and emit a next-agent answer."""
    with trace_span("stage", "writer"):
        notes = write_ctg_evidence_notes(nctid_triples, condition_pairs)
        evidence.extend(notes)
        stage_answers.append(
            emit_stage_answer(
                agent="writer",
                brief=brief,
                answer=writer_answer_text(notes, evidence),
                run_id=run_id,
                loop=loop,
                extras={
                    "notes_added": len(notes),
                    "evidence_total": len(evidence),
                },
            )
        )
        trace_info("notes appended", notes=len(notes), total=len(evidence))
        return notes


def run_evaluator_stage(
    brief: str,
    *,
    loop: int,
    evidence: list[CtgEvidenceNote],
    failures: list[str],
    run_id: str,
    diary: list[DiaryEntry],
    stage_answers: list[AgentAnswer],
) -> DiaryEntry:
    """Evaluate the loop and emit a next-agent answer."""
    with trace_span("stage", "evaluator"):
        entry = evaluate_ctg_loop(
            brief, loop=loop, evidence=evidence, failures=failures
        )
        write_diary(entry, name_prefix=f"{run_id}/ctg")
        diary.append(entry)
        stage_answers.append(
            emit_stage_answer(
                agent="evaluator",
                brief=brief,
                answer=evaluator_answer_text(entry),
                run_id=run_id,
                loop=loop,
                extras=entry.model_dump(mode="json"),
            )
        )
        trace_info("decision", decision=entry.decision.value)
        return entry
