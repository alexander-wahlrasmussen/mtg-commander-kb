import { useEffect, useState } from "react";
import { SegmentedControl, Card, Chip, LineChart } from "../../components";
import { getClocks, PALETTE } from "../data";
import type { ClocksData } from "../data";
import { track } from "../inflight";
import L from "../App.module.css";

const whichOpts = [
  { value: "decap", label: "decap" },
  { value: "table", label: "table" },
];
const DEFAULT_SEL = ["radiation_sickness", "genome_project", "replication_crisis", "grand_design"];

export function Clocks() {
  const [data, setData] = useState<ClocksData | null>(null);
  const [which, setWhich] = useState<"decap" | "table">("decap");
  const [sel, setSel] = useState<Set<string>>(new Set(DEFAULT_SEL));

  useEffect(() => {
    track(getClocks()).then(setData).catch(() => {});
  }, []);

  if (!data) return null;

  const toggle = (slug: string) => {
    const n = new Set(sel);
    if (n.has(slug)) n.delete(slug);
    else n.add(slug);
    setSel(n);
  };

  const series = data.decks
    .map((d, i) => ({ d, i }))
    .filter(({ d }) => sel.has(d.slug))
    .map(({ d, i }) => ({
      name: d.name,
      color: PALETTE[i % PALETTE.length],
      points: d.grid.map((g, j) => ({ x: g, y: (which === "decap" ? d.decap : d.table)[j] })),
    }));

  return (
    <div>
      <div className={L.controls}>
        <SegmentedControl
          aria-label="curve"
          options={whichOpts}
          value={which}
          onChange={(v) => setWhich(v as "decap" | "table")}
        />
        <div className={L.chips}>
          {data.decks.map((d, i) => (
            <Chip
              key={d.slug}
              label={d.name}
              active={sel.has(d.slug)}
              color={PALETTE[i % PALETTE.length]}
              onClick={() => toggle(d.slug)}
            />
          ))}
        </div>
      </div>
      <Card title="Clock curves" hint={`cumulative P(${which} ≤ turn) %`}>
        <LineChart height={520} series={series} xLabel="turn" yLabel={`cum P(${which} ≤ turn) %`} refLineY={50} />
      </Card>
    </div>
  );
}
