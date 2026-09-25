import type { AuthUser } from "aws-amplify/auth";
import type { CognitoChallengeStep } from "@/auth";

export type AuthContextValue = {
  user: AuthUser | null;
  accessToken: string | null;
  challengeStep: CognitoChallengeStep | null;
  isBootstrapping: boolean;
  isAuthenticated: boolean;
  login: (username: string, password: string) => Promise<void>;
  confirmChallenge: (response: string) => Promise<void>;
  logout: () => Promise<void>;
};

export type ChatMeta = {
  chat_id: string;
  title: string;
  created_at: string;
  updated_at: string;
};

export type ChatMessage = {
  role: "user" | "assistant";
  content: string;
  ts: string;
  run_id: string | null;
};

export type RunEvent = {
  seq: number;
  type: "stage" | "final" | "error";
  loop?: number | null;
  agent?: string | null;
  status?: string | null;
  summary?: string;
  answer?: string | null;
};

export type RunView = {
  status: string;
  answer?: string | null;
  error?: string | null;
};
