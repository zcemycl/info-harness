"""Placeholder test — replace as features land."""


def test_echo_tool() -> None:
    from tools.echo import run_echo

    assert run_echo("ping") == "ping"
