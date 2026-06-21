import { getRoster } from "../data";
import type { RosterData } from "../data";
import { usePageData } from "../hooks";
import { Masthead, Pips, tierColor } from "../pagekit";
import s from "../pages.module.css";

const TIER_LABELS: Record<string, string> = { elite: "Elite", solid: "Solid", developing: "Developing", unscored: "Unscored" };

export function Decks({ onOpenDeck }: { onOpenDeck: (slug: string) => void }) {
  const { data, error } = usePageData<RosterData>(getRoster);
  if (error) return <div className={s.error}>error: {error}</div>;
  if (!data) return <div className={s.loading}>loading roster…</div>;

  const counts: Record<string, number> = {};
  data.decks.forEach((d) => (counts[d.tier] = (counts[d.tier] ?? 0) + 1));
  const chipTiers = ["elite", "solid", "developing", "unscored"].filter((t) => counts[t]);

  return (
    <div className={s.page}>
      <Masthead
        kicker="Library · Bracket 3"
        title="Decks"
        right={
          <div className={s.tierChips}>
            {chipTiers.map((t) => (
              <span key={t} className={s.tierChip} style={{ color: tierColor(t) }}>
                <i style={{ background: tierColor(t) }} />
                {TIER_LABELS[t]} {counts[t]}
              </span>
            ))}
          </div>
        }
      />
      <table className={s.deckTable}>
        <thead>
          <tr>
            <th style={{ width: 118 }}>Score</th>
            <th>Deck</th>
            <th>Colors</th>
            <th>Archetype</th>
            <th>Clock</th>
            <th style={{ textAlign: "center" }}>GC</th>
          </tr>
        </thead>
        <tbody>
          {data.decks.map((d) => (
            <tr key={d.slug} className={s.deckRow} onClick={() => onOpenDeck(d.slug)}>
              <td>
                <div className={s.scoreWrap}>
                  <span className={s.scoreNum}>{d.score == null ? "—" : `${d.score}/20`}</span>
                  <span className={s.scoreBar}>
                    <span className={s.scoreBarFill} style={{ width: `${((d.score ?? 0) / 20) * 100}%`, background: tierColor(d.tier) }} />
                  </span>
                </div>
              </td>
              <td>
                <div className={s.deckName}>{d.name}</div>
                <div className={s.deckCmdr}>{d.commander}</div>
              </td>
              <td>
                <span style={{ display: "flex", gap: 4, alignItems: "center" }}>
                  <Pips letters={d.pips} size={13} />
                  <span className={s.cardSet}>{d.colors}</span>
                </span>
              </td>
              <td className={s.archetypeCell}>{d.archetype}</td>
              <td className={s.clockCell} style={{ whiteSpace: "nowrap" }}>
                {d.decap ?? "—"} / {d.table ?? "—"}
              </td>
              <td className={s.gcCell} style={{ color: d.gc ? "var(--gold)" : "var(--faint)" }}>
                {d.gc == null ? "—" : `${d.gc}/3`}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
