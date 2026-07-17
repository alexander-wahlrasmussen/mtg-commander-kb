# Proposal: "War of Attrition" — Yahenni, Undying Partisan (mono-black aristocrats / voltron / combo, Sephiroth hidden engine)

*Status: candidate, drafted 2026-07-17. Working deck name "War of Attrition" (rename at will).*
*Two lists on file:*
- ***`decks/considering/war-of-attrition-owned-20260717.txt`*** *— **THE DELIVERABLE.** Best deck from the **free pool only** (owned − deployed; zero buys, zero cannibalising other decks). 100 cards, 1/3 GC, deck_doctor-clean.*
- *`decks/considering/war-of-attrition-20260717.txt` — aspirational build derived from the shared online list (buy-heavy). Kept for reference only.*

---

## ★ The owned/free build — recommended (zero buys, zero cannibalising)

User brief: *"the best deck we can build with my currently owned **free** cards."* So this is built from the **surplus-aware free pool** — cards owned (real + proxy) minus every copy already deployed in an active roster deck. New reusable tool for this: **`scripts/free_pool.py`** (`--colors B` to enumerate; `--check <list>` to prove a decklist is 100% free). The pool is deep — **624 free mono-black cards** — so the constraint barely bit.

**What it is:** a **Bracket-3 mono-black aristocrats / attrition / voltron** deck. Yahenni (owned, free) grows off *opponents'* creature deaths driven by a fat removal + edict package (Grave Pact, Dictate of Erebos, Fleshbag/Merciless/Accursed/Gaius edicts, Toxic Deluge, Living Death), while Blood-Artist drains chip the table and burst finishers (Kokusho ×recur, Gray Merchant, Sephiroth) close. **1 Game Changer (Tergrid).**

**Sephiroth, Fabled Soldier is owned & free** and slots in exactly as theorised — the removal-proof emblem drain + sac-draw engine. Verified: it's the *hidden engine* here too.

**Honest win-con shift vs the inspiration list:** the premium **combo core is NOT free** (Nether Traitor, Blight Mound, Genesis Chamber = unowned; Phyrexian Altar, Pitiless Plunderer = locked in other decks). `find_combos` (2026-07-17) → **0 complete infinites as built.** This is a **grind/attrition deck, not a combo deck.** BUT it is **one cheap card from a hard wincon:**
- `Nim Deathmantle + Marionette Apprentice + Ashnod's Altar` → **infinite lifeloss** (Ashnod's Altar ≈ €5, both other pieces already in the free list).
- `Carrion Feeder`/`Yahenni + Metallic Mimic` → infinite tokens/death triggers.

**Validation (2026-07-17):**
- `free_pool.py --check` → **ALL FREE** (surplus-aware; basics exempt; doesn't touch any existing deck).
- `deck_doctor` → 100 cards, singleton-clean, **all 100 legal**, own 100/100.
- **GC = 1 (Tergrid), verified against `REF_Game_Changers_List.md`.** deck_doctor *originally under-reported 0* — a DFC Game Changer listed under its full name (`Tergrid, God of Fright // Tergrid's Lantern`) evaded its matcher. **Fixed** this session: extracted `deck_doctor.match_game_changers()` (front-face + reskin aware) + 2 regression tests; fast gate green.
- **Clock (labbed):** `Clock: T6–7 decap (voltron ceiling) / T11 table (woa_clock_lab 2026-07-17)` — see below.

### Clock — `scripts/woa_clock_lab.py` (40k trials, seed 20260717)

Kill shape confirmed first (find_combos + card_lookup): grind aristocrats with a voltron axis (Yahenni **21 commander damage**, not 40) + a drain chip, and an *optional* bought combo. Three compared options:

| build | decap (one opp) | table (all three) | note |
|---|---|---|---|
| base free (no buy) | median **T6** | median **T11** | voltron+drain grind |
| + Ashnod's Altar | median **T6** | median **T11** | *no change* |

**The headline: adding Ashnod's Altar does NOT speed the deck.** The `Nim Deathmantle + Dread Drone + Ashnod's Altar` infinite is real, but it's **3 singletons with almost no tutors → assembles <3% of games by T16** (combo-availability mode). So the €5/donor piece is a *win-more*, not a clock upgrade — to make it matter you'd need combo *consistency* (tutors / a 2nd altar / Buried Alive-style setup), which is a bigger rebuild.

**Caveats (this is a ceiling, per the verification rule):** the **decap** clock is optimistic — goldfish combat is unblocked and it assumes opponents feed Yahenni ~1.5 creature-deaths/turn via our removal (the counter-accrual rate is the dominant assumption; the `sweep` mode shows decap median T6 @1.5 → T7 @1.0). **Table T11 is the more honest "win the game" number** (sequential voltron + a flat drain chip; the drain axis isn't fully modelled, so real grind may differ). No opponent interaction/removal-on-Yahenni modelled.

**Ashnod's Altar is owned but LOCKED in `zero-sum-game`** (own 1, deployed 1 → not free). The combo variant `decks/considering/war-of-attrition-owned-ashnod-20260717.txt` therefore needs a Zero-Sum pull *or* a 2nd copy (~€5, price unverified).

**Recommendation from the lab:** run the **base free build** — it's the same clock without spending or cannibalising. Only chase the combo if you're willing to add real tutor density (a separate build).

---

## Commander — Yahenni, Undying Partisan  `{2}{B}` 2/2 (verified via card_lookup)

- **Haste.**
- **Whenever a creature an _opponent_ controls dies, put a +1/+1 counter on Yahenni.**
- **Sacrifice another creature: Yahenni gains indestructible until end of turn.**

Three roles in one card: a **self-protecting voltron threat** (grows + goes indestructible), the deck's **free sac outlet**, and a **combo engine** (see combo #4 — Yahenni is literally an infinite-loop piece here, not just a beater).

**Load-bearing rules nuance:** the counter trigger is **opponents'** creatures only. Your own aristocrats fodder dying does *not* grow Yahenni — it feeds the **drain** payoffs (Zulaport, Bastion, Ayara, Sephiroth). The voltron clock is driven by your **removal package** killing *their* board. Grave Pact / Dictate of Erebos bridge the two axes: you sac your fodder → opponents are forced to sac → their creatures die → Yahenni grows *and* the drains fire.

---

## The Sephiroth "hidden commander" thesis

**Sephiroth, Fabled SOLDIER // One-Winged Angel** `{2}{B}` 3/3 — **color identity B (mono-black, fully legal under Yahenni; verified).** Owned, unallocated (FREE).

- **Front:** on ETB *or attack*, may sac a creature → draw. "Whenever another creature dies, target opponent loses 1, you gain 1." A Blood Artist on a body that is *also* a sac-draw engine.
- After that death-drain resolves **4× in one turn**, flips to a 5/5 flyer and grants an **emblem**: "Whenever a creature dies, target opponent loses 1, you gain 1."

**Why it makes sense (and where it doesn't):**
1. **Removal-proof combo payoff.** With any of the deck's infinite death loops, Sephiroth flips after 4 deaths (trivial mid-combo) and the **emblem cannot be removed** — kill Sephiroth or wipe the board mid-loop and the drain continues. Strictly more resilient than the Zulaport/Bastion/Ayara payoffs already present. CSB independently indexes Sephiroth as a combo payoff (line `4050-5544-6578`: Sephiroth + Phyrexian Altar + Forsaken Miner → infinite lifeloss).
2. **Earns its slot when you're *not* comboing** — repeatable sac-outlet + card draw.
3. **Healthy "hidden commander" footprint** (per `reference_hidden_commander_footprint`): its payoff role has analogs (Zulaport, Bastion, Ayara, Gray Merchant), so it's redundancy, not a linchpin you rebuild around.

**Honest reframing:** Sephiroth reinforces the **combo/aristocrats** axis, *not* the voltron axis — **Yahenni stays the voltron threat** (equipment + Hatred/The Black Gate for commander damage). And its drains are **single-target** ("target opponent"), unlike Zulaport/Bastion which hit *all* opponents per death; an infinite loop still kills the table (distribute triggers), but as a *fair* aristocrat it's a touch weaker than the all-opponent drains. Corroboration that it's a known fit: the K'rrik "Deficit Spending" candidate (`decks/considering/deficit-spending-20260712.txt`) already runs Sephiroth in the same mono-black-sac role.

---

## Game Changer plan — 3/3 (was 5, over the hard cap)

The online list ran **5 GCs** (verified against `REF_Game_Changers_List.md`): Ancient Tomb, Demonic Tutor, Necropotence, Orcish Bowmasters, Vampiric Tutor — **2 over the pod's hard 3-cap.**

- **Cut Ancient Tomb** — colorless + 2-life ping is awkward in a black-devotion deck (Nykthos, Crypt Ghast, Cabal Coffers, Gray Merchant) and adds to this list's already-heavy life tax.
- **Cut Vampiric Tutor** — the redundant 2nd unconditional tutor; costs 2 life in a deck that pays life everywhere (Necro, Bitterblossom, Dark Prophecy, BMC, Dreadhorde, Bastion, Hatred). Tutor density stays high (Demonic + Sidisi + Buried Alive + the new Diabolic Intent).
- **Kept:** Demonic Tutor (card-neutral dig), Necropotence (irreplaceable engine), Orcish Bowmasters (multi-role: removal + fodder + draw-hoser + Yahenni-growth).
- *Alt cut if you'd rather keep both tutors: cut Orcish Bowmasters instead of Vampiric. Close call; I favor Bowmasters for its uniqueness.*

**Refills (both owned, on-theme, non-GC):**
- **Arcane Signet** — untapped black rock; this is literally the deck's own intended Mana Crypt replacement (the primer's 2024 changelog names it, but it was absent from the pasted 99). Restores the missing slot as a mana source for the cut Ancient Tomb.
- **Diabolic Intent** — `{1}{B}` sac-a-creature tutor. Perfect in a fodder-rich deck, no life cost, replaces Vampiric's tutoring.

Note: the pasted list was **98 + commander = 99** (one slot open — the missing Arcane Signet). Net change to reach a legal 100 @ 3 GC: **+Sephiroth, +Arcane Signet, +Diabolic Intent, −Ancient Tomb, −Vampiric Tutor.**

---

## Combo / kill shape — CSB-confirmed (not primer-trusted)

`find_combos.py` (Commander Spellbook API, 2026-07-17) — **4 complete infinite combos in the list:**

1. **Pitiless Plunderer + Reassembling Skeleton + Phyrexian Altar** → infinite death/ETB/LTB/sac triggers
2. **Phyrexian Altar + Reassembling Skeleton + Blight Mound** → + infinite lifegain
3. **Nether Traitor + Phyrexian Altar + Blight Mound** → **infinite colored mana** + all of the above
4. **Blight Mound + Reassembling Skeleton + Yahenni + Pitiless Plunderer** → infinite triggers, **using the commander as the sac outlet** (no external altar)

Any of these + a drain payoff in play (Zulaport / Bastion / Ayara / **Sephiroth** / its emblem) = table kill. **Voltron kill line:** Yahenni + equipment (Commander's Plate, Sword of Feast and Famine, Sword of Sinew and Steel, Shadowspear) or **Hatred + The Black Gate** (pay life, unblockable, 21 commander damage). 83 further combos are one card away (cheap enablers: Gravecrawler, Ashnod's Altar, Pawn of Ulamog).

**Honest caveat:** every *complete* line needs pieces that are **not FREE** — Blight Mound & Nether Traitor are **buys**, Phyrexian Altar & Pitiless Plunderer are **proxy donor-pulls** (locked in Zero-Sum Game / The Dark Lords Army). So the **combo axis is aspirational until sourced**; the deck still functions as aristocrats + voltron on the owned shell.

---

## Clock — UNVERIFIED (no lab run)

No `*_clock_lab.py` exists for this deck, so **no turn-window claim is made** (per the kill-window hard rule). deck_doctor estimates **WotC bracket ~4** (an infinite combo is present); under house rules infinites are accepted (2026-06-19). A `war_of_attrition_clock_lab.py` is required before any Summary states a decap/table turn.

---

## Owned-pool sourcing (availability_check.py + deck_doctor buildability, CSV 2026-07-11)

- **Commander + hidden engine: both owned & FREE** — Yahenni ×1, Sephiroth ×1.
- **69 / 100 owned** (real + proxy; basics assumed owned).
- **31 buys ≈ €224** — prices from the **2026-06-12** bulk (stale; re-price at order time). Top: The Soul Stone €54, Hatred €27, Lifeline €22, Damnation €16, Crypt Ghast €14, Attrition €13, Gisa's Favorite Shovel €12, Witch's Clinic €12, Whip of Erebos €8, Sword of Sinew and Steel €7 … (+16). **The combo core (Nether Traitor, Blight Mound) is in this buy list.**
- **41 owned-but-deployed (donor pulls)** — would strip active decks (e.g. Phyrexian Altar ← Zero-Sum Game, Pitiless Plunderer ← Dark Lords Army, Necropotence ← Genome/Zero-Sum, Cabal Coffers ← Croak).
- **Contention flag:** Sephiroth is a **single physical copy** also wanted by the K'rrik "Deficit Spending" candidate — only one of the two can field it.

---

## Verified-facts ledger (what this rests on)

- Yahenni, Sephiroth, Arcane Signet, Diabolic Intent, Blood Artist, The Soul Stone — read via `card_lookup.py` (2026-07-17).
- GC tally cross-checked against `REF_Game_Changers_List.md`; Braids, Arisen Nightmare confirmed **≠** Braids, Cabal Minion (the GC).
- Reskin check (`REF_Reskin_Aliases.md`): none of the 31 unowned cards resolve to an owned alias.
- **Unverified (local data stale, 2026-06-12):** `Barrow-Downs` and `Weathertop` are absent from local bulk and were **not** verified — the primer describes both as mono-black utility lands (Weathertop untaps lands; Barrow-Downs a black land). Run `update_scryfall_data.py`, then re-run deck_doctor to confirm CI/legality and re-price the buy list.

---

## Open questions for the build session

1. **No-buy variant?** I can build an **owned-only** cut (drop the unowned combo core — Nether Traitor, Blight Mound — and the €54 Soul Stone, lean pure aristocrats/voltron from the FREE + donor pool). Trades the infinite-mana line for buildability today.
2. **GC cut:** keep Orcish Bowmasters (my pick) vs keep both tutors (cut Bowmasters instead)?
3. **Clock lab:** authorize a `war_of_attrition_clock_lab.py` so we can state a real decap/table window.
4. **Data refresh:** OK to run `update_scryfall_data.py` (176 MB) to close the Barrow-Downs/Weathertop gap and refresh prices?
