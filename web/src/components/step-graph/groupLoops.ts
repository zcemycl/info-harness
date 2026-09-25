import type { RunEvent } from "@/types";

export type RunTier = "outer" | "inner" | "worker";

export type RunStep = {
  id: string;
  tier: RunTier;
  domain: string;
  stage: string | null;
  loop: number | null;
  title: string;
  meta: string;
  detail: string;
  accent: string;
};

export type LoopBlock = {
  id: string;
  tier: "outer" | "inner";
  domain: string;
  loop: number;
  ended: boolean;
  steps: RunStep[];
  inners: LoopBlock[];
};

const INNER = new Set(["fda", "ctg", "pubmed", "icd"]);
const PEWE = new Set(["planner", "executor", "writer", "evaluator"]);

const ACCENT: Record<string, string> = {
  research: "#0c1f1a",
  fda: "#1d4e89",
  ctg: "#0f6e6e",
  pubmed: "#5b3d8c",
  icd: "#8a5a12",
};

function hostDomain(name: string): string | null {
  if (name.startsWith("fda")) return "fda";
  if (name.startsWith("ctg")) return "ctg";
  if (name.startsWith("pubmed")) return "pubmed";
  if (name.startsWith("icd")) return "icd";
  return null;
}

function pretty(value: string): string {
  return value.replaceAll("_", " ");
}

function pathBody(path: string | null | undefined): string[] {
  if (!path) return [];
  const parts = path.split("/").filter(Boolean);
  const diary = parts.indexOf("diary");
  const rest = diary >= 0 ? parts.slice(diary + 2) : parts;
  return rest.at(-1)?.endsWith(".json") ? rest.slice(0, -1) : rest;
}

function inferred(event: RunEvent): { tier: RunTier; domain: string; stage: string | null; loop: number | null } {
  if (event.tier === "outer" || event.tier === "inner" || event.tier === "worker") {
    return {
      tier: event.tier,
      domain: event.domain?.trim() || event.agent?.trim() || "step",
      stage: event.stage ?? null,
      loop: event.loop ?? null,
    };
  }
  const body = pathBody(event.path);
  const agent = event.agent?.trim() || "step";
  const stage = body.length >= 3 && body[1]?.startsWith("loop-") ? body[2] : PEWE.has(agent) ? agent : null;
  const domain = body[0] || agent;
  const loop = body[1]?.startsWith("loop-") ? Number(body[1].slice(5)) || event.loop || null : event.loop ?? null;
  if (domain === "research" || agent === "research") return { tier: "outer", domain: "research", stage, loop };
  if (INNER.has(domain)) return { tier: "inner", domain, stage, loop };
  return { tier: "worker", domain, stage: null, loop };
}

function toStep(event: RunEvent): RunStep | null {
  if (event.type !== "stage" && event.type !== "error") return null;
  const scope = inferred(event);
  const stage = scope.stage && PEWE.has(scope.stage) ? scope.stage : scope.tier === "worker" ? null : scope.stage;
  const title = stage ? pretty(stage) : scope.tier === "worker" ? pretty(scope.domain) : "answer";
  const status = event.status || event.type;
  return {
    id: `s${event.seq}`,
    tier: scope.tier,
    domain: scope.domain,
    stage,
    loop: scope.loop,
    title,
    meta: `${scope.tier} · ${status}`,
    detail: (event.summary || event.answer || "").trim() || "No details yet.",
    accent: event.type === "error" ? "#b42318" : (ACCENT[scope.domain] ?? ACCENT[hostDomain(scope.domain) ?? ""] ?? "#3d5a50"),
  };
}

function block(tier: "outer" | "inner", domain: string, loop: number): LoopBlock {
  return { id: `loop-${tier}-${domain}-${loop}`, tier, domain, loop, ended: false, steps: [], inners: [] };
}

function hostInner(inners: LoopBlock[], domain: string): LoopBlock | undefined {
  const matches = inners.filter((item) => item.domain === domain);
  for (let index = matches.length - 1; index >= 0; index -= 1) {
    if (!matches[index]?.ended) return matches[index];
  }
  return matches.at(-1);
}

export function groupLoops(events: RunEvent[], forceEnded = false): LoopBlock[] {
  const outers: LoopBlock[] = [];
  const inners: LoopBlock[] = [];
  let current: LoopBlock | undefined;
  for (const event of events) {
    const step = toStep(event);
    if (!step) continue;
    if (step.tier === "worker") {
      const host = hostInner(inners, hostDomain(step.domain) ?? "") ?? current;
      host?.steps.push(step);
      continue;
    }
    const loop = step.loop ?? 1;
    const list = step.tier === "outer" ? outers : inners;
    let group = list.find((item) => item.domain === step.domain && item.loop === loop);
    if (!group) {
      group = block(step.tier === "inner" ? "inner" : "outer", step.domain, loop);
      list.push(group);
      if (group.tier === "inner") (current ?? outers.at(-1))?.inners.push(group);
      else current = group;
    }
    if (group.tier === "outer") current = group;
    group.steps.push(step);
    if (step.stage === "evaluator") group.ended = true;
  }
  if (forceEnded) {
    for (const outer of outers) {
      outer.ended = true;
      for (const inner of outer.inners) inner.ended = true;
    }
  }
  return outers;
}

export function findLoop(loops: LoopBlock[], id: string): LoopBlock | undefined {
  for (const loop of loops) {
    if (loop.id === id) return loop;
    const inner = findLoop(loop.inners, id);
    if (inner) return inner;
  }
  return undefined;
}

export function loopExpanded(loop: LoopBlock, open: Readonly<Record<string, boolean>>): boolean {
  if (loop.id in open) return open[loop.id] === true;
  return !loop.ended;
}

export function activeStepId(loops: LoopBlock[], openLoops: Readonly<Record<string, boolean>>): string {
  let latest = "";
  const visit = (loop: LoopBlock) => {
    if (!loopExpanded(loop, openLoops)) return;
    const last = loop.steps.at(-1);
    if (last && !loop.ended) latest = last.id;
    for (const inner of loop.inners) visit(inner);
  };
  for (const loop of loops) visit(loop);
  return latest;
}
