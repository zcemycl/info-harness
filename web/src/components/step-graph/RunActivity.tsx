import { useEffect, useState } from "react";
import type { RunEvent } from "@/types";
import { activeStepId, findLoop, groupLoops, loopExpanded } from "./groupLoops";
import { StepGraph } from "./StepGraph";
import { StreamThreads } from "./StreamThreads";

export function RunActivity({ events, settled }: { events: RunEvent[]; settled: boolean }) {
  const [panelOpen, setPanelOpen] = useState(true);
  const [openLoops, setOpenLoops] = useState<Record<string, boolean>>({});
  const [openSteps, setOpenSteps] = useState<Record<string, boolean>>({});

  useEffect(() => {
    setPanelOpen(!settled);
  }, [settled]);

  const show = !settled || panelOpen;
  const loops = groupLoops(events, settled);

  function toggleLoop(id: string) {
    const found = findLoop(loops, id);
    const wasOpen = found ? loopExpanded(found, openLoops) : false;
    setOpenLoops((current) => ({ ...current, [id]: !wasOpen }));
  }

  function toggleStep(id: string) {
    const active = activeStepId(loops, openLoops);
    setOpenSteps((current) => {
      const wasOpen = id in current ? current[id] : id === active;
      return { ...current, [id]: !wasOpen };
    });
  }

  return (
    <section className="mt-3">
      <button
        type="button"
        className="flex items-center gap-2 text-left text-sm font-medium text-[#0c1f1a]"
        onClick={() => {
          if (settled) setPanelOpen((open) => !open);
        }}
      >
        <span>{show ? "▾" : "▸"}</span>
        {settled ? "Streams and graph" : "Streaming"}
      </button>
      {show ? (
        <div className="mt-2 grid items-start gap-2 md:grid-cols-2">
          <StreamThreads
            events={events}
            settled={settled}
            openLoops={openLoops}
            openSteps={openSteps}
            onToggleLoop={toggleLoop}
            onToggleStep={toggleStep}
          />
          <StepGraph
            events={events}
            settled={settled}
            openLoops={openLoops}
            openSteps={openSteps}
            onToggleLoop={toggleLoop}
            onToggleStep={toggleStep}
          />
        </div>
      ) : null}
    </section>
  );
}
