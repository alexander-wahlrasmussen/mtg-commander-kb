# The Grand Design — Finisher-Redundancy Optimization Pass

> **ARCHIVED / SUPERSEDED 2026-06-13** by the single canonical GD upgrade
> (`proposals/Grand_Design_Upgrade_2026-06-13.md`), which folds Craterhoof in as swap #6 of a
> lab-validated 7-for-7 (ramp + diversified finisher). Kept for the finisher-fragility analysis.

**Date:** 2026-06-08
**Trigger:** The speed-curve analysis (`Grand_Design_Speed_Curve_Analysis.md`) found the 2026-05-02 swaps were speed-neutral and reliability-mixed. Follow-up ask: the deck leans on **one** finisher (Finale of Devastation) — add redundancy — plus evaluate the pod's "no maximum hand size" suggestion. Enabled by **The Loam Cycle being dismantled** (Craterhoof frees to Grand Design at $0; a few Loam cards go to Calamity Tax).
**Card text verified** via `card_lookup.py` for every add/cut. **GC checked** (`REF_Game_Changers_List.md`): all adds are non-GC; deck stays **3/3** (Force of Will, Rhystic Study, Cyclonic Rift). **Cross-deck/ownership checked** against `moxfield_haves_2026-06-07-1031Z.csv` + `decks/*.txt`.

> **Bottom line:** The deck's real structural flaw isn't "few kill lines" — it's that **all 10 kill lines funnel through one card (Finale), and that card is invisible to the deck's own tutors** (Pod / Chord / Eladamri's / Defense / Razaketh all find *creatures*; Finale is a sorcery). The single highest-impact, **$0** fix is **+ Craterhoof Behemoth** — a second mass finisher that the entire creature engine *can* find, that is reanimatable, Pod-able, and Defense-able. The sim shows it lifts "a finisher available by T6" from **12% → 47%** (with the creature engine) — roughly **4×**. The no-max-hand-size idea is a value upgrade, not a win-condition fix; your skepticism is correct.

---

## 1. The problem, confirmed: one finisher, and the tutors can't find it

The Summary lists "10 kill lines," but classify them by what actually *deals lethal*:

| Kill line | What it really does | Finisher? |
|---|---|---|
| 1. Finale X≥10 | the kill | **Finale** |
| 2. Defense of the Heart | fetches 2 creatures → "cast Finale next turn" | → Finale |
| 3. Razaketh tutor chain | "tutor Finale" → cast it | → Finale |
| 4. Chord → Razaketh | → tutor Finale | → Finale |
| 5. Protected kill turns | protect the **Finale** turn | → Finale |
| 6. Karmic + Reveillark loop | "tutor Finale + protection" | → Finale |
| 7. Birthing Pod chain | value/inevitability — no actual lethal | none |
| 8. Living Death | rebuild board → "kill next turn via Finale" | → Finale |
| 9. Sidisi exploit | "tutor any card" → Finale | → Finale |
| 10. Atraxa combat | 21 commander damage over 3 connects | slow backup |

**9 of 10 are "find / cast / protect Finale."** The only Finale-independent kill is Atraxa swinging three times — far too slow against a T6–7 combo pod. If Finale is countered, exiled, or buried, the deck has **no fast mass-kill.** That is a genuine single-point-of-failure, and it's worse than it looks: **every tutor in the deck (Birthing Pod, Chord of Calling, Eladamri's Call, Defense of the Heart, Razaketh) fetches creatures — none can find Finale.** The deck's deep tutor suite cannot dig for its own only closer.

---

## 2. The fix: a *creature* finisher the engine can find — Craterhoof Behemoth

**Craterhoof Behemoth** `{5}{G}{G}{G}` — Creature, Haste; ETB: creatures you control gain trample and get +X/+X where X = creatures you control. Verified text. Why it is the ideal add for *this* deck specifically:

- **Findable by the whole engine:** Birthing Pod (MV 8), Chord of Calling, Eladamri's Call, **Defense of the Heart (puts it straight onto the battlefield → immediate kill), Razaketh, and Finale itself** (Finale at X≥8 fetches Craterhoof to the battlefield). The deck's tutors finally point at a finisher.
- **Reanimatable:** Buried Alive / Grisly bin it; Reanimate / Animate Dead / Necromancy / Victimize / Dread Return bring it back — a 1–3 mana overrun. **Persist now has a legal target too** (Craterhoof is nonlegendary), so the deck's weakest reanimate spell gets better instead of being a cut.
- **Combos with Finale, doesn't just duplicate it:** Finale X≥10 gives the team +X/+X **and haste**, then fetches Craterhoof whose ETB adds *another* +(creature count). Finale's haste also covers Craterhoof's one weakness (its ETB pumps the team but only Craterhoof itself has haste).
- **Doubles under the flicker engine:** Panharmonicon / Elesh Norn make Craterhoof's ETB fire 2–3×; Ephemerate/Soulherder/Thassa re-trigger it.

### Simulation — finisher availability by turn (40k trials, `gd_speed_lab.py --mode finishers`)

| build | T4 | **T6** | T8 | T10 |
|---|---|---|---|---|
| **CURRENT** — Finale only, drawn (tutors can't help) | 10 | **12** | 14 | 16 |
| **+ Craterhoof** — drawn | 19 | **22** | 26 | 29 |
| **+ Craterhoof** — **+ creature-tutors** | 41 | **47** | 53 | 58 |
| + Craterhoof **& Pathbreaker Ibex** — drawn | 26 | **31** | 36 | 40 |
| + Craterhoof & Ibex — + creature-tutors | 46 | **53** | 60 | 65 |

Adding **one** creature finisher takes "have a closer by T6" from **12% to 47%**, because the creature tutors can now fetch it (and Defense/Razaketh, not even counted here, add more). A second creature finisher pushes it to 53%.

---

## 3. Recommended package (collapsed, single 3-for-3)

Keeps the deck at **100 cards** and **3/3 GC** (no GC added). Net cost **~$5** (one buy), or **$0** if you drop the Ibex line.

| OUT | IN | Cost | Role |
|---|---|---|---|
| Ghostly Flicker | **Craterhoof Behemoth** | $0 (Loam teardown) | Primary 2nd finisher — engine-findable, reanimatable, Defense→direct kill, combos with Finale. |
| Bloom Tender | **Pathbreaker Ibex** | ~$5 (buy) | Secondary creature finisher — repeatable overrun, reanimatable, Pod MV 6. Replaces the board-conditional dork. |
| Grisly Salvage | **Grim Tutor** | $0 (owned, undeployed) | A tutor that can **finally find Finale or Craterhoof** (the root-cause fix) or any answer; replaces the ~15%-per-cast random binner. |

**Cut rationale:** *Ghostly Flicker* is the narrowest flicker piece (must exile **two** targets — can't blink a lone Craterhoof), so it's the softest cut; 5 flicker outlets remain to re-trigger Craterhoof's ETB. *Bloom Tender* is the board-conditional ramp the speed analysis flagged. *Grisly Salvage* is the ~15% enabler.

**Add rationale:** two **creature** finishers turn the whole tutor suite (Pod/Chord/Eladamri's/Defense/Razaketh/Finale) into finisher-finders; **Grim Tutor** ($0, owned, non-GC) is a generic find-anything that can grab Finale itself, a finisher, a protection piece, or a reanimate spell — closing the "no tutor can find the closer" gap from the other direction too.

---

## 3b. Was this the best we could do without more Game Changers?

**For the core flaw — yes, essentially.** A *creature* finisher is the correct *shape*, not just "another finisher," because it makes the five existing creature-tutors productive. Everything else I weighed (text-verified) is worse for that specific problem:

| Option considered | Verdict | Why |
|---|---|---|
| **Craterhoof Behemoth** | ✅ best | Instant overrun, haste, ETB, MV-8 Pod target, reanimatable, Finale-fetchable. |
| **Pathbreaker Ibex** | ✅ #2 | Creature, repeatable; engine-findable. The right second creature finisher. |
| **Insurrection** | ❌ **off-colour** | `{5}{R}{R}{R}` — **mono-red**; illegal in WUBG. (You own it; it can't go here.) Verified — don't be fooled by the "steal the table" reputation. |
| Overwhelming Stampede / Triumph of the Hordes | ⚠️ weaker | Sorcery overruns — add redundancy but are **un-tutorable** (not creatures), so they don't fix the engine-findability problem. Triumph is also infect + oversubscribed. |
| **Rise of the Dark Realms** | ⚠️ niche | Legal non-GC reanimator haymaker (reanimate *all* graveyards), but **9 mana, win-more, un-tutorable**. A top-end option if you want one, not a fix. |
| Generic noncreature tutor (**Grim Tutor** / Diabolic Tutor) | ✅ as the 3rd slot | One tutor that finds Finale is a *weaker* single fix than Craterhoof (which adds a finisher **and** activates 5 tutors) — but Grim Tutor is **owned/$0**, so it earns the third slot as flexible consistency rather than the headline. |
| Natural Order, Tooth and Nail (as Craterhoof-fetch) | ❌ / ⚠️ | Natural Order **is a GC** (would break the cap). Tooth and Nail is non-GC but a clunky 9-mana win-more. |

**Where we can still do better (honest):**
1. **The third slot is a genuine judgment call.** Grim Tutor ($0) is the flexible pick. If you'd rather specifically *restore reanimation determinism* (the speed-analysis ding), a **binner** is better there: **Corpse Connoisseur** (~$2 — a *creature* that bins Craterhoof/Razaketh and unearths; on-theme and engine-findable) or **Jarad's Orders** (~$2, creatures-only Final Parting). The original **Final Parting** is the strongest 2-for-1 (bin + grab a reanimate spell) but it's the **single copy claimed by the Calamity Tax pivot** — only viable if you buy a 2nd (~$4).
2. **No non-GC option meaningfully improves *speed*.** As the speed analysis concluded, this deck's kills are mana/setup-gated; finisher redundancy fixes *reliability of having a closer*, not the clock. The only real speed levers are GCs (fast mana / tutors) — excluded by the 3-cap.

So: optimal on the finisher-redundancy axis you asked about; the one open choice is *what flavour* the third slot is (flexible tutor vs deterministic binner).

---

## 4. The pod's "no maximum hand size" suggestion — honest verdict

**Your skepticism is right: it won't give you what you want.** No-max-hand-size is a *value/grind* upgrade — it lets you keep the overflow from Atraxa's 5–7-card ETB, Rhystic Study, and especially **Vilis** (lose life → draw that many; Razaketh/fetches/painlands feed it). But it **adds no finisher and closes no game faster.** It is *complementary* to adding finishers (you draw and keep more closers), never a substitute. Spend the slot on a finisher first.

If you still want a nod to it:
- **Thought Vessel** (owned, surplus) is the *only* version worth a slot — because it's **also a {C} mana rock** (ramp toward 8-mana Craterhoof / 12-mana Finale), so it earns its keep as ramp and the no-max-hand-size rides along free. Even so, it's a marginal ramp piece, not a priority.
- **Avoid Reliquary Tower.** A colorless land in a 4-color deck still dilutes coloured sources for zero board impact. *(Correction 2026-06-09: the "~39% by T6" originally cited here was a sim artifact — the corrected floor is ~90%, see `Grand_Design_Mana_Fixing_Pass_2026-06-09.md`. The argument weakens but the verdict stands: a colorless utility land whose only payoff is value-retention isn't worth a coloured source in WUBG.)*

---

## 5. Compliance & sourcing summary

- **GC:** 3/3 held (no GC added — Craterhoof, Ibex, Stampede, Final Parting, Thought Vessel are all non-GC; **Natural Order and Tooth-and-Nail-as-tutor were avoided** — Natural Order *is* a GC; Tooth and Nail is *not* (delisted 2025-10-21) but is a clunky 9-mana win-more).
- **Count:** every tier is a 1-for-1; deck stays at 99 + commander.
- **Ownership / cross-deck:** Craterhoof — own 2, Loam's copy frees here ($0). **Grim Tutor — owned, undeployed ($0).** Pathbreaker Ibex — not owned (~$5 buy). Final Parting — own 1, **claimed by Calamity Tax** (only viable here if you buy a 2nd, ~$4); Corpse Connoisseur / Jarad's Orders — not owned (~$2) if you want a binner instead. Thought Vessel — owned, surplus (no-max-hand-size, §4).
- **Reskin aliases:** none of these are UB reskins.

## 6. Caveats & next step
- `gd_speed_lab.py --mode finishers` is a card-availability model — it ignores mana and the board. "Finisher available" ≠ "lethal this turn"; Craterhoof still needs a board to pump and ~its cheat-cost (reanimate/Pod/Defense) or 8 mana. The finishers are designed to be **cheated in, not hardcast** — adding them nudges avg CMC up (~+0.1) but that's not how they're deployed.
- Not applied to the `.txt` yet — this is a proposal. On approval: apply the 3-for-3 package, bump the dated filename (`the-grand-design-<today>.txt`), archive the old list, recount to 100, and update the Summary's kill-line section (Craterhoof/Ibex are now co-primary finishers; correct the "10 kill lines" framing to "2–3 finishers + enablers").

---

Related: `Grand_Design_Speed_Curve_Analysis.md` · `The_Grand_Design_Summary.md` · `Calamity_Tax_Reanimator_Pivot.md` (Final Parting contention) · [[project_pod_combo_opponent]] · [[feedback_card_availability_check]] · [[feedback_bracket_4_in_spirit]]
