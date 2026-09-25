"""Chats for one Cognito user are invisible to another."""

from __future__ import annotations

from pathlib import Path

import pytest

from tools.chat.bind_chat_owner import bind_chat_owner
from tools.chat.create_chat import create_chat
from tools.chat.list_chats import list_chats
from tools.chat.load_history import load_history


def test_other_account_cannot_see_chats(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("CHAT_DATA_DIR", str(tmp_path))
    monkeypatch.setenv("CHAT_S3_BUCKET", "")
    with bind_chat_owner("rocket8-sub"):
        created = create_chat()
        assert [item.chat_id for item in list_chats()] == [created.chat_id]
    with bind_chat_owner("rocket888-sub"):
        assert list_chats() == []
        assert load_history(created.chat_id) is None
