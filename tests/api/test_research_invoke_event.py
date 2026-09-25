"""Async research invoke is an HTTP event for the Web Adapter."""

from __future__ import annotations

import json

from api.research_invoke_event import research_invoke_event


def test_research_invoke_event_targets_internal_route() -> None:
    event = research_invoke_event("chat", "run", "the brief", "token")
    assert event["rawPath"] == "/internal/research"
    assert event["requestContext"]["http"]["method"] == "POST"
    assert event["headers"]["authorization"] == "Bearer token"
    assert json.loads(event["body"]) == {
        "chat_id": "chat",
        "run_id": "run",
        "brief": "the brief",
    }
