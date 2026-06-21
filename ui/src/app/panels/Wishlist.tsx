import { getWishlist } from "../data";
import type { WishlistData } from "../data";
import { usePageData } from "../hooks";
import { Masthead, SectionRule } from "../pagekit";
import s from "../pages.module.css";

const COST_TAG: Record<string, { cls: string; label: string }> = {
  free: { cls: s.tagFree, label: "Free · own" },
  small: { cls: s.tagSmall, label: "Small buy" },
  major: { cls: s.tagMajor, label: "Major" },
};

function Tag({ cls, label }: { cls: string; label: string }) {
  return <span className={`${s.tag} ${cls}`}>{label}</span>;
}

function rowTags(row: { cost: string; gate: boolean; applied?: boolean }) {
  const tags = [];
  if (row.applied) tags.push(<Tag key="a" cls={s.tagApplied} label="Applied" />);
  else {
    const c = COST_TAG[row.cost] ?? COST_TAG.free;
    tags.push(<Tag key="c" cls={c.cls} label={c.label} />);
  }
  if (row.gate) tags.push(<Tag key="g" cls={s.tagApproval} label="Approval" />);
  return tags;
}

export function Wishlist() {
  const { data, error } = usePageData<WishlistData>(getWishlist);
  if (error) return <div className={s.error}>error: {error}</div>;
  if (!data) return <div className={s.loading}>loading tracker…</div>;
  const c = data.counts;

  return (
    <div className={s.page}>
      <Masthead kicker="Wishlist" title="Build & Swap Tracker" />

      <div className={s.kpiStrip}>
        <div className={s.kpi}><div className={s.kpiLabel}>Free swaps</div><div className={s.kpiValue} style={{ color: "var(--good)" }}>{c.free}</div></div>
        <div className={s.kpi}><div className={s.kpiLabel}>Small buys</div><div className={s.kpiValue}>{c.small}</div></div>
        <div className={s.kpi}><div className={s.kpiLabel}>Builds</div><div className={s.kpiValue}>{c.builds}</div></div>
        <div className={s.kpi}><div className={s.kpiLabel}>Approvals</div><div className={s.kpiValue} style={{ color: "var(--gold)" }}>{c.gates}</div></div>
      </div>

      <div>
        <SectionRule title="Recommended swaps" right="cut a surplus, shore up a thin role" />
        <div className={s.legend}>
          <Tag cls={s.tagFree} label="Free · own" />
          <Tag cls={s.tagSmall} label="Small buy" />
          <Tag cls={s.tagMajor} label="Major" />
          <Tag cls={s.tagApproval} label="Approval" />
        </div>
        {data.swaps.map((sw, i) => (
          <div key={i} className={s.swapRow}>
            <span className={s.swapDeck}>{sw.deck}</span>
            <div className={s.swapChange}>
              {sw.out ? (
                <>
                  <span className={s.swapOut}>{sw.out}</span>
                  <span className={s.swapArrow}>→</span>
                  <span className={s.swapInto}>{sw.into}</span>
                </>
              ) : (
                <span className={s.swapInto} style={{ fontWeight: 400 }}>{sw.change}</span>
              )}
            </div>
            <span className={s.tagRow}>{rowTags(sw)}</span>
          </div>
        ))}
      </div>

      <div>
        <SectionRule title="New brews to build" right="the active build order" />
        <div className={s.builds}>
          {data.builds.map((b, i) => (
            <div key={i} className={s.buildCard}>
              <div className={s.buildHead}>
                <span className={s.buildName}>{b.name}</span>
                <span className={s.buildTags}>{rowTags({ cost: b.cost, gate: b.gate })}</span>
              </div>
              <div className={s.buildTheme}>{b.theme}</div>
              <div className={s.buildStats}>
                <div><div className={s.buildStatLabel}>Clock</div><div className={s.buildStatValue}>{b.clock || "—"}</div></div>
                <div><div className={s.buildStatLabel}>GC</div><div className={s.buildStatValue}>{b.gc || "—"}</div></div>
                <div><div className={s.buildStatLabel}>To acquire</div><div className={s.buildStatValue} style={{ color: "var(--acc)" }}>{b.acquire != null ? `${b.acquire} cards` : "—"}</div></div>
              </div>
            </div>
          ))}
        </div>
      </div>

      {data.buys.length > 0 && (
        <div>
          <SectionRule title="Cheap unlocks" right="small buys that free up a swap" />
          <div className={s.buys}>
            {data.buys.map((b, i) => (
              <div key={i} className={s.buyRow}>
                <span className={s.buyCard}>{b.card}</span>
                <span className={s.buyUnlocks}>→ {b.unlocks}</span>
                <span className={s.buyQty}>{b.qty}</span>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
