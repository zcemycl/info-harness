"""Thin CLI: run the CTG condition autocomplete worker."""

from __future__ import annotations

import typer

from agents.ctg_search_condition.run import run_ctg_search_condition
from cli.agent.echo_agent_answer import echo_agent_answer


def ctg_search_condition(
    brief: str = typer.Argument(..., help="User brief for the condition worker"),
    max_turns: int = typer.Option(8, "--max-turns"),
    run_id: str | None = typer.Option(None, "--run-id"),
) -> None:
    """Run CTG condition worker (search_ctg_condition; q% vs %q%)."""
    try:
        result = run_ctg_search_condition(brief, max_turns=max_turns, run_id=run_id)
    except (FileNotFoundError, RuntimeError, ValueError) as exc:
        typer.secho(str(exc), fg=typer.colors.RED, err=True)
        raise typer.Exit(code=1) from exc
    echo_agent_answer(result)
