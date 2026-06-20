import type { ReactNode } from "react";
import styles from "./EmptyState.module.css";

export interface EmptyStateProps {
  /** Big emoji / glyph. */
  glyph?: string;
  title: string;
  children?: ReactNode;
}

/** A centred placeholder shown before a heavy view has been run. */
export function EmptyState({ glyph = "✨", title, children }: EmptyStateProps) {
  return (
    <div className={styles.empty}>
      <div className={styles.glyph}>{glyph}</div>
      <h3 className={styles.title}>{title}</h3>
      {children && <p className={styles.text}>{children}</p>}
    </div>
  );
}
