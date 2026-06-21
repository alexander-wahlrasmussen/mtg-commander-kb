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
- **Gruvbox retheme (2026-06-21).** `src/theme/tokens.css` `:root` carries the warm Gruvbox dark palette
  (`--accent:#fe8019`, `--bg:#282828`, `--text:#fbf1c7`, …) + a `[data-pg-theme="light"]` Gruvbox-light
  block; body radial gradients are gruvbox (`#3c3836`/`#32302f`). The values match the project templates'
  local `[data-pg-theme]` overrides — so rethemeing the bundle makes those overrides redundant. `app/data.ts`
  `PALETTE` is the warm set (accent-first). **The chart/chip STORIES hardcode series hex** (they don't read
  tokens — SVG `fill` can't resolve `var(--*)`), so BarChart/LineChart/Chip stories were remapped old→new
  PALETTE positions (`#5cd2ff→#fe8019`, `#ffb454→#fabd2f`, `#46d39a→#b8bb26`, `#ff6b6b→#fb4934`, `#b48cff→#d3869b`).
  A token-only change leaves the chart cards their old color — the stories MUST move too.
- **Fonts self-hosted via base64 `@font-face` (2026-06-21).** `tokens.css` first line is `@import "./fonts.css"`;
  `src/theme/fonts.css` holds 7 `@font-face` rules (Spectral 400/500/600/700, IBM Plex Mono 400/500/600, latin
  subset) with `src:url(data:font/woff2;base64,…)`. Regenerate with `.design-sync/fetch-fonts.mjs` (downloads from
  Google, base64-inlines). Data-URI faces survive Vite untouched (no asset hashing) → ship verbatim in
  `_ds_bundle.css` and render in storybook too. The remote Google `@import` is GONE → the converter prints NO
  font warning. Superseded the `@import` decision.
- **`/* @kind */` token comments are source-only.** `--mono` and `--ease` carry `/* @kind font */` /
  `/* @kind other */` in `tokens.css`, but this design-sync converter has NO `@kind` consumer (grep
  finds none) and Vite's CSS minifier strips them from `dist/style.css` anyway — they never reach the
  bundle. Kept in source as intent/for any external token compiler; they do not affect the sync.
- **cardMode: column** for the wide components (BarChart, Heatmap, LineChart, TabBar) — their
  stories are wider than a grid cell; column mode keeps full width per story.

## Re-sync risks
- Fonts: self-hosted base64 `@font-face` — no font warning expected (no remote dependency). `src/theme/fonts.css`
  is generated; regenerate with `.design-sync/fetch-fonts.mjs` if weights/subset change. Latin subset only — non-latin
  glyphs fall back to the stack (`Georgia` / `ui-monospace`).
- A palette/token change in `tokens.css` re-renders every preview and triggers a `canary` reference-drift
  spot-check (grades carry). But chart/chip STORY color edits change those components' sourceKeys → they
  re-grade. Verify a BarChart card is orange (not cyan) after any palette change.
- vite-plugin-dts also emits `*.stories.d.ts` into dist (harmless; not exported from index.d.ts).
