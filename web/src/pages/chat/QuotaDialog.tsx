import { useState } from "react";
import { apiFetch } from "@/api/client";

type QuotaNotice = {
  resetsOn: string | null;
};

type BillingMode = "open" | "table" | "stripe" | null;

export function QuotaDialog({
  notice,
  token,
  mode,
  onClose,
}: {
  notice: QuotaNotice;
  token: string;
  mode: BillingMode;
  onClose: () => void;
}) {
  const [pending, setPending] = useState(false);
  const [upgradeError, setUpgradeError] = useState<string | null>(null);
  const when = notice.resetsOn ? formatResetDate(notice.resetsOn) : "one month from your last window";

  async function upgrade() {
    setPending(true);
    setUpgradeError(null);
    try {
      const response = await apiFetch(token, "/billing/checkout", { method: "POST" });
      if (!response.ok) {
        setUpgradeError("Checkout is unavailable right now.");
        return;
      }
      const body = (await response.json()) as { url?: string };
      if (!body.url) {
        setUpgradeError("Checkout is unavailable right now.");
        return;
      }
      window.location.assign(body.url);
    } catch {
      setUpgradeError("Checkout is unavailable right now.");
    } finally {
      setPending(false);
    }
  }

  return (
    <div className="fixed inset-0 z-20 flex items-center justify-center bg-[#0c1f1a]/40 p-4" role="presentation" onClick={onClose}>
      <div
        className="w-full max-w-md rounded-xl bg-white p-6 shadow-lg"
        role="dialog"
        aria-modal="true"
        aria-labelledby="quota-title"
        onClick={(event) => event.stopPropagation()}
      >
        <h2 id="quota-title" className="text-lg font-bold text-[#0c1f1a]">
          Out of quota for the free trial
        </h2>
        <ul className="mt-3 space-y-2 text-sm text-[#35584a]">
          <li>Wait until {when} for the allowance to reset.</li>
          {mode === "stripe" ? null : <li>Or upgrade to the Pro plan.</li>}
        </ul>
        {upgradeError ? <p className="mt-3 text-sm text-red-700">{upgradeError}</p> : null}
        <div className="mt-5 flex gap-2">
          {mode === "stripe" ? (
            <button
              type="button"
              className="rounded-lg bg-[#1f7a4d] px-4 py-2 text-sm text-white disabled:opacity-60"
              disabled={pending}
              onClick={() => void upgrade()}
            >
              {pending ? "Opening Checkout…" : "Upgrade to Pro"}
            </button>
          ) : null}
          <button type="button" className="rounded-lg bg-[#0c1f1a] px-4 py-2 text-sm text-white" onClick={onClose}>
            Close
          </button>
        </div>
      </div>
    </div>
  );
}

function formatResetDate(iso: string): string {
  const [year, month, day] = iso.split("-").map(Number);
  if (!year || !month || !day) return iso;
  return new Date(year, month - 1, day).toLocaleDateString(undefined, {
    day: "numeric",
    month: "long",
    year: "numeric",
  });
}
