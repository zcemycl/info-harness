"""Lambda entry: HTTP via Mangum, or an async research invocation."""

from __future__ import annotations

from typing import Any

from mangum import Mangum

from api.app import app
from pipeline.run_chat_turn import run_chat_turn

_asgi = Mangum(app, lifespan="off")


def handler(event: dict[str, Any], context: Any) -> Any:
    """Serve FastAPI, or run one chat turn when ``action`` is ``research``.

    The CLI stays ``src/main.py``. The container entrypoint is uvicorn, so
    Lambda research runs ``POST /internal/research`` instead of this branch.
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
