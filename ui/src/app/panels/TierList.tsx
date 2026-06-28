import { getTierList } from "../data";
import type { TierListData, TierRow } from "../data";
import { usePageData } from "../hooks";
import { Masthead } from "../pagekit";
import s from "../pages.module.css";

// Letter-tier accents (distinct from the Decks page's CC tiers): S good → D faint.
const TIER_COLOR: Record<string, string> = {
  S: "var(--good)", A: "var(--acc)", B: "var(--gold)", C: "var(--muted)", D: "var(--faint)",
};

const clamp = (v: number) => Math.max(0, Math.min(100, v));

function Axis({ value, color }: { value: number | null; color: string }) {
  if (value == null) return <span className={s.tierAxisVal} style={{ color: "var(--faint)" }}>—</span>;
  return (
    <span className={s.tierAxis}>
      <span className={s.tierAxisBar}>
        <span className={s.tierAxisFill} style={{ width: `${clamp(value)}%`, background: color }} />
      </span>
      <span className={s.tierAxisVal}>{value}%</span>
    </span>
  );
}

export function TierList() {
  const { data, error } = usePageData<TierListData>(getTierList);
  if (error) return <div className={s.error}>error: {error}</div>;
  if (!data) return <div className={s.loading}>loading tier list…</div>;

  const counts: Record<string, number> = {};
  data.rows.forEach((r) => (counts[r.tier] = (counts[r.tier] ?? 0) + 1));
  const w = data.weights;
  const byTier = data.tiers
    .map((t) => ({ tier: t, rows: data.rows.filter((r) => r.tier === t) }))
    .filter((g) => g.rows.length);

  return (
    <div className={s.page}>
      <Masthead
        kicker={`Power Ranking · ${data.version}`}
        title="Tier List"
        right={
          <div className={s.tierChips}>
            {data.tiers.filter((t) => counts[t]).map((t) => (
              <span key={t} className={s.tierChip} style={{ color: TIER_COLOR[t] }}>
                <i style={{ background: TIER_COLOR[t] }} />
                {t} {counts[t]}
              </span>
            ))}
          </div>
        }
      />

      <p className={s.tierLede}>
        Ranked by the three convergent <strong>outcome</strong> oracles — not the build score.
        Composite ={" "}
        <span className={s.tierFormula}>
          ANTI-POD&nbsp;{w.antipod} · INTERACTION&nbsp;{w.inter} · SELF-META&nbsp;{w.self}
        </span>
        . The Conversion Check <code>(cc)</code> is shown for contrast only — note how the 19/20
        builds scatter down the board (<em>score ⊥ winning</em>).
      </p>

      <table className={s.deckTable}>
        <thead>
          <tr>
            <th style={{ width: 132 }}>Comp</th>
            <th>Deck</th>
            <th style={{ width: 116 }}>Anti-pod</th>
            <th style={{ width: 116 }}>Interaction</th>
            <th style={{ width: 116 }}>Self-meta</th>
            <th style={{ textAlign: "center", width: 48 }}>cc</th>
            <th style={{ width: 86 }}>Clock</th>
          </tr>
        </thead>
        <tbody>
          {byTier.map((g) => (
            <TierGroup key={g.tier} tier={g.tier} rows={g.rows} />
          ))}
        </tbody>
      </table>

      <p className={s.tierFoot}>
        Anti-pod = P(beat the T6-7 combo pod). Interaction / Self-meta = the same mirror bar at two
        fidelities (interaction adds the answer-trading tax). Read tiers and big gaps, not single
        Comp points — every axis is a goldfish ceiling with soft priors.
      </p>
    </div>
  );
}

function TierGroup({ tier, rows }: { tier: string; rows: TierRow[] }) {
  const color = TIER_COLOR[tier] ?? "var(--faint)";
  return (
    <>
      <tr className={s.tierBand}>
        <td colSpan={7}>
          <span className={s.tierBandLetter} style={{ background: color }}>{tier}</span>
          <span className={s.tierBandCount}>{rows.length} deck{rows.length === 1 ? "" : "s"}</span>
        </td>
      </tr>
      {rows.map((r) => (
        <tr key={r.slug} className={s.tierRow}>
          <td>
            <div className={s.scoreWrap}>
              <span className={s.scoreNum} style={{ width: 34 }}>{r.comp}</span>
              <span className={s.scoreBar}>
                <span className={s.scoreBarFill} style={{ width: `${clamp(r.comp)}%`, background: color }} />
              </span>
            </div>
          </td>
          <td>
            <div className={s.deckName}>{r.name}</div>
          </td>
          <td><Axis value={r.anti} color="var(--acc)" /></td>
          <td><Axis value={r.inter} color="var(--accent-ink)" /></td>
          <td><Axis value={r.self} color="var(--muted)" /></td>
          <td style={{ textAlign: "center", color: r.cc == null ? "var(--faint)" : "var(--muted)", fontFamily: "var(--mono)" }}>
            {r.cc == null ? "—" : r.cc}
          </td>
          <td className={s.clockCell} style={{ whiteSpace: "nowrap" }}>{r.decap} / {r.table}</td>
        </tr>
      ))}
    </>
  );
}
