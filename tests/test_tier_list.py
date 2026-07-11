"""Tier-1 tests for tier_list.compute_rows — the shared core behind the CLI print AND the
dashboard's /api/tierlist (so the dashboard can't silently drift from the committed list).

Not bulk-gated: reads the committed pod_gauntlet_clocks.json + runs the MC oracles at a small
trial count (~1s, no Scryfall data). Guards the STRUCTURE/CONTRACT the dashboard depends on —
ordering, tier validity, the v2-vs-legacy axis shape — not the exact stochastic numbers.
"""
import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def _load(name):
    spec = importlib.util.spec_from_file_location(name, ROOT / "scripts" / f"{name}.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


tl = _load("tier_list")


def test_v2_payload_contract():
    p = tl.compute_rows(trials=800, legacy=False)
    assert p["version"] == "v2"
    assert p["tiers"] == ["S", "A", "B", "C", "D"]
    assert set(p["weights"]) == {"antipod", "inter", "self"}
    rows = p["rows"]
    assert len(rows) >= 15                                   # whole active roster (15 after Earthbend retired 2026-07-11)
    # every row carries the dashboard's required fields
    for r in rows:
        assert set(r) >= {"slug", "name", "tier", "comp", "anti", "inter", "self", "cc",
                          "decap", "table"}
        assert r["tier"] in p["tiers"]
        assert r["inter"] is not None                        # v2: the interaction axis is live


def test_rows_are_comp_descending_and_tiers_contiguous():
    rows = tl.compute_rows(trials=800, legacy=False)["rows"]
    comps = [r["comp"] for r in rows]
    assert comps == sorted(comps, reverse=True)              # ranked best-first
    # a tier letter, once left, never reappears (rows are grouped by tier)
    seen, prev = [], None
    for r in rows:
        if r["tier"] != prev:
            assert r["tier"] not in seen, f"tier {r['tier']} not contiguous"
            seen.append(r["tier"]); prev = r["tier"]


def test_legacy_drops_the_interaction_axis():
    p = tl.compute_rows(trials=800, legacy=True)
    assert p["version"] == "v1"
    assert "inter" not in p["weights"] and "power" in p["weights"]
    assert all(r["inter"] is None for r in p["rows"])


def test_seed_is_deterministic():
    a = tl.compute_rows(trials=800, seed=123, legacy=False)["rows"]
    b = tl.compute_rows(trials=800, seed=123, legacy=False)["rows"]
    assert [(r["slug"], r["comp"]) for r in a] == [(r["slug"], r["comp"]) for r in b]
