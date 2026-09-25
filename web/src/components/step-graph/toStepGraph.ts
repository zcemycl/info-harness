import type { RunEvent } from "@/types";
import { activeStepId, groupLoops, loopExpanded, type LoopBlock, type RunStep } from "./groupLoops";

export type StepCard = RunStep & { expanded: boolean; comboId: string; compact?: boolean };

export type LoopCombo = {
  id: string;
  parent?: string;
  label: string;
  collapsed: boolean;
  tier: "outer" | "inner";
  accent: string;
};

export type StepGraphModel = {
  cards: StepCard[];
  edges: { id: string; source: string; target: string }[];
  combos: LoopCombo[];
};

function pushLoop(
  loop: LoopBlock,
  parent: string | undefined,
  openSteps: Readonly<Record<string, boolean>>,
  openLoops: Readonly<Record<string, boolean>>,
  active: string,
  model: StepGraphModel,
): string {
  const expanded = loopExpanded(loop, openLoops);
  const accent = loop.steps[0]?.accent ?? "#3d5a50";
  const label = `${loop.tier} · ${loop.domain} · loop ${loop.loop}`;
  if (!expanded) {
    model.cards.push({
      id: loop.id,
      tier: loop.tier,
      domain: loop.domain,
      stage: null,
      loop: loop.loop,
      title: label,
      meta: loop.ended ? "done" : "open",
      detail: "",
      accent,
      running: false,
      expanded: false,
      compact: loop.tier === "inner",
      comboId: parent ?? "",
    });
    return loop.id;
  }
  const box = `box-${loop.id}`;
  model.combos.push({ id: box, parent, label, collapsed: false, tier: loop.tier, accent });
  let spine: string | null = null;
  for (const name of ["planner", "executor", "writer", "evaluator"]) {
    const step = loop.steps.find((item) => item.stage === name);
    if (!step) continue;
    model.cards.push({ ...step, comboId: box, expanded: openSteps[step.id] ?? step.id === active });
    if (spine) model.edges.push({ id: `${spine}-${step.id}`, source: spine, target: step.id });
    spine = step.id;
  }
  const executor = loop.steps.find((step) => step.stage === "executor");
  const writer = loop.steps.find((step) => step.stage === "writer");
  const branches: string[] = [];
  for (const worker of loop.workers) {
    model.cards.push({ ...worker, comboId: box, expanded: openSteps[worker.id] ?? worker.id === active });
    branches.push(worker.id);
  }
  for (const inner of loop.inners) branches.push(pushLoop(inner, box, openSteps, openLoops, active, model));
  for (const branch of branches) {
    if (executor) model.edges.push({ id: `${executor.id}-${branch}`, source: executor.id, target: branch });
    if (writer) model.edges.push({ id: `${branch}-${writer.id}`, source: branch, target: writer.id });
  }
  return box;
}

export function toStepGraph(
  events: RunEvent[],
  openSteps: Readonly<Record<string, boolean>>,
  openLoops: Readonly<Record<string, boolean>>,
  settled: boolean,
): StepGraphModel {
  const loops = groupLoops(events, settled);
  const model: StepGraphModel = { cards: [], edges: [], combos: [] };
  const active = activeStepId(loops, openLoops);
  let previousOuter: string | null = null;
  for (const loop of loops) {
    const visible = pushLoop(loop, undefined, openSteps, openLoops, active, model);
    if (previousOuter) model.edges.push({ id: `${previousOuter}-${visible}`, source: previousOuter, target: visible });
    previousOuter = visible;
  }
  return model;
}
