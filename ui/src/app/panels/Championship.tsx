import { useState } from "react";
import {
  Slider, SegmentedControl, Badge, Card, EmptyState, BracketPod, ChampionBanner, StatTable,
} from "../../components";
import type { Column, Medal } from "../../components";
import { getChampionship, mode } from "../data";
import type { ChampData, ChampDraw, SeasonRow } from "../data";
import { track } from "../inflight";
import { kfmt } from "../hooks";
import type { Status } from "../hooks";
import L from "../App.module.css";

const swapOpts = [
  { value: "0", label: "current" },
  { value: "1", label: "swapped" },
];

const seasonCols: Column<SeasonRow>[] = [
  { key: "seed", label: "Seed", mono: true, render: (r) => `#${r.seed}` },
  { key: "name", label: "Deck", render: (r) => r.name + (r.swap ? " ←swap" : "") },
  { key: "table_med", label: "table", mono: true },
  { key: "never", label: "never", mono: true, render: (r) => `${r.never}%` },
  { key: "dura", label: "dura", mono: true, render: (r) => r.dura.toFixed(2) },
  { key: "pwin", label: "P(win)", mono: true, bar: (r) => r.pwin, render: (r) => `${r.pwin.toFixed(0)}%` },
];

function champNote(d: ChampDraw, swapped: boolean) {
  let n = `Runner-up: ${d.notes.runner_up.name} (#${d.notes.runner_up.seed}).`;
  if (d.notes.upset) n += ` ⚡ UPSET — the #${d.champion.seed} seed took the crown.`;
  if (d.notes.cinderella) n += ` ✨ Cinderella: ${d.notes.cinderella.name} (#${d.notes.cinderella.seed}).`;
  if (swapped && d.notes.changed.length) n += ` Swaps: ${d.notes.changed.join(", ")}.`;
  return n;
}

export function Championship() {
  const [trials, setTrials] = useState(15000);
  const [season, setSeason] = useState(40000);
  const [tg, setTg] = useState(10);
  const [swapped, setSwapped] = useState("0");
  const [data, setData] = useState<ChampData | null>(null);
  const [drawIdx, setDrawIdx] = useState(0);
  const [status, setStatus] = useState<Status>({ text: "idle", variant: "default" });

  const fetchChamp = () =>
    track(getChampionship({ trials, season_trials: season, t_grind: tg, swapped: swapped === "1" }));

  const run = async () => {
    setStatus({ text: "simulating…", variant: "busy" });
    try {
      setData(await fetchChamp());
      setDrawIdx(0);
      setStatus({ text: "done", variant: "ok" });
    } catch (e) {
      setStatus({ text: "error: " + (e as Error).message, variant: "err" });
    }
  };

  // Re-draw: static cycles the baked sample draws; live fetches a fresh draw and
  // appends it to the in-memory history (the season ranking is unchanged).
  const redraw = async () => {
    if (!data) return;
    if (mode.static) {
      setDrawIdx((i) => (i + 1) % data.draws.length);
      return;
    }
    setStatus({ text: "drawing…", variant: "busy" });
    try {
      const d = await fetchChamp();
      setData({ ...data, draws: [...data.draws, ...d.draws] });
      setDrawIdx(data.draws.length);
      setStatus({ text: "done", variant: "ok" });
    } catch (e) {
      setStatus({ text: "error: " + (e as Error).message, variant: "err" });
    }
  };

  const idx = data ? Math.min(drawIdx, data.draws.length - 1) : 0;
  const cur: ChampDraw | null = data ? data.draws[idx] : null;

  return (
    <div>
      <div className={L.controls}>
        <Slider label="Playoff trials" value={trials} min={2000} max={60000} step={1000} display={kfmt(trials)} onChange={setTrials} />
        <Slider label="Season trials" value={season} min={5000} max={120000} step={5000} display={kfmt(season)} onChange={setSeason} />
        <Slider label="T_grind" value={tg} min={6} max={14} step={1} display={String(tg)} onChange={setTg} />
        <SegmentedControl aria-label="pending swaps" options={swapOpts} value={swapped} onChange={setSwapped} />
        <button className={L.run} onClick={run}>▶ Run the tournament</button>
        <div className={L.statusRight}>
          <Badge variant={status.variant}>{status.text}</Badge>
        </div>
      </div>

      {!data || !cur ? (
        <EmptyState glyph="🏆" title="No tournament run yet">
          Set the trials and T_grind, then press <strong>Run the tournament</strong> to seed the roster,
          draw 4 group pods at random, and crown a champion.
        </EmptyState>
      ) : (
        <>
          <div style={{ display: "flex", alignItems: "center", gap: 12, marginBottom: 12 }}>
            <button className={L.run} onClick={redraw}>🎲 Re-draw</button>
            <Badge>{`draw ${idx + 1} of ${data.draws.length} · seed ${cur.draw_seed}`}</Badge>
            <span style={{ opacity: 0.7, fontSize: ".85em" }}>
              {mode.static ? "baked sample draws — Re-draw cycles them" : "live — Re-draw reshuffles the pods"}
            </span>
          </div>
          <div style={{ marginBottom: 16 }}>
            <ChampionBanner name={cur.champion.name} seed={cur.champion.seed} note={champNote(cur, data.params.swapped)} />
          </div>
          <div className={L.bracket}>
            {cur.groups.map((g) => (
              <BracketPod
                key={g.pod}
                title={`Pod ${g.pod}`}
                hint="win share"
                seats={g.seats.map((s) => ({ name: s.name, seed: s.seed, share: s.share, advances: s.advances }))}
              />
            ))}
          </div>
          <div style={{ marginBottom: 16 }}>
            <BracketPod
              final
              title="The Final Four"
              hint="group winners"
              seats={cur.final.map((s) => ({
                name: s.name,
                seed: s.seed,
                share: s.share,
                medal: (s.medal || undefined) as Medal | undefined,
              }))}
            />
          </div>
          <Card title="Regular season" hint="seeded by P(win | random 4-seat pod)">
            <StatTable columns={seasonCols} rows={data.season} rowKey={(r) => r.slug} />
          </Card>
        </>
      )}
    </div>
  );
}
