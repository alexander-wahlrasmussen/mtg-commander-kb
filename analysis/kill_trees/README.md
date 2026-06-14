# Kill trees — a deck's win lines as a decision diagram

Backlog #4. Each tree reads top-to-bottom as the decision a pilot actually makes:
**try the fastest available kill line; if its pieces aren't assembled, fall to the
next.** The lines, their pieces, and their clocks come straight from the deck's
`*_clock_lab.py` (KILL CHECKS, cheapest-first) and its audited Summary — this is
pure visualization, not a new model.

Leaf colours: 🩷 **combo** (deterministic/loop) · 💜 **table** (all-opponent
drain/poison) · 🧡 **combat** (focus-fire one opponent = decap) · 💚 **enabler**
(tutor/reset that feeds another line). The dashed lane is an **always-on**
background clock that ticks regardless of which line you assemble.

Generate with `python scripts/kill_tree.py <deck>` (`--list` for encoded decks,
`--all` for every one); the `.mmd` files here are the output. GitHub renders the
fenced ` ```mermaid ` blocks below natively; the Mermaid Chart tool validated both.

---

## Radiation Sickness — The Wise Mothman

Five lines that nearly all kill the **whole table at once** (the rad/drain engine
hits every opponent), so decap and table converge — and a passive rad drain that
closes on its own around T10 even if no combo lands.

```mermaid
flowchart TD
    classDef root fill:#222,color:#fff,stroke:#000,stroke-width:2px;
    classDef ask fill:#f7f7f7,stroke:#999;
    classDef combo fill:#fde2f0,stroke:#c0398a,stroke-width:2px;
    classDef table fill:#e6e8ff,stroke:#4b54c4,stroke-width:2px;
    classDef combat fill:#ffeccb,stroke:#e08a00,stroke-width:2px;
    classDef enabler fill:#e3f6e3,stroke:#2f9e44,stroke-width:2px;
    classDef bg fill:#f0fff0,stroke:#2f9e44,stroke-dasharray:5 4;
    classDef stall fill:#f1f1f1,stroke:#bbb,color:#666;

    S(["The Wise Mothman resolved<br/>rad counters tick every opponent's main phase"]):::root
    S --> A1{"Mindcrank + Bloodchief Ascension<br/>(3 quest counters live)"}:::ask
    A1 -- assembled --> K1["<b>infinite mill → drain loop</b><br/>⏱ table T7"]:::combo
    A1 --> A2{"Simic Ascendancy reaches<br/>20 growth counters"}:::ask
    A2 -- assembled --> K2["<b>win at your upkeep</b><br/>⏱ table T8–9"]:::combo
    A2 --> A3{"Triumph of the Hordes<br/>+ a wide creature board"}:::ask
    A3 -- assembled --> K3["<b>+1/+1, trample & INFECT → 10 poison</b><br/>⏱ table T8"]:::table
    A3 --> A4{"counter-grown creatures connect<br/>(fallback)"}:::ask
    A4 -- assembled --> K4["<b>focus one opponent</b><br/>⏱ decap T7"]:::combat
    A4 -- not yet --> STALL["keep ticking rad + stacking counters —<br/>the passive drain closes ~T10"]:::stall
    BG[["rad counters + proliferate<br/>(Vorinclex / Tekuthal / Inexorable Tide)"]]:::bg
    BG -. always on .-> KBG["<b>all-opponent rad drain</b><br/>⏱ table ~T10"]:::table
```

## Diminishing Returns — Teysa Karlov

Five distinct closing lines, all routed through Teysa (every death trigger fires
twice) — one deterministic loop, three drains, a reset, plus a tutor that can
fetch the missing piece of any of them. The table clock is slow (T12+): this deck
disrupts and grinds, it doesn't race.

```mermaid
flowchart TD
    classDef root fill:#222,color:#fff,stroke:#000,stroke-width:2px;
    classDef ask fill:#f7f7f7,stroke:#999;
    classDef combo fill:#fde2f0,stroke:#c0398a,stroke-width:2px;
    classDef table fill:#e6e8ff,stroke:#4b54c4,stroke-width:2px;
    classDef combat fill:#ffeccb,stroke:#e08a00,stroke-width:2px;
    classDef enabler fill:#e3f6e3,stroke:#2f9e44,stroke-width:2px;
    classDef stall fill:#f1f1f1,stroke:#bbb,color:#666;

    S(["Teysa Karlov online<br/>every death trigger fires TWICE"]):::root
    S --> A1{"Gravecrawler + Phyrexian Altar<br/>+ a sac outlet"}:::ask
    A1 -- assembled --> K1["<b>infinite deaths → drain (deterministic)</b><br/>⏱ table T9+"]:::combo
    A1 --> A2{"Gray Merchant of Asphodel<br/>+ heavy black devotion"}:::ask
    A2 -- assembled --> K2["<b>ETB drain ×2</b><br/>⏱ table"]:::table
    A2 --> A3{"Kokusho, the Evening Star<br/>+ a sac outlet"}:::ask
    A3 -- assembled --> K3["<b>5-drain ×2 each death cycle</b><br/>⏱ table"]:::table
    A3 --> A4{"Living Death<br/>(mass reanimation)"}:::ask
    A4 -- assembled --> K4["<b>refill board → re-fire every death</b><br/>⏱ reset → table"]:::table
    A4 --> A5{"Razaketh, the Foulblooded<br/>+ fodder to sacrifice"}:::ask
    A5 -- assembled --> K5["<b>tutor the missing piece of any line</b><br/>⏱ enabler"]:::enabler
    A5 --> A6{"wide token board swings<br/>(fallback)"}:::ask
    A6 -- assembled --> K6["<b>focus one opponent</b><br/>⏱ decap T9"]:::combat
    A6 -- not yet --> STALL["grind deaths — the table drain is slow (T12+);<br/>this deck disrupts, it doesn't race"]:::stall
```

---

*Adding a deck: encode its lab's KILL CHECKS (cheapest-first) into `DECKS` in
`scripts/kill_tree.py` — id, pieces needed, kill, lab clock, kind — then
`--all`. Keep the clocks lab-sourced so the picture stays honest.*
