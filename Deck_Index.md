# Deck Index

One-page view of the active roster. Scores reflect the most recent audit. Ground truth for deck contents is each deck's `.txt` file — this index is a summary.

---

## Active roster

| Deck                   | Commander                   | Colors |     Score | Archetype                   | Status                                                            |
| ---------------------- | --------------------------- | ------ | --------: | --------------------------- | ----------------------------------------------------------------- |
| The Grand Design       | Atraxa, Grand Unifier       | WUBG   |     19/20 | Midrange / superfriends     | Elite (audited 2026-05-02)                                        |
| Croak and Dagger       | Glarb, Calamity's Augur     | Sultai |     18/20 | Topdeck combo-control       | Elite (Clock T9 decap / T9 table — Sensei's Top → Aetherflux inevitability combo, counter-immune kill; promoted 2026-07-01, lab `glarb_inevitable_lab.py`) |
| Lightning War          | Fire Lord Azula             | Grixis |     19/20 | Spellslinger / burn         | Elite (Clock decap T8 / table T9 best-line — lab 2026-06-28; built + fully owned, `lightning-war-20260706` — Increasing Vengeance→Irma + Vedalken Orrery swap 2026-07-06) |
| The Dark Lord's Army   | Sauron, the Dark Lord       | Grixis |     19/20 | Tokens / The Ring           | Elite (audited 2026-05-08; Clock decap T9 / table T12 typical pod, tempo-dependent, lab 2026-06-13) |
| The Exile's Return     | Fire Lord Zuko              | Mardu  |     17/20 | Exile-matters / firebending | Elite                                                             |
| Earthbend the Meta     | Toph, the First Metalbender | Naya   |     17/20 | Artifact stompy             | Elite (Clock T8 decap / T12 table, lab 2026-06-13)              |
| The Replication Crisis | Satya, Aetherflux Genius    | Jeskai |     17/20 | Copy / clone                | Elite (rescored 2026-05-13)                                       |
| Curse of the Scarab    | The Scarab God              | Dimir  |     17/20 | Zombie tribal               | Elite (Clock T8 decap / T11 table, lab 2026-06-13)              |
| Crystal Sickness       | Golbez, Crystal Collector   | Dimir  |     17/20 | Reanimator                  | Elite (Clock T11 decap / T13 table, lab 2026-06-13)              |
| Lorehold Spirits       | Quintorius, History Chaser  | Boros  |     18/20 | Spirits / graveyard cycling | Elite (Clock T8 decap / T10 table, lab 2026-06-13)              |
| The Genome Project     | Kuja, Genome Sorcerer       | Rakdos |     15/20 | Reanimator / combo          | Solid                                                             |
| Ms. Bumbleflower       | Ms. Bumbleflower            | Bant   |     16/20 | Spellslinger / tempo-control | Solid (Clock T8 decap ceiling / T11 table, front edge doubled — lab 2026-07-03; **"quiet exits" package applied 2026-07-03**: +Approach +Intruder Alarm +Wizard Class, close-mixture 60/32/8, 0 GCs, KR 3→4; buy 2 cards ≈ €6) |
| Eldrazi Stampede Chaos | Maelstrom Wanderer          | Temur  |     14/20 | Ramp / cascade / huge stuff | Solid (audited 2026-05-08; Clock T8 decap / T12 table, lab 2026-06-13) |
| Radiation Sickness     | Wise Mothman                | Sultai |     18/20 | Rad / toxic                 | Elite (audited 2026-05-13; Clock T10 table-win / T7 decap, lab 2026-06-13) |
| Zero-Sum Game          | Witherbloom, the Balancer   | Golgari |     16/20 | Lifeloop combo / spellslinger-drain | **Built & physically assembled 2026-07-08** (final cards sourced by dismantling Diminishing Returns; sleeved `zero-sum-game-20260707.txt`; audited 2026-06-27 = 5/5/4/2, Interaction-floored; Clock T9 decap=table, lab 2026-06-11) |
| Forced Liquidation     | Kefka, Court Mage           | Grixis  |     16/20 | Wheel-burn / punisher static | **Built & physically assembled 2026-07-08** (final cards sourced by dismantling Diminishing Returns; sleeved `forced-liquidation-20260707.txt`; audited 2026-06-27 = 5/4/3/4, Durability-capped; Clock decap T8 / table T9, lab 2026-06-25; 3/3 GC; no pod approval — kills through statics) |

### Retired

| Deck | Commander | Note |
| --- | --- | --- |
| Diminishing Returns | Teysa Karlov | Dismantled 2026-07-08 (was 17/20 Elite); torn down to physically source Zero-Sum Game (10 cards) + Forced Liquidation (Lightning Greaves); decklist + summary archived to `archive/old_decklists/`, remaining cards returned to pool |
| The Loam Cycle | Teval, the Balanced Scale | Dismantled 2026-06-08; decklist archived 2026-06-11; cards returned to pool |
| Peace Offering | Ms. Bumbleflower | Dismantled 2026-06-13; redundant 2nd Ms. Bumbleflower build (This Bunny Goes to Market is the active one); decklist archived to `archive/old_decklists/`, cards returned to pool |

---

## Tier summary

- **Elite (17+):** 11 decks (Diminishing Returns 17 left the roster — dismantled 2026-07-08).
- **Solid (13–16):** 5 decks (incl. Zero-Sum Game 16 + Forced Liquidation 16, audited 2026-06-27 from the list — both **built & physically assembled 2026-07-08** (final cards pulled from the Diminishing Returns teardown); re-audit after first pod games).
- **Developing (9–12):** 0.
- **Unscored:** 0.
- **Active roster:** 16 decks.

---

## Outstanding work

- **H2:** Ms. Bumbleflower formal summary — ✅ done 2026-05-30 (15/20; `Ms_Bumbleflower_Summary.md`).
- **Lorehold Spirits:** upgrade pass applied 2026-05-03. Goblin Bombardment acquired 2026-05-30 — combo line live; rescored 17/20 → 18/20.
- **Proxy list:** 35 cards for cross-deck testing, physical testing not yet completed.

---

## Candidate new builds

Flagged for consideration, not yet built:

- ~~**Berta, Wise Extrapolator** (GU)~~ — **SHELVED 2026-06-14.** Real-engine re-lab (adding her own Intruder Alarm infinite + a dig engine the external lists run) lifted the in-cap clock only to **36% by T12 / median never / T7 10%** — still a decisively worse Najeela. Combo is falsified *for the 3-GC cap* (un-tutorable singleton enablers in GU; the bottleneck is drawing them, which more dorks/draw don't fix); "competes" would require **waiving the cap** (external Deck #1 = 7 GCs). Worked record: `proposals/PROP_Berta_Wise_Extrapolator.md` + `analysis/Candidate_Clock_Labs_Berta_Najeela_2026-06-13.md` (06-14 addendum).
- ~~**Hashaton, Scarab's Fist** (Esper)~~ — **DROPPED 2026-06-27.** Was the sole Thassa's Oracle deck; user is **not building a Thoracle deck** (neither Hashaton nor the old Calamity-hybrid). Thoracle is out of the roster entirely. Proposal kept for record: `proposals/PROP_Hashaton_Scarabs_Fist.md`. The build slot went to **Forced Liquidation (Kefka)** — wheel-burn, no Thoracle, no pod approval — now cards-on-order in the active roster.
- ~~**Najeela, the Blade-Blossom** (5C)~~ — **DROPPED 2026-06-14** (user done with the Berta/Najeela round). Warrior tribal + infinite-combat combo; `proposals/PROP_Najeela_Blade_Blossom.md`. Not falsified — clock lab 2026-06-13 had it at median T10 (reliable combo, not a T6–7 racer), the stronger of the two candidates, so it's the better starting point if ever revisited. See `analysis/Candidate_Clock_Labs_Berta_Najeela_2026-06-13.md`.
- ~~**Winota, Joiner of Forces** (RW)~~ — **CLOSED 2026-07-01 — not building.** Go-wide Human-flood racer; genuine clock (decap **T6–7** / table **T9–11**) once the command-zone engine bug was fixed. The 2026-07-01 owned-buildability check (owned-only + no-new-purchase variants) confirmed it's buildable from the collection at only a slight clock cost, but that was never the blocker: it's a **peer, not an upgrade**, of the existing T6–7 racers (Genome/Radiation/Replication), and adding it deepens the race plan when the goal is to diversify *away* from racing. Worked record + closure table: `proposals/PROP_Winota_Joiner_of_Forces.md`; lab `scripts/winota_clock_lab.py`.
- Hinata
- Krark + Sakashima (pairs / partner shell)

Before building: verify no mechanical overlap with existing roster (see `REF_Bracket_3_House_Rules.md` — Mechanical distinctiveness is a hard filter).

---

## Maintenance notes

- Update this file whenever a score changes, a new deck enters the roster, or a deck is retired.
- Re-audit triggers: any swap of more than 3 cards; commander change; any shift that alters the Core Loop description.
- This file is state, not reference. Don't treat old entries as authoritative — check each deck's `_Summary.md` and `.txt`.
