import { useState } from "react";
import { Slider, SegmentedControl, Badge, Card, EmptyState, Heatmap } from "../../components";
import { getLocks } from "../data";
import type { LocksData } from "../data";
import { track } from "../inflight";
import { kfmt } from "../hooks";
import type { Status } from "../hooks";
import L from "../App.module.css";

const strictOpts = [
  { value: "decap", label: "decap" },
  { value: "table", label: "table" },
];
const podOpts = [
  { value: "fast", label: "fast" },
  { value: "base", label: "base" },
  { value: "slow", label: "slow" },
];

function cellText(lift: number) {
  return lift >= 0.5 ? `+${lift.toFixed(0)}` : lift > -0.5 ? "·" : lift.toFixed(0);
}

export function Locks() {
  const [a, setA] = useState(0.3);
  const [r, setR] = useState(0.25);
  const [strict, setStrict] = useState("decap");
  const [pod, setPod] = useState("base");
  const [trials, setTrials] = useState(2000);
  const [data, setData] = useState<LocksData | null>(null);
  const [status, setStatus] = useState<Status>({ text: "idle", variant: "default" });

  const run = async () => {
    setStatus({ text: "measuring…", variant: "busy" });
    try {
      const d = await track(getLocks({ a, r, strict: strict === "table", pod, trials }));
      setData(d);
      setStatus({ text: `${d.rows.length} decks · ${kfmt(d.params.trials)} trials · ${d.params.which}`, variant: "ok" });
    } catch (e) {
      setStatus({ text: "error: " + (e as Error).message, variant: "err" });
    }
  };

  const rows = data
    ? [...data.rows].reverse().map((row) => ({
        label: `${row.name}  ·  ${(row.cur * 100).toFixed(0)}%`,
        cells: row.cells.map((c) => ({ value: c.lift, text: cellText(c.lift), owned: c.owned })),
      }))
    : [];
  const cols = data ? data.locks.map((l) => data.abbr[l] || l) : [];

  return (
    <div>
      <div className={L.controls}>
        <Slider label="Abolisher P(out)" value={a} min={0} max={1} step={0.05} display={a.toFixed(2)} onChange={setA} />
        <Slider label="Pod removes lock /turn" value={r} min={0} max={1} step={0.05} display={r.toFixed(2)} onChange={setR} />
        <SegmentedControl aria-label="win condition" options={strictOpts} value={strict} onChange={setStrict} />
        <SegmentedControl aria-label="pod speed" options={podOpts} value={pod} onChange={setPod} />
        <Slider label="Trials" value={trials} min={500} max={8000} step={500} display={kfmt(trials)} onChange={setTrials} />
        <button className={L.run} onClick={run}>▶ Run lock sweep</button>
        <div className={L.statusRight}>
          <Badge variant={status.variant}>{status.text}</Badge>
        </div>
      </div>

      {!data ? (
        <EmptyState glyph="🔒" title="No lock sweep run yet">
          Press <strong>Run lock sweep</strong> to measure what each persistent lock buys each deck vs
          the pod (tutored-availability ceiling). Heavy compute in live mode — give it a few seconds.
        </EmptyState>
      ) : (
        <Card title="Lock-lift heatmap" hint="P(win) points added vs the no-lock baseline · ringed cell = deck already runs it">
          <Heatmap rows={rows} cols={cols} />
        </Card>
      )}
    </div>
  );
}
