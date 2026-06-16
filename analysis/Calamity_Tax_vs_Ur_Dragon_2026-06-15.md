# Calamity Tax (Glarb) as the Ur-Dragon counter — lab + build

**2026-06-15.** Re-roles The Calamity Tax (Glarb, Calamity's Augur) into the pod's
**anti-fair / Ur-Dragon specialist**, and quantifies the matchup with the first
board-attrition model (`scripts/vs_dragon_lab.py` — the `--vs-board` gap the Pod
Gauntlet flagged: the gauntlet races a *combo turn K*, which is the wrong shape for
a fair board deck). Relates [[project_ur_dragon_matchup]], [[project_calamity_tax_rebuild_direction]].

## Why Glarb for this job

Ur-Dragon is the archenemy's **only fair deck** — a combat-trigger board deck (eminence
cost reduction + attack→draw/cheat), not a combo. Beating it **inverts** the gauntlet:
grind/wrath/over-the-top decks win where race/glass decks get walled. Glarb fits and the
re-role **un-sticks** the deck:

- Glarb's kill is a **board-independent drain** (Torment of Hailfire / Kokusho+Rite /
  Gray Merchant) that goes *over* a flying dragon board — no blockers needed.
- The shell already runs flying-agnostic resets (Toxic Deluge, Meathook, Massacre Wurm),
  Maze of Ith, and heavy recursion (Crucible + Life from the Loam + Lumra).
- It was the **worst deck vs his combo** (5% gauntlet blend), so specializing it against
  his fair deck costs ~no combo equity, and it resolves the open "Glarb-hybrid vs Hashaton
  are redundant Thoracle decks" question — **Hashaton owns the Thoracle lane, Glarb owns
  the grind/anti-fair lane** (Thoracle direction dropped).

## The model (`vs_dragon_lab.py`)

Races our board-independent kill (grind-fortress decap CDF, lab `ct_speed_lab`, median
~T9 — **unchanged by the package**, which cuts win-more not kill pieces) against an
Ur-Dragon that's gone live and is swinging **16, +7/turn, focused on us**. Our answers:
**wrath** (resets their board, finite, drawn), **fog** (skips an attack; Constant Mists
repeatable in a 39-land + Crucible/Loam shell — the package's edge), **Maze** (passive,
neutralizes one attacker), **spot removal**. One meaningful interaction per turn; cheap
fogs partly bypass the mana tax. Priors (go-live, damage curve, reset/fog effects) are
**judgment, swept**; the kill clock is lab-sourced.

## Result — the archetype wins; the package is marginal free insurance

| Build | P(win vs Ur-Dragon) |
|---|---|
| grind-fortress, no package | **87%** |
| + Spore Frog + Constant Mists + Beast Within | **89%** |
| **Package lift** | **+2–3 pp** |

Robust across the sweep (+2 to +3), concentrated in the dangerous games — **fast go-live,
they pack counters, you brick on a wrath** — and **+0 when flooding answers** (the extra
fogs are redundant with three wraths). **Headline: Glarb-grind beats Ur-Dragon by
ARCHETYPE** (3 flying-agnostic wraths + Maze + recursion + an over-the-top ~T9 kill), not
by the 3-card package. The package is **free** (the cut cards do nothing in this matchup),
positive, and never negative — worth taking, but it's polish.

**Caveats (load-bearing):** **87% is a heads-up goldfish ceiling** — one-on-one, ignores
the other two seats; the real 4-pod number is lower. And this is a **hard archetype read**:
committing Glarb assumes he's on Ur-Dragon; if he sits down with Acererak/H&K, Glarb is the
*worst* pick (5%). **Dark Lord's Army** stays the stronger single anti-fair choice (3
sweepers + opponent-fed clock) if you want best odds / pivot resilience.

## Build applied (committed)

Deployed list promoted to the grind-fortress shell + package:
`decks/calamity-tax-20260615.txt` (old `…20260405` → `archive/old_decklists/`).

- **OUT:** Blasphemous Edict (symmetric 13-creature sac), Espers to Magicite (niche gy-hate
  copy), Doppelgang (expensive win-more — Rite + Finale stay).
- **IN:** Spore Frog (recurring Fog, owned), Constant Mists (repeatable Fog, ~$2 buy),
  Beast Within (instant destroy-any-permanent, owned).

Stays **99 + Glarb = 100**, **3/3 GCs untouched** (Seedborn Muse / Fierce Guardianship /
Demonic Tutor — none added is a GC; note Cyclonic Rift, which the old Summary referenced,
can't go in without dropping a GC). Cross-deck availability verified (Spore Frog idle;
Beast Within ×5, Crucible ×4 owned; Constant Mists the only buy). Conversion-Check re-audit
pending — kill clock cites `vs_dragon_lab` + `ct_speed_lab` (grind-fortress decap ~T9).
