"""Final research outer-loop result."""

from __future__ import annotations

from pydantic import BaseModel, Field

from model.research.agent_answer import AgentAnswer
from model.research.diary_entry import DiaryEntry
from model.research.research_eval_result import ResearchEvalResult
from model.research.research_memory import ResearchMemory
from model.research.research_pack import ResearchPack
from model.research.research_plan import ResearchPlan


class ResearchResult(BaseModel):
    """Outer research PEWE result for humans / CLI / eval."""

    answer: AgentAnswer = Field(description="Human-facing synthesized answer")
    stage_answers: list[AgentAnswer] = Field(default_factory=list)
    plan: ResearchPlan | None = None
    pack: ResearchPack = Field(default_factory=ResearchPack)
    diary: list[DiaryEntry] = Field(default_factory=list)
    evaluation: ResearchEvalResult | None = None
    memory: ResearchMemory = Field(default_factory=ResearchMemory)
    loops: int = Field(ge=0, description="Outer loops actually run")
    run_id: str
