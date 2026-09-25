import { useCallback, useEffect, useState } from "react";
import { fetchAuthSession, getCurrentUser, signOut, type AuthUser } from "aws-amplify/auth";
import { getPendingSignInChallenge, mapSignInStep, type CognitoChallengeStep } from "@/auth";
import { amplifyConfirmSignIn, amplifySignIn } from "@/utils";

export function useCognitoAuth() {
  const [user, setUser] = useState<AuthUser | null>(null);
  const [accessToken, setAccessToken] = useState<string | null>(null);
  const [challengeStep, setChallengeStep] = useState<CognitoChallengeStep | null>(null);
  const [isBootstrapping, setIsBootstrapping] = useState(true);

  const refreshSession = useCallback(async () => {
    try {
      const session = await fetchAuthSession();
      const token = session.tokens?.accessToken?.toString() ?? null;
      if (token) {
        const current = await getCurrentUser();
        setUser(current);
        setAccessToken(token);
        setChallengeStep(null);
        return { user: current, accessToken: token };
      }
    } catch {
      // signed out or challenge pending
    }

    const pending = getPendingSignInChallenge();
    setUser(null);
    setAccessToken(null);
    setChallengeStep(pending);
    return { user: null, accessToken: null, challengeStep: pending };
  }, []);

  useEffect(() => {
    let active = true;
    void refreshSession().finally(() => {
      if (active) setIsBootstrapping(false);
    });
    return () => {
      active = false;
    };
  }, [refreshSession]);

  const login = useCallback(
    async (username: string, password: string) => {
      const output = await amplifySignIn({ username, password });
      const step = mapSignInStep(output.nextStep?.signInStep);
      if (step === "DONE") return refreshSession();
      setChallengeStep(step);
      return { challengeStep: step };
    },
    [refreshSession],
  );

  const confirmChallenge = useCallback(
    async (challengeResponse: string) => {
      const output = await amplifyConfirmSignIn({ challengeResponse });
      const step = mapSignInStep(output.nextStep?.signInStep);
      if (step !== "DONE") {
        setChallengeStep(step);
        return { challengeStep: step };
      }
      return refreshSession();
    },
    [refreshSession],
  );

  const logout = useCallback(async () => {
    await signOut();
    setUser(null);
    setAccessToken(null);
    setChallengeStep(null);
  }, []);

  return {
    user,
    accessToken,
    challengeStep,
    hasPendingSignIn: challengeStep !== null && challengeStep !== "DONE",
    isBootstrapping,
    isAuthenticated: user !== null && accessToken !== null,
    login,
    confirmChallenge,
    logout,
    refreshSession,
  };
}
