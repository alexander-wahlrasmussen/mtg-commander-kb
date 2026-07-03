// Matchups — the deck × measured-opponent matrix (Backlog #13 Phase 3). Each cell
// races a roster deck against ONE deck of his measured stable via pg.simulate_vs
// (per-opponent attempt curves from the opponent labs), so the per-opponent SPREAD
// is visible — the headline the weighted blend hides: H&K is the stomp threat, and
// a deck's H&K column can sit 20-45pp below its Acererak column.
import { useState } from "react";
import { SegmentedControl, Slider, Badge, Card, Heatmap } from "../../components";
import { getMatchup } from "../data";
import type { MatchupData } from "../data";
import { useDebouncedData, kfmt } from "../hooks";
import L from "../App.module.css";

const strictOpts = [
  { value: "decap", label: "decap" },
  { value: "table", label: "table" },
];

export function Matchups() {
  const [strict, setStrict] = useState("decap");
  const [trials, setTrials] = useState(12000);

  const { data, status } = useDebouncedData<MatchupData>(
    () => getMatchup({ strict: strict === "table", trials }),
    [strict, trials],
    (d) => `${d.rows.length} decks × ${d.opponents.length} opponents · ${kfmt(d.params.trials)} trials`,
  );

  const cols = data ? [...data.opponents.map((o) => `${o.label} ${o.med}`), "BLEND"] : [];
  const rows = data
    ? data.rows.map((r) => ({
        label: r.name,
        cells: [
          ...data.opponents.map((o) => ({ value: r.per[o.key] - 50, text: `${r.per[o.key]}` })),
          { value: r.blend - 50, text: `${r.blend}` },
        ],
      }))
    : [];

  return (
    <div>
      <div className={L.controls}>
        <SegmentedControl aria-label="win condition" options={strictOpts} value={strict} onChange={setStrict} />
        <Slider label="Trials" value={trials} min={2000} max={40000} step={2000} display={kfmt(trials)} onChange={setTrials} />
        <div className={L.statusRight}>
          <Badge variant={status.variant}>{status.text}</Badge>
        </div>
      </div>

      {data && (
        <>
          <Card
            title="Who beats whom — his measured stable"
            hint="cell = P(win) % · green = favoured, vermillion = unfavoured, paper ≈ coin flip"
          >
            <Heatmap rows={rows} cols={cols} rowHeight={28} />
          </Card>

          <Card title="The stable" hint="per-opponent measured attempt curves (opp_*_lab) · weights = observed rotation">
            <div style={{ display: "grid", gap: 10, padding: "4px 2px 6px" }}>
              {data.opponents.map((o) => (
                <div key={o.key} style={{ display: "grid", gridTemplateColumns: "180px 64px 52px 1fr", gap: 12, alignItems: "baseline", fontSize: 12.5, lineHeight: 1.45 }}>
                  <strong style={{ fontFamily: "var(--disp, inherit)", fontSize: 13 }}>{o.name}</strong>
                  <span style={{ fontFamily: "var(--mono, monospace)", fontSize: 11, color: "var(--muted, #666)" }}>w {Math.round(o.weight * 100)}%</span>
                  <span style={{ fontFamily: "var(--mono, monospace)", fontSize: 11, color: "var(--muted, #666)" }}>{o.med}</span>
                  <span style={{ color: "var(--muted, #666)" }}>{o.note}</span>
                </div>
              ))}
            </div>
          </Card>

          <p style={{ fontSize: 12.5, lineHeight: 1.55, color: "var(--muted, #666)", maxWidth: 760, margin: "14px 2px 4px" }}>
            <strong>Read the spread, not the blend</strong> — the rotation-weighted BLEND hides the
            stomp deck: pick your deck for the opponent he actually brings, and mind the H&K column.
            Opponent clocks are PROXY reconstructions (never citation-grade); the Ur-Dragon column is
            his <em>unblocked</em> goldfish ceiling — the defended, fair-game matchup inverts toward
            grind/wrath decks (vs_dragon_lab owns that axis). Acererak's curve is a floor.
          </p>
        </>
      )}
    </div>
  );
}
