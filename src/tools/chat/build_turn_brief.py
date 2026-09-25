"""Turn the last assistant answer plus a new prompt into a research brief."""

from __future__ import annotations


def build_turn_brief(*, last_answer: str | None, prompt: str) -> str:
    """First turn is the prompt. Later turns carry the prior answer as context."""
    question = prompt.strip()
    prior = (last_answer or "").strip()
    if not prior:
        return question
    return (
        "Prior research answer:\n"
        f"{prior}\n\n"
        "Follow-up question:\n"
        f"{question}\n\n"
        "Treat the follow-up as the new research brief. Use the prior answer "
        "as context; do not repeat it unless correcting or extending."
    )
