# Auto-Brewer — the owned-pool commander sweep (2026-07-15)

**Instrument:** `scripts/auto_brewer.py` · **Data:** `analysis/autobrew/leaderboard.json`,
`analysis/autobrew/lists/*.txt`, `analysis/autobrew/csb_variants_cache.json` ·
**Tests:** `tests/test_auto_brewer.py` (24 hermetic)

Every deck in this repo's history was *human-proposed, machine-verified*. This flips the
pipeline: the machine proposes, the human vets. The tool enumerates every owned card that
can legally helm a deck, seeds each with the Commander Spellbook combos we already own the
pieces for, drafts a template 99 from the owned pool, and screens the draft with the
repo's own consistency instruments. Deficit Spending and the Winota re-open were this
process done by hand; this is the process as an instrument.

**Every number below is SCREEN-grade** (consistency / availability). The assembly figure
is P(combo pieces *seen* by a turn) — no mana costs, no opposition, no kill resolution.
Nothing here is a kill-window claim. A winner graduates the same way every deck does:
hand-written proposal → `availability_check.py` → real `*_clock_lab`.

---

## The sweep

- **420** owned commander candidates (Legendary Creature front face or "can be your
  commander" text, banlist-filtered). 391 are NEW (not roster, not previously evaluated);
  all 391 were brewed and scored at 2 000 trials.
- **102 / 391** candidates anchor at least one **fully-owned** CSB combo; 55 anchor five
  or more. Median SCREEN score 59.0; only 6 candidates clear 90.
- House rules enforced *inside* the brew: ≤3 Game Changers (commander counted), mass land
  denial excluded outright, ≤1 extra-turn card, combos producing turns skipped.
- CSB fetches are cached (`csb_variants_cache.json`, ~5 MB, the repo's first CSB cache).
  First run burned 310/391 fetches on HTTP 429 — `_csb_get` now paces requests (0.8 s
  gap) and honours Retry-After; the re-run had zero failures.

## Leaderboard (top 15 of 391)

| # | Commander | CI | SCREEN | Owned combos | Asm@T10 | Keep% | Dead turns |
|--:|---|---|--:|--:|--:|--:|--:|
| 1 | Nissa, Resurgent Animist | G | 93.5 | 14 | 28.4% | 99.2 | 0.95 |
| 2 | Endrek Sahr, Master Breeder | B | 93.3 | 4 | 42.6% | 99.5 | 0.87 |
| 3 | Sheoldred, the Apocalypse | B | 92.3 | 7 | 29.1% | 99.2 | 0.98 |
| 4 | Szarel, Genesis Shepherd | BGR | 92.2 | 12 | 41.5% | 99.7 | 1.03 |
| 5 | Gev, Scaled Scorch | BR | 91.3 | 8 | 28.9% | 99.1 | 1.23 |
| 6 | Vivi Ornitier | RU | 91.1 | 3 | 40.5% | 99.5 | 0.84 |
| 7 | Long Feng, Grand Secretariat | BG | 87.4 | 19 | 29.1% | 99.2 | 0.91 |
| 8 | Vito, Thorn of the Dusk Rose | B | 87.3 | 2 | 40.8% | 99.5 | 0.93 |
| 9 | Avatar Aang // Aang, Master of Elements | 5C | 84.8 | 2 | 27.2% | 99.1 | 0.95 |
| 10 | Monk Gyatso | W | 84.8 | 19 | 15.9% | 99.3 | 0.48 |
| 11 | Alania, Divergent Storm | RU | 83.8 | 4 | 16.4% | 99.2 | 0.45 |
| 12 | Niv-Mizzet, Parun | RU | 82.9 | 3 | 16.9% | 99.4 | 0.29 |
| 13 | Mazirek, Kraul Death Priest | BG | 82.8 | 9 | 16.1% | 99.2 | 0.97 |
| 14 | Yahenni, Undying Partisan | B | 82.4 | 90 | 16.5% | 99.5 | 0.87 |
| 15 | Neheb, the Eternal | R | 82.1 | 1 | 28.2% | 99.2 | 1.10 |

Commander text of the top 8 verified against the bulk before writing this (read-the-card
rule); brewed lists for all 15 are in `analysis/autobrew/lists/`.

## Spotlights (text-verified)

- **Endrek Sahr, Master Breeder (#2, mono-B)** — {4}{B} Human Wizard: every creature
  spell breeds MV-worth of Thrull tokens (sacrifices himself at 7+ Thrulls — a real
  tension the screen does not model). Best assembly screen of the field (42.6% @T10)
  because his packages are 2-piece (Phyrexian/Ashnod's Altar cluster + Gray Merchant)
  inside mono-B tutor density.
- **Vito, Thorn of the Dusk Rose (#8, mono-B)** — the leanest kill shape found:
  **commander + one card** (Exquisite Blood, with Bloodthirsty Conqueror as a true
  redundant copy) is a closed loop. Two cards of redundancy on a 2-piece infinite where
  one piece is always castable from the command zone.
- **Nissa, Resurgent Animist (#1, mono-G)** — landfall mana + Elf/Elemental chain-dig;
  14 owned combos (Springheart Nantuko / Lumra / Zuran Orb). Highest composite, but the
  packages are land-loop combos — pilot-intensive, and the screen can't see that.
- **Sheoldred, the Apocalypse (#3, mono-B)** — the draw-punisher shell: Peer into the
  Abyss one-shot plus Top/Citadel/Necropotence engines (2 GCs, cap respected). Note the
  seeded package includes **K'rrik** — see the contention warning below.
- **The altar cluster (Szarel #4, Gev #5, Long Feng #7, Mazirek #13, Yahenni #14)** —
  five of the top 15 are the *same* owned aristocrats core (Ashnod's Altar, Phyrexian
  Altar, Viscera Seer, Carrion Feeder, Goblin Bombardment, Altar of Dementia…) wearing
  different commanders. The sweep independently rediscovered the mono-B/x aristocrats
  space the hand-written Deficit Spending proposal (K'rrik) just picked — corroboration
  for the archetype, and a queue: **one** of these can exist physically at a time.
- **Combo-density outliers** — Ashaya, Soul of the Wild (94 owned combos), Yahenni (90),
  Kodama of the East Tree (87); Yahenni is also 445 combos *one card away*. The
  composite ranks them mid-table (their packages are 3-4 pieces, weaker assembly), but as
  raw "the collection already contains this deck" signals they are remarkable.

## Contention warning (do NOT skip at graduation)

The top packages lean heavily on cards **physically deployed in active decks** — the
altar cluster overlaps Zero-Sum Game and Forced Liquidation card-for-card, and the
Sheoldred package wants K'rrik while the Deficit Spending proposal wants him as its
commander. The brewer screens against the *whole* collection by design (ownership, not
availability). Any graduation must run `availability_check.py` first, per the hard rule.

## Instrument notes / known biases

1. **Keepable% saturates** (template builds all land ~99%) — it only flags broken
   manabases; the differentiating axes are assembly, flow, and combo depth.
2. **Quota-fill vs scorer mismatch**: the brew fills ramp/draw quotas from Scryfall otags,
   but the scorer counts the stricter framework_bakeoff tagger (Long Feng: 12 filled by
   otag, 4 counted by the scorer). Conservative direction, consistent across all decks;
   a calibration pass could align them.
3. **The combo axis is deliberately heavy** (35/100): this pod's bar is a proven kill
   package (kill-shape lens), so value decks with no owned combo cap at ~65.
4. **No partner/background pairing** (v1) — partner pairs like Krark+Sakashima are
   invisible; Krark solo has exactly 1 CSB variant, which the probe confirmed is real.
5. **Theme heuristics are coarse** (curated trigger→tag table + tribal-mention check).
   Good enough to fill a screen 99; not a substitute for reading the 99.
6. **CSB popularity/variants shift** — the cache is dated 2026-07-15; refresh with
   `--refresh-combos` when re-running months later.

## Suggested graduations (user's call)

1. **Vito, Thorn of the Dusk Rose** — cheapest vet: 2-card closed loop with command-zone
   access and owned redundancy; mono-B grind shell that dodges the pod's counterspell
   profile the same way Zero-Sum does. Check Exquisite Blood / Conqueror contention first.
2. **Endrek Sahr** — best assembly screen; but same pool as Deficit Spending; treat as a
   *competitor* to K'rrik for the mono-B aristocrats seat, not an addition.
3. **Gev, Scaled Scorch** — the interesting *non*-overlap: BR counters/lizards with the
   altar package, would inherit the Winota-adjacent aggressive seat if the redundancy
   question kills the Winota rebuild.

Next instrument steps (only if the screen earns trust at graduation): align the two
taggers (bias #2), partner pairing, and a `--free-pool` mode that nets out deployed cards.
