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
fenced ` ```mermaid ` blocks below natively; the Mermaid Chart tool validated them.
All **17 active decks** are encoded (the 4 detailed showcases below, then the rest);
the dashboard deck pages render the same ladders natively.

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

## Lorehold Spirits — Quintorius, History Chaser

Spirit go-wide off Quintorius's −4 alpha, a Purphoros table-ping line, and the Reveillark / Karmic Guide / Goblin Bombardment loop as the combo.

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

    S(["Quintorius (planeswalker) resolved<br/>each time cards LEAVE your graveyard → a 3/2 Spirit (one per event)"]):::root
    S --> A1{"Quintorius −4 (ready ~1 turn after landing) + 4+ Spirits<br/>(Akroma's Will / anthems pile on)"}:::ask
    A1 -- assembled --> K1["<b>Spirits gain double strike + vigilance → lethal alpha across the table</b><br/>⏱ table T7–9"]:::combat
    A1 --> A2{"Purphoros + Anointed Procession<br/>+ a recursion turn (3 events)"}:::ask
    A2 -- assembled --> K2["<b>2→4 dmg to EACH opp per Spirit ETB → ~12 to each opp passively</b><br/>⏱ table T7–9"]:::table
    A2 --> A3{"Moonshaker Cavalry ETB<br/>+ a wide Spirit board (Procession / Patchwork)"}:::ask
    A3 -- assembled --> K3["<b>all creatures gain flying + a counter → one-turn lethal swing on one opp</b><br/>⏱ decap T7–9"]:::combat
    A3 --> A4{"Reveillark + Karmic Guide + Goblin Bombardment<br/>+ a ≤2-power creature in yard"}:::ask
    A4 -- assembled --> K4["<b>unbounded sac loop → arbitrary GB damage + arbitrary Spirits</b><br/>⏱ table T7–8"]:::combo
    A4 --> A5{"Patchwork Banner + Balefire Liege + Tocasia's Welcome<br/>(Quintorius & Moonshaker down) (fallback)"}:::ask
    A5 -- assembled --> K5["<b>anthem + 3-per-RW-cast chip → 3–4 turn grindout</b><br/>⏱ table T9–11"]:::table
    A5 -- not yet --> STALL["run Quintorius +1 to fill the yard + dig; deploy recursion + a multiplier —<br/>every recursion event is a Spirit, so build toward the −4 alpha"]:::stall
```

## Earthbend the Meta — Toph, the First Metalbender

Lands-matter: Scute Swarm + Purphoros table ping, Triumph infect, and All Will Be One counter-burn — decap and table both land in the T7–9 window.

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

    S(["Toph resolved — your nontoken artifacts are LANDS (each artifact ETB is a landfall)<br/>end step earthbends a land into a 0/0+counters creature"]):::root
    S --> A1{"Scute Swarm at 6+ lands + Purphoros<br/>(+ Impact Tremors / Cathars' Crusade)"}:::ask
    A1 -- assembled --> K1["<b>each landfall copies Scute → 2 dmg to EACH opp per body → 20+ to each opp</b><br/>⏱ table T7–9"]:::table
    A1 --> A2{"Triumph of the Hordes<br/>+ 3 earthbent lands at 4+ counters"}:::ask
    A2 -- assembled --> K2["<b>+1/+1, trample & INFECT → 10 poison kills regardless of life</b><br/>⏱ table T7–9"]:::table
    A2 --> A3{"All Will Be One + amplifier suite<br/>(Hardened Scales / Earth Crystal / Doubling Season)"}:::ask
    A3 -- assembled --> K3["<b>each +1/+1 counter placed → that much to ONE opp; earthbend 2 = 12+</b><br/>⏱ decap T7–9"]:::combat
    A3 --> A4{"Toph, Greatest Earthbender (double strike)<br/>+ 3–4 earthbent lands (8–24 each)"}:::ask
    A4 -- assembled --> K4["<b>land-creatures swing for lethal double-strike damage on one opp</b><br/>⏱ decap T7–9"]:::combat
    A4 --> A5{"Moraug + multiple land drops<br/>+ double-strike land-creatures (fallback)"}:::ask
    A5 -- assembled --> K5["<b>3–5 extra combat phases → lethal through accumulated steps on one opp</b><br/>⏱ decap T7–9"]:::combat
    A5 -- not yet --> STALL["ramp + animate lands each end step, stacking counters under the amplifier suite —<br/>the deck doesn't tutor, so dig for a finisher while Scute snowballs"]:::stall
```

## The Exile's Return — Fire Lord Zuko

The Zuko counter-stack commander-damage line is the real clock (decap T8); the Hellkite Charger + Sozin's Comet infinite-combats is the rare marquee (table T10).

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

    S(["Fire Lord Zuko resolved<br/>each cast-from-exile + each permanent entering from exile puts +1/+1 on EACH creature you control"]):::root
    S --> A1{"blink + cast-from-exile engine running<br/>(Panharmonicon doubles enters-events) → Zuko 7+ power"}:::ask
    A1 -- assembled --> K1["<b>counter-pumped board + 21 Zuko commander damage in ~3 swings</b><br/>⏱ decap T7–8"]:::combat
    A1 --> A2{"Hellkite Charger + Sozin's Comet<br/>(firebending 5 on all; only Diabolic Intent finds either)"}:::ask
    A2 -- assembled --> K2["<b>20R combat income pays Hellkite's 5RR → infinite extra combats → table</b><br/>⏱ table T10"]:::combo
    A2 --> A3{"The Legend of Roku III → Avatar Roku<br/>(4/4 firebending 4)"}:::ask
    A3 -- assembled --> K3["<b>attacks for 4R, funds dragon-token activations — backup when blink is down</b><br/>⏱ decap T11+"]:::combat
    A3 --> A4{"Sun Titan attacks → return a ≤MV3 permanent<br/>(+ a blink piece to re-loop it) (fallback)"}:::ask
    A4 -- assembled --> K4["<b>rebuild the engine every attack → grind out, very durable post-wipe</b><br/>⏱ decap (slow/durable)"]:::enabler
    A4 -- not yet --> STALL["land an impulse-draw or blinker, then a doubler (Panharmonicon) / repeating blink<br/>(Teleportation Circle, Airbender Ascension, Norin) — pile counters until Zuko swings"]:::stall
```

## Zero-Sum Game — Witherbloom, the Balancer

The Exquisite Blood lifeloop is commander-INDEPENDENT (table T9), with a Chain of Smog two-card drain and the slower affinity infinite as resilience.

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

    S(["go wide cheaply (dorks / Bitterblossom / Saprolings)<br/>Witherbloom's instant/sorcery affinity discounts your tutors & rituals<br/>(the primary lifeloop is commander-INDEPENDENT)"]):::root
    S --> A1{"a blood-half (Exquisite Blood / Bloodthirsty Conqueror)<br/>+ a vito-half (Vito / Sanguine Bond / Enduring Tenacity / Defiant Bloodlord)<br/>+ any life event (combat, Cauldron Familiar, a sac)"}:::ask
    A1 -- assembled --> K1["<b>the loop drains the whole table one player at a time, at instant speed</b><br/>⏱ table T9"]:::combo
    A1 --> A2{"Chain of Smog + Witherbloom Apprentice<br/>(no board, no commander needed)"}:::ask
    A2 -- assembled --> K2["<b>target yourself → infinite magecraft copies → 1–2 to each opp per copy</b><br/>⏱ table"]:::combo
    A2 --> A3{"Witherbloom + 4+ creatures + Sprout Swarm<br/>(or Lab Rats + Phyrexian Altar) + Witherbloom Apprentice"}:::ask
    A3 -- assembled --> K3["<b>infinite free casts → magecraft drains the table</b><br/>⏱ table (later)"]:::combo
    A3 --> A4{"Razaketh, the Foulblooded + tokens to sacrifice"}:::ask
    A4 -- assembled --> K4["<b>2 life + a token each → tutor the missing loop piece at instant speed</b><br/>⏱ enabler"]:::enabler
    A4 --> A5{"Bitterblossom fliers + Tendershoot + Hornet Queen<br/>(fallback)"}:::ask
    A5 -- assembled --> K5["<b>focus one opponent — irrelevant as a clock, real as loop ignition</b><br/>⏱ decap T12+"]:::combat
    A5 -- not yet --> STALL["build a token board (affinity discounts + sac fodder + ignition) and dig<br/>with the tutors for a blood-half + a vito-half — the loop is the deck"]:::stall
```

## Curse of the Scarab — The Scarab God

The Scarab God upkeep drain is the always-on table lane (~T11); Gray Merchant burst and lord-pumped combat are the faster decap (~T8).

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

    S(["The Scarab God resolved (~T5)<br/>flood the board with Zombies (tribal + tokens + reanimation)<br/>Zombie count drives drain, draw & combat"]):::root
    S --> A1{"Gray Merchant of Asphodel ETB<br/>(devotion 6–10; recur via Reanimate / Necromancy / Scarab activated)"}:::ask
    A1 -- assembled --> K1["<b>each opponent loses your black devotion on ETB; recurs for repeat bursts</b><br/>⏱ table (fastest non-combo)"]:::table
    A1 --> A2{"Warren Soultrader + Gravecrawler + Plague Belcher<br/>(Rule 0)"}:::ask
    A2 -- assembled --> K2["<b>sac/recast Gravecrawler loop → each cycle drains 1; up to 39 at 40 life</b><br/>⏱ table T8+"]:::combo
    A2 --> A3{"Rooftop Storm + Necroduality + Diregraf Colossus"}:::ask
    A3 -- assembled --> K3["<b>empty a Zombie hand for free → 12+ Zombies → 12+ Scarab drain next upkeep</b><br/>⏱ table T9–10"]:::table
    A3 --> A4{"lord-pumped Zombies (Death Baron / Warchief / Mikaeus)<br/>+ Cyclonic Rift (overload) clears blockers (fallback)"}:::ask
    A4 -- assembled --> K4["<b>focus-fire one opponent with a 4/4+ wide board</b><br/>⏱ decap T8"]:::combat
    A4 -- not yet --> STALL["grow the Zombie count + draw (Kindred Discovery); the upkeep drain is passive<br/>inevitability — board wipes feed the yard for Living Death, so don't fear them"]:::stall
    BG[["a wide Zombie board live"]]:::bg
    BG -. always on .-> KBG["<b>each opponent loses X = Zombies you control, every upkeep (no mana/attack)</b><br/>⏱ table ~T11"]:::table
```

## Ms. Bumbleflower — Ms. Bumbleflower

A slow, combat-only kill: the Jolrael full-hand alpha (decap T8), Willbreaker theft, and evasive counter-beats — no infinite, no drain.

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

    S(["Ms. Bumbleflower online (~T3–4)<br/>each spell you cast: an opp draws, +1/+1 counter (+flying) on a creature;<br/>the 2nd cast each turn → you draw two"]):::root
    S --> A1{"Jolrael, Mwonvuli Recluse + a full hand + a board<br/>(Cats / payoff creatures / stolen bodies)"}:::ask
    A1 -- assembled --> K1["<b>Jolrael's 4GG pump sets your team to X/X (X = cards in hand) → 8–12-power alpha</b><br/>⏱ decap T8"]:::combat
    A1 --> A2{"Willbreaker + aim Bumbleflower's counter at an opp's creature each cast"}:::ask
    A2 -- assembled --> K2["<b>steal a creature every spell (it flies in that turn) → swing with their own board</b><br/>⏱ decap (grindy)"]:::combat
    A2 --> A3{"pile +1/+1 counters & flying on one carrier each cast<br/>(optionally vacuum them into Sin, Unending Cataclysm) (fallback)"}:::ask
    A3 -- assembled --> K3["<b>a single evasive counter-grown threat flies over</b><br/>⏱ decap T8+ (slowest)"]:::combat
    A3 -- not yet --> STALL["out-value the table — chain cantrips for the 2nd-cast draw-two, deploy draw payoffs,<br/>hold up the deep counter/removal suite; the kill is slow & combat-only, so close from dominance"]:::stall
```

## Eldrazi Stampede Chaos — Maelstrom Wanderer

Ramp into Wanderer / Ghalta decap beats, with the Craterhoof trample-distribute table alpha as the real table kill (T12).

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

    S(["Maelstrom Wanderer cast (5GUR)<br/>two cascades into nonland MV<8 + creatures you control have haste"]):::root
    S --> A1{"Ghalta, Primal Hunger<br/>(a wide Eldrazi/power board drops its cost toward GG)"}:::ask
    A1 -- assembled --> K1["<b>12/12 trample lands cheap → annihilator + trample close</b><br/>⏱ decap T5–7"]:::combat
    A1 --> A2{"Wanderer's two hasty cascades<br/>+ its own 7 power + beater pile"}:::ask
    A2 -- assembled --> K2["<b>15–25 turn-of-cast → focus one opponent</b><br/>⏱ decap T8"]:::combat
    A2 --> A3{"Craterhoof Behemoth (8 mana, haste)<br/>+ 8 creatures on board"}:::ask
    A3 -- assembled --> K3["<b>+X/+X & TRAMPLE → swing distributes across the table</b><br/>⏱ table T12"]:::table
    A3 --> A4{"Sunbird's Invocation resolved<br/>then hardcast a big Eldrazi from hand"}:::ask
    A4 -- assembled --> K4["<b>free chained spells off each cast → snowball to lethal</b><br/>⏱ table T6+"]:::enabler
    A4 --> A5{"Ulamog, the Ceaseless Hunger hardcast (10 mana)<br/>(fallback)"}:::ask
    A5 -- assembled --> K5["<b>attacks exile 20 cards → mill out (uncounterable back-up)</b><br/>⏱ table T8+ (slow)"]:::table
    A5 -- not yet --> STALL["re-ramp toward the 8-mana Wanderer cast and a wide board —<br/>no passive drain; the Craterhoof table-alpha is what closes (~T12)"]:::stall
```

## The Dark Lord's Army — Sauron, the Dark Lord

Opponent-driven: an always-on draw-punisher drain (table T12) plus an evasive Orc Army decap and an aristocrats / reanimation grind.

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

    S(["Sauron resolved — engine is OPPONENT-DRIVEN<br/>every opponent spell amasses Orcs; the draw-punishers drain on every opponent draw"]):::root
    S --> A1{"Army amassed by opponent spells<br/>+ evasion (Cover of Darkness / Rogue's Passage)"}:::ask
    A1 -- assembled --> K1["<b>10+ power unblockable Orc Army → focus one opponent in 2–3 swings</b><br/>⏱ decap T9"]:::combat
    A1 --> A2{"Gray Merchant of Asphodel ETB<br/>(high black devotion from the engine)"}:::ask
    A2 -- assembled --> K2["<b>each opponent loses your black devotion on ETB → burst close</b><br/>⏱ table (burst)"]:::table
    A2 --> A3{"Dictate of Erebos + Goblin Bombardment + Pitiless Plunderer<br/>(sac the Army, it reforms free)"}:::ask
    A3 -- assembled --> K3["<b>forced opponent sacs + Treasure → relentless grind</b><br/>⏱ grind (relentless)"]:::enabler
    A3 --> A4{"Living Death / Reanimate / Agadeem's Awakening<br/>(Ring discards stock the yard)"}:::ask
    A4 -- assembled --> K4["<b>reanimate Sheoldred / Gray Merchant / Yawgmoth → re-fire the drain</b><br/>⏱ reset → table"]:::enabler
    A4 -- not yet --> STALL["let the pod play the game — amass + drain feed on THEIR spells and draws;<br/>deploy engine pieces and hold up interaction (faster vs active pods)"]:::stall
    BG[["Sheoldred + Underworld Dreams + Bowmasters<br/>(Wound Reflection doubles the end-step loss)"]]:::bg
    BG -. always on .-> KBG["<b>all-opponent drain on every opponent draw</b><br/>⏱ table T12 (typical pod)"]:::table
```

## Lightning War — Fire Lord Azula

Best-line: the Reiterate + Seething Song combo (table T9) raced against the X-burn / pinger chip on one game; Banefire deletes the counter-wall.

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

    S(["Fire Lord Azula attacking — every spell you cast that combat is COPIED<br/>(3× with Twinning Staff); she only needs to be DECLARED as an attacker, not connect"]):::root
    S --> A1{"Reiterate + Seething Song (infinite red mana)<br/>or Narset's Reversal + Frantic Search / Turnabout / Storm-Kiln"}:::ask
    A1 -- assembled --> K1["<b>infinite mana/draw → Torment of Hailfire / multikicked Comet Storm = dead table</b><br/>⏱ table T9"]:::combo
    A1 --> A2{"Azula attacking + an X-finisher (Crackle / Comet Storm)<br/>doubled by Twinning Staff / Galvanic Iteration"}:::ask
    A2 -- assembled --> K2["<b>Crackle X=3 ×Twinning = 45 to each opp; chip from Guttersnipe / Vivi pingers</b><br/>⏱ table T11 / decap T10"]:::table
    A2 --> A3{"Banefire X≥5 (uncounterable, can't be prevented)<br/>copied by Azula + a flash enabler"}:::ask
    A3 -- assembled --> K3["<b>delete the counter-wall player — ignores countermagic</b><br/>⏱ decap"]:::combat
    A3 --> A4{"flash enabler + Yawgmoth's Will / Past in Flames / Invoke Calamity<br/>(replay the yard in Azula's combat)"}:::ask
    A4 -- assembled --> K4["<b>every replayed spell copied → 40+ damage (non-infinite, dies to gy hate)</b><br/>⏱ table (fragile backup)"]:::enabler
    A4 -- not yet --> STALL["tutor toward one loop piece + a sink and kill on YOUR turn<br/>(Abolisher can't stop a kill cast in your own combat); burn doubles as removal — delete Grand Abolisher on sight"]:::stall
```

## The Grand Design — Atraxa, Grand Unifier

Craterhoof is the working finisher (decap T9, tutorable); Defense of the Heart cheats it in, Razaketh chains to it, and Finale X≥10 is the late ceiling.

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

    S(["Atraxa cast — ETB reveals top 10, take one of each card type (nets 5–7 cards)<br/>fuels reanimation + flicker + Birthing Pod creature chain"]):::root
    S --> A1{"Craterhoof Behemoth + a board<br/>(hardcast 8, or Pod / Defense / reanimate / Finale X≥8 cheat it in)"}:::ask
    A1 -- assembled --> K1["<b>ETB haste: creatures gain TRAMPLE + +X/+X → overrun (reliably decaps; table slower)</b><br/>⏱ decap T9"]:::combat
    A1 --> A2{"Defense of the Heart resolves<br/>(any opponent has 3+ creatures at your upkeep)"}:::ask
    A2 -- assembled --> K2["<b>free: search 2 creatures onto battlefield (Craterhoof straight to play → immediate kill)</b><br/>⏱ decap T9"]:::enabler
    A2 --> A3{"Razaketh reanimated (Reanimate ~1 mana)<br/>+ creatures to sacrifice"}:::ask
    A3 -- assembled --> K3["<b>sac fodder, pay 2 life: tutor any card → grab Craterhoof / Finale → kill next turn</b><br/>⏱ decap T10–11"]:::enabler
    A3 --> A4{"Finale of Devastation X≥10 (12 mana, untutorable sorcery)<br/>+ a creature in play"}:::ask
    A4 -- assembled --> K4["<b>+X/+X & haste to all — but no trample, so it FOCUS-FIRES one opponent</b><br/>⏱ decap T11 (~9% of games)"]:::combat
    A4 --> A5{"Atraxa swinging (7/7 flying, vigilance, deathtouch, lifelink)<br/>+ a developed board (fallback)"}:::ask
    A5 -- assembled --> K5["<b>incremental combat — 96% of the deck's decaps; or 21 commander damage</b><br/>⏱ decap T10 / table T12+"]:::combat
    A5 -- not yet --> STALL["build the engine (reanimate a bomb T3–4, cast Atraxa T6–7, or start a Pod chain) —<br/>the deck grinds at sorcery speed; protect the kill turn behind a counter or Teferi (protection is thin)"]:::stall
```

## Crystal Sickness — Golbez, Crystal Collector

Golbez's end-step drain off a binned high-power creature (Dreadnought 12) is the table clock (T13); Urza / Thopter combat decaps ~2 turns sooner.

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

    S(["Golbez online with 8+ artifacts<br/>each end step return a creature from your yard; with 8+ artifacts EACH opponent loses life = its power"]):::root
    S --> A1{"Phyrexian Dreadnought in the yard (12 power)<br/>recur + re-bin for 1 mana each turn"}:::ask
    A1 -- assembled --> K1["<b>12 drain to each opponent every end step → ~4 cycles</b><br/>⏱ table T13"]:::table
    A1 --> A2{"Master of Etherium in the yard<br/>(= your artifact count; reads in graveyard)"}:::ask
    A2 -- assembled --> K2["<b>10+ drain to each opponent, scales with the 8-artifact board</b><br/>⏱ table T13"]:::table
    A2 --> A3{"Tezzeret, Master of the Bridge +2<br/>(X = artifacts, to EACH opponent, once/turn)"}:::ask
    A3 -- assembled --> K3["<b>stacks with Golbez → 20+ life loss per opp per turn</b><br/>⏱ table ~T11"]:::table
    A3 --> A4{"Urza's Construct (= artifacts) / 6+ flying Thopters<br/>(3/3 with Master + Stridehangar)"}:::ask
    A4 -- assembled --> K4["<b>focus-fire one opponent in the air (decap leads by ~2)</b><br/>⏱ decap T11"]:::combat
    A4 --> A5{"Mirrodin Besieged (Phyrexian)<br/>+ 15 artifact cards in YOUR graveyard (fallback)"}:::ask
    A5 -- assembled --> K5["<b>target opponent loses the game each end step (dodges lifegain/fog)</b><br/>⏱ table T13+ (slowest)"]:::table
    A5 -- not yet --> STALL["deploy artifacts toward the 8-count and bin a drain bomb (Dreadnought self-sac / Troll swampcycle / surveil);<br/>refill the hand — the engine is card draw, not the curve"]:::stall
```

## Croak and Dagger — Glarb, Calamity's Augur

Glarb grind-fortress: Torment of Hailfire X=12+ (table T10) and a kicked Rite of Replication copy kill, backed by the Seedborn value engine.

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

    S(["Glarb online (cast MV4+ spells & play lands off the top, tap to surveil 2)<br/>+ a massive land count; Seedborn Muse untaps him + lands on EVERY opponent's turn"]):::root
    S --> A1{"Torment of Hailfire X=12+ (~14 mana via Cabal Coffers + Urborg)<br/>just the spell + a big Coffers tap"}:::ask
    A1 -- assembled --> K1["<b>each opponent: 12× lose-3 / sac / discard → lethal table drain (board-independent)</b><br/>⏱ table T10"]:::table
    A1 --> A2{"kicked Rite of Replication (9 mana) on a drainer<br/>— Gray Merchant (~60/opp) or Kokusho (25/opp)"}:::ask
    A2 -- assembled --> K2["<b>5 token copies' ETBs / legend-rule deaths drain the whole table at once</b><br/>⏱ table T10"]:::combo
    A2 --> A3{"Glarb surveil bins Gray Merchant → Reanimate (1 mana) returns him<br/>→ kicked Rite (9)"}:::ask
    A3 -- assembled --> K3["<b>feeds the Rite copy kill from the graveyard (~10 mana, 2 cards)</b><br/>⏱ enabler → table T10"]:::enabler
    A3 --> A4{"Seedborn engine — Glarb untapped every opponent's turn<br/>+ flash enabler → Archon of Cruelty / Massacre Wurm value"}:::ask
    A4 -- assembled --> K4["<b>grind the table out through accumulated drain / removal (no single combo)</b><br/>⏱ table (grind)"]:::table
    A4 --> A5{"drainers + creatures attack (Archon attack trigger)<br/>(fallback)"}:::ask
    A5 -- assembled --> K5["<b>focus one opponent</b><br/>⏱ decap T10"]:::combat
    A5 -- not yet --> STALL["ramp toward 10+ lands + Coffers/Urborg and surveil for Torment —<br/>can't out-race the T6–7 pod, so grind + hold the counter suite; don't announce the kill"]:::stall
```

## Forced Liquidation — Kefka, Court Mage

A wheel cast on your turn feeding static draw-punishers (fires through Grand Abolisher): Notion Thief + Psychosis Crawler is the marquee table kill (T9).

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

    S(["Grixis 'forced draw' punisher shell — static draw/discard punishers in play<br/>the kill is a WHEEL cast on YOUR turn feeding STATICS, so it fires THROUGH Grand Abolisher"]):::root
    S --> A1{"Notion Thief + Psychosis Crawler + any wheel<br/>(Niv-Mizzet, Parun = redundant version)"}:::ask
    A1 -- assembled --> K1["<b>you draw ~28 (your 7 + ~21 redirected) → each opponent loses ~28 AND draws nothing</b><br/>⏱ table T9"]:::table
    A1 --> A2{"2+ opponent-draw punishers (Underworld Dreams / Fate Unraveler / Sheoldred / Ob Nixilis)<br/>+ a wheel · Bloodletter of Aclazotz doubles it"}:::ask
    A2 -- assembled --> K2["<b>each opponent draws 7 → ~14–28 life loss each (lethal-or-bust — never spin on one)</b><br/>⏱ table T9"]:::table
    A2 --> A3{"Peer into the Abyss aimed at one opponent<br/>with a draw-punisher out"}:::ask
    A3 -- assembled --> K3["<b>they draw ~half their library → that much damage + lose half their life</b><br/>⏱ decap T8"]:::combat
    A3 --> A4{"Displacer Kitten + Aether Channeler + Sol Ring + Mana Vault<br/>+ Niv-Mizzet or Psychosis Crawler (all in play)"}:::ask
    A4 -- assembled --> K4["<b>infinite ETB → infinite draw → lethal (Abolisher-proof, commander-independent)</b><br/>⏱ table ~1% by T12 (slow backup)"]:::combo
    A4 -- not yet --> STALL["assemble + protect ~2 punishers to the wheel turn (lethal-or-bust — a half-loaded wheel refuels the pod);<br/>kill Grand Abolisher / draw-deniers on sight, and don't stack Notion Thief with the opponent-draw punishers"]:::stall
```

---

*Adding/refreshing a deck: encode its lab's KILL CHECKS (cheapest-first) into
`KILL_TREES` in `scripts/deck_registry.py` — id, pieces needed, kill, lab clock,
kind — then `python scripts/kill_tree.py --all` (regenerates the `.mmd`) and
re-bake the deck pages (the dashboard reads the same specs via
`kb_content._kill_tree`). Keep the clocks lab-sourced so the picture stays honest.*
