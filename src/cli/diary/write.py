"""Thin CLI: write a structured diary entry from JSON."""

from __future__ import annotations

from pathlib import Path

import typer
from pydantic import ValidationError

from model.research.diary_entry import DiaryEntry
from tools.diary.default_diary_dir import DEFAULT_DIARY_DIR
from tools.diary.write_diary import write_diary


def write(
    entry_json: str = typer.Argument(
        ...,
        help="DiaryEntry JSON object (loop, decision, lists, ...).",
    ),
    diary_dir: Path = typer.Option(
        DEFAULT_DIARY_DIR,
        "--diary-dir",
        help="Root directory for diary files.",
    ),
    name_prefix: str | None = typer.Option(
        None,
        "--name-prefix",
        help="Optional subfolder under diary-dir, e.g. run-id/outer.",
    ),
) -> None:
    """Validate diary JSON, write a new file, print the relative path."""
    try:
        entry = DiaryEntry.model_validate_json(entry_json)
        path = write_diary(entry, diary_dir=diary_dir, name_prefix=name_prefix)
    except (ValidationError, ValueError, OSError) as exc:
        typer.secho(str(exc), fg=typer.colors.RED, err=True)
        raise typer.Exit(code=1) from exc
    typer.echo(path)
