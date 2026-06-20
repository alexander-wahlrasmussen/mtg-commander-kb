import styles from "./BracketPod.module.css";

export type Medal = "gold" | "silver" | "bronze";

export interface Seat {
  name: string;
  seed?: number;
  /** Win share 0..1 — drives the fill width and the percentage label. */
  share: number;
  advances?: boolean;
  medal?: Medal;
}

export interface BracketPodProps {
  title: string;
  hint?: string;
  seats: Seat[];
  /** Gold-accented styling for the final pod. */
  final?: boolean;
}

const MEDALS: Record<Medal, string> = { gold: "🥇", silver: "🥈", bronze: "🥉" };

/** One tournament pod — a list of seats with win-share bars and advance/medal accents. */
export function BracketPod({ title, hint, seats, final = false }: BracketPodProps) {
  const max = Math.max(1e-9, ...seats.map((s) => s.share));
  return (
    <div className={`${styles.pod} ${final ? styles.final : ""}`}>
      <h3 className={styles.head}>
        <span>{title}</span>
        {hint && <span className={styles.hint}>{hint}</span>}
      </h3>
      {seats.map((s, i) => (
        <div
          key={i}
          className={[styles.seat, s.advances ? styles.adv : "", s.medal ? styles[s.medal] : ""]
            .filter(Boolean)
            .join(" ")}
        >
          <span className={styles.fill} style={{ width: `${(s.share / max) * 100}%` }} />
          {s.medal && <span className={styles.medal}>{MEDALS[s.medal]}</span>}
          <span className={styles.nm}>
            {s.name}
            {s.advances && <span className={styles.arrow}> ➜</span>}
          </span>
          {s.seed != null && <span className={styles.sd}>#{s.seed}</span>}
          <span className={styles.pct}>{(s.share * 100).toFixed(1)}%</span>
        </div>
      ))}
    </div>
  );
}
