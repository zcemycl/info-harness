/// <reference types="vite/client" />

interface ImportMetaEnv {
  readonly VITE_COGNITO_USER_POOL_ID: string;
  readonly VITE_COGNITO_USER_POOL_CLIENT_ID: string;
  readonly VITE_COGNITO_REGION?: string;
  readonly VITE_COGNITO_IDENTITY_POOL_ID?: string;
  readonly VITE_API_BASE_URL?: string;
  readonly VITE_AGENTIC_CHAT_STREAM_URL?: string;
  readonly VITE_APP_BASENAME?: string;
}

interface ImportMeta {
  readonly env: ImportMetaEnv;
}
