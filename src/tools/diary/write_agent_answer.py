"""Persist an AgentAnswer under the diary tree."""

from __future__ import annotations

from datetime import UTC, datetime
from pathlib import Path
from uuid import uuid4

from model.research.agent_answer import AgentAnswer
from tools.diary.default_diary_dir import DEFAULT_DIARY_DIR
from tools.diary.diary_folder import diary_folder


def write_agent_answer(
    entry: AgentAnswer,
    *,
    diary_dir: Path = DEFAULT_DIARY_DIR,
    name_prefix: str | None = None,
    filename_stem: str = "answer",
) -> AgentAnswer:
    """Write ``{stem}-<stamp>.json`` and return entry with ``path`` set."""
    root = diary_dir.expanduser().resolve()
    folder = diary_folder(root, name_prefix)
    folder.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now(UTC).strftime("%Y%m%dT%H%M%S")
    path = folder / f"{filename_stem}-{stamp}-{uuid4().hex[:8]}.json"
    written = entry.model_copy(
        update={"path": path.relative_to(Path.cwd().resolve()).as_posix()}
    )
    path.write_text(written.model_dump_json(indent=2) + "\n", encoding="utf-8")
    return written
