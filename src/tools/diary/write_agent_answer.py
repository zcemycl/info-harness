"""Persist an AgentAnswer under the diary tree."""

from __future__ import annotations

from datetime import UTC, datetime
from pathlib import Path
from uuid import uuid4

from model.research.agent_answer import AgentAnswer
from tools.diary.default_diary_dir import diary_root
from tools.diary.diary_folder import diary_folder
from tools.diary.relative_diary_path import relative_diary_path


def write_agent_answer(
    entry: AgentAnswer,
    *,
    diary_dir: Path | None = None,
    name_prefix: str | None = None,
    filename_stem: str = "answer",
) -> AgentAnswer:
    """Write ``{stem}-<stamp>.json`` and return entry with ``path`` set."""
    root = diary_root(diary_dir)
    folder = diary_folder(root, name_prefix)
    folder.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now(UTC).strftime("%Y%m%dT%H%M%S")
    path = folder / f"{filename_stem}-{stamp}-{uuid4().hex[:8]}.json"
    written = entry.model_copy(update={"path": relative_diary_path(path, root)})
    path.write_text(written.model_dump_json(indent=2) + "\n", encoding="utf-8")
    _notify_stage(written)
    return written


def _notify_stage(entry: AgentAnswer) -> None:
    """Push a stage event when a chat run bound a listener. CLI runs no-op."""
    from tools.chat.stage_events import notify_stage

    notify_stage(entry)
