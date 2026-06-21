## Pod Gauntlet — how to build with this system

A dark, data-dense analytics design system (the "Pod Gauntlet" dashboard) on a warm **Gruvbox** palette.
Compose the exported React components; style your own layout glue with the design **tokens** below. There
are **no utility classes** and **no theme provider** — the tokens live on `:root` in the bundled stylesheet
(plus a `[data-pg-theme="light"]` Gruvbox-light variant), so components are styled the moment the system's
CSS is present. Just render them.

### Styling idiom — CSS custom properties (tokens)

Style everything you add (page background, grid gaps, spacing, your own text) with these tokens via
`var(--token)`. Do **not** invent hex colors or hardcoded pixels — use the scale.

- **Surfaces:** `--bg` (page), `--bg-2`, `--bg-3`, `--panel`, `--panel-2`, `--line`, `--line-2`
- **Text:** `--text`, `--muted`, `--faint`
- **Brand / data:** `--accent` (primary orange), `--accent-2` (yellow), `--accent-ink` (text on accent),
  `--good` (green), `--warn` (red), `--gold`, `--silver`, `--bronze`
- **Type:** `--font` (UI), `--mono` (numbers/tabular); sizes `--fs-xs … --fs-2xl`
- **Spacing:** `--s1`(4px) `--s2`(8) `--s3`(12) `--s4`(16) `--s5`(24) `--s6`(32)
- **Shape/motion:** `--radius`, `--radius-sm`, `--shadow`, `--shadow-lg`, `--ease`

Put the page on `background: var(--bg); color: var(--text); font-family: var(--font)`.

### Components (compose these)

- **Layout/chrome:** `Card` (titled panel w/ accent tick), `TabBar`, `EmptyState`, `ProgressBar`
- **Controls:** `SegmentedControl`, `Slider`, `Chip`, `Badge` (status: `default|busy|ok|err`)
- **Data:** `StatTable` (columns can render in-cell bars), `BracketPod` + seats, `ChampionBanner`
- **Charts (SVG):** `BarChart`, `LineChart`, `Heatmap` — pass an explicit `color` per series (a real hex,
  e.g. the Gruvbox palette `#fe8019` `#fabd2f` `#b8bb26` `#fb4934` `#d3869b`); SVG `fill` does **not** resolve `var(--*)`

Each component's props are in its `.d.ts` (`<Name>Props`) and usage in its `.prompt.md` — read those
before composing. Numbers should use `font-family: var(--mono)` and `font-variant-numeric: tabular-nums`.

### A typical build

```tsx
import { Card, SegmentedControl, Slider, Badge, BarChart } from "pod-gauntlet-ui";

<div style={{ background: "var(--bg)", color: "var(--text)", padding: "var(--s5)", fontFamily: "var(--font)" }}>
  <div style={{ display: "flex", gap: "var(--s5)", alignItems: "flex-end", marginBottom: "var(--s4)" }}>
    <SegmentedControl options={[{ value: "decap", label: "decap" }, { value: "table", label: "table" }]} value="decap" onChange={() => {}} />
    <Slider label="Abolisher P(out)" value={0.3} min={0} max={1} step={0.05} display="0.30" onChange={() => {}} />
    <Badge variant="ok">16 decks</Badge>
  </div>
  <Card title="P(beat the pod)" hint="· DECAP clock">
    <BarChart
      series={[{ key: "win", label: "P(WIN)", color: "#fe8019" }, { key: "pure", label: "PURE RACE", color: "#fabd2f" }]}
      rows={[{ label: "Radiation Sickness", values: { win: 69, pure: 57 } }]}
    />
  </Card>
</div>
```

Note: the UI font is **Spectral** (a serif) and numbers/tabular use **IBM Plex Mono** — both shipped as
self-hosted `@font-face` (base64 woff2, latin subset) in the bundled stylesheet, so the real fonts render
with no remote dependency.
