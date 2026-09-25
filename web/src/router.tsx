import { BrowserRouter, Navigate, Route, Routes } from "react-router-dom";
import { ProtectedRoute } from "@/components";
import { PRIVATE_HOME_PATH } from "@/constants";
import { AuthProvider } from "@/context";
import { ChatPage } from "@/pages/chat";
import { LoginPage } from "@/pages/LoginPage";

const basename = (import.meta.env.VITE_APP_BASENAME ?? "").replace(/\/$/, "");

export function AppRouter() {
  return (
    <BrowserRouter basename={basename}>
      <AuthProvider>
        <Routes>
          <Route path="/login" element={<LoginPage />} />
          <Route element={<ProtectedRoute />}>
            <Route path={PRIVATE_HOME_PATH} element={<ChatPage />} />
          </Route>
          <Route path="*" element={<Navigate to={PRIVATE_HOME_PATH} replace />} />
        </Routes>
      </AuthProvider>
    </BrowserRouter>
  );
}
