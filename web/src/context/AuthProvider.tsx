import { useCallback, useEffect, useMemo, type ReactNode } from "react";
import { useLocation, useNavigate } from "react-router-dom";
import { PRIVATE_HOME_PATH, PUBLIC_PATHS } from "@/constants";
import { AuthContext } from "@/context/auth-context";
import { useCognitoAuth } from "@/hooks/useCognitoAuth";
import type { AuthContextValue } from "@/types";

export function AuthProvider({ children }: { children: ReactNode }) {
  const navigate = useNavigate();
  const pathname = useLocation().pathname;
  const cognito = useCognitoAuth();

  const postLogin = useCallback(
    async (username: string, password: string) => {
      const result = await cognito.login(username, password);
      if ("challengeStep" in result && result.challengeStep && result.challengeStep !== "DONE") {
        return;
      }
      navigate(PRIVATE_HOME_PATH, { replace: true });
    },
    [cognito, navigate],
  );

  const postConfirm = useCallback(
    async (response: string) => {
      const result = await cognito.confirmChallenge(response);
      if ("challengeStep" in result && result.challengeStep && result.challengeStep !== "DONE") {
        return;
      }
      navigate(PRIVATE_HOME_PATH, { replace: true });
    },
    [cognito, navigate],
  );

  const postLogout = useCallback(async () => {
    await cognito.logout();
    navigate("/login", { replace: true });
  }, [cognito, navigate]);

  useEffect(() => {
    if (cognito.isBootstrapping) return;
    const isPublic = PUBLIC_PATHS.some((path) => pathname === path);
    if (cognito.hasPendingSignIn && !isPublic) {
      navigate("/login", { replace: true });
      return;
    }
    if (!cognito.isAuthenticated && !isPublic) {
      navigate("/login", { replace: true });
      return;
    }
    if (cognito.isAuthenticated && pathname === "/login") {
      navigate(PRIVATE_HOME_PATH, { replace: true });
    }
  }, [cognito.hasPendingSignIn, cognito.isAuthenticated, cognito.isBootstrapping, navigate, pathname]);

  const value = useMemo<AuthContextValue>(
    () => ({
      user: cognito.user,
      accessToken: cognito.accessToken,
      challengeStep: cognito.challengeStep,
      isBootstrapping: cognito.isBootstrapping,
      isAuthenticated: cognito.isAuthenticated,
      login: postLogin,
      confirmChallenge: postConfirm,
      logout: postLogout,
    }),
    [cognito, postConfirm, postLogin, postLogout],
  );

  if (cognito.isBootstrapping) {
    return (
      <div className="flex min-h-svh items-center justify-center bg-[#f4f7f5]">
        <div className="h-10 w-10 animate-spin rounded-full border-4 border-slate-300 border-t-[#0c1f1a]" />
      </div>
    );
  }

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}
