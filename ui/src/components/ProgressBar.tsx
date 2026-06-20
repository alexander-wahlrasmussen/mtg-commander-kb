import styles from "./ProgressBar.module.css";

export interface ProgressBarProps {
  /** When true, shows an indeterminate sliding bar pinned to the top. */
  active: boolean;
}

/** A thin top-of-page indeterminate progress indicator for in-flight work. */
export function ProgressBar({ active }: ProgressBarProps) {
  return <div className={`${styles.progress} ${active ? styles.on : ""}`} aria-hidden={!active} />;
}
