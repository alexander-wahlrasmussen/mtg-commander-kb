# Proposal: "Quantitative Easing" — Kinnan, Bonder Prodigy (Simic Mana-Combo → Ballista Table Kill)

*(The mana-doubler prints money until the table is bankrupt. Strategic hook: it's a tuned
mirror of the pod's own Kinnan deck — see "The pitch in one line".)*

Status: **proposal — not built.** Drafted 2026-06-12 as the FOURTH clean-sheet candidate for
the reliable-T6–7 brief (alongside `PROP_Yuriko_Insider_Trading.md`,
`PROP_Godo_Hostile_Takeover.md`, `PROP_Urza_Planned_Obsolescence.md` — user picks one).
Same constraints: beats the pod combo deck, bracket-4 in spirit, hard 3-GC cap; protected
donors Lightning War / Calamity Tax / Grand Design / Genome Project / Zero Sum Game.

All texts below verified via `card_lookup.py` 2026-06-12 (Kinnan, Basalt Monolith, Walking
Ballista, Finale of Devastation). GC statuses checked against `REF_Game_Changers_List.md`
(Feb 2026, incl. the Oct-2025 Removed section).

---

## The pitch in one line

**Beat the pod's own Kinnan deck with a tuned Kinnan deck.** The recurring opponent runs
Kinnan, Bonder Prodigy as one of their five rotation decks (`pod-combo-opponent` memory).
This is the "we have watched exactly how this wins, and we built the faster version" pick —
and the political argument writes itself: *the table already lets a Kinnan combo off at this
power level.*

## Commander

**Kinnan, Bonder Prodigy** — `{G}{U}`, 2/2 Legendary Creature — Human Druid. *(buy, ~€5–10 unverified)*

> Whenever you tap a nonland permanent for mana, add one mana of any type that permanent produced.
> {5}{G}{U}: Look at the top five cards of your library. You may put a non-Human creature card
> from among them onto the battlefield. Put the rest on the bottom of your library in a random order.

**Delisted from the GC list 2025-10-21** (same purge as Yuriko/Urza/Winota/Food Chain) — a
card WotC rated GC-grade eight months ago, now **0 of 3 GC slots**. Like Yuriko and Urza, this
is bracket-4 power for a bracket-3 slot. Not owned — but at ~€5–10 he is the cheapest commander
of all four candidates, and the combo pieces behind him are already in the binder.

---

## The combo (rules-verified, two cards, one of them the commander)

**Kinnan + Basalt Monolith → infinite colorless mana.**

- Basalt Monolith: `{T}: Add {C}{C}{C}` / `{3}: Untap this artifact` / doesn't untap normally.
- Tap Basalt for `{C}{C}{C}`. Kinnan triggers — *"add one mana of any type that permanent
  produced"* → add `{C}`. Total **four** colorless. Pay `{3}` to untap Basalt. **Net +1 each
  cycle.** Repeat for unbounded colorless.
- Scryfall ruling on Basalt: *"If you believe you've found a way to generate an unbounded
  amount of mana with it, you're probably right."* Kinnan's ruling confirms it only triggers
  on `{T}`-symbol mana abilities — Basalt's `{T}: Add {C}{C}{C}` qualifies exactly.

This is effectively a **one-card-from-the-99 combo**: Kinnan starts in the command zone, so you
only need to draw or tutor **Basalt Monolith — owned ×2, deployed in zero decks, completely
free.** Same consistency profile as Godo (commander fetches/anchors the kill), but the missing
half is already paid for.

## Kill lines (all on our own turn — Abolisher-irrelevant)

The lock the pod wins behind — Grand Abolisher — only stops *opponents* from acting *during the
Abolisher controller's turn*. Every line here fires on **our** turn, off **activated abilities**,
so Abolisher never gets a word. (Same structural immunity as Godo's combats and Urza's combo.)

1. **Primary — Walking Ballista.** Infinite colorless → cast Walking Ballista for huge X (it
   enters with X +1/+1 counters; `{X}{X}` is generic so colorless pays it), then *"Remove a
   +1/+1 counter: deals 1 damage to any target"* → ping all three opponents dead. If Ballista is
   already on board, `{4}: put a +1/+1 counter` + the removal ability loops to the same end.
   **Owned ×1 — but deployed in Radiation Sickness (18/20); buy a 2nd copy (~€8) rather than gut
   an Elite deck.**
2. **Secondary — Finale of Devastation** *(owned, 1 of 4 copies free; the other 3 sit in the
   protected GD/Calamity/ZSG donors).* Infinite mana → X = lethal; at X≥10 your creatures get
   +X/+X and haste = same-turn alpha strike. Combat *can* diverge decap/table, but with infinite
   mana the swing is same-turn regardless, so it functions as a true table-kill backup.
3. **Grind insurance — Kinnan's own `{5}{G}{U}`.** With infinite mana, activate repeatedly to
   dump every non-Human creature from your library onto the battlefield. Not a clean instant-kill
   (Ballista put in this way enters as a 0/0 and dies — it must be *cast* to carry counters), but
   it deploys an overwhelming board when no finisher is in hand. The lab tunes how many dedicated
   outlets vs. how much grind the deck actually wants.

**Why this beats the pod specifically:** their decks are combo-not-counters, and a combo race at
parity favours whoever is faster + more protected. We are turbo (free fast-mana GCs land Kinnan
T1–2), and unlike Godo we are in **blue** — the combo can sit behind Veil of Summer / Fierce
Guardianship-class protection, which Godo's mono-red shell can't offer.

---

## Verified rules facts the design rests on

- **Kinnan trigger** only fires on mana abilities with `{T}` in the cost; the extra mana is
  produced *by Kinnan*, of a type the permanent produced (so Basalt → colorless). It carries no
  restrictions.
- **Basalt Monolith** untap cost `{3}` < the `{4}` Kinnan-doubled output = the +1 engine. (Grim
  Monolith does **not** combo: it also taps for 3 → 4 under Kinnan, but its untap costs `{4}` =
  net zero. Grim is fast mana here, not a combo piece.)
- **Walking Ballista** `{X}{X}` = pay twice X; enters with X counters; the ping is an activated
  ability with no mana cost (just remove a counter) — uncounterable and Abolisher-proof.

---

## Game Changer plan (3/3 — all owned, free, idle; zero GC buys)

Kinnan is free (delisted), so all three slots are pure upside — and unlike the DR/ZSG "fast mana
is flat" verdict (which applied to *cheap-assembly* combo decks), this deck's gate is genuinely
"land a 2-mana commander, then resolve one artifact." Accelerating that is exactly what fast mana
is *for* — the same argument that carried in the Godo and Urza proposals.

| Slot | Card | Status |
|---|---|---|
| 1 | **Mana Vault** | GC (Fast Mana). **Owned ×3, free.** T1 Kinnan enabler |
| 2 | **Grim Monolith** | GC (Fast Mana). **Owned, free.** Turbo; taps for 4 under Kinnan |
| 3 | **Survival of the Fittest** | GC (Tutors). **Owned, free.** Repeatable green creature tutor — finds Ballista, dorks, protection bodies, hatebears |

- **Lab A/B for slot 3:** Survival vs. **Worldly Tutor** (free — top-of-library, can fetch
  Basalt *or* Ballista to hand) vs. **Ancient Tomb** (free — more turbo). Survival is the engine
  pick; Worldly is the surgical-combo pick. The lab decides.
- Considered and passed: Mystical Tutor (free, but finds instants/sorceries — misses Basalt the
  artifact and Ballista the creature), Chrome Mox ×2 (free — bench, fine 4th-GC-NO). Vampiric
  Tutor is deployed in Radiation Sickness (contested) — buy if wanted, don't pull.

---

## Shell from the collection (owned-free unless noted)

- **Combo core:** Basalt Monolith ×2 (free) · Walking Ballista (buy 2nd, ~€8) · Finale of
  Devastation (1 free copy)
- **Mana dorks / ramp** (deploy Kinnan + double everything): **Bloom Tender** (×2 owned but BOTH
  deployed — Rad Sickness + Grand Design; buy a 3rd or substitute), Birds/Elves/Incubation Druid
  /Utopia Sprawl-class (cheap buys), **Selvala, Heart of the Wilds** (owned, free — big-mana
  legend, a secondary mana-combo axis with Umbral Mantle/Staff if the lab wants redundancy)
- **Fast mana (GC + non-GC):** Mana Vault ×3, Grim Monolith, Ancient Tomb, Chrome Mox ×2, Sol
  Ring, Arcane Signet, Simic Signet (spares)
- **Tutors / dig:** Survival of the Fittest (GC), Worldly Tutor (GC, if not slot-3), Whir of
  Invention / Fabricate / Reshape (cheap buys — find Basalt the artifact), Mystic Sanctuary
- **Protection (the blue edge over Godo):** Veil of Summer, Autumn's Veil, Heroic Intervention,
  Swiftfoot Boots ×3 (spares), counters as the lab allows — keep Kinnan alive through the combo turn
- **Redundancy combos (buys, lab decides count):** Freed from the Real / Pemmin's Aura on a
  ≥2-mana dork (Kinnan doubles → infinite), Incubation Druid + untapper
- **Lands:** ~30, Simic duals + Forests/Islands; Gaea's Cradle if acquired (green creatures)

**Buy list (prices unverified — Cardmarket at order time):** Kinnan ~€8, 2nd Walking Ballista
~€8, dork package ~€8, artifact tutors (Whir/Fabricate/Reshape) ~€7, Freed/Pemmin redundancy
~€4, protection ~€5, misc ~€5 → **~€45 total.** Ties Godo as the cheapest candidate, because the
combo engine (Basalt) and all three GCs are already owned.

---

## Roster fit

- **Distinctiveness:** the roster has no Simic deck, no mono-resource mana-combo deck, and no
  Kinnan. Closest neighbours are Eldrazi Stampede (Temur ramp/cascade) and Replication Crisis
  (Jeskai copy) — different colors, different play pattern. Clean pass.
- **Donor impact:** near zero. Combo engine (Basalt ×2) free; the only contested owned pieces are
  Walking Ballista and Bloom Tender (both 1-copy-deployed in Elite decks) — resolved by **buying**
  redundant copies, not pulling. No GC leaves any deck. No protected donor touched (Finale's free
  copy is the 4th, genuinely spare).
- **Politics:** 2-card infinite (Kinnan+Basalt) → pod approval, same request as the other three
  candidates. **Unique mitigation: it mirrors a deck already in the pod** — the strongest
  precedent argument available. Plus the kill is fully on-your-turn and the combo creature
  (Kinnan) is removable before it goes off.

## The honest weaknesses

- **Two-card reliant.** If Kinnan eats removal before Basalt resolves (or vice versa), the deck
  reverts to a ramp shell with no native haymaker — weaker fallback than Yuriko's chip clock or
  Urza's stax. Mitigation: protection density + Survival digging redundancy.
- **Finisher delivery.** Ballista must reach hand to carry counters (Kinnan's ability deploys it
  as a 0/0). The deck needs ~2–3 redundant infinite-mana outlets + tutors-to-hand so "I have
  infinite mana and nothing to spend it on" never happens. Lab sweeps outlet density.
- **Colorless mana, colored outlets.** The combo makes `{C}`; Finale and Kinnan's ability need
  `{G}`/`{G}{U}`. Trivial with one untapped dual/dork, but the list must guarantee a colored
  source is available — flag for the build.

## Clock — *(unverified — lab gates the build)*

Structural estimate, NOT a citation: turbo profile. Fast-mana GCs + a 2-mana commander + a single
owned artifact = the fastest assembly of the four candidates on its best draws. Target **median
table kill T4–6**, comparable to Godo and ahead of Yuriko/Urza — but two-card-reliant, so the
*median* may sit higher than the *ceiling*. Per the verification rule this gets a dedicated
`knn_clock_lab.py` (on `speed_lab_core.py`) BEFORE the decklist is finalized — modeling the
Kinnan-landing curve, Basalt-find rate, outlet-in-hand rate, and removal-disruption sensitivity.
If the lab says median T8+, the "turbo" premise is falsified and we say so.

## Open questions for the build session

1. **Pod approval** for the Kinnan+Basalt infinite (lead with the mirror-precedent argument).
2. `knn_clock_lab.py` — kill-turn distribution, outlet-density sweep, disruption sensitivity,
   GC A/B (Survival vs. Worldly vs. Ancient Tomb).
3. **Finisher count** — how many of Ballista / Finale / Blue Sun's Zenith / Kinnan-ability the
   deck needs so infinite mana always converts.
4. **Redundancy combos** — buy Freed from the Real / Pemmin's Aura (+ dorks) for non-Basalt lines?
5. Bloom Tender / Walking Ballista — confirm buy-don't-pull (both deployed in Elite decks).
