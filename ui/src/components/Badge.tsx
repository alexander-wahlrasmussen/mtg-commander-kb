import type { ReactNode } from "react";
import styles from "./Badge.module.css";

export type BadgeVariant = "default" | "busy" | "ok" | "err";

export interface BadgeProps {
  children: ReactNode;
  /** Status colour. `busy` pulses. */
  variant?: BadgeVariant;
}

/** A small monospace status pill (ready / running / done / error). */
export function Badge({ children, variant = "default" }: BadgeProps) {
  return <span className={`${styles.badge} ${styles[variant]}`}>{children}</span>;
}
