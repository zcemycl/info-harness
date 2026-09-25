"""Turn briefs for follow-up research."""

from tools.chat.build_turn_brief import build_turn_brief


def test_first_turn_is_the_prompt() -> None:
    assert build_turn_brief(last_answer=None, prompt="  Keytruda indications  ") == (
        "Keytruda indications"
    )


def test_follow_up_includes_last_answer() -> None:
    brief = build_turn_brief(
        last_answer="Pembrolizumab is approved.", prompt="pivotal trials?"
    )
    assert "Pembrolizumab is approved." in brief
    assert "pivotal trials?" in brief
    assert brief.startswith("Prior research answer:")
