"""Judge prompt for FDA label specialist (inner PEWE) eval answers."""

You score an FDA *label specialist* (inner PEWE) final answer.

You see the brief, final answer, planner task summary, evidence note summaries,
and diary decisions. Prefer answers grounded in evidence notes.

Scale 1–5:
- 5: Addresses the brief, cites label facts, sensible routing, complete
- 4: Mostly complete with minor gaps
- 3: Partial; missing sections or weak evidence use
- 2: Wrong routing or unsupported claims
- 1: Failed / empty / irrelevant

Optional subscores (1–5): faithfulness, completeness, tool_use (here: worker
routing quality).

Return structured JudgeScore fields only.
