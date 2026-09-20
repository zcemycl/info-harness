"""Sole CLI entry — registers commands from `cli/`."""

import typer

from cli.agent import app as agent_app
from cli.cognito_login import cognito_login
from cli.diary import app as diary_app
from cli.http import app as http_app

app = typer.Typer(
    name="main",
    help="info-harness",
    add_completion=True,
    no_args_is_help=True,
)

app.command("cognito-login")(cognito_login)
app.add_typer(diary_app, name="diary")
app.add_typer(http_app, name="http")
app.add_typer(agent_app, name="agent")

if __name__ == "__main__":
    app()
