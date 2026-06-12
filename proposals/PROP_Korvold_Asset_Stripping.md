# Proposal: "Asset Stripping" — Korvold, Fae-Cursed King (Jund Aristocrats Treasure-Combo)

Status: **proposal — not built.** Drafted 2026-06-12 as the FIFTH clean-sheet candidate for the
reliable-T6–7 brief (alongside `PROP_Yuriko_Insider_Trading.md`, `PROP_Godo_Hostile_Takeover.md`,
`PROP_Urza_Planned_Obsolescence.md`, `PROP_Kinnan_Quantitative_Easing.md` — user picks one).
Same constraints: beats the pod combo deck, bracket-4 in spirit, hard 3-GC cap; protected donors
Lightning War / Calamity Tax / Grand Design / Genome Project / Zero Sum Game.

All texts below verified via `card_lookup.py` 2026-06-12 (Korvold, Pitiless Plunderer, Ashnod's
Altar, Reassembling Skeleton, Mayhem Devil, Nadier's Nightblade, Zulaport Cutthroat, Gravecrawler,
Goblin Bombardment, Dockside Extortionist). GC statuses checked against `REF_Game_Changers_List.md`.

**Verification catch:** **Dockside Extortionist is BANNED in Commander** (confirmed by lookup) —
the obvious Korvold treasure enabler is illegal and is excluded from this build. Logged here so it
doesn't resurface.

---

## The pitch in one line

**The corporate raider.** Korvold dismantles his own board for profit — sacrifice an asset, draw a
card, grow. Bolt on a Treasure-recursion loop and the dismantling becomes infinite, and a single
aristocrats payoff converts it into damage that hits **all three opponents at once**. This is the
candidate the brief's lab series actually points at: the **Genome-Project kill shape** (a trigger
that drains every opponent simultaneously, so decap and table converge) rather than combat
focus-fire — and it's ~90% built from binder spares.

## Commander

**Korvold, Fae-Cursed King** — `{2}{B}{R}{G}`, 4/4 Flying Legendary Dragon Noble. **Owned, free.**

> Flying
> Whenever Korvold enters or attacks, sacrifice another permanent.
> Whenever you sacrifice a permanent, put a +1/+1 counter on Korvold and draw a card.

**Korvold is not a Game Changer** (never listed) — so, like a delisted commander, he costs **0 of
3 GC slots** while playing well above bracket 3. He is also a self-contained engine: even with no
combo assembled he draws a card every time anything is sacrificed and grows into an evasive clock.
That card-advantage motor is what digs the deck to its pieces — the deck tutors *itself*.

---

## The combo (rules-verified — infinite, on our turn, Abolisher-proof)

**Ashnod's Altar + Pitiless Plunderer + Reassembling Skeleton → infinite sacrifice / mana / draw.**

- **Ashnod's Altar:** `Sacrifice a creature: Add {C}{C}.`
- **Pitiless Plunderer:** `Whenever another creature you control dies, create a Treasure token.`
- **Reassembling Skeleton:** `{1}{B}: Return this card from your graveyard to the battlefield.`

Loop: Sac Skeleton to Ashnod's → **+{C}{C}**. Plunderer sees a creature die → **+1 Treasure**.
Korvold sees a sacrifice → **draw + counter**. Return Skeleton for `{1}{B}` — pay the `{1}` with a
`{C}` from Ashnod's, pay the `{B}` by sacrificing the Treasure. **Net +{C} every loop**, plus a
draw and a sacrifice trigger each time. (Gravecrawler — owned, recur for `{B}` with any second
Zombie out — is the even-more-mana-positive alternate engine; run both for redundancy.)

The loop is mana-positive and unbounded. Bolt on **any one** aristocrats payoff and it kills:

| Payoff | Text (verified) | Owned? |
|---|---|---|
| **Mayhem Devil** | "Whenever a player sacrifices a permanent, deals 1 damage to any target." | **free** |
| **Zulaport Cutthroat** | "Whenever this or another creature you control dies, each opponent loses 1." | buy 2nd (~€2) |
| **Nadier's Nightblade** | "Whenever a token you control leaves the battlefield, each opponent loses 1." (the Treasures) | **2 free** |
| **Goblin Bombardment** | "Sacrifice a creature: 1 damage to any target." (doubles as the sac outlet) | buy 3rd (~€10) |
| **Marionette Master** | "Whenever an artifact you control is put into a graveyard, opponent loses life = its power." (the Treasures) | **free** |

Mayhem Devil pings **any target** → spread lethal across all three opponents. Zulaport/Nadier's
drain **each opponent** simultaneously — the Genome-Project shape, decap = table. Every one of these
is a **triggered ability on our own turn**: Grand Abolisher (which only locks opponents during the
*Abolisher controller's* turn) never gets a word, exactly like Godo's combats and Urza's combo.

**Five owned-or-near-owned payoffs** = the combo is extremely hard to disrupt: kill one piece and
another finishes. This redundancy is the whole reason the user picked Korvold over the leaner
2-card piles — it trades a slightly later median kill for a combo that is very hard to interact
with and that refills itself through Korvold.

## Backup lines (no full combo needed)

- **Partial loop = win anyway.** Ashnod's + Plunderer + Skeleton *without* a payoff still makes
  infinite mana + Treasures and draws your deck → cast **Walking Ballista** (buy; the owned copy is
  in Radiation Sickness) or **Marionette Master** (free) sacking infinite Treasures to drain out.
- **Korvold standalone.** He draws a card per sacrifice and grows — a one-card card-engine and a
  flying beater. Even a disrupted game leaves you out-carding the table.

---

## Game Changer plan (3/3 — all owned, free, idle; zero GC buys)

Korvold is free, so all three slots are upside. Per the lab record this deck is **combo-assembly**
(like ZSG/Genome — a real infinite to find), not the incremental-drain pattern Diminishing Returns
labbed as "death-volume-bound," so the GCs lean **tutors over fast mana**:

| Slot | Card | Status |
|---|---|---|
| 1 | **Survival of the Fittest** | GC (Tutors). **Owned, free.** Every combo payoff and the engine creatures (Plunderer, Skeleton, Mayhem, Zulaport, Gravecrawler) are *creatures* — Survival assembles the kill by itself |
| 2 | **Gamble** | GC (Tutors). **Owned, free.** Red broad tutor for Ashnod's / any missing piece; the random-discard downside is cushioned because Korvold refills |
| 3 | **Mana Vault** | GC (Fast Mana). **Owned ×3, free.** Turbo a 5-mana commander to T3 |

- **Lab A/B for slot 3:** Mana Vault (turbo) vs. a third tutor — **Vampiric Tutor** (buy/contested
  in Rad Sickness) or **Bolas's Citadel** (buy ~€20, a low-curve aristocrats card-engine). The
  ZSG/Genome precedent says tutors edge fast mana in assembly decks, but Korvold's own draw engine
  may already cover card-finding — the lab decides whether the deck wants speed or a third tutor.
- Survival is *also* the Kinnan proposal's slot-3 pick; only one of the five candidates is built,
  so no real contention.

---

## Shell from the collection (owned-free unless noted)

- **Combo engine:** Reassembling Skeleton ×4 (free) · Gravecrawler (free spares) · **Ashnod's
  Altar — both copies in DR + protected ZSG → buy a 2nd (~€15)** · **Pitiless Plunderer — owned 1,
  in Dark Lord's Army → buy a 2nd (~€2)**
- **Payoffs:** Mayhem Devil (free) · Nadier's Nightblade (2 free) · Marionette Master (free) ·
  Zulaport Cutthroat (buy 2nd ~€2)
- **Sac outlets (free, at-will):** Korvold's own enter/attack sac; buy cheap redundancy — Viscera
  Seer (~€0.5), Carrion Feeder (~€1), Woe Strider (~€1). Ashnod's is the *mana-positive* outlet the
  loop needs; the others are insurance
- **Treasure / token fuel:** Pitiless Plunderer (core), plus cheap token-makers and sac fodder;
  **avoid Dockside (banned)**
- **Tutors / draw:** Survival (GC), Gamble (GC), Jarad's-class creature recursion, plus Korvold
  drawing the deck
- **Removal / protection:** Jund has the best removal in the game — Deadly Rollick (free counter for
  creatures), Heroic Intervention, Bedevil, Abrupt Decay; keep Korvold or the engine alive
- **Ramp / lands:** Sol Ring, Signets, ~36 Jund lands + duals; treasures double as ramp

**Buy list (prices unverified — Cardmarket at order time):** 2nd Ashnod's Altar ~€15, 2nd Pitiless
Plunderer ~€2, 2nd Zulaport ~€2, cheap sac outlets ~€3, Walking Ballista (2nd) ~€8, fodder/removal
~€10, lands ~€10 → **~€50 total.** The combo and all three GCs are already owned; the spend is
redundant copies of contested aristocrats staples so no Elite or protected deck is gutted.

---

## Roster fit — the honest asterisk

- **Distinctiveness — the closest-neighbour candidate of the five.** The roster already runs three
  sacrifice decks: Diminishing Returns (Orzhov, Teysa token-doubling drain), Genome Project (Rakdos,
  Kuja reanimator-combo) and Zero-Sum Game (Golgari, Witherbloom lifeloop). Korvold is **Jund** (no
  Jund deck exists) and its engine is distinct — *Treasure-recursion infinite + draw-on-sac*, not
  token-doubling, reanimation, or lifeloop. Defensible, and the user has explicitly accepted
  archetype overlap for this exercise — but this is the one to scrutinise against the
  mechanical-distinctiveness filter before building, and it shares a deep piece pool with DR/ZSG.
- **Donor impact:** zero pulls required — every contested piece (Ashnod's, Plunderer, Zulaport,
  Gravecrawler partly) is resolved by buying a cheap redundant copy. No protected donor touched; no
  Elite deck loses a card. The free core (Korvold, Skeletons, Mayhem, Nadier's, Marionette) carries
  most of the build.
- **Politics:** infinite-combo approval, same request as the other four candidates. Mitigations: the
  payoffs are removable creatures/enchantments, the kill is fully on-our-turn, and the deck has an
  honest "fair" face (Korvold value-grind) it can play when the combo is answered.

## Clock — *(unverified — lab gates the build)*

Structural estimate, NOT a citation: the kill *shape* is ideal (simultaneous table drain, decap =
table), but the assembly is **4 pieces** (sac outlet + Treasure-maker + recur creature + payoff) —
more than ZSG's two — cushioned by Korvold's draw engine and five redundant payoffs + two redundant
engines. Realistic target **median table kill T7–9**, with a faster tail when Survival/Gamble front-
load a piece. This is the *resilient, grindy* candidate, not the *fastest* one — the user chose it
on those terms. Per the verification rule it gets a dedicated `kvd_clock_lab.py` (on
`speed_lab_core.py`) BEFORE the decklist is finalized, modeling assembly rate, the Korvold-draw dig,
payoff redundancy, and disruption resilience. If the lab medians T9+ like Diminishing Returns did,
we say so and weigh it honestly against the faster candidates.

## Open questions for the build session

1. **Pod approval** for the infinite (any payoff line).
2. **Mechanical-distinctiveness sign-off** vs. DR / ZSG / Genome — the real gate for this one.
3. `kvd_clock_lab.py` — kill-turn distribution, assembly rate with vs. without Korvold's dig,
   payoff/engine redundancy value, GC A/B (Mana Vault vs. a third tutor).
4. **Buy-don't-pull confirmation** on Ashnod's / Pitiless Plunderer / Zulaport (all in active decks,
   two of them protected).
5. Finisher for the partial loop — Walking Ballista (2nd copy) vs. lean on Marionette Master (free).
