import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { apiFetch } from "@/api/client";
import { PRIVATE_HOME_PATH } from "@/constants";
import { useAuth } from "@/hooks";

export function BillingSuccessPage() {
  const { accessToken } = useAuth();
  const [plan, setPlan] = useState<string | null>(null);

  useEffect(() => {
    const token = accessToken ?? "";
    if (!token) return;
    let stopped = false;
    let attempts = 0;
    let timer = 0;

    async function poll() {
      if (stopped) return;
      attempts += 1;
      try {
        const response = await apiFetch(token, "/billing/me");
        if (response.ok) {
          const body = (await response.json()) as { plan?: string };
          if (!stopped) setPlan(body.plan ?? null);
          if (body.plan === "pro") return;
        }
      } catch {
        if (stopped) return;
      }
      if (stopped || attempts >= 20) return;
      timer = window.setTimeout(() => void poll(), 1500);
    }

    void poll();
    return () => {
      stopped = true;
      window.clearTimeout(timer);
    };
  }, [accessToken]);

  const ready = plan === "pro";
  return (
    <main className="mx-auto flex min-h-svh max-w-md flex-col justify-center bg-[#f4f7f5] px-6">
      <h1 className="text-xl font-bold text-[#0c1f1a]">{ready ? "Pro is active" : "Confirming Pro"}</h1>
      <p className="mt-3 text-sm text-[#35584a]">
        {ready
          ? "The next research run uses the Pro allowance."
          : "Stripe is confirming the subscription. This page checks again automatically."}
      </p>
      <Link className="mt-6 text-sm underline text-[#1f7a4d]" to={PRIVATE_HOME_PATH}>
        Back to chat
      </Link>
    </main>
  );
}
