// Shared newsprint chrome for the content pages — masthead, section rules, mana
// pips, tier colours. Token-styled (Tale of the Tape); no component-library deps.
import type { ReactNode } from "react";
import s from "./pages.module.css";

/** WUBRG mana-pip fills (earthy newsprint inks, not screen-bright). */
export const WUBRG: Record<string, string> = {
  W: "#b08a1a", U: "#0a6c87", B: "#6f5577", R: "#b8331f", G: "#5f7510", C: "#7c6f64",
};

/** Tier → accent colour (good / vermillion / faint), used for score bars + dots. */
export function tierColor(tier: string): string {
  if (tier === "elite") return "var(--good)";
  if (tier === "solid") return "var(--acc)";
  return "var(--faint)";
}

export function Pips({ letters, size = 14 }: { letters: string[]; size?: number }) {
  return (
    <span className={s.pips}>
      {letters.map((l, i) => (
        <i key={i} style={{ width: size, height: size, background: WUBRG[l] ?? WUBRG.C }} />
      ))}
    </span>
  );
}

/** Page header — mono kicker over an Oswald title, optional right-aligned slot. */
export function Masthead({ kicker, title, right }: { kicker: string; title: string; right?: ReactNode }) {
  return (
    <div className={s.masthead}>
      <div>
        <div className={s.kicker}>{kicker}</div>
        <h2 className={s.title}>{title}</h2>
      </div>
      {right && <div className={s.mastheadRight}>{right}</div>}
    </div>
  );
}

/** The 2px-ink underlined section heading shared across the templates. */
export function SectionRule({ title, right }: { title: string; right?: ReactNode }) {
  return (
    <div className={s.sectionRule}>
      <h3 className={s.sectionTitle}>{title}</h3>
      {right && <span className={s.sectionRight}>{right}</span>}
    </div>
  );
}
