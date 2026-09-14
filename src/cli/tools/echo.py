"""Thin CLI wrapper for the echo tool."""

import typer

from tools.echo import run_echo


def echo(message: str) -> None:
    """Echo a message via the tools layer."""
    typer.echo(run_echo(message))
