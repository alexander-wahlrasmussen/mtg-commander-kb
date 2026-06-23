# The Grand Design — Atraxa, Grand Unifier (Bracket 3, Final)

## Quick Reference

|Field               |Value                                            |
|--------------------|-------------------------------------------------|
|**Commander**       |Atraxa, Grand Unifier (WUBG)                     |
|**Archetype**       |Reanimator / Flicker / Creature Toolbox          |
|**Bracket**         |3 (strict — exactly 3 Game Changers)             |
|**Game Changers**   |Force of Will, Rhystic Study, Cyclonic Rift      |
|**Conversion Check**|**18/20** (5/5/5/3) — was 19/20; Interaction 4→3 after the 2026-06-23 ramp swap cut 5 interaction/protection pieces (see breakdown)|
|**Kill Window**     |Goldfish: decap T8–11 (median T10) / table T12+ **(board)** — lab-verified 2026-06-10 (`scripts/gd_clock_lab.py`). Old "T6–8" was the optimistic front edge (T6 ≈ 1% god-hand; T8 ≈ 20%). Finale X≥10 fires median T11 / ~9% of games, so the deck decaps via **incremental combat (96% of kills)**, not its named finisher. **Upgraded 2026-06-23** (`decks/the-grand-design-20260623.txt`): ramp + a tutorable Craterhoof move the applied build to **decap median T9 / whiff 10%→5%** (`gd_clock_lab.py --mode userpkg`). See `analysis/Grand_Design_Speed_Curve_Analysis.md` |

-----

> **Anti-archenemy standing (2026-06-15): bring it as the anti-Acererak / anti-tail CONTROLLER, not a racer.**
> `pod_gauntlet.py --vs-lock` (on the **swap** clock — the canonical upgrade's ramp+finisher, decap T10→T9):
> swap alone is **37% blend / 42% vs Acererak**; adding GD's **Elesh Norn** as a persistent ETB-lock takes
> it to **45% blend (up to 49% if the lock sticks) and 59% vs Acererak** (his favorite). It needs **no new
> card** — GD already runs the tech: **Elesh Norn** (opponents' ETBs don't trigger → hard-stops Acererak's
> venture loop), **Path / Swords** (exile → answers *either* commander without the destroy-vs-exile trap
> that feeds Hidetsugu and Kairi / reloads Acererak), and **Teferi T.R. + Force of Will** (protect-own).
> ⚠️ **Correction 2026-06-23:** the 7-for-7 ramp swap **cut Grand Abolisher** — earlier text crediting GD's
> "own Grand Abolisher (the only shell that runs Abolisher)" no longer holds; the protect-own pillar is now
> Teferi + Force of Will + Elesh Norn only. The Elesh-Norn-lock numbers stand (the lift is draw/tutor-gated,
> Abolisher-independent), but the Abolisher tempo edge is gone. It is **weakest vs Hidetsugu and Kairi
> (~34%)** — the ETB-lock is provably **inert** vs a death trigger, so there only exile + counters answer it.
>
> **External corroboration (Draftsim cEDH tier list, 2026-06-18):** an outside ranking framework that weights *speed* and *timing* (does the deck win on the stack / an opponent's turn, or must it commit the whole board?) independently lands on this same controller reframe — GD's primary kill is `board`-timed combat at sorcery speed, the maximal answer window, which is exactly why a 19/20 deck plays a turn-12 table clock. Confirms `score ⊥ clock`; the Timing tag is now in `REF_The_Conversion_Check.md`.
>
> **The swap is the necessary floor, not the lever — and more ramp was tested and rejected.** `gd_clock_lab
> --mode levers/ramp`: an idealized "+2 mana/turn" knob screams T10→**T7**, but that's an always-on artifact
> (the LW-pinger trap); **real** ramp cards cap the decap at **T9** (= the swap) and cost interaction (GD's
> edge), and the Elesh Norn lock is **draw/tutor-gated, not mana-gated** (a single 5-drop), so ramp barely
> moves it. Caveats: the 45–59% uses **tutored** availability and is a **floor** (reanimation uncounted →
> true number higher); it's **removal-sensitive** (mono-B Acererak can kill Elesh Norn → the lift decays at
> high `r` toward the no-lock 42%); `e=0.95` vs ETB is a prior, but the *structure* (inert vs death) is certain.

## What the Deck Does

Atraxa is a 7-mana 7/7 with flying, vigilance, deathtouch, and lifelink. When she enters the battlefield, reveal the top 10 cards of your library and take one of each card type — typically netting 5–7 cards.

The deck abuses this ETB through three interlocking engines:

**Reanimation Engine (9 spells + Karmic Guide):** The deck’s primary reanimation targets in the early game are Razaketh (repeatable tutor), Vilis (massive draw), and Elesh Norn (ETB doubler) — dumped into the graveyard via Buried Alive (deterministic), Grisly Salvage (instant-speed mill 5), or Fauna Shaman (slow but recurring), then reanimated for 1–3 mana. Atraxa herself can only be reanimated after she has been cast from the command zone at least once and you choose to send her to the graveyard instead of back to the command zone when she dies. Early game: reanimate bombs. Mid-to-late game: reanimate Atraxa for cheap re-entry.

**Flicker Engine (6 pieces):** Ephemerate, Thassa Deep-Dwelling, Soulherder, Panharmonicon, Restoration Angel, and Ghostly Flicker blink creatures to re-trigger ETBs (Displacer Kitten cut in the 2026-06-23 swap). Panharmonicon and Elesh Norn Mother of Machines each add one additional ETB trigger — with both in play, each ETB fires 3 times total (base + 1 from Panharmonicon + 1 from Elesh Norn). Note: Elesh Norn also shuts off all opponents’ ETB triggers.

**Creature Toolbox (Birthing Pod + tutors):** Birthing Pod sacrifices a creature to find the next mana value up, directly to the battlefield. Activated at sorcery speed, once per turn. The deck has a complete creature chain from MV 1 through MV 8:

- MV 1: Birds of Paradise
- MV 2: Fauna Shaman, Bloom Tender, Fanatic of Rhonas, Sakura-Tribe Elder
- MV 3: Ranger-Captain of Eos, Eternal Witness, Springbloom Druid
- MV 4: Restoration Angel, Glen Elendra Archmage, Solemn Simulacrum
- MV 5: Karmic Guide, Reveillark, Sidisi, Soulherder
- MV 6: Sun Titan
- MV 7: Atraxa (from command zone first, then graveyard), Elesh Norn
- MV 8: Razaketh, Vilis, Craterhoof Behemoth

Chord of Calling (instant speed, convoke) and Eladamri’s Call (instant speed, to hand) supplement Pod as creature tutors.

-----

## How We End Games

> **⚡ Upgraded 2026-06-23 (7-for-7, applied — `decks/the-grand-design-20260623.txt`).**
> OUT: Carpet of Flowers, Veil of Summer, Flawless Maneuver, Dovin's Veto, Grand Abolisher,
> Displacer Kitten, Heroic Intervention. IN: Solemn Simulacrum, Sakura-Tribe Elder, Springbloom
> Druid, Kodama's Reach, Coalition Relic, **Craterhoof Behemoth**, Fanatic of Rhonas (rationale:
> `proposals/Grand_Design_Upgrade_2026-06-13.md`). **Craterhoof is the new *tutorable* primary
> finisher** (Kill Line 1b below); Finale becomes the un-tutorable backup; ramp lifts decap T10→T9.
> ✅ **Reconciled 2026-06-23:** the Decklist section, the Interaction sub-score (**4/5 → 3/5**,
> CC **19→18**; 5 interaction/protection pieces cut), Kill Lines 1b/5/6, the Pod creature chain,
> the flicker count, the anti-archenemy banner, and the piloting notes are all updated to the
> current 100. The Shopping List (a from-scratch acquisition list) is the only section still
> pre-swap — flagged inline there.

### Kill Line 1: Finale of Devastation at X≥10 — Primary One-Card Win

**Cost:** 12 mana (GG + X where X=10). **Cards needed:** Just Finale.

Finale searches your library or graveyard for a creature with MV ≤X, puts it onto the battlefield, and if X≥10, ALL your creatures get +X/+X and haste until end of turn. At X=10, that’s +10/+10 and haste to everything. With even 3 creatures on board, that’s 30+ power with haste — but note **the deck has almost no trample**, so without it this focus-fires **one opponent** (a decap), not the table; tabling needs a wide board or repeated swings.

> **Clock reality (lab 2026-06-10, `scripts/gd_clock_lab.py`):** the "12 mana by turn 6–7" line is a god-hand, not the norm. Across 40k goldfish trials a lethal Finale (X≥10) fires in only **~9% of games, median turn 11** — too slow and too mana-hungry to be the deck's working closer. **96% of the deck's decaps are incremental combat** (Atraxa + cast/reanimated creatures grinding), median decap **T10**. Treat Finale as the **late-game ceiling**, not "Kill Line 1 — Primary"; the real primary clock is now **Kill Line 1b (Craterhoof, tutorable)** + Kill Line 10 (combat). This is exactly why a *fetchable* creature finisher mattered — fixed in the applied 2026-06-23 upgrade `proposals/Grand_Design_Upgrade_2026-06-13.md` (lab-validated 7-for-7: ramp T10→T9 + Craterhoof; supersedes the older Finisher/ETB/Mana passes, now in `archive/proposals/`).

12 mana for Finale is reachable with Sol Ring, Arcane Signet, Carpet of Flowers (conditional — needs opponents’ Islands), and Bloom Tender producing WUBG (4 mana) once Atraxa is on the battlefield — but the lab shows that conjunction lands a median of turn 11, not 6–7.

The haste clause also solves the Living Death timing problem — if you cast Living Death to rebuild your board (everything has summoning sickness), casting Finale the following turn gives everything haste, making summoning sickness irrelevant.

### Kill Line 1b: Craterhoof Behemoth — Tutorable Overrun (added 2026-06-23)

**Cost:** {5}{G}{G}{G} hardcast (8 mana), or cheated in for far less — reanimate (1–3 mana), Birthing Pod (MV 8), Defense of the Heart, or Finale at X≥8. **Cards needed:** just Craterhoof + a board.

ETB (with haste): creatures you control gain **trample** and get +X/+X where X = the number of creatures you control — it swings the turn it lands. The reason it's the deck's new working finisher: unlike Finale (an **untutorable sorcery**), Craterhoof is a **creature**, so the entire engine finds it — **Birthing Pod, Chord of Calling, Eladamri's Call, Defense of the Heart (straight onto the battlefield → immediate kill), Razaketh, and Finale itself (X≥8 fetches it to play).** It is reanimatable (Buried Alive / Grisly bin it; Reanimate / Animate Dead / Necromancy / Dread Return return it as a 1–3-mana overrun), **Persist now has a legal nonlegendary target**, and the flicker shell (Panharmonicon / Elesh Norn / Ephemerate / Soulherder / Thassa) re-triggers its ETB. The team-wide **trample** also fixes Finale's no-trample focus-fire limitation when both are online. Lab: adding it (with ramp) takes decap median **T10 → T9** and lifts the T8 front edge while halving the whiff rate (`gd_clock_lab.py --mode userpkg`). Finale stays as the late-game ceiling; Craterhoof is the closer the tutors can actually reach.

### Kill Line 2: Defense of the Heart — Automatic

**Cost:** 4 mana to cast, then free. **Condition:** Any opponent controls 3+ creatures at the beginning of your upkeep.

Sacrifice Defense of the Heart → search your library for two creatures, put them directly onto the battlefield. Standard targets: Razaketh + Elesh Norn. Razaketh immediately tutors for Finale (sac a creature, pay 2 life). Elesh Norn doubles all your future ETBs and shuts off opponents’. Cast Finale next turn to close.

Opponents must either remove Defense before your upkeep or keep their creature count under 3, which cripples most Commander strategies.

### Kill Line 3: Razaketh Reanimation → Tutor Chain

**Setup:** Buried Alive or Grisly Salvage dumps Razaketh into graveyard. Reanimate brings him back for 1 mana (pay 8 life).

Razaketh’s ability: pay 2 life, sacrifice another creature, search your library for any card. No tap required — activate as many times as you have life and creatures.

With 2–3 creatures on board after reanimating Razaketh:

1. Sac creature #1 → tutor Finale of Devastation (pay 2 life)
1. Sac creature #2 → tutor Grand Abolisher or Veil of Summer (pay 2 life)
1. Next turn: deploy protection → cast Finale → win

This is a 2-turn kill from a 1-mana Reanimate. The first turn establishes Razaketh and tutors the win; the second turn executes it.

### Kill Line 4: Chord of Calling → Razaketh

**Cost:** X=8 with convoke (tap non-attacking creatures to help pay). Cast on an opponent’s end step.

Razaketh enters at end of opponent’s turn. Sac a creature to tutor Finale. Your turn: cast Finale for the win.

Note: unlike the old Craterhoof line, this works on an opponent’s end step because Razaketh tutors to HAND (not a battlefield buff that expires). You cast Finale on your own turn when the +X/+X and haste matter.

### Kill Line 5: Protected Kill Turns

> _Thinned by the 2026-06-23 swap: **Grand Abolisher** (the only your-turn lock) and **Veil of
> Summer** were cut for ramp. Two protection methods remain — and protection is now the deck's
> softest axis (see Interaction 3/5)._

Two independent protection methods, both tutorable through the creature engine:

|Protector                |How it works                                                                                                                                                            |Limitation                                                                                                                                                     |How you find it                                        |
|-------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------|-------------------------------------------------------|
|**Ranger-Captain of Eos**|Sacrifice: opponents can’t cast **noncreature** spells this turn.                                                                                                       |Does NOT stop creature spells. Opponents could flash in a creature. Stops counterspells, removal, and wraths.                                                  |Chord, Pod, Eladamri’s Call                            |
|**Teferi, Time Raveler** |Static: opponents can only cast spells at sorcery speed.                                                                                                                |Must be on battlefield before the kill turn (loyalty abilities, not an ETB — flickering Teferi resets loyalty but doesn’t trigger anything with Panharmonicon).|Natural draws, Atraxa ETB                              |

### Kill Line 6: Karmic Guide + Reveillark Value Loop

**Requires:** Karmic Guide + Reveillark + Razaketh (as a non-tapping sacrifice outlet) all on the battlefield.

1. Sacrifice Karmic Guide to Razaketh (tutor any card, pay 2 life)
1. Sacrifice Reveillark to Razaketh (tutor any card, pay 2 life)
1. Reveillark’s leave-the-battlefield trigger: return Karmic Guide + one other power ≤2 creature (Eternal Witness, Fauna Shaman, etc.) from graveyard
1. Karmic Guide ETB: return Reveillark from graveyard
1. Repeat from step 1

Each cycle: tutor 2 cards, return a utility creature, costs 4 life. Continue until you’ve tutored Finale + protection + anything else needed. This requires 3 specific creatures on the battlefield simultaneously, so it’s the most setup-intensive line but the most powerful once assembled.

Note: Phyrexian Tower does NOT enable this loop because it taps (one sacrifice per turn cycle). Razaketh’s sacrifice ability has no tap requirement, enabling multiple activations per turn.

Valid Reveillark targets in the deck (power ≤2): Karmic Guide (2/2), Eternal Witness (2/1), Fauna Shaman (2/2), Birds of Paradise (0/1), Bloom Tender (1/1), Glen Elendra Archmage (2/2), Solemn Simulacrum (2/2), Sakura-Tribe Elder (1/1), Springbloom Druid (1/1), Fanatic of Rhonas (1/4). Note: Ranger-Captain of Eos is 3/3 and Craterhoof Behemoth is 5/5 — NOT valid Reveillark targets.

### Kill Line 7: Birthing Pod Chain — Incremental Inevitability

Birthing Pod sacrifices a creature to find MV+1, directly to battlefield. **Sorcery speed only, one activation per turn.** This is a multi-turn chain:

- Turn A: Sac Birds (MV 1) → Fauna Shaman (MV 2, dumps reanimation targets)
- Turn B: Sac Fauna Shaman (MV 2) → Eternal Witness (MV 3, returns a spell)
- Turn C: Sac Eternal Witness (MV 3) → Restoration Angel (MV 4, flickers another creature)
- Turn D: Sac Restoration Angel (MV 4) → Karmic Guide (MV 5, reanimates from graveyard)
- Turn E: Sac Karmic Guide (MV 5) → Sun Titan (MV 6, returns MV ≤3 permanent)
- Turn F: Sac Sun Titan (MV 6) → Elesh Norn (MV 7, doubles ETBs)
- Turn G: Sac Elesh Norn (MV 7) → Razaketh (MV 8, tutors anything)

Each step generates value. The chain can’t be stopped by countering a single spell (Pod is an activated ability, not a spell). You don’t need to go all the way to MV 8 — stopping at Karmic Guide or Sidisi is often enough to close.

### Kill Line 8: Living Death — Board Recovery Into Kill

**Cost:** 5 mana. Living Death sacrifices all creatures on the battlefield, then returns all creature cards from all graveyards to the battlefield.

**Critical rules note:** All returned creatures have summoning sickness. They cannot attack the turn they enter. This is NOT a same-turn kill. Living Death rebuilds your board (Atraxa drawing 5–7 on ETB, Elesh Norn doubling triggers, Razaketh ready to tutor) and sets up a kill on the following turn via Finale (which grants haste, bypassing summoning sickness).

### Kill Line 9: Sidisi, Undead Vizier — Exploit Tutor

Sidisi’s exploit ETB sacrifices a creature to tutor any card. With Panharmonicon, the exploit ETB triggers twice — sacrifice two creatures, tutor two cards. With both Panharmonicon and Elesh Norn, it triggers three times. Each exploit that sacrifices a creature generates a separate tutor.

Sidisi can exploit herself (sacrificing herself for one tutor with no other creatures needed). Flickering Sidisi with Ephemerate or Thassa repeats the exploit.

### Kill Line 10: Atraxa Combat — Backup

Atraxa is a 7/7 with flying, vigilance, deathtouch, and lifelink. Three combat steps per player for commander damage lethal (21). Lightning Greaves provides haste for immediate connection. Not flashy, but always available from the command zone.

-----

## Conversion Check Breakdown

### Core Loop: 5/5

Three interlocking engines: 7 flicker pieces, 9 reanimation spells + Karmic Guide, and Birthing Pod with a complete MV 1–8 creature chain. 40+ cards directly serve the engine. Every creature is tutorable, reanimatable, and (mostly) flickerable.

Panharmonicon + Elesh Norn = 3x ETB triggers (not 4x — each adds one additional trigger to the base).

Known interaction restrictions: Restoration Angel cannot flicker Karmic Guide (both are Angels — Restoration Angel says “non-Angel”). All 5 other flicker pieces work on Karmic Guide normally.

Persist (the spell) cannot reanimate legendary creatures (Atraxa, Razaketh, Vilis, Elesh Norn, Sidisi are all legendary). It remains useful as a cheap way to reanimate Karmic Guide, who then reanimates any legendary creature — a 2-card chain rather than a direct reanimate.

### Kill Reliability: 5/5

Multiple distinct kill paths plus Atraxa combat as a permanent backup. **Craterhoof Behemoth (added 2026-06-23) is now the working primary finisher** — a *tutorable* creature overrun the whole engine can fetch (Pod / Chord / Eladamri's / Defense / Razaketh / Finale itself) and reanimate, fixing the old single-point-of-failure where every line funneled through the un-tutorable Finale. Finale of Devastation at X≥10 remains the late-game one-card ceiling (12 mana). Defense of the Heart is an automatic win (now fetching Craterhoof straight to the battlefield). Razaketh provides adaptable tutoring for the exact closer needed; the Karmic Guide + Reveillark + Razaketh loop tutors your entire deck; Birthing Pod provides incremental inevitability.

The deck draws 5–7 cards per Atraxa ETB, making it highly likely to find a finisher naturally even without tutoring. Holds **5/5** — diversifying to a tutorable finisher kept reliability high while the ramp swap moved the clock (decap T10→T9).

### Durability: 5/5

9 reanimation spells for the primary targets (all cleanly hit legendary creatures except Persist, which chains through Karmic Guide). Living Death and Dread Return work from the graveyard. Karmic Guide provides creature-based reanimation that works with the flicker engine. Fauna Shaman dumps targets into graveyard while finding replacements.

Atraxa can only be reanimated after dying from the battlefield at least once (she starts in the command zone, not the library — Buried Alive and Grisly Salvage cannot put her into the graveyard directly). The early reanimation targets are Razaketh, Vilis, and Elesh Norn, which are often better early targets anyway.

### Interaction: 3/5  _(was 4/5 — dropped 2026-06-23; the ramp swap cut 5 interaction/protection pieces)_

> **Re-scored 2026-06-23.** The 7-for-7 ramp/finisher swap cut **Dovin's Veto, Grand Abolisher,
> Heroic Intervention, Flawless Maneuver, and Veil of Summer** — taking interaction/protection from
> **20 → 15 pieces**. The *counter + removal* core is intact and still deep, but the deck lost its
> **only proactive your-turn lock (Grand Abolisher)** and **3 of its 4 protection spells** — the
> exact "protect the kill turn" tools. Counters/removal quantity alone clears the bar for 4, but the
> protection collapse (down to Lightning Greaves + Teferi) is a full-grade quality hit, so **3/5**.
> ⚠️ This also dents the "disruption-led fortress" identity below: the anti-archenemy plan that
> credited *own Grand Abolisher* now leans on Teferi + Force of Will + Elesh Norn only.

**Counterspells (5 spells + 1 creature):**

- Force of Will (GC) — free (pitch a blue card, lose 1 life), counters ANY spell on ANY turn. 5 mana hard-cast.
- Force of Negation — free on **opponents’ turns only** (pitch a blue card), noncreature spells only. On your own turn it costs 1UU.
- Counterspell — 2 mana, counters ANY spell
- Mana Drain — 2 mana, counters ANY spell, generates mana
- Swan Song — 1 mana, counters instant/sorcery/enchantment only
- Glen Elendra Archmage — sacrifice to counter a noncreature spell. Persist returns her with a -1/-1 counter for one more use (2 total per cycle). Flickering removes the counter for 2 more. Not unlimited — 2 per flicker cycle.

**Counterspell, Mana Drain, and Force of Will can counter creature spells.** The gap on flash creatures and creature-based combos is closed by Force of Will.

**On your own turn:** 2 free spells (Force of Will, Deadly Rollick). Force of Negation costs full price.
**On opponents’ turns:** 3 free spells (add Force of Negation).

**Removal (6):** Cyclonic Rift (GC, asymmetric bounce), Deadly Rollick (free with Atraxa), Swords to Plowshares, Path to Exile, Generous Gift, Assassin’s Trophy, Toxic Deluge

**Proactive disruption (1):** Teferi Time Raveler (opponents can only cast at sorcery speed — note: Teferi’s abilities are loyalty abilities, not ETBs; flickering resets his loyalty but does not trigger Panharmonicon or Elesh Norn). _(Grand Abolisher cut.)_

**Protection (1):** Lightning Greaves. _(Heroic Intervention, Flawless Maneuver, Veil of Summer cut.)_ Ranger-Captain of Eos (sac → no opponent noncreature spells) remains a tutorable soft-protection creature.

**Total: 15 interaction and protection pieces.** Still good quantity and mostly tutorable through the creature engine; the un-tutorable-noncreature ceiling (no Demonic/Vampiric Tutor — both GCs) is unchanged. The drop to 3/5 is the **protection collapse**, not the counter/removal suite.

-----

## Bracket 3 Compliance

Exactly 3 Game Changers:

1. **Force of Will** — free counter (pitch a blue card, lose 1 life), counters any spell on any turn
1. **Rhystic Study** — passive card-draw engine; opponents pay 1 or you draw
1. **Cyclonic Rift** — asymmetric board wipe

**Notable non-GC power cards:** Razaketh, Finale of Devastation, Craterhoof Behemoth, Defense of the Heart, Birthing Pod, Chord of Calling, Force of Negation, Teferi Time Raveler, Mana Drain, Deadly Rollick, Glen Elendra Archmage, Ranger-Captain of Eos, Elesh Norn Mother of Machines, Karmic Guide, Reveillark, Sidisi Undead Vizier, Panharmonicon, Sun Titan, Phyrexian Tower.

-----

## Decklist (100 cards)

### Commander (1)

1 Atraxa, Grand Unifier

### Game Changers (3)

1 Force of Will
1 Rhystic Study
1 Cyclonic Rift

> _Decklist reconciled to the 2026-06-23 swap (`decks/the-grand-design-20260623.txt`)._

### Flicker Engine (6)

1 Ephemerate
1 Thassa, Deep-Dwelling
1 Panharmonicon
1 Soulherder
1 Restoration Angel
1 Ghostly Flicker

### Reanimation & Graveyard Filler (9)

1 Reanimate
1 Animate Dead
1 Necromancy
1 Victimize
1 Living Death
1 Dread Return
1 Persist
1 Buried Alive
1 Grisly Salvage

### Creatures — Value & Finishers (10)

1 Elesh Norn, Mother of Machines
1 Razaketh, the Foulblooded
1 Vilis, Broker of Blood
1 Sun Titan
1 Karmic Guide
1 Reveillark
1 Sidisi, Undead Vizier
1 Eternal Witness
1 Fauna Shaman
1 Craterhoof Behemoth

### Creatures — Interactive (2)

1 Glen Elendra Archmage
1 Ranger-Captain of Eos

### Planeswalker (1)

1 Teferi, Time Raveler

### Tutors & Kill (4)

1 Eladamri’s Call
1 Chord of Calling
1 Birthing Pod
1 Finale of Devastation

### Enchantment — Kill Setup (1)

1 Defense of the Heart

### Counterspells (4)

1 Counterspell
1 Mana Drain
1 Force of Negation
1 Swan Song

### Removal (6)

1 Swords to Plowshares
1 Path to Exile
1 Generous Gift
1 Assassin's Trophy
1 Toxic Deluge
1 Deadly Rollick

### Protection (1)

1 Lightning Greaves

### Ramp (13)

1 Sol Ring
1 Arcane Signet
1 Coalition Relic
1 Three Visits
1 Nature’s Lore
1 Farseek
1 Kodama’s Reach
1 Birds of Paradise
1 Bloom Tender
1 Sakura-Tribe Elder
1 Springbloom Druid
1 Solemn Simulacrum
1 Fanatic of Rhonas

### Lands (39)

1 Command Tower
1 Exotic Orchard
1 Breeding Pool
1 Hallowed Fountain
1 Overgrown Tomb
1 Watery Grave
1 Temple Garden
1 Godless Shrine
1 Polluted Delta
1 Windswept Heath
1 Verdant Catacombs
1 Misty Rainforest
1 Flooded Strand
1 Marsh Flats
1 Bojuka Bog
1 Otawara, Soaring City
1 Eiganjo, Seat of the Empire
1 Yavimaya, Cradle of Growth
1 Indatha Triome
1 Zagoth Triome
1 Rejuvenating Springs
1 Undergrowth Stadium
1 Vault of Champions
1 Morphic Pool
1 Phyrexian Tower
1 Reflecting Pool
1 City of Brass
3 Forest
3 Island
4 Plains
2 Swamp

-----

## Shopping List

> ⚠️ **Pre-swap (2026-06-23).** This is the original from-scratch acquisition list and still lists
> cut cards (Carpet of Flowers, Displacer Kitten, Veil of Summer) and omits the swap's adds
> (Craterhoof, Solemn, Sakura, Springbloom, Kodama's, Coalition Relic, Fanatic of Rhonas — all owned
> spares, $0). The applied swap needs **no purchases**; see `proposals/Grand_Design_Upgrade_2026-06-13.md`.

|Card                     |Role                                     |Est. Price|
|-------------------------|-----------------------------------------|----------|
|Force of Will            |Free counter (any spell, any turn) — GC  |~$70      |
|Rhystic Study            |Passive card-draw engine — GC            |~$50      |
|Bloom Tender             |MV-2 ramp creature; WUBG with Atraxa     |~$30      |
|Force of Negation        |Free counter (opponents’ turns)          |~$35      |
|Razaketh, the Foulblooded|Repeatable creature tutor / sac outlet   |~$15      |
|Assassin’s Trophy        |2-mana removal (any permanent)           |~$8       |
|Bojuka Bog               |Utility land — graveyard hate            |~$3       |
|Grisly Salvage           |Instant-speed mill 5 (graveyard filler)  |~$0.50    |
|Atraxa, Grand Unifier    |Commander                                |~$15      |
|Birthing Pod             |Repeatable creature chain                |~$12      |
|Defense of the Heart     |Automatic 2-creature tutor               |~$10      |
|Finale of Devastation    |One-card win at X≥10                     |~$20      |
|Indatha Triome           |Land                                     |~$8       |
|Zagoth Triome            |Land                                     |~$6       |
|Phyrexian Tower          |Sac outlet on a land                     |~$8       |
|Carpet of Flowers        |Premium ramp                             |~$6       |
|Displacer Kitten         |Flicker on noncreature casts             |~$5       |
|Chord of Calling         |Instant creature tutor with convoke      |~$5       |
|Teferi, Time Raveler     |Sorcery-speed lock                       |~$5       |
|Veil of Summer           |Blue/black protection                    |~$5       |
|Vilis, Broker of Blood   |Draw engine reanimation target           |~$4       |
|Ranger-Captain of Eos    |Tutorable noncreature Silence            |~$4       |
|Sun Titan                |MV 6 Pod bridge + recursion              |~$1       |
|Sidisi, Undead Vizier    |Exploit ETB tutor                        |~$2       |
|Karmic Guide             |Creature-based reanimation               |~$3       |
|Reveillark               |Returns power ≤2 creatures from graveyard|~$1       |
|Glen Elendra Archmage    |2 counters per flicker cycle             |~$2       |
|Fauna Shaman             |Creature tutor + graveyard enabler       |~$3       |
|Persist                  |Cheap reanimate (nonlegendary only)      |~$2       |
|Reflecting Pool          |4-color fixing                           |~$3       |
|City of Brass            |4-color fixing                           |~$5       |
|**Total**                |                                         |**~$372** |

### Conflict cards (need extra copies):

|Card              |Shared with                                          |Fix cost|
|------------------|-----------------------------------------------------|--------|
|Reanimate         |Teysa, Sauron                                        |~$2     |
|Animate Dead      |Sauron                                               |~$3     |
|Necromancy        |Sauron                                               |~$4     |
|Buried Alive      |Sauron                                               |~$2     |
|Swan Song         |Loam Cycle, Sauron                                   |~$3     |
|Temple Garden     |Bumbleflower, Toph, Sythis                           |~$10    |
|Bojuka Bog        |6+ decks (zero-surplus per Collection_Master_Status) |~$3     |
|**Conflict total**|                                                     |**~$27**|

*Note: post-swap shared-card analysis needs `WF_Deck_Safe_Collection.md` re-run to be exact. Bloom Tender, Rhystic Study, Force of Will, Assassin’s Trophy, and Grisly Salvage may also create new conflicts depending on other decks’ demand.*

## Don't-Miss Rulings

- **Atraxa starts in the command zone**, so Buried Alive / Grisly Salvage **cannot** mill her. She's only reanimatable after she's died *from the battlefield* (choose graveyard over command zone). Early reanimation targets are **Razaketh, Vilis, Elesh Norn**.
- **Panharmonicon + Elesh Norn = 3× ETBs** (each adds one trigger: base + 1 + 1), not 4×. Elesh Norn also **shuts off opponents' ETB triggers**.
- **Restoration Angel can't flicker Karmic Guide** — both are Angels, and she only blinks a non-Angel. The other five flicker pieces work fine.
- **Persist can't reanimate legendaries.** Use it on Karmic Guide, who then returns a legend — a 2-card chain.
- **Razaketh's sacrifice has no tap cost** — activate as many times as you have creatures and life (2 each). This is why **Phyrexian Tower does NOT** enable the Karmic Guide + Reveillark loop (it taps), but Razaketh does.
- **Living Death is not a same-turn kill** — returned creatures have summoning sickness. Rebuild now, win next turn with Finale's haste.
- **Teferi, Time Raveler's abilities are loyalty, not ETB** — flickering him resets loyalty but triggers nothing.
- **Reveillark returns power ≤2 only** (Ranger-Captain is a 3/3 — not a valid target). **Veil of Summer protects vs. blue/black only.**

## Piloting Notes (for borrowers)

**Mulligan.** Looking for: **mana toward a reanimation or Atraxa line** — a dork/rock plus either a graveyard-filler (Buried Alive, Grisly Salvage) and a cheap reanimate, or a Birthing Pod start.

- **Keep:** hands that reanimate a bomb by T3–4, cast Atraxa T6–7, or start a Pod chain with a creature.
- **Toss:** no-mana hands; reanimation spells with nothing to fill the yard; all-payoff/no-setup.
- You **do not** need Finale in your opener — Atraxa's ETB draws 5–7 and finds it.

**Threats & timing.**

- **Interaction is deep** — Force of Will, Counterspell, and Mana Drain all hit creature spells; Force of Will and Deadly Rollick are free with Atraxa. Hold counters up on opponents' turns.
- **Graveyard hate hurts the reanimation half**, but Birthing Pod and Atraxa's ETB still function — you have a non-yard backup plan, so don't fold.
- **You can't tutor noncreature answers** (no Demonic/Vampiric Tutor — that would break the 3-GC cap). Find interaction by drawing it.
- **Protect the kill turn (now thin — see Interaction 3/5):** Ranger-Captain (sac → no opponent noncreature spells), Teferi (sorcery-speed only), Lightning Greaves (shroud the finisher), plus held counters. The 2026-06-23 ramp swap cut Grand Abolisher / Veil of Summer / Flawless Maneuver / Heroic Intervention, so sequence the kill behind a counter or Teferi rather than a dedicated lock.
