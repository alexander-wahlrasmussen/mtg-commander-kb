## Pod Gauntlet — how to build with this system

A dark, data-dense analytics design system (the "Pod Gauntlet" dashboard). Compose the exported
React components; style your own layout glue with the design **tokens** below. There are **no
utility classes** and **no theme provider** — the tokens live on `:root` in the bundled stylesheet,
so components are styled the moment the system's CSS is present. Just render them.

### Styling idiom — CSS custom properties (tokens)

Style everything you add (page background, grid gaps, spacing, your own text) with these tokens via
`var(--token)`. Do **not** invent hex colors or hardcoded pixels — use the scale.

- **Surfaces:** `--bg` (page), `--bg-2`, `--bg-3`, `--panel`, `--panel-2`, `--line`, `--line-2`
- **Text:** `--text`, `--muted`, `--faint`
- **Brand / data:** `--accent` (primary cyan), `--accent-2` (amber), `--accent-ink` (text on accent),
  `--good`, `--warn`, `--gold`, `--silver`, `--bronze`
- **Type:** `--font` (UI), `--mono` (numbers/tabular); sizes `--fs-xs … --fs-2xl`
- **Spacing:** `--s1`(4px) `--s2`(8) `--s3`(12) `--s4`(16) `--s5`(24) `--s6`(32)
- **Shape/motion:** `--radius`, `--radius-sm`, `--shadow`, `--shadow-lg`, `--ease`

Put the page on `background: var(--bg); color: var(--text); font-family: var(--font)`.

### Components (compose these)

- **Layout/chrome:** `Card` (titled panel w/ accent tick), `TabBar`, `EmptyState`, `ProgressBar`
- **Controls:** `SegmentedControl`, `Slider`, `Chip`, `Badge` (status: `default|busy|ok|err`)
- **Data:** `StatTable` (columns can render in-cell bars), `BracketPod` + seats, `ChampionBanner`
- **Charts (SVG, theme-aware):** `BarChart`, `LineChart`, `Heatmap`

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
      series={[{ key: "win", label: "P(WIN)", color: "var(--accent)" }, { key: "pure", label: "PURE RACE", color: "var(--accent-2)" }]}
      rows={[{ label: "Radiation Sickness", values: { win: 69, pure: 57 } }]}
    />
  </Card>
</div>
```

Note: the system references Inter / JetBrains Mono but does not bundle the woff2 — it falls back to
system sans/mono unless you load those fonts yourself.
