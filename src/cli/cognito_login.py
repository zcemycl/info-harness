"""CLI: Cognito username/password login → JWT tokens."""

import typer

from tools.cognito_login import run_cognito_login
from tools.cognito_tokens_path import COGNITO_TOKENS_PATH


def cognito_login(
    username: str = typer.Option(..., "--username", "-u", help="Cognito username"),
    password: str = typer.Option(
        ...,
        "--password",
        "-p",
        prompt=True,
        hide_input=True,
        help="Cognito password",
    ),
) -> None:
    """Log in to Cognito, save JWTs to `.cognito_tokens.json`, and print them."""
    try:
        tokens = run_cognito_login(username, password)
    except (ValueError, RuntimeError) as exc:
        typer.secho(str(exc), fg=typer.colors.RED, err=True)
        raise typer.Exit(code=1) from exc

    typer.echo(f"saved={COGNITO_TOKENS_PATH.resolve()}")
    typer.echo(f"token_type={tokens.token_type or 'Bearer'}")
    if tokens.expires_in is not None:
        typer.echo(f"expires_in={tokens.expires_in}")
    typer.echo(f"id_token={tokens.id_token}")
    typer.echo(f"access_token={tokens.access_token}")
    if tokens.refresh_token:
        typer.echo(f"refresh_token={tokens.refresh_token}")
