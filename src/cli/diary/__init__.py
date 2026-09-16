"""Typer sub-app for research diary tools."""

import typer

from cli.diary.read import read
from cli.diary.write import write

app = typer.Typer(
    name="diary",
    help="Read and write structured research diary entries.",
    add_completion=False,
    no_args_is_help=True,
)

app.command("write")(write)
app.command("read")(read)
