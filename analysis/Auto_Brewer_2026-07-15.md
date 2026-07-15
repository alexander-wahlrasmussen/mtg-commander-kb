# Auto-Brewer — the owned-pool commander sweep (2026-07-15)

**Instrument:** `scripts/auto_brewer.py` · **Data:** `analysis/autobrew/leaderboard.json`,
`analysis/autobrew/lists/*.txt`, `analysis/autobrew/csb_variants_cache.json` ·
**Tests:** `tests/test_auto_brewer.py` (25 hermetic, incl. the template-gating REGRESSION)

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

## Correction, same day: template-gated combos (the vet worked)

The first published leaderboard read CSB variants with **template requirements** as
complete combos. The user's first vet question ("what are the Gev combos?") falsified
row #5 within the hour: all 8 of Gev's "owned 2-card combos" are Gev + a free sac
outlet **+ any persist creature** (a CSB `requires` template the cache trim had
dropped) — and `pool_search` shows we own **zero** BR persist creatures. Gev's true
state: 0 complete, 8 template-gated, rank 295.

Fix: `fetch_variants` now records `requires`; `combos_for` puts any template-carrying
variant in its own `template_gated` bucket (strict — the screen never assumes a generic
slot is fillable); regression test pins the Gev case. Only 19/391 commanders had gated
variants at all, but they concentrated at the top of the board — "commander + outlet +
template" is exactly the 2-piece shape that wins the assembly screen. Nissa (old #1,
93.5) kept 12 genuine combos but lost her leanest packages to the gate → 70.9, rank 33;
Szarel (old #4) similarly 12→4 complete. Endrek/Sheoldred/Vivi/Vito were requires-free
and kept their scores to the decimal.

## The sweep (corrected numbers)

- **420** owned commander candidates (Legendary Creature front face or "can be your
  commander" text, banlist-filtered). 391 NEW candidates brewed and scored at 2 000
  trials.
- **97 / 391** candidates anchor at least one **fully-owned, requires-free** CSB combo;
  52 anchor five or more; 19 carry template-gated variants (tracked separately).
- House rules enforced *inside* the brew: ≤3 Game Changers (commander counted), mass land
  denial excluded outright, ≤1 extra-turn card, combos producing turns skipped.
- CSB fetches are cached (`csb_variants_cache.json`, the repo's first CSB cache).
  Unpaced fetching burned 310/391 requests on HTTP 429; `_csb_get` paces (0.8 s gap)
  and honours Retry-After — the paced re-runs had zero failures.

## Leaderboard (top 15 of 391, corrected)

| # | Commander | CI | SCREEN | Owned combos | Asm@T10 | Keep% | Dead turns |
|--:|---|---|--:|--:|--:|--:|--:|
| 1 | Endrek Sahr, Master Breeder | B | 93.3 | 4 | 42.6% | 99.5 | 0.87 |
| 2 | Sheoldred, the Apocalypse | B | 92.3 | 7 | 29.1% | 99.2 | 0.98 |
| 3 | Vivi Ornitier | RU | 91.1 | 3 | 40.5% | 99.5 | 0.84 |
| 4 | Long Feng, Grand Secretariat | BG | 87.4 | 11 | 29.1% | 99.2 | 0.91 |
| 5 | Vito, Thorn of the Dusk Rose | B | 87.3 | 2 | 40.8% | 99.5 | 0.93 |
| 6 | Avatar Aang // Aang, Master of Elements | 5C | 84.8 | 2 | 27.2% | 99.1 | 0.95 |
| 7 | Alania, Divergent Storm | RU | 83.8 | 4 | 16.4% | 99.2 | 0.45 |
| 8 | Niv-Mizzet, Parun | RU | 82.9 | 3 | 16.9% | 99.4 | 0.29 |
| 9 | Mazirek, Kraul Death Priest | BG | 82.8 | 9 | 16.1% | 99.2 | 0.97 |
| 10 | Yahenni, Undying Partisan | B | 82.4 | 79 | 16.5% | 99.5 | 0.87 |
| 11 | Neheb, the Eternal | R | 82.1 | 1 | 28.2% | 99.2 | 1.10 |
| 12 | Mikaeus, the Unhallowed | B | 81.4 | 35 | 16.4% | 99.2 | 1.35 |
| 13 | The Necrobloom | BGW | 80.3 | 19 | 15.1% | 99.6 | 1.07 |
| 14 | Brago, King Eternal | UW | 79.6 | 9 | 17.1% | 99.0 | 1.07 |
| 15 | Quina, Qu Gourmet | G | 79.4 | 24 | 11.2% | 99.2 | 0.91 |

Commander text of the (pre-correction) top 8 verified against the bulk before writing
(read-the-card rule); brewed lists for the corrected 15 are in `analysis/autobrew/lists/`.

## Spotlights (text-verified)

- **Endrek Sahr, Master Breeder (#1, mono-B)** — {4}{B} Human Wizard: every creature
  spell breeds MV-worth of Thrull tokens (he sacrifices himself at 7+ Thrulls — a real
  tension the screen does not model). Best assembly screen of the field (42.6% @T10):
  requires-free 2-piece packages (Phyrexian/Ashnod's Altar cluster + Gray Merchant)
  inside mono-B tutor density.
- **Sheoldred, the Apocalypse (#2, mono-B)** — the draw-punisher shell: Peer into the
  Abyss one-shot plus Top/Citadel/Necropotence engines (2 GCs, cap respected). The
  seeded package includes **K'rrik** — see the contention warning.
- **Vivi Ornitier (#3, RU)** — {0}: add X U/R mana off his power + noncreature-spell
  ping; genuine owned packages (Deadeye Navigator / Marvin / Nim Deathmantle +
  Ashnod's). A spellslinger combo shell in colours the roster barely uses.
- **Vito, Thorn of the Dusk Rose (#5, mono-B)** — the leanest genuine kill of the
  field: **commander + one card** (Exquisite Blood; Bloodthirsty Conqueror is a true
  redundant copy) is a closed, requires-free loop. Command-zone access to half the
  combo, owned redundancy on the other half.
- **Mikaeus, the Unhallowed (#12, mono-B)** — 35 genuine owned combos (Walking
  Ballista / Yawgmoth, Thran Physician / altars + undying) — the classic engine, all
  pieces owned. Ranked mid-board only because the packages are 3-piece (weaker assembly
  screen); as a raw "this deck already exists in the collection" signal he is top-5.
- **The altar cluster (Long Feng #4, Mazirek #9, Yahenni #10, Mikaeus #12)** — the
  same owned aristocrats core (Ashnod's Altar, Phyrexian Altar, Viscera Seer, Carrion
  Feeder…) wearing different commanders. The sweep independently rediscovered the
  mono-B/x aristocrats space the hand-written Deficit Spending proposal (K'rrik) just
  picked — corroboration for the archetype, and a queue: **one** of these can exist
  physically at a time.
- **Combo-density outliers** — Ashaya, Soul of the Wild (94), Kodama of the East Tree
  (87), Yahenni (79), Peregrin Took (67), Mikaeus (35); Yahenni is also 445 combos one
  card away. The composite ranks most of them mid-table (bigger packages), but they are
  the strongest "the collection already contains this deck" signals.
- **Gev, Scaled Scorch (rank 295 after correction)** — all 8 variants persist-gated;
  we own no BR persist creature. He is however a *one-cheap-card unlock*: Murderous
  Redcap (his top one-away, 7.5k decks) is both the persist body and the damage payoff,
  turning every owned outlet into a kill. Price unverified.

## Contention warning (do NOT skip at graduation)

The top packages lean heavily on cards **physically deployed in active decks** — the
altar cluster overlaps Zero-Sum Game and Forced Liquidation card-for-card, and the
Sheoldred package wants K'rrik while the Deficit Spending proposal wants him as its
commander. The brewer screens against the *whole* collection by design (ownership, not
availability). Any graduation must run `availability_check.py` first, per the hard rule.

## Instrument notes / known biases

1. **Template requirements are excluded from "complete" (strict).** Some templates are
   trivially fillable from the pool ("Free Sacrifice Outlet" — we own eight); resolving
   that honestly needs a template→cards engine (future work). Until then gated combos
   under-count real buildability, never over-count it.
2. **Keepable% saturates** (template builds all land ~99%) — it only flags broken
   manabases; the differentiating axes are assembly, flow, and combo depth.
3. **Quota-fill vs scorer mismatch**: the brew fills ramp/draw quotas from Scryfall otags,
   but the scorer counts the stricter framework_bakeoff tagger (Long Feng: 12 filled by
   otag, 4 counted). Conservative direction, consistent across all decks.
4. **The combo axis is deliberately heavy** (35/100): this pod's bar is a proven kill
   package (kill-shape lens), so value decks with no owned combo cap at ~65.
5. **No partner/background pairing** (v1) — partner pairs like Krark+Sakashima are
   invisible; Krark solo has exactly 1 CSB variant (probe-confirmed real).
6. **Theme heuristics are coarse** (curated trigger→tag table + tribal-mention check).
   Good enough to fill a screen 99; not a substitute for reading the 99.
7. **CSB popularity/variants shift** — the cache is dated 2026-07-15; refresh with
   `--refresh-combos` when re-running months later.

## Suggested graduations (user's call)

1. **Vito, Thorn of the Dusk Rose** — cheapest vet: genuine 2-card closed loop with
   command-zone access and owned redundancy; mono-B grind shell that dodges the pod's
   counterspell profile the same way Zero-Sum does. Check Exquisite Blood / Conqueror
   contention first.
2. **Endrek Sahr** — best assembly screen of the field; but same pool as Deficit
   Spending — treat as a *competitor* to K'rrik for the mono-B aristocrats seat.
3. **Vivi Ornitier** — the non-overlap option: RU spellslinger combo, colours and
   cards the roster and the other proposals barely touch.
4. **Mikaeus, the Unhallowed** — deepest genuine combo well (35); worth a look purely
   for redundancy-of-kill, if the 3-piece assembly reality checks out in a lab.

Next instrument steps (only if the screen earns trust at graduation): template→cards
resolution for gated combos, otag-vs-fb-tagger quota alignment, partner pairing, and a
`--free-pool` mode that nets out deployed cards.
