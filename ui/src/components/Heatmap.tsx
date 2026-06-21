import { useElementWidth } from "./useElementWidth";
import styles from "./Chart.module.css";

export interface HeatCell {
  value: number;
  text: string;
}
export interface HeatRow {
  label: string;
  cells: HeatCell[];
}
export interface HeatmapProps {
  rows: HeatRow[];
  cols: string[];
  rowHeight?: number;
}

// Newsprint diverging ramp: vermillion (negative) → paper (mid) → olive-good (positive).
const NEG = [198, 58, 27];    // --acc #c63a1b
const MID = [241, 236, 223];  // --paper2 #f1ecdf
const POS = [79, 107, 30];    // --good #4f6b1e
const lerp = (a: number[], b: number[], t: number) => a.map((x, i) => Math.round(x + (b[i] - x) * t));
function diverging(v: number, maxabs: number) {
  const t = Math.max(0, Math.min(1, (v + maxabs) / (2 * maxabs)));
  const c = t < 0.5 ? lerp(NEG, MID, t / 0.5) : lerp(MID, POS, (t - 0.5) / 0.5);
  return `rgb(${c[0]} ${c[1]} ${c[2]})`;
}

/** Diverging vermillion→paper→olive matrix — e.g. deck × lock win-probability lift. */
export function Heatmap({ rows, cols, rowHeight = 30 }: HeatmapProps) {
  const [ref, width] = useElementWidth<HTMLDivElement>();
  const m = { left: 200, right: 14, top: 26, bottom: 6 };
  const pw = Math.max(10, width - m.left - m.right);
  const cw = pw / Math.max(1, cols.length);
  const height = m.top + m.bottom + rows.length * rowHeight;
  const maxabs = Math.max(3, ...rows.flatMap((r) => r.cells.map((c) => Math.abs(c.value))));

  return (
    <div className={styles.chart} ref={ref}>
      <svg width={width} height={height} role="img">
        {cols.map((c, ci) => (
          <text key={c} x={m.left + ci * cw + cw / 2} y={16} className={styles.colLabel} textAnchor="middle">
            {c}
          </text>
        ))}
        {rows.map((r, ri) => {
          const y = m.top + ri * rowHeight;
          return (
            <g key={r.label}>
              <text x={m.left - 10} y={y + rowHeight / 2} className={styles.rowLabel} textAnchor="end" dominantBaseline="middle">
                {r.label}
              </text>
              {r.cells.map((cell, ci) => (
                <g key={ci}>
                  <rect
                    x={m.left + ci * cw + 1.5}
                    y={y + 1.5}
                    width={cw - 3}
                    height={rowHeight - 3}
                    rx={4}
                    fill={diverging(cell.value, maxabs)}
                  />
                  <text
                    x={m.left + ci * cw + cw / 2}
                    y={y + rowHeight / 2}
                    className={styles.heatText}
                    textAnchor="middle"
                    dominantBaseline="middle"
                  >
                    {cell.text}
                  </text>
                </g>
              ))}
            </g>
          );
        })}
      </svg>
    </div>
  );
}
