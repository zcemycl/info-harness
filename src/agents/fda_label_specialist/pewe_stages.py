"""PEWE stage runners that always emit an AgentAnswer for the next stage."""

from __future__ import annotations

from typing import Any

from agents.fda_label_specialist.emit_stage_answer import emit_stage_answer
from agents.fda_label_specialist.evaluate_loop import evaluate_fda_loop
from agents.fda_label_specialist.execute_tasks import execute_fda_tasks
from agents.fda_label_specialist.expand_fda_section_table_triples import (
    expand_fda_section_table_triples,
)
from agents.fda_label_specialist.plan_tasks import plan_fda_tasks
from agents.fda_label_specialist.stage_answer_text import (
    evaluator_answer_text,
    executor_answer_text,
    planner_answer_text,
    writer_answer_text,
)
from agents.fda_label_specialist.write_notes import write_evidence_notes
from model.fda.fda_label_attr_page import FdaLabelAttrPage
from model.research.agent_answer import AgentAnswer, AnswerStatus
from model.research.diary_entry import DiaryEntry
from model.research.evidence_note import EvidenceNote
from model.research.planner_output import PlannerOutput
from model.research.worker_plan import FdaAttrName, WorkerPlan
from tools.diary.write_diary import write_diary
from tools.trace_call import trace_info, trace_span

PageTriple = tuple[WorkerPlan, FdaAttrName, FdaLabelAttrPage[Any]]


def run_planner_stage(
    brief: str,
    *,
    loop: int,
    diary: list[DiaryEntry],
    evidence: list[EvidenceNote],
    run_id: str,
    stage_answers: list[AgentAnswer],
) -> PlannerOutput:
    """Plan tasks and emit a next-agent answer."""
    with trace_span("stage", "planner"):
        planned = plan_fda_tasks(brief, loop=loop, diary=diary, evidence=evidence)
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
    tasks: list[WorkerPlan],
    run_id: str,
    stage_answers: list[AgentAnswer],
) -> tuple[list[PageTriple], list[str]]:
    """Execute tasks and emit a next-agent answer."""
    with trace_span("stage", "executor", tasks=len(tasks)):
        pairs, failures = execute_fda_tasks(tasks)
        pairs, expand_failures = expand_fda_section_table_triples(pairs)
        failures = [*failures, *expand_failures]
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
    pairs: list[PageTriple],
    evidence: list[EvidenceNote],
    run_id: str,
    stage_answers: list[AgentAnswer],
) -> list[EvidenceNote]:
    """Write evidence notes and emit a next-agent answer."""
    with trace_span("stage", "writer"):
        notes = write_evidence_notes(pairs, run_id=run_id)
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
    evidence: list[EvidenceNote],
    failures: list[str],
    run_id: str,
    diary: list[DiaryEntry],
    stage_answers: list[AgentAnswer],
) -> DiaryEntry:
    """Evaluate the loop and emit a next-agent answer."""
    with trace_span("stage", "evaluator"):
        entry = evaluate_fda_loop(
            brief, loop=loop, evidence=evidence, failures=failures
        )
        write_diary(entry, name_prefix=f"{run_id}/fda")
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
