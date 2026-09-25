import type { StepCard } from "./toStepGraph";

function escapeHtml(value: string): string {
  return value.replaceAll("&", "&amp;").replaceAll("<", "&lt;").replaceAll(">", "&gt;").replaceAll('"', "&quot;");
}

export function stepNodeShape(card: StepCard): {
  innerHTML: string;
  size: [number, number];
  dx: number;
  dy: number;
} {
  const width = card.compact ? 176 : card.expanded ? 300 : 220;
  const lines = Math.min(8, Math.max(2, Math.ceil(card.detail.length / 42)));
  const bodyHeight = card.expanded && !card.compact ? 16 + lines * 18 : 0;
  const height = (card.compact ? 36 : 48) + bodyHeight;
  const detail = escapeHtml(card.detail);
  const body = card.expanded
    ? `<div style="height:${bodyHeight}px;box-sizing:border-box;padding:8px 12px;font-size:12px;line-height:18px;color:#24352e;white-space:pre-wrap;overflow:auto;background:#fbfaf6;">${detail}</div>`
    : "";
  const innerHTML = `
<div data-step-id="${card.id}" style="width:${width}px;height:${height}px;box-sizing:border-box;border-radius:12px;background:#fff;border:1px solid #d9cbb3;box-shadow:0 6px 16px rgba(12,31,26,0.08);overflow:hidden;font-family:'DM Sans',ui-sans-serif,system-ui,sans-serif;cursor:pointer;">
  <div style="display:flex;align-items:center;gap:8px;height:${card.compact ? 36 : 48}px;padding:0 10px;border-left:4px solid ${card.accent};box-sizing:border-box;">
    <span style="color:${card.accent};font-size:12px;line-height:1;">${card.expanded ? "▾" : "▸"}</span>
    <span style="min-width:0;flex:1;">
      <span style="display:block;font-size:13px;font-weight:700;color:#0c1f1a;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;">${escapeHtml(card.title)}</span>
      <span style="display:block;margin-top:2px;font-size:11px;color:#5a7a6c;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;">${escapeHtml(card.meta)}</span>
    </span>
  </div>
  ${body}
</div>`;
  return { innerHTML, size: [width, height], dx: -width / 2, dy: -height / 2 };
}
