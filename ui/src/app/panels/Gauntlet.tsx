import { useState } from "react";
import { Slider, SegmentedControl, Badge, Card, BarChart, LineChart, StatTable } from "../../components";
import type { Column } from "../../components";
import { getGauntlet, PALETTE } from "../data";
import type { GauntletData, GauntletRow } from "../data";
import { useDebouncedData, kfmt } from "../hooks";
import L from "../App.module.css";

const podOpts = [
  { value: "fast", label: "fast" },
  { value: "base", label: "base" },
  { value: "slow", label: "slow" },
];
const strictOpts = [
  { value: "decap", label: "decap" },
  { value: "table", label: "table" },
];

const cols: Column<GauntletRow>[] = [
  { key: "name", label: "Deck" },
  { key: "score", label: "Sc", mono: true, render: (r) => r.score ?? "" },
  { key: "decap_med", label: "decap", mono: true },
  { key: "table_med", label: "table", mono: true },
  { key: "pure", label: "pure", mono: true, render: (r) => `${(r.pure * 100).toFixed(0)}%` },
  { key: "disruption", label: "D@a", mono: true, render: (r) => `${(r.disruption * 100).toFixed(0)}%` },
  { key: "win", label: "P(WIN)", mono: true, bar: (r) => r.win, render: (r) => `${(r.win * 100).toFixed(0)}%` },
];

export function Gauntlet() {
  const [a, setA] = useState(0.3);
  const [pod, setPod] = useState("base");
  const [strict, setStrict] = useState("decap");
  const [trials, setTrials] = useState(12000);

  const { data, status } = useDebouncedData<GauntletData>(
    () => getGauntlet({ a, pod, strict: strict === "table", trials }),
    [a, pod, strict, trials],
    (d) => `${d.rows.length} decks · ${kfmt(d.params.trials)} trials`,
  );

  return (
    <div>
      <div className={L.controls}>
        <Slider label="Abolisher P(out)" value={a} min={0} max={1} step={0.05} display={a.toFixed(2)} onChange={setA} />
        <SegmentedControl aria-label="pod speed" options={podOpts} value={pod} onChange={setPod} />
        <SegmentedControl aria-label="win condition" options={strictOpts} value={strict} onChange={setStrict} />
        <Slider label="Trials" value={trials} min={2000} max={60000} step={2000} display={kfmt(trials)} onChange={setTrials} />
        <div className={L.statusRight}>
          <Badge variant={status.variant}>{status.text}</Badge>
        </div>
      </div>

      {data && (
        <>
          <div className={L.grid2}>
            <Card
              title="P(beat the T6-7 pod)"
              hint={data.params.which === "table" ? "· TABLE clock" : "· DECAP clock"}
            >
              <BarChart
                height={520}
                rows={data.rows.map((r) => ({ label: r.name, values: { win: r.win * 100, pure: r.pure * 100 } }))}
                series={[
                  { key: "win", label: "P(WIN)", color: "var(--accent)" },
                  { key: "pure", label: "PURE RACE", color: "var(--accent-2)" },
                ]}
              />
            </Card>
            <Card title="Abolisher sweep" hint="P(win) vs P(Abolisher out)">
              <LineChart
                height={520}
                series={data.rows.map((r, i) => ({
                  name: r.name,
                  color: PALETTE[i % PALETTE.length],
                  points: r.band.map((b, j) => ({ x: data.params.a_sweep[j], y: b * 100 })),
                }))}
                xLabel="P(Abolisher out)"
                yLabel="P(win) %"
              />
            </Card>
          </div>
          <Card title="The numbers">
            <StatTable columns={cols} rows={data.rows} rowKey={(r) => r.slug} />
          </Card>
        </>
      )}
    </div>
  );
}
