# Mass Production

## Quick Reference

| Field | Value |
|---|---|
| **Commander** | Baylen, the Haymaker ({R}{G}{W}, Legendary Creature — Rabbit Warrior) |
| **Colors** | Naya ({R}{G}{W}) |
| **Archetype** | Go-wide tokens — swarm/overrun, fully-owned zero-contention build |
| **Bracket** | 3 by GC count (2/3). No infinites in this build (the Broodscale combo lives in the archived premium draft). |
| **Game Changers** | Smothering Tithe, Survival of the Fittest (2 of 3) |
| **Conversion Check** | **15/20 (B)** · self-assessed 2026-07-11 (not yet framework-audited) |
| **Kill Window** | Clock: **T7 decap / T10 table (board)** (lab 2026-07-11, `mp_clock_lab.py`) · through interaction slower *(unverified)* |
| **Status** | **ACTIVE ROSTER — promoted 2026-07-11** (17th seat, no retirement) — ground truth `decks/mass-production-owned-20260711.txt` |

**Every card is owned and free** — zero contention with the 16 active decks (verified vs the 2026-07-11 Moxfield CSV + all deployed lists). The premium draft (Craterhoof/Purphoros/Broodscale, ~25 contended cards) is archived at `archive/old_decklists/mass-production-20260711.txt`; it measured **identical** on clock and wipe-recovery, so the owned list is the keeper.

-----

## Commander Rules Text

**Baylen, the Haymaker** — {R}{G}{W}, 4/3.
- *Tap two untapped tokens you control: Add one mana of any color.* — Mana ability (no stack, can't be responded to); tokens that entered this turn may be tapped. Every token is a mana rock the turn it lands.
- *Tap three untapped tokens: Draw a card.* — Repeatable board-fueled draw.
- *Tap four untapped tokens: Put three +1/+1 counters on Baylen. It gains trample until end of turn.* — Minor finisher; counters double under Branching Evolution / The Earth Crystal / Doubling Season.

Baylen is a **value/mana engine, not a combo linchpin** — the kills run through the 99; Baylen is an accelerant we're happy to recast.

-----

## What the Deck Does

The deck exploits **creature tokens as a fungible resource** and multiplies it. Twenty-two token producers — mass spells (Hop to It, Battle Screech, Awaken the Woods, Decree of Justice, Forth Eorlingas!, The Crystal's Chosen, Gather the White Lotus) and per-turn engines (Scute Swarm, Avenger of Zendikar, Rampaging Baloths, Felidar Retreat, God-Eternal Oketra, Hanweir Garrison, Tendershoot-class drips) — feed three token **doublers** (Doubling Season, Parallel Lives, Elspeth Storm Slayer) and the **Ojer Taq tripler**, which stack multiplicatively. Baylen converts the wide board into mana and cards; Cathars' Crusade, Rosie Cotton, Elesh Norn and the counter-doublers convert it into stats; a redundant Overrun cluster (Blossoming Bogbeast, Legion Loyalty, Jazal Goldmane, Salvation Colossus) converts it into a one-turn table swing. It is a fast, smooth, rebuildable swarm — measured, not hoped: decap T7 / table T10, 1.88 mean dead turns, +2 turns to recover from a wrath.

-----

## Kill Lines

**Line 1 — Overrun alpha (primary, board):** Go wide, then swing with a pump: **Jazal Goldmane** ({3}{W}{W}: attackers +X/+X where X = attacker count — quadratic), **Blossoming Bogbeast** (attack trigger: team trample +X/+X), **Salvation Colossus** (+2/+2 + indestructible on attack), or **Elesh Norn** (+2/+2 / opponents −2/−2, strips their token blockers). Redundant pieces, same mechanism: sorcery-speed combat, fog/wrath-answerable.

**Line 2 — Myriad table-wide (Legion Loyalty):** All creatures gain myriad — each attacker replicates at *every* opponent, so one alpha hits the whole table at once instead of focus-firing. Converges the table clock; the copies are still blockable ground tokens.

**Line 3 — ETB burn chip (Colossus of the Blood Age × Twinflame Tyrant):** Colossus ETBs for 3 to each opponent, **doubled to 6 by Twinflame Tyrant**; Twinflame also doubles all combat damage. A chip line, not a standalone kill — the only board-independent damage in the build.

*(All three lines are combat-adjacent — the build's one structural weakness. First-kill mixture from the lab: combat 99%.)*

-----

## Kill Window

- **Goldfish:** Clock **T7 decap / T10 table (board)** (lab 2026-07-11, `scripts/mp_clock_lab.py`, 20k trials; evidence `analysis/Mass_Production_Clock_Lab_2026-07-11.md`). Identical to the archived premium draft — the doubler+swarm engine drives the clock, not the premium finishers.
- **Through interaction:** slower *(unverified — goldfish has no blockers/wipes)*. Measured proxies: a T6 wrath slips the table clock to T12 (+2); vs the Ur-Dragon *blocking* board, P(win) ≈ **50%** (vs-dragon roster lab, 2026-07-11 — best of the roster's nine combat-axis decks, but well behind the drain decks' 57–99%).
- **Wipe recovery (measured):** +2 turns @ T6 wrath, +3 @ T8, +4 after a double wrath (`--mode wipe`).

-----

## Conversion Check — 15/20 (self-assessed 2026-07-11)

Scored from the list per `reference/REF_The_Conversion_Check.md`. Four judged axes; the clock is measured.

| Axis | Score | Rationale |
|---|---|---|
| **Core Loop** | **5/5** | 22 token makers + 4 doublers/tripler + 2 counter-doublers serve one machine; immediately recognizable, highly redundant. |
| **Kill Reliability** | **4/5** | Fast (decap T7 measured) with redundant, card-independent finishers — but they share ONE mechanism (combat), so the redundancy is in pieces, not axes. |
| **Durability** | **3/5** | Measured: +2/+3 turn recovery from a wrath; cheap redundant rebuilds + surviving enchantment doublers; but no protection = a timely sweeper still costs the race. |
| **Interaction** | **3/5** | 9 pieces (7 removal + 2 team protection), ~85% instant-speed, mechanism-diverse removal — but zero stack interaction and zero proactive statics (delay_lab: 48% answer T7 → 5% under Abolisher). |

**Reading:** Solid B. The limiting structure is **axis-monotony** (everything is combat) — priced at 50% vs a blocking wall and 5% disruption under Abolisher, both measured.

-----

## Durability

**Measured** (`mp_clock_lab.py --mode wipe`): a creature wrath slips the table clock **+2 turns @ T6, +3 @ T8** (T10 → T12/T13); a double wrath +4 with ~45% never-table-in-14. The token base is cheap and redundant (Hop to It, Battle Screech flashback, Awaken, Decree cycling, Rally, Group-Project-class refills), the doublers are enchantments/artifacts that **survive the wrath**, and Baylen refills cards off whatever rebuilds. God-Eternal Oketra re-buries itself; Ojer Taq returns as a land; Survival of the Fittest finds the right body. Hold **Heroic Intervention / Flawless Maneuver** against a known sweeper. Pod-overlay read (temporary 17th-seat wiring, 2026-07-11): **#5 of 17** on both `self_meta_lab` (durability 0.79, never-table 3%) and `interaction_meta_lab` (Δ only −2 under the interaction tax) — measured as durable and interaction-robust, not a glass cannon.

-----

## Interaction Package

**9 pieces total.** Removal: 7 — Swords to Plowshares, Path to Exile, Generous Gift, Beast Within, Skyclave Apparition, Zuko's Exile, Battle Menu (modal). Counters: 0 (off-color). Protection: Heroic Intervention, Flawless Maneuver (free). Instant speed: ~85%. Measured availability (delay_lab): 48% hold-an-answer on the pod's T7 — **collapsing to 5% under Grand Abolisher** (no statics, no own-turn locks).

-----

## Known Weaknesses

- **Single kill axis (combat).** 99% of first-kills are combat (lab mixture). Fogs, chump walls, and flying blockers all tax it: vs the Ur-Dragon fair board it is a **50% matchup** (best of the combat decks, but the drain decks sit 57–99%). The archived premium draft's burn/combo axes are the known fix if this ever needs to change.
- **Wipe-sensitive (measured, not fatal).** +2–3 turns per wrath; two wraths ≈ half the games never table in 14.
- **Nothing under Abolisher.** All answers are spells; a resolved Grand Abolisher on the combo player's turn blanks the whole suite (5% measured). We race instead — decap T7 is the plan.
- **Hellbent late.** Flow model: 30% hellbent by T8 (deploy-all upper bound; Baylen's tap-3 draw isn't in that model, so reality is a bit better — but the deck does dump its hand).

-----

## Don't-Miss Rulings

- **Baylen's mana ability** — a mana ability (no stack, no response window), and tokens that entered this turn can be tapped. Tapping tokens for mana/cards removes them from combat — decide before attacks.
- **Ojer Taq** triples **creature** tokens only, multiplicatively with the doublers (Doubling Season ×2 → Ojer Taq ×3 = ×6). Awaken the Woods' Dryads are creature tokens — multiplied. When it dies it returns transformed as a land and can flip back.
- **Legion Loyalty** myriad copies enter *tapped and attacking each other opponent* and are **exiled at end of combat** — they never stay, and they're still blockable; myriad spreads the alpha, it doesn't evade.
- **Blossoming Bogbeast** — X = life gained **this turn**; its own attack trigger banks 2 first, so the floor is team +2/+2 + trample every attack.
- **Elesh Norn** — only *opponents'* creatures get −2/−2; she erases their 2-toughness blockers (and opposing token swarms) while pumping ours.
- **The Crystal's Chosen / Cathars' Crusade counters** — doubled by Branching Evolution / The Earth Crystal / Doubling Season; counters put on entering creatures count as "put" for the doublers.
- **Skyclave Apparition** — exiles a nonland, *nontoken* permanent MV ≤ 4; their Illusion comes back sized to the exiled card's MV.

-----

## Decklist (100 cards)

### Commander (1)
- Baylen, the Haymaker

### Token doublers & tripler (4)
- Doubling Season
- Parallel Lives
- Elspeth, Storm Slayer
- Ojer Taq, Deepest Foundation

### +1/+1 counter doublers (2)
- Branching Evolution
- The Earth Crystal

### Token makers — engines & mass (22)
- Esika's Chariot
- Scute Swarm
- Avenger of Zendikar
- Rampaging Baloths
- Nesting Dragon
- Felidar Retreat
- God-Eternal Oketra
- Monastery Mentor
- Hanweir Garrison
- Oviya Pashiri, Sage Lifecrafter
- Suki, Kyoshi Warrior
- Angel of Invention
- Herald of the Host
- Hop to It
- Awaken the Woods
- Decree of Justice
- Battle Screech
- Forth Eorlingas!
- The Crystal's Chosen
- Rally at the Hornburg
- Gather the White Lotus
- Scurry of Gremlins

### Payoffs — anthems & pingers (6)
- Cathars' Crusade
- Intangible Virtue
- Rosie Cotton of South Lane
- Twinflame Tyrant
- Elesh Norn, Grand Cenobite
- Colossus of the Blood Age

### Finishers — overrun & myriad (4)
- Blossoming Bogbeast
- Legion Loyalty
- Salvation Colossus
- Jazal Goldmane

### Card draw (4)
- Guardian Project
- Welcoming Vampire
- Tempt with Bunnies
- Harmonize

### Removal & protection (9)
- Swords to Plowshares
- Path to Exile
- Generous Gift
- Beast Within
- Skyclave Apparition
- Zuko's Exile
- Battle Menu
- Heroic Intervention
- Flawless Maneuver

### Ramp (11)
- Sol Ring
- Arcane Signet
- Fellwar Stone
- Birds of Paradise
- Elvish Mystic
- Cultivate
- Kodama's Reach
- Nature's Lore
- Three Visits
- Farseek
- Rampant Growth

### Game Changers (2)
- Smothering Tithe  *(GC)*
- Survival of the Fittest  *(GC)*

### Lands (35)
- Command Tower
- Jetmir's Garden
- Path of Ancestry
- Exotic Orchard
- Temple Garden
- Sacred Foundry
- Stomping Ground
- Wooded Foothills
- Windswept Heath
- Arid Mesa
- Clifftop Retreat
- Cinder Glade
- Canopy Vista
- Rugged Prairie
- Sunbaked Canyon
- Castle Ardenvale
- War Room
- Sheltered Thicket
- Kyoshi Village
- Forest x6
- Plains x5
- Mountain x5

-----

## Piloting Notes (for borrowers)

- **Mulligans are easy** — 99.2% keepable (deck_sim); keep land + an early token maker; a hand of only payoffs does nothing.
- **Smoothness is real:** 1.88 mean dead turns T1–10 (between Lorehold 1.49 and Eldrazi 3.28); 96% have a play by T3. The deck plays itself early — the skill is the mid-game.
- **Sequence doubler → mass-maker in the same turn**; a doubler after the tokens does nothing for that batch.
- **Baylen tap-for-value vs attack** is the recurring decision — tapped tokens don't swing. Go wide enough to do both; use Baylen's draw to find the Overrun piece rather than over-extending.
- **Against wraths:** measured cost is +2–3 turns; hold Heroic Intervention/Flawless Maneuver once you're presenting lethal, and prefer rebuilding through the surviving doublers over dumping a second full hand.
- **Against fliers/walls (Ur-Dragon-class):** you're the best-positioned combat deck (~50%) but still walled — Elesh Norn shrinks their tokens (not dragons), Jazal makes blocks bad, Legion Loyalty spreads damage so chump-blocking one attacker doesn't save the table. Race early before the wall assembles; don't grind into it.

-----

## Changelog

- **2026-07-11:** Initial build from the Naya token pool (premium draft: Craterhoof/Purphoros/Broodscale). `find_combos.py` flagged the Broodscale+Rosie / +Cathars' infinites; Broodscale added.
- **2026-07-11:** Built `scripts/mp_clock_lab.py` (20k) → **T7 decap / T10 table (board)**. Finding: the combo was resilience-flavored, not speed (identical clock disabled).
- **2026-07-11:** Built the fully-owned zero-contention variant; labbed **identical** (T7/T10). Wipe-recovery measured **equal** (+2/+3/+4 slip both lists) — premium's burn/combo axes bought no durability (Broodscale dies to the wrath). Pod overlays (temporary 17th-seat wiring): **#5/17 on self_meta AND interaction_meta**.
- **2026-07-11:** Walking Ballista lever test **FLAT** (clock/wipe unchanged, ping 1%, no new combos) — dropped; Battle Menu keeps the slot.
- **2026-07-11:** **Owned list promoted to keeper.** Premium draft archived (`archive/old_decklists/mass-production-20260711.txt`); lab repointed; `mass-production` added to `EXTRA_COMMANDERS`. New measurements: **vs Ur-Dragon blocking board 50%** (best of 9 combat-axis decks; sweep-stable 34–67%); **flow 1.88 mean dead turns, 99.2% keepable** (deck_sim --flow). Summary rewritten to the owned list as ground truth.
- **2026-07-11:** **PROMOTED to the active roster** (17th seat, no retirement) per `WF_New_Deck` Stages 3–7: registry `DECKS` row + `KILL_TREES`; pod_gauntlet CLOCKS + PROTECT 0.15; delay_lab suite (48% T7 → 5% under Abolisher); framework_bakeoff oracles (pod 57 / self-meta 31 / interaction 29); clock_check + golden snapshot; keep_specs. Harvested: **pod gauntlet P(win) 57% — #4/17**; **vs Ur-Dragon 51%** (@40k, PROTECT credited).
