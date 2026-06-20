import { useElementWidth } from "./useElementWidth";
import styles from "./Chart.module.css";

export interface BarSeries {
  key: string;
  label: string;
  color: string;
}
export interface BarRow {
  label: string;
  values: Record<string, number>;
}
export interface BarChartProps {
  rows: BarRow[];
  series: BarSeries[];
  /** Axis max (defaults to 100 for percentages). */
  max?: number;
  unit?: string;
  height?: number;
  /** Print the first series' value at the bar end. */
  showValues?: boolean;
}

/** Horizontal grouped bar chart (e.g. P(WIN) vs PURE RACE per deck). */
export function BarChart({
  rows,
  series,
  max = 100,
  unit = "%",
  height,
  showValues = true,
}: BarChartProps) {
  const [ref, width] = useElementWidth<HTMLDivElement>();
  const m = { left: 150, right: 22, top: 6, bottom: 26 };
  const h = height ?? Math.max(220, rows.length * (series.length * 13 + 12) + m.top + m.bottom);
  const pw = Math.max(10, width - m.left - m.right);
  const ph = h - m.top - m.bottom;
  const band = ph / rows.length;
  const barH = Math.min(15, (band - 6) / series.length);
  const x = (v: number) => (v / max) * pw;
  const ticks = [0, 0.25, 0.5, 0.75, 1].map((f) => f * max);

  return (
    <div className={styles.chart} ref={ref}>
      <svg width={width} height={h} role="img">
        {ticks.map((t) => (
          <g key={t}>
            <line
              x1={m.left + x(t)}
              x2={m.left + x(t)}
              y1={m.top}
              y2={m.top + ph}
              className={styles.grid}
            />
            <text x={m.left + x(t)} y={m.top + ph + 17} className={styles.tick} textAnchor="middle">
              {t}
              {unit}
            </text>
          </g>
        ))}
        {rows.map((r, i) => {
          const y0 = m.top + i * band + (band - barH * series.length) / 2;
          return (
            <g key={r.label}>
              <text x={m.left - 10} y={y0 + (barH * series.length) / 2} className={styles.rowLabel} textAnchor="end" dominantBaseline="middle">
                {r.label}
              </text>
              {series.map((s, si) => {
                const v = r.values[s.key] ?? 0;
                const y = y0 + si * barH;
                return (
                  <g key={s.key}>
                    <rect
                      x={m.left}
                      y={y + 1}
                      width={x(v)}
                      height={barH - 2}
                      rx={3}
                      fill={s.color}
                    />
                    {showValues && si === 0 && (
                      <text x={m.left + x(v) + 5} y={y + barH / 2} className={styles.barVal} dominantBaseline="middle">
                        {v.toFixed(0)}
                        {unit}
                      </text>
                    )}
                  </g>
                );
              })}
            </g>
          );
        })}
      </svg>
      <div className={styles.legend}>
        {series.map((s) => (
          <span key={s.key} className={styles.legendItem}>
            <span className={styles.swatch} style={{ background: s.color }} />
            {s.label}
          </span>
        ))}
      </div>
    </div>
  );
}
