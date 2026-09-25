"""Truncated evaluator output does not fail the research run."""

from unittest.mock import MagicMock

import pytest
from openai import LengthFinishReasonError

from agents.research.evaluate_loop import evaluate_research_loop
from model.research.diary_entry import DiaryDecision
from model.research.research_memory import ResearchMemory
from model.research.research_pack import ResearchPack
from model.research.research_plan import ResearchPlan


class _Limited:
    def bind_tools(self, _tools: object) -> "_Limited":
        return self

    def with_structured_output(self, _schema: object) -> "_Limited":
        return self

    def invoke(self, _messages: object) -> object:
        completion = MagicMock()
        completion.usage = None
        raise LengthFinishReasonError(completion=completion)


def test_length_limit_continues(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(
        "agents.research.evaluate_loop.chat_model",
        lambda **_kwargs: _Limited(),
    )
    result = evaluate_research_loop(
        "brief",
        loop=2,
        plan=ResearchPlan(rationale="because"),
        pack=ResearchPack(),
        answer_text="synthesis",
        memory=ResearchMemory(),
    )
    assert result.decision is DiaryDecision.CONTINUE
    assert result.loop == 2
