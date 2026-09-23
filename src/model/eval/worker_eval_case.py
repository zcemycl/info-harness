"""Worker eval case: brief + deterministic fixture expectations."""

from __future__ import annotations

from pydantic import BaseModel, Field

from model.eval.eval_worker_name import EvalWorkerName


class WorkerEvalCase(BaseModel):
    """One axis-worker benchmark case (FDA or CTG)."""

    id: str = Field(description="Stable case id (filename stem)")
    brief: str
    worker: EvalWorkerName
    tags: list[str] = Field(default_factory=list)
    source_run_id: str | None = Field(
        default=None, description="Diary run id used to curate GT"
    )
    pass_threshold: float | None = Field(
        default=None, description="Override FDA_EVAL_PASS_THRESHOLD"
    )
    status_in: list[str] = Field(default_factory=lambda: ["ok"])
    must_include: list[str] = Field(default_factory=list)
    must_not_include: list[str] = Field(default_factory=list)
    expected_tools_any: list[str] = Field(
        default_factory=list,
        description="At least one of these tools must have been called",
    )
    expected_tools_all: list[str] = Field(
        default_factory=list,
        description="Every listed tool must have been called",
    )
    min_answer_chars: int = Field(default=40, ge=0)
