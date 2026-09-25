"""Read stage events for a run."""

from __future__ import annotations

from model.chat.run_event import RunEvent
from tools.chat.chat_id_for_run import chat_id_for_run
from tools.chat.object_key import object_key
from tools.chat.object_store import open_object_store


def load_run_events(run_id: str) -> list[RunEvent]:
    """Return events in ``seq`` order. Empty when the run is unknown."""
    chat_id = chat_id_for_run(run_id)
    if chat_id is None:
        return []
    raw = open_object_store().get_text(
        object_key("events", chat_id=chat_id, run_id=run_id)
    )
    if not raw:
        return []
    return [
        RunEvent.model_validate_json(line) for line in raw.splitlines() if line.strip()
    ]
