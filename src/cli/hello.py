"""Smoke-check that the CLI is wired."""

import typer


def hello() -> None:
    """Print a short readiness message."""
    typer.echo("info-harness ready")
