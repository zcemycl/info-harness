"""Stage-answer JSON is readable in the same windows as evidence artifacts."""

from __future__ import annotations

import json
from pathlib import Path

from tools.diary.read_evidence_artifact import read_evidence_artifact


def test_read_stage_answer_window(tmp_path: Path) -> None:
    payload = {
        "agent": "fda_label_specialist",
        "status": "ok",
        "answer": "ABCDEFGHIJ",
        "path": "run/answer.json",
    }
    target = tmp_path / "run" / "answer.json"
    target.parent.mkdir(parents=True)
    target.write_text(json.dumps(payload), encoding="utf-8")
    window = read_evidence_artifact(
        "run/answer.json",
        offset=2,
        limit_chars=4,
        diary_dir=tmp_path,
    )
    assert window["text"] == "CDEF"
    assert window["meta"]["agent"] == "fda_label_specialist"
    assert window["next_offset"] == 6
    assert window["total_chars"] == 10
