"""Thin CLI: read a structured diary entry from disk."""

from __future__ import annotations

from pathlib import Path

import typer
from pydantic import ValidationError

from cli.http.dump_json import dump_json
from tools.diary.default_diary_dir import DEFAULT_DIARY_DIR
from tools.diary.read_diary import read_diary


def read(
    path: str = typer.Argument(..., help="Diary JSON path under diary-dir."),
    diary_dir: Path = typer.Option(
        DEFAULT_DIARY_DIR,
        "--diary-dir",
        help="Root directory for diary files.",
    ),
) -> None:
    """Load a diary file and print validated DiaryEntry JSON."""
    try:
        entry = read_diary(path, diary_dir=diary_dir)
    except (FileNotFoundError, ValidationError, ValueError, OSError) as exc:
        typer.secho(str(exc), fg=typer.colors.RED, err=True)
        raise typer.Exit(code=1) from exc
    typer.echo(dump_json(entry))
