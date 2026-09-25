"""Writer continuations append when the model stops for length."""

from unittest.mock import MagicMock

from openai import LengthFinishReasonError

from agents.research.invoke_until_stop import invoke_until_stop


class _Reply:
    def __init__(self, content: str, finish_reason: str) -> None:
        self.content = content
        self.response_metadata = {"finish_reason": finish_reason}


class _Writer:
    def __init__(self) -> None:
        self.calls = 0

    def invoke(self, _messages: object) -> _Reply:
        self.calls += 1
        if self.calls == 1:
            return _Reply("First half", "length")
        return _Reply(" and the rest.", "stop")


def test_length_stop_requests_another_chunk() -> None:
    assert invoke_until_stop(_Writer(), [{"role": "user", "content": "go"}]) == (
        "First half and the rest."
    )


def test_length_exception_keeps_partial_text() -> None:
    completion = MagicMock()
    completion.usage = None
    completion.choices[0].message.content = "Partial table"

    class _Boom:
        def invoke(self, _messages: object) -> object:
            raise LengthFinishReasonError(completion=completion)

    assert invoke_until_stop(_Boom(), []) == "Partial table"
