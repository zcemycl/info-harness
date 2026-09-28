"""GET /billing/me reports the backend run cap."""

from __future__ import annotations

import pytest
from fastapi.testclient import TestClient

from api.app import app
from api.require_access_token import ChatCaller, require_access_token


def test_open_mode_has_no_run_limit(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("BILLING_MODE", "open")
    app.dependency_overrides[require_access_token] = lambda: ChatCaller("token", "user")
    body = TestClient(app).get("/billing/me").json()
    app.dependency_overrides.clear()
    assert body["mode"] == "open"
    assert body["runs_limit"] is None


def test_table_mode_returns_the_configured_cap(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("BILLING_MODE", "table")
    monkeypatch.setenv("FREE_RESEARCH_RUNS", "5")
    app.dependency_overrides[require_access_token] = lambda: ChatCaller("token", "user")
    body = TestClient(app).get("/billing/me").json()
    app.dependency_overrides.clear()
    assert body["mode"] == "table"
    assert body["plan"] == "free"
    assert body["runs_limit"] == 5
    assert body["runs_used"] == 0
