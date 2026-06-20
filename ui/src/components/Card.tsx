import type { ReactNode } from "react";
import styles from "./Card.module.css";

export interface CardProps {
  /** Card heading — gets the accent tick. Omit for a chrome-less panel. */
  title?: ReactNode;
  /** Dim helper text shown beside the title. */
  hint?: ReactNode;
  children?: ReactNode;
  className?: string;
}

/** A framed panel with the design system's signature accent-tick heading. */
export function Card({ title, hint, children, className }: CardProps) {
  return (
    <section className={[styles.card, className].filter(Boolean).join(" ")}>
      {title != null && (
        <h2 className={styles.head}>
          {title}
          {hint != null && <span className={styles.hint}>{hint}</span>}
        </h2>
      )}
      {children}
    </section>
  );
}
