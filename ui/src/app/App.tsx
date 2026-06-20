import { useEffect, useState } from "react";
import { TabBar, ProgressBar } from "../components";
import { initMode, mode } from "./data";
import { useBusy } from "./inflight";
import { Gauntlet } from "./panels/Gauntlet";
import { Clocks } from "./panels/Clocks";
import { Locks } from "./panels/Locks";
import { Championship } from "./panels/Championship";
import styles from "./App.module.css";

const TABS = [
  { id: "gauntlet", label: "⚔️ Gauntlet" },
  { id: "clocks", label: "⏱️ Clocks / Labs" },
  { id: "locks", label: "🔒 Locks" },
  { id: "championship", label: "🏆 Championship" },
];

export function App() {
  const [ready, setReady] = useState(false);
  const [tab, setTab] = useState("gauntlet");
  const busy = useBusy();

  useEffect(() => {
    initMode().then(() => setReady(true));
  }, []);

  if (!ready) return <div className={styles.boot}>loading…</div>;

  const subtitle = mode.static
    ? `static build · precomputed ${mode.manifest?.generated ?? ""}`
    : "control room for the lab stack — race · labs · championship";

  return (
    <>
      <ProgressBar active={busy} />
      <header className={styles.topbar}>
        <div className={styles.brand}>
          <span className={styles.logo}>🏟️</span>
          <div>
            <h1 className={styles.h1}>The Pod Gauntlet</h1>
            <p className={styles.subtitle}>{subtitle}</p>
          </div>
        </div>
        <TabBar tabs={TABS} active={tab} onChange={setTab} />
      </header>

      <main className={styles.main}>
        {tab === "gauntlet" && <Gauntlet />}
        {tab === "clocks" && <Clocks />}
        {tab === "locks" && <Locks />}
        {tab === "championship" && <Championship />}
      </main>

      <footer className={styles.discipline}>
        <strong>Read shapes, not decimals.</strong> Clock curves are unblocked goldfish ceilings;
        disruption is availability, not effectiveness; the durability tiebreak and T_grind are
        judgment. This is a viewer for the lab stack — trust the ranking and the gaps.
      </footer>
    </>
  );
}
