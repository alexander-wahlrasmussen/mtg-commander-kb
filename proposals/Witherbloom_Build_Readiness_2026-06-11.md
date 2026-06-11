# Witherbloom v2b — Build Readiness Pass (2026-06-11)

Context: after the kill-turn lab sweep (7 of 8 windows falsified, all optimistic), the user asked
whether a **new** deck is the realistic route to a T6–7 win — specifically to beat the pod combo
opponent (Ur-Dragon + Hidetsugu/Kairi/Kenrith/Kinnan, T6–7 behind Grand Abolisher).

**Constraint set for this pass:** build primarily from the collection; decks are fair donors
EXCEPT Lightning War, Calamity Tax (post 2026-05-31 swap), Grand Design (post swap), Genome
Project. New buys allowed when strategy-critical. Loam Cycle is dismantled (free donor, excluded
from deployment counts).

Tool: `scripts/availability_check.py` (new, reusable) — candidate list vs Moxfield CSV
(`moxfield_haves_2026-06-07-1031Z.csv`) + all `decks/*.txt`, with protected-deck locking and
reserve list for the pending Calamity Tax adds (Exsanguinate, Sheoldred, Mystic Remora,
Bloom Tender, Carpet of Flowers). Reskin-alias check completed: no aliases among unowned cards.

---

## Verdict

**Build Witherbloom, the Balancer (v2b list, `witherbloom-balancer-v2b-20260607.txt`) as the new
deck.** It survives the donor restrictions almost untouched: of 96 unique cards, 44 are owned and
free or pullable from non-protected decks, the commander + both new combo redundancy pieces
(Bloodthirsty Conqueror, Jet Medallion, Professor Dellian Fel) are owned and undeployed, and the
12 cards locked in protected decks are almost all lands/utility with cheap substitutes. None of
the five cards reserved for the Calamity Tax post-swap state are in the v2b list.

**Clock: T6–8 decap = table** (combo kill is table-wide infinite drain, clocks converge).
Mana-aware deployment model 2026-06-07 (40k trials, in `PROP_Witherbloom_the_Balancer.md`
§Consistency scale-up): deployable kill **33% T6 / 46% T7 / 56% T8 / 70% T10**; median ≈ T7–8,
T6 is the ~1-in-3 nut. *A dedicated `wb_clock_lab.py` run on the harness is required before the
Summary states a window* — the deployment model is a simulation citation, but not yet a
speed-lab-harness run.

**Honesty vs the brief:** this is not a guaranteed T6 kill — nothing at 3 GCs is. It is the only
roster deck or candidate whose *median* contests the pod's T6–7 window, and the kill is
commander-independent, resolves on our own turn (Abolisher-proof in the same way Kefka's is), and
instantaneous once deployed (no combat telegraph). Against the pod specifically: ~33–46% of games
we are level or ahead on raw goldfish; Veil of Summer / Deadly Rollick / removal push their
window back in the rest.

Why not the other shelf candidates:
- **Kefka** — right anti-Abolisher mechanics but ceiling ~17/20 and wheel-kill needs 2–3 punishers
  down first; slower median than Blood+Vito.
- **Najeela** — Grand Design was the central donor; GD is now protected. Dead under current rules.
- **Wandering Minstrel / Berta** — value engines, no sub-T8 kill median; Berta also leans on
  contested Survival/Mana Vault.

---

## Availability summary (96 unique cards)

| Status | Count | Meaning |
|---|---|---|
| Owned, free | 13 | undeployed, incl. commander, Bloodthirsty Conqueror, Bitterblossom, Jet Medallion, Dellian Fel |
| Donor pull | 31 | owned copies in non-protected decks (or spares) |
| Locked in protected decks | 12 | every owned copy sits in LW/CT/GD/GP — substitute or buy |
| Proxy-only in collection | 10 | physical 0; print new proxy or buy |
| Unowned | 30 | buy or proxy; no reskin aliases |

### Locked cards → resolutions

| Card | Resolution |
|---|---|
| Bayou, Cabal Coffers, Urborg | **Cut** — Coffers/Urborg package dies with both halves locked in Calamity/Genome; replace with basics. Affinity is the deck's big-mana engine anyway. |
| Boseiju, Who Endures; Yavimaya; Undergrowth Stadium | Sub basics (nice-to-haves). |
| Wooded Foothills | Sub basic — all other BG-capable fetches already in list with spare copies. |
| Bojuka Bog; Night's Whisper | Cheap buys (~€1–2 each, unverified). |
| Black Market Connections; Deadly Rollick; Heroic Intervention | Physical-vs-proxy location ambiguous across decks — resolve with a DeckSafe rebuild; default to new proxy. |

### Donor pulls that cost another deck something (user calls)

| Card | Donor | Impact |
|---|---|---|
| **Vampiric Tutor** | Radiation Sickness | One of Mothman's 3 GCs (added 2026-05-13). Pull = downgrade Mothman, or buy/proxy a 2nd copy. **Biggest contention.** |
| **Demonic Tutor** | Curse of the Scarab *or* Dark Lord's Army | All 3 owned copies deployed (3rd locked in Calamity). Pull = GC downgrade for the donor. |
| Razaketh | Diminishing Returns | DR is mid-B4-pivot (pod approval pending); check the post-pivot list before pulling. |
| Ashnod's Altar, Viscera Seer, Zulaport Cutthroat | Diminishing Returns | DR's aristocrat core — its clock lab says death *volume* is its bottleneck; these pulls hurt. Alternatives: Phyrexian Tower spares, Warren Soultrader (Curse), Marionette Apprentice ×2 free. |
| Skullclamp | Crystal Sickness / Curse / DR / DLA | 2 physical across 4 users — DeckSafe pass to locate. |
| Tendershoot Dryad, Delighted Halfling | Eldrazi Stampede | Minor. |
| Springheart Nantuko | Earthbend the Meta | Minor. |
| Warren Soultrader | Curse of the Scarab | Minor-moderate (its sac engine). |

No-cost pulls (spares exist): Birds of Paradise (3 free), Sol Ring, Arcane Signet, Command Tower,
Toxic Deluge (7 owned), most fetches, Dark Ritual, Mirkwood Bats (2 free), Demonic Tutor only if
a 4th copy is bought.

### GC slot fallback (if the tutor pulls are vetoed)

Mana Vault: **3 owned, 2 free** (only Eldrazi runs one). Grim Monolith 1 free. Both GC. The
deployment model shows mana — not card availability — halves the T6 rate, so
**Necropotence + Demonic (or Vampiric) + Mana Vault** is a credible alternative 3-GC suite that
costs zero donor GC downgrades on one tutor. Sim the two suites head-to-head in the clock lab
before locking.

Note: Necropotence itself is proxy-only (the proxy lives in Genome) — new proxy or real buy.

---

## Buy list (prices = 2026-06 proposal estimates, **unverified** — check Cardmarket before ordering)

**Tier 1 — combo core, strategy-critical, no substitutes (~€15):**
Exquisite Blood ~€5 · Vito, Thorn of the Dusk Rose ~€3 · Sanguine Bond ~€2 ·
Enduring Tenacity ~€1 · Defiant Bloodlord ~€1 · Witherbloom Apprentice ~€1 · Blood Artist ~€2

**Tier 2 — Line B token loop (~€8):**
Sprout Swarm · Lab Rats · Corpse Dance · Cauldron Familiar · Witch's Oven ·
Saproling Migration · Hornet Queen (all ~€0.5–2) · Phyrexian Altar = proxy (real copy €€€)

**Tier 3 — tutor depth (~€10):**
Beseech the Queen · Increasing Ambition · Dark Petition · Nature's Rhythm

**Tier 4 — dorks, substitutable (~€10):**
Llanowar Elves · Fyndhorn Elves · Arbor Elf · Boreal Druid · Elves of Deep Shadow (~€1 each) ·
Deathrite Shaman ~€5–8 (skippable)

**Tier 5 — interaction/lands (~€15):**
Abrupt Decay · Pernicious Deed · Cabal Ritual · Castle Locthwain · Darkbore Pathway ·
Necroblossom Snarl · Bojuka Bog · Night's Whisper

**Total ~€55–70 real (unverified), of which only Tier 1 (~€15) is strictly strategy-critical** if
the rest is proxied/substituted. Proxy-first is established practice in this collection.

---

## Roster consequences

1. **The Calamity Tax 99-route dies.** `The_Calamity_Tax_Swaps_2026-06-01.md` deferred slotting
   Witherbloom + Dellian Fel into Calamity as 99s; building her as commander consumes both cards.
2. **Diminishing Returns overlap.** DR (post-pivot) is the WB aristocrats deck; Witherbloom is BG
   cast-trigger spellslinger/drain. Mechanically distinct per the house-rules test, but DR is also
   the heaviest donor — pulling its pieces while its own pivot awaits pod approval needs an
   explicit user call.
3. **Pod approval.** The Blood+Vito 2-card was pod-approved for this build per the 2026-06-01
   proposal; this would be the roster's ~5th–6th 2-card exception. Consider finally codifying the
   exception pattern in `REF_Bracket_3_House_Rules.md`.
4. **Roster slot.** 16+ decks; either expand or retire (Pest Control proposal is the natural
   casualty — unbuilt, same substrate).

## Pre-sleeve checklist

1. User calls: Vampiric/Demonic pulls vs Mana Vault GC suite; DR donor pulls; roster slot.
2. `wb_clock_lab.py` on `speed_lab_core.py` — decap/table window + GC-suite A/B. **Blocking** for
   any Summary clock claim.
3. Re-verify card text via `card_lookup.py` for the Line B loop pieces (Sprout Swarm, Lab Rats,
   Corpse Dance, Warren Soultrader, Marionette Apprentice, Springheart Nantuko) — the 2026-06-01
   verification log predates them; the 2026-06-07 comparison doc verified some, not all.
4. Apply the locked-card substitutions to a dated `.txt`, count to exactly 100, rerun DeckSafe to
   locate ambiguous physical copies, verify prices before ordering.
