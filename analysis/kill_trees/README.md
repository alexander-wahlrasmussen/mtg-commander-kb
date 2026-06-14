# Kill trees — a deck's win lines as a decision diagram

Backlog #4. Each tree reads top-to-bottom as the decision a pilot actually makes:
**try the fastest available kill line; if its pieces aren't assembled, fall to the
next.** The lines, their pieces, and their clocks come straight from the deck's
`*_clock_lab.py` (KILL CHECKS, cheapest-first) and its audited Summary — this is
pure visualization, not a new model.

Leaf colours: 🩷 **combo** (deterministic/loop) · 💙 **table** (all-opponent
drain/poison) · 🧡 **combat** (focus-fire one opponent = decap) · 💚 **enabler**
(tutor/reset that feeds another line). The dashed lane is an **always-on**
background clock that ticks regardless of which line you assemble.

Styling is **dark-theme-safe**: every node sets an explicit text colour, so the
diagrams stay legible under a dark viewer (e.g. gruvbox in Obsidian) where nodes
otherwise inherit a light foreground and wash out, as well as on GitHub light/dark.

Generate with `python scripts/kill_tree.py <deck>` (`--list` for encoded decks,
`--all` for every one); the `.mmd` files here are the output. GitHub renders the
fenced ` ```mermaid ` blocks below natively; the Mermaid Chart tool validated all four.

---

## Radiation Sickness — The Wise Mothman

Five lines that nearly all kill the **whole table at once** (the rad/drain engine
hits every opponent), so decap and table converge — and a passive rad drain that
closes on its own around T10 even if no combo lands.

```mermaid
flowchart TD
    classDef root fill:#3c3836,color:#fbf1c7,stroke:#fabd2f,stroke-width:3px;
    classDef ask fill:#ebdbb2,color:#1d2021,stroke:#7c6f64,stroke-width:1.5px;
    classDef combo fill:#f5b8d6,color:#1d2021,stroke:#b16286,stroke-width:2px;
    classDef table fill:#aed1f0,color:#1d2021,stroke:#458588,stroke-width:2px;
    classDef combat fill:#fec07c,color:#1d2021,stroke:#d65d0e,stroke-width:2px;
    classDef enabler fill:#b8e6a0,color:#1d2021,stroke:#689d6e,stroke-width:2px;
    classDef bg fill:#cbe8b8,color:#1d2021,stroke:#689d6e,stroke-width:1.5px,stroke-dasharray:5 4;
    classDef stall fill:#d5c4a1,color:#3c3836,stroke:#928374,stroke-width:1.5px;

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
    classDef root fill:#3c3836,color:#fbf1c7,stroke:#fabd2f,stroke-width:3px;
    classDef ask fill:#ebdbb2,color:#1d2021,stroke:#7c6f64,stroke-width:1.5px;
    classDef combo fill:#f5b8d6,color:#1d2021,stroke:#b16286,stroke-width:2px;
    classDef table fill:#aed1f0,color:#1d2021,stroke:#458588,stroke-width:2px;
    classDef combat fill:#fec07c,color:#1d2021,stroke:#d65d0e,stroke-width:2px;
    classDef enabler fill:#b8e6a0,color:#1d2021,stroke:#689d6e,stroke-width:2px;
    classDef bg fill:#cbe8b8,color:#1d2021,stroke:#689d6e,stroke-width:1.5px,stroke-dasharray:5 4;
    classDef stall fill:#d5c4a1,color:#3c3836,stroke:#928374,stroke-width:1.5px;

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

## The Genome Project — Kuja, Genome Sorcerer

A **race leader** (decap T7 / table T8, lab `gp_clock_lab.py`). Unlike the combat
decks, Kuja's Wizard tokens ping **every opponent** on each noncreature cast, so
decap and table converge off the *same* ping clock instead of diverging. There's
no passive lane — pings need casts — so the ladder is an escalation: stack
multipliers for a one-spell kill, or chain cheap spells; the combat leaf is a
minor fallback, not a separate slow clock.

```mermaid
flowchart TD
    classDef root fill:#3c3836,color:#fbf1c7,stroke:#fabd2f,stroke-width:3px;
    classDef ask fill:#ebdbb2,color:#1d2021,stroke:#7c6f64,stroke-width:1.5px;
    classDef combo fill:#f5b8d6,color:#1d2021,stroke:#b16286,stroke-width:2px;
    classDef table fill:#aed1f0,color:#1d2021,stroke:#458588,stroke-width:2px;
    classDef combat fill:#fec07c,color:#1d2021,stroke:#d65d0e,stroke-width:2px;
    classDef enabler fill:#b8e6a0,color:#1d2021,stroke:#689d6e,stroke-width:2px;
    classDef bg fill:#cbe8b8,color:#1d2021,stroke:#689d6e,stroke-width:1.5px,stroke-dasharray:5 4;
    classDef stall fill:#d5c4a1,color:#3c3836,stroke:#928374,stroke-width:1.5px;

    S(["Kuja resolved — Wizard tokens ping EVERY opponent on each noncreature cast<br/>transforms to Trance Kuja (×2 ALL Wizard damage) at 4 Wizards"]):::root
    S --> A1{"Trance Kuja + City on Fire (×3 all dmg)<br/>and/or Harmonic Prodigy / Roaming Throne"}:::ask
    A1 -- assembled --> K1["<b>12–16+ damage per opponent per spell → one or two casts kill the table</b><br/>⏱ table T7"]:::combo
    A1 --> A2{"Trance Kuja + 4 Wizard tokens<br/>(Birgi / Storm-Kiln refund the mana)"}:::ask
    A2 -- assembled --> K2["<b>8 dmg per opponent per noncreature cast → ~5 cheap casts</b><br/>⏱ table T8"]:::table
    A2 --> A3{"stocked graveyard + Mizzix's Mastery<br/>(Dawn Warriors' Legacy) or Underworld Breach"}:::ask
    A3 -- assembled --> K3["<b>recast every i/s from the yard — each a REAL cast = full pings</b><br/>⏱ table T7–8"]:::combo
    A3 --> A4{"mana flood (Mana Geyser / Neheb / Jeska's Will)<br/>or 50 life via Aetherflux Reservoir"}:::ask
    A4 -- assembled --> K4["<b>board-independent table drain / 50-life laser</b><br/>⏱ table (backup)"]:::table
    A4 --> A5{"Trance Kuja + a Wizard board<br/>(Trance doubles Wizard power) (fallback)"}:::ask
    A5 -- assembled --> K5["<b>focus one opponent</b><br/>⏱ decap T7"]:::combat
    A5 -- not yet --> STALL["build Wizards toward the 4-count transform & stock the yard —<br/>pings need CASTS (no passive drain), so dig for a multiplier + a cheap chain"]:::stall
```

## The Replication Crisis — Satya, Aetherflux Genius

A **race leader** on the decap clock (T7) but with the clock **diverging** hard —
table is T10+ — because every line is combat-gated on Satya connecting. Two fast
alpha lines (infinite combats; Brudiclad conversion), a token-flood, a disruption
line, and a slow value grind as the fallback. The whole tree rests on protecting a
3/5: that's the deck's defining vulnerability, surfaced in the stall.

```mermaid
flowchart TD
    classDef root fill:#3c3836,color:#fbf1c7,stroke:#fabd2f,stroke-width:3px;
    classDef ask fill:#ebdbb2,color:#1d2021,stroke:#7c6f64,stroke-width:1.5px;
    classDef combo fill:#f5b8d6,color:#1d2021,stroke:#b16286,stroke-width:2px;
    classDef table fill:#aed1f0,color:#1d2021,stroke:#458588,stroke-width:2px;
    classDef combat fill:#fec07c,color:#1d2021,stroke:#d65d0e,stroke-width:2px;
    classDef enabler fill:#b8e6a0,color:#1d2021,stroke:#689d6e,stroke-width:2px;
    classDef bg fill:#cbe8b8,color:#1d2021,stroke:#689d6e,stroke-width:1.5px,stroke-dasharray:5 4;
    classDef stall fill:#d5c4a1,color:#3c3836,stroke:#928374,stroke-width:1.5px;

    S(["Satya attacking — each attack makes a free token COPY of a nontoken<br/>creature you control + {E}{E} · EVERY line needs Satya to connect"]):::root
    S --> A1{"Sword of Feast and Famine on Satya<br/>+ Aggravated Assault"}:::ask
    A1 -- assembled --> K1["<b>combat untaps all lands → infinite combats → infinite tokens + ETBs</b><br/>⏱ decap T6–7"]:::combo
    A1 --> A2{"Brudiclad + a token pile<br/>+ a fat Satya copy (Inferno Titan)"}:::ask
    A2 -- assembled --> K2["<b>convert every token into the bomb → lethal alpha (no infinite needed)</b><br/>⏱ decap T7"]:::combat
    A2 --> A3{"Adeline + Anointed Procession"}:::ask
    A3 -- assembled --> K3["<b>~6 humans per attack + doubled Satya token → wide alpha swing</b><br/>⏱ decap T7–8"]:::combat
    A3 --> A4{"Satya copies Zealous Conscripts<br/>(+ Strionic Resonator / Aggravated Assault)"}:::ask
    A4 -- assembled --> K4["<b>steal the pod's best permanents, one per combat</b><br/>⏱ disrupt → decap"]:::enabler
    A4 --> A5{"repeated ETB copies (Inferno Titan ping,<br/>Cloudblazer draw, Skyclave exile) (fallback)"}:::ask
    A5 -- assembled --> K5["<b>grind the pod out over 3–4 combats</b><br/>⏱ table T10+"]:::table
    A5 -- not yet --> STALL["Satya must survive as a 3/5 through combat — protect her<br/>(Greaves / Boots / Slip Out the Back) and hold for a safe swing"]:::stall
```

---

*Adding a deck: encode its lab's KILL CHECKS (cheapest-first) into `DECKS` in
`scripts/kill_tree.py` — id, pieces needed, kill, lab clock, kind — then
`--all`. Keep the clocks lab-sourced so the picture stays honest.*
