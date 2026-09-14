"""Typer sub-app for invoking tools directly from the CLI."""

import typer

from cli.tools.echo import echo

app = typer.Typer(
    name="tools",
    help="Run project tools directly.",
    add_completion=False,
    no_args_is_help=True,
)

app.command("echo")(echo)
