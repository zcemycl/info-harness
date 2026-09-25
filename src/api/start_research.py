"""Start research in-process locally, or as an async Lambda self-invoke."""

from __future__ import annotations

import json
import os
import threading

import boto3

from api.research_invoke_event import research_invoke_event
from pipeline.run_chat_turn import run_chat_turn
from tools.chat.put_run_status import put_run_status


def start_research(
    chat_id: str,
    run_id: str,
    brief: str,
    *,
    access_token: str,
) -> None:
    """Return quickly. CLI stays a separate sync entrypoint."""
    function_name = _function_name()
    if function_name and os.getenv("CHAT_INLINE_RESEARCH") != "1":
        _invoke(function_name, chat_id, run_id, brief, access_token)
        return
    threading.Thread(
        target=_guarded,
        kwargs={
            "chat_id": chat_id,
            "run_id": run_id,
            "brief": brief,
            "access_token": access_token,
        },
        daemon=True,
    ).start()


def _function_name() -> str:
    override = os.getenv("RESEARCH_FUNCTION_NAME", "").strip()
    if override:
        return override
    return os.getenv("AWS_LAMBDA_FUNCTION_NAME", "").strip()


def _invoke(
    function_name: str,
    chat_id: str,
    run_id: str,
    brief: str,
    access_token: str,
) -> None:
    payload = research_invoke_event(chat_id, run_id, brief, access_token)
    try:
        boto3.client("lambda").invoke(
            FunctionName=function_name,
            InvocationType="Event",
            Payload=json.dumps(payload).encode("utf-8"),
        )
    except Exception as exc:
        message = f"{type(exc).__name__}: {exc}"
        put_run_status(chat_id, run_id, "failed", error=message)
        raise


def _guarded(chat_id: str, run_id: str, brief: str, access_token: str) -> None:
    try:
        run_chat_turn(chat_id, run_id, brief, access_token=access_token)
    except Exception:
        return
