// Deck Doctor — the roster pre-flight as a triage board. One row per deck from
// the SAME quiet doctor the CLI's --all table runs; a cell is a check, red means
// fix it before the deck hits a table. Click a row to read the doctor's notes
// (the non-OK messages behind the cells). Advisory columns (gap / fp% / frg% and
// the vitals) are context, not verdicts — they never flip a row red.
import { Fragment, useState } from "react";
import { getDoctor } from "../data";
import type { DoctorData, DoctorRow } from "../data";
import { usePageData } from "../hooks";
import { Masthead } from "../pagekit";
import s from "../pages.module.css";

const TAG_COLOR: Record<string, string> = {
  PASS: "var(--good)", WARN: "var(--gold)", FAIL: "var(--acc)", ERR: "var(--acc)",
};
const SEV_COLOR: Record<string, string> = {
  ERROR: "var(--acc)", WARN: "var(--gold)", INFO: "var(--ink3)",
};

const mono9 = {
  fontFamily: "var(--mono)", fontSize: 9.5, letterSpacing: ".06em",
  textTransform: "uppercase",
} as const;

function TagChip({ tag }: { tag: string }) {
  const c = TAG_COLOR[tag] ?? "var(--ink)";
  return (
    <span style={{ ...mono9, fontWeight: 600, color: c, border: `1.5px solid ${c}`, padding: "2px 7px" }}>
      {tag}
    </span>
  );
}

/** A hard-check cell: all-clear renders as a quiet dot, a problem as a red count. */
function Flag({ v, bad }: { v: number | undefined; bad: boolean }) {
  if (v === undefined) return <td style={{ textAlign: "center", color: "var(--faint)" }}>—</td>;
  return (
    <td style={{ textAlign: "center", fontFamily: "var(--mono)", fontSize: 12, fontWeight: bad ? 700 : 400, color: bad ? "var(--acc)" : "var(--faint)" }}>
      {bad ? v : "·"}
    </td>
  );
}

/** An advisory cell: plain muted number (amber when flagged), never a verdict. */
function Info({ text, amber }: { text: string; amber?: boolean }) {
  return (
    <td style={{ textAlign: "center", fontFamily: "var(--mono)", fontSize: 12, color: amber ? "var(--gold)" : "var(--muted)" }}>
      {text}
    </td>
  );
}

function NotesRow({ row, cols }: { row: DoctorRow; cols: number }) {
  const notes = row.notes.filter((n) => n.sev !== "INFO");
  const info = row.notes.filter((n) => n.sev === "INFO");
  return (
    <tr>
      <td colSpan={cols} style={{ background: "var(--paper2)", padding: "12px 18px 14px", borderBottom: "1.5px solid var(--ink)" }}>
        {[...notes, ...info].map((n, i) => (
          <div key={i} style={{ display: "grid", gridTemplateColumns: "52px 172px 1fr", gap: 10, alignItems: "baseline", padding: "3px 0", fontSize: 12.5, lineHeight: 1.45 }}>
            <span style={{ ...mono9, fontWeight: 600, color: SEV_COLOR[n.sev] ?? "var(--ink3)" }}>{n.sev}</span>
            <span style={{ ...mono9, color: "var(--ink3)" }}>{n.sec}</span>
            <span style={{ color: "var(--ink2)" }}>{n.msg}</span>
          </div>
        ))}
        {row.notes.length === 0 && (
          <span style={{ ...mono9, color: "var(--ink3)" }}>all checks clear — nothing to report</span>
        )}
      </td>
    </tr>
  );
}

export function Doctor() {
  const { data, error } = usePageData<DoctorData>(getDoctor);
  const [open, setOpen] = useState<string | null>(null);
  if (error) return <div className={s.error}>error: {error}</div>;
  if (!data) return <div className={s.loading}>examining the roster…</div>;

  const vitals = data.vitals;
  const nCols = 13 + (vitals ? 3 : 0);
  const th = (label: string, title?: string) => (
    <th key={label} title={title} style={{ textAlign: "center", whiteSpace: "nowrap" }}>{label}</th>
  );

  return (
    <div className={s.page}>
      <Masthead
        kicker="Deck Doctor · pre-flight"
        title="Health Board"
        right={
          <div className={s.tierChips}>
            {([["FAIL", data.counts.fail], ["WARN", data.counts.warn], ["PASS", data.counts.ok]] as const)
              .filter(([, n]) => n > 0)
              .map(([t, n]) => (
                <span key={t} className={s.tierChip} style={{ color: TAG_COLOR[t] }}>
                  <i style={{ background: TAG_COLOR[t] }} />
                  {t} {n}
                </span>
              ))}
          </div>
        }
      />

      <p className={s.tierLede}>
        The mechanical pre-flight (<code>deck_doctor.py --all</code>) over the active roster —
        size, singleton, banlist, colour identity, house rules, Game Changers and Summary
        clock drift. <strong style={{ color: "var(--acc)" }}>Red = fix before the deck hits a table.</strong>{" "}
        The right-hand columns are advisory context (interaction holes, engine footprint,
        wipe fragility{vitals ? ", keepable hands, smoothness" : ""}) — screening lenses, not verdicts.
        Click a row for the doctor's notes.
      </p>

      <table className={s.deckTable}>
        <thead>
          <tr>
            <th style={{ width: 66 }}>Verdict</th>
            <th>Deck</th>
            {th("size", "100 cards exactly")}
            {th("sing", "singleton violations")}
            {th("ill", "Commander-banned cards")}
            {th("off", "off-colour-identity cards")}
            {th("MLD", "house-banned mass land destruction")}
            {th("GC", "Game Changers (max 3)")}
            {th("brk", "estimated WotC bracket")}
            {th("drift", "Summary Clock: line vs lab medians")}
            {th("gap", "interaction-coverage holes (0-6)")}
            {th("fp%", "nonland cards dead without the engine")}
            {th("frg%", "nonland permanents on wipe-vulnerable types")}
            {vitals && th("keep%", "keepable opening hands (deck_sim)")}
            {vitals && th("dead", "mean dead turns T1-10")}
            {vitals && th("hlb%", "hellbent by T8 — lower is smoother")}
          </tr>
        </thead>
        <tbody>
          {data.rows.map((r) => {
            const f = r.facts;
            const expanded = open === r.slug;
            return (
              <Fragment key={r.slug}>
                <tr
                  className={s.tierRow}
                  style={{ cursor: "pointer", background: expanded ? "var(--paper2)" : undefined }}
                  onClick={() => setOpen(expanded ? null : r.slug)}
                >
                  <td><TagChip tag={r.tag} /></td>
                  <td>
                    <div className={s.deckName}>
                      {r.name}
                      <span style={{ ...mono9, color: "var(--ink3)", marginLeft: 8 }}>{expanded ? "▾" : "▸"}</span>
                    </div>
                  </td>
                  <td style={{ textAlign: "center", fontFamily: "var(--mono)", fontSize: 12, fontWeight: f.size === 100 ? 400 : 700, color: f.size === 100 ? "var(--faint)" : "var(--acc)" }}>
                    {f.size === 100 ? "·" : f.size ?? "—"}
                  </td>
                  <Flag v={f.singleton ?? 0} bad={(f.singleton ?? 0) > 0} />
                  <Flag v={f.illegal ?? 0} bad={(f.illegal ?? 0) > 0} />
                  <Flag v={f.offcolor ?? 0} bad={(f.offcolor ?? 0) > 0} />
                  <Flag v={f.mld ?? 0} bad={(f.mld ?? 0) > 0} />
                  <td style={{ textAlign: "center", fontFamily: "var(--mono)", fontSize: 12, fontWeight: (f.gc ?? 0) > 3 ? 700 : 400, color: (f.gc ?? 0) > 3 ? "var(--acc)" : "var(--muted)" }}>
                    {f.gc ?? "—"}/3
                  </td>
                  <Info text={f.bracket != null ? String(f.bracket) : "—"} />
                  <Flag v={f.drift} bad={(f.drift ?? 0) > 0} />
                  <Info text={f.intxn_gaps != null ? (f.intxn_gaps === 0 ? "·" : String(f.intxn_gaps)) : "—"} amber={(f.intxn_gaps ?? 0) > 0} />
                  <Info text={f.footprint_pct != null ? `${f.footprint_pct}` : "—"} />
                  <Info text={f.fragility_pct != null ? `${f.fragility_pct}` : "—"} />
                  {vitals && <Info text={f.keepable != null ? `${f.keepable}` : "—"} />}
                  {vitals && <Info text={f.mean_dead != null ? f.mean_dead.toFixed(1) : "—"} />}
                  {vitals && <Info text={f.hellbent8 != null ? `${f.hellbent8}` : "—"} />}
                </tr>
                {expanded && <NotesRow row={r} cols={nCols} />}
              </Fragment>
            );
          })}
        </tbody>
      </table>

      <p className={s.tierFoot}>
        Same checks, same code path as the CLI (<code>Report(quiet=True)</code>) — a green board
        here means <code>--all</code> prints PASS down the line. Buildability (owned / buy €) is
        deliberately absent: this page is publicly hosted and carries no collection data. Drill
        deeper: <code>python scripts/deck_doctor.py &lt;slug&gt; --deep</code>.
      </p>
    </div>
  );
}
