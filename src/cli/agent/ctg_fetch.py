"""Thin CLI: run the CTG live NCT-id fetch worker."""

from __future__ import annotations

import typer

from agents.ctg_fetch.run import run_ctg_fetch
from cli.agent.echo_agent_answer import echo_agent_answer


def ctg_fetch(
    brief: str = typer.Argument(
        ..., help="User brief for the live NCT-id fetch worker"
    ),
    max_turns: int = typer.Option(8, "--max-turns"),
    run_id: str | None = typer.Option(None, "--run-id"),
) -> None:
    """Run live CT.gov fetch-by-NCT-id worker (sections + references)."""
    try:
        result = run_ctg_fetch(brief, max_turns=max_turns, run_id=run_id)
    except (FileNotFoundError, RuntimeError, ValueError) as exc:
        typer.secho(str(exc), fg=typer.colors.RED, err=True)
        raise typer.Exit(code=1) from exc
    echo_agent_answer(result)
