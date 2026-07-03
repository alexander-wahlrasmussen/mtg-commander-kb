import { useEffect, useState } from "react";
import { TabBar, ProgressBar } from "../components";
import { initMode, mode } from "./data";
import { useBusy } from "./inflight";
import { Home } from "./panels/Home";
import { Gauntlet } from "./panels/Gauntlet";
import { Clocks } from "./panels/Clocks";
import { Locks } from "./panels/Locks";
import { Matchups } from "./panels/Matchups";
import { Championship } from "./panels/Championship";
import { TierList } from "./panels/TierList";
import { Decks } from "./panels/Decks";
import { Doctor } from "./panels/Doctor";
import { Collection } from "./panels/Collection";
import { Wishlist } from "./panels/Wishlist";
import { DeckPage } from "./panels/DeckPage";
import styles from "./App.module.css";

const TABS = [
  { id: "home", label: "Home" },
  { id: "gauntlet", label: "Gauntlet" },
  { id: "clocks", label: "Clocks" },
  { id: "locks", label: "Locks" },
  { id: "matchups", label: "Matchups" },
  { id: "championship", label: "Championship" },
  { id: "tiers", label: "Tier List" },
  { id: "decks", label: "Decks" },
  { id: "doctor", label: "Doctor" },
  { id: "collection", label: "Collection" },
  { id: "wishlist", label: "Wishlist" },
];

const SUBTITLES: Record<string, string> = {
  home: "the hub — roster, champion, kill-clocks, season awards",
  gauntlet: "P(beat the pod) — the race lab",
  clocks: "harvested decap / table kill-curves",
  locks: "deck × lock win-probability lift",
  matchups: "deck × his measured stable — read the spread, not the blend",
  championship: "the 16-deck bracket",
  tiers: "the v2 power ranking — three outcome oracles, score ⊥ winning",
  decks: "the active roster — Conversion Check + measured clock",
  doctor: "the roster pre-flight — red means fix it before it hits a table",
  collection: "the card browser",
  wishlist: "the build & swap tracker",
};

export function App() {
  const [ready, setReady] = useState(false);
  const [tab, setTab] = useState("home");
  const [deck, setDeck] = useState<string | null>(null);
  const busy = useBusy();

  useEffect(() => {
    initMode().then(() => setReady(true));
  }, []);

  if (!ready) return <div className={styles.boot}>loading…</div>;

  const openDeck = (slug: string) => {
    setDeck(slug);
    window.scrollTo(0, 0);
  };
  const nav = (id: string) => {
    setDeck(null);
    setTab(id);
  };

  const subtitle = deck
    ? "scouting report"
    : mode.static
      ? `static build · precomputed ${mode.manifest?.generated ?? ""}`
      : SUBTITLES[tab] ?? "control room for the lab stack";

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
        <TabBar tabs={TABS} active={deck ? "" : tab} onChange={nav} />
      </header>

      <main className={styles.main}>
        {deck ? (
          <DeckPage slug={deck} onBack={() => setDeck(null)} />
        ) : (
          <>
            {tab === "home" && <Home onOpenDeck={openDeck} onNav={nav} />}
            {tab === "gauntlet" && <Gauntlet />}
            {tab === "clocks" && <Clocks />}
            {tab === "locks" && <Locks />}
            {tab === "matchups" && <Matchups />}
            {tab === "championship" && <Championship />}
            {tab === "tiers" && <TierList />}
            {tab === "decks" && <Decks onOpenDeck={openDeck} />}
            {tab === "doctor" && <Doctor />}
            {tab === "collection" && <Collection />}
            {tab === "wishlist" && <Wishlist />}
          </>
        )}
      </main>

      <footer className={styles.discipline}>
        <strong>Read shapes, not decimals.</strong> Clock curves are unblocked goldfish ceilings;
        disruption is availability, not effectiveness; the durability tiebreak and T_grind are
        judgment. Roster, clocks and scores are read from the knowledge base; the sim tabs run the
        live lab stack.
      </footer>
    </>
  );
}
