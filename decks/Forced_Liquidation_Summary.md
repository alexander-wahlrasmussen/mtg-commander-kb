# Forced Liquidation

**Commander:** Kefka, Court Mage // Kefka, Ruler of Ruin (Grixis / BRU)
**Archetype:** Spellslinger — forced-draw wheel-burn / punisher static
**Bracket:** 3 (3 GC; B4-in-spirit per house rules)
**Score:** 16/20 (5 / 4 / 3 / 4) · Clock: T8 decap / T9 table (spell, sorcery) (lab `kfk_clock_lab.py` 2026-06-25). Audited 2026-06-27 from the list (pre-pod; re-audit after first games).

> Build ground truth: `decks/considering/forced-liquidation-20260625.txt` (cards on order as of 2026-06-27; promote to `decks/` on arrival). Proposal: `proposals/PROP_Kefka_Court_Mage.md`. Buy list: `analysis/Buy_List_ZeroSum_LightningWar_ForcedLiquidation_2026-06-25.md`.

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

---

## Changelog

- **2026-06-12:** Built as bake-off candidate (`forced-liquidation-20260612.txt`).
- **2026-06-23:** Displacer Kitten optimization pass (7 swaps) — cut Wheel of Fortune (+Jace's Archivist) and Memory Jar (+Displacer Kitten); removal/tutor swaps to owned copies. GC count held 3/3.
- **2026-06-25:** Bolas/Channeler combo pass — −Naktamun Lorespinner +Aether Channeler, −Prismatic Lens +Nicol Bolas, the Ravager (adds the CSB-registered backup combo + a discard-feeder). Cost-cut −Time Spiral +Molten Psyche (drops an ~€80 buy, clock-neutral). Clock re-labbed: decap T8 / table T9.
- **2026-06-27:** Cards on order; deck entered the roster as the sole new build (Thoracle/Hashaton dropped). Summary drafted.
