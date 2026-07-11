#!/usr/bin/env python3
"""clock_check.py — flag Summary Clock: citations that DRIFTED from the labs.

Backlog #2. `validate.py` check #4 verifies a clock citation EXISTS; this one
verifies it is still TRUE. Our #1 recurring failure is clock claims drifting
from reality (7 of 8 hand-estimates were falsified) — and a Summary can also go
stale after its deck changes and re-labs to a different median.

SOURCE OF TRUTH = `analysis/pod_gauntlet_clocks.json`, the aggregated decap/table
medians harvested from every `*_clock_lab.py` by `pod_gauntlet.py --refresh`
(the practical realisation of "labs emit JSON {decap,table,never}"). Refresh it,
then run this. For each active-roster deck we parse the canonical
"Kill Window / Clock:" line of its Summary, pull the cited decap and table turns,
and compare to the lab median:

    OK       within TOL turns of the lab median (or both open-ended "never/T+")
    DRIFT    >= TOL turns off — the Summary's clock no longer matches the lab
    UNPARSED couldn't read a turn out of the line (shown for a human to eyeball)

A LINT, NOT A GATE: parsing prose clock lines (ranges, reversed decap/table
order, "T12+") is heuristic, so the raw line is printed with every finding and
DRIFT is a WARNING by default. `--strict` exits non-zero on any DRIFT for CI.
Only the canonical citation line is checked — the historical "Goldfish T7-9"
prose (usually already marked falsified) is deliberately ignored.

Usage
    python scripts/pod_gauntlet.py --refresh   # 1. re-harvest the lab medians
    python scripts/clock_check.py              # 2. lint the Summary clocks
    python scripts/clock_check.py --strict     # exit 1 on any DRIFT
"""
import argparse
import json
import re
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CLOCKS_JSON = ROOT / "analysis" / "pod_gauntlet_clocks.json"
MATRIX = ROOT / "Pod_Matchup_Matrix.md"
TOL = 2                      # turns of slack before a citation counts as drifted

for _s in (sys.stdout, sys.stderr):           # echo arbitrary doc lines safely
    if hasattr(_s, "reconfigure"):
        try:
            _s.reconfigure(encoding="utf-8", errors="replace")
        except (ValueError, OSError):
            pass

# slug (pod_gauntlet) -> Summary filename. Active roster only; candidate decks
# (decks/considering/) live in the bake-off docs, not these Summaries.
SUMMARY = {
    "genome_project": "The_Genome_Project_Summary.md",
    "radiation_sickness": "Radiation_Sickness_Summary.md",
    "replication_crisis": "The_Replication_Crisis_Summary.md",
    "lorehold_spirits": "Lorehold_Spirits_Summary.md",
    "exiles_return": "The_Exiles_Return_Summary.md",
    "zero_sum_game": "Zero_Sum_Game_Summary.md",
    "curse_of_the_scarab": "Curse_of_the_Scarab_Summary.md",
    "bumbleflower": "Ms_Bumbleflower_Summary.md",
    "eldrazi_stampede": "Eldrazi_Stampede_Chaos_Summary.md",
    "dark_lords_army": "The_Dark_Lord_s_Army_Summary.md",
    "lightning_war": "Lightning_War_Summary.md",
    "grand_design": "The_Grand_Design_Summary.md",
    "crystal_sickness": "Crystal_Sickness_Summary.md",
    "croak_and_dagger": "Croak_And_Dagger_Summary.md",      # was calamity_tax (renamed)
    "forced_liquidation": "Forced_Liquidation_Summary.md",  # 17th deck, was missing
    "creative_destruction": "Creative_Destruction_Summary.md",  # promoted 2026-07-11
}

# Guard against the stale-slug drift the 2026-06-29 audit found (calamity_tax pointed at a
# deleted Summary; croak/forced_liquidation were silently [SKIP]ped). The mapping must cover
# exactly the active roster (deck_registry is the single source of truth).
_REG = ROOT / "scripts" / "deck_registry.py"
if _REG.exists():
    import importlib.util as _ilu
    _spec = _ilu.spec_from_file_location("deck_registry", _REG)
    _dr = _ilu.module_from_spec(_spec); _spec.loader.exec_module(_dr)
    assert set(SUMMARY) == set(_dr.fb_decks()), (
        f"clock_check.SUMMARY drifted from the active roster: "
        f"missing={set(_dr.fb_decks()) - set(SUMMARY)}, stale={set(SUMMARY) - set(_dr.fb_decks())}")


def parse_med(s):
    """JSON median 'T7' -> 7 ; '>T14' / 'never' -> None (open-ended)."""
    s = (s or "").strip()
    if s.startswith(">") or "never" in s.lower():
        return None
    m = re.search(r"\d+", s)
    return int(m.group()) if m else None


def find_clock_line(text):
    """The canonical citation line: the 'Kill Window'/'Clock:' row, preferring
    one that cites a lab. Returns the line or None."""
    best, best_score = None, 0
    for ln in text.splitlines():
        if not re.search(r"[Tt]\d", ln) or not re.search(r"decap|table", ln, re.I):
            continue
        score = 1
        if re.search(r"\bClock\b", ln):
            score += 3
        if "Kill Window" in ln:
            score += 3
        if re.search(r"_clock_lab|_speed_lab|lab 20", ln):
            score += 2
        if score > best_score:
            best, best_score = ln, score
    return best


# The clock value always sits BEFORE the lab citation / the '·' interaction
# separator; everything after is prose (chip-assisted edges, 'Through
# interaction', secondary medians) that must not hijack the read.
HEAD_CUT = re.compile(r"·|\(lab |lab 20|`scripts|`\w+_(?:clock|speed)_lab", re.I)
# decap synonyms: some Summaries write the single-opponent clock as '(one player)'.
DECAP_KW = ("decap", "one player", "one opponent", "(player")


def cited_turns(line):
    """Pull the decap and table turns from a canonical 'decap … / table …' line.

    Truncate at the citation/interaction marker, then split the head into clauses
    ('/' or ';'). Per clause: prefer an explicit '(median Tn)', else open markers
    ('>Tn', 'Tn+', 'never', 'rarely'), else the first 'Tn'. Last clause wins for a
    keyword (summaries put the 'typical' value last). Returns {'decap': (turn|None,
    open), 'table': ...}, None if the keyword is absent.
    """
    cut = HEAD_CUT.search(line)
    head = line[:cut.start()] if cut else line
    # Header-format lines put the clock AFTER a '·' (e.g. "Score: … · Clock: T8 decap …"),
    # so cutting at the first '·' can discard the whole clock clause. If the head lost every
    # clock keyword, the '·' was a leading separator, not the trailing interaction marker —
    # fall back to cutting only at the lab citation (keeps the clock, drops the prose tail).
    if not re.search(r"decap|table", head, re.I):
        cut2 = re.search(r"\(lab |lab 20|`scripts|`\w+_(?:clock|speed)_lab", line, re.I)
        head = line[:cut2.start()] if cut2 else line
    out = {"decap": None, "table": None}
    for seg in re.split(r"[/;]", head):
        low = seg.lower()
        has_d = any(k in low for k in DECAP_KW)
        has_t = "table" in low
        if not (has_d or has_t):
            continue
        openish = (">" in seg or "never" in low or "rarely" in low
                   or bool(re.search(r"[Tt]\d+\s*\+", seg)))
        med = re.search(r"median\D{0,6}[Tt](\d{1,2})", seg, re.I)
        first = re.search(r"[Tt](\d{1,2})", seg)
        turn = (int(med.group(1)) if med
                else int(first.group(1)) if first
                else None)
        if turn is None and not openish:
            continue
        val = (turn, openish)
        if has_d and not has_t:
            out["decap"] = val
        elif has_t and not has_d:
            out["table"] = val
        else:                                   # both keywords in one clause
            out["decap"] = out["decap"] or val
            out["table"] = val
    return out


def classify(cited, lab_med):
    if cited is None:
        return "UNPARSED", "no turn near keyword"
    ct, copen = cited
    if lab_med is None:                                    # lab says never/late
        if copen or (ct is not None and ct >= 12):
            return "OK", "both open-ended (never/late)"
        return "DRIFT", f"summary T{ct}, lab median never/late"
    if ct is None:
        return "UNPARSED", "open-ended cite, numeric lab median"
    if copen:                                              # summary 'T{ct}+'
        return (("OK", "open ≥, consistent") if ct <= lab_med + TOL
                else ("DRIFT", f"summary ≥T{ct}, lab median T{lab_med}"))
    d = abs(ct - lab_med)
    return (("OK", "") if d < TOL
            else ("DRIFT", f"summary T{ct} vs lab T{lab_med} (Δ{d})"))


def scan_matrix(data):
    """Lint Pod_Matchup_Matrix.md's Clock cells ('Tx / Ty') against lab medians.
    The matrix is reordered/regenerated from the labs, so this catches a row that
    fell out of sync. Returns (ok, drift)."""
    if not MATRIX.exists():
        return 0, 0
    name2slug = {rec["name"]: slug for slug, rec in data.items()}
    drift = ok = 0
    print(f"\n  -- {MATRIX.name} Clock cells (Tx / Ty) --")

    def cite(p):
        return (parse_med(p), ">" in p or "+" in p or "never" in p.lower())

    for ln in MATRIX.read_text(encoding="utf-8").splitlines():
        cols = [c.strip() for c in ln.strip().strip("|").split("|")]
        if len(cols) < 4 or not cols[0].isdigit():
            continue
        name, clock = cols[1], cols[3]
        slug = name2slug.get(name)
        if slug is None:
            continue
        rec = data[slug]
        parts = clock.split("/")
        vd, _ = classify(cite(parts[0]), parse_med(rec["med"][0]))
        vt, _ = classify(cite(parts[1]) if len(parts) > 1 else (None, False),
                         parse_med(rec["med"][1]))
        if "DRIFT" in (vd, vt):
            print(f"  [DRIFT ] {name[:30]:30} cell '{clock}' vs lab "
                  f"{rec['med'][0]} / {rec['med'][1]}  (decap {vd} / table {vt})")
            drift += 1
        else:
            ok += 1
    print(f"  matrix: {ok} ok · {drift} DRIFT")
    return ok, drift


def main():
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--strict", action="store_true", help="exit 1 on any DRIFT")
    args = ap.parse_args()

    if not CLOCKS_JSON.exists():
        sys.exit(f"ERROR: {CLOCKS_JSON.relative_to(ROOT)} missing — run "
                 f"`python scripts/pod_gauntlet.py --refresh` first.")
    data = json.loads(CLOCKS_JSON.read_text(encoding="utf-8"))
    age_h = (time.time() - CLOCKS_JSON.stat().st_mtime) / 3600
    print(f"lab medians: {CLOCKS_JSON.relative_to(ROOT)} "
          f"({len(data)} decks, harvested {age_h:.0f}h ago)\n")

    drift = unparsed = ok = 0
    for slug, fname in SUMMARY.items():
        rec = data.get(slug)
        path = ROOT / "decks" / fname
        if rec is None or not path.exists():
            print(f"  [SKIP ] {fname}  (no lab record / file)")
            continue
        lab_d, lab_t = parse_med(rec["med"][0]), parse_med(rec["med"][1])
        line = find_clock_line(path.read_text(encoding="utf-8"))
        if line is None:
            print(f"  [UNPARSED] {fname}  — no canonical Clock line found")
            unparsed += 1
            continue
        cites = cited_turns(line)
        vd, nd = classify(cites["decap"], lab_d)
        vt, nt = classify(cites["table"], lab_t)
        sev = "DRIFT" if "DRIFT" in (vd, vt) else (
            "UNPARS" if "UNPARSED" in (vd, vt) else "OK")
        labstr = f"lab decap {rec['med'][0]} / table {rec['med'][1]}"
        print(f"  [{sev:6}] {fname[:34]:34}  {labstr}")
        print(f"            decap: {vd:8} {nd}".rstrip())
        print(f"            table: {vt:8} {nt}".rstrip())
        if sev == "DRIFT":
            print(f"            cite: {line.strip()[:120]}")
        drift += sev == "DRIFT"
        unparsed += sev == "UNPARS"
        ok += sev == "OK"

    m_ok, m_drift = scan_matrix(data)
    drift += m_drift

    print(f"\n=== {ok} ok · {drift} DRIFT · {unparsed} unparsed "
          f"({len(SUMMARY)} Summaries + {m_ok + m_drift} matrix rows) ===")
    if drift:
        print("DRIFT = a Clock no longer matches the lab. Re-run the deck's lab and "
              "update its Kill Window line / matrix cell, or fix the citation.")
    return 1 if (drift and args.strict) else 0


if __name__ == "__main__":
    sys.exit(main())
