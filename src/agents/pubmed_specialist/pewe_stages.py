"""PEWE stage runners for the PubMed specialist."""

from __future__ import annotations

from typing import Any

from agents.pubmed_specialist.emit_stage_answer import emit_stage_answer
from agents.pubmed_specialist.evaluate_loop import evaluate_pubmed_loop
from agents.pubmed_specialist.execute_tasks import execute_pubmed_tasks
from agents.pubmed_specialist.plan_tasks import plan_pubmed_tasks
from agents.pubmed_specialist.stage_answer_text import (
    evaluator_answer_text,
    executor_answer_text,
    planner_answer_text,
    writer_answer_text,
)
from agents.pubmed_specialist.write_notes import write_pubmed_evidence_notes
from model.pubmed.pubmed_attr_name import PubmedAttrName
from model.pubmed.pubmed_attr_page import PubmedAttrPage
from model.pubmed.pubmed_evidence_note import PubmedEvidenceNote
from model.pubmed.pubmed_planner_output import PubmedPlannerOutput
from model.pubmed.pubmed_worker_plan import PubmedWorkerPlan
from model.research.agent_answer import AgentAnswer, AnswerStatus
from model.research.diary_entry import DiaryEntry
from tools.diary.write_diary import write_diary
from tools.trace_call import trace_info, trace_span

IdTriple = tuple[PubmedWorkerPlan, PubmedAttrName, PubmedAttrPage[Any]]


def run_planner_stage(
    brief: str,
    *,
    loop: int,
    diary: list[DiaryEntry],
    evidence: list[PubmedEvidenceNote],
    run_id: str,
    stage_answers: list[AgentAnswer],
) -> PubmedPlannerOutput:
    """Plan PubMed tasks and emit a next-agent answer."""
    with trace_span("stage", "planner"):
        planned = plan_pubmed_tasks(brief, loop=loop, diary=diary, evidence=evidence)
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
    tasks: list[PubmedWorkerPlan],
    run_id: str,
    stage_answers: list[AgentAnswer],
) -> tuple[list[IdTriple], list[str]]:
    """Execute tasks and emit a next-agent answer."""
    with trace_span("stage", "executor", tasks=len(tasks)):
        triples, failures = execute_pubmed_tasks(tasks)
        if failures:
            trace_info("failures", count=len(failures))
        status = AnswerStatus.ERROR if failures and not triples else AnswerStatus.OK
        stage_answers.append(
            emit_stage_answer(
                agent="executor",
                brief=brief,
                answer=executor_answer_text(triples, failures),
                run_id=run_id,
                loop=loop,
                status=status,
                extras={
                    "id_pages": len(triples),
                    "failures": failures,
                },
            )
        )
        return triples, failures


def run_writer_stage(
    brief: str,
    *,
    loop: int,
    triples: list[IdTriple],
    evidence: list[PubmedEvidenceNote],
    run_id: str,
    stage_answers: list[AgentAnswer],
) -> list[PubmedEvidenceNote]:
    """Write evidence notes and emit a next-agent answer."""
    with trace_span("stage", "writer"):
        notes = write_pubmed_evidence_notes(triples)
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
    evidence: list[PubmedEvidenceNote],
    failures: list[str],
    run_id: str,
    diary: list[DiaryEntry],
    stage_answers: list[AgentAnswer],
) -> DiaryEntry:
    """Evaluate the loop and emit a next-agent answer."""
    with trace_span("stage", "evaluator"):
        entry = evaluate_pubmed_loop(
            brief, loop=loop, evidence=evidence, failures=failures
        )
        write_diary(entry, name_prefix=f"{run_id}/pubmed")
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
