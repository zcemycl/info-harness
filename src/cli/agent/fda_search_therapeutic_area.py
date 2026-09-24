"""Thin CLI: run the FDA therapeutic-area search worker."""

from __future__ import annotations

import typer

from agents.fda_search_therapeutic_area.run import run_fda_search_therapeutic_area
from cli.agent.echo_agent_answer import echo_agent_answer


def fda_search_therapeutic_area(
    brief: str = typer.Argument(..., help="User brief for the TA worker"),
    max_turns: int = typer.Option(8, "--max-turns"),
    run_id: str | None = typer.Option(None, "--run-id"),
) -> None:
    """Run search-by-therapeutic-area worker (per-attr FDA label tools)."""
    try:
        result = run_fda_search_therapeutic_area(
            brief, max_turns=max_turns, run_id=run_id
        )
    except (FileNotFoundError, RuntimeError, ValueError) as exc:
        typer.secho(str(exc), fg=typer.colors.RED, err=True)
        raise typer.Exit(code=1) from exc
    echo_agent_answer(result)
