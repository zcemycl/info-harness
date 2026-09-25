"""Lambda entry: HTTP via Mangum, or an async research invocation."""

from __future__ import annotations

from typing import Any

from mangum import Mangum

from api.app import app
from pipeline.run_chat_turn import run_chat_turn

_asgi = Mangum(app, lifespan="off")


def handler(event: dict[str, Any], context: Any) -> Any:
    """Serve FastAPI, or run one chat turn when ``action`` is ``research``.

    The CLI stays ``src/main.py``. On Lambda, ``POST /messages`` invokes this
    function asynchronously so the HTTP response returns a ``run_id`` while
    PEWE continues (up to the function timeout).
    """
    if event.get("action") == "research":
        run_chat_turn(
            str(event["chat_id"]),
            str(event["run_id"]),
            str(event["brief"]),
            access_token=str(event.get("access_token") or "") or None,
        )
        return {"ok": True}
    return _asgi(event, context)
