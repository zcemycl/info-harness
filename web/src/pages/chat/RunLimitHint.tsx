import { useEffect, useState } from "react";
import { apiFetch } from "@/api/client";

type BillingMode = "open" | "table" | "stripe";

type BillingMe = {
  mode: BillingMode;
  plan: string;
  runs_limit: number | null;
  runs_used: number | null;
};

export function RunLimitHint({
  token,
  revision,
  onMode,
}: {
  token: string;
  revision: number;
  onMode?: (mode: BillingMode) => void;
}) {
  const [body, setBody] = useState<BillingMe | null>(null);
  const [portalError, setPortalError] = useState<string | null>(null);

  useEffect(() => {
    if (!token) return;
    let cancelled = false;
    void apiFetch(token, "/billing/me")
      .then(async (response) => {
        if (!response.ok) return null;
        return (await response.json()) as BillingMe;
      })
      .then((next) => {
        if (cancelled || !next) return;
        setBody(next);
        onMode?.(next.mode);
      })
      .catch(() => {
        if (!cancelled) setBody(null);
      });
    return () => {
      cancelled = true;
    };
  }, [token, revision, onMode]);

  async function manage() {
    setPortalError(null);
    const response = await apiFetch(token, "/billing/portal", { method: "POST" });
    if (!response.ok) {
      setPortalError("Billing portal is unavailable.");
      return;
    }
    const payload = (await response.json()) as { url?: string };
    if (!payload.url) {
      setPortalError("Billing portal is unavailable.");
      return;
    }
    window.location.assign(payload.url);
  }

  const limit = body?.runs_limit;
  const used = body?.runs_used ?? 0;
  const metered = (body?.mode === "table" || body?.mode === "stripe") && limit != null;
  const width = metered && limit > 0 ? Math.min(100, (used / limit) * 100) : 0;
  const planLabel = body?.plan === "pro" ? "Pro Plan" : "Free Plan";

  if (!body) {
    return (
      <div className="mt-auto border-t border-[#0c1f1a]/10 pt-3" aria-busy="true">
        <p className="mb-1 flex items-center gap-1.5 text-xs font-semibold text-[#0c1f1a]">
          <PlanIcon />
          Free Plan
        </p>
        <p className="mb-1.5 text-xs text-[#5a7a6c]">Usage</p>
        <div className="h-1.5 overflow-hidden rounded-full bg-[#d9cbb3]">
          <div className="h-full w-1/3 animate-pulse rounded-full bg-[#5a7a6c]" />
        </div>
      </div>
    );
  }

  if (!metered) {
    return <p className="mt-auto border-t border-[#0c1f1a]/10 pt-3 text-xs text-[#5a7a6c]">No run limit</p>;
  }

  return (
    <div className="mt-auto border-t border-[#0c1f1a]/10 pt-3">
      <p className="mb-1 flex items-center gap-1.5 text-xs font-semibold text-[#0c1f1a]">
        <PlanIcon />
        {planLabel}
      </p>
      <p className="mb-1.5 font-mono text-xs text-[#5a7a6c]">
        Usage: {used}/{limit}
      </p>
      <div
        className="h-1.5 overflow-hidden rounded-full bg-[#d9cbb3]"
        role="progressbar"
        aria-valuemin={0}
        aria-valuemax={limit}
        aria-valuenow={used}
        aria-label={`${used} of ${limit} research runs used`}
      >
        <div className="h-full rounded-full bg-[#0c1f1a] transition-[width]" style={{ width: `${width}%` }} />
      </div>
      {body.plan === "pro" ? (
        <button type="button" className="mt-2 text-xs underline text-[#1f7a4d]" onClick={() => void manage()}>
          Manage subscription
        </button>
      ) : null}
      {portalError ? <p className="mt-1 text-xs text-red-700">{portalError}</p> : null}
    </div>
  );
}

function PlanIcon() {
  return (
    <svg width="14" height="14" viewBox="0 0 14 14" aria-hidden="true" className="shrink-0 text-[#1f7a4d]">
      <circle cx="7" cy="7" r="6" fill="currentColor" opacity="0.15" />
      <path
        d="M7 3.2 8.1 5.5l2.5.3-1.8 1.7.4 2.5L7 8.8 4.8 10l.4-2.5L3.4 5.8l2.5-.3L7 3.2Z"
        fill="currentColor"
      />
    </svg>
  );
}
