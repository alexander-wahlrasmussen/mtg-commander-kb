# Build & Swap Tracker

*Created 2026-06-14. One place to track the active build order (Hashaton + Kefka) and every
standing upgrade swap, with sourcing for each card.*

This is a **working dashboard**, not a reference doc — it will go stale as cards are bought and
lists are sleeved. Ground truth always remains the dated `.txt` decklists. Prices are **unverified**
(per [[feedback_verify_prices]]) unless a Cardmarket date is given — confirm before buying.

## How sourcing was checked

- Ownership + cross-deck deployment: `python scripts/availability_check.py <list> --csv collection/moxfield_haves_2026-06-07-1031Z.csv` (run 2026-06-14).
- GC counts: cross-checked against `reference/REF_Game_Changers_List.md` (52-card list, current 2026-02-09).
- Swap-add ownership spot-checked directly against the Moxfield CSV.

**Status legend**

| Tag | Meaning |
|---|---|
| 🟢 **$0 / own** | Doable with cards you already have — real copies, surplus staples, or proxies already in the pool |
| 🟡 **small buy** | Minor spend (≲ €20 of cheap singletons) |
| 🔴 **major buy / raid** | Significant spend and/or strips cards out of active decks |
| 🔒 **pod approval** | Needs Rule-0 sign-off before sleeving (2-card combo / bracket-4-in-spirit) |

---

## TL;DR — "what can I do with cards I already own?"

Ranked from free-and-now to expensive:

1. 🟢 **Radiation Sickness GC-fix** — **do this first.** It's *mandatory* (the deck is currently illegal at 4 GCs) and it's **$0, no approval needed.** Cut Survival of the Fittest; add Sylvan Library + Hedron Crab (both owned real) + Sidisi (proxy in pool).
2. 🟢🟡 **Grand Design upgrade** — almost entirely owned spares; only **~€5–10** of new cards (Wood Elves, Rune-Scarred Demon). No approval needed.
3. 🟢🔒 **Diminishing Returns Stage 1** — **$0** (Nim Deathmantle + Grave Titan + Grim Tutor + Jet Medallion all owned, undeployed) but **needs pod approval** for the combo.
4. 🟡🔒 **Exile's Return** (Drannith owned + 1× Kiki ~€10–15) and **Replication Crisis** (2nd Kiki ~€10–15) — small buys, both need approval.
5. 🟢 **Calamity Tax grind-fortress upgrade** — **$0, all owned, no approval** (it dropped the Thoracle/combo direction — §5). Another free win.
6. 🔴🔒 **The two builds (Hashaton, Kefka)** — neither is buildable from free cards; each needs ~24–37 acquired cards and raids your black decks. See §1.

**Headline:** the *swaps* — and now the Calamity grind upgrade — are where the free wins are; the
two *builds* are where the money and the deck-cannibalisation are. The Hashaton/Calamity Thoracle
redundancy is **resolved** (Calamity went grind — §5).

---

## 1. The two builds

Both are 3/3 GC-legal (verified). Both pull heavily from your existing **black decks** — The Dark
Lord's Army (Sauron), Crystal Sickness, Curse of the Scarab, Calamity Tax — so building them
*and* keeping those decks intact means buying duplicates of the shared pieces.

### 1a. Hashaton, Scarab's Fist — *Thassa's Oracle combo* 🔴🔒
- **List:** `decks/considering/hashaton-thoracle-20260614.txt` · **Clock:** T6 decap = table (lab `hsh_clock_lab.py`) · **GCs:** 3/3 (Thassa's Oracle, Demonic Tutor, Vampiric Tutor)
- **Wincon:** discard/deploy Thassa's Oracle → Demonic Consultation / Tainted Pact empties library → ETB win. Hashaton is the tutor/dig/resilience engine.
- **Sourcing (availability sweep, 100 cards):** **9 free** · 27 unowned · 10 proxy-only · 54 owned-but-deployed (most are surplus staples = effectively free; the scarce ones below are the real cost).
- **Must acquire — the combo + key spells:** Thassa's Oracle, Demonic Consultation, Tainted Pact, Jace Wielder of Mysteries, Beseech the Mirror, Spellseeker, Putrid Imp, Tireless Tribe, Skirge Familiar, Ghostly Pilferer, Astral Dragon, Wishclaw Talisman, Scheming Symmetry, Painful Truths, Cut Down, Fatal Push, Prismatic Ending, Supreme Verdict, Silence, Shark Typhoon, Flusterstorm.
- **Must acquire — the manabase is the budget-killer:** **Tundra, Scrubland, Mana Confluence** (unowned; Tundra/Scrubland are reserved-list ≈ €200–400 each), plus Darkslick Shores, Castle Locthwain. **Underground Sea** is owned (×2) but both copies are in Calamity Tax + Crystal Sickness.
- **Scarce shared singletons it raids:** Mana Drain, Dauthi Voidwalker, Vampiric Tutor, Demonic Tutor (all owned but fully committed to other decks — buy or pull).
- **Reality:** *Not priced yet, but this is the most expensive option by far if bought in paper.* The realistic path is **proxy the cEDH manabase** (Tundra/Scrubland/Underground Sea) and buy the cheap combo/dig pieces.
- **Gate:** 🔒 pod approval of Thassa's Oracle + Consultation (the high-stigma combo).

### 1b. Kefka, Court Mage — *Forced Liquidation (wheel-burn)* 🔴
- **List:** `decks/considering/forced-liquidation-20260612.txt` · **Clock:** T8 decap / T9 table (lab) · **GCs:** 3/3 (Notion Thief, Demonic Tutor, Mana Vault) · **Commander owned (free).**
- **Wincon:** wheel (draw 7s) + static punishers (Sheoldred / Underworld Dreams / Fate Unraveler / Psychosis Crawler / Niv-Mizzet). Resolves on *your* turn through *statics* → **the one kill that ignores Grand Abolisher → no pod approval needed.**
- **Sourcing (sweep, 80 cards):** **10 free** · 24 unowned · 7 proxy-only · 39 owned-deployed (manabase, rocks, protection, Notion Thief, Psychosis Crawler are free/surplus).
- **Must acquire — premium wheels:** Wheel of Fortune, Echo of Eons, Time Spiral, Memory Jar, Reforge the Soul, Dark Deal.
- **Must acquire — punishers:** Fate Unraveler, Niv-Mizzet Parun, Megrim, Liliana's Caress, Ob Nixilis the Hate-Twisted, Kederekt Parasite, Glint-Horn Buccaneer, Bloodletter of Aclazotz; (Underworld Dreams owned proxy-only).
- **Must acquire — rest:** Cursed Totem, Waste Not, Diabolic Tutor, Mastermind's Acquisition, Bedevil, Terminate, Infernal Grasp, Bloodchief's Thirst, Rakdos Charm, Negate.
- **Scarce shared singleton:** **Sheoldred, the Apocalypse** (own 1, in The Dark Lord's Army) — buy a copy for Kefka or pull from Sauron.
- **Estimate:** ~€140–190 (bake-off) / ~$85–140 (proposal) — both **unverified**, both pre-date the availability sweep. The wheels (Wheel of Fortune / Echo of Eons / Time Spiral / Memory Jar) are the bulk of the spend.
- **Gate:** none. This is the deck you can build without asking the pod.

---

## 2. Recommended swaps (per deck)

| Deck | Out → In | Source of the "In" cards | Cost | Gate | Status |
|---|---|---|---|---|---|
| **Radiation Sickness** ⚠️ | −Survival of the Fittest (GC) **+**Sylvan Library; −Generous Patron +Hedron Crab; −Guardian Project +Sidisi, Brood Tyrant | Sylvan Library (own ×2 real) · Hedron Crab (own ×2 real) · Sidisi (**proxy-only** — play proxy or buy ~€2) — all ex-Loam | 🟢 **$0** | none | **Mandatory** (fixes 4-GC illegal → 3/3). Not yet applied. |
| **The Grand Design** | 7-for-7 (see proposal). Adds: Solemn Simulacrum, Sakura-Tribe Elder, Wood Elves, Faeburrow Elder, Coalition Relic, **Craterhoof Behemoth**, Rune-Scarred Demon | Solemn/Sakura/Coalition/Craterhoof = owned spares (real); Faeburrow = ex-Peace Offering (own 1); **Wood Elves + Rune-Scarred = buy** | 🟡 **~€5–10** | none | Proposal only. No new combo → no approval. |
| **Diminishing Returns** | Staged toward B4. **Stage 1:** +Nim Deathmantle +Grave Titan +Grim Tutor (+Jet Medallion) −Mother of Runes −Skrelv −Giver of Runes | All Stage-1 adds owned + undeployed (Deathmantle ×1, Grave Titan ×3, Grim Tutor ×1, Jet Medallion ×1) | 🟢 **$0** (Stage 1) | 🔒 yes | Proposal only. Later stages cost money (see below). |
| **The Exile's Return** | +Kiki-Jiki +Drannith Magistrate −Night's Whisper −Light Up the Stage | Drannith (own 1, undeployed) free; **Kiki-Jiki = buy** | 🟡 **~€10–15** | 🔒 yes | Proposal only. (Avatar's Wrath is NOT a cut — re-verified.) |
| **Replication Crisis** | +Kiki-Jiki −Bident of Thassa | **Kiki-Jiki = buy a dedicated 2nd** (so it runs independently of Exile's Return) | 🟡 **~€10–15** | 🔒 yes | Proposal only. |
| **The Calamity Tax** | **Grind-fortress upgrade** (`glarb-grind-fortress-20260614.txt`): −6 weak +Bloom Tender +Birds +Delighted Halfling +Crucible +Life from the Loam +Lier | **All 6 owned ($0)** — Loam pile + spares | 🟢 **$0** | none | Thoracle/Isochron dropped (combo unreliable here — lab 2026-06-14). Grind T9. Aspirational = Strong Glarb. See `analysis/Calamity_Grind_Fortress_2026-06-14.md`. |

**Diminishing Returns later stages** (all need the same pod approval as Stage 1):
- Stage 2 — 🟡 +Leonin Relic-Warder (buy ~€1–5, the most efficient combo card) +Wishclaw Talisman (optional, buy).
- Stage 3 — 🔴 +Exquisite Blood (€20–23, Cardmarket 2026-06-10) +Vito (~€9–13). Defensible to skip.
- ~~Stage 4 — GC reallocation (+Demonic Tutor +Vampiric Tutor)~~ — **dropped 2026-06-14 (user: not worth it).** Bonus: removes DR from the Demonic/Vampiric Tutor contention in §4.

---

## 3. Consolidated shopping list (the actual buys)

Grouped by what they unlock. Quantities matter where a card is wanted by more than one plan (§4).

**Cheap, high-value, unlock free swaps:**
- Wood Elves ×1, Rune-Scarred Demon ×1 → Grand Design (~€5–10 total)
- Leonin Relic-Warder ×1 → Diminishing Returns Stage 2 (~€1–5)
- Kiki-Jiki, Mirror Breaker **×2** → Exile's Return + Replication Crisis (~€20–30 total)
- *(optional)* Sidisi, Brood Tyrant ×1 if you want a real copy for Radiation Sickness (~€2) — else play the proxy

**Kefka — the wheel-burn deck (~€140–190, unverified):**
- Wheels: Wheel of Fortune, Echo of Eons, Time Spiral, Memory Jar, Reforge the Soul, Dark Deal
- Punishers: Fate Unraveler, Niv-Mizzet Parun, Megrim, Liliana's Caress, Ob Nixilis the Hate-Twisted, Kederekt Parasite, Glint-Horn Buccaneer, Bloodletter of Aclazotz
- Support: Cursed Totem, Waste Not, Diabolic Tutor, Mastermind's Acquisition, Bedevil, Terminate, Infernal Grasp, Bloodchief's Thirst, Rakdos Charm, Negate
- Contested: **Sheoldred** (buy 1 or pull from Sauron); Underworld Dreams (own proxy only)

**Hashaton — the Thoracle deck (not priced; proxy the manabase):**
- Combo + dig: Thassa's Oracle, Demonic Consultation, Tainted Pact, Jace Wielder of Mysteries, Beseech the Mirror, Spellseeker, Putrid Imp, Tireless Tribe, Skirge Familiar, Ghostly Pilferer, Astral Dragon, Wishclaw Talisman, Scheming Symmetry
- Interaction: Painful Truths, Cut Down, Fatal Push, Prismatic Ending, Supreme Verdict, Silence, Shark Typhoon, Flusterstorm
- Manabase (**proxy-recommended** — reserved-list): Tundra, Scrubland, Mana Confluence, Darkslick Shores, Castle Locthwain
- Contested: Mana Drain, Dauthi Voidwalker, Demonic Tutor, Vampiric Tutor, Underground Sea

---

## 4. Cross-deck contention — don't double-spend the same card

These cards are wanted by **more than one** plan. Owning one copy ≠ enough.

| Card | Wanted by | Owned (free) | Action |
|---|---|---|---|
| **Thassa's Oracle** | Hashaton (only) | 0 | Buy 1 for Hashaton (Calamity dropped Thoracle — §5) |
| **Demonic Consultation** | Hashaton (only) | 0 | Buy 1 for Hashaton |
| **Demonic Tutor** (GC) | Hashaton + Kefka | 3, all deployed | Buy 1–2 more, or free one by dismantling a black deck |
| **Vampiric Tutor** (GC) | Hashaton (only; aspirational Strong-Glarb also wants it) | 1, over-committed | Buy 1 for Hashaton |
| **Sheoldred, the Apocalypse** | Kefka + Dark Lord's Army (deployed) | 1 (in Sauron) | Buy 1 for Kefka, or pull from Sauron |
| **Kiki-Jiki, Mirror Breaker** | Exile's Return + Replication Crisis | 0 | Buy **2** (decision already made: run independently) |
| **Grim Tutor** | Hashaton + DR-Stage 1 | 1 | Only one gets the free copy → buy a 2nd (~€ cheap) for the other |
| **Final Parting** | Grand Design (Calamity's old reanimator claim is **retired**) | 1 (ex-Loam) | Free for GD now — contention resolved |
| **Dauthi Voidwalker** | Hashaton + Dark Lord's Army (deployed) | 1 (in Sauron) | Buy or pull |

**Donor decks getting raided:** The Dark Lord's Army (Sauron) is hit by *both* builds (Sheoldred,
Underworld Dreams, Dauthi). Crystal Sickness / Curse of the Scarab / Calamity Tax supply the
shared Dimir manabase + tutors. If you want those decks to stay playable, the shared pieces become
buys, not pulls.

---

## 4b. Does dismantling existing decks unlock the builds? — mostly *no*

Tested with `availability_check.py --exclude-deck` (simulates a teardown), run 2026-06-14:

| Scenario | Hashaton (free / unowned) | Kefka (free / unowned) |
|---|---|---|
| Dismantle nothing | 9 / 27 | 10 / 24 |
| Dismantle Dark Lord's Army only | 10 / 27 | 11 / 24 |
| Dismantle the whole black/Grixis cluster (4 decks) | 15 / 27 | 13 / 24 |

**The `unowned` count never moves** — no teardown creates a card you don't own. The ~24–27
must-buys per deck (the combo, the premium wheels, the reserved-list duals) are buy-gated, full
stop. Even dismantling *four* decks frees only a handful of cards, because most shared cards are
either high-count surplus staples (already effectively free) or sit in several decks at once.

**What dismantling actually buys you** is a few *premium owned singletons*, so you skip a
duplicate-buy or avoid gutting a deck you'd keep:
- **Dark Lord's Army (Sauron)** → **Sheoldred** for Kefka (its #1 most-wanted owned card) + Dauthi Voidwalker for Hashaton. Highest-overlap donor for *both* builds and thematically closest (black drain/punisher ≈ Kefka; black tutors ≈ Hashaton).
- The Dimir decks (Crystal Sickness / Curse of the Scarab / Calamity) → an Underground Sea, a Mana Drain, a Demonic Tutor for Hashaton.

**Verdict:** dismantle for *roster* reasons (you're adding two more black decks to an already
black-heavy roster), not as a cost hack — it won't make either build cheap. If you tear down one,
**Sauron is the highest-value teardown** for this build order.

---

## 5. ✅ Resolved: Calamity is the grind pillar (not a Thoracle deck)

**Resolved 2026-06-14.** Calamity Tax drops the Thoracle direction entirely and becomes a **grind /
inevitability fortress** — its natural identity (Glarb casts MV4+ bombs off the top). A non-Thoracle
Isochron Scepter + Dramatic Reversal combo was tested and **rejected** (unreliable in this shell —
36% by T14; the deck can't tutor a non-creature combo and the GC cap blocks the blue tutors; lab
`glarb_iso_clock_lab.py`). So **Hashaton is now the sole Thassa's Oracle deck** — no duplicated
wincon, no doubled combo buys, no shared approval.

- **Now ($0, no approval):** the grind-fortress upgrade in §2 — 6 owned adds, grind T9.
- **Aspirational (work toward):** migrate toward the Strong-Glarb external — Tier 1 Nyxbloom
  Ancient + Uro; Tier 2 Sphinx of the Second Sun + Beledros + Wilderness Reclamation; Tier 3 flash
  package (Leyline owned-proxy + Tidal Barracuda) + Spelunking; then a GC reconfig (Crop Rotation
  owned + Field of the Dead owned-proxy + Vampiric Tutor buy). See `analysis/Calamity_Grind_Fortress_2026-06-14.md`.

---

## 6. Pod approvals outstanding

Everything combo-flavoured needs Rule-0 sign-off. There are two *classes*:

- **Thassa's Oracle / Consultation (high stigma):** Hashaton, Calamity-hybrid. The "win out of nowhere, deck yourself" combo the pod is most likely to push back on.
- **Standard 2-card infinites:** Exile's Return (Kiki+Felidar), Replication Crisis (Kiki+Conscripts/Resto), Diminishing Returns (Deathmantle+Titan, LRW+aura).

Kefka needs **none** — that's its whole pitch.

These are now the 5th–7th per-deck approval requests. The standing suggestion (multiple memories)
is to **ask once for a blanket policy and codify the exception in `REF_Bracket_3_House_Rules.md`**
rather than tracking per-deck. Worth doing in the same pod conversation.

---

## 7. Parked / out of scope for this build order

- **Berta, Wise Extrapolator** — candidate **falsified** (clock median never-in-12; GU tutor poverty + 3-GC cap). Not recommended; lists kept for the record only.
- **Najeela, the Blade-Blossom** — candidate, ceiling 18–19/20, median T10 (reliable combo, not a T6–7 racer). A *new from-scratch 5C deck*, not a swap. Stronger than Berta if you ever want a new build slot.
- **The Wandering Minstrel** — candidate, ceiling 17–18/20, parked.
- **Calamity reanimator-pivot / oppression swaps** — retired, superseded by the hybrid (in `archive/proposals/`).

---

## 8. Suggested order of operations

1. **Now, free, no approval:** apply the **Radiation Sickness** GC-fix (mandatory — the deck is illegal until you do). Then the **Grand Design** upgrade (buy only Wood Elves + Rune-Scarred ≈ €5–10).
2. **Resolve §5:** decide Hashaton vs Calamity-hybrid (vs both). This sets the whole Thoracle shopping bill.
3. **One pod conversation:** ask for the Thoracle approval (for the deck chosen in step 2) *and* the standard 2-card infinites (Kiki ×2 decks, DR), and propose codifying the blanket exception.
4. **After approval, free:** apply **Diminishing Returns Stage 1** ($0).
5. **Small buys after approval:** Kiki ×2 → Exile's Return + Replication Crisis.
6. **Big builds:** **Kefka** (no approval — can start any time; spend is the wheels) and the chosen **Thoracle deck** (Hashaton or Calamity-hybrid). Proxy the reserved-list manabase.

---

*Maintenance: when a swap is sleeved, bump the deck's dated `.txt`, archive the old list, update its
Summary, and strike the row here. When the Thoracle decision (§5) is made, delete the losing option
from §1/§3/§4.*
