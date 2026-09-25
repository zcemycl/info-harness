import path from "node:path";
import { fileURLToPath } from "node:url";
import react from "@vitejs/plugin-react";
import { defineConfig, loadEnv } from "vite";

const __dirname = path.dirname(fileURLToPath(import.meta.url));

export default defineConfig(({ mode }) => {
  const env = loadEnv(mode, __dirname, "");
  const appBasename = (env.VITE_APP_BASENAME ?? "").replace(/\/$/, "");

  return {
    base: appBasename ? `${appBasename}/` : "/",
    plugins: [react()],
    server: {
      port: 3000,
    },
    build: {
      rollupOptions: {
        input: {
          main: path.resolve(__dirname, "index.html"),
          notfound: path.resolve(__dirname, "404.html"),
        },
      },
      assetsDir: "assets",
    },
    resolve: {
      alias: { "@": path.resolve(__dirname, "./src") },
    },
  };
});
