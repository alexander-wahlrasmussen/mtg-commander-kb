# Calamity Tax (Glarb) — Grind Fortress + Isochron lab + Strong-Glarb aspirational target (2026-06-14)

**Supersedes the Thoracle-hybrid direction** in `proposals/Calamity_Tax_Direction_Glarb_Lists_2026-06-13.md`.
Context shift: with **Hashaton** now the roster's Thassa's Oracle deck and **Kefka** the
Abolisher answer, Calamity no longer needs to race the pod — it's freed to be the **grind /
inevitability pillar** nothing else covers. User chose: a $0 owned grind upgrade now + the
Strong-Glarb external as an aspirational build to work toward.

Glarb, Calamity's Augur (card_lookup 2026-06-14): {B}{G}{U} 2/4 deathtouch; look at top any
time; **play lands + cast MV4+ spells from the top**; {T}: surveil 2. → a value/inevitability
engine that wants high-impact MV4+ bombs, NOT a 2-card combo (combos ignore him).

---

## DECISION: build the grind fortress (`decks/considering/glarb-grind-fortress-20260614.txt`)

6-for-6 vs deployed V1 (`calamity-tax-20260405-061741.txt`), **all adds owned = $0**, stays
**3/3 GC** (Demonic Tutor, Fierce Guardianship, Seedborn Muse — no add is a GC):

| Out (prior-lab-vetted weakest 6) | In (owned grind/ramp/value) | Role |
|---|---|---|
| Druid of Purification | **Bloom Tender** | BGU dork — ramp + fixing (3 mana with Glarb out) |
| Flash Photography | **Birds of Paradise** | T1 dork / fixing |
| High Fae Trickster | **Delighted Halfling** | dork that also makes Glarb **uncounterable** |
| Mirrorform | **Crucible of Worlds** | recur fetches → Coffers fuel + anti-flood; Glarb plays them from yard too |
| Savvy Trader | **Life from the Loam** | land card-advantage engine (dredge) |
| Starfield Vocalist | **Lier, Disciple of the Drowned** | flashback all your I/S (recast Torment/removal/ramp) + **your spells can't be countered** |

All card text verified via `card_lookup.py` 2026-06-14.

### Clock (`scripts/glarb_iso_clock_lab.py`, grind via ct_speed_lab engine, 20k/seed 20260614)

| Build | decap | table |
|---|:--:|:--:|
| V1 committed | T9 | T10 |
| **Grind fortress** | **T9** | **T9** |

decap cum (fortress): 16% T7 / 38% T8 / 62% T9 / 80% T10. The grind is **preserved and a hair
smoother** — but the median is mana-gated (creature-count-independent X-drain), so the real wins
are **off-clock** and the goldfish can't score them: Crucible/Life from the Loam = card advantage
and anti-flood; Lier = recursion + counter-immunity for the kill; Delighted Halfling = commander
protection. Same framework result as the RS/GD upgrade passes (adds move the distribution / the
unmeasured axes, not the median).

---

## Why NOT the Isochron combo (tested, rejected)

Tested a non-Thoracle **Isochron Scepter + Dramatic Reversal → infinite mana → Torment** combo
on `decks/considering/glarb-grind-iso-20260614.txt` (`glarb_iso_clock_lab.py` combo model):
**combo assembles only 36% by T14, median never (64% never-in-14).** Diagnosis — the combo can't
be supported in this shell:

- **No creature-tutors apply** — Glarb's GSZ/Chord/Finale fetch creatures; Isochron (artifact) +
  Dramatic (instant) get none.
- **GC cap locks out the blue tutors** — Vampiric/Mystical Tutor would find the pieces but both
  are GCs (deck is at 3/3).
- **Glarb can't dig for them** — he top-casts MV4+; both pieces are MV2.

One tutor (Demonic) + surveil to assemble two specific cards ≈ 36%. The Thoracle combo worked
*because Thoracle is a creature with five tutors* — exactly why Hashaton keeps it and Calamity
can't replicate it. Verdict: not worth 2 slots + a pod-approval ask for a 1-in-3 backup that
Hashaton/Kefka already cover better. **Dropped.** (Build file + lab retained as the evidence.)

---

## Aspirational target: the Strong-Glarb external (`glarb-strong-ext-20260613.txt`)

Same grind DNA, pushed harder: premium ramp payoffs + a flash/value package + a different GC
config. The delta over the grind fortress = the "work toward" list:

**Tier 1 — premium ramp (biggest impact):**
- **Nyxbloom Ancient** (buy) — *triples* your mana; absurd with Cabal Coffers. The single best upgrade.
- **Uro, Titan of Nature's Wrath** (buy) — ramp + lifegain + draw + recurring escape body.

**Tier 2 — big-mana value engines:**
- **Sphinx of the Second Sun** (buy) — extra upkeep = double Glarb surveils + double draws.
- **Beledros Witherbloom** (buy) — untap all lands (pay life) = a 2nd big-mana turn + tokens.
- **Wilderness Reclamation** (buy) — untap all lands at end step → hold up a huge flash turn.

**Tier 3 — flash/tempo package + extras:**
- **Leyline of Anticipation** (owned proxy) + **Tidal Barracuda** (buy) — flash everything; Barracuda taxes opponents' instant-speed.
- **Spelunking** (buy) — lands enter untapped + extra land drop.

**GC reconfiguration (changes the deck's GC identity — a decision, not a free add):** Strong Glarb
runs **Crop Rotation** (owned ×1) + **Field of the Dead** (owned proxy) + **Vampiric Tutor** (buy)
as its 3 GCs vs our Demonic/Fierce/Seedborn. Adopting them = swapping GC slots, and Strong Glarb
also trades V1's counter/reanimator package for more proactive ramp (lighter on Mana Drain/Pact/
Reanimate/Kokusho). The aspirational build is therefore a *gradual* migration: slot the premium
ramp as you acquire it, then decide on the GC/interaction rebalance.

**Owned already (can slot now, $0):** Crop Rotation (real ×1, GC), Delighted Halfling, Lier (both
in the fortress build). **Owned as proxy:** Field of the Dead, Leyline of Anticipation, Titania.
**Buys:** Nyxbloom Ancient, Uro, Sphinx of the Second Sun, Beledros Witherbloom, Wilderness
Reclamation, Tidal Barracuda, Spelunking, Vampiric Tutor.

---

## Status

- **Grind fortress = the chosen build.** $0 (all owned), no pod approval (no combo). Deployed
  `.txt` stays V1 until sleeved; to apply, bump to a dated roster filename, archive V1, update the
  Summary's decklist + Bracket-3 sections (still 3/3 GC), carry `Clock: T9 decap / T9 table (lab
  2026-06-14)`.
- Isochron combo build + lab retained as evidence (`glarb-grind-iso-20260614.txt`,
  `glarb_iso_clock_lab.py`).
- Strong Glarb = aspirational; acquire Tier 1→3 over time, then revisit the GC/interaction balance.
