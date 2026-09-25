import type { RunEvent } from "@/types";
import { activeStepId, groupLoops, loopExpanded, type LoopBlock, type RunStep } from "./groupLoops";

type StreamThreadsProps = {
  events: RunEvent[];
  settled: boolean;
  openLoops: Readonly<Record<string, boolean>>;
  openSteps: Readonly<Record<string, boolean>>;
  onToggleLoop: (id: string) => void;
  onToggleStep: (id: string) => void;
};

function StepRow({ step, open, onToggle }: { step: RunStep; open: boolean; onToggle: (id: string) => void }) {
  return (
    <div>
      <button type="button" className="flex w-full items-center gap-2 text-left text-sm text-[#0c1f1a]" onClick={() => onToggle(step.id)}>
        <span style={{ color: step.accent }}>{open ? "▾" : "▸"}</span>
        <span className="font-semibold">{step.title}</span>
        <span className="truncate text-xs text-[#5a7a6c]">{step.meta}</span>
      </button>
      {open ? <p className="mt-1 pl-5 text-xs leading-5 text-[#24352e]">{step.detail}</p> : null}
    </div>
  );
}

function LoopThread({
  loop,
  active,
  openLoops,
  openSteps,
  onToggleLoop,
  onToggleStep,
}: {
  loop: LoopBlock;
  active: string;
  openLoops: Readonly<Record<string, boolean>>;
  openSteps: Readonly<Record<string, boolean>>;
  onToggleLoop: (id: string) => void;
  onToggleStep: (id: string) => void;
}) {
  const open = loopExpanded(loop, openLoops);
  const tight = loop.tier === "inner";
  return (
    <li className={tight ? "my-1" : "my-2"}>
      <button
        type="button"
        className={`flex w-full items-center gap-2 rounded-lg border border-[#d9cbb3] bg-white text-left ${tight ? "px-2 py-0.5 text-[11px]" : "px-2 py-1.5 text-sm"}`}
        onClick={() => onToggleLoop(loop.id)}
      >
        <span>{open ? "▾" : "▸"}</span>
        <span className="font-semibold">
          {loop.tier} · {loop.domain} · loop {loop.loop}
        </span>
        {loop.ended ? <span className="text-[#5a7a6c]">done</span> : loop.steps.some((step) => step.running) ? (
          <span className="text-[#8a5a12]">running</span>
        ) : null}
      </button>
      {open ? (
        <ul className={`space-y-1 border-l border-[#d9cbb3] pl-3 ${tight ? "mt-1" : "mt-2"}`}>
          {loop.steps.map((step) => (
            <li key={step.id}>
              <StepRow step={step} open={openSteps[step.id] ?? step.id === active} onToggle={onToggleStep} />
              {step.stage === "executor" ? (
                <ul className="mt-1 space-y-1 border-l border-[#8aa396] pl-3">
                  {loop.workers.map((worker) => (
                    <li key={worker.id}>
                      <StepRow step={worker} open={openSteps[worker.id] ?? false} onToggle={onToggleStep} />
                    </li>
                  ))}
                  {loop.inners.map((inner) => (
                    <LoopThread
                      key={inner.id}
                      loop={inner}
                      active={active}
                      openLoops={openLoops}
                      openSteps={openSteps}
                      onToggleLoop={onToggleLoop}
                      onToggleStep={onToggleStep}
                    />
                  ))}
                </ul>
              ) : null}
            </li>
          ))}
          {loop.steps.some((step) => step.stage === "executor") ? null : (
            <>
              {loop.workers.map((worker) => (
                <li key={worker.id}>
                  <StepRow step={worker} open={openSteps[worker.id] ?? false} onToggle={onToggleStep} />
                </li>
              ))}
              {loop.inners.map((inner) => (
                <LoopThread
                  key={inner.id}
                  loop={inner}
                  active={active}
                  openLoops={openLoops}
                  openSteps={openSteps}
                  onToggleLoop={onToggleLoop}
                  onToggleStep={onToggleStep}
                />
              ))}
            </>
          )}
        </ul>
      ) : null}
    </li>
  );
}

export function StreamThreads({ events, settled, openLoops, openSteps, onToggleLoop, onToggleStep }: StreamThreadsProps) {
  const loops = groupLoops(events, settled);
  const active = activeStepId(loops, openLoops);
  return (
    <div className="h-80 overflow-auto rounded-lg border border-[#0c1f1a]/10 bg-[#fbfaf6] p-2" aria-label="Streaming threads">
      <ul>
        {loops.map((loop) => (
          <LoopThread
            key={loop.id}
            loop={loop}
            active={active}
            openLoops={openLoops}
            openSteps={openSteps}
            onToggleLoop={onToggleLoop}
            onToggleStep={onToggleStep}
          />
        ))}
      </ul>
    </div>
  );
}
