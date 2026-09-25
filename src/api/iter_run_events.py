"""Yield SSE lines for a run until the terminal event."""

from __future__ import annotations

import asyncio
from collections.abc import AsyncIterator

from tools.chat.load_run import load_run
from tools.chat.load_run_events import load_run_events


async def iter_run_events(run_id: str, after: int) -> AsyncIterator[str]:
    """Poll stored events and yield SSE ``data:`` lines."""
    cursor = after
    idle_polls = 0
    while idle_polls < 900:
        events = await asyncio.to_thread(load_run_events, run_id)
        progressed = False
        for event in events:
            if event.seq <= cursor:
                continue
            cursor = event.seq
            progressed = True
            yield f"data: {event.model_dump_json()}\n\n"
            if event.type in {"final", "error"}:
                return
        view = await asyncio.to_thread(load_run, run_id)
        if view and view.status in {"succeeded", "failed"} and not progressed:
            return
        if not progressed:
            yield ": ping\n\n"
            idle_polls += 1
        else:
            idle_polls = 0
        await asyncio.sleep(1)
