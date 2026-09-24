"""Thin CLI: run the CTG resolve_trial worker."""

from __future__ import annotations

import typer

from agents.ctg_resolve_trial.run import run_ctg_resolve_trial
from cli.agent.echo_agent_answer import echo_agent_answer


def ctg_resolve_trial(
    brief: str = typer.Argument(..., help="User brief for resolve_trial worker"),
    max_turns: int = typer.Option(8, "--max-turns"),
    run_id: str | None = typer.Option(None, "--run-id"),
) -> None:
    """Resolve study name / protocol id to NCT (CT.gov + PubMed)."""
    try:
        result = run_ctg_resolve_trial(brief, max_turns=max_turns, run_id=run_id)
    except (FileNotFoundError, RuntimeError, ValueError) as exc:
        typer.secho(str(exc), fg=typer.colors.RED, err=True)
        raise typer.Exit(code=1) from exc
    echo_agent_answer(result)
