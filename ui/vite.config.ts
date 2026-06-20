import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";
import dts from "vite-plugin-dts";
import { resolve } from "node:path";

// Two build modes:
//   default  -> the runnable dashboard app (npm run build)
//   --mode lib -> the component library dist/ that /design-sync consumes (npm run build:lib)
export default defineConfig(({ mode }) => {
  if (mode === "lib") {
    return {
      plugins: [
        react(),
        // Emit per-component .d.ts (Card.d.ts/CardProps …) — the API contract the
        // design-sync converter enumerates exports from and the design agent codes against.
        dts({ include: ["src/components"], entryRoot: "src/components", insertTypesEntry: true }),
      ],
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
