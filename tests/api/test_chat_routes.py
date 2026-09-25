"""Chat API using a local directory instead of S3."""

from __future__ import annotations

from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from api.app import app
from api.require_access_token import require_access_token


def test_chat_message_stores_follow_up_brief(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("CHAT_DATA_DIR", str(tmp_path))
    monkeypatch.setenv("CHAT_S3_BUCKET", "")
    monkeypatch.setenv("RESEARCH_FUNCTION_NAME", "")
    monkeypatch.setenv("AWS_LAMBDA_FUNCTION_NAME", "")
    started: dict[str, str] = {}

    def fake_start(
        chat_id: str,
        run_id: str,
        brief: str,
        *,
        access_token: str,
    ) -> None:
        started["chat_id"] = chat_id
        started["run_id"] = run_id
        started["brief"] = brief
        started["token"] = access_token

    monkeypatch.setattr("api.routes.post_message.start_research", fake_start)
    app.dependency_overrides[require_access_token] = lambda: "test-token"
    client = TestClient(app)
    created = client.post("/chats")
    assert created.status_code == 200
    chat_id = created.json()["chat_id"]

    first = client.post(
        f"/chats/{chat_id}/messages", json={"prompt": "Keytruda indications"}
    )
    assert first.status_code == 200
    assert started["brief"] == "Keytruda indications"

    history_path = tmp_path / "chats" / chat_id / "history.json"
    history_path.write_text(
        '{"messages": ['
        '{"role": "user", "content": "Keytruda indications",'
        ' "ts": "t", "run_id": null},'
        '{"role": "assistant", "content": "Approved for melanoma.",'
        ' "ts": "t", "run_id": "r1"}'
        "]}",
        encoding="utf-8",
    )
    second = client.post(
        f"/chats/{chat_id}/messages",
        json={"prompt": "What pivotal trials?"},
    )
    assert second.status_code == 200
    assert "Approved for melanoma." in started["brief"]
    assert "What pivotal trials?" in started["brief"]
    view = client.get(f"/runs/{second.json()['run_id']}")
    assert view.status_code == 200
    assert view.json()["status"] == "running"
    assert started["token"] == "test-token"
    app.dependency_overrides.clear()


def test_delete_chat_removes_the_session(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("CHAT_DATA_DIR", str(tmp_path))
    monkeypatch.setenv("CHAT_S3_BUCKET", "")
    app.dependency_overrides[require_access_token] = lambda: "test-token"
    client = TestClient(app)
    created = client.post("/chats")
    chat_id = created.json()["chat_id"]
    removed = client.delete(f"/chats/{chat_id}")
    assert removed.status_code == 204
    assert client.get(f"/chats/{chat_id}").status_code == 404
    app.dependency_overrides.clear()


def test_chat_routes_require_cognito(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("CHAT_DATA_DIR", str(tmp_path))
    monkeypatch.setenv("CHAT_S3_BUCKET", "")
    app.dependency_overrides.clear()
    client = TestClient(app)
    assert client.get("/health").status_code == 200
    assert client.get("/chats").status_code == 401
