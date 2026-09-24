"""Thin CLI: run the FDA setid search worker."""

from __future__ import annotations

import typer

from agents.fda_search_id.run import run_fda_search_id
from cli.agent.echo_agent_answer import echo_agent_answer


def fda_search_id(
    brief: str = typer.Argument(..., help="User brief for the setid worker"),
    max_turns: int = typer.Option(8, "--max-turns"),
    run_id: str | None = typer.Option(None, "--run-id"),
) -> None:
    """Run search-by-setid worker (per-attr FDA label tools)."""
    try:
        result = run_fda_search_id(brief, max_turns=max_turns, run_id=run_id)
    except (FileNotFoundError, RuntimeError, ValueError) as exc:
        typer.secho(str(exc), fg=typer.colors.RED, err=True)
        raise typer.Exit(code=1) from exc
    echo_agent_answer(result)
