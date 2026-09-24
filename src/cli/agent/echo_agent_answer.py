"""Thin CLI helper: print an AgentAnswer for humans."""

from __future__ import annotations

import typer

from model.research.agent_answer import AgentAnswer


def echo_agent_answer(result: AgentAnswer) -> None:
    """Print answer text; path/status go to stderr for debugging."""
    header = (
        f"=== answer ({result.agent} / {result.audience.value} / "
        f"{result.status.value}) ==="
    )
    typer.secho(header, fg=typer.colors.CYAN, err=True)
    typer.echo(result.answer)
    if result.path:
        typer.secho(f"wrote {result.path}", fg=typer.colors.CYAN, err=True)
