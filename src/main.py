"""Sole CLI entry — registers commands from `cli/`."""

import typer

from cli.cognito_login import cognito_login
from cli.hello import hello
from cli.tools import app as tools_app

app = typer.Typer(
    name="main",
    help="info-harness",
    add_completion=True,
    no_args_is_help=True,
)

app.command()(hello)
app.command("cognito-login")(cognito_login)
app.add_typer(tools_app, name="tools")

if __name__ == "__main__":
    app()
