import { useState, type FormEvent } from "react";
import { useAuth } from "@/hooks";

const inputClassName =
  "rounded-lg border border-[#0c1f1a]/15 bg-white px-3 py-2.5 text-[#0c1f1a] outline-none focus:border-[#1f6b4a] focus:ring-2 focus:ring-[#1f6b4a]/20";

export function LoginPage() {
  const { login, confirmChallenge, challengeStep } = useAuth();
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [challengeResponse, setChallengeResponse] = useState("");
  const [error, setError] = useState<string | null>(null);
  const [submitting, setSubmitting] = useState(false);
  const needsChallenge = challengeStep !== null && challengeStep !== "DONE";
  const challengeLabel =
    challengeStep === "CONFIRM_SIGN_IN_WITH_NEW_PASSWORD_REQUIRED" ? "New password" : "Verification code";

  async function handleSignIn(event: FormEvent) {
    event.preventDefault();
    setError(null);
    setSubmitting(true);
    try {
      await login(username.trim(), password);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Sign in failed");
    } finally {
      setSubmitting(false);
    }
  }

  async function handleConfirm(event: FormEvent) {
    event.preventDefault();
    setError(null);
    setSubmitting(true);
    try {
      await confirmChallenge(challengeResponse);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Challenge confirmation failed");
    } finally {
      setSubmitting(false);
    }
  }

  return (
    <main className="grid min-h-svh lg:grid-cols-2">
      <aside className="relative hidden overflow-hidden bg-[#0c1f1a] px-10 py-12 text-[#e8f5ef] lg:flex lg:flex-col lg:justify-between">
        <div className="login-aside-glow" aria-hidden />
        <div className="relative">
          <p className="font-mono text-sm font-bold tracking-[0.14em] uppercase">info-harness</p>
          <h1 className="mt-8 max-w-sm text-3xl font-extrabold leading-tight">Sign in to research</h1>
          <p className="mt-4 max-w-sm text-sm leading-relaxed text-[#a8cbb8]">
            Cognito issues the access token. Every chat call sends it to the API.
          </p>
        </div>
      </aside>
      <section className="flex items-center justify-center bg-[#f4f7f5] px-4 py-12">
        <div className="w-full max-w-sm rounded-xl border border-[#0c1f1a]/10 bg-white p-8 shadow-sm">
          <h2 className="text-center text-lg font-extrabold text-[#0c1f1a]">
            {needsChallenge ? "Continue sign-in" : "Welcome back"}
          </h2>
          {error ? <p className="mt-4 rounded-md bg-red-50 px-3 py-2 text-sm text-red-700">{error}</p> : null}
          {needsChallenge ? (
            <form className="mt-6 flex flex-col gap-4" onSubmit={handleConfirm}>
              <label className="flex flex-col gap-1.5 text-sm text-[#3d5a50]">
                {challengeLabel}
                <input
                  className={inputClassName}
                  type={challengeStep === "CONFIRM_SIGN_IN_WITH_NEW_PASSWORD_REQUIRED" ? "password" : "text"}
                  value={challengeResponse}
                  onChange={(event) => setChallengeResponse(event.target.value)}
                  required
                />
              </label>
              <button className="rounded-lg bg-[#0c1f1a] px-4 py-2.5 text-[#e8f5ef] disabled:opacity-60" disabled={submitting}>
                {submitting ? "Confirming…" : "Continue"}
              </button>
            </form>
          ) : (
            <form className="mt-6 flex flex-col gap-4" onSubmit={handleSignIn}>
              <label className="flex flex-col gap-1.5 text-sm text-[#3d5a50]">
                Username or email
                <input className={inputClassName} value={username} onChange={(event) => setUsername(event.target.value)} autoComplete="username" required />
              </label>
              <label className="flex flex-col gap-1.5 text-sm text-[#3d5a50]">
                Password
                <input className={inputClassName} type="password" value={password} onChange={(event) => setPassword(event.target.value)} autoComplete="current-password" required />
              </label>
              <button className="rounded-lg bg-[#0c1f1a] px-4 py-2.5 text-[#e8f5ef] disabled:opacity-60" disabled={submitting}>
                {submitting ? "Signing in…" : "Sign in"}
              </button>
            </form>
          )}
        </div>
      </section>
    </main>
  );
}
