import type { RunEvent } from "@/types";

export async function readRunStream(response: Response, onEvent: (event: RunEvent) => void): Promise<void> {
  const reader = response.body?.getReader();
  if (!reader) return;
  const decoder = new TextDecoder();
  let buffer = "";
  while (true) {
    const { value, done } = await reader.read();
    if (done) return;
    buffer += decoder.decode(value, { stream: true });
    const frames = buffer.split("\n\n");
    buffer = frames.pop() ?? "";
    for (const frame of frames) {
      const line = frame.split("\n").find((item) => item.startsWith("data: "));
      if (!line) continue;
      const event = JSON.parse(line.slice(6)) as RunEvent;
      onEvent(event);
      if (event.type === "final" || event.type === "error") return;
    }
  }
}
