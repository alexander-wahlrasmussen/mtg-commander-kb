import { ChampionBanner, LineChart } from "../../components";
import { getHome, PALETTE } from "../data";
import type { HomeData } from "../data";
import { usePageData } from "../hooks";
import { SectionRule, tierColor } from "../pagekit";
import s from "../pages.module.css";

export function Home({ onOpenDeck, onNav }: { onOpenDeck: (slug: string) => void; onNav: (tab: string) => void }) {
  const { data, error } = usePageData<HomeData>(getHome);
  if (error) return <div className={s.error}>error: {error}</div>;
  if (!data) return <div className={s.loading}>loading dashboard…</div>;

  const maxPct = Math.max(75, ...data.pod.map((p) => p.pct));

  return (
    <div className={s.page}>
      <div className={s.kpiStrip}>
        {data.kpis.map((k, i) => (
          <div key={i} className={s.kpi}>
            <div className={s.kpiLabel}>{k.label}</div>
            <div className={s.kpiValue}>{k.value}</div>
            <div className={s.kpiSub}>{k.sub}</div>
          </div>
        ))}
      </div>

      {data.champion.name && (
        <div role="button" tabIndex={0} style={{ cursor: "pointer" }} onClick={() => onNav("championship")}>
          <ChampionBanner name={data.champion.name} seed={data.champion.seed} note={data.champion.note} />
        </div>
      )}

      <div className={s.homeGrid}>
        <div className={s.col}>
          <div>
            <SectionRule title="Kill clocks" right={<button className={s.linkBtn} onClick={() => onNav("gauntlet")}>gauntlet →</button>} />
            <LineChart
              height={248}
              xLabel="turn"
              yLabel="cum P(decap) %"
              refLineY={50}
              series={data.clockSeries.map((c, i) => ({
                name: c.name,
                color: PALETTE[i % PALETTE.length],
                points: c.grid.map((x, j) => ({ x, y: c.decap[j] })),
              }))}
            />
          </div>
          <div>
            <SectionRule title="Top decks" right={<button className={s.linkBtn} onClick={() => onNav("decks")}>roster →</button>} />
            {data.roster.map((d) => (
              <button key={d.slug} className={s.rosterRow} onClick={() => onOpenDeck(d.slug)}>
                <span className={s.dot} style={{ background: tierColor(d.tier) }} />
                <span>
                  <span className={s.deckName}>{d.name}</span>
                  <span className={s.deckCmdr}>{d.commander}</span>
                </span>
                <span className={s.clockCell}>{d.decap ?? "—"} / {d.table ?? "—"}</span>
                <span className={s.scoreCell}>{d.score == null ? "—" : `${d.score}/20`}</span>
              </button>
            ))}
          </div>
        </div>

        <div className={s.col}>
          <div>
            <SectionRule title="Bring vs the pod" right={<button className={s.linkBtn} onClick={() => onNav("gauntlet")}>matrix →</button>} />
            <div style={{ display: "flex", flexDirection: "column", gap: 11 }}>
              {data.pod.map((p, i) => (
                <div key={i} className={s.podRow}>
                  <div>
                    <div style={{ fontSize: 13.5, marginBottom: 5 }}>{p.name}</div>
                    <span className={s.bar}>
                      <span className={s.barFill} style={{ width: `${Math.min(100, (p.pct / maxPct) * 100)}%` }} />
                    </span>
                  </div>
                  <span className={s.pct}>{p.pct}%</span>
                </div>
              ))}
            </div>
          </div>
          <div>
            <SectionRule title="Season awards" />
            {data.awards.map((a, i) => (
              <div key={i} className={s.award}>
                <div className={s.awardLabel}>{a.label}</div>
                <div className={s.awardWinner}>{a.winner}</div>
                <div className={s.awardNote}>{a.note}</div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}
