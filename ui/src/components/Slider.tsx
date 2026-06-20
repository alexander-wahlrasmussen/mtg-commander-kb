import styles from "./Slider.module.css";

export interface SliderProps {
  label: string;
  value: number;
  min: number;
  max: number;
  step?: number;
  /** Text shown next to the label (e.g. "0.30" or "12k"). Defaults to the value. */
  display?: string;
  onChange?: (value: number) => void;
  /** Lock the control and show `display` as a baked/read-only value. */
  frozen?: boolean;
}

/** A labelled range slider with a live value read-out. */
export function Slider({
  label,
  value,
  min,
  max,
  step = 1,
  display,
  onChange,
  frozen = false,
}: SliderProps) {
  return (
    <div className={styles.ctrl}>
      <label className={styles.label}>
        {label} <output className={styles.out}>{display ?? value}</output>
      </label>
      <input
        type="range"
        className={styles.range}
        min={min}
        max={max}
        step={step}
        value={value}
        disabled={frozen}
        onChange={(e) => onChange?.(+e.target.value)}
      />
    </div>
  );
}
