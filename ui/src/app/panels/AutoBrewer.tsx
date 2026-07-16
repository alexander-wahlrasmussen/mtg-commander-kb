import { useMemo, useState } from "react";
import { getAutobrew } from "../data";
import type { AutobrewData, AutobrewRow } from "../data";
import { usePageData } from "../hooks";
import { Masthead, Pips } from "../pagekit";
import s from "../pages.module.css";

// Combo-type accent inks (newsprint earth tones). Keyed by auto_brewer's
// _combo_category labels; the fallback covers "Infinite loop" / "Combo engine".
const TYPE_COLOR: Record<string, string> = {
  "Instant win": "#9d0006",
  "Infinite damage": "#b8331f",
  "Infinite drain": "#8f3f71",
  "Infinite mill": "#6f5577",
  "Infinite tokens": "#5f7510",
  "Infinite mana": "#b57614",
  "Infinite draw": "#076678",
};
const typeColor = (t: string | null) => (t && TYPE_COLOR[t]) || "#7c6f64";

// Composite axis caps (auto_brewer.composite weights) — so each bar reads
// against the points it could have contributed, not the total.
const AXIS_META: Record<string, { label: string; max: number }> = {
  keepable: { label: "Keepable", max: 20 },
  flow: { label: "Flow", max: 15 },
  colors: { label: "Colors", max: 10 },
  ramp: { label: "Ramp", max: 10 },
  draw: { label: "Draw", max: 10 },
  assembly: { label: "Assembly", max: 25 },
  combo_depth: { label: "Combo depth", max: 10 },
};
const AXIS_ORDER = ["assembly", "combo_depth", "keepable", "flow", "colors", "ramp", "draw"];

const COLORS = ["W", "U", "B", "R", "G", "C"];
const scoreColor = (v: number) => (v >= 85 ? "var(--good)" : v >= 75 ? "var(--acc)" : "var(--muted)");
const PAGE = 40;
const num = (v: number | null, suffix = "") => (v == null ? "—" : `${v}${suffix}`);

export function AutoBrewer() {
  const { data, error } = usePageData<AutobrewData>(getAutobrew);
  const [query, setQuery] = useState("");
  const [color, setColor] = useState<string | null>(null);
  const [type, setType] = useState<string | null>(null);
  const [combosOnly, setCombosOnly] = useState(false);
  const [limit, setLimit] = useState(PAGE);
  const [open, setOpen] = useState<Set<number>>(new Set());

  const typeCounts = useMemo(() => {
    const c: Record<string, number> = {};
    data?.rows.forEach((r) => r.comboType && (c[r.comboType] = (c[r.comboType] ?? 0) + 1));
    return c;
  }, [data]);

  const shown = useMemo(() => {
    if (!data) return [];
    const q = query.trim().toLowerCase();
    return data.rows.filter(
      (r) =>
        (!q || r.commander.toLowerCase().includes(q) || r.playstyle.toLowerCase().includes(q)) &&
        (!color || r.colors.includes(color)) &&
        (!type || r.comboType === type) &&
        (!combosOnly || r.combosOwned > 0),
    );
  }, [data, query, color, type, combosOnly]);

  if (error) return <div className={s.error}>error: {error}</div>;
  if (!data) return <div className={s.loading}>loading leaderboard…</div>;

  const reset = () => {
    setLimit(PAGE);
    setOpen(new Set());
  };
  const toggleColor = (c: string) => {
    setColor(color === c ? null : c);
    reset();
  };
  const toggleType = (t: string) => {
    setType(type === t ? null : t);
    reset();
  };
  const toggleOpen = (rank: number) => {
    const next = new Set(open);
    if (next.has(rank)) next.delete(rank);
    else next.add(rank);
    setOpen(next);
  };
  const typeKeys = Object.keys(TYPE_COLOR).filter((t) => typeCounts[t]);

  return (
    <div className={s.page}>
      <Masthead
        kicker={`Auto-Brewer · SCREEN-grade · swept ${data.generated}`}
        title="Owned-Pool Leaderboard"
        right={
          <div className={s.tierChips}>
            <span className={s.tierChip}>
              <i style={{ background: "var(--ink3)" }} />
              {data.candidates} commanders
            </span>
          </div>
        }
      />

      <p className={s.tierLede}>
        Every owned commander candidate, brewed a template 99 from the collection and screened by{" "}
        <code>auto_brewer.py</code>. The machine proposes; a human vets. <strong>These are screening
        numbers, not kill windows</strong> — <em>Assembly</em> is P(combo pieces <em>seen</em> by turn
        10), never a turn a game ends. A winner here still has to graduate through a hand-written
        proposal and a real clock lab. Combo <em>type</em> is Commander Spellbook's own produced-feature
        classification; <em>playstyle</em> is the brew's oracle-text themes.
      </p>

      <div className={s.abToolbar}>
        <input
          className={s.abSearch}
          placeholder="Search commander / playstyle…"
          value={query}
          onChange={(e) => {
            setQuery(e.target.value);
            reset();
          }}
        />
        <span className={s.abColors}>
          {COLORS.map((c) => (
            <button
              key={c}
              className={s.abColorBtn}
              title={c}
              onClick={() => toggleColor(c)}
              style={{ opacity: color && color !== c ? 0.3 : 1, outline: color === c ? "2px solid var(--ink)" : "none" }}
            >
              <Pips letters={[c]} size={15} />
            </button>
          ))}
        </span>
        <button
          className={`${s.tag} ${combosOnly ? s.tagFree : ""}`}
          style={{ cursor: "pointer", border: "1px solid var(--hair)", background: combosOnly ? undefined : "var(--hair2)", color: combosOnly ? undefined : "var(--ink2)" }}
          onClick={() => {
            setCombosOnly(!combosOnly);
            reset();
          }}
        >
          {combosOnly ? "✓ " : ""}Owned combo only
        </button>
        <span className={s.colCount} style={{ marginLeft: "auto" }}>
          {shown.length} of {data.candidates}
        </span>
      </div>

      {typeKeys.length > 0 && (
        <div className={s.abTypeRow}>
          {typeKeys.map((t) => (
            <button
              key={t}
              className={s.abTypeChip}
              onClick={() => toggleType(t)}
              style={{
                color: type === t ? "#fff" : typeColor(t),
                background: type === t ? typeColor(t) : "transparent",
                borderColor: typeColor(t),
              }}
            >
              {t} {typeCounts[t]}
            </button>
          ))}
        </div>
      )}

      <div className={s.abList}>
        {shown.slice(0, limit).map((r) => (
          <Row key={r.rank} r={r} open={open.has(r.rank)} onToggle={() => toggleOpen(r.rank)} />
        ))}
      </div>

      {shown.length > limit && (
        <div className={s.more}>
          <button className={s.linkBtn} onClick={() => setLimit(limit + PAGE)}>
            show {Math.min(PAGE, shown.length - limit)} more · {shown.length - limit} hidden
          </button>
        </div>
      )}

      <p className={s.tierFoot}>
        SCREEN axes (points toward the 0–100 composite): Assembly 25 · Combo depth 10 · Keepable 20 ·
        Flow 15 · Colors 10 · Ramp 10 · Draw 10. The combo axis is deliberately heavy — this pod's bar
        is a proven kill package, not raw value. Reskins resolve automatically; proxies count as owned;
        cross-deck contention is not enforced here — run <code>availability_check.py</code> before
        building anything.
      </p>
    </div>
  );
}

function Row({ r, open, onToggle }: { r: AutobrewRow; open: boolean; onToggle: () => void }) {
  const score = r.score ?? 0;
  return (
    <div className={s.abRow}>
      <div className={s.abHead} onClick={onToggle}>
        <span className={s.abRank}>{r.rank}</span>
        <span className={s.scoreWrap} style={{ width: 96 }}>
          <span className={s.scoreNum} style={{ width: 40 }}>{r.score == null ? "—" : r.score}</span>
          <span className={s.scoreBar}>
            <span className={s.scoreBarFill} style={{ width: `${score}%`, background: scoreColor(score) }} />
          </span>
        </span>
        <span className={s.abNameCol}>
          <span className={s.deckName}>{r.commander}</span>
          <span className={s.deckCmdr}>{r.playstyle}</span>
        </span>
        <span className={s.abColorCell}>
          <Pips letters={r.colors} size={12} />
        </span>
        <span className={s.abTypeCell}>
          {r.comboType ? (
            <span className={s.abTypeTag} style={{ color: typeColor(r.comboType), borderColor: typeColor(r.comboType) }}>
              {r.comboType}
            </span>
          ) : (
            <span className={s.abNoCombo}>no 2-card combo</span>
          )}
        </span>
        <span className={s.abQuick}>
          <b>{num(r.assemblyT10, "%")}</b> seen@T10
        </span>
        <span className={s.abQuick}>
          <b>{r.combosOwned}</b> combo{r.combosOwned === 1 ? "" : "s"}
        </span>
        <span className={s.openArrow}>{open ? "▾" : "▸"}</span>
      </div>

      {open && (
        <div className={s.abDetail}>
          {r.playstyleGloss && <p className={s.abGloss}>{r.playstyleGloss}.</p>}

          {r.combo ? (
            <div className={s.abComboBox}>
              <div className={s.filterHead} style={{ marginBottom: 8 }}>
                Headline combo · <span style={{ color: typeColor(r.comboType) }}>{r.comboType}</span>
                {r.combo.popularity > 0 && (
                  <span className={s.abPop}> · {r.combo.popularity.toLocaleString()} CSB decks</span>
                )}
              </div>
              <div className={s.abCombo}>
                {r.combo.pieces.map((p, i) => (
                  <span key={i}>
                    {i > 0 && <span className={s.abPlus}>+</span>}
                    <span className={s.abPiece}>{p}</span>
                  </span>
                ))}
                <span className={s.abArrow}>→</span>
                {r.combo.produces.map((p, i) => (
                  <span key={i} className={s.abProduce}>{p}</span>
                ))}
              </div>
            </div>
          ) : (
            r.combosOwned > 0 && (
              <p className={s.abGloss}>
                {r.combosOwned} owned combo{r.combosOwned === 1 ? "" : "s"} in Commander Spellbook, but
                the seeded package didn't reconstruct a headline (an off-colour or land piece) — inspect
                with <code>auto_brewer.py brew "{r.commander}"</code>.
              </p>
            )
          )}

          <div className={s.abStatsRow}>
            <Stat label="Pool" value={`${r.pool}`} />
            <Stat label="Keepable" value={num(r.keepable, "%")} />
            <Stat label="Dead turns" value={num(r.deadTurns)} />
            <Stat label="Colors@T4" value={num(r.colorsT4, "%")} />
            <Stat label="Ramp / Draw" value={`${r.ramp ?? "—"} / ${r.draw ?? "—"}`} />
            <Stat label="1-away combos" value={`${r.combosOneAway}`} />
            {r.combosGated > 0 && <Stat label="Template-gated" value={`${r.combosGated}`} />}
            {r.gc.length > 0 && <Stat label="Game Changers" value={`${r.gc.length}/3`} accent />}
          </div>

          {Object.keys(r.axes).length > 0 && (
            <div className={s.abAxes}>
              {AXIS_ORDER.filter((k) => k in r.axes).map((k) => {
                const meta = AXIS_META[k];
                const v = r.axes[k];
                return (
                  <div key={k} className={s.abAxis}>
                    <span className={s.abAxisLabel}>{meta.label}</span>
                    <span className={s.abAxisBar}>
                      <span className={s.abAxisFill} style={{ width: `${(v / meta.max) * 100}%` }} />
                    </span>
                    <span className={s.abAxisVal}>{v}<i>/{meta.max}</i></span>
                  </div>
                );
              })}
            </div>
          )}

          {r.package.length > 0 && (
            <div>
              <div className={s.filterHead} style={{ margin: "4px 0 7px" }}>
                Seeded combo package ({r.package.length})
              </div>
              <div className={s.abPkg}>
                {r.package.map((p, i) => (
                  <span key={i} className={s.abPkgCard}>{p}</span>
                ))}
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  );
}

function Stat({ label, value, accent }: { label: string; value: string; accent?: boolean }) {
  return (
    <span className={s.abStat}>
      <span className={s.abStatLabel}>{label}</span>
      <span className={s.abStatVal} style={accent ? { color: "var(--gold)" } : undefined}>{value}</span>
    </span>
  );
}
