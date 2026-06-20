import styles from "./SegmentedControl.module.css";

export interface SegmentOption<T extends string = string> {
  value: T;
  label: string;
}

export interface SegmentedControlProps<T extends string = string> {
  options: SegmentOption<T>[];
  value: T;
  onChange: (value: T) => void;
  /** Hide (rather than show-disabled) options outside this allow-list. */
  allowed?: T[];
  "aria-label"?: string;
}

/** A pill-style segmented toggle for small mutually-exclusive choices. */
export function SegmentedControl<T extends string = string>({
  options,
  value,
  onChange,
  allowed,
  ...rest
}: SegmentedControlProps<T>) {
  return (
    <div className={styles.seg} role="group" aria-label={rest["aria-label"]}>
      {options.map((o) => {
        const hidden = allowed ? !allowed.includes(o.value) : false;
        return (
          <button
            key={o.value}
            type="button"
            className={value === o.value ? styles.on : undefined}
            style={hidden ? { display: "none" } : undefined}
            disabled={hidden}
            onClick={() => onChange(o.value)}
          >
            {o.label}
          </button>
        );
      })}
    </div>
  );
}
