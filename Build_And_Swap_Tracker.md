# Build & Swap Tracker

*Created 2026-06-14. One place to track the active build order and every
standing upgrade swap, with sourcing for each card.*

> **✅ STATUS UPDATE 2026-07-08 — the Kefka/Witherbloom build order is settled physically.**
> **Forced Liquidation (Kefka)** and **Zero-Sum Game (Witherbloom)** are now **physically assembled**
> (sleeved `forced-liquidation-20260707.txt` / `zero-sum-game-20260707.txt`). The 2026-06-30
> "treated as bought" marker is now real: the final cards were sourced by **dismantling Diminishing
> Returns** (10 cards → Zero-Sum, Lightning Greaves → Forced Liquidation; the rest of DR returned to the
> pool). **Diminishing Returns is retired** — so every "Diminishing Returns" swap/stage row below
> (§2, §6) is **VOID** (there is no DR to swap). The 2026-07-06 physical-build-sourcing doc that mapped
> the pulls has been deleted (its job is done). Still owed elsewhere: the Replication Crisis 2nd Imperial
> Recruiter. Next housekeeping: re-run DeckSafe against a fresh Moxfield export to refresh the snapshot.

> **⚠️ STATUS UPDATE 2026-06-27 — read before using §1/§3/§4/§5/§6.**
> The build order changed. **Thassa's Oracle is out of the roster entirely** — the user is
> building **neither Hashaton nor a Calamity-Thoracle hybrid.** The single build proceeding is
> **Forced Liquidation (Kefka)** — wheel-burn, no Thoracle, no pod approval (kills through statics).
> **2026-06-30 — treated as bought (per user direction):** Forced Liquidation, Zero-Sum Game, and
> the Lightning War upgrade are now marked **built/acquired** (consolidated buy list
> `analysis/Buy_List_ZeroSum_LightningWar_ForcedLiquidation_2026-06-25.md` — fulfilled-as-if-bought;
> physical settlement still owed where copies were contention buys). Their `.txt` builds already
> carried the cards. **Replication Crisis −Strionic +Imperial Recruiter also applied 2026-06-30**
> (`the-replication-crisis-20260630.txt`; 2nd Recruiter copy still owed).
> Croak and Dagger (ex-Calamity Tax) **REBUILT again 2026-07-01** — the grind/lands fortress was
> replaced by the **"Glarb Inevitable" topdeck-combo** (Sensei's Top → Aetherflux, T9, counter-immune):
> `decks/croak-and-dagger-20260701.txt`. Clock T13→T9, P(beat pod) ~7–8%→~30%. 8 buys ≈ €32 (+ a 2nd
> Aetherflux; Sensei's Top was owned/free). See `proposals/Glarb_Inevitable_Topdeck_Combo_2026-06-30.md`.
> **2026-07-05 — second build queued: Creative Destruction** (Hearthhull, World Shapers precon +
> Earthbend retirement) — named + approved, **held as a proposal until the precon arrives**. See §1c.
> Everything below tagged "Hashaton" / "Thassa's Oracle" / "Thoracle decision" is **superseded** — kept for record only.

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

1. ✅ **Radiation Sickness GC-fix — DONE 2026-06-15.** Was *mandatory* (illegal at 4 GCs), **$0, no approval.** Cut Survival of the Fittest; added Sylvan Library + Hedron Crab + Sidisi. Now `decks/radiation-sickness-20260622.txt`, **3/3 legal** (validate.py: 0 errors). *(Later swap 2026-06-22: −Vorinclex, Monstrous Raider +Timeless Witness — Durability/post-wrath recovery, $0 owned; the deck's last unowned card is gone, now 100% owned/proxy.)*
2. ✅ **Grand Design upgrade — DONE 2026-06-25.** 7-for-7 sleeved (owned spares + Wood Elves/Rune-Scarred bought). No approval needed. Now `decks/the-grand-design-20260623.txt`.
3. ~~**Diminishing Returns Stage 1**~~ — **VOID (deck dismantled 2026-07-08).**
4. 🟡🔒 **Exile's Return** (Drannith owned + 1× Kiki ~€10–15) — small buy, needs approval. **Replication Crisis Kiki swap DECLINED 2026-06-30** (rc_speed_lab: a 3rd infinite assembles only ~6%/T12); replaced by **−Strionic Resonator +Imperial Recruiter** — **✅ APPLIED 2026-06-30** (as-if-bought) to `the-replication-crisis-20260630.txt`; a tutor that doubles the *existing* Satya+LR line (11→22% T6 / 18→32% T12), no pod approval needed (not a new combo). **2nd Recruiter copy still owed** (owned one is in Exile's Return). See `decks/The_Replication_Crisis_Swaps_2026-06-30.md`.
5. ✅ **Croak and Dagger grind-fortress upgrade — DONE 2026-06-25.** $0, all owned, no approval (it dropped the Thoracle/combo direction — §5). Final build −Lier +Aesi; now `decks/croak-and-dagger-20260623-215731.txt`.
6. 🟢 **Forced Liquidation (Kefka)** — the one build proceeding (Hashaton dropped 2026-06-27). ~57 true buys across this + Zero-Sum + Lightning War; **treated as bought/built 2026-06-30** (physical settlement owed on contention buys). No pod approval (statics kill). See §1b + buy list.

**Headline:** the *swaps* are the free wins; the **Forced Liquidation build** is where the money goes
(now **treated as bought/built 2026-06-30** alongside Zero-Sum + the Lightning War upgrade — physical
settlement owed on contention buys). The Hashaton/Calamity Thoracle question is moot — **Thoracle is
out of the roster**; Croak and Dagger went grind (§5), Hashaton was dropped.

---

## 1. The build (Forced Liquidation / Kefka)

> **Updated 2026-06-27:** this section originally tracked *two* builds (Hashaton + Kefka). **Hashaton
> is dropped** — see §1a, struck. Only **Forced Liquidation (Kefka)** is proceeding, and it's now
> **treated as bought/built (2026-06-30)**. It pulls from your existing **black decks** (Sauron, Crystal Sickness, Curse of the
> Scarab, Croak and Dagger), so keeping those intact means buying duplicate shared pieces — see the
> contention buys in `analysis/Buy_List_ZeroSum_LightningWar_ForcedLiquidation_2026-06-25.md`.

### 1a. ~~Hashaton, Scarab's Fist — *Thassa's Oracle combo*~~ 🔴🔒 — **DROPPED 2026-06-27 (Thoracle out of roster)**
- **List:** `decks/considering/hashaton-thoracle-20260614.txt` · **Clock:** T6 decap = table (lab `hsh_clock_lab.py`) · **GCs:** 3/3 (Thassa's Oracle, Demonic Tutor, Vampiric Tutor)
- **Wincon:** discard/deploy Thassa's Oracle → Demonic Consultation / Tainted Pact empties library → ETB win. Hashaton is the tutor/dig/resilience engine.
- **Sourcing (availability sweep, 100 cards):** **9 free** · 27 unowned · 10 proxy-only · 54 owned-but-deployed (most are surplus staples = effectively free; the scarce ones below are the real cost).
- **Must acquire — the combo + key spells:** Thassa's Oracle, Demonic Consultation, Tainted Pact, Jace Wielder of Mysteries, Beseech the Mirror, Spellseeker, Putrid Imp, Tireless Tribe, Skirge Familiar, Ghostly Pilferer, Astral Dragon, Wishclaw Talisman, Scheming Symmetry, Painful Truths, Cut Down, Fatal Push, Prismatic Ending, Supreme Verdict, Silence, Shark Typhoon, Flusterstorm.
- **Must acquire — the manabase is the budget-killer:** **Tundra, Scrubland, Mana Confluence** (unowned; Tundra/Scrubland are reserved-list ≈ €200–400 each), plus Darkslick Shores, Castle Locthwain. **Underground Sea** is owned (×2) but both copies are in Croak and Dagger + Crystal Sickness.
- **Scarce shared singletons it raids:** Mana Drain, Dauthi Voidwalker, Vampiric Tutor, Demonic Tutor (all owned but fully committed to other decks — buy or pull).
- **Reality:** *Not priced yet, but this is the most expensive option by far if bought in paper.* The realistic path is **proxy the cEDH manabase** (Tundra/Scrubland/Underground Sea) and buy the cheap combo/dig pieces.
- **Gate:** 🔒 pod approval of Thassa's Oracle + Consultation (the high-stigma combo).

### 1b. Kefka, Court Mage — *Forced Liquidation (wheel-burn)* 🟢 — **BUILT (treated as bought 2026-06-30; cards on order 2026-06-27)**
- **List:** `decks/considering/forced-liquidation-20260625.txt` (Displacer Kitten + Bolas/Channeler passes; older `-20260612`/`-20260623` archived) · **Clock:** decap T8 / table T9 (lab `kfk_clock_lab.py`, 2026-06-25) · **GCs:** 3/3 (Notion Thief, Demonic Tutor, Mana Vault) · **Commander owned (free).** · **Buys:** see `analysis/Buy_List_ZeroSum_LightningWar_ForcedLiquidation_2026-06-25.md`.
- **Wincon:** wheel (draw 7s) + static punishers (Sheoldred / Underworld Dreams / Fate Unraveler / Psychosis Crawler / Niv-Mizzet). Resolves on *your* turn through *statics* → **the one kill that ignores Grand Abolisher → no pod approval needed.**
- **Sourcing (sweep, 80 cards):** **10 free** · 24 unowned · 7 proxy-only · 39 owned-deployed (manabase, rocks, protection, Notion Thief, Psychosis Crawler are free/surplus).
- **Must acquire — premium wheels:** Wheel of Fortune, Echo of Eons, Time Spiral, Memory Jar, Reforge the Soul, Dark Deal.
- **Must acquire — punishers:** Fate Unraveler, Niv-Mizzet Parun, Megrim, Liliana's Caress, Ob Nixilis the Hate-Twisted, Kederekt Parasite, Glint-Horn Buccaneer, Bloodletter of Aclazotz; (Underworld Dreams owned proxy-only).
- **Must acquire — rest:** Cursed Totem, Waste Not, Diabolic Tutor, Mastermind's Acquisition, Bedevil, Terminate, Infernal Grasp, Bloodchief's Thirst, Rakdos Charm, Negate.
- **Scarce shared singleton:** **Sheoldred, the Apocalypse** (own 1, in The Dark Lord's Army) — buy a copy for Kefka or pull from Sauron.
- **Estimate:** ~€140–190 (bake-off) / ~$85–140 (proposal) — both **unverified**, both pre-date the availability sweep. The wheels (Wheel of Fortune / Echo of Eons / Time Spiral / Memory Jar) are the bulk of the spend.
- **Gate:** none. This is the deck you can build without asking the pod.

### 1c. Hearthhull, the Worldseed — *Creative Destruction* (Jund land-sac) 🟢 — **QUEUED (named + approved 2026-07-05; awaiting precon arrival)**
- **List:** `decks/considering/world-shapers-tuned-20260704.txt` (build target; supersedes upgraded/merged) · **Clock:** decap T10 / table T11 (`ws_clock_lab` @40k 2026-07-05, post commander-registry fix) · **GCs:** 3/3 (Crop Rotation, Gamble, Natural Order) · **Vs Ur-Dragon: 69% (#7)** — 2× the Earthbend seat it retires (33%) · **Tier C #12** (composite 30.7, `ws_place --tuned --measure-inter`).
- **Wincon:** stationed land-sac drain + Mazirek/Broodscale loop (Abolisher-immune) + landfall slug; Meathook/Jarad/Exsanguinate/AWBO converters.
- **Sourcing:** the precon (350 DKK, **on order**) + free pool + **Earthbend the Meta retirement** (same archetype seat) + **DR donor pulls per user carve-out** (The Meathook Massacre, Prismatic Vista, Verdant Catacombs, Takenuma — **bump DR's `.txt` when pulled**). Zero further card buys.
- **Gate:** none (2-card infinite covered by the 2026-06-19 pod combo OK; Planetary Annihilation stays in the box pile pending any ruling).
- **On arrival:** sleeve-day checklist in `proposals/PROP_World_Shapers_Hearthhull.md` (status block) — DR pulls, Earthbend archive, promote as `decks/creative-destruction-YYYYMMDD.txt`, register the stem in `deck_registry.EXTRA_COMMANDERS`, DeckSafe re-run, first-games audit.

---

## 2. Recommended swaps (per deck)

| Deck | Out → In | Source of the "In" cards | Cost | Gate | Status |
|---|---|---|---|---|---|
| **Radiation Sickness** ✅ | −Survival of the Fittest (GC) **+**Sylvan Library; −Generous Patron +Hedron Crab; −Guardian Project +Sidisi, Brood Tyrant | Sylvan Library (own ×2 real) · Hedron Crab (own ×2 real) · Sidisi (**proxy-only** — play proxy or buy ~€2) — all ex-Loam | 🟢 **$0** | none | **✅ APPLIED 2026-06-15** → `radiation-sickness-20260622.txt`, 3/3 legal; **+2026-06-22 −Vorinclex +Timeless Witness** (Durability, $0); **+2026-07-07 −Birds of Paradise +Nightshade Dryad** (fixing-neutral; Birds → Zero-Sum) → `radiation-sickness-20260707.txt` |
| **The Grand Design** ✅ | 7-for-7. Adds: Solemn Simulacrum, Sakura-Tribe Elder, Wood Elves, Faeburrow Elder, Coalition Relic, **Craterhoof Behemoth**, Rune-Scarred Demon | Solemn/Sakura/Coalition/Craterhoof = owned spares (real); Faeburrow = ex-Peace Offering (own 1); Wood Elves + Rune-Scarred bought | 🟢 **done** | none | **✅ APPLIED 2026-06-25** → `the-grand-design-20260623.txt`. Proposal archived. |
| **The Exile's Return** | +Kiki-Jiki +Drannith Magistrate −Night's Whisper −Light Up the Stage | Drannith (own 1, undeployed) free; **Kiki-Jiki = buy** | 🟡 **~€10–15** | 🔒 yes | Proposal only. (Avatar's Wrath is NOT a cut — re-verified.) |
| **Replication Crisis** ✅ | ~~+Kiki-Jiki −Bident~~ **DECLINED.** Applied: **+Imperial Recruiter −Strionic Resonator** | **Imperial Recruiter = owe a 2nd copy** (owned one is in Exile's Return); price unverified, budget-reprinted | 🟢 **APPLIED 2026-06-30** (as-if-bought) | none (tutor, not a new combo) | **✅ → `the-replication-crisis-20260630.txt`** (old archived; deck_doctor 100/3-GC). Lab `rc_speed_lab.py`: tutors the *existing* Satya+LR infinite → 11→22% T6 / 18→32% T12; ANY line 24→33% / 36→48%. Doc: `decks/The_Replication_Crisis_Swaps_2026-06-30.md`. |
| **Croak and Dagger** ✅ | **"Inevitable" topdeck-combo rebuild** (2026-07-01, supersedes the grind fortress): −13 (Demonic Tutor, Gray Merchant, Kokusho, Rite, Submerge, V.A.T.S., Crucible, Loam, Splendid, Ramunap, Titania's Command, Spore Frog, Blossoming Tortoise) +13 (Bolas's Citadel, Sensei's Top, Aetherflux, Ancient Cellarspawn, One with the Multiverse, Fortune Teller's Talent, Reality Chip, Savvy Trader, Emergent Ultimatum, Insidious Dreams, Tidal Barracuda, Tatyova, Scheming Symmetry) | **8 buys ≈ €32** + a 2nd Aetherflux; Sensei's Top owned/free | 🟢 **PROMOTED** | none (B4-in-spirit combo; pod OK'd combos 06-19) | **✅ APPLIED 2026-07-01** → `croak-and-dagger-20260701.txt`. Only GC change Demonic Tutor→Bolas's Citadel (3/3). Clock T13→**T9** (lab `glarb_inevitable_lab.py`); P(beat pod) ~7–8%→~30%. |

~~**Diminishing Returns later stages**~~ — **VOID 2026-07-08: Diminishing Returns is dismantled.** The B4 staging plan (Stages 2–4 below) is dead; kept struck for the record only.
- ~~Stage 2 — 🟡 +Leonin Relic-Warder (buy ~€1–5, the most efficient combo card) +Wishclaw Talisman (optional, buy).~~
- ~~Stage 3 — 🔴 +Exquisite Blood (€20–23, Cardmarket 2026-06-10) +Vito (~€9–13). Defensible to skip.~~
- ~~Stage 4 — GC reallocation (+Demonic Tutor +Vampiric Tutor)~~ — **dropped 2026-06-14 (user: not worth it).**

---

## 3. Consolidated shopping list (the actual buys)

Grouped by what they unlock. Quantities matter where a card is wanted by more than one plan (§4).

**Cheap, high-value, unlock free swaps:**
- ~~Wood Elves ×1, Rune-Scarred Demon ×1 → Grand Design~~ — **bought, applied 2026-06-25.**
- Kiki-Jiki, Mirror Breaker **×1** → Exile's Return (~€10–15) *(Replication Crisis dropped its Kiki — DECLINED 2026-06-30)*
- Imperial Recruiter **×1** → Replication Crisis (2nd copy; owned one is in Exile's Return) — price unverified, budget-reprinted
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

*Verified EUR prices (as of 2026-06-02 — re-confirm before buying, per [[feedback_verify_prices]]) for the still-relevant buys (Kiki, the Kefka wheels + punishers) are in the archived buylist `archive/build_scratch/Proposed_Buys_2026-06-02.md`. Its Loam / Berta / Witherbloom sections are dead (dismantled / parked).*

---

## 4. Cross-deck contention — don't double-spend the same card

These cards are wanted by **more than one** plan. Owning one copy ≠ enough.

> Regenerate this from raw data with `python scripts/unlock_optimizer.py` (backlog #3):
> it counts demand across the 16 active decklists + the live builds, nets out
> owned+proxy copies, and ranks the over-committed cards + the shared one-purchase
> unlocks. Pending per-deck swaps not yet written to a `.txt` (e.g. the Kiki-Jiki
> Exile's/Replication swap) aren't seen — the table below adds those by hand.

| Card | Wanted by | Owned (free) | Action |
|---|---|---|---|
| **Thassa's Oracle** | Hashaton (only) | 0 | Buy 1 for Hashaton (Calamity dropped Thoracle — §5) |
| **Demonic Consultation** | Hashaton (only) | 0 | Buy 1 for Hashaton |
| **Demonic Tutor** (GC) | Hashaton + Kefka | 3, all deployed | Buy 1–2 more, or free one by dismantling a black deck |
| **Vampiric Tutor** (GC) | Hashaton (only; aspirational Strong-Glarb also wants it) | 1, over-committed | Buy 1 for Hashaton |
| **Sheoldred, the Apocalypse** | Kefka + Dark Lord's Army (deployed) | 1 (in Sauron) | Buy 1 for Kefka, or pull from Sauron |
| **Kiki-Jiki, Mirror Breaker** | Exile's Return (Replication Crisis dropped it — DECLINED 2026-06-30) | 0 | Buy **1** for Exile's Return |
| **Imperial Recruiter** | Replication Crisis + Exile's Return (deployed) | 1 (in Exile's Return) | Buy **1** for Replication Crisis (−Strionic; tutors the Satya+LR line) |
| **Grim Tutor** | Hashaton + DR-Stage 1 | 1 | Only one gets the free copy → buy a 2nd (~€ cheap) for the other |
| **Final Parting** | Grand Design (Calamity's old reanimator claim is **retired**) | 1 (ex-Loam) | Free for GD now — contention resolved |
| **Dauthi Voidwalker** | Hashaton + Dark Lord's Army (deployed) | 1 (in Sauron) | Buy or pull |

**Donor decks getting raided:** The Dark Lord's Army (Sauron) is hit by *both* builds (Sheoldred,
Underworld Dreams, Dauthi). Crystal Sickness / Curse of the Scarab / Croak and Dagger supply the
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

**Resolved 2026-06-14.** Croak and Dagger drops the Thoracle direction entirely and becomes a **grind /
inevitability fortress** — its natural identity (Glarb casts MV4+ bombs off the top). A non-Thoracle
Isochron Scepter + Dramatic Reversal combo was tested and **rejected** (unreliable in this shell —
36% by T14; the deck can't tutor a non-creature combo and the GC cap blocks the blue tutors; lab
`glarb_iso_clock_lab.py`). So **Hashaton is now the sole Thassa's Oracle deck** — no duplicated
wincon, no doubled combo buys, no shared approval.

- ✅ **Applied 2026-06-25 ($0, no approval):** the grind-fortress upgrade in §2 — owned adds, grind T9 (final build −Lier +Aesi).
- **Aspirational (work toward):** migrate toward the Strong-Glarb external — Tier 1 Nyxbloom
  Ancient + Uro; Tier 2 Sphinx of the Second Sun + Beledros + Wilderness Reclamation; Tier 3 flash
  package (Leyline owned-proxy + Tidal Barracuda) + Spelunking; then a GC reconfig (Crop Rotation
  owned + Field of the Dead owned-proxy + Vampiric Tutor buy). See `analysis/Calamity_Grind_Fortress_2026-06-14.md`.

---

## 6. Pod approvals outstanding

Everything combo-flavoured needs Rule-0 sign-off. There are two *classes*:

- ~~**Thassa's Oracle / Consultation (high stigma):** Hashaton, Calamity-hybrid.~~ **No longer needed (2026-06-27) — Thoracle is out of the roster.**
- **Standard 2-card infinites:** Exile's Return (Kiki+Felidar). *(~~Diminishing Returns (Deathmantle+Titan, LRW+aura)~~ — VOID, DR dismantled 2026-07-08.)* *(Replication Crisis dropped its proposed Kiki line 2026-06-30; its in-deck Satya+Lightning Runner infinite predates this and the Imperial Recruiter add is just a tutor for it — no new approval.)*

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

1. ✅ **Done (free, no approval):** the **Radiation Sickness** GC-fix, the **Grand Design** upgrade, and the **Croak and Dagger** grind-fortress upgrade are all sleeved (2026-06-15 → 2026-06-25).
2. ✅ **Resolved 2026-06-27 — §5 + Thoracle decision both closed.** No Thoracle deck is being built (Hashaton dropped; Croak went grind). The build proceeding is **Forced Liquidation (Kefka)**.
3. ✅ **Treated as bought/built 2026-06-30 (per user direction):** Forced Liquidation + Zero-Sum + the Lightning War upgrade — consolidated buy list fulfilled-as-if-bought (physical settlement owed on contention buys). **Kefka needs no pod approval** (statics kill).
4. **One pod conversation (still pending):** ask for the **standard 2-card infinites** (Exile's Return Kiki, DR), and propose codifying the blanket exception. *(The high-stigma Thoracle approval is no longer needed — Thoracle is out. Replication Crisis's Recruiter add needs no approval — tutor, not a new combo.)*
5. **Small buys:** Kiki ×1 → Exile's Return; Imperial Recruiter ×1 → Replication Crisis (no approval). *(The Diminishing Returns Stage-1 step is void — deck dismantled 2026-07-08.)*
6. **On physical arrival of the owed copies:** re-run DeckSafe with the updated Moxfield export, then refresh `Collection_Master_Status.md` from the real ownership numbers (the 2026-06-30 "as-if-bought" status here is a planning marker, not a DeckSafe result). Forced Liquidation is already promoted to `decks/`; Zero-Sum/Lightning War `.txt` builds already carry their cards.
7. **On the World Shapers precon's arrival:** run the Creative Destruction sleeve-day checklist (§1c / PROP status block) — DR donor pulls (+ DR `.txt` bump), Earthbend retirement, promote the tuned list as `decks/creative-destruction-YYYYMMDD.txt`, register the stem, DeckSafe re-run, first-games audit.

---

*Maintenance: when a swap is sleeved, bump the deck's dated `.txt`, archive the old list, update its
Summary, and strike the row here. When the Thoracle decision (§5) is made, delete the losing option
from §1/§3/§4.*
