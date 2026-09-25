"""Store the final research answer for a run."""

from __future__ import annotations

import json

from tools.chat.object_key import object_key
from tools.chat.object_store import open_object_store
from tools.chat.utc_now import utc_now


def put_run_result(
    chat_id: str,
    run_id: str,
    *,
    answer: str,
    loops: int,
) -> None:
    """Write ``result.json`` for ``GET /runs/{id}``."""
    payload = {
        "chat_id": chat_id,
        "run_id": run_id,
        "answer": answer,
        "loops": loops,
        "updated_at": utc_now(),
    }
    open_object_store().put_text(
        object_key("result", chat_id=chat_id, run_id=run_id),
        json.dumps(payload),
    )
