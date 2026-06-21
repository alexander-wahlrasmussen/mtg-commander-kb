import { useMemo, useState } from "react";
import { getCollection } from "../data";
import type { CollectionCard, CollectionData } from "../data";
import { usePageData } from "../hooks";
import { Masthead, WUBRG } from "../pagekit";
import s from "../pages.module.css";

const COLOR_LABELS: Record<string, string> = { W: "White", U: "Blue", B: "Black", R: "Red", G: "Green", C: "Colorless", M: "Multicolor" };
const COLOR_ORDER = ["W", "U", "B", "R", "G", "M", "C"];
const ROLE_META: Record<string, { label: string; color: string }> = {
  ramp: { label: "Ramp", color: "#79740e" }, draw: { label: "Draw", color: "#076678" },
  removal: { label: "Removal", color: "#9d0006" }, wipe: { label: "Wipes", color: "#8f3f71" },
  prot: { label: "Protect", color: "#427b58" }, recur: { label: "Recur", color: "#af3a03" },
  tutor: { label: "Tutors", color: "#b57614" }, fin: { label: "Finish", color: "#a5430a" },
};
const PAGE = 240;

const pipColor = (c: string) => (c === "M" ? "#946112" : WUBRG[c] ?? WUBRG.C);

export function Collection() {
  const { data, error } = usePageData<CollectionData>(getCollection);
  const [color, setColor] = useState<string | null>(null);
  const [role, setRole] = useState<string | null>(null);
  const [rarity, setRarity] = useState<string | null>(null);
  const [limit, setLimit] = useState(PAGE);

  const shown = useMemo(() => {
    if (!data) return [];
    return data.cards.filter(
      (c) => (!color || c.color === color) && (!role || c.role === role) && (!rarity || c.rarity === rarity),
    );
  }, [data, color, role, rarity]);

  if (error) return <div className={s.error}>error: {error}</div>;
  if (!data) return <div className={s.loading}>loading collection…</div>;

  const toggle = <T,>(cur: T | null, v: T, set: (x: T | null) => void) => {
    set(cur === v ? null : v);
    setLimit(PAGE);
  };
  const colorKeys = COLOR_ORDER.filter((k) => data.facets.color[k]);
  const roleKeys = Object.keys(ROLE_META).filter((k) => data.facets.role[k]);
  const rarityKeys = ["Common", "Uncommon", "Rare", "Mythic"].filter((k) => data.facets.rarity[k]);

  return (
    <div className={s.page}>
      <Masthead kicker="Library" title="Collection" right={<span className={s.colCount}>{data.count.toLocaleString()} unique</span>} />
      <div className={s.colLayout}>
        <aside className={s.filters}>
          <div>
            <div className={s.filterHead}>Color</div>
            {colorKeys.map((k) => (
              <button key={k} className={s.filterRow} style={{ color: color === k ? "var(--acc)" : undefined }} onClick={() => toggle(color, k, setColor)}>
                <i style={{ width: 13, height: 13, borderRadius: "50%", background: pipColor(k), flex: "none", border: "1px solid rgba(22,19,15,.3)" }} />
                <span>{COLOR_LABELS[k] ?? k}</span>
                <span className={s.facetCount}>{data.facets.color[k]}</span>
              </button>
            ))}
          </div>
          {roleKeys.length > 0 && (
            <div>
              <div className={s.filterHead}>Role</div>
              <div className={s.filterChips}>
                {roleKeys.map((k) => (
                  <button key={k} className={s.roleTag} style={{ color: role === k ? ROLE_META[k].color : undefined, borderColor: role === k ? ROLE_META[k].color : undefined }} onClick={() => toggle(role, k, setRole)}>
                    <i style={{ background: ROLE_META[k].color }} />
                    {ROLE_META[k].label}
                  </button>
                ))}
              </div>
            </div>
          )}
          {rarityKeys.length > 0 && (
            <div>
              <div className={s.filterHead}>Rarity</div>
              {rarityKeys.map((k) => (
                <button key={k} className={s.filterRow} style={{ color: rarity === k ? "var(--acc)" : undefined }} onClick={() => toggle(rarity, k, setRarity)}>
                  <span style={{ width: 13, height: 13, border: "1.5px solid var(--ink2)", flex: "none" }} />
                  <span>{k}</span>
                  <span className={s.facetCount}>{data.facets.rarity[k]}</span>
                </button>
              ))}
            </div>
          )}
        </aside>

        <div>
          <div className={s.colToolbar}>
            <span style={{ fontFamily: "var(--mono)", fontSize: 11, color: "var(--faint)" }}>Filters</span>
            {[color && COLOR_LABELS[color], role && ROLE_META[role].label, rarity].filter(Boolean).map((t, i) => (
              <span key={i} className={`${s.tag} ${s.tagFree}`} style={{ background: "var(--hair2)", color: "var(--ink2)" }}>{t}</span>
            ))}
            <span className={s.colCount}>{shown.length.toLocaleString()} of {data.count.toLocaleString()}</span>
          </div>
          <div className={s.cardGrid}>
            {shown.slice(0, limit).map((c: CollectionCard, i) => {
              const rm = ROLE_META[c.role];
              return (
                <div key={i}>
                  <div className={s.cardArt}>
                    {c.qty > 1 && <span className={s.cardQty}>×{c.qty}</span>}
                    <span className={s.cardPip} style={{ background: pipColor(c.color) }} />
                    {c.cost && <span className={s.cardCost}>{c.cost.replace(/[{}]/g, "")}</span>}
                  </div>
                  <div className={s.cardName}>{c.name}</div>
                  <div className={s.cardMeta}>
                    {c.set && <span className={s.cardSet}>{c.set}</span>}
                    {rm && <span className={s.roleTag} style={{ color: rm.color, borderColor: rm.color }}><i style={{ background: rm.color }} />{rm.label}</span>}
                  </div>
                </div>
              );
            })}
          </div>
          {shown.length > limit && (
            <div className={s.more}>
              <button className={s.linkBtn} onClick={() => setLimit(limit + PAGE)}>show {Math.min(PAGE, shown.length - limit)} more · {shown.length - limit} hidden</button>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
