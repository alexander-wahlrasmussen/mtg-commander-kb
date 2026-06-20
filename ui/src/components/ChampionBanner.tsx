import type { ReactNode } from "react";
import styles from "./ChampionBanner.module.css";

export interface ChampionBannerProps {
  name: string;
  seed?: number;
  note?: ReactNode;
}

/** The gold celebratory banner crowning the tournament champion. */
export function ChampionBanner({ name, seed, note }: ChampionBannerProps) {
  return (
    <div className={styles.banner}>
      <div className={styles.trophy}>🏆</div>
      <div>
        <h2 className={styles.name}>{name}</h2>
        <p className={styles.sub}>Champion{seed != null ? ` · seed #${seed}` : ""}</p>
        {note && <p className={styles.note}>{note}</p>}
      </div>
    </div>
  );
}
