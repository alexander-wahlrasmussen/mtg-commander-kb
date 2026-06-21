# design-sync notes — pod-gauntlet-ui

Repo-specific gotchas and decisions for future syncs. Committed; read before re-syncing.

## Setup facts
- Package lives in `ui/` (subdir), not repo root. `storybookConfigDir: ui/.storybook`.
- The package's own source repo has no `node_modules/<pkg>`, so the converter runs with
  `--entry ui/dist/pod-gauntlet-ui.js --node-modules ui/node_modules`. Build dist first:
  `cd ui && npm run build:lib` (Vite lib mode + vite-plugin-dts → `dist/*.d.ts`).
- The component library entry (`src/components/index.ts`) imports `../theme/tokens.css`, and `tokens.css`
  first line `@import "./fonts.css"` — so the lib `dist/style.css` is self-contained (fonts + tokens +
  component CSS). Without either import, previews lose all `var(--*)` and/or the real fonts.
- The synced project (claude.ai/design **"Pod Gauntlet"**, id `68c44cf9-79e2-4bb6-b086-0a13cd0d20aa`) also
  holds MANY non-synced user files (`templates/*.dc.html`, `analysis/`, `decks/`, `dashboard/data/`,
  `ui-theme/tokens.gruvbox.css`, top-level KB markdown). design-sync owns ONLY its slice: `components/`,
  `_preview/`, `_vendor/`, `_ds_bundle.*`, `styles.css`, `README.md`, `_ds_sync.json`, `_ds_needs_recompile`.
  The anchored diff's `deletePaths` is authoritative — it was `[]` on the 2026-06-21 newsprint sync. NEVER
  widen the plan's `deletes` to clobber the user's other project files.

## Decisions
- **Active theme = "Tale of the Tape" newsprint LIGHT (2026-06-21).** The master merge
  (`9023009 newsprint supersedes the Gruvbox retheme`) replaced the warm Gruvbox dark palette. `tokens.css`
  `:root` now carries newsprint primitives — cream paper (`--paper #e9e3d4`/`--paper2 #f1ecdf`), near-black
  ink (`--ink #16130f`), one vermillion accent (`--acc #c63a1b`), gold `#946112`, olive `--good #4f6b1e` —
  plus the same remap-token names the components consume (`--bg`, `--text`, `--accent`, `--mono`, …). Square
  corners (`--radius:0`), flat fills (`--shadow:none`), faint newsprint hatch on `body`. **No `[data-pg-theme]`
  variant anymore** — light only. The old config/NOTES/conventions all described Gruvbox and were stale until
  this sync caught up.
- **Three type faces (newsprint).** `--font`/`--serif` = **Georgia** (system serif, running body),
  `--disp` = **Oswald** (condensed display headings — ChampionBanner etc.), `--mono` = **IBM Plex Mono**
  (every figure/number). Library `dist/style.css` uses `var(--disp)` ×5, `var(--mono)` ×17, `var(--serif)`/`--font` ×5.
- **Font self-host RESTORED for newsprint (2026-06-21, this run).** The newsprint redesign named Oswald +
  IBM Plex Mono in the tokens but **dropped** the `@import "./fonts.css"` the Gruvbox build had, and never
  regenerated `fonts.css` (it still held Spectral) → both fonts fell back to system fonts everywhere,
  including the deployed Pages app (`[FONT_MISSING]`; the compare oracle can't see it — both panels fall back
  identically). Fix: regenerated `ui/src/theme/fonts.css` via `.design-sync/fetch-fonts.mjs` (now fetches
  **Oswald 400/500/600/700 + IBM Plex Mono 400/500/600**, base64 woff2 latin) and re-added `@import "./fonts.css"`
  as line 1 of `tokens.css`. Result: 7 `@font-face` inlined into `dist/style.css` (188 KB), `✓ bundle complete`,
  no font warning. Georgia is a system face — no `@font-face`.
- **Chart/Chip story colors are bright Gruvbox-era hex, on purpose-ish.** `BarChart`/`LineChart`/`Chip`
  stories hardcode `#fe8019 #fabd2f #b8bb26 #fb4934 #d3869b` (a bright qualitative set, good multi-series
  legibility on cream) — NOT the muted newsprint `PALETTE` in `ui/src/app/data.ts` (`#c63a1b #946112 #4f6b1e …`).
  These story files were last touched by the Gruvbox commit; the newsprint commit didn't update them, yet the
  diff flags them `changed` (sourceKey recipe). Storybook + preview render the same hardcoded hex → all grade
  `match`. The conventions header documents the bright set as the chart series palette and `--accent #c63a1b`
  as the single brand accent. To make charts on-brand newsprint, edit those 3 stories (will re-grade them).
- **`/* @kind */` token comments are source-only.** `--mono`/`--ease` carry `/* @kind font|other */`; no
  `@kind` consumer in this converter and Vite minifies them out of `dist/style.css`. Harmless.

## Re-sync risks
- **Fonts:** self-hosted base64 `@font-face` (Oswald + IBM Plex Mono) via `tokens.css` `@import "./fonts.css"`.
  No remote dependency → no font warning expected. Regenerate `ui/src/theme/fonts.css` with
  `.design-sync/fetch-fonts.mjs` if weights/subset change. Latin subset only — non-latin glyphs fall back
  (Georgia / ui-monospace / ui-sans-serif). If the newsprint redesign ever rewrites `tokens.css` again, CHECK
  line 1 still has `@import "./fonts.css"` — losing it silently re-breaks Oswald + IBM Plex Mono everywhere.
- **Reference must move with the lib build.** After ANY theme/source change, rebuild BOTH `cd ui && npm run
  build:lib` AND `npx storybook build -c ui/.storybook -o .design-sync/sb-reference` (absolute `-o`). A
  styling/font change re-renders every preview but grades carry; rebuilding sb-reference can trigger a
  `reference_drift` canary spot-check (grades kept — confirm the named sheets). On 2026-06-21 the font fix
  fired one over Heatmap/Slider/ChampionBanner/ProgressBar/SegmentedControl — all confirmed `match`.
- A palette/token change re-renders previews (grades carry). But chart/chip STORY hex edits change those 3
  components' sourceKeys → they re-grade. Verify a BarChart card's bar colors after any such change.
- vite-plugin-dts also emits `*.stories.d.ts` into dist (harmless; not exported from index.d.ts).
- **Windows lock gotcha:** never leave a shell cwd — or a background poll loop — inside `ds-bundle/`. The
  driver's `rmSync(ds-bundle)` then EPERMs ("Device or resource busy") and the build stage fails. Keep cwd at
  repo root; if it locks, find the bash.exe whose cwd is in `ds-bundle` (a stuck `until` poll loop is the
  usual culprit) and `Stop-Process` it, then re-run.
