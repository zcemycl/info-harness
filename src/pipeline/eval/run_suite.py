"""Run an eval suite and write reports under data/eval/."""

from __future__ import annotations

import json
import uuid
from pathlib import Path

from model.eval.eval_case_report import EvalCaseReport
from model.eval.eval_layer import EvalLayer
from pipeline.eval.list_cases import list_eval_case_ids
from pipeline.eval.run_case import run_eval_case

_DATA_EVAL = Path(__file__).resolve().parents[3] / "data" / "eval"


def run_eval_suite(
    layers: list[EvalLayer],
    *,
    case_id: str | None = None,
    use_judge: bool = True,
    suite_id: str | None = None,
) -> list[EvalCaseReport]:
    """Run selected cases; persist summary JSON; return reports."""
    sid = suite_id or uuid.uuid4().hex[:12]
    out_dir = _DATA_EVAL / sid
    out_dir.mkdir(parents=True, exist_ok=True)
    reports: list[EvalCaseReport] = []
    for layer in layers:
        ids = [case_id] if case_id else list_eval_case_ids(layer)
        for cid in ids:
            if case_id and cid not in list_eval_case_ids(layer):
                continue
            report = run_eval_case(layer, cid, use_judge=use_judge)
            reports.append(report)
            (out_dir / f"{layer.value}_{cid}.json").write_text(
                report.model_dump_json(indent=2), encoding="utf-8"
            )
    summary = {
        "suite_id": sid,
        "passed": sum(1 for r in reports if r.passed),
        "total": len(reports),
        "cases": [r.model_dump(mode="json") for r in reports],
    }
    (out_dir / "summary.json").write_text(
        json.dumps(summary, indent=2), encoding="utf-8"
    )
    return reports
