# Proposal: Deficit Spending — K'rrik, Son of Yawgmoth (mono-B life-as-mana aristocrats)

Status: **PROPOSAL (drafted 2026-07-12)** — candidate list
`decks/considering/deficit-spending-20260712.txt` (100 cards, validated: deck_doctor PASS,
3/3 GC, all mono-B, all Commander-legal). Stem registered in `deck_registry.EXTRA_COMMANDERS`.
Gates: **user rename** (working name below), **buy decision** (§ Buy path), and a **first
physical goldfish** to check the conservative lab floor (§ Clock).

*The name:* deficit spending — paying today's costs by borrowing against your own reserves —
which is K'rrik's literal text: every {B} in any cost is payable with 2 life. Sits in the
roster's econ register beside Zero-Sum Game / Forced Liquidation / Creative Destruction /
Mass Production. Provisional; the user names decks.

**Verdict up front: the strongest owned-core candidate found by the 2026-07-12 collection
scan.** The engine is a **20-combo redundant web already complete in this exact 100**
(`find_combos.py` 2026-07-12 — twenty COMPLETE combos, 174 more one-away), built around four
cards the scan surfaced: Sephiroth (owned real, free), Warren Soultrader, Yawgmoth, and
Mikaeus. Only **6 cards are unowned — ≈€22** (deck_doctor, indicative Scryfall 2026-07-12).
The honest catch is **contention**: the loop pieces cluster in Curse of the Scarab and
Zero-Sum Game, so a zero-raid build adds ~€70+ of second copies (§ Buy path). The lab clock
is a **conservative assembly floor** (§ Clock) — mid-roster at worst, likely faster in hand.

Every card named below was read via `card_lookup.py` at draft time (CLAUDE.md hard rule).
Combos verified against Commander Spellbook via `find_combos.py` on this exact list; loop
mechanics traced per-iteration (trace-the-loop rule). Ownership split real-vs-proxy from
`moxfield_haves_2026-07-11-0716Z.csv` (the availability run excludes the branch-only,
unbuilt Gitrog list).

---

## Commander (verified)

**K'rrik, Son of Yawgmoth** — {4}{B/P}{B/P}{B/P}, 2/2 Phyrexian Horror Minion, Lifelink.
*"For each {B} in a cost, you may pay 2 life rather than pay that mana."* Casts T3–4 off
4 generic mana + 6 life. In a 100% mono-black list, life is a second mana pool for **every
pip in every cost** — spells, activations, even special actions (official ruling). Grows
with each black spell cast; lifelink claws back the spent life in combat. Not a Game
Changer (verified vs `REF_Game_Changers_List.md` active section).

## The engine core (the reason this deck exists)

| Card | Cost | Verified role | Availability (real copies) |
|---|---|---|---|
| **Sephiroth, Fabled SOLDIER** | {2}{B} | Blood Artist + free sac outlet + draw on one card; transforms after 4 death-triggers/turn → **emblem drain that survives removal** | **1 real, FREE** (premium FIN copy; CSV row is the full `//` DFC name — front-face greps miss it) |
| **Warren Soultrader** | {2}{B} | "Pay 1 life, sac another creature: create a Treasure." A **Zombie** — enables Gravecrawler's recast; Treasure pays the {B}. The loop crank | 2 real, **both locked** (Scarab, Zero-Sum) → 3rd copy €13.89 or pull |
| **Yawgmoth, Thran Physician** | {2}{B}{B} | "Pay 1 life, sac another creature: −1/−1 counter + **draw**." Outlet + engine + the undying-cancel that makes Mikaeus loops airtight. Protection from Humans | **proxy-only, and the proxy is deployed in DLA** → real copy €27.62 |
| **Mikaeus, the Unhallowed** | {3}{B}{B}{B} | Other non-Humans get undying → every sac loops | 1 real, locked in Scarab → pull or buy *(price unverified — no EUR in snapshot)* |

**The primary loop, traced (S1):** Soultrader + Gravecrawler + any drain. Pay 1 life, sac
Gravecrawler → Treasure; drain triggers (Blood Artist-class: opponent −1, you +1 → **life-
neutral**); crack Treasure for {B}, recast Gravecrawler from the yard (Soultrader is the
Zombie). Mana-neutral, life-neutral, infinite iterations → table dead. All-activated on our
own turn — a resolved **Grand Abolisher does not stop it** (Abolisher restricts us only on
*his controller's* turn), and only the Gravecrawler recasts ever touch the stack.

**The redundancy (all 20 complete, CSB-verified on this list):** 6 drain payoffs make S1
six combos (Blood Artist / Zulaport / Nadier's Nightblade / Bontu's Monument / Aetherflux /
Sephiroth); Mikaeus+Soultrader+drain adds **infinite Treasures = infinite mana**;
Yawgmoth+Mikaeus+{Gray Merchant | Kokusho} and Yawgmoth+Nest of Scarabs+drain are parallel
webs; K'rrik himself anchors Chainer+Gray Merchant+outlet and Gravecrawler+Aetherflux+outlet.
No single card is load-bearing: lose Soultrader, Yawgmoth webs remain; lose both, Chainer
reanimates from the bin.

**Rejected on verification (recorded so it isn't re-tried):** *Necrodominance* (free-owned!)
— its third line **exiles anything that would hit your graveyard**, a hard nonbo with every
loop above. *Syr Konrad + Tortured Existence* (the first-pass "free kill line") — **both are
proxy-only**; the original claim was proxy-blind. *Thassa's Oracle* — blue; not legal here.
*Emeritus of Woe // Demonic Tutor* IS in (free): a prepared creature casting Demonic Tutor
*copies*, re-preparing whenever 2+ creatures died in a turn — trivial here, and per the SOS
ruling its own name keeps it **off the GC count**.

## Game Changers — 3/3

**Ad Nauseam** (buy €8.69), **Bolas's Citadel** (own 1, locked in Croak → 2nd copy €6.48),
**Mana Vault** (own 3, **1 free**). All three are life-payment engines — the commander's
text is their discount. Verified against the active GC list; Necropotence/Demonic/Vampiric
deliberately excluded to hold the cap.

## Clock — lab-cited, conservative floor

- **Goldfish (assembly-only model):** decap = table — **9% by T7, 20% by T9, 26% by T10,
  49% by T14, median beyond T14** (lab `scripts/krk_clock_lab.py`, 40k trials, 2026-07-12).
  decap == table by construction (an executed loop drains the pod).
- **Read this as a floor, not the deck.** The model assembles combo sets from *hand casts
  only*: it omits the reanimation assembly half (Chainer / Whisper / Victimize / Dread
  Return / Unmarked Grave binning pieces), most of the draw suite (Cryptbreaker, Vilis,
  Eviscerator's Insight, Witch's Cauldron), Ad Nauseam beyond a flat draw-5, Citadel
  storm-offs, and all chip damage (Gary ETB, Kokusho, Sephiroth passive). Those are the
  cards the deck actually digs with. Model v2 + a physical goldfish are the promotion gate.
- **Through interaction:** unmodeled *(unverified)*. Structural note: the kill is
  activated-ability-based on our own turn (Abolisher-proof, counterspell-light surface);
  Imp's Mischief redirects the one targeted answer that matters.
- Roster band at the floor numbers: Curse of the Scarab / Crystal Sickness territory —
  behind Kefka T8/T9 and Zero-Sum T9. If the real goldfish lands T7–8 (plausible given the
  omissions), it's in the racer conversation. Don't quote better than the lab without a lab.

## Buy path

**Tier 0 — unowned core, ≈€22 (deck_doctor, indicative Scryfall 2026-07-12):**
Ad Nauseam €8.69 · Culling the Weak €6.95 · Nest of Scarabs €3.69 · Bubbling Muck €2.42 ·
Chainer, Dementia Master **€0.27** · *(Doomsday Excruciator €0.65 — already acquired by the
user, pending CSV ingest; K'rrik casts it for 12 life, 0 mana.)*

**Tier 1 — contention buys (2nd/3rd copies so no roster deck is raided), ≈€70–75:**
Yawgmoth real €27.62 · Aetherflux Reservoir real €14.84 *(current copy is proxy-only,
deployed ×2)* · Warren Soultrader 3rd €13.89 · Bolas's Citadel 2nd €6.48 · Imp's Mischief
3rd €5.25 · Zulaport 2nd €1.49 · Viscera Seer 2nd €0.51 · Blood Artist / Cabal Ritual /
Dark Ritual 2nds *(cheap; unverified — no EUR in snapshot)*.

**Tier 2 — pull-or-buy:** Mikaeus, the Unhallowed *(price unverified)* — the one expensive
piece with a pull option.

**Donor concentration warning:** the pull path raids **Curse of the Scarab** (Mikaeus,
Soultrader, Cryptbreaker, Gravecrawler surplus is free but the rest isn't) and **Zero-Sum
Game** (Blood Artist, Zulaport, Viscera Seer, Soultrader, Cabal Ritual) — Zero-Sum is a
fresh 2026-07-08 build; recommend buying the cheap seconds instead of raiding it.
Everything else in the 100 — 33 FREE + 37 nominal "donor pulls" that are surplus copies
(Sol Ring ×26, Arcane Signet ×25, swamps, etc.) — costs nothing.

## Next steps

1. User: keep/rename "Deficit Spending"; approve a buy tier (Tier 0 alone is playable with
   proxies for Yawgmoth/Aetherflux; Tier 0+1 ≈ €95 is the zero-raid real-card build).
2. Model v2 of `krk_clock_lab.py` (reanimation assembly + draw suite) and/or a physical
   goldfish set — re-cite the clock before any Summary/Deck_Index claim.
3. On build: bump the `.txt` date, promote out of `considering/`, DeckSafe re-run after the
   Moxfield export ingests the buys + Doomsday Excruciator, first-games audit.
