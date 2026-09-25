import { apiFetch, streamFetch } from "@/api/client";
import type { RunEvent, RunView } from "@/types";
import { readRunStream } from "./readRunStream";

export async function followRun(token: string, runId: string, onEvent: (event: RunEvent) => void): Promise<void> {
  let finished = false;
  const track = (event: RunEvent) => {
    onEvent(event);
    if (event.type === "final" || event.type === "error") finished = true;
  };
  const stream = await streamFetch(token, `/runs/${runId}/events/stream`);
  if (stream.ok && stream.body) {
    try {
      await readRunStream(stream, track);
    } catch {
      // A broken stream falls through to REST polling.
    }
    if (finished) return;
  }
  let after = 0;
  for (let attempt = 0; attempt < 900; attempt += 1) {
    const polled = await apiFetch(token, `/runs/${runId}/events?after=${after}`);
    if (polled.ok) {
      const events = (await polled.json()) as RunEvent[];
      for (const event of events) {
        after = Math.max(after, event.seq);
        track(event);
        if (finished) return;
      }
    }
    const viewResponse = await apiFetch(token, `/runs/${runId}`);
    if (viewResponse.ok) {
      const view = (await viewResponse.json()) as RunView;
      if (view.status === "succeeded" || view.status === "failed") {
        track({
          seq: after,
          type: view.status === "failed" ? "error" : "final",
          answer: view.answer,
          summary: view.error ?? "",
        });
        return;
      }
    }
    await new Promise((resolve) => window.setTimeout(resolve, 1000));
  }
}
