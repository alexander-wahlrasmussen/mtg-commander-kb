# design-sync notes — pod-gauntlet-ui

Repo-specific gotchas and decisions for future syncs. Committed; read before re-syncing.

## Setup facts
- Package lives in `ui/` (subdir), not repo root. `storybookConfigDir: ui/.storybook`.
- The package's own source repo has no `node_modules/<pkg>`, so the converter runs with
  `--entry ui/dist/pod-gauntlet-ui.js --node-modules ui/node_modules`. Build dist first:
  `cd ui && npm run build:lib` (Vite lib mode + vite-plugin-dts → `dist/*.d.ts`).
- The component library entry (`src/components/index.ts`) imports `../theme/tokens.css` so the
  lib `dist/style.css` is self-contained (tokens + component CSS). Without that, previews lose
  all `var(--*)` and render unstyled.

## Decisions
- **[FONT_MISSING] accepted (system substitutes).** The DS references "Inter" / "JetBrains Mono"
  (loaded from Google Fonts CDN in the real app via a `<link>`). We did NOT bundle woff2 via
  `cfg.extraFonts`, so claude.ai/design previews fall back to system sans/mono. Acceptable for
  this hobby exploration; revisit by adding woff2 + `@font-face` if exact type matters.
- **cardMode: column** for the wide components (BarChart, Heatmap, LineChart, TabBar) — their
  stories are wider than a grid cell; column mode keeps full width per story.

## Re-sync risks
- Fonts: the [FONT_MISSING] warning will recur by design (substitutes accepted) — not a regression.
- vite-plugin-dts also emits `*.stories.d.ts` into dist (harmless; not exported from index.d.ts).
