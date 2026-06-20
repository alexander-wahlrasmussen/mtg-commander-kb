import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";
import { resolve } from "node:path";

// Two build modes:
//   default  -> the runnable dashboard app (npm run build)
//   --mode lib -> the component library dist/ that /design-sync consumes (npm run build:lib)
export default defineConfig(({ mode }) => {
  if (mode === "lib") {
    return {
      plugins: [react()],
      build: {
        outDir: "dist",
        lib: {
          entry: resolve(__dirname, "src/components/index.ts"),
          name: "PodGauntletUI",
          fileName: "pod-gauntlet-ui",
          formats: ["es", "umd"],
        },
        rollupOptions: {
          external: ["react", "react-dom", "react/jsx-runtime"],
          output: {
            globals: {
              react: "React",
              "react-dom": "ReactDOM",
              "react/jsx-runtime": "jsxRuntime",
            },
          },
        },
      },
    };
  }
  // dev / app build — talks to the Python server in dev via a proxy
  return {
    plugins: [react()],
    server: {
      proxy: { "/api": "http://127.0.0.1:8765" },
    },
  };
});
