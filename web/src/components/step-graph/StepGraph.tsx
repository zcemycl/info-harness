import { useEffect, useRef } from "react";
import { Graph, type IPointerEvent } from "@antv/g6";
import type { RunEvent } from "@/types";
import { stepNodeShape } from "./stepNodeHtml";
import { toStepGraph } from "./toStepGraph";

type StepGraphProps = {
  events: RunEvent[];
  settled: boolean;
  openLoops: Readonly<Record<string, boolean>>;
  openSteps: Readonly<Record<string, boolean>>;
  onToggleLoop: (id: string) => void;
  onToggleStep: (id: string) => void;
};

export function StepGraph({ events, settled, openLoops, openSteps, onToggleLoop, onToggleStep }: StepGraphProps) {
  const containerRef = useRef<HTMLDivElement>(null);
  const graphRef = useRef<Graph | null>(null);
  const loopRef = useRef(onToggleLoop);
  const stepRef = useRef(onToggleStep);
  const fitted = useRef(0);
  loopRef.current = onToggleLoop;
  stepRef.current = onToggleStep;

  useEffect(() => {
    const container = containerRef.current;
    if (!container) return;
    const graph = new Graph({
      container,
      autoResize: true,
      zoomRange: [0.2, 2.5],
      layout: { type: "antv-dagre", rankdir: "LR", nodesep: 16, ranksep: 40 },
      node: { type: "html" },
      combo: { type: "rect" },
      edge: { type: "polyline", style: { stroke: "#8aa396", lineWidth: 1.5, endArrow: true, radius: 8 } },
      behaviors: ["drag-canvas", "zoom-canvas"],
    });
    graph.on("node:click", (event: IPointerEvent) => {
      const id = String((event.target as { id?: string })?.id ?? "");
      if (!id) return;
      if (id.startsWith("loop-")) loopRef.current(id);
      else stepRef.current(id);
    });
    graph.on("combo:click", (event: IPointerEvent) => {
      const id = String((event.target as { id?: string })?.id ?? "");
      const loopId = id.startsWith("box-") ? id.slice(4) : id;
      if (loopId.startsWith("loop-")) loopRef.current(loopId);
    });
    graphRef.current = graph;
    return () => {
      graph.destroy();
      graphRef.current = null;
      fitted.current = 0;
    };
  }, []);

  useEffect(() => {
    const graph = graphRef.current;
    if (!graph || graph.destroyed) return;
    const model = toStepGraph(events, openSteps, openLoops, settled);
    let cancelled = false;
    void graph
      .clear()
      .then(() => {
        if (cancelled || graph.destroyed) return;
        graph.setData({
          nodes: model.cards.map((card) => {
            const shape = stepNodeShape(card);
            return {
              id: card.id,
              combo: card.comboId || undefined,
              style: { size: shape.size, dx: shape.dx, dy: shape.dy, innerHTML: shape.innerHTML },
            };
          }),
          edges: model.edges,
          combos: model.combos.map((combo) => ({
            id: combo.id,
            combo: combo.parent,
            style: {
              fill: "#f7f3ea",
              stroke: combo.accent,
              lineWidth: 1,
              radius: 12,
              padding: 16,
              labelText: combo.label,
              labelFill: "#0c1f1a",
              labelFontSize: 12,
              labelPlacement: "top",
            },
          })),
        });
        return graph.render();
      })
      .then(async () => {
        if (cancelled || graph.destroyed) return;
        if (fitted.current === events.length) return;
        fitted.current = events.length;
        await graph.fitView({ when: "always" });
      })
      .catch(() => undefined);
    return () => {
      cancelled = true;
    };
  }, [events, openLoops, openSteps, settled]);

  return <div ref={containerRef} className="h-80 rounded-lg border border-[#0c1f1a]/10 bg-[#fbfaf6]" aria-label="Streaming step graph" />;
}
