import type { ReactNode } from "react";
import styles from "./StatTable.module.css";

export interface Column<Row> {
  key: string;
  label: string;
  align?: "left" | "right";
  /** Monospace, tabular figures (for numbers). */
  mono?: boolean;
  /** Custom cell content. Defaults to String(row[key]). */
  render?: (row: Row) => ReactNode;
  /** Draw a horizontal fill behind the cell, scaled to this value / column max. */
  bar?: (row: Row) => number;
}

export interface StatTableProps<Row> {
  columns: Column<Row>[];
  rows: Row[];
  rowKey?: (row: Row, i: number) => string | number;
}

const colAlign = <Row,>(c: Column<Row>) => c.align ?? (c.mono || c.bar ? "right" : "left");

/** A dense data table; columns can render as monospace figures or in-cell bars. */
export function StatTable<Row>({ columns, rows, rowKey }: StatTableProps<Row>) {
  const maxes = columns.map((c) =>
    c.bar ? Math.max(1e-9, ...rows.map((r) => c.bar!(r))) : 1,
  );
  return (
    <div className={styles.wrap}>
      <table className={styles.table}>
        <thead>
          <tr>
            {columns.map((c) => (
              <th key={c.key} style={{ textAlign: colAlign(c) }}>
                {c.label}
              </th>
            ))}
          </tr>
        </thead>
        <tbody>
          {rows.map((r, i) => (
            <tr key={rowKey ? rowKey(r, i) : i}>
              {columns.map((c, ci) => (
                <td
                  key={c.key}
                  className={[c.mono ? styles.num : "", c.bar ? styles.barCell : ""]
                    .filter(Boolean)
                    .join(" ")}
                  style={{ textAlign: colAlign(c) }}
                >
                  {c.bar && (
                    <span
                      className={styles.fill}
                      style={{ width: `${(c.bar(r) / maxes[ci]) * 100}%` }}
                    />
                  )}
                  <span className={styles.inner}>
                    {c.render ? c.render(r) : String((r as Record<string, unknown>)[c.key] ?? "")}
                  </span>
                </td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
