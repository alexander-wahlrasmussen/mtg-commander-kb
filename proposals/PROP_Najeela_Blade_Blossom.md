# Proposal: Najeela, the Blade-Blossom

Status: **not built.** Saved for future consideration.
Drafted: 2026-05-08.

Card text verified against local Scryfall data per `CLAUDE.md` hard rules. The Hashaton 2026-05-02 incident is the canonical reason proposals must verify before drafting. Every card named in the combo math below has been Scryfall-checked at draft time; re-verify at build time.

> ⚠️ **LAB CLOCK (2026-06-13).** `scripts/naj_clock_lab.py` (20k, GC-legal modelling build `decks/considering/najeela-blade-blossom-20260613.txt`) measures **median kill T10** (34% never-in-12; 12% by T6, 23% by T7, 66% by T12). The "deterministic + tutorable" framing holds — Najeela lands far more reliably than Berta because the enablers (Druids' Repository, Bear Umbra, Sword) *are* tutorable — **but it is a T10 reliability clock, not a T6–7 racer**; gated by 5-colour mana + commander dependence. **GC note:** the Bracket-4 "unlimited GC" plan violates the repo's hard 3-GC cap, and Smothering Tithe / Chrome Mox / Cyclonic Rift are GCs — the modelling build uses the legal trio Demonic Tutor / Vampiric Tutor / Mana Vault. Full writeup: `analysis/Candidate_Clock_Labs_Berta_Najeela_2026-06-13.md`.

---

## Commander

**Najeela, the Blade-Blossom** (WUBRG). `{2}{R}`, Legendary Creature — Human Warrior, 3/2.

> Whenever a Warrior attacks, you may have its controller create a 1/1 white Warrior creature token that's tapped and attacking.
>
> `{W}{U}{B}{R}{G}`: Untap all attacking creatures. They gain trample, lifelink, and haste until end of turn. After this phase, there is an additional combat phase. Activate only during combat.

**Color identity: WUBRG (5C).** Najeela's *casting cost* is `{2}{R}`, but her color identity is five-color because of her activated ability — full 5C deckbuilding access.

Owned: 1 copy. Currently undeployed.

**Engine note.** The first ability triggers off *any* Warrior attacking, including the tokens it creates — but the tokens enter "tapped and attacking," so they don't trigger declare-attackers themselves. They become eligible attackers in the *next* combat phase, where they will trigger the ability when declared. The activated ability untaps "all attacking creatures," which includes the just-created tapped tokens. So a combat phase with N attackers produces N tokens; the next combat phase declares 2N attackers, produces 2N tokens; the third declares 4N, etc. Token count doubles per cycle, while WUBRG cost is constant — the engine becomes net-positive on mana the moment any source produces WUBRG faster than 1×/cycle.

---

## Replacement context

This proposal is a **net add**, not a slot swap. The roster currently sits at 17 active decks (per `Deck_Index.md`). Najeela does not displace an existing deck — she sits alongside Berta-Mothman replacement plans as a separate consideration.

If roster slot pressure becomes an issue, the natural retirement candidates remain Radiation Sickness (already flagged in Berta proposal), The Genome Project (lowest current Elite/Solid score at 15/20), or Ms. Bumbleflower (uncertain audit baseline). Najeela does not mechanically overlap with any of those.

---

## Archetype framing

**5C Warrior tribal with infinite-combat finishers, not pure tribal aggro.** The Warrior tribal substrate is necessary — Najeela's first ability requires Warriors to trigger, and Warrior anthems / Warrior tutoring give the deck a fair-play floor. But the *win condition* is the infinite-combat loop, not turn-X tribal alpha-strike.

- **Engine = self-multiplying token attackers.** Each combat doubles attacker count. Cost is constant WUBRG per loop. With any cheap WUBRG-per-combat source, the loop is genuinely infinite.
- **5C means access to every interaction package.** Force of Will, Mana Drain, Cyclonic Rift, Toxic Deluge, Swords to Plowshares, Assassin's Trophy, Pongify — full toolbox.
- **Tutor density is the second engine.** The collection has 11/13 premium tutors. Tutoring a single combo enabler is the deck's actual game plan; the Warrior shell is the body.
- **Bracket 4-leaning.** User explicitly flagged "slightly unfair is no problem." This puts the deck in Bracket 4 territory, which lifts the 3-GC cap (per `REF_Game_Changers_List.md` line 123: "Bracket 4–5: Unlimited Game Changers").

Right archetype label: *5C Warrior tribal with infinite-combat combo finish.*

---

## Distinctiveness check

Cross-checked against `Deck_Index.md` active roster:

- **No 5C deck currently exists.** Atraxa Grand Design is closest at 4C (WUBG, no red).
- **No Warrior tribal deck.** No tribal payoff overlap with Curse of the Scarab (Zombies), Lorehold Spirits, or Eldrazi Stampede.
- **No extra-combat archetype.** Aggravated Assault and Hellkite Charger appear scattered across decks (Lightning War, Replication Crisis, Exile's Return) but as *side payoffs*, not as the central engine.
- **Closest mechanical neighbor: The Exile's Return (Zuko, Mardu).** Both are combat-centric, but Zuko's identity is exile-matters / firebending and runs Hellkite Charger as one of several attack triggers — not the same engine. Distinct.

**Verdict: distinct.** Clean addition to the roster.

---

## Power ceiling from collection

**Realistic ceiling: 18–19/20 (Elite).** Higher than Berta's 15–16 ceiling because the win line is *deterministic and tutorable*, the manabase is already built (29/34 of the 5C staples owned), and the interaction package is cEDH-grade (11/13 premium tutors, Force of Will + Mana Drain + Pact of Negation).

The ceiling is bounded by:
- **Single primary combo line** (Najeela + WUBRG-per-combat source). Multiple enablers (Druids' Repository, Bear Umbra, Sword of F&F, Aggravated Assault) provide redundancy, but they all funnel through Najeela herself. Removing the commander breaks the engine.
- **Commander dependency = high.** Najeela is `{2}{R}`, 3/2 — easy to remove, easy to counter. Each recast adds 2 to commander tax.
- **5C manabase tempo cost.** Even with the full fetch/shock/triome package, the deck enters play 1–2 turns slower than 2C decks like Berta. Mitigated by fast mana (Mana Vault, Mox Opal, Grim Monolith, Sol Ring, Chrome Mox, Lotus Petal — 6 owned).

A pure cEDH Najeela list ceilings at ~20/20. The reason this proposal caps at 19 is the missing $200+ pieces (Mana Crypt, Imperial Seal, Mox Diamond, full original-dual manabase) and the tier-down on protection density (no Mental Misstep, no Flusterstorm).

---

## Combo lines (verified math)

All combo math below uses card text Scryfall-verified at draft time.

### Line 1 — Najeela + Druids' Repository (primary)

**Druids' Repository** (verified): `Whenever a creature you control attacks, put a charge counter on this enchantment. Remove a charge counter from this enchantment: Add one mana of any color.`

Setup: Najeela + Repository + 5+ creatures.

1. Combat 1: declare 5 attackers → 5 charge counters added; 5 tokens enter tapped + attacking. Total attacking: 10.
2. Spend 5 charges (1 each → WUBRG) → activate Najeela: untap all 10 attackers; additional combat.
3. Combat 2: declare 10 attackers → 10 charge counters; 10 new tokens. Total attacking: 20. Repository now holds (10 − 5 spent last loop) + 10 = ~15 charges.
4. Each loop: charges grow by N − 5 where N is attacker count. Net positive from 6+ attackers; explodes from there.
5. Win: any opponent without a board wipe in hand dies to trample/lifelink swing in combat 2 or 3.

**Deterministic, tutorable, Bracket 4 floor.**

### Line 2 — Najeela + Bear Umbra or Sword of Feast and Famine (backup)

**Bear Umbra** (verified): `Enchanted creature gets +2/+2 and has "Whenever this creature attacks, untap all lands you control." Umbra armor.`
**Sword of Feast and Famine** (verified): `Whenever equipped creature deals combat damage to a player, that player discards a card and you untap all lands you control.`

Setup: Najeela + Umbra/Sword on Najeela or another attacker, 5+ lands tapping for WUBRG.

1. Attack with enchanted/equipped creature. Lands untap on the attack trigger (Umbra) or on damage (Sword).
2. Tap WUBRG → activate Najeela: additional combat.
3. Lands untap again on next attack. WUBRG repeats. Loop.

**Difference vs. Repository:** Sword requires combat damage to connect (blockers/protection can break); Umbra is on-attack so cleaner. Bear Umbra also has umbra armor — protects Najeela from one removal spell.

### Line 3 — Najeela + Aggravated Assault + WUBRG mana source

**Aggravated Assault** (verified): `{3}{R}{R}: Untap all creatures you control. After this main phase, there is an additional combat phase followed by an additional main phase. Activate only as a sorcery.`

This is the *backup-to-the-backup*. Aggravated Assault alone with sufficient mana goes infinite combats; Najeela amplifies via tokens. Slot AA primarily as a redundant enabler that doesn't require Najeela to function.

### Line 4 — Hellkite Charger redundancy

**Hellkite Charger** (verified): `Whenever this creature attacks, you may pay {5}{R}{R}. If you do, untap all attacking creatures and after this phase, there is an additional combat phase.`

Slow, mana-hungry, but a non-Najeela combat doubler. Worth the slot as third-deep redundancy. Requires haste (Najeela's activation gives haste; Lightning Greaves; Concordant Crossroads).

### Line 5 — Earthcraft + 5+ untapped creatures (deep redundancy)

**Earthcraft** (verified): `Tap an untapped creature you control: Untap target basic land.`

With Earthcraft + Cryptolith Rite + 5+ creatures of mixed colors, basics can produce WUBRG repeatedly. Mostly relevant if the primary Repository line is disrupted; needs basics (light count in a fetch-heavy 5C base).

---

## Owned shell that maps onto Najeela

Verified ownership against `collection/moxfield_haves_2026-05-02-2113Z.csv`. ⚠️ = currently deployed in another active deck; owning a copy doesn't necessarily mean it's free. Column to the right of each card shows "owned / deployed" — if owned > deployed, Najeela claims a free copy.

### Combo enablers (the engine)

| Card | Status | Notes |
|---|---|---|
| Aggravated Assault | 2/2 ⚠️ | Held by Lightning War, Replication Crisis. **Najeela needs one** — see contention table. |
| Hellkite Charger | 1/1 ⚠️ | Held by Exile's Return. **Sole copy.** |
| Sword of Feast and Famine | 2/2 ⚠️ | Held by Radiation Sickness, Replication Crisis. |
| Earthcraft | 1/0 free | Undeployed. |
| Mana Echoes | 1/0 free | Undeployed. Win-line accelerator (token-creature triggers add `{C}` per Warrior). |
| Reconnaissance | 1/1 ⚠️ | Held by Exile's Return. Niche but powerful — removes attackers from combat so they don't take damage. |
| Maze of Ith | 1/1 ⚠️ | Held by Calamity Tax. |
| Druids' Repository | 0 | **Must buy** (~€10). Primary combo enabler. |
| Bear Umbra | 0 | **Must buy** (~€10). |
| Cryptolith Rite | 0 | **Must buy** (~€2). |

### Fast mana

Mana Vault ⚠️ (Eldrazi Stampede), Sol Ring (26 owned), Chrome Mox (2 owned, 1 deployed — free copy), Mox Opal ⚠️ (Crystal Sickness, sole copy), Lotus Petal ⚠️ (2 owned, both deployed), Grim Monolith (1 owned, undeployed — free), Ancient Tomb ⚠️ (Eldrazi Stampede, sole copy).

### Tutors (cEDH-tier package)

Demonic Tutor (4 owned, 3 deployed — free copy), Vampiric Tutor (1 owned, undeployed — free), Mystical Tutor (1, free), Worldly Tutor (1, free), Enlightened Tutor (2, 1 deployed — free), Survival of the Fittest (1, free), Eladamri's Call ⚠️ (Grand Design, sole copy), Green Sun's Zenith ⚠️ (Calamity Tax, sole copy), Diabolic Intent (2, both deployed), Grim Tutor (1, free), Finale of Devastation (3, 2 deployed — free).

**11/13 premium tutors owned.** Missing only Imperial Seal (~€200) and Wishclaw Talisman (~€5).

### Counters / interaction

Force of Will ⚠️ (Grand Design, sole copy), Mana Drain ⚠️ (4 owned, 4 deployed — zero slack), Counterspell (multiple owned), Pact of Negation ⚠️ (Calamity Tax, sole copy), Force of Negation (6/5 — free copy), Fierce Guardianship (7/7 — zero slack), Swan Song (multiple), An Offer You Can't Refuse (multiple deployed but multiple owned), Cyclonic Rift (5/5 — zero slack), Toxic Deluge (10/10 — zero slack), Swords to Plowshares, Path to Exile, Assassin's Trophy, Pongify, Rapid Hybridization.

### 5C manabase

29/34 of the targeted manabase owned and free or surplused: full Onslaught fetch cycle, full RTR shock cycle, Prismatic Vista, Reflecting Pool, Path of Ancestry, Exotic Orchard, Spara's Headquarters, Xander's Lounge, Jetmir's Garden, Command Tower (24 copies), Sol Ring (26).

Missing manabase pieces: Mana Confluence, Forbidden Orchard, Tarnished Citadel, Raffine's Tower, Ziatora's Proving Ground.

### Najeela-specific payoffs

Smothering Tithe (3/3 ⚠️ — zero slack), Esper Sentinel (4/4 — zero slack), Rhystic Study ⚠️ (Grand Design, sole copy), Mystic Remora ⚠️ (Replication Crisis, sole copy).

---

## Cross-deck contention table — donor decisions

For each contested card Najeela needs, exactly *one* physical copy is required. The donor is the deck that loses its copy. Decisions ranked by impact:

### Singletons (no slack — one deck must yield)

| Card | Currently in | Recommended donor | Cost to host deck |
|---|---|---|---|
| **Force of Will** | Grand Design | Grand Design | Significant. Grand Design drops from 19/20 → ~17/20. Replace with Counterspell + Mana Drain redundancy. |
| **Rhystic Study** | Grand Design | Grand Design | Significant. Grand Design's draw engine. Replace with Mystic Remora (also wanted by Najeela) or Sphinx of the Second Sun. |
| **City of Brass** | Grand Design | Grand Design | Minor. Replace with Tarnished Citadel buy (~€3) or basic land. |
| **Eladamri's Call** | Grand Design | Grand Design | Minor — alternative tutors exist (Worldly Tutor + Mystical Tutor are already in Najeela). Or **skip Eladamri's Call entirely.** |
| **Pact of Negation** | Calamity Tax | Calamity Tax | Moderate. Calamity Tax has Force of Negation + Mana Drain + Fierce Guardianship — losing Pact tightens the counter package but doesn't break it. |
| **Green Sun's Zenith** | Calamity Tax | Calamity Tax | Significant for Calamity Tax. Replace with Worldly Tutor (currently undeployed — will go to Najeela; would need a buy). |
| **Maze of Ith** | Calamity Tax | Calamity Tax | Minor — replaceable with Bojuka Bog or basic. Or **skip Maze of Ith for Najeela.** |
| **Mox Opal** | Crystal Sickness | Crystal Sickness | Moderate. Crystal Sickness is artifact-heavy — Mox Opal is on-archetype there. Buying a duplicate (~€60) is a real consideration. |
| **Hellkite Charger** | Exile's Return | Exile's Return | Moderate. Exile's Return loses one of its extra-combat enablers. Backup with Combat Celebrant (free, undeployed — see below). |
| **Mystic Remora** | Replication Crisis | Replication Crisis | Moderate. Replace with Esper Sentinel duplicate or Sylvan Library. |
| **Reconnaissance** | Exile's Return | **Skip.** Maze of Ith already handles attacker protection elsewhere. Or buy a duplicate (~€10). |
| **Ancient Tomb** | Eldrazi Stampede | Eldrazi Stampede | Moderate. Stampede already at 14/20 — losing Ancient Tomb may push it to 13/20. Or buy duplicate (~€100). |

### Zero-slack multiples (every copy deployed)

| Card | Owned/Deployed | Donor decision |
|---|---|---|
| **Mana Drain** | 4/4 | Donate from **The Dark Lord's Army** (lowest impact — Sauron has Counterspell + Force of Negation + Fierce Guardianship as backup). Grand Design / Calamity Tax / Crystal Sickness keep theirs. |
| **Aggravated Assault** | 2/2 | Donate from **Lightning War** (Azula has Twinning Staff + spell-double mechanics; AA is less central). Replication Crisis keeps its copy. |
| **Sword of Feast and Famine** | 2/2 | Donate from **Radiation Sickness** (already retirement-flagged in Berta proposal). |
| **Lotus Petal** | 2/2 | Donate from **The Dark Lord's Army** (lower marginal value than in Crystal Sickness's artifact shell). |
| **Smothering Tithe** | 3/3 | **Don't take.** Najeela can run without — Esper Sentinel surplus is enough draw. Or buy duplicate (~€20). |
| **Esper Sentinel** | 4/4 | **Don't take.** Buy duplicate (~€10). |
| **Cyclonic Rift** | 5/5 | Donate from **Replication Crisis** (Satya already has Farewell-tier resets; Rift is least central there). |
| **Toxic Deluge** | 10/10 | Donate from **Eldrazi Stampede** (Stampede is the lowest-priority deck on this list and has minimal need for a 3-MV symmetrical wipe). |
| **Fierce Guardianship** | 7/7 | Donate from **Curse of the Scarab** (Scarab has Counterspell + Cyclonic Rift; FG least central). |

### Net donor summary

Decks ranked by total cards yielded to Najeela:

1. **The Grand Design** — 4 cards (Force of Will, Rhystic Study, City of Brass, Eladamri's Call). Drops 19 → ~17. **Biggest hit.**
2. **Calamity Tax** — 3 cards (Pact of Negation, GSZ, Maze of Ith). Drops 18 → ~16–17.
3. **Crystal Sickness** — 1 card (Mox Opal). Drops 17 → ~16. Or buy duplicate.
4. **The Dark Lord's Army** — 2 cards (Mana Drain, Lotus Petal). Drops 17 → ~16.
5. **The Exile's Return** — 1 card (Hellkite Charger). Drops 17 → ~16. Replace with Combat Celebrant.
6. **Replication Crisis** — 2 cards (Mystic Remora, Cyclonic Rift). Drops 17 → ~15–16.
7. **Eldrazi Stampede** — 2 cards (Ancient Tomb, Toxic Deluge). Drops 14 → ~12–13. Lowest-priority deck.
8. **Lightning War** — 1 card (Aggravated Assault). Drops 18 → ~17.
9. **Radiation Sickness** — 1 card (Sword of F&F). Already retirement-flagged.
10. **Curse of the Scarab** — 1 card (Fierce Guardianship). Drops 17 → ~16.

**Key call:** is the user willing to drop Grand Design from Elite to high-Solid? That's the central decision. Force of Will and Rhystic Study are not optional inclusions for a Bracket 4 5C deck; if they stay in Grand Design, Najeela ceiling drops to ~17/20 and Berta-tier (Solid) is the realistic outcome.

---

## Game Changers (Bracket 4 — unlimited cap)

User's stated power level (Bracket 4-leaning) lifts the 3-GC cap. Verified GC list per `REF_Game_Changers_List.md` (Feb 2026 update). Recommended GCs for Najeela:

**High-value, owned, available:**
1. **Demonic Tutor** ✓ (free copy)
2. **Vampiric Tutor** ✓ (free copy)
3. **Mystical Tutor** ✓ (free copy)
4. **Worldly Tutor** ✓ (free copy)
5. **Enlightened Tutor** ✓ (free copy)
6. **Survival of the Fittest** ✓ (free copy) — finds Najeela combo creatures
7. **Mana Vault** ⚠️ (donor: Eldrazi Stampede)
8. **Grim Monolith** ✓ (free copy)
9. **Chrome Mox** ✓ (free copy)
10. **Force of Will** ⚠️ (donor: Grand Design)
11. **Fierce Guardianship** ⚠️ (zero slack — donor: Curse of the Scarab)
12. **Cyclonic Rift** ⚠️ (donor: Replication Crisis)
13. **Smothering Tithe** ⚠️ (zero slack — buy duplicate or skip)
14. **Rhystic Study** ⚠️ (donor: Grand Design)
15. **Seedborn Muse** — surplus available (2 owned, 1 deployed in Calamity Tax). Massively powerful in Najeela: untap on each opponent's turn = WUBRG repeats off Druids' Repository charges from previous turn. Strong include.
16. **Ancient Tomb** ⚠️ (donor: Eldrazi Stampede)

**Worth buying:**
- **Imperial Seal** (~€200) — completes the tutor package. Skip unless explicitly chasing 20/20.
- **Mox Diamond** (~€700) — Bracket 4 polish only. Skip.
- **Jeska's Will** ⚠️ (Lightning War). Strong in Najeela — Najeela's color identity supports it. Donor would be Lightning War.

**Bracket 3 fallback (3-GC cap):** if the deck plays in Bracket 3 nights, recommended slots are **Force of Will, Rhystic Study, Demonic Tutor.** All three are donor-required.

---

## Buy list summary

**Required buys (combo enablers Najeela cannot run without):**
- Druids' Repository (~€10) — primary combo
- Bear Umbra (~€10) — backup combo
- Cryptolith Rite (~€2) — deep redundancy

**Strongly recommended buys:**
- Combat Celebrant (~€5) — replaces Hellkite Charger if Exile's Return keeps Charger
- Wishclaw Talisman (~€5) — adds tutor density without donor pressure
- Mana Confluence (~€80) — manabase polish
- Forbidden Orchard (~€30) — manabase polish
- Esper Sentinel duplicate (~€10) — avoids zero-slack contention
- Jeska's Will (~€20) — alt to taking from Lightning War

**Optional (Bracket 4 polish only):**
- Mana Crypt (~€200)
- Mox Diamond (~€700)
- Imperial Seal (~€200)
- Original duals (varies, ~€500–€2000 each)

**Minimum viable build cost: ~€25** (the three combo enablers). Recommended build cost: ~€100–€150 with manabase polish and conflict-avoidance duplicates. Bracket 4 polish: open-ended.

---

## Construction direction

- **Warrior count: 20–25.** Enough to make tribal anthems live and to keep the Najeela trigger consistently fed. Najeela is a Human Warrior, so tribal payoffs that key off either type work.
- **Token doublers: 1–2.** Anointed Procession (owned) doubles white tokens — Najeela's tokens are white. Doubling Season (owned, ⚠️ Earthbend the Meta) is the premium option but contested. Parallel Lives (owned, undeployed) covers green effects but Najeela's tokens are white-only — Parallel Lives **does not double Najeela's tokens** because they're not green. **Skip Parallel Lives.**
- **Mana doublers: 1.** Mana Reflection if budget allows; otherwise rely on fast mana density.
- **Protection for Najeela: 2–3.** Lightning Greaves (cheap), Swiftfoot Boots, Heroic Intervention (owned), Teferi's Protection if going 4th GC.
- **Non-Warrior creatures: keep tight.** Mana dorks (Birds of Paradise — owned, 6 copies; Bloom Tender — owned but ⚠️; Faeburrow Elder — buy), Selvala Heart of the Wilds (⚠️ Eldrazi Stampede), creature-based win redundancies. Don't run more than ~10 non-Warrior creatures or the tribal payoffs degrade.
- **Manabase: 33–34 lands.** 5C ramp is land-hungry; the full fetch/shock package is owned. Add 1–2 utility lands (Reflecting Pool — owned; Path of Ancestry — owned; Cavern of Souls if budget allows).

---

## Open questions for future build session

- **Donor decision on Grand Design.** This is the central question. Force of Will + Rhystic Study from Grand Design = Bracket 4 Najeela; keeping them in Grand Design = Bracket 3.5 Najeela ceiling ~17/20.
- **Confirm Bracket 4 vs. Bracket 3 target.** User said "slightly unfair is no problem" — that reads as Bracket 4. Confirm before locking the GC slot list, since Bracket 3 caps GCs at 3 and the deck sketch above uses 8–10.
- **Re-verify Najeela's first-ability interaction with self-created tokens.** The combo math assumes tokens created in combat 1 can be declared as attackers in combat 2 (after Najeela's untap). Confirm: tokens enter "tapped and attacking" — they do not need haste because they're never *declared* as attackers in the combat they enter; they become available in the next combat where Najeela's haste-grant covers them. Re-check at build time against current Comprehensive Rules.
- **Decide whether Eldrazi Stampede stays on the roster.** Stampede is the lowest-impact donor for Ancient Tomb + Toxic Deluge + Mana Vault. If it's already on the bubble, retiring it and absorbing its mana base into Najeela may be cleaner than incremental donations.
- **Re-verify all Game Changer slots at build time.** GC list updated twice in the last year (Oct 2025, Feb 2026). Don't lock the list without re-checking `REF_Game_Changers_List.md` at build time.
- **Sleeve-up cost.** Najeela does not retire any current deck — physical sleeves and slot are net additions. Confirm willingness to maintain an 18-deck active roster.
