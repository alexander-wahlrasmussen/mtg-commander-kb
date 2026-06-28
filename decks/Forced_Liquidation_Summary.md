# Forced Liquidation

**Commander:** Kefka, Court Mage // Kefka, Ruler of Ruin (Grixis / BRU)
**Archetype:** Spellslinger — forced-draw wheel-burn / punisher static
**Bracket:** 3 (3 GC; B4-in-spirit per house rules)
**Score:** 16/20 (5 / 4 / 3 / 4) · Clock: T8 decap / T9 table (spell, sorcery) (lab `kfk_clock_lab.py` 2026-06-25). Audited 2026-06-27 from the list (pre-pod; re-audit after first games).

> Build ground truth: `decks/forced-liquidation-20260625.txt` (promoted from `considering/` to the active roster 2026-06-28). Proposal: `proposals/PROP_Kefka_Court_Mage.md`. Buy list: `analysis/Buy_List_ZeroSum_LightningWar_ForcedLiquidation_2026-06-25.md`.

---

## Core Loop

This deck weaponizes *drawing cards* as a damage source. The shell is ~7 wheel effects (Windfall, Echo of Eons, Reforge the Soul, Magus of the Wheel, Jace's Archivist, Molten Psyche, Dark Deal) plus Peer into the Abyss, backed by a redundant suite of static punishers that convert every draw or discard into life loss. Because the kill is a *wheel resolved on your own turn* feeding *static* triggers — not casts or activated abilities — it fires straight through a Grand Abolisher lock, which is the entire reason this deck exists (it answers the pod's recurring T6–7 Abolisher combo archenemy that the counter-heavy decks can't). Kefka himself is the value/disruption engine and a deliberate removal-magnet, **not** a combo linchpin: his ETB (each player discards, you draw one per card *type* discarded) is guaranteed value per cast, and the win runs entirely from the command zone if he dies.

---

## Closing Lines

1. **Notion Thief + Psychosis Crawler + any wheel** *(marquee, near-deterministic)* — Notion Thief redirects every opponent's wheel-draws to you; Psychosis Crawler pings each opponent 1 per *your* draw. One wheel → you draw your 7 + ~21 redirected ≈ 28 → each opponent loses ~28 → table dead, **and they draw nothing** (solves the refuel trap). Niv-Mizzet, Parun is the redundant version (~28 aimed damage). Online from ~T6–7 once two pieces assemble.
2. **Multi-punisher wheel** *(the default burn)* — with 2+ opponent-draw punishers down (Underworld Dreams, Fate Unraveler, Kederekt Parasite, Ob Nixilis the Hate-Twisted, Sheoldred), one wheel makes each opponent draw 7 → ~14–28 damage/life-loss each. **Bloodletter of Aclazotz doubles all of it** during your turn. **Lethal-or-bust:** never spin on a single punisher — that hands them 7 fresh cards.
3. **Peer into the Abyss** *(single-target nuke)* — pointed at one opponent with a draw-punisher out: they draw ~half their library (→ that much damage) and lose half their life. Kills one player and only refuels that player, not the table. The answer to a board too symmetric to wheel safely.
4. **Displacer Kitten + Aether Channeler + Sol Ring + Mana Vault** *(backup combo — resilience, not speed)* — CSB-registered complete combo `1170-1393-2364-5034`: infinite ETB + infinite colorless mana; route Channeler's "draw a card" ETB each iteration into Niv-Mizzet (1 dmg/draw) or Psychosis Crawler (each opp −1/draw) for a lethal that's commander-independent and resolves on your turn. **Caveat:** the lab assembles this in only ~1.2% of games by T12 and it never beats the burn — it's a $0 Abolisher-proof *backup* axis, not the plan.

---

## Don't-Miss Rulings

- **Notion Thief is a replacement, not a trigger** — it uses no stack and can't be countered. It redirects to you every opponent draw *except* the first one in each of their draw steps; wheel draws aren't draw-step draws, so **all** of them are stolen. Flash it in *before* the wheel resolves.
- **Notion Thief turns OFF your opponent-draw punishers** — while it's out, opponents don't draw (you do), so **Underworld Dreams / Fate Unraveler won't fire on a wheel.** Psychosis Crawler carries that kill instead. Don't plan on both at once.
- **Psychosis Crawler counts YOUR draws** — each opponent loses 1 life per card *you* draw, once per card (its ruling: multiple draws → multiple triggers). Notion Thief + a 7-card wheel = ~7 per opponent stolen onto you = a ~21 table swing. The marquee line.
- **Kefka draws per card TYPE, not per card** — each player discards one card; you draw one card for each *distinct type* among them (three lands → 1 draw; land + instant + creature → 3). And those are *your* draws, so they ping through Psychosis Crawler.
- **Peer into the Abyss rounds UP both halves** — aimed at an opponent with the draw-punishers out, they ping themselves drawing half their library; aimed at an opponent under your Notion Thief, *you* draw their half-library (Crawler hammers the table) and they still lose half their life. It only refuels that one player, never the table.
- **Underworld Dreams / Fate Unraveler ping per card and only on OPPONENTS' draws** — a "put into hand" that doesn't use the word *draw* (a tutor) doesn't ping; a wheel or Peer does.
- **The wheel-kill resolves THROUGH a Grand Abolisher** — it's a sorcery cast on *your* turn feeding *static* triggers, with no targeting of opponents' permanents and no stack interaction with their combo, so their Abolisher (which only locks you out on *their* turn) can't stop it. The entire reason this deck exists.
- **Displacer Kitten triggers on NONCREATURE spells only** — the backup combo (Kitten + Aether Channeler + Sol Ring + Mana Vault) blinks a rock for net mana and Channeler for a draw each cast. Don't blink a *token* (it vanishes), and remember the blink strips counters and auras.

---

## Kill Window

- **Goldfish:** Clock decap T8 / table T9 (lab `scripts/kfk_clock_lab.py`, 40k trials, 2026-06-25). Slower than the proposal's hand-estimated T6–7 brief — the usual optimistic-estimate correction.
- **Through Interaction:** *(unverified)* — slower; the deck is lethal-or-bust and must protect ~2 punishers to the wheel turn.

---

## Conversion Check — 16/20 (audited 2026-06-27)

Scored from the list per `reference/REF_The_Conversion_Check.md`. The four axes are judged; the clock is measured (`kfk_clock_lab.py`). Pre-pod — re-audit after first games.

| Axis | Score | Rationale |
|---|---|---|
| **Core Loop** | **5/5** | ~7 wheels × ~13 punisher/payoff cards + 3 tutors = 20+ pieces serving one recognizable machine (force draws/discards → static punishers convert to damage). The loop is the deck; highly redundant. |
| **Kill Reliability** | **4/5** | Multiple independent lines — Notion Thief + Psychosis (marquee), multi-punisher wheel, Peer, Kitten+Channeler backup combo. Held off 5 by *lethal-or-bust* (a mistimed wheel refuels opponents) and a sorcery-speed median T8/T9 kill. |
| **Durability** | **3/5** | The cap. Grixis (no green/white), punishers are wrath-fragile creatures/enchantments, Past in Flames recurs only the wheels (not the enchantment punishers). Redundant but recovers slowly for a racing deck with no inevitability. |
| **Interaction** | **4/5** | ~14 pieces — 8 removal (survive an Abolisher lock) + 6 counters + Deflecting Swat, instant-heavy and diverse. Off 5 because a racing, lethal-or-bust deck can't freely spend interaction without derailing its own clock. |

**Reading:** Solid (13–16), top of band. Lowest axis is **Durability** — the deck races and is wrath-vulnerable; it wins by assembling the Abolisher-proof burn before the pod combos, not by grinding. Same total as Zero-Sum Game (16) but the opposite shape (ZSG is Interaction-floored, FL is Durability-capped).

---

## Functional Baseline

- **Ramp:** 14 sources (2 burst / 11 repeatable + 1 creature) · 49 mana sources · 36 land · avg CMC 2.89 (`ramp_audit.py` 2026-06-27). **In-band (~48–50), no flags** — the repeatable-heavy split fits a deck that recasts wheels and redeploys punishers each turn; the 2 burst (Seething Song + a treasure) fund an explosive wheel turn. 4 nonland payoffs at CMC ≥ 6.
- **Buildability:** own 83/100 real+proxy (`availability_check.py` vs `moxfield_haves_2026-06-25-0748Z.csv`). **17 true buys ≈ €78** (premium = Bloodletter of Aclazotz ~€25, Echo of Eons ~€12; the rest cheap). 14 free undeployed copies incl. the commander, Notion Thief, Psychosis Crawler, Displacer Kitten, Nicol Bolas, Magus of the Wheel, Molten Psyche, Grim Tutor, Final Parting. **Scarce contention** (only copy locked elsewhere): **Sheoldred** (Dark Lord's Army) and **Seething Song / Ponder / Preordain / Past in Flames** — the last four are shared with **Lightning War**, the other on-order deck, so buy a 2nd or proxy to run both. Everything else flagged donor-pull is surplus (Sol Ring ×25, Lightning Greaves ×5, etc.) = effectively free.

---

## Durability

**The limiting axis (3/5).** Grixis has no green/white, so post-wrath recovery leans on recursion (Past in Flames re-buys wheels/punishers from the yard, Final Parting stacks the graveyard + tutors) and on Kefka's command-zone recastability. The punishers are mostly enchantments (Underworld Dreams, Fate Unraveler, Megrim, Liliana's Caress, Waste Not) and small creatures, so a board wipe on T7 sets the kill back ~2–3 turns to redeploy two punishers + a wheel. Redundancy is the real resilience: ~7 wheels and ~11 punisher/amplifier effects mean no single removal spell turns off the plan, and Kefka baits removal off the pieces that actually kill. The deck races rather than grinds — if it can't assemble before the pod's T6–7 combo, it loses.

---

## Interaction Package

**~15 pieces total.**

- **Removal:** 8 — Soul Shatter, Heartless Act, Go for the Throat, Bloodchief's Thirst, Dismember, Chaos Warp, Rakdos Charm, Blasphemous Act (board wipe). Cheap instant-speed answers to kill Grand Abolisher / combo pieces on sight.
- **Counters:** 6 — Counterspell, Negate, Swan Song, An Offer You Can't Refuse, Arcane Denial, Drown in the Loch. (Blank on the opponent's Abolisher turn — hence the kill is built to dodge that, and the counters cover non-Abolisher windows.)
- **Protection / redirect:** Deflecting Swat + Lightning Greaves + Swiftfoot Boots — protect Kefka and the wheel turn.

Instant speed: ~90% (nearly all removal + every counter, incl. Blasphemous Act). Sorcery speed: Bloodchief's Thirst.

---

## Game Changer Slots

**3 / 3 used.** *(Deck Doctor verified 2026-06-27: 3/3, no off-list GCs.)*

1. Notion Thief
2. Demonic Tutor
3. Mana Vault

No reskins. *Verified against `REF_Game_Changers_List.md` on 2026-06-27.*

---

## Known Weaknesses

- **Lethal-or-bust refuel trap.** A wheel with fewer than 2 punishers online (or no Notion Thief) hands the table fresh cards — actively helps the combo opponent. The deck must reliably assemble two pieces before T6, which is what the tutors (Demonic, Grim, Final Parting) and Mana Vault speed are for.
- **Wrath-vulnerable, racing deck.** Grixis can't go wide-and-recover like a green deck; a well-timed board wipe on the punisher shell costs ~2–3 turns and the deck has no inevitability to fall back on.
- **Draw-denier anti-synergy.** Notion Thief and Narset-type effects turn off the *opponent-draw* punishers (opponents draw nothing). Notion Thief earns its slot via the *your-draw* axis (Psychosis/Niv) — but don't stack draw-deniers and expect the opponent-facing burn to still fire.
- **Niv-Mizzet, Parun's `UUURRR` cost** strains a 3-color base; first cut if the manabase proves greedy.
- **No real land answers** (Deck Doctor `--interaction`: 1 — Chaos Warp). The one coverage hole; acceptable for a racer not trying to fight manabases. Every other type is healthy (creature 17 / artifact 6 / enchantment 5 / indestructible 8 / past-protection 9). Early ramp is also a touch light (10 sources by T3 / 61%, under the BDD ~12 anchor) — offset by draw (16 sources, 88% by T6).

---

## Decklist (100 cards)

*Functional buckets — partitioned card-for-card against `forced-liquidation-20260625.txt` (the dated `.txt` is ground truth; these headings only label it). Sums to 99 + commander.*

### Commander (1)
1 Kefka, Court Mage

### Wheels & Mass Draw (8)
1 Windfall
1 Echo of Eons
1 Reforge the Soul
1 Magus of the Wheel
1 Jace's Archivist
1 Molten Psyche
1 Dark Deal
1 Peer into the Abyss

### Draw Punishers (8)
1 Sheoldred, the Apocalypse
1 Underworld Dreams
1 Fate Unraveler
1 Kederekt Parasite
1 Ob Nixilis, the Hate-Twisted
1 Notion Thief
1 Psychosis Crawler
1 Niv-Mizzet, Parun

### Discard Punishers & Amplifiers (6)
1 Megrim
1 Liliana's Caress
1 Waste Not
1 Glint-Horn Buccaneer
1 Bloodletter of Aclazotz
1 Nicol Bolas, the Ravager

### Backup Combo (Displacer Kitten line) (2)
1 Displacer Kitten
1 Aether Channeler

### Tutors (3)
1 Demonic Tutor
1 Grim Tutor
1 Final Parting

### Card Filtering & Recursion (6)
1 Faithless Looting
1 Frantic Search
1 Thrill of Possibility
1 Ponder
1 Preordain
1 Past in Flames

### Removal (8)
1 Soul Shatter
1 Heartless Act
1 Go for the Throat
1 Bloodchief's Thirst
1 Chaos Warp
1 Dismember
1 Rakdos Charm
1 Blasphemous Act

### Counters (6)
1 Counterspell
1 Negate
1 Swan Song
1 An Offer You Can't Refuse
1 Arcane Denial
1 Drown in the Loch

### Protection & Static (4)
1 Lightning Greaves
1 Swiftfoot Boots
1 Deflecting Swat
1 Cursed Totem

### Mana Rocks & Rituals (12)
1 Sol Ring
1 Arcane Signet
1 Dimir Signet
1 Rakdos Signet
1 Izzet Signet
1 Talisman of Dominance
1 Mind Stone
1 Thought Vessel
1 Commander's Sphere
1 Ruby Medallion
1 Seething Song
1 Mana Vault

### Lands (36)
1 Command Tower
1 Exotic Orchard
1 Blood Crypt
1 Steam Vents
1 Watery Grave
1 Sulfur Falls
1 Drowned Catacomb
1 Shivan Reef
1 Underground River
1 Temple of Epiphany
1 Temple of Deceit
1 Otawara, Soaring City
1 Reliquary Tower
8 Island
8 Swamp
7 Mountain

---

## Changelog

- **2026-06-12:** Built as bake-off candidate (`forced-liquidation-20260612.txt`).
- **2026-06-23:** Displacer Kitten optimization pass (7 swaps) — cut Wheel of Fortune (+Jace's Archivist) and Memory Jar (+Displacer Kitten); removal/tutor swaps to owned copies. GC count held 3/3.
- **2026-06-25:** Bolas/Channeler combo pass — −Naktamun Lorespinner +Aether Channeler, −Prismatic Lens +Nicol Bolas, the Ravager (adds the CSB-registered backup combo + a discard-feeder). Cost-cut −Time Spiral +Molten Psyche (drops an ~€80 buy, clock-neutral). Clock re-labbed: decap T8 / table T9.
- **2026-06-27:** Cards on order; deck entered the roster as the sole new build (Thoracle/Hashaton dropped). Summary drafted.
