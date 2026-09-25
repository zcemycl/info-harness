"""Schema loop parses JSON after optional diary reads."""

from langchain_core.messages import AIMessage
from pydantic import BaseModel

from agents.invoke_schema_with_reader import invoke_schema_with_reader


class _Out(BaseModel):
    name: str


class _LLM:
    def bind_tools(self, _tools: object) -> "_LLM":
        return self

    def invoke(self, _messages: object) -> AIMessage:
        return AIMessage(content='{"name": "abacavir"}')


def test_schema_reader_parses_final_json() -> None:
    parsed = invoke_schema_with_reader(
        _LLM(),
        _Out,
        system="plan",
        user="brief",
    )
    assert parsed.name == "abacavir"
