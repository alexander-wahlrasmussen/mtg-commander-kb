# Glarb, Calamity's Augur — Pack Pull Swaps (2026-06-01)

> **RETIRED 2026-06-13.** Superseded by the chosen rebuild — the Thoracle-combo **Hybrid**
> (`proposals/Calamity_Tax_Direction_Glarb_Lists_2026-06-13.md`). Also stale: Witherbloom is now
> Zero-Sum Game's commander, so the 99-route here isn't available. Kept for history.

**Deck:** The Calamity Tax (`calamity-tax-20260405-061741.txt`)
**Trigger:** 2026-06-01 pack pull — user opened Witherbloom, the Balancer + Professor Dellian Fel and asked whether they belong in Calamity Tax 99s versus building a new deck around Witherbloom. Companion to `proposals/PROP_Witherbloom_the_Balancer.md`.
**Status:** Decision deferred. Both this swap path AND the standalone Witherbloom build documented in parallel.
**Relationship to 2026-05-31 swaps:** This is an *additive* layer. The 5 oppressive/speed swaps in `The_Calamity_Tax_Swaps_2026-05-31.md` still apply. This doc adds 2 more (Witherbloom + Dellian Fel) and identifies the cuts they would require beyond the planned 5.

---

## Card text (verified 2026-06-01 post-Scryfall-refresh)

### Witherbloom, the Balancer — `{6}{B}{G}` (8 MV), 5/5 Elder Dragon, BG
- Affinity for creatures *(this spell costs {1} less to cast for each creature you control)*
- Flying, deathtouch
- **Instant and sorcery spells you cast have affinity for creatures.**

### Professor Dellian Fel — `{2}{B}{G}` (4 MV), Legendary Planeswalker — Dellian, BG
- +2: You gain 3 life.
- 0: You draw a card and lose 1 life.
- −3: Destroy target creature.
- −6: Emblem — *Whenever you gain life, target opponent loses that much life.*
- **Cannot be commander** (no enabling text on the card).

Both BG, both fit Sultai. Both owned (1 each from the pack pull).

---

## Why these two cards specifically fit Calamity Tax

The deck's primary kill is **X-spell drain** (Torment of Hailfire), with copy effects as secondary kills (kicked Rite of Replication, Doppelgang, Mirrorform, Espers to Magicite). Witherbloom's `Instant and sorcery spells you cast have affinity for creatures` clause is a *global* generic-cost reduction on every one of those kills.

**With Witherbloom in play + 12 creatures on board (achievable mid-game in this deck):**

| Spell | Native cost | With affinity |
|---|---|---|
| Torment of Hailfire X=20 | `{20}{B}{B}` = 22 mana | ~`{2}{B}{B}` (affinity reduces by 12, X itself reduces from 20 to whatever you can pay) — net ~4 mana for X=20 |
| Exsanguinate X=20 | 22 mana | ~4 mana |
| Doppelgang X=4 | `{4}{4}{4}{G}{U}` = 14 mana | `{G}{U}` |
| Rite of Replication (kicked) | `{7}{U}{U}` = 9 mana | `{U}{U}` |
| Mirrorform | `{4}{U}{U}` | `{U}{U}` |
| Espers to Magicite | `{3}{B}` | `{B}` |
| Flash Photography (if kept) | `{4}` | free with 4+ creatures |
| Reanimate, Noxious Revival | unchanged (no generic) | — |
| Mana Drain, Force of Negation | mostly unchanged (colored-pip heavy) | small reduction |

Witherbloom herself is MV 8 — castable from the top via Glarb. Or skip the cast: Glarb's surveil mills her, Reanimate for `{B}` puts her into play T3–4. **The deployment line is exactly the kind Calamity Tax already runs.**

Dellian Fel doesn't have a unique synergy hook, but she's a **0-loyalty card-draw engine forever** at 4 MV — perfect for a value-grind deck. Glarb top-casts her. The +2 (gain 3 life) keeps her alive trivially while triggering Sheoldred (planned add — opponents losing life on draw) incidentally. The -6 emblem is a flavor finisher; the deck doesn't naturally fuel lifegain triggers, so the ult isn't a planned kill line.

---

## Swap plan (additive to 2026-05-31)

### Cut: Archon of Cruelty → In: Witherbloom, the Balancer

- **Archon of Cruelty (out):** 8-MV finisher with ETB drain (each opponent loses 3 life, discards, sacrifices; you draw, gain life). Powerful one-shot. Copy target for Rite of Replication kicked.
- **Witherbloom, the Balancer (in):** 8-MV global cost reducer on every I/S spell + 5/5 flying deathtouch body.
- **Why:** Witherbloom's affinity reduction applies to *every* X-spell and copy-spell turn, not just the turn she enters. Archon is good once; Witherbloom is good forever. The deck still has Kokusho as a copy target for Rite of Replication, so the "copy-finisher" axis isn't gutted.
- **Tradeoff:** lose the Archon-via-Mirrorform line (5 nonland permanents become Archons → 5 drain triggers). Witherbloom isn't a great Mirrorform target on her own (one big body), but the Mirrorform line still works on Kokusho.

### Cut: Starfield Vocalist → In: Professor Dellian Fel — **conflicts with planned Carpet of Flowers swap**

- **Starfield Vocalist (out):** already a planned cut in the 2026-05-31 swap doc (going to Carpet of Flowers).
- **Professor Dellian Fel (in):** 0-loyalty card draw forever, 4 MV.
- **Conflict:** The 2026-05-31 plan had Starfield → Carpet of Flowers (anti-blue ramp). Both Dellian Fel and Carpet can't take the same slot. **Two resolutions:**
  1. **Dellian Fel beats Carpet of Flowers for that slot** (Dellian's value is universal; Carpet is blue-meta-specific and a blank vs. non-blue tables). Skip Carpet entirely.
  2. **Keep Carpet of Flowers; find a different cut for Dellian Fel.** Candidate: Massacre Wurm (redundant with Toxic Deluge + Meathook Massacre as sweeper; not the deck's primary kill line).

**Recommended resolution: option 1.** Dellian Fel's free card every turn outvalues Carpet's anti-blue ramp on average. Carpet stays in the maybeboard as a meta-flex.

### Net deck composition under full plan (2026-05-31 + 2026-06-01)

**Total cuts: 6** — Savvy Trader, Flash Photography, Druid of Purification, High Fae Trickster, Starfield Vocalist, Archon of Cruelty
**Total adds: 6** — Exsanguinate, Sheoldred, Mystic Remora, Bloom Tender, Witherbloom (the Balancer), Professor Dellian Fel
**Dropped from 2026-05-31 plan:** Carpet of Flowers (slot taken by Dellian Fel; Carpet bumped to maybeboard)

Deck stays at 100 cards. GCs unchanged (Seedborn Muse + Fierce Guardianship + Demonic Tutor remain 3/3).

---

## Expected ceiling impact

**18/20 → 19/20** was the 2026-05-31 swap projection (5/5/4/5).

**With Witherbloom + Dellian Fel additionally: 19/20 → likely 19/20 still, but more reliably.** The Conversion Check axes don't move by a full point per axis, but each gets quietly better:

- **Core Loop (5/5):** unchanged structurally. Dellian Fel as a 0-loyalty draw engine bolsters card velocity; Witherbloom amplifies every spell's impact.
- **Kill Reliability (5/5):** Witherbloom doesn't add a new kill *line*, but she shifts the *mana threshold* for the existing lines. Torment at lethal X drops from ~14 mana to ~4 mana. This means more turns where a kill is castable from a non-optimal hand. Material improvement in practice.
- **Durability (4/5):** unchanged. Witherbloom is a 5/5 flying deathtouch body, decent against the pod's Ur-Dragon attacks. Dellian Fel is a planeswalker (fragile to creature attack but loyalty stays high via +2).
- **Interaction (5/5):** unchanged. Witherbloom's affinity also cheapens counter/removal I/S (Toxic Deluge, Force of Negation get small reductions on their generic floors).

**Why not 20?** Same cap as before — no deterministic 1-card kill; finisher pool exile-vulnerable; graveyard hate still threatens Reanimate/Lumra/Icetill. Witherbloom doesn't address those caps.

---

## What this gives up vs. the standalone Witherbloom proposal

If Witherbloom slots into Calamity Tax as a 99, she **does not** unlock the Vito + Exquisite Blood 2-card pod-approved combo from `proposals/PROP_Witherbloom_the_Balancer.md`. That combo needs:
- Commander-zone Witherbloom with always-available affinity acceleration
- Heavier creature density (Pest tokens via Beledros, Saproling tokens via Tendershoot, etc.)
- Dedicated combo pieces (Vito, Exquisite Blood, Sanguine Bond) that don't fit Calamity Tax's value plan
- Life-gain trigger density (Witherbloom Apprentice magecraft, Aetherflux Reservoir storm)

Slotting Witherbloom in Calamity Tax means **giving up the disgusting bracket-4-in-spirit identity** in exchange for a smoother existing deck. The deck goes from 18/20 → 19/20-and-better-feeling, not 18/20 → 18-19/20 with a new combo line.

---

## Open questions

1. **Which path?** Standalone Witherbloom commander deck (18–19/20 ceiling, ~€80–90 buy, Vito+Blood combo, conflicts with Pest Control) vs. Calamity Tax 99-route (modest upgrade to a 19/20 deck, zero buy, no roster fight). User call deferred per 2026-06-01 session.
2. **If 99-route:** does Dellian Fel beat Carpet of Flowers for the Starfield slot? Or do we cut Massacre Wurm and keep both?
3. **If standalone build:** Pest Control archetype overlap (BG sac-tutor-drain substrate) needs a mechanical-distinctiveness call.
4. **Mothman retirement question** is orthogonal — neither path requires it.

---

## Changelog

- **2026-06-01:** Companion swap doc created in response to user pack pull (Witherbloom, the Balancer + Professor Dellian Fel) and the deferral decision. Card text verified post-Scryfall-refresh on 2026-06-01. Linked from the standalone Witherbloom proposal. No physical changes to the deck — proposals only.
