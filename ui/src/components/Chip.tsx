import styles from "./Chip.module.css";

export interface ChipProps {
  label: string;
  active?: boolean;
  /** Accent colour when active (e.g. a per-deck palette colour). */
  color?: string;
  onClick?: () => void;
}

/** A toggleable filter chip — used to pick which series to overlay. */
export function Chip({ label, active = false, color, onClick }: ChipProps) {
  return (
    <button
      type="button"
      className={`${styles.chip} ${active ? styles.on : ""}`}
      style={{
        borderColor: color,
        background: active && color ? color : undefined,
      }}
      onClick={onClick}
    >
      {label}
    </button>
  );
}
