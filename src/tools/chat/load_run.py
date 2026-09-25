"""Load run status and the final answer when present."""

from __future__ import annotations

import json

from model.chat.run_view import RunView
from tools.chat.chat_id_for_run import chat_id_for_run
from tools.chat.object_key import object_key
from tools.chat.object_store import open_object_store


def load_run(run_id: str) -> RunView | None:
    """Return a run view, or ``None`` when the run index is missing."""
    chat_id = chat_id_for_run(run_id)
    if chat_id is None:
        return None
    store = open_object_store()
    status_raw = store.get_text(object_key("run_index", run_id=run_id))
    if status_raw is None:
        return None
    status = json.loads(status_raw)
    result_raw = store.get_text(object_key("result", chat_id=chat_id, run_id=run_id))
    result = json.loads(result_raw) if result_raw else {}
    return RunView(
        chat_id=chat_id,
        run_id=run_id,
        status=str(status.get("status", "running")),
        brief=str(status.get("brief") or ""),
        answer=result.get("answer"),
        error=status.get("error"),
        loops=result.get("loops"),
    )
