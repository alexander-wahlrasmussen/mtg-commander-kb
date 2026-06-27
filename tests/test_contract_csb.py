"""Tier-2 CONTRACT test for the Commander Spellbook combo finder (Backlog.md #9).

deck_doctor --combos and find_combos.py both lean on the CSB find-my-combos API.
A network call can't run in the hermetic suite, and we don't want a test that
silently passes when CSB is down or breaks when CSB renames a field. So this is
a record/replay contract test:

  REPLAY (default, offline) — monkeypatch find_combos._post to serve a recorded
    response (tests/fixtures/csb_find_my_combos.json) and assert find_my_combos
    parses + paginates + aggregates it into the (identity, included, almost,
    changing) shape the rest of the code consumes. Pins OUR side of the contract.

  RECORD (opt-in, network) — `python tests/test_contract_csb.py --record`
    re-hits the live API with the fixture's stored payload and rewrites the
    fixture, so CSB API drift surfaces as a reviewable fixture diff, deliberately,
    not as a surprise red in unrelated work.

The fixture is a REAL response, trimmed to id/uses/produces and SPLIT across two
pages so the pagination loop is genuinely exercised (CSB returned it in one page).
"""
import importlib.util
import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
_SCRIPTS = str(ROOT / "scripts")
if _SCRIPTS not in sys.path:
    sys.path.insert(0, _SCRIPTS)

FIXTURE = Path(__file__).resolve().parent / "fixtures" / "csb_find_my_combos.json"

pytestmark = pytest.mark.contract


def _load_find_combos():
    spec = importlib.util.spec_from_file_location("find_combos", ROOT / "scripts" / "find_combos.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


@pytest.fixture(scope="module")
def fc():
    return _load_find_combos()


@pytest.fixture
def fixture():
    return json.loads(FIXTURE.read_text(encoding="utf-8"))


def _replay(fc, pages, monkeypatch):
    """Make fc._post serve `pages` in order; the page's own 'next' drives the
    loop, exactly as the real paginator does."""
    queue = list(pages)

    def fake_post(url, payload):
        assert queue, "find_my_combos requested more pages than recorded"
        return queue.pop(0)

    monkeypatch.setattr(fc, "_post", fake_post)
    return queue


def test_replay_matches_recorded_shape(fc, fixture, monkeypatch):
    """find_my_combos aggregates the recorded pages into the expected counts."""
    queue = _replay(fc, fixture["pages"], monkeypatch)
    identity, included, almost, changing = fc.find_my_combos({"commanders": [], "main": []})
    exp = fixture["expect"]
    assert identity == exp["identity"]
    assert len(included) == exp["included"]
    assert len(almost) == exp["almost"]
    assert len(changing) == exp["changing"]
    assert not queue, "paginator stopped before consuming every recorded page"


def test_combo_field_extraction(fc, fixture, monkeypatch):
    """_uses / _features read the documented uses[].card.name and
    produces[].feature.name paths — the contract deck_doctor's combo report
    depends on. Asserts against the real Thassa's Oracle line in the fixture."""
    _replay(fc, fixture["pages"], monkeypatch)
    _, included, _, _ = fc.find_my_combos({"commanders": [], "main": []})
    win = next((c for c in included if "Win the game" in fc._features(c)), None)
    assert win is not None, "recorded 'Win the game' combo vanished — CSB shape drift?"
    uses = {n.lower() for n in fc._uses(win)}
    assert "thassa's oracle" in uses and "demonic consultation" in uses


def test_aggregates_changing_commanders_field(fc, monkeypatch):
    """The CSB response splits results across FOUR lists; included/almost are
    covered by the real fixture, this pins includedByChangingCommanders +
    multi-page aggregation with minimal synthetic pages (key-rename guard)."""
    combo = lambda i: {"id": i, "uses": [{"card": {"name": "X"}}],
                       "produces": [{"feature": {"name": "Win the game"}}]}
    pages = [
        {"next": "p2", "results": {"identity": "U", "included": [combo("a")],
                                   "almostIncluded": [], "includedByChangingCommanders": [combo("c1")]}},
        {"next": None, "results": {"identity": "U", "included": [combo("b")],
                                   "almostIncluded": [combo("x")], "includedByChangingCommanders": [combo("c2")]}},
    ]
    _replay(fc, pages, monkeypatch)
    identity, included, almost, changing = fc.find_my_combos({"commanders": [], "main": []})
    assert identity == "U"
    assert [c["id"] for c in included] == ["a", "b"]      # aggregated across pages
    assert [c["id"] for c in almost] == ["x"]
    assert [c["id"] for c in changing] == ["c1", "c2"]    # the key under test


def _record():
    """Opt-in: re-hit the live CSB API with the fixture's payload and rewrite the
    fixture (trimmed + split into 2 pages). Surfaces API drift as a fixture diff."""
    fc = _load_find_combos()
    payload = json.loads(FIXTURE.read_text(encoding="utf-8"))["_meta"]["payload"]
    d = fc._post(fc.API + "?limit=500", payload)
    res = d["results"]

    def trim(c):
        return {"id": c["id"],
                "uses": [{"card": {"name": u["card"]["name"]}} for u in c.get("uses", [])],
                "produces": [{"feature": {"name": p["feature"]["name"]}} for p in c.get("produces", [])]}

    inc = [trim(c) for c in res.get("included", [])]
    alm = [trim(c) for c in res.get("almostIncluded", [])][:3]
    chg = [trim(c) for c in res.get("includedByChangingCommanders", [])][:1]
    ident = res["identity"]
    if len(inc) < 2:
        sys.exit(f"need >=2 included combos to split across pages; got {len(inc)} — pick another payload")
    pages = [
        {"count": len(inc), "next": fc.API + "?limit=500&offset=1", "previous": None,
         "results": {"identity": ident, "included": inc[:1],
                     "includedByChangingCommanders": [], "almostIncluded": alm}},
        {"count": len(inc), "next": None, "previous": None,
         "results": {"identity": ident, "included": inc[1:],
                     "includedByChangingCommanders": chg, "almostIncluded": []}},
    ]
    out = {"_meta": {"recorded_via": "find_combos._post (CSB find-my-combos)",
                     "payload": payload,
                     "note": "real pages SPLIT to test pagination; combos trimmed to id/uses/produces"},
           "pages": pages,
           "expect": {"identity": ident, "included": len(inc), "almost": len(alm), "changing": len(chg)}}
    FIXTURE.write_text(json.dumps(out, indent=2) + "\n", encoding="utf-8")
    print(f"rewrote {FIXTURE.relative_to(ROOT)}: identity {ident}, included {len(inc)}, "
          f"almost {len(alm)}, changing {len(chg)}")


if __name__ == "__main__":
    if "--record" in sys.argv:
        _record()
    else:
        sys.exit("usage: python tests/test_contract_csb.py --record   (hits the live CSB API)")
