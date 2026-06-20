import { useState } from "react";
import {
  Slider, SegmentedControl, Badge, Card, EmptyState, BracketPod, ChampionBanner, StatTable,
} from "../../components";
import type { Column, Medal } from "../../components";
import { getChampionship } from "../data";
import type { ChampData, SeasonRow } from "../data";
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

function champNote(d: ChampData) {
  let n = `Runner-up: ${d.notes.runner_up.name} (#${d.notes.runner_up.seed}).`;
  if (d.notes.upset) n += ` ⚡ UPSET — the #${d.champion.seed} seed took the crown.`;
  if (d.notes.cinderella) n += ` ✨ Cinderella: ${d.notes.cinderella.name} (#${d.notes.cinderella.seed}).`;
  if (d.params.swapped && d.notes.changed.length) n += ` Swaps: ${d.notes.changed.join(", ")}.`;
  return n;
}

export function Championship() {
  const [trials, setTrials] = useState(15000);
  const [season, setSeason] = useState(40000);
  const [tg, setTg] = useState(10);
  const [swapped, setSwapped] = useState("0");
  const [data, setData] = useState<ChampData | null>(null);
  const [status, setStatus] = useState<Status>({ text: "idle", variant: "default" });

  const run = async () => {
    setStatus({ text: "simulating…", variant: "busy" });
    try {
      const d = await track(
        getChampionship({ trials, season_trials: season, t_grind: tg, swapped: swapped === "1" }),
      );
      setData(d);
      setStatus({ text: "done", variant: "ok" });
    } catch (e) {
      setStatus({ text: "error: " + (e as Error).message, variant: "err" });
    }
  };

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

      {!data ? (
        <EmptyState glyph="🏆" title="No tournament run yet">
          Set the trials and T_grind, then press <strong>Run the tournament</strong> to seed 16 decks,
          play 4 group pods, and crown a champion.
        </EmptyState>
      ) : (
        <>
          <div style={{ marginBottom: 16 }}>
            <ChampionBanner name={data.champion.name} seed={data.champion.seed} note={champNote(data)} />
          </div>
          <div className={L.bracket}>
            {data.groups.map((g) => (
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
              seats={data.final.map((s) => ({
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
