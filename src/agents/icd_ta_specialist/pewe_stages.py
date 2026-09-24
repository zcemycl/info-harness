"""PEWE stage runners for the ICD therapeutic-area specialist."""

from __future__ import annotations

from agents.icd_ta_specialist.emit_stage_answer import emit_stage_answer
from agents.icd_ta_specialist.evaluate_loop import evaluate_icd_loop
from agents.icd_ta_specialist.execute_tasks import execute_icd_tasks
from agents.icd_ta_specialist.plan_tasks import plan_icd_tasks
from agents.icd_ta_specialist.stage_answer_text import (
    evaluator_answer_text,
    executor_answer_text,
    planner_answer_text,
    writer_answer_text,
)
from agents.icd_ta_specialist.write_notes import write_icd_evidence_notes
from model.research.agent_answer import AgentAnswer, AnswerStatus
from model.research.diary_entry import DiaryEntry
from model.therapeutic_area.icd_evidence_note import IcdEvidenceNote
from model.therapeutic_area.icd_planner_output import IcdPlannerOutput
from model.therapeutic_area.icd_worker_plan import IcdWorkerPlan
from tools.diary.write_diary import write_diary
from tools.trace_call import trace_info, trace_span

SearchPair = tuple[IcdWorkerPlan, list[str]]


def run_planner_stage(
    brief: str,
    *,
    loop: int,
    diary: list[DiaryEntry],
    evidence: list[IcdEvidenceNote],
    run_id: str,
    stage_answers: list[AgentAnswer],
) -> IcdPlannerOutput:
    """Plan ICD TA searches and emit a next-agent answer."""
    with trace_span("stage", "planner"):
        planned = plan_icd_tasks(brief, loop=loop, diary=diary, evidence=evidence)
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
    tasks: list[IcdWorkerPlan],
    run_id: str,
    stage_answers: list[AgentAnswer],
) -> tuple[list[SearchPair], list[str]]:
    """Execute searches and emit a next-agent answer."""
    with trace_span("stage", "executor", tasks=len(tasks)):
        pairs, failures = execute_icd_tasks(tasks)
        if failures:
            trace_info("failures", count=len(failures))
        status = AnswerStatus.ERROR if failures and not pairs else AnswerStatus.OK
        stage_answers.append(
            emit_stage_answer(
                agent="executor",
                brief=brief,
                answer=executor_answer_text(pairs, failures),
                run_id=run_id,
                loop=loop,
                status=status,
                extras={"pages": len(pairs), "failures": failures},
            )
        )
        return pairs, failures


def run_writer_stage(
    brief: str,
    *,
    loop: int,
    pairs: list[SearchPair],
    evidence: list[IcdEvidenceNote],
    run_id: str,
    stage_answers: list[AgentAnswer],
) -> list[IcdEvidenceNote]:
    """Write evidence notes and emit a next-agent answer."""
    with trace_span("stage", "writer"):
        notes = write_icd_evidence_notes(pairs)
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
    evidence: list[IcdEvidenceNote],
    failures: list[str],
    run_id: str,
    diary: list[DiaryEntry],
    stage_answers: list[AgentAnswer],
) -> DiaryEntry:
    """Evaluate the loop and emit a next-agent answer."""
    with trace_span("stage", "evaluator"):
        entry = evaluate_icd_loop(
            brief, loop=loop, evidence=evidence, failures=failures
        )
        write_diary(entry, name_prefix=f"{run_id}/icd")
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
