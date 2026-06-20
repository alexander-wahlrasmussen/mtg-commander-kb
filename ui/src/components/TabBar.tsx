import styles from "./TabBar.module.css";

export interface TabItem {
  id: string;
  label: string;
}

export interface TabBarProps {
  tabs: TabItem[];
  active: string;
  onChange: (id: string) => void;
}

/** The top-level pill navigation between dashboard views. */
export function TabBar({ tabs, active, onChange }: TabBarProps) {
  return (
    <nav className={styles.tabs}>
      {tabs.map((t) => (
        <button
          key={t.id}
          type="button"
          className={`${styles.tab} ${active === t.id ? styles.active : ""}`}
          onClick={() => onChange(t.id)}
        >
          {t.label}
        </button>
      ))}
    </nav>
  );
}
