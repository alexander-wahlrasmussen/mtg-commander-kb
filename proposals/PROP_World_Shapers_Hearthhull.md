# Proposal: World Shapers precon (Hearthhull, the Worldseed) — owned-only upgrade

Status: **evaluation — precon not yet purchased.** Drafted 2026-07-04.

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
lines. Still not a Genome/Kefka-speed racer.

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
kill axes instead of one. **Retirement dividend:** Earthbend's off-Jund staples
return to the free pool — Smothering Tithe (GC), Esper Sentinel, Doubling Season,
Path to Exile, Swords to Plowshares, Cathars' Crusade, The Ozolith, Triumph of the
Hordes, Lightning Greaves, Swiftfoot Boots, Bootleggers' Stash — available to the
rest of the roster or a future white deck.

## Recommendation

Buy the precon if a Jund lands deck is wanted *as a deck*: the free upgrade is real
(a legal infinite, +1 turn on the table clock, dramatically better recursion, exactly
3 GCs, zero additional spend) and it produces an honest **mid-roster B3 deck**. Do
**not** buy it expecting the free pool to make it race Genome/Radiation/Replication
or the pod's T6–7 combo seat — it measurably cannot. If it is bought, next steps:
pod ruling on Planetary Annihilation (kept in the box pile only), physical build from
`world-shapers-upgraded-20260704.txt`, first-games audit, then the buy-path lab.
