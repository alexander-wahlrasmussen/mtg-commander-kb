# Proposal: Creative Destruction — World Shapers precon (Hearthhull, the Worldseed)

Status: **APPROVED — named "Creative Destruction" 2026-07-05; held as a proposal until
the precon arrives.** Build target: `decks/considering/world-shapers-tuned-20260704.txt`.
Drafted 2026-07-04.

*The name:* Schumpeter's creative destruction — tearing down your own structures to
build more productive ones — which is the deck's literal game plan (sacrifice lands
for value/drain, Splendid-Reclamation them back bigger). Sits in the roster's econ
register beside Diminishing Returns / Zero-Sum Game / Forced Liquidation.

*On arrival (sleeve-day checklist):* pull the DR donor cards (The Meathook Massacre,
Prismatic Vista, Verdant Catacombs, Takenuma) and **bump Diminishing Returns' dated
`.txt`**; retire Earthbend the Meta (archive its list; off-Jund staples return to the
free pool); sleeve from the tuned list and promote it as
`decks/creative-destruction-YYYYMMDD.txt`; add the `creative-destruction` stem to
`deck_registry.EXTRA_COMMANDERS` (commander detection is stem-prefix based — the
2026-07-05 correction below is the cautionary tale); re-run DeckSafe with a fresh
Moxfield export; first-games audit.

The question asked: *if I buy the World Shapers precon (Edge of Eternities Commander,
EOC), can it be made competitive with the rest of the roster using only collection
cards not deployed in any other deck?*

**Verdict up front: partially.** A 19-swap, zero-buy upgrade (every add verified
free = owned − deployed > 0 on `moxfield_haves_2026-06-25-0748Z.csv`) gives the box a
real, pod-legal 2-card infinite and moves it to
`Clock: T10 decap / T12 table (board → spell; combo ≈ 30% of kills) (ws_clock_lab v2 2026-07-04)`.
That lands it in the **middle of the roster** — the Diminishing Returns / Curse of the
Scarab band — but **not** in the racer half (Genome T7/T8, Radiation, Replication,
Kefka T8/T9, Croak T9, Zero-Sum T9). The binding constraint is combo assembly: two
singleton pieces and only three tutors. Closing that gap requires buys (§ Buy path),
not anything the free pool has.

Every card named below was read via `card_lookup.py` / the local oracle file at draft
time (CLAUDE.md hard rule). Combos cross-checked with `find_combos.py` (CSB).
Reskin-alias check run on all unowned claims — no UB aliases apply to the upgrade;
four apply to the external list (§ External build).

**2026-07-04 addendum:** a community primer build was evaluated the same day
(§ The external primer build) and the lab model unified across all three lists —
clock lines below cite the v2 model run (upgraded table clock read T11 under v1,
T12 under v2; within model noise, the v2 numbers are the ones to quote).

---

## Commander — and a load-bearing rules finding

**Hearthhull, the Worldseed** — {1}{B}{R}{G} Legendary Artifact — Spacecraft, 6/7.
Station · **2+ |** {1}, {T}, Sacrifice a land: Draw two cards. You may play an
additional land this turn. · **8+ |** Flying, vigilance, haste — *and* "Whenever you
sacrifice a land, each opponent loses 2 life."

**The drain is station-gated.** Scryfall's oracle text is ambiguous about whether the
land-sac drain is always-on; the printed card (image pulled 2026-07-04) shows it
**inside the 8+ box**, sharing the shaded block with the keywords and the 6/7 P/T
plate. Until the ship is stationed to 8 charge (tap ≥8 power at sorcery speed), the
commander is a draw engine only.

**How much the gate actually costs (measured — `--mode drain`, 15k, 2026-07-04):**
in-goldfish the deck reaches station-8 in **86–96% of games, median T8–9** (charge
persists across turns; pre-8 the ship is a *noncreature* artifact, so it dodges
creature wipes while charging). A counterfactual always-on-from-cast drain moves the
median clock by **at most one turn** (stock table T12→T11; upgraded decap T10→T9)
and roughly doubles drain sacs/game (≈4→8). So the gate itself is cheap; the real
limitation is the **rate**: at ~1 land sac per turn the drain totals ≈10 damage per
opponent per game either way — an accelerant, not a wincon. It would only become a
kill engine with a mass land-sac outlet (Zuran Orb-class — owned only as proxies,
locked in Earthbend) feeding Splendid Reclamation rebuys. The practical takeaway is
not "the drain is dead" but that Hearthhull must not be *evaluated* as a T4 drain
commander, and the build wants spare bodies (vigilance welcome) to feed the station.

---

## The stock box (baseline, measured)

Jund lands-matter battlecruiser: land-sac value (Gitrog, Szarel, Braids, Korvold),
mass land recursion (Splendid Reclamation, Aftermath Analyst, Multani, Titania),
landfall combat payoffs (Omnath, Rampaging Baloths, Moraug). `deck_doctor`: 100 cards,
0 GCs, all legal, CI clean.

- **No combo in the box.** find_combos: only Gitrog + Dakmor Salvage (a self-mill
  engine with no payoff attached — inert).
- **Clock (stock): T9 decap / T12 table (board) (ws_clock_lab --mode stock 2026-07-04).**
  Kill mixture 99% combat. This is an *unblocked-goldfish ceiling* — the real pod
  blocks, fogs and wraths it, and the Ur-Dragon deck walls it outright.
- **House-rule flag:** the box ships **Planetary Annihilation** ("each player chooses
  six lands, sacrifices the rest" + 6 to each creature). The house rules ban mass land
  denial "symmetrical or not"; keep-6 is partial MLD and needs an explicit pod ruling.
  The upgrade cuts it regardless.

---

## The upgrade — 19 swaps, all free, 3/3 GCs

List: `decks/considering/world-shapers-upgraded-20260704.txt`
(stock reference: `decks/considering/world-shapers-precon-20260704.txt`)

**Out (17 nonland + 2 lands):** Planetary Annihilation (house rules), Sprouting
Goblin, Groundskeeper, Centaur Vinecrasher, Scouring Swarm, Eumidian Wastewaker,
Baloth Prime, Rampaging Baloths, Hammer of Purphoros, God-Eternal Bontu, Formless
Genesis, Horizon Explorer, Evendo Brushrazer, Soul of Windgrace, World Breaker, Juri,
Uurg · lands: Escape Tunnel, Wastes.

**In (19, with free margins own−deployed):**

| Role | Adds |
|---|---|
| **The combo** | Basking Broodscale (2−1) |
| Converters | Exsanguinate (2−1), Jarad, Golgari Lich Lord (2−0) — Mayhem Devil already in the box |
| Tutors/speed (**the 3 GCs**) | Natural Order (1−0), Gamble (2−1), Mana Vault (3−2) |
| Combo recursion | Victimize (5−3), Meren of Clan Nel Toth (2−0), Woe Strider (2−1, free sac outlet/igniter) |
| Lands engine | Icetill Explorer (2−1), Life from the Loam (2−0), Crucible of Worlds (2−1), Ramunap Excavator (1−0), Conduit of Worlds (2−1), Wrenn and Six (1−0) |
| Payoffs | Ob Nixilis, the Fallen (2−0), Avenger of Zendikar (2−1), Valakut Exploration (1−0) |
| Protection | Veil of Summer (3−2) |

`availability_check.py` + strict own−deployed pass: **all 19 adds FREE**; most of the
lands-engine pieces were freed by the Loam Cycle teardown and the Croak 2026-07-01
rebuild (which removed Crucible/Loam/Splendid-class cards). `deck_doctor`: 100 cards,
**GCs exactly 3/3 (Natural Order, Gamble, Mana Vault)**, banlist + CI clean.

### The kill (traced, CSB-confirmed COMPLETE: combo 317-5641)

**Mazirek, Kraul Death Priest** ("whenever a player sacrifices *another* permanent,
put a +1/+1 counter on each creature you control") + **Basking Broodscale** ("whenever
one or more +1/+1 counters are put on this creature, create a 0/1 Eldrazi Spawn with
'Sacrifice this token: Add {C}'").

- **Ignition** (first counter on Broodscale): any sacrifice while both are out — a
  fetch/sac-land crack (the deck runs ten), Hearthhull's own draw activation, Woe
  Strider's free outlet, a Harrow-class ramp spell — or its own adapt {1}{G}.
- **Loop:** sac Spawn → {C} floats + Mazirek counters everything → new Spawn.
  Infinite colorless mana, infinite sac triggers, infinite +1/+1 counters. All
  triggers and mana abilities — nothing to counter once the creatures have resolved,
  and it fires on our own turn, so **Grand Abolisher does not stop it** (the same
  structural argument that motivated the Kefka build).
- **Conversion:** Mayhem Devil (infinite pings, table), Jarad ({1}{B}{G}, sac one
  infinitely-pumped body: each opponent loses its power, table), Exsanguinate (X from
  the loop mana, table), Worldsoul's Rage (decap), or simply an arbitrarily pumped
  Spawn army next combat.
- Natural Order fetches Mazirek (green) to the battlefield; it **cannot** fetch
  Broodscale (devoid = colorless card). Gamble finds either half; Victimize rebuys
  both from the yard (the deck self-mills).

---

## Measured clocks (ws_clock_lab.py v2, 40k trials, seed 20260704)

| List | decap | table | mixture |
|---|---|---|---|
| Stock box | **T9** med (3% by T7) | **T12** med | combat 96% |
| Full upgrade | **T10** med (8% by T7, 43% by T9) | **T12** med (32% by T10) | combat 63% / combo 29% / drain+slug 7% |
| External primer build | **T9** med (4% by T7, 51% by T9) | **T11** med (35% by T10) | drain 51% / combat 33% / slug 14% |
| Upgrade, combat fully answered (`--mode comboclock`) | T14 med, 28% never-in-16 | T15 med | combo 50% of trials fire |

Decomposition (`--mode levers`, 20k): the combo package alone (no GCs) improves the
table clock T12→T11; adding the GC slice (Natural Order/Gamble/Mana Vault) buys the
front edge (decap by T7: 3%→10%; table by T10: 25%→38%). The full 19-swap list gives
back ~5 decap points at T9 versus the 9-swap core because it trades fat beaters for
engine/recursion/protection whose value a goldfish cannot see — accepted deliberately.

**Reading per the framework:** the goldfish decap (T9–10) is mostly `board` damage —
blockable, foggable, wipe-punished, and the Ur-Dragon deck walls it. The honest
competitive asset is the loop: `spell, sorcery` timing, Abolisher-immune,
counter-exposed only on the creature casts (Veil of Summer covers exactly that turn).
But as a *pure* combo deck it is slow (median T14 when combat is answered): two
singletons, three tutors, no redundancy in the Broodscale slot.

---

## Conversion Check (judged 2026-07-04, list not yet built)

**15/20 — 4 / 3 / 4 / 4 · Clock: T10 decap / T12 table (board → spell; combo ≈30%) (ws_clock_lab v2 2026-07-04)**

- **Core Loop 4** — land-sac/recursion engine, 18+ serving cards, commander-boosted
  but commander-independent.
- **Kill Reliability 3** — two genuinely independent lines (combat overrun; the
  Mazirek loop with four converter exits), but the fast line is two specific
  singletons: window narrow until tutored. Timing lens: the loop is the rare
  Abolisher-proof, wipe-the-stack-proof close.
- **Durability 4** — Meren/Victimize/Loam/Crucible/Wrenn/Faun recursion; rebuilds
  from a wipe in 2–3 turns; commander is an accelerant, not a dependency.
- **Interaction 4** — 11 pieces (Beast Within, Putrefy, Infernal Grasp, Tear Asunder,
  Rakdos Charm, Windgrace's Judgment, Gaze of Granite, Pest Infestation, Blasphemous
  Act, Binding the Old Gods, Veil of Summer), instant-heavy, mechanism-diverse
  (targeted / sweeper / GY-hate / anti-counter).

Pod fit: cannot race the measured pod combo opponent (T6–7 behind Abolisher) — true
of everything outside Genome/Radiation/Replication — but its removal suite works
*before* the Abolisher turn and its own kill works *through* one. The grind axis is
well set up for the Ur-Dragon matchup (grind wins that seat).

---

## Contention & bookkeeping notes

- **Mana Vault** (own 3): copies live in Eldrazi Stampede + Forced Liquidation; this
  takes the third. The **Urza (Planned Obsolescence) proposal also wants one** — if
  Urza ever gets built, one deck must proxy or re-tune. Flagged, not blocking.
- **Rakdos Charm**: own 0 — the Forced Liquidation list runs one that is *not owned*
  (on its buy list). The precon supplies a physical copy; if Kefka's order didn't
  include it, decide who keeps it.
- **Basking Broodscale** (own 2): one deployed in Radiation Sickness; this takes the
  free copy.
- **Earthbend the Meta** already owns the lands-matter identity at the table (Zuran
  Orb, Lotus Cobra, Amulet of Vigor etc. are locked there). No card conflict in this
  list, but the two decks overlap thematically — a roster-composition consideration,
  not a rules one.
- Precon purchase price: not verified against current market — check before buying.

## Buy path (out of scope for the question; prices unverified)

If the deck should reach the roster's top half, the lever is **combo redundancy +
tutor density**, not more fat: e.g. Scurry Oak (a second Broodscale-class counter
loop with Mazirek + Woe Strider), Eldritch Evolution / Chord of Calling (creature
tutors that find either half), Fecundity-class draw on the loop. Per the house rule:
lab the candidate swap first (`ws_clock_lab.py --deck <variant>`), buy only on a
measured delta.

## The external primer build (evaluated 2026-07-04)

List: `decks/considering/world-shapers-external-20260704.txt` — a community primer
build (~$1400 CK per its author), self-described as "B4 in spirit under a 3-GC cap":
Jund lands with a **mass-land-sacrifice** identity rather than the box's battlecruiser
one. Four alt-name printings resolve via `REF_Reskin_Aliases.md` (added 2026-07-04,
Scryfall-confirmed): Fangorn Forest = Yavimaya Cradle of Growth, La abuela siempre
generosa = Tireless Provisioner, Master Emerald Shrine = Command Tower, Newfound
Adventure = Farseek. `deck_doctor`: 100 cards, all legal, CI clean, **GCs exactly
3/3 (Crop Rotation, Field of the Dead, Glacial Chasm)** — the primer's claim holds.

**Kill shape (verified):** stationed Hearthhull turns every land sacrifice into a
2-to-each drain; landfall slug statics (Tannuk, Sabotender, Vinelasher, Retreat to
Hagra, Chocobo-doubled) chip alongside; the close is a mass sacrifice — Scapeshift
(sac all, drain 2/each per sac, refetch for a full slug wave), Zuran Orb / Squandered
Resources / Sylvan Safekeeper dumps — with Lumra as the rebuild. `find_combos`:
**32 COMPLETE combos** (Springheart + Cobra/Provisioner/Nissa, Quirion Ranger +
Ashaya, Shifting Woodland + Analyst + outlet, Chasm/Mists locks) — every flagship
line in the primer is CSB-canonical. Two primer nits: Springheart's copy cost is
{1}{G} (the primer's loops say "pay 1"/"pay 2" — loops still close, the mana math is
just looser than written), and The Earth King's "6 power to station" line needs the
2+ charge already banked, which the primer does state.

**Measured (ws_clock_lab --mode external, 40k, v2 model):**
`Clock: T9 decap / T11 table (spell-led: drain 51% / combat 33% / slug 14%) (lab 2026-07-04)`
— and this is a **floor**: the 32 infinites, earthbend lines, Urza's Saga, Windgrace
and the Chasm/Mists fog locks are all unmodelled. Against the same model the owned
upgrade reads T10 decap / T12 table at 63% *blockable* combat. The external build is
roughly a turn faster on paper and much better than a turn better in practice — its
kills are non-combat (wrath/fog/blocker-proof), its manabase is untapped duals +
11 fetches, and it holds real defensive locks. Roster placement: the Croak /
Zero-Sum band on the floor model, plausibly upper-middle piloted with the combo
lines. Still not a Genome/Kefka-speed racer. *(Measured 2026-07-04: on the synthesis
oracles it actually places Tier D, composite 11.6 — the band call above was clock-only
and ignored its thin interaction/durability. See § Tuned vs the external list.)*

**Ownership reality (strict own−deployed, CSV 2026-06-25):** of 91 nonbasics —
**24 free · 35 locked in active decks · 10 proxy-only · 22 unowned (≈ €182 + 3
unpriced; top: Squandered Resources €49 (reserved list), Scapeshift €30, Traveling
Chocobo €19)**. The locked/proxy mass is concentrated in two places: **Earthbend the
Meta holds this archetype's entire combo core** (Zuran Orb, Sylvan Safekeeper,
Ashaya, Springheart, Badgermole Cub, Amulet of Vigor, Field of the Dead, Scute
Swarm, Tannuk, Lotus Cobra, Crop Rotation, Ba Sing Se — largely as proxies), and
**Croak + the racer decks hold the fetches/shocks/duals**. Building this list as
written therefore means one of:

1. **Cannibalize Earthbend the Meta** (the natural donor — this build is close to
   "Earthbend 2.0 with a real payoff commander") + buy the €182 slice + source the
   fetch/dual overlap (proxy-normal for reserved list in this pod). Roster cost: one
   deck retires, the lands-matter seat gets strictly stronger.
2. **Buy/proxy everything, touch nothing** — the full ~67 missing-or-locked cards;
   approaches the primer's $1400 figure once real fetches/shocks/duals are included.
3. **Converge from the owned-only upgrade** — the free pool already holds a
   surprising slice of the external tech (Orcish Lumberjack, The Earth King, Toph,
   Rydia, Sabotender, Urza's Saga, Valakut Exploration, plus free real Taiga,
   Badlands, Stomping Ground, Scalding Tarn for the manabase). A v2 owned-only pass
   could adopt the slug/land-sac skeleton without touching other decks; the ceiling
   stays below the external list until Zuran/Squandered/Scapeshift-class mass
   outlets and Springheart-class loops are sourced.

**Pod notes:** the Glacial Chasm and Constant Mists recursion locks are house-legal
(not MLD, no extra turns) but are the "total degenerates" package by the primer's
own words — worth a pod heads-up. The drain kill is Abolisher-immune (our turn,
triggers); the slug statics keep working through everything short of enchantment/
creature removal.

## The merged build — precon + Earthbend retirement, zero further buys (2026-07-04)

User constraint: buy the precon (350 DKK), retire **Earthbend the Meta** into it,
buy nothing else. Earthbend is Naya (Toph, the First Metalbender — 17/20, decap T8
per `ebm_clock_lab` 2026-06-13), so only its Jund-identity slice carries over — but
that slice is exactly the archetype core: Zuran Orb, Sylvan Safekeeper, Springheart
Nantuko, Ashaya, Badgermole Cub, Ba Sing Se, Lotus Cobra, Tireless Provisioner,
Tannuk, Scute Swarm, Evolution Sage, Crop Rotation, Purphoros, **All Will Be One**
(CI red — verified), Deflecting Swat, Yavimaya, Boseiju, Lotus Field, Urza's Saga
and three real fetches.

List: `decks/considering/world-shapers-merged-20260704.txt` — every nonbasic
verified sourceable from precon ∪ free pool ∪ Earthbend (script check 2026-07-04);
`deck_doctor` all-OK; **GCs exactly 3/3: Crop Rotation, Gamble, Natural Order**
(Field of the Dead and Mana Vault deliberately left out — the latter also dissolves
the Urza-proposal contention). ~38 lands incl. free real Taiga/Badlands/Stomping
Ground/Scalding Tarn.

**Three stacked kill axes** (find_combos: 9 COMPLETE combos):
1. *Mass-sac drain* — station 8+ (Evolution Sage proliferates charge: +1 per
   landfall from 2+, reaching 8 without tapping a board) + Zuran/Safekeeper dumps,
   Tannuk/Sabotender/Ob Nixilis slug, Titania tokens.
2. *Mazirek + Basking Broodscale infinite* — converters now Mayhem Devil, Jarad,
   Exsanguinate **and All Will Be One** (every loop counter = damage).
3. *Springheart Nantuko + Lotus Cobra / Tireless Provisioner* infinites (CSB
   -canonical) with Purphoros/Impact-class ETB conversion via token waves —
   unmodelled in the lab, pure upside.

**Measured (ws_clock_lab v2.1, 40k, 2026-07-04):**
`Clock: T9 decap / T11 table (spell-led: drain 31% / combat 26% / Mazirek combo 25% / slug 7% / AWBO 6% / Purphoros 4%) — floor; Springheart lines unmodelled`
— statistically **identical to the $1400 external list** (T9/T11) with a more
diverse, less blockable kill mixture, and it keeps real interaction (Deflecting
Swat, Veil of Summer, Pyroblast-class stays in Earthbend's ex-pool if wanted).

**Cost accounting:** 350 DKK (the box) + zero card buys. What it gives up vs the
external list: Scapeshift/Squandered burst redundancy (Zuran + Crop Rotation +
Urza's Saga *fetching* Zuran cover the slot), Glacial Chasm / Constant Mists
fog-locks (social-flag cards anyway), Lumra/Traveling Chocobo/Horn of Greed value.
What it costs the roster: the Earthbend seat (17/20, decap T8) retires — accepted
by design since the two decks are the same archetype seat; the merged deck is
faster to table (T11 vs T12), spell-led rather than combat-led, and runs three
kill axes instead of one. **Retirement dividend:** Earthbend's *off-Jund* staples
return to the free pool — Smothering Tithe (GC), Esper Sentinel, Path to Exile,
Swords to Plowshares, Cathars' Crusade, Lightning Greaves, Swiftfoot Boots,
Terra Eternal-class white cards — available to the rest of the roster or a future
white deck. (Correction 2026-07-04: **Doubling Season, The Ozolith, Triumph of the
Hordes, Bootleggers' Stash, Hardened Scales are all Jund-legal green** and were
mis-listed as off-Jund — they're *candidates for the merged deck*, not dividend.
Doubling Season in particular doubles Scute/Titania tokens, the Mazirek counters,
and Hearthhull's **charge** counters (faster station-8) — a real flex slot to test.)

## Merged build — combo power & playability study (`ws_combo_lab.py`, 40k, 2026-07-04)

Every combo piece card_lookup-verified; loops cross-checked against CSB via
find_combos. `scripts/ws_combo_lab.py` reuses the canonical deck_sim engine
(simulate / simulate_flow / draw_map) — deck_sim's own `--combos`/`--flow` can't
see `decks/considering/`, which is the only reason the driver exists.

### The combos — what actually wins, and how redundant it is

find_combos reports **9 CSB-complete lines**, which collapse into **three engines +
one non-win engine**:

| Engine | Pieces (verified) | Per-iteration output | In-deck win payoff |
|---|---|---|---|
| **A. Mazirek loop** | Mazirek + Basking Broodscale | infinite {C} + infinite +1/+1 counters + infinite sac/death | All Will Be One (counter→dmg), Mayhem Devil (sac→ping), Exsanguinate, Jarad — **table** |
| **B. Springheart landfall** | Springheart + {Lotus Cobra \| Tireless Provisioner \| Nissa Resurgent} + {Ashaya \| Badgermole} | infinite landfall + tapped land tokens | Tannuk / Sabotender / Ob Nixilis (drain per landfall), Scute (bodies), Cobra mana→Exsanguinate |
| **C. Ashaya + Badgermole + outlet** | Ashaya + Badgermole + {Sylvan Safekeeper \| Zuran Orb \| Woe Strider} | infinite landfall / sac / death | same drain payoffs as B |
| D. Gitrog + Dakmor Salvage | Gitrog + Dakmor | infinite self-mill + draw + yard-fill | **none — not a standalone win** (no Thassa's Oracle); feeds Splendid Reclamation |

**The structural read:** the win engines are A, B, C. **B and C share Ashaya**, and
Badgermole enables B and is a piece of C — so *Ashaya is the linchpin*: it arms two
of the three engines at once, and removing it (or a well-timed answer on it) drops
the deck back to Mazirek + the fair Plan-A drain. The free sac outlets that engine C
uses (Zuran / Safekeeper / Woe Strider) are the **same cards the non-combo Plan-A
mass-sac drain uses** — the "every combo piece is also a good fair card" property the
primer sells is real and measurable here.

**Assembly probability** (P engine online ≤ T; drawn-only, and +tutors = Natural
Order / Green Sun's Zenith / Gamble as a *free* ceiling):

| | T6 | T8 | T10 | T12 |
|---|---|---|---|---|
| ≥1 WIN engine — drawn only | 2% | 3% | 4% | 6% |
| ≥1 WIN engine — +tutors (ceiling) | 8% | 12% | 16% | **20%** |

So even at the optimistic tutor ceiling the deck has a combo *assembled* in only
~1-in-5 games by T12 — which **confirms the primer's central claim**: this is a fair
grind/drain deck that *can* combo, not a combo deck. The combo is a reward for the
games that go long, not the plan. (Caveats: Natural Order/GSZ fetch green creatures
only — they can't get devoid Broodscale; the ceiling ignores their mana/sac cost and
Gamble's random discard. Engine D assembles far more often, ~18% +tutors by T12, but
doesn't win — it's the draw/yard-fill engine.)

### Playability — is it smooth to pilot?

The primer warns "you shuffle a lot / mana is a volatile number / needs acceleration
in the opening hand." Measured (`simulate_flow`, greedy = emptying upper bound):

| Metric | Merged | Earthbend (retiring) | Genome (smooth ref) | Croak (grind ref) |
|---|---|---|---|---|
| keepable hand | 99.4% | 98.6% | 99.2% | 99.5% |
| mean dead turns (greedy / one) | **1.48 / 1.30** | 1.26 / 1.10 | 1.37 / 1.10 | 1.81 / 1.57 |

- **It sits mid-pack — between Genome and Croak, ~0.2 dead-turns clunkier than the
  Earthbend deck it replaces.** Not a smooth deck, not a slog; a grind deck that asks
  for attention.
- **The clunk is front-loaded and real:** dead-**starved** (a spell stuck under too
  few lands — the "volatile mana" tax) is **22% on T2, 7% on T3**, then clears. Late
  dead turns are the opposite — **flooded** (11% by T10) as the hand empties
  (hellbent 51% by T8, greedy). It's a deck that can stumble early on a slow draw and
  run out of gas late if it doesn't find its card-draw engines — exactly the two
  feel-bads the primer names.
- **Hearthhull on curve:** ≥4 mana by **T3 only 14%, T4 74%, T5 83%**. The primer's
  "get the boss down T3" needs a real accelerant (Sol Ring / Orcish Lumberjack / a
  2-mana rock) in hand — T4 is the honest median. This validates its mulligan advice:
  **keep for acceleration, ship durdly land-heavy sevens.**

**Verdict on feel:** engaging and decision-dense (lots of small meaningful actions,
mana as a live resource), noticeably higher piloting load than Earthbend, and it
punishes autopilot — you will occasionally lose a game to your own clumsy sequencing
that Earthbend would have coasted through. If that trade (more skill expression, less
"untap-swing-pass") is the appeal, it's a feature; if you want some easy games, it's
the cost.

## Where it places — pod gauntlet & tier list (`ws_place.py`, 2026-07-04)

`scripts/ws_place.py` injects the merged deck's measured clock (decap T9 / table T11,
ws_clock_lab 40k) into the two synthesis oracles by reusing their own functions — the
same harvest a promoted deck would get. CC scored **17 (5/4/4/4)**, disruption bucketed
**"warn"** (conservative — see caveats). Baseline integrity confirmed: every non-swapped
deck matches canonical `tier_list.py` byte-for-byte.

**Pod gauntlet (P beat the T6-7 combo pod, decap clock, Abolisher P=0.30):**

| rank | deck | pure race | P(win) |
|---|---|---|---|
| 1 | Genome | 63% | 67% |
| … | (racers) | | |
| 14 | Dark Lord's Army | 15% | 24% |
| **15** | **World Shapers (merged)** | **8%** | **19%** |
| 16 | Diminishing Returns | 13% | 19% |
| 17 | Crystal Sickness | 7% | 9% |

**#15 of 17.** It cannot race the pod's combo — pure race 8% (needs a T≤7 decap; merged
hits T7 only 6% of the time). It sits with the other grind decks that don't race
(Diminishing, Dark Lord).

**Tier list v2 (composite: anti-pod 0.45 · interaction 0.35 · self-meta 0.20):**

Merged lands **Tier D** (composite ~20), and — the load-bearing finding — **it rates
BELOW the Earthbend deck it replaces** (Earthbend: Tier C, composite 36):

| | anti-pod | interaction | self-meta | composite | tier |
|---|---|---|---|---|---|
| Earthbend (retiring) | 42% | 12% | 12% | 36 | **C** |
| World Shapers (merged) | 18% | — (unmeasured) | **22%** | 20 | **D** |

**Read this honestly.** The composite is weighted 0.45 toward *racing the T6-7 combo
pod*, and the merged deck is a **grind/inevitability deck, not a racer** — so it scores
low on the axis that dominates the ranking, exactly like the other high-CC decks the
tier list parks in C/D (Dark Lord's Army **19/20** → C; Grand Design **18/20** → D).
By these metrics it is a **bottom-third deck**, and a **downgrade from Earthbend** on
the pod-race axis specifically.

Three things keep that from being the whole story, and all three are real:

1. **Its self-meta (mirror) score is HIGHER than Earthbend's (22 vs 12).** Racing your
   *own* roster over full games, the merged deck's inevitability wins more than
   Earthbend's go-wide — the grind signal the anti-pod axis can't see. Over long pod
   games it overperforms its tier; if the pod races out T6-7, it underperforms.
2. **Its anti-pod is conservatively bucketed.** "warn" models reactive answers dying to
   Grand Abolisher, but the merged deck's anti-combo removal is *proactive* (kill the
   piece on our own turn) and its drain kill is Abolisher-immune — so the true anti-pod
   number is somewhat higher than 18%. (Separately, the pod's *fair* Ur-Dragon build
   inverts the gauntlet — grind wins that one; the gauntlet only models his combo decks.)
3. **It has no interaction-oracle datapoint.** The 0.35 interaction axis only covers
   delay_lab-MEASURED decks; a candidate scores `—` there, which redistributes weight
   onto its weak anti-pod and drags the composite down. Promoted + delay_lab-measured,
   its 7-piece instant-removal suite would post a real interaction score and likely lift
   it into **Tier C** — i.e. roughly where Earthbend sits, not below it.
   *(Measured same-day — it doesn't: inter = 22 lifts the composite 20 → 24, still
   Tier D. See § Interaction axis — MEASURED.)*

**Net placement verdict:** by the roster's own synthesis metrics it is a lower-third,
Tier-D deck today and does not out-rank the Earthbend seat it retires. It is a *grind
deck in a race-weighted ranking*; its honest home once measured is Tier C (grindy,
durable, can't-race — the Dark Lord / Curse band), and its appeal is the mirror/long-game
axis and the Abolisher-proof kill, none of which the headline tier captures. If the goal
is to climb the roster's tier list, this swap does not do it; if the goal is a distinct,
resilient, fun-to-pilot grind seat that beats the fair-Dragon matchup, it delivers that
at 350 DKK.

## Moving it up without tutors (2026-07-04)

The tier composite is 0.45 anti-pod (decap race) · 0.35 interaction · 0.20 self-meta.
Two levers were tested; one is flat, one works.

**Lever 1 — lean into the counters → All Will Be One → single-target-decap axis
(FLAT, dropped).** AWBO deals its counter-count to *one* opponent, so feeding it
counter-generators from the retirement pool (Bristly Bill landfall counters, Doubling
Season / The Earth Crystal doubling, Impact Tremors) is the on-theme, Abolisher-proof,
tutor-free way to try to speed the decap. `ws_clock_lab --mode mergedlevers` (40k):

| variant | decap med | T7 | T8 |
|---|---|---|---|
| merged base | T9 | 6% | 23% |
| + Bristly Bill | T9 | 6% | 23% |
| + counter pkg (3) | T9 | 6% | 23% |
| + counter pkg (4, −Roiling) | **T10** | 5% | 22% |

Flat on the front edge, and the 4-card version is *slower* (cut too much mana). AWBO's
counter-damage only comes online once you're already stationed or in the Mazirek loop —
same T8+ timing as the drain it supplements. It thickens the mid-game grind but **does
not race**, so it does not move the tier. (Per the lab-first rule: measured, flat,
dropped — keep these only if wanted as grind/redundancy, not for placement.)

**Lever 2 — the interaction axis (0.35), which is *unmeasured*, not weak (THE lever).**
`ws_place.py --inter` sensitivity (injecting a manual interaction score for the merged
deck):

| injected interaction | composite | tier |
|---|---|---|
| — (unmeasured, today) | 20 | D (#14) |
| 15 | 20 | D (#14) |
| 25 | 26 | D (#13) |
| **35** | **31** | **C (#12)** |

At an interaction score ~35 it crosses into **Tier C — level with the Earthbend seat it
replaces.** The deck already has a real 7-piece instant suite; the free/retirement pool
holds plenty of premium Jund interaction to push it there without a single tutor or buy:
**Toxic Deluge, Deadly Rollick, Assassin's Trophy, Chaos Warp, Go for the Throat,
Vandalblast, Force of Vigor, Heroic Intervention** (all Jund-legal, all free or
Earthbend-proxy, **none a Game Changer** — 3/3 holds). Concrete on-brand swap: cut
low-decap value slots (Escape to the Wilds, Augur of Autumn, Tireless Tracker,
Springbloom Druid) for ~4 of those. This is exactly what a *grind* deck wants — great
answers, not a faster combo — so it fits the identity instead of fighting it.

**Lever 3 — a maxed premium manabase (a REAL, on-theme lever — corrected 2026-07-04).**
An earlier draft lumped "premium lands" in with rejected fast mana; that was wrong. For a
landfall aristocrat deck a fetch is *not* ramp — it's two landfall triggers + a sacrifice
trigger + deck-thinning + colour-fixing, and it's recurring fuel under Crucible / Ramunap /
Life from the Loam / Hearthhull. The user rejects **artifact fast mana** (Sol Ring / Mana
Vault / Ancient Tomb) and **tutors** and **racing** — not good lands. Tested (+6 real
fetches replacing basics, `ws_clock_lab`, 30k):

| | T7 | T8 | T9 | table T10 |
|---|---|---|---|---|
| merged base | 6% | 23% | 51% | 37% |
| + 6 fetches | 7% | 25% | 54% | 41% |

A couple of front-edge points, and — unlike the flat counters package — it lands on the
**anti-pod axis**: gauntlet pure race 8%→10%, P(win) 19%→20%. Modest, because the list is
*already* fetch-dense (~10 fetch-type lands), so it's diminishing returns; the bigger wins
(untapped fixing → Hearthhull on curve, fetches as recurring landfall+sac fuel) are real
but under-counted by the colour-blind goldfish. It's also simply correct deckbuilding.

**The ceiling, stated honestly:** the anti-pod (race) axis stays *low* (~18-20) — it's a
grind deck and won't race the T6-7 combo without artifact fast mana + tutors, which the
build rejects on identity. Premium lands nudge it a little; they don't turn it into a
racer. So the two working levers — **interaction** (D→C, the big one) and **manabase**
(a few anti-pod points + real consistency) — **stack to a firm low Tier C, level with the
Earthbend seat**, and that is the honest ceiling without changing what the deck *is*.
**Next step to bank it:** build the interaction-leaned, maxed-manabase variant and get it
delay_lab-measured (so the 0.35 axis is real, not injected) — offer standing.

## Interaction axis — MEASURED (2026-07-04 follow-up)

User asked what the axis is *today*, so the current merged list was put through the
canonical delay_lab engine via `ws_place.py --measure-inter` (answer spec oracle-verified
in the script; Tear Asunder costed kicked at 4, Deflecting Swat / Veil / Pest Infestation
excluded per lab rules; PROTECT prior 0.30, mirroring Zero-Sum's "Abolisher-proof kill +
Veil, no counters" rationale). Injected as `pg.MEASURED` + `pg.PROTECT` — the promoted-deck
harvest path — so both synthesis oracles read it. 20k trials, seed 20260612/12345.

**Raw availability (delay_lab, drawn, a=0):** suite = 6 instant removal + 1 preempt-only,
**0 counters, 0 statics**. Live answer on their T6 **44%** / T7 **48%** — ~4pp *below*
the Earthbend deck's measured 48/52. Under Abolisher it collapses to 2% at a=1 (the
preempt→reactive chain is thin: 3-6%), same cliff as every counters-light roster deck.

**Tier axis (interaction-overlay mirror):** **inter = 22** (post-retirement roster) /
**24** (17-deck head-to-head field) — **~2× Earthbend's 11-12** despite the slightly
lower raw availability, because the overlay rewards what the suite protects: the T11
table clock, the counter-immune close (PROTECT 0.30) and 7-answer durability lose less
to the tax than Earthbend's board kill. Composite moves **20 → 24.0 (#13 of 17)** —
**still Tier D**, ~4 points short of the C cut (28). Earthbend head-to-head: 35.1 (C).
The earlier sensitivity ladder holds up (measured 22 sits between the injected-15 and
-25 rows): reaching C needs inter ≈ 35, i.e. the **Lever-2 interaction-leaned swap**,
not just measuring the current suite.

**Anti-pod correction (caveat inverted):** with measured disruption + PROTECT replacing
the "warn" bucket, gauntlet P(win) reads **16% (#16 of 17, below Diminishing Returns
18%)**, not 19%. The § placement caveat that the bucket was "conservative" was wrong in
direction — the bucket was slightly generous (measured D at a=0.30 ≈ 0.35 vs bucket
0.39, and PROTECT doesn't offset it). Another datapoint for the framework-clock-gap
lesson: measure, don't extrapolate caveats.

**Net today:** anti-pod 18 · inter 22 (measured) · self-meta 20 → composite 24, Tier D,
one tier below the Earthbend seat it would replace. The D→C path is unchanged but now
quantified: ~4 composite points must come from the interaction-leaned build (+ fetch
manabase), and the measured baseline to beat is inter 22.

## The TUNED build — Levers 2+3 applied, measured to Tier C (2026-07-04)

User approved incorporating both levers **without touching the core plan**, and asked to
pull **all available premium lands**. List: `decks/considering/world-shapers-tuned-20260704.txt`
(12-for-12 vs the merged list; engine, combo pieces, tutors, GC trio all untouched;
`deck_doctor`: 100 cards, singleton/banlist/names clean, **GCs 3/3 unchanged** — every add
GC-grep-checked clear).

**Availability correction first (Lever 2's list was wrong).** The strict
`availability_check` pass (CSV 2026-06-25, Earthbend excluded as donor) shows the section
above's named package was **not** free: Deadly Rollick (6 copies, 7 deployed slots),
Assassin's Trophy (3/3), Chaos Warp (5/6), Go for the Throat (2/3) are fully consumed —
some with *phantom* slots (more list slots than tracked copies) — and Force of Vigor is
locked. "All free or Earthbend-proxy" was written without running the check; another
narrated-availability miss. What IS free: **Abrade (own 7, 5 free), Bitter Triumph (4
free), Murderous Rider (3 free)**, plus — per the user's 2026-07-04 carve-out that
**Diminishing Returns is a donor** (bar anything Zero-Sum-earmarked; nothing in the
Zero-Sum eval names a DR card) — **The Meathook Massacre, Prismatic Vista, Verdant
Catacombs, Takenuma** as DR pulls. Toxic Deluge exists only as a proxy-spare and was
skipped: Meathook covers the sweeper slot *on-plan* (its death-drain is a fifth Mazirek
converter — infinite Spawn deaths = table kill — and it drains on every Titania/Scute
token sac in fair games).

**The swaps** (every add card_lookup-verified, CI-legal, non-GC):

| Out | In | Note |
|---|---|---|
| Escape to the Wilds | Abrade | R/P 2 — hits Abolisher, Kinnan, dorks, artifacts |
| Augur of Autumn | Bitter Triumph | R/P 2 — any creature/PW, life not mana |
| Tireless Tracker | Murderous Rider | R/P 3 — Swift End + a 2/3 lifelink station body |
| Springbloom Druid | The Meathook Massacre | P wipe + **on-plan loop converter** (DR pull) |
| Evolving Wilds | Prismatic Vista | strict upgrade, untapped (DR pull) |
| Terramorphic Expanse | Verdant Catacombs | fetches Swamp/Forest *cards* incl. duals (DR pull) |
| Forest, Forest | Woodland Cemetery, Myriad Landscape | check land; sac-fetch-2 = ramp + sac trigger |
| Swamp, Swamp | Tainted Wood, Takenuma | cond-untapped BG; channel recursion (DR pull) |
| Mountain, Mountain | Raging Ravine, Command Beacon | manland flood-insurance; commander rebuy whose sac IS a land-sac trigger |

Basics 11 → **5** (2F/1M/2S). Stopped there deliberately: four more proxy fetch spares
exist (Bloodstained Mire ×2, Misty Rainforest, Marsh Flats, Polluted Delta via DR) but the
list already carries ~10 basic-search effects (Fabled, 3 NCC sac-lands, Vista, Myriad,
Cultivate/Harrow/Roiling/Entish) against 5 basics — the colour-blind sim cannot see the
whiffs, so going lower on judgment, not measurement. Kessig Wolf Run (Earthbend) available
but off-plan; flagged only. **Meathook flag:** Zero-Sum is its natural alternative home
(Croak holds the other copy) — reassign if preferred.

**Measured deltas (all same model/seed/trials as the base):**

- **Clock (ws_clock_lab @40k):** decap front edge −2pp (T8 23→21, T9 51→49; median label
  T9→**T10** at the 49% boundary), **table T11 holds** (T12 78→74). The draw cuts also thin
  Natural Order's sac fodder: combo share 25→22%. This is the price of the swap and it is
  real — the tier bet is that disruption buys more than the goldfish loses.
- **Flow (ws_combo_lab):** **better where it hurt** — T2 dead-starved 22→17% (the premium
  manabase), mean dead turns 1.48→1.42 (greedy); late hellbent 51→54% by T8 (the draw
  cuts). Keepable 99.3%, Hearthhull-on-curve unchanged (T4 73%).
- **delay_lab (9 R + 2 P, still 0 counters/statics):** live answer on their T6 **59%** /
  T7 **62%** (drawn, a=0) — up from 44/48, now *above* Earthbend's 48/52; preempt chain
  7→17% at T7; a=1 collapse improves only to 5-7% (no statics — that gap needs a
  Cursed Totem-class buy, unowned).
- **Placement (ws_place --tuned --measure-inter):** anti-pod **24** (gauntlet P(win)
  16→**20%**, #15 of 17, back above Diminishing Returns) · inter **23** · self **20** →
  **composite 29.5 → TIER C (#13 of 17)**, crossing the 28 cut. Head-to-head 18-deck
  field: tuned 30.3 (C, #14) vs Earthbend 35.2 (C, #12).

**Honest mechanism note:** the D→C crossing came mostly through the **anti-pod axis**
(measured disruption of the pod's combo turn), not the mirror-overlay inter axis the
sensitivity ladder pointed at (22→23 only — that oracle is dominated by clock/protect,
and the table clock softened slightly). Right destination, different door. Net: the tuned
build lands **level with the Earthbend seat as a tier (C), ~5 composite points below it**,
with the grind profile (self-meta 20-21 vs 12, Abolisher-immune close, 11-answer suite)
the composite still undercounts.

## Tuned vs the external list — placed head-to-head (2026-07-04)

User asked how the tuned build stacks up against the $1400 primer list, so the external
list got the same treatment (`ws_place --variant external --measure-inter`; clock
re-harvested @40k from the true external list; answer suite verified — only **four**
pod-relevant instants: Abrupt Decay, Assassin's Trophy, Beast Within, Tear Asunder;
Chasm/Mists/Safekeeper are protect-own and excluded per lab rules; no CC judgment exists,
weights redistribute as for Zero-Sum). Same replace-Earthbend 17-deck field:

| | **Tuned (owned, 350 DKK)** | **External (~$1400 / €182+locked as written)** |
|---|---|---|
| Clock | decap T10 / table T11 | decap **T9** / table T11 |
| Kill mixture | drain 31 / combat 28 / Mazirek ~22 / slug+AWBO+Purph 18 | drain **51** / combat 33 / slug 14 |
| delay_lab live answer T6/T7 (a=0) | **59% / 62%** (9R+2P) | 35% / 38% (4R) |
| Gauntlet P(win) | **20%** (#15) | 13% (#16) |
| Tier axes (anti · inter · self) | **24 · 23 · 20** | 13 · 12 · 12 |
| Composite → tier | **29.5 → C (#13)** | 11.6 → **D (#15)** |

**At the modelled floor, the owned tuned build beats the $1400 list by a full tier band**
— but see the asymmetry audit below before quoting that: the floor is NOT equally tight
for the two lists, and the honest verdict is a bracket, not a band. What separates them at
the floor is interaction and durability — the primer spent its budget on manabase, combo
density and value, and runs almost no answers, which is exactly what the anti-pod, inter
and self-meta axes all price. That part is not model bias: the deck really runs 4 answers.

### Asymmetry audit (2026-07-04 — user challenge: "is it apples to apples?")

It wasn't, fully. Inventory of what each clock models: the tuned clock **includes its
primary combo** (Mazirek loop + tutors ≈ 22% of kills) and omits the Springheart/Ashaya
engines, Meathook-as-converter and Takenuma/Beacon utility; the external clock omits
**all** of its combo lines. The Springheart/Ashaya engines are in *both* lists and
omitted from *both* clocks (symmetric); the net bias favours the tuned number.

**Quantified with the same instrument** (`ws_combo_lab --mode assembly`, external
taxonomy added — B/C/Quirion+Ashaya/Shifting Woodland lines, its own tutors GSZ/Nature's
Rhythm/Formidable Speaker/Crop Rotation, 40k):

| P(≥1 win engine online ≤T) | T6 | T8 | T10 | T12 |
|---|---|---|---|---|
| Tuned — drawn / +tutor ceiling | 2 / 8 | 3 / 12 | 4 / 15 | 5 / 20 |
| External — drawn / +tutor ceiling | 1 / 9 | 2 / 14 | 3 / 20 | 5 / **26** |

Drawn-only the lists are **identical**; external's free-tutor ceiling runs ~6pp ahead by
T12. So the unmodelled mass is an *option in at most a quarter of long games* (ceiling —
free tutors, no mana/discard/fodder costs), heavily overlapping games the fair plan was
already winning by T9–T11.

**Bracketing run** (`--variant externalfast`): shifting external's ENTIRE clock one turn
earlier — deliberately over-generous, it credits 100% of games with what the ceiling says
is a ≤26% option — lands it at **composite 32.0, Tier C, #12 — two points ABOVE the tuned
build (29.5, #13)**. The gauntlet is that clock-sensitive at the T8/T9 margin.

**Revised verdict, honestly stated:** external-as-modelled **11.6 (D)** · external at the
over-generous +1-turn bound **32.0 (C)** · tuned as measured **29.5 (C)**. The
proportionate combo credit sits well below the bound, so the tuned build likely still
edges it — but "beats it by a full tier band" was too strong; the defensible claim is
**rough parity at best for the external list, at ~€182 + two decks' worth of locked
staples vs zero additional spend**. Unpriced on each side after this audit: external's
Chasm/Mists locks and untapped-dual consistency (needs a `--vs-lock` overlay / colour-aware
sim); tuned's Springheart lines (≤8pp ceiling), Meathook converter, and 11-vs-4 answer
suite in real games where the pod *answers back* — none of the goldfish oracles model
opposing interaction against a 4-answer deck. The cost-adjusted recommendation is
unchanged: build the tuned list; treat the primer's mass-sac burst and fog-locks as
buy-path candidates.

## Correction 2026-07-05 — the tuned clock was harvested without its commander

`world-shapers-tuned` was missing from `deck_registry.EXTRA_COMMANDERS`, so every
2026-07-04 tuned lab run parsed with **commander None** — Hearthhull sat in the
library instead of the command zone (the parse prints `library 100 + commander None`;
none of us read that line). Registry fixed (+ a comment), clocks re-harvested @40k:
decap **[0,1,6,22,50,73,92,97]** on the [5..14] grid (T8 21→22, T9 49→50), table
**[0,1,3,7,17,35,76,93]** — ~1–2pp *faster* than the broken harvest, medians
**T10 decap / T11 table** hold. Placement re-run post-fix (`ws_place --tuned
--measure-inter`): gauntlet P(win) **21%** (#15), delay_lab live-answer T6 **59** /
T7 **63**, tier axes anti **24** · inter **24** · self **20** → **composite 30.7,
TIER C, #12 of 17** (was 29.5/#13). Every 2026-07-04 tuned conclusion survives the
fix, slightly stronger. The external-list comparison is unaffected (its stem was
registered).

## Vs the Ur-Dragon — the seat's defining matchup, now measured (2026-07-05)

The Earthbend seat exists to fight the pod's fair Ur-Dragon deck, and the standing
worry — "neither deck has flying or reach, he can simply outrun us" — was tested
directly. `ws_place.py --dragon [--variant tuned]` injects a World Shapers list into
`vs_dragon_roster_lab` (the model that ranked all 16 decks) using its **combat-off
clock**: what the deck does when plain combat is *fully answered* — a flying wall
included. (ws_clock_lab --mode comboclock @40k: merged decap T11 med, tuned T11,
~95% of games still kill by T16; mixture shifts to land-sac drain ~40% / Mazirek
combo ~18% / slug+AWBO+Purphoros ~27%.)

| | P(win vs Ur-Dragon) | axis | sweep range |
|---|---|---|---|
| **World Shapers (tuned)** | **69% — #7 of 17** | over | 59–82%, above Earthbend in ALL scenarios |
| World Shapers (merged, base) | 58% — #7 | over | 45–71% |
| Earthbend the Meta (retiring) | 33% — #13 | combat (walled) | 20–51% |

The flying/reach worry is answered by *kill shape*, not blockers: Earthbend must
connect with ground land-creatures (walled → 33%); the World Shapers kill — drain,
loop converters, slug statics — goes **over** the wall, and the tuned list's Meathook
(2nd wrath) + 9-instant suite + lifegain push it to 69%, wedged between Zero-Sum
(70%) and Crystal Sickness (57%) in the "over" cluster. **This is the axis where the
new deck decisively out-classes the seat it retires** — it more than doubles the
Earthbend matchup number the seat exists for. The pod-race tier (low C ceiling) never
was its case; the Dragon matchup is.

*Caveats:* the injected clock already excludes the walled combat share; ~11% of its
combat-off kills are pumped-Spawn swings that survive only via the tapped-attacker
crackback window — flagged, small. protect=0.0 (Veil/Swat not modelled as
counter-war) is conservative. Model fixes shipped the same day (oracle-index
poisoning + spot-regex under-catch; roster ranking unchanged — see the addendum in
`analysis/VsDragon_Roster_2026-06-15.md`).

### "Hearthhull is busted" (online) vs what we measure

Both are true, about different questions. The hype discourse evaluates the deck in
precon-upgrade / mid-power metas, where a resilient T9–T11 engine deck with an
Abolisher-immune close and a 32-combo ceiling *is* oppressive — and note our own
model scores the $1400 primer build only T9/T11 **as a floor** (its infinites are
unmodelled), statistically identical to our zero-buy lists. Our roster's bar is
different: the pod's combo seat goldfishes T6–7 behind Grand Abolisher, and
*nothing* outside Genome/Radiation/Replication races that. "Busted" online ≈
"dominates fair tables" — which is exactly the profile measured here (69% vs the
fair archenemy deck, 2× the seat it replaces; top-half self-meta), not "races a
T6–7 combo pod". The two claims never disagreed — they answer different metas.

## Tag-tool gap-fill pass (`collection_by_tag`, 2026-07-05)

The new narrowing cuts (`--color BRG --exclude-deck world-shapers-merged --max-cmc
--permanents --no-lands`) were swept over the merged list's three measured gaps (T2
mana stumble 22%, hellbent 51% by T8, 1-wrath toolkit). Shortlist → `card_lookup` →
strict `availability_check` → lab. Results, per the lab-first rule:

- **"Gas & wraths" package (7 swaps: +Greater Good/Sylvan Library/Phyrexian Arena/
  Meathook Massacre/Toxic Deluge/Birds/Phyrexian Tower) — FLAT on flow, rejected as
  a package.** List: `world-shapers-merged-gas-20260705.txt`. Flow: mean dead turns
  1.47 vs 1.48, starved-T2 22→19%, hellbent slightly *worse* (55% T8); clock ~½ turn
  slower (goldfish-dead removal slots + cut immediate gas). The deck's draw was
  already adequate — draw engines don't earn the slots the cuts vacate. (The tuned
  build had independently reached the same conclusion from the interaction side: its
  package spends those slots on answers, which the tier oracles *do* price.)
- **Birds of Paradise micro-swap (for Roiling Regrowth) — neutral, free, optional.**
  List: `world-shapers-merged-birds-20260705.txt`. Clock identical (T9/T11), flow
  marginal. Real value (colour-fixing, a T1 body that taps to station) is invisible
  to the colour-blind goldfish. "Correct deckbuilding" tier, like the fetch lever;
  compatible with the tuned list (same cut exists there — judgment call).
- **Card-text find (independently re-derived):** The Meathook Massacre's death
  trigger drains OPPONENTS when *our* creatures die — wrath + lifegain + another
  Mazirek-loop converter. The tuned build had already pulled it from Diminishing
  Returns under the user's donor carve-out; the tag sweep confirms it's the best
  wrath-slot card in the pool. Its +11pp on the vs-Dragon number (58→69 with the
  rest of the tuned interaction) is measured above.
- **Contention findings (the strict check caught what name-grep missed — alias
  printings):** Sylvan Library (2/2 deployed), Meathook (2/2 — one now allocated to
  tuned via the DR carve-out), Toxic Deluge (9 deployed vs 7 owned), Greater Good
  (1/1, Eldrazi Stampede), Phyrexian Tower (deficit), Skullclamp (5 deployed vs 4
  owned). Phyrexian Arena is genuinely free but measured flat here. **Always resolve
  availability with `availability_check.py`, never a name grep over decks/*.txt** —
  second narrated-availability miss in two days.
- **Net:** the free pool holds no measurable ramp/draw upgrade beyond what the tuned
  list already banked. The tag tool's contribution is the *process* (gap-fill
  shortlists + reading candidates before wanting them), and it closed the ramp/draw
  question with a measurement instead of a hunch.

## Extra land drops (Exploration / Azusa) & the land count (2026-07-09)

User question: would Exploration / Azusa, Lost but Seeking improve the build, and
does a landfall deck want more than the tuned list's **38 lands**?

**Method.** `ws_clock_lab` extended: `EXTRA_DROP` is now a weighted permit dict and
models **Azusa (2 extra drops, cast on curve with the engine creatures)**; Exploration
(1 drop, {G}) was already in the vocabulary. Six probe lists (built, measured 40k
seed 20260704, then deleted — swaps recorded here; probes cut clock-model-INERT
removal so the delta isolates the add): +Exploration −Abrade · +Azusa −Abrade ·
+both −Abrade/−Putrefy · 40 lands (+Forest/+Swamp −Abrade/−Putrefy) · 36 lands
(−Forest/−Swamp +2 inert stand-ins) · 40 lands+both drops.

**Clock (P kill ≤T, %; decap | table):**

| variant | T8 | T9 | T10 | table T10 | table T12 |
|---|---|---|---|---|---|
| tuned base (38 lands) | 22 | 50 | 73 | 35 | 76 |
| + Exploration | 23 | 50 | 73 | 36 | 76 |
| + Azusa | 22 | 50 | 73 | 35 | 76 |
| + both permits | 23 | 50 | 73 | 35 | 76 |
| **40 lands** | 24 | **53** | 75 | **38** | **79** |
| 36 lands | 20 | 47 | 70 | 32 | 72 |
| 40 lands + both permits | 25 | 54 | 76 | 39 | 79 |

**Extra-drop permits are FLAT** — even given best-case framing (each replaced a
goldfish-blank) and stacked on 40 lands they add ≤1pp. The arithmetic: Hearthhull's
draw-2 refills ≈0.76 lands/turn (38% land density), below what even ONE extra
drop/turn consumes — the permits idle for want of spare lands in hand; the binding
constraint is fuel, not permission. Model caveats, stated honestly: Loam is
single-shot in-model (no dredge lock), Oracle's top-of-library play and
Crucible-replay-on-spare-drops aren't modelled — the Azusa+Crucible/Loam perpetual
line is undercounted. But the same direction was measured independently by the
2026-07-05 gas-package test (draw/ramp FLAT), and neither card adds resilience
(1/2 body / dead late topdeck in a deck 51% hellbent by T8), so per the lab-first
rule they are **dropped, not bought and not pulled**. Availability anyway:
`availability_check` 2026-07-09 — **both owned ×1 and DEPLOYED in Croak & Dagger**
(donor pull, not free); Wrenn and Six is the only free card in the class and was
already evaluated out of the tuned list.

**Land count: 38 is right.** The response curve is real and monotone (36→38→40 gains
2–3pp per step on the decap/table front edge), but flow (`ws_combo_lab smoothness`,
20k) prices the other side: at 40 lands mean dead turns 1.47→**1.57** greedy, hellbent
by T10 70→**73%**, flood 13→15%, while the **T2 starve does NOT improve** (16→18%) —
the early stumble is colour/curve volatility, not count — and Hearthhull-on-curve
gains only +3pp at T4 (74→77). In a real build the two slots would also come out of
interaction, the measured D→C tier axis. Net: keep 38; the superior manabase lever
remains land QUALITY (Lever 3 fetches, already measured on the anti-pod axis), not
count, and the superior slot use remains answers (Lever 2).

`Clock: T9–10 decap / T11 table — unchanged by land-drop permits (ws_clock_lab 40k 2026-07-09)`

**Same-day sourcing correction → `world-shapers-tuned-20260709.txt` (the new build
target).** The CSV's loose Tainted Wood was a miscount — the only physical copy is
sleeved in Zero-Sum Game. User holds loose spares of Blood Crypt / Overgrown Tomb /
Bloodstained Mire (verified not Earthbend copies), so a 3-for-3 land-quality swap
replaces the probe question "more lands?" with the measured-better lever "better
lands": **out** Tainted Wood (unavailable; Swamp-conditional colours anyway),
Viridescent Bog (the list's worst land — {1},{T} filter, produces nothing alone),
Raging Ravine (ETB tapped; its manland/station-fodder body is the one real loss);
**in** Overgrown Tomb, Blood Crypt, Bloodstained Mire. Both shocks are typed
(Swamp Forest / Swamp Mountain → Nature's Lore, Skyshroud Claim, Farseek and Mire
itself can fetch them), Mire is a modelled fetch (2 landfall + sac + thinning +
Crucible/Loam fuel). Measured (40k / 20k, same seeds): decap +1pp T8, table +1pp
T10, flow unchanged — flat-to-positive, as expected for tempo/fixing the
colour-blind, tapped-blind goldfish can't price; the swap is carried on sourcing
necessity + deckbuilding correctness (the Lever-3 direction). `deck_doctor` clean:
100 cards, GC 3/3, {BGR} CI, banlist OK. Lands stay 38, basics stay 5.

**Earthbend package screened (2026-07-09, user question) — no adds.** 31 Jund-legal
earthbend cards exist (oracle sweep); 13 sit in the Earthbend teardown beyond the two
already taken (Ba Sing Se — repeatable earthbend on a LAND slot; Badgermole Cub — B/C
combo engine piece). Every candidate routes into an axis a prior measurement already
closed: station accelerants (Avatar Kyoshi 8CMC, Bumi Unleashed, Toph Greatest, Bitter
Work, Earthbending Student) are bounded by the `--mode drain` counterfactual — even
ALWAYS-ON drain buys ≤1 median turn, and the rate cap (~1 sac/turn) is the real limit;
counters-matter (Solid Ground, Bumi Eclectic, Toph Blind Bandit) = Lever-1 counter
package, measured FLAT and dropped; combat-leaning (Bumi's extra land-creature combat,
Toph Master snowball, Badgermole trample) pushes the blockable 27% axis the Ur-Dragon
walls and the tier de-weights; draw (The Legend of Kyoshi saga) = the 07-05 gas
package, measured flat-to-worse; removal (Earth Rumble sorcery fight) downgrades the
premium-instant suite that IS the tier lever. The deck already runs the right two
earthbend cards: the one that costs no spell slot and the one that wins the game.

## Recommendation

Buy the precon if a Jund lands deck is wanted *as a deck*: the free upgrade is real
(a legal infinite, +1 turn on the table clock, dramatically better recursion, exactly
3 GCs, zero additional spend) and it produces an honest **mid-roster B3 deck** that
**more than doubles the retiring seat's number in the matchup the seat exists for
(69% vs 33% against the Ur-Dragon deck — measured 2026-07-05)**. Do
**not** buy it expecting the free pool to make it race Genome/Radiation/Replication
or the pod's T6–7 combo seat — it measurably cannot. If it is bought, next steps:
pod ruling on Planetary Annihilation (kept in the box pile only), physical build from
**`world-shapers-tuned-20260709.txt`** (the measured-Tier-C Levers-2+3 build with the
2026-07-09 Tainted Wood sourcing correction; supersedes the 20260704 tuned, upgraded
and base-merged lists as the build target), first-games audit, then the buy-path lab.
