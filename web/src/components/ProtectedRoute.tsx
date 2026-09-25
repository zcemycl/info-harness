import { Navigate, Outlet } from "react-router-dom";
import { useAuth } from "@/hooks";

export function ProtectedRoute() {
  const { isAuthenticated, challengeStep } = useAuth();
  if (challengeStep || !isAuthenticated) return <Navigate to="/login" replace />;
  return <Outlet />;
}
