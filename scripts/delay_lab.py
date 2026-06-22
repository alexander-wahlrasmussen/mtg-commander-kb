#!/usr/bin/env python3
"""delay_lab.py — answer-availability ("counter-clock") lab vs the pod's combo turn.

Post-bake-off follow-up (2026-06-12, user request). The Stage-3 clock labs
measured how fast WE kill; the other clock is how reliably we can DISRUPT the
recurring pod combo deck's T6-7 win attempt (project_pod_combo_opponent:
Ur-Dragon + Hidetsugu/Kairi/Kenrith/Kinnan shells, wins behind Grand
Abolisher). Key user correction baked into the design: **Abolisher is a drawn
card, not a constant** — so this lab measures OUR answer availability as
scenario CONDITIONALS and composes them across a swept P(Abolisher out).

SCENARIOS on the opponent's key turn K (we are assumed earlier in turn order,
so we have completed our turn K — a half-turn optimism, shared by all configs):

  A   no Abolisher out. Live: reactive answers (counters, instant removal)
      held with mana open, plus any deployed static.
  B1  Abolisher out with >=1 turn of window. Verified rules fact: Abolisher
      stops ALL our spells on their turn (not just counters). Live: deployed
      statics, OR own-turn removal on OUR turn K (kill Abolisher / the visible
      piece) followed by a held reactive answer (cost_removal + cost_react <=
      our mana — lands tapped on our turn stay tapped on theirs).
  B2  Abolisher dropped the same turn as the combo (no window). Statics only.

  P(disrupt) = (1-a)*A + a*( w*B1 + (1-w)*B2 ),  a swept 0..1, w = --window.

COVERAGE WEIGHTS — judgment parameters, printed with results, NOT measured:
the pod rotates 4 shells; Kinnan/Kenrith/Hidetsugu win through ACTIVATED
abilities (Cursed Totem / Phyrexian Revoker class works; a counterspell
cannot counter an activation), Kairi through spells/triggers.
  W_STATIC  = 0.75  (activation share, 3 of 4 known shells)
  W_REMOVAL = 0.90  (combo pieces are creatures; discount for boots/greaves)
  W_COUNTER = 0.50  (full vs spell lines, partial vs activation lines — the
                     key turn usually still casts *something*)

CEILING CONVENTIONS (same philosophy as the clock labs — trust deltas, not
absolutes): a seen singleton is a held singleton; mana = lands-only floor
(min(turn, lands seen)); we are always willing to hold mana open; the tutor
variant pays tutor + target in one turn. This lab measures answer
AVAILABILITY, not EFFECTIVENESS — a live answer does not model their backup
lines, a second protection piece, or recursion. Decap/table racing is the
other half of the matchup and lives in the *_clock_lab.py results.

CLASSIFICATION (oracle text verified via card_lookup.py / oracle dump,
2026-06-12). Excluded on verified text, per deck below: redirects (Deflecting
Swat, Bolt Bend — the pod loops aren't single-target-dependent),
combat-conditioned pieces (Dokuchi Silencer, Hope of Ghirapur), protect-own
(Siren Stormtamer, Fugitive Droid, Greaves/Boots), sorcery tempo/steal that
doesn't answer a key turn (Consuming Tide, Blatant Thievery), narrow tutors
(Demonic Counsel demon-only sans delirium, Step Through wizard-only, Lively
Dirge fetches to yard). Cost overrides documented inline.

Configs: the bake-off pick (Yuriko), the fallback (Kefka-burn), the fallback +
the 3-card Kefka-external port (-Negate -Arcane Denial -An Offer / +Phyrexian
Revoker +Volatile Stormdrake +Fire Covenant), and Kefka-external itself as the
counter-wall calibrator.

ROSTER EXTENSION (same day, user request): Lightning War / Calamity Tax /
Grand Design added for candidates-vs-roster positioning. Roster-specific
conventions, all documented judgment: 1-card-pitch and commander-conditional
free spells modelled at 0 when the commander is cheap (Azula 4 / Glarb 3 —
both reliably out by their T6); GD's Deadly Rollick kept at full cost 4
(Atraxa 7 is rarely out by T6). 2-card pitch (Commandeer) stays full-cost.
Deploy-in-advance creature answers (Glen Elendra, Ranger-Captain) modelled as
held spells at body cost — same Abolisher behaviour as counters (their
activations are opponent creature abilities on the lock turn). NOT modelled,
all UNDERSTATING the roster decks: CT's Seedborn+Glarb instant-speed
top-of-library casting (its reactive mana is far better than the lands floor),
LW's Snapcaster flashback, GD's own Grand Abolisher (protect-own, excluded by
class). LW's Emeritus of Conflict prepared-Bolt included at 2 (needs its
3rd-spell trigger — optimistic early, fine by T6). GD's Teferi static doesn't
stop a main-phase combo — only his -3 bounce counts (preempt).

Data: collection/oracle-cards.json (refreshed 2026-06-12)
Writeup: proposals/Delay_Lab_Disruption_Analysis_2026-06-12.md
"""
import argparse
import importlib.util
import random
from pathlib import Path

ROOT = Path(__file__).parent.parent
_spec = importlib.util.spec_from_file_location(
    "speed_lab_core", Path(__file__).parent / "speed_lab_core.py")
slc = importlib.util.module_from_spec(_spec); _spec.loader.exec_module(slc)
ds = slc.ds

SEED = 20260612
KS = [5, 6, 7, 8]            # the opponent's candidate key turns
A_SWEEP = [0.0, 0.25, 0.50, 0.75, 1.0]   # P(Abolisher out on the key turn)

W_STATIC, W_REMOVAL, W_COUNTER = 0.75, 0.90, 0.50

# answer spec: name -> (classes, effective_cost, tags)
#   classes subset of {"C","R","P","S"}: Counter / Reactive removal (instant) /
#   Preempt-capable on our own turn / Static. Every instant R is also P.
#   tags: "ios" instant-or-sorcery (Mystical/Solve fetchable),
#         "ublue" blue instant (Merchant Scroll fetchable).
# tutor spec: name -> (cost, filter) with filter in {"any","ios","ublue","mv2"};
#   "mv2" = transmute for mana value exactly 2 (real MV, not the override).

YURIKO = {
    "answers": {
        "Counterspell":             ({"C"}, 2, {"ios", "ublue"}),
        "Mana Drain":               ({"C"}, 2, {"ios", "ublue"}),
        "Swan Song":                ({"C"}, 1, {"ios", "ublue"}),
        "Spell Pierce":             ({"C"}, 1, {"ios", "ublue"}),
        "An Offer You Can't Refuse": ({"C"}, 1, {"ios", "ublue"}),
        "Dispel":                   ({"C"}, 1, {"ios", "ublue"}),
        "Commandeer":               ({"C"}, 7, {"ios", "ublue"}),  # pitch-cast ignored: underestimates
        "Go for the Throat":        ({"R", "P"}, 2, {"ios"}),
        "Fatal Push":               ({"R", "P"}, 1, {"ios"}),      # MV<=2 catches Kinnan/Abolisher
        "Murderous Cut":            ({"R", "P"}, 3, {"ios"}),      # delve override (MV5; Yuriko bins fast)
        "Curtains' Call":           ({"R", "P"}, 3, {"ios"}),      # undaunted, 3 opponents (MV6)
        "Bloodchief's Thirst":      ({"P"}, 1, {"ios"}),           # SORCERY: preempt only; unkicked hits MV<=2
    },
    "tutors": {
        "Demonic Tutor": (2, "any"), "Wishclaw Talisman": (4, "any"),  # cast 2 + activate 1+tap
        "Mystical Tutor": (1, "ios"), "Merchant Scroll": (2, "ublue"),
        "Solve the Equation": (3, "ios"), "Lim-Dûl's Vault": (2, "any"),  # dig-to-top, modelled broad
    },
}

HASHATON = {
    # NEW 2026-06-14: the Thoracle-Hashaton benchmark target. Counter+removal heavy,
    # 0 statics (same structural Abolisher gap as Yuriko), but a DEEPER tutor suite.
    # NOTE: this lab measures DISRUPT-THE-POD only. Hashaton's distinctive resilience
    # (protect-own combo: counter-dodging discard-deploy of Thoracle, Razaketh
    # recursion, redundant oracles, Silence) is a DIFFERENT axis this lab does not see.
    "answers": {
        "Counterspell":              ({"C"}, 2, {"ios", "ublue"}),
        "Mana Drain":                ({"C"}, 2, {"ios", "ublue"}),
        "Swan Song":                 ({"C"}, 1, {"ios", "ublue"}),
        "An Offer You Can't Refuse": ({"C"}, 1, {"ios", "ublue"}),
        "Pact of Negation":          ({"C"}, 0, {"ios", "ublue"}),   # free on their turn
        "Dovin's Veto":              ({"C"}, 2, {"ios", "ublue"}),
        "Flusterstorm":              ({"C"}, 1, {"ios", "ublue"}),
        "Delay":                     ({"C"}, 2, {"ios", "ublue"}),
        "Spell Pierce":              ({"C"}, 1, {"ios", "ublue"}),
        "Drown in the Loch":         ({"C", "R", "P"}, 2, {"ios", "ublue"}),  # both modes; yard size not modelled
        "Swords to Plowshares":      ({"R", "P"}, 1, {"ios"}),
        "Path to Exile":             ({"R", "P"}, 1, {"ios"}),
        "Fatal Push":                ({"R", "P"}, 1, {"ios"}),       # MV<=2: Kinnan/Abolisher
        "Go for the Throat":         ({"R", "P"}, 2, {"ios"}),
        "Cut Down":                  ({"R", "P"}, 2, {"ios"}),       # P+T<=5: Abolisher 2/2 + dorks
        "Prismatic Ending":          ({"P"}, 3, {"ios"}),            # SORCERY: preempt only
        "Toxic Deluge":              ({"P"}, 3, {"ios"}),            # X=2 wrath
        "Supreme Verdict":           ({"P"}, 4, {"ios"}),
    },
    "tutors": {
        "Demonic Tutor": (2, "any"), "Vampiric Tutor": (1, "any"),  # to-top, modelled same-turn (cf. Mystical)
        "Grim Tutor": (3, "any"), "Wishclaw Talisman": (4, "any"),
        "Diabolic Intent": (2, "any"), "Beseech the Mirror": (4, "any"),
        "Solve the Equation": (3, "ios"), "Merchant Scroll": (3, "ublue"),
    },
}

KEFKA_BURN = {
    "answers": {
        "Counterspell":             ({"C"}, 2, {"ios"}),
        "Negate":                   ({"C"}, 2, {"ios"}),
        "Swan Song":                ({"C"}, 1, {"ios"}),
        "An Offer You Can't Refuse": ({"C"}, 1, {"ios"}),
        "Arcane Denial":            ({"C"}, 2, {"ios"}),
        "Drown in the Loch":        ({"C", "R", "P"}, 2, {"ios"}),  # genuinely both modes
        "Bedevil":                  ({"R", "P"}, 3, {"ios"}),
        "Terminate":                ({"R", "P"}, 2, {"ios"}),
        "Go for the Throat":        ({"R", "P"}, 2, {"ios"}),
        "Infernal Grasp":           ({"R", "P"}, 2, {"ios"}),
        "Rakdos Charm":             ({"R", "P"}, 2, {"ios"}),
        "Chaos Warp":               ({"R", "P"}, 3, {"ios"}),
        "Bloodchief's Thirst":      ({"P"}, 1, {"ios"}),
        "Blasphemous Act":          ({"P"}, 5, {"ios"}),            # cost-reduction judgment override (MV9)
        "Cursed Totem":             ({"S"}, 2, set()),
    },
    "tutors": {
        "Demonic Tutor": (2, "any"), "Diabolic Tutor": (4, "any"),
        "Mastermind's Acquisition": (4, "any"),
    },
}

# the 3-card port from the Kefka-external scout (availability checked 2026-06-12:
# Stormdrake owned free / Revoker + Fire Covenant = buys, Genome's Covenant protected)
PORT_REMOVES = ["Negate", "Arcane Denial", "An Offer You Can't Refuse"]
PORT_ADDS = {
    "Phyrexian Revoker":   ({"S"}, 2, set()),        # names Kinnan/Kenrith/Hidetsugu (informed by key turn)
    "Volatile Stormdrake": ({"P"}, 2, set()),        # own-turn theft; can take Abolisher itself (MV2 <= 4 energy)
    "Fire Covenant":       ({"R", "P"}, 3, {"ios"}), # X-life multi-kill: Abolisher AND a dork in one instant
}

KEFKA_EXT = {
    "answers": {
        "An Offer You Can't Refuse": ({"C"}, 1, {"ios"}),
        "Arcane Denial":            ({"C"}, 2, {"ios"}),
        "Delay":                    ({"C"}, 2, {"ios"}),
        "Dispel":                   ({"C"}, 1, {"ios"}),
        "Drown in the Loch":        ({"C", "R", "P"}, 2, {"ios"}),
        "Memory Lapse":             ({"C"}, 2, {"ios"}),
        "Miscast":                  ({"C"}, 1, {"ios"}),
        "Spell Pierce":             ({"C"}, 1, {"ios"}),
        "Malevolent Hermit":        ({"C"}, 2, set()),  # sac = OUR creature ability on THEIR turn: Abolisher-dead too
        "Lightning Bolt":           ({"R", "P"}, 1, {"ios"}),
        "Fatal Push":               ({"R", "P"}, 1, {"ios"}),
        "Abrade":                   ({"R", "P"}, 2, {"ios"}),
        "Fire Covenant":            ({"R", "P"}, 3, {"ios"}),
        "Suspend":                  ({"R", "P"}, 1, {"ios"}),   # temporary exile: answers the key turn
        "Snapback":                 ({"R", "P"}, 1, {"ios"}),   # pitch override (MV2): bounce, tempo only
        "Unsubstantiate":           ({"R", "P"}, 2, {"ios"}),
        "Retraction Helix":         ({"R"}, 1, {"ios"}),        # needs an untapped creature; reactive only
        "Volatile Stormdrake":      ({"P"}, 2, set()),
        "Phyrexian Revoker":        ({"S"}, 2, set()),
    },
    "tutors": {
        "Wishclaw Talisman": (4, "any"),
        "Ringsight": (3, "any"),       # needs a legendary creature out; Grixis shares broadly — optimistic
        "Shred Memory": (3, "mv2"),    # transmute: MV-2 targets only (Revoker, Counterspell-class)
    },
}


LIGHTNING_WAR = {
    "answers": {
        "Fierce Guardianship":      ({"C"}, 0, {"ios", "inst"}),   # Azula (4) out by their T6
        "Force of Negation":        ({"C"}, 0, {"ios", "inst"}),   # 1-card pitch on their turn
        "Swan Song":                ({"C"}, 1, {"ios", "inst"}),
        "Stubborn Denial":          ({"C"}, 1, {"ios", "inst"}),   # Azula = ferocious
        "Delay":                    ({"C"}, 2, {"ios", "inst"}),
        "Three Steps Ahead":        ({"C"}, 2, {"ios", "inst"}),   # counter mode {1}{U}
        "Narset's Reversal":        ({"C"}, 2, {"ios", "inst"}),   # copy+bounce their key sorcery
        "Hullbreaker Horror":       ({"C"}, 7, {"inst"}),          # flash; repeatable spell-bounce
        "Electrodominance":         ({"R", "P"}, 4, {"ios", "inst"}),  # X=2 kills Abolisher/Kinnan
        "Comet Storm":              ({"R", "P"}, 4, {"ios", "inst"}),
        "V.A.T.S.":                 ({"R", "P"}, 4, {"ios", "inst"}),  # split second
        "Deadly Rollick":           ({"R", "P"}, 0, {"ios", "inst"}),
        "Snap":                     ({"R", "P"}, 2, {"ios", "inst"}),
        "Sink into Stupor":         ({"R", "P"}, 3, {"ios", "inst"}),
        "March of Swirling Mist":   ({"R", "P"}, 2, {"ios", "inst"}),  # X=1 phases out the piece
        "Nowhere to Run":           ({"R", "P"}, 2, {"inst"}),     # flash; -3/-3 kills the 2/2s
        "Vendilion Clique":         ({"R", "P"}, 3, {"inst"}),     # flash hand-strip (soft)
        "Emeritus of Conflict":     ({"R", "P"}, 2, set()),        # prepared Bolt (conditional)
        "Toxic Deluge":             ({"P"}, 3, {"ios"}),
        "Banefire":                 ({"P"}, 3, {"ios"}),           # X=2
        "Crackle with Power":       ({"P"}, 5, {"ios"}),           # X=1
        "Opposition Agent":         ({"S"}, 3, {"inst"}),          # flash; hoses their tutors
    },
    "tutors": {
        "Mystical Teachings": (4, "inst"), "Waterlogged Teachings": (4, "inst"),
        "Emeritus of Woe": (6, "any"),    # SOS body 4 + prepared Demonic Tutor copy 2
    },
}

CALAMITY_TAX = {
    "answers": {
        "Pact of Negation":         ({"C"}, 0, {"ios", "inst"}),
        "Force of Negation":        ({"C"}, 0, {"ios", "inst"}),
        "Fierce Guardianship":      ({"C"}, 0, {"ios", "inst"}),   # Glarb (3) out by their T6
        "Mana Drain":               ({"C"}, 2, {"ios", "inst"}),
        "Swan Song":                ({"C"}, 1, {"ios", "inst"}),
        "Venser, Shaper Savant":    ({"C", "R", "P"}, 4, {"crea"}),  # flash; bounce spell OR permanent
        "Deadly Rollick":           ({"R", "P"}, 0, {"ios", "inst"}),
        "Submerge":                 ({"R", "P"}, 5, {"ios", "inst"}),  # free mode (their Forest) not credited
        "Espers to Magicite":       ({"R", "P"}, 4, {"ios", "inst"}),  # yard exile vs recursion lines
        "V.A.T.S.":                 ({"R", "P"}, 4, {"ios", "inst"}),
        "Toxic Deluge":             ({"P"}, 3, {"ios"}),
        "Blasphemous Edict":        ({"P"}, 5, {"ios"}),
        "Culling Ritual":           ({"P"}, 4, {"ios"}),           # sweeps MV<=2 setups
        "Massacre Wurm":            ({"P"}, 6, {"crea"}),
        "The Meathook Massacre":    ({"P"}, 4, {"ios"}),           # X=2
    },
    "tutors": {"Demonic Tutor": (2, "any")},
}

GRAND_DESIGN = {
    "answers": {
        "Force of Will":            ({"C"}, 0, {"ios", "inst"}),
        "Force of Negation":        ({"C"}, 0, {"ios", "inst"}),
        "Counterspell":             ({"C"}, 2, {"ios", "inst"}),
        "Mana Drain":               ({"C"}, 2, {"ios", "inst"}),
        "Dovin's Veto":             ({"C"}, 2, {"ios", "inst"}),
        "Swan Song":                ({"C"}, 1, {"ios", "inst"}),
        "Glen Elendra Archmage":    ({"C"}, 4, {"crea"}),          # deploy-in-advance sac counter
        "Ranger-Captain of Eos":    ({"C"}, 3, {"crea"}),          # sac: no noncreature spells this turn
        "Deadly Rollick":           ({"R", "P"}, 4, {"ios", "inst"}),  # Atraxa (7) rarely out: full cost
        "Path to Exile":            ({"R", "P"}, 1, {"ios", "inst"}),
        "Swords to Plowshares":     ({"R", "P"}, 1, {"ios", "inst"}),
        "Assassin's Trophy":        ({"R", "P"}, 2, {"ios", "inst"}),
        "Generous Gift":            ({"R", "P"}, 3, {"ios", "inst"}),
        "Cyclonic Rift":            ({"R", "P"}, 2, {"ios", "inst"}),
        "Toxic Deluge":             ({"P"}, 3, {"ios"}),
        "Teferi, Time Raveler":     ({"P"}, 3, set()),             # -3 bounce; static irrelevant to their main phase
        "Elesh Norn, Mother of Machines": ({"S"}, 5, {"crea"}),    # opponents' ETB triggers don't trigger
    },
    "tutors": {"Eladamri's Call": (2, "crea"), "Chord of Calling": (7, "crea")},
}


# ===========================================================================
# ROSTER DISRUPTION SUITES (2026-06-15) — the other 13 active decks, so the
# pod_gauntlet's disruption is MEASURED for all 16, not class-bucketed for 13
# (gauntlet limitation #2). Answers harvested by the delay_lab interaction
# inventory pattern (broad, not exhaustive — a missed answer UNDERSTATES) and
# oracle-verified 2026-06-15. Classification follows this lab's engine: R
# (instant removal) and C (counters) drive scenario A; P-only sorcery
# sweepers/edicts contribute only via the preempt chain; statics survive
# Abolisher. EXCLUDED per the established rules: redirects (Deflecting Swat,
# Imp's Mischief), protect-own (Veil of Summer — anti-counter + hexproof, not a
# combo stop), Snapcaster (yard-dependent value, not modelled — understates).
# Fierce Guardianship / Deadly Rollick free (cost 0) only behind a cheap,
# reliably-cast commander (<=4, like Azula/Glarb); full cost otherwise.
# Tutors are left empty: the gauntlet reads the DRAWN (no-tutor) composed
# value (its existing convention), so the +tutors ceiling isn't needed here.
# Pyroblast/REB are blue-conditional (the pod is partly blue); credited as
# counters at face, discounted by W_COUNTER. Edicts (Plaguecrafter/Fleshbag)
# are dodgeable; Pernicious Deed's crack is an ACTIVATED ability -> Abolisher-
# blocked on their turn, so it is preempt-only (P).
# ===========================================================================

def _A(*rows):
    return {"answers": dict(rows), "tutors": {}}

GENOME = _A(  # Kuja 4 -> Rollick free; thin (combo deck)
    ("Deadly Rollick", ({"R", "P"}, 0, {"ios", "inst"})),
    ("Chaos Warp", ({"R", "P"}, 3, {"ios"})),
    ("Blasphemous Act", ({"P"}, 5, {"ios"})))           # cost-reduction override

RADIATION = _A(  # Wise Mothman (BUG); counter + instant-removal heavy
    ("Counterspell", ({"C"}, 2, {"ios", "ublue"})),
    ("Swan Song", ({"C"}, 1, {"ios", "ublue"})),
    ("An Offer You Can't Refuse", ({"C"}, 1, {"ios", "ublue"})),
    ("Force of Negation", ({"C"}, 0, {"ios", "ublue", "inst"})),
    ("Drown in the Loch", ({"C", "R", "P"}, 2, {"ios", "ublue"})),
    ("Assassin's Trophy", ({"R", "P"}, 2, {"ios"})),
    ("Beast Within", ({"R", "P"}, 3, {"ios"})),
    ("Pongify", ({"R", "P"}, 1, {"ios"})),
    ("Cyclonic Rift", ({"R", "P"}, 2, {"ios"})),        # single-target bounce
    ("Toxic Deluge", ({"P"}, 3, {"ios"})))

REPLICATION = _A(  # Satya 4 -> FG free; deep blue control suite
    ("Counterspell", ({"C"}, 2, {"ios", "ublue"})),
    ("Swan Song", ({"C"}, 1, {"ios", "ublue"})),
    ("An Offer You Can't Refuse", ({"C"}, 1, {"ios", "ublue"})),
    ("Arcane Denial", ({"C"}, 2, {"ios", "ublue"})),
    ("Fierce Guardianship", ({"C"}, 0, {"ios", "ublue", "inst"})),
    ("Abrade", ({"R", "P"}, 2, {"ios"})),
    ("Chaos Warp", ({"R", "P"}, 3, {"ios"})),
    ("Generous Gift", ({"R", "P"}, 3, {"ios"})),
    ("Path to Exile", ({"R", "P"}, 1, {"ios"})),
    ("Pongify", ({"R", "P"}, 1, {"ios"})),
    ("Swords to Plowshares", ({"R", "P"}, 1, {"ios"})),
    ("Cyclonic Rift", ({"R", "P"}, 2, {"ios"})))

LOREHOLD = _A(  # Quintorius (RW) — white removal only, no counters
    ("Path to Exile", ({"R", "P"}, 1, {"ios"})),
    ("Swords to Plowshares", ({"R", "P"}, 1, {"ios"})),
    ("Generous Gift", ({"R", "P"}, 3, {"ios"})))

EARTHBEND = _A(  # Toph (Naya-ish) — removal + blue-conditional REB/Pyroblast
    ("Path to Exile", ({"R", "P"}, 1, {"ios"})),
    ("Swords to Plowshares", ({"R", "P"}, 1, {"ios"})),
    ("Generous Gift", ({"R", "P"}, 3, {"ios"})),
    ("Beast Within", ({"R", "P"}, 3, {"ios"})),
    ("Pyroblast", ({"C", "R", "P"}, 1, {"ios"})),       # blue-only (pod is partly blue)
    ("Red Elemental Blast", ({"C", "R", "P"}, 1, {"ios"})))

EXILES = _A(  # Zuko 3 -> Rollick free; Mardu removal/sweepers, no hard counters
    ("Path to Exile", ({"R", "P"}, 1, {"ios"})),
    ("Swords to Plowshares", ({"R", "P"}, 1, {"ios"})),
    ("Generous Gift", ({"R", "P"}, 3, {"ios"})),
    ("Abrade", ({"R", "P"}, 2, {"ios"})),
    ("Chaos Warp", ({"R", "P"}, 3, {"ios"})),
    ("Deadly Rollick", ({"R", "P"}, 0, {"ios", "inst"})),
    ("Blasphemous Act", ({"P"}, 5, {"ios"})),
    ("Toxic Deluge", ({"P"}, 3, {"ios"})))

ZEROSUM = _A(  # Witherbloom 8 -> Rollick full cost; Golgari removal + Deed
    ("Assassin's Trophy", ({"R", "P"}, 2, {"ios"})),
    ("Beast Within", ({"R", "P"}, 3, {"ios"})),
    ("Deadly Rollick", ({"R", "P"}, 4, {"ios", "inst"})),
    ("Toxic Deluge", ({"P"}, 3, {"ios"})),
    ("Pernicious Deed", ({"P"}, 4, set())))             # crack is activated -> Abolisher-blocked

CURSE = _A(  # Scarab God 5 -> FG full cost (not reliably out by their T6)
    ("Counterspell", ({"C"}, 2, {"ios", "ublue"})),
    ("An Offer You Can't Refuse", ({"C"}, 1, {"ios", "ublue"})),
    ("Arcane Denial", ({"C"}, 2, {"ios", "ublue"})),
    ("Force of Negation", ({"C"}, 0, {"ios", "ublue", "inst"})),
    ("Fierce Guardianship", ({"C"}, 3, {"ios", "ublue", "inst"})),
    ("Go for the Throat", ({"R", "P"}, 2, {"ios"})),
    ("Rapid Hybridization", ({"R", "P"}, 1, {"ios"})),
    ("Cyclonic Rift", ({"R", "P"}, 2, {"ios"})),
    ("Fleshbag Marauder", ({"P"}, 3, {"crea"})),        # edict, dodgeable
    ("Toxic Deluge", ({"P"}, 3, {"ios"})))

BUMBLE = _A(  # Ms. Bumbleflower (Bant) — white removal + a counter
    ("An Offer You Can't Refuse", ({"C"}, 1, {"ios", "ublue"})),
    ("Path to Exile", ({"R", "P"}, 1, {"ios"})),
    ("Swords to Plowshares", ({"R", "P"}, 1, {"ios"})),
    ("Generous Gift", ({"R", "P"}, 3, {"ios"})),
    ("Beast Within", ({"R", "P"}, 3, {"ios"})),
    ("Pongify", ({"R", "P"}, 1, {"ios"})),
    ("Snap", ({"R", "P"}, 2, {"ios"})))                 # bounce, tempo

ELDRAZI = _A(  # Maelstrom Wanderer (Temur big-mana) — minimal interaction
    ("Beast Within", ({"R", "P"}, 3, {"ios"})),
    ("Chaos Warp", ({"R", "P"}, 3, {"ios"})))

DARKLORD = _A(  # Sauron 6 -> FG/Rollick full cost; Grixis control, deep suite
    ("Counterspell", ({"C"}, 2, {"ios", "ublue"})),
    ("Mana Drain", ({"C"}, 2, {"ios", "ublue"})),
    ("Swan Song", ({"C"}, 1, {"ios", "ublue"})),
    ("An Offer You Can't Refuse", ({"C"}, 1, {"ios", "ublue"})),
    ("Arcane Denial", ({"C"}, 2, {"ios", "ublue"})),
    ("Force of Negation", ({"C"}, 0, {"ios", "ublue", "inst"})),
    ("Go for the Throat", ({"R", "P"}, 2, {"ios"})),
    ("Chaos Warp", ({"R", "P"}, 3, {"ios"})),
    ("Cyclonic Rift", ({"R", "P"}, 2, {"ios"})),
    ("Deadly Rollick", ({"R", "P"}, 4, {"ios", "inst"})),
    ("Blasphemous Act", ({"P"}, 5, {"ios"})),
    ("Toxic Deluge", ({"P"}, 3, {"ios"})))

DIMINISHING = _A(  # Teysa 4 (Orzhov aristocrats) — removal + edicts + sweepers
    ("Path to Exile", ({"R", "P"}, 1, {"ios"})),
    ("Swords to Plowshares", ({"R", "P"}, 1, {"ios"})),
    ("Generous Gift", ({"R", "P"}, 3, {"ios"})),
    ("Plaguecrafter", ({"P"}, 3, {"crea"})),            # edict, dodgeable
    ("Fleshbag Marauder", ({"P"}, 3, {"crea"})),
    ("The Meathook Massacre", ({"P"}, 4, {"ios"})),     # X=2 wrath
    ("Toxic Deluge", ({"P"}, 3, {"ios"})))

CRYSTAL = _A(  # Golbez 2 -> FG free; Dimir, lean counter + sweeper
    ("Mana Drain", ({"C"}, 2, {"ios", "ublue"})),
    ("An Offer You Can't Refuse", ({"C"}, 1, {"ios", "ublue"})),
    ("Arcane Denial", ({"C"}, 2, {"ios", "ublue"})),
    ("Fierce Guardianship", ({"C"}, 0, {"ios", "ublue", "inst"})),
    ("Toxic Deluge", ({"P"}, 3, {"ios"})))

# gauntlet slug -> (decklist filename under decks/, config). All 16 active decks:
# the 13 above + the three delay_lab already measured (reuse their configs/paths).
ROSTER = {
    "genome_project": ("the-genome-project-20260510.txt", GENOME),
    "radiation_sickness": ("radiation-sickness-20260615.txt", RADIATION),
    "replication_crisis": ("the-replication-crisis-20260622.txt", REPLICATION),
    "lorehold_spirits": ("lorehold-spirit-20260503-154449.txt", LOREHOLD),
    "earthbend_the_meta": ("earthbend-the-meta-20260404-075423.txt", EARTHBEND),
    "exiles_return": ("the-exiles-return-20260417-194010.txt", EXILES),
    "zero_sum_game": ("zero-sum-game-20260619.txt", ZEROSUM),
    "curse_of_the_scarab": ("curse-of-the-scarab-20260510-215526.txt", CURSE),
    "bumbleflower": ("this-bunny-goes-to-market-20260404-080311.txt", BUMBLE),
    "eldrazi_stampede": ("eldrazi-stampede-chaos-20260306-133311.txt", ELDRAZI),
    "dark_lords_army": ("the-dark-lords-army-20260417-211206.txt", DARKLORD),
    "diminishing_returns": ("diminishing-returns-20260505.txt", DIMINISHING),
    "crystal_sickness": ("crystal-sickness-20260322-152311.txt", CRYSTAL),
    "lightning_war": ("../archive/old_decklists/lightning-war-20260614.txt", LIGHTNING_WAR),
    "calamity_tax": ("calamity-tax-20260405-061741.txt", CALAMITY_TAX),
    "grand_design": ("the-grand-design-20260502.txt", GRAND_DESIGN),
}


def fits(filt, entry, real_mv):
    classes, cost, tags = entry
    if filt == "any":
        return True
    if filt == "ios":
        return "ios" in tags
    if filt == "ublue":
        return "ublue" in tags
    if filt == "inst":
        return "inst" in tags
    if filt == "crea":
        return "crea" in tags
    if filt == "mv2":
        return real_mv == 2
    return False


def check_names(label, lib, spec):
    names = {nm for nm, _ in lib}
    missing = [n for n in list(spec["answers"]) + list(spec["tutors"]) if n not in names]
    if missing:
        raise SystemExit(f"{label}: spec names not in parsed deck: {missing}")


def simulate(label, lib, spec, trials, rng, window):
    answers, tutors = spec["answers"], spec["tutors"]
    mv = {nm: rec["cmc"] for nm, rec in lib if nm in answers}
    cnt = {k: {"C": 0, "R": 0, "S": 0, "PR": 0, "TC": 0, "TR": 0, "TS": 0} for k in KS}
    comp = {k: {a: [0.0, 0.0] for a in A_SWEEP} for k in KS}   # [drawn, with-tutors]

    for _ in range(trials):
        deck = lib[:]
        hand, _m = ds.opening_hand(deck, rng)
        seen, lands = set(), 0
        for nm, rec in hand:
            seen.add(nm)
            if ds.is_land(rec):
                lands += 1
        ptr = 7
        for K in range(2, max(KS) + 1):
            if ptr < len(deck):
                nm, rec = deck[ptr]; ptr += 1
                seen.add(nm)
                if ds.is_land(rec):
                    lands += 1
            if K not in cnt:
                continue
            M = min(K, lands)
            held = [(n,) + answers[n] for n in seen if n in answers]
            C = any("C" in c and cost <= M for _, c, cost, _t in held)
            R = any("R" in c and cost <= M for _, c, cost, _t in held)
            S = any("S" in c and cost <= M for _, c, cost, _t in held)
            PRr = PRc = False
            pre = [(n, cost) for n, c, cost, _t in held if "P" in c]
            for pn, pc in pre:
                for qn, qc, qcost, _t in held:
                    if qn == pn or pc + qcost > M:
                        continue
                    if "R" in qc:
                        PRr = True
                    if "C" in qc:
                        PRc = True
            # tutor variant: fetch an unseen answer, tutor + target in one payment
            TC, TR, TS = C, R, S
            tut = [(n, tutors[n]) for n in seen if n in tutors]
            if tut:
                unseen = [(n,) + answers[n] for n in answers if n not in seen]
                for _tn, (tc, filt) in tut:
                    for n, c, cost, tags in unseen:
                        if tc + cost <= M and fits(filt, (c, cost, tags), mv[n]):
                            TC = TC or "C" in c
                            TR = TR or "R" in c
                            TS = TS or "S" in c
            for key, val in (("C", C), ("R", R), ("S", S), ("PR", PRr or PRc),
                             ("TC", TC), ("TR", TR), ("TS", TS)):
                cnt[K][key] += val
            effA = 1 - (1 - W_STATIC * S) * (1 - W_REMOVAL * R) * (1 - W_COUNTER * C)
            effA_t = 1 - (1 - W_STATIC * TS) * (1 - W_REMOVAL * TR) * (1 - W_COUNTER * TC)
            effB1 = 1 - (1 - W_STATIC * S) * (1 - W_REMOVAL * PRr) * (1 - W_COUNTER * PRc)
            effB1_t = 1 - (1 - W_STATIC * TS) * (1 - W_REMOVAL * PRr) * (1 - W_COUNTER * PRc)
            for a in A_SWEEP:
                comp[K][a][0] += (1 - a) * effA + a * (window * effB1 + (1 - window) * W_STATIC * S)
                comp[K][a][1] += (1 - a) * effA_t + a * (window * effB1_t + (1 - window) * W_STATIC * TS)

    nC = sum(1 for v in answers.values() if "C" in v[0])
    nR = sum(1 for v in answers.values() if "R" in v[0])
    nS = sum(1 for v in answers.values() if "S" in v[0])
    nP = sum(1 for v in answers.values() if v[0] == {"P"})
    print(f"\n== {label} ==")
    print(f"  suite: {nC} counters / {nR} instant removal / {nP} preempt-only / "
          f"{nS} statics ; {len(tutors)} tutors")
    print("  measured availability, % of games (drawn-only):"
          + "".join(f"   their T{k}" for k in KS))
    rows = [("counter held + mana open  (C)", "C"), ("instant removal held      (R)", "R"),
            ("static deployed           (S)", "S"), ("preempt->reactive chain  (B1)", "PR"),
            ("C with tutors", "TC"), ("R with tutors", "TR"), ("S with tutors", "TS")]
    for txt, key in rows:
        print("    " + txt.ljust(34)
              + "".join(f"{100.0 * cnt[k][key] / trials:10.0f}" for k in KS))
    print(f"  composed P(disrupt their key turn)  [w(indow)={window}]:")
    print("    " + "P(Abolisher out) ->".ljust(34)
          + "".join(f"{int(a * 100):9d}%" for a in A_SWEEP))
    for k in (6, 7):
        for j, lab in ((0, "drawn"), (1, "+tutors")):
            print(f"    their T{k} {lab}".ljust(38)
                  + "".join(f"{100.0 * comp[k][a][j] / trials:10.0f}" for a in A_SWEEP))
    return comp


def emit_json(index, aliases, trials):
    """Run every ROSTER deck and write the DRAWN composed P(disrupt their T6/T7) across the
    Abolisher a-grid to analysis/delay_disruption.json — consumed by pod_gauntlet.py so the
    matchup disruption is MEASURED for all 16 decks, not class-bucketed for 13 (limitation #2)."""
    import json as _json
    print(f"emit-json — composing measured disruption for {len(ROSTER)} decks "
          f"(trials={trials}; drawn-only is what the gauntlet reads)\n")
    out = {}
    for slug, (fname, spec) in ROSTER.items():
        lib, _ = slc.load_parsed(ROOT / "decks" / fname, index, aliases, warn=False)
        names = {nm for nm, _ in lib}      # parsed MAINDECK is ground truth (drops sideboard)
        drop = [n for n in list(spec["answers"]) + list(spec["tutors"]) if n not in names]
        spec_f = {"answers": {n: v for n, v in spec["answers"].items() if n in names},
                  "tutors": {n: v for n, v in spec["tutors"].items() if n in names}}
        comp = simulate(slug, lib, spec_f, trials, random.Random(SEED), 0.5)
        if drop:
            print(f"    (dropped — not in {fname} maindeck: {drop})")
        out[slug] = {str(k): [round(100.0 * comp[k][a][0] / trials, 1) for a in A_SWEEP]
                     for k in (6, 7)}
    path = ROOT / "analysis" / "delay_disruption.json"
    path.write_text(_json.dumps(out, indent=2), encoding="utf-8")
    print(f"\n  wrote {path.relative_to(ROOT)}  (T6/T7 drawn P(disrupt) over a-grid "
          f"{A_SWEEP}; pod_gauntlet reads it)")


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--trials", type=int, default=20000)
    ap.add_argument("--seed", type=int, default=SEED)
    ap.add_argument("--window", type=float, default=0.5,
                    help="P(Abolisher deployed >=1 turn before the combo | out)")
    ap.add_argument("--emit-json", action="store_true",
                    help="write analysis/delay_disruption.json for all 16 (pod_gauntlet reads it)")
    args = ap.parse_args()
    rng = random.Random(args.seed)
    index = ds.load_oracle_index()
    aliases = ds.load_reskin_aliases()
    if args.emit_json:
        emit_json(index, aliases, args.trials)
        return

    cons = ROOT / "decks" / "considering"
    dks = ROOT / "decks"

    def L(path):
        """Load a decklist, or skip it if archived since the bake-off."""
        try:
            return slc.load_parsed(path, index, aliases)[0]
        except FileNotFoundError:
            print(f"  (skip: {path.name} not found — archived since the bake-off)")
            return None

    hsh = L(cons / "hashaton-thoracle-20260614.txt")
    yur = L(cons / "insider-trading-20260612.txt")
    kfk = L(cons / "forced-liquidation-20260612.txt")
    ext = L(cons / "kefka-external-20260612.txt")
    port = slc.build_lib(kfk, index, PORT_REMOVES, list(PORT_ADDS)) if kfk else None
    burn_port = {"answers": {n: v for n, v in KEFKA_BURN["answers"].items()
                             if n not in PORT_REMOVES} | PORT_ADDS,
                 "tutors": KEFKA_BURN["tutors"]}
    lw = L(ROOT / "archive" / "old_decklists" / "lightning-war-20260614.txt")
    cal = L(dks / "calamity-tax-20260405-061741.txt")
    gd = L(dks / "the-grand-design-20260502.txt")

    raw_configs = [
        ("Hashaton / Thoracle (NEW — benchmark target)", hsh, HASHATON),
        ("Yuriko / Insider Trading (the pick)", yur, YURIKO),
        ("Kefka-burn / Forced Liquidation (fallback)", kfk, KEFKA_BURN),
        ("Kefka-burn + 3-card port (-Negate -ArcDenial -AnOffer "
         "/ +Revoker +Stormdrake +FireCov)", port, burn_port),
        ("Kefka-external (counter-wall calibrator)", ext, KEFKA_EXT),
        ("ROSTER: Lightning War (19/20, clock T6-7 goldfish)", lw, LIGHTNING_WAR),
        ("ROSTER: Calamity Tax (18/20, clock T7-9 goldfish)", cal, CALAMITY_TAX),
        ("ROSTER: Grand Design (19/20, clock T10 decap lab)", gd, GRAND_DESIGN),
    ]
    configs = [c for c in raw_configs if c[1] is not None]
    print(f"delay_lab — trials={args.trials} seed={args.seed} window={args.window}")
    print(f"weights (judgment): static {W_STATIC} / removal {W_REMOVAL} / counter {W_COUNTER}")
    for label, lib, spec in configs:
        check_names(label, lib, spec)
        simulate(label, lib, spec, args.trials, random.Random(args.seed), args.window)


if __name__ == "__main__":
    main()
