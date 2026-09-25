import { fetchAuthSession } from "aws-amplify/auth";

function apiBase(): string {
  return (import.meta.env.VITE_API_BASE_URL ?? "http://127.0.0.1:8080").replace(/\/$/, "");
}

function streamBase(): string {
  const configured = (import.meta.env.VITE_AGENTIC_CHAT_STREAM_URL ?? "").trim().replace(/\/$/, "");
  return configured || apiBase();
}

function joinUrl(base: string, path: string): string {
  const normalized = path.startsWith("/") ? path : `/${path}`;
  return `${base}${normalized}`;
}

let refreshInFlight: Promise<string | null> | null = null;

function secondsLeft(token: string): number | null {
  const part = token.split(".")[1];
  if (!part) return null;
  try {
    const padded = part.replace(/-/g, "+").replace(/_/g, "/");
    const payload = JSON.parse(atob(padded)) as { exp?: number };
    if (typeof payload.exp !== "number") return null;
    return payload.exp - Math.floor(Date.now() / 1000);
  } catch {
    return null;
  }
}

async function sessionAccessToken(fallback: string): Promise<string> {
  const usable = fallback.split(".").length === 3 && (secondsLeft(fallback) ?? 0) > 60;
  if (usable) return fallback;
  if (!refreshInFlight) {
    refreshInFlight = fetchAuthSession({ forceRefresh: true })
      .then((session) => session.tokens?.accessToken?.toString() ?? null)
      .finally(() => {
        refreshInFlight = null;
      });
  }
  const refreshed = await refreshInFlight;
  if (refreshed && refreshed.split(".").length === 3) return refreshed;
  return fallback;
}

export async function apiFetch(token: string, path: string, init: RequestInit = {}): Promise<Response> {
  const headers = new Headers(init.headers);
  headers.set("Authorization", `Bearer ${await sessionAccessToken(token)}`);
  if (init.body && !headers.has("Content-Type")) {
    headers.set("Content-Type", "application/json");
  }
  return fetch(joinUrl(apiBase(), path), { ...init, headers });
}

export async function streamFetch(token: string, path: string): Promise<Response> {
  const headers = new Headers();
  headers.set("Authorization", `Bearer ${await sessionAccessToken(token)}`);
  headers.set("Accept", "text/event-stream");
  return fetch(joinUrl(streamBase(), path), { headers });
}
