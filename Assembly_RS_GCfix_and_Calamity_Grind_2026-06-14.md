# Assembly guide — Radiation Sickness GC-fix + Calamity grind-fortress

**2026-06-14.** The two ungated build improvements the pod gauntlet flagged
(`campaigns/Pod_Gauntlet_2026-06-14.md`, `--swapped`). Sourcing below is verified
against `collection/moxfield_haves_2026-06-07-1031Z.csv` + a scan of every
`decks/*.txt` (which deck each owned copy currently sits in). Prices are
**unverified** — confirm before buying ([[feedback_verify_prices]]).

> **Proxy note:** this is a proxy-friendly Bracket-3 collection, so "play the
> proxy" is a legitimate $0 path for any card below. The "buy" prices are only if
> you want a real copy.

---

## 1. Radiation Sickness — GC-fix (MANDATORY, 3-for-3)

**Build:** `decks/considering/radiation-sickness-gcfix-20260614.txt` (100 cards,
**now 3/3 GC** — fixes the illegal 4/3; Survival of the Fittest was the uncounted
4th alongside Seedborn Muse / Vampiric Tutor / Cyclonic Rift).
**Clock:** decap ~T7 (unchanged) · table **T10→T9** (`rs_clock_lab.py --mode
upgrade`). The win here is *legality*, not speed.
**Gauntlet:** 68% → 69% (the clock barely moves — the rad drain is
creature-count-independent).

### Cards to ADD — where each comes from

| Card | Source | Cost |
|---|---|---|
| **Sylvan Library** | own **2 real** (1 is in Calamity → goes to the grind-fortress; the **2nd real spare** is free for RS). ex-Loam. | **$0** |
| **Hedron Crab** | own **2 real**, deployed in no deck → free spare. ex-Loam. | **$0** |
| **Sidisi, Brood Tyrant** | own **0 real, 1 proxy** → play the proxy, or buy a real | **$0 (proxy)** / ~€2 |

### Cards to CUT (back to the spares pile)
Survival of the Fittest *(the illegal 4th GC)* · Generous Patron · Guardian Project.

**Bottom line: $0.** Pull the 2 free real spares (Sylvan Library, Hedron Crab),
proxy Sidisi.

---

## 2. The Calamity Tax — grind-fortress rebuild (6-for-6)

**Build:** `decks/considering/glarb-grind-fortress-20260614.txt` (100 cards, 3/3
GC, Glarb). Thoracle/Isochron dropped — pure grind.
**Clock:** decap **T13→T9**, table **>T14→T9** (lab: `ct_speed_lab.kill_turns` on
the build, 12k 2026-06-14 — decap 16% T7 / 38% T8 / 63% T9 / 80% T10).
**Gauntlet:** **4% → 29%** — the single biggest ungated improvement on the roster.

### Cards to ADD — where each comes from

| Card | Source | Cost |
|---|---|---|
| **Birds of Paradise** | own **6 real**, 4 deployed (Eldrazi/Radiation/GD/Zero-Sum) → **2 free spares** | **$0** |
| **Crucible of Worlds** | own **2 real** (1 in Crystal Sickness) +2 proxy → **1 free real spare** | **$0** |
| **Lier, Disciple of the Drowned** | own **1 real**, deployed nowhere → free | **$0** |
| **Life from the Loam** | own **2 real**, deployed nowhere → free. ex-Loam. | **$0** |
| **Bloom Tender** ⚠ | own **1 real + 1 proxy**, but the real is in **Radiation + Grand Design** → use the **proxy** (or buy a real) | **$0 (proxy)** / ~€10 |
| **Delighted Halfling** ⚠ | own **1 real**, deployed in **Eldrazi + Zero-Sum** (no proxy) → **proxy or buy**, or pull from Eldrazi/Zero-Sum | ~€8 / proxy |

### Cards to CUT (back to the spares pile)
Druid of Purification · Flash Photography · High Fae Trickster · Mirrorform ·
Savvy Trader · Starfield Vocalist.

**Bottom line:** 4 free spares (Birds, Crucible, Lier, Life from the Loam). The
**§2 "all 6 owned $0" was optimistic** — two are committed elsewhere: **Bloom
Tender** (proxy it; the real copy stays in RS/GD) and **Delighted Halfling** (no
proxy on hand → proxy/buy ~€8, or pull one from Eldrazi/Zero-Sum). All-proxy path
= **$0**; all-real path ≈ **€18** (unverified).

---

## Cross-build contention (because you're assembling both at once)

- **Sylvan Library** — own 2; one goes to the grind-fortress (it was Calamity's),
  one to RS. Exactly covered, no buy.
- **Bloom Tender** — own 1 real + 1 proxy, now wanted by **RS + Grand Design +
  grind-fortress** (3 decks). The real stays put; the grind-fortress runs the
  **proxy**. If you want all-real, buy 1.

## Once assembled

These live in `decks/considering/` as build files (the deployed `.txt`s still
show the current decks — ground-truth rule). When the physical cards are in the
sleeves, promote each: rename to `decks/<deck>-20260614.txt`, move the old
version to `archive/old_decklists/`, and update the deck's `*_Summary.md`. The RS
GC-fix is the priority — the deployed list is **illegal at 4 GC** until you do.

*Regenerate the contention math anytime: `python scripts/unlock_optimizer.py`.*
