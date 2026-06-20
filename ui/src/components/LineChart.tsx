import { useElementWidth } from "./useElementWidth";
import styles from "./Chart.module.css";

export interface LinePoint {
  x: number;
  y: number;
}
export interface LineSeries {
  name: string;
  color: string;
  points: LinePoint[];
}
export interface LineChartProps {
  series: LineSeries[];
  height?: number;
  xLabel?: string;
  yLabel?: string;
  yMax?: number;
  /** Explicit x tick positions; defaults to the union of series x's. */
  xTicks?: number[];
  /** Dotted horizontal reference line (e.g. the 50% mark). */
  refLineY?: number;
  unit?: string;
}

/** Multi-series line chart with markers, gridlines and a legend (clock curves, sweeps). */
export function LineChart({
  series,
  height = 360,
  xLabel,
  yLabel,
  yMax = 100,
  xTicks,
  refLineY,
  unit = "",
}: LineChartProps) {
  const [ref, width] = useElementWidth<HTMLDivElement>();
  const m = { left: 52, right: 18, top: 10, bottom: 40 };
  const pw = Math.max(10, width - m.left - m.right);
  const ph = height - m.top - m.bottom;

  const allX = series.flatMap((s) => s.points.map((p) => p.x));
  const xMin = allX.length ? Math.min(...allX) : 0;
  const xMax = allX.length ? Math.max(...allX) : 1;
  const xs = xTicks ?? Array.from(new Set(allX)).sort((a, b) => a - b);
  const px = (v: number) => m.left + ((v - xMin) / (xMax - xMin || 1)) * pw;
  const py = (v: number) => m.top + ph - (v / yMax) * ph;
  const yTicks = [0, 0.25, 0.5, 0.75, 1].map((f) => f * yMax);

  return (
    <div className={styles.chart} ref={ref}>
      <svg width={width} height={height} role="img">
        {yTicks.map((t) => (
          <g key={t}>
            <line x1={m.left} x2={m.left + pw} y1={py(t)} y2={py(t)} className={styles.grid} />
            <text x={m.left - 8} y={py(t)} className={styles.tick} textAnchor="end" dominantBaseline="middle">
              {t}
            </text>
          </g>
        ))}
        {xs.map((t) => (
          <text key={t} x={px(t)} y={m.top + ph + 16} className={styles.tick} textAnchor="middle">
            {t}
          </text>
        ))}
        {refLineY != null && (
          <line x1={m.left} x2={m.left + pw} y1={py(refLineY)} y2={py(refLineY)} className={styles.refLine} />
        )}
        {yLabel && (
          <text transform={`translate(14 ${m.top + ph / 2}) rotate(-90)`} className={styles.axisLabel} textAnchor="middle">
            {yLabel}
          </text>
        )}
        {xLabel && (
          <text x={m.left + pw / 2} y={height - 4} className={styles.axisLabel} textAnchor="middle">
            {xLabel}
          </text>
        )}
        {series.map((s) => {
          const d = s.points
            .map((p, i) => `${i === 0 ? "M" : "L"} ${px(p.x)} ${py(p.y)}`)
            .join(" ");
          return (
            <g key={s.name}>
              <path d={d} className={styles.line} stroke={s.color} />
              {s.points.map((p, i) => (
                <circle key={i} cx={px(p.x)} cy={py(p.y)} r={3} fill={s.color} className={styles.marker} />
              ))}
            </g>
          );
        })}
      </svg>
      <div className={styles.legend}>
        {series.map((s) => (
          <span key={s.name} className={styles.legendItem}>
            <span className={styles.swatch} style={{ background: s.color }} />
            {s.name}
            {unit}
          </span>
        ))}
      </div>
    </div>
  );
}
