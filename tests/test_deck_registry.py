"""Tier-1 tests for deck_registry.py — the single source of truth for per-deck
static metadata. Every consumer (deck_sim, framework_bakeoff, pod_gauntlet,
kill_tree, keep_spec, report) reads these rows, so a malformed row or a
prefix-collision in the stems mis-routes a whole batch run silently."""
import deck_registry as reg

REQUIRED = {"name", "stem", "commander", "lab", "cc", "cc_axes", "win_line",
            "bottleneck", "min_lands", "max_lands", "hi_curve", "mixed"}
AXES = {"FINDING", "MANA", "BOARD"}


def test_every_row_has_the_required_keys():
    for slug, row in reg.DECKS.items():
        assert REQUIRED <= set(row), f"{slug} missing {REQUIRED - set(row)}"


def test_cc_axes_sum_to_cc():
    # The four Conversion-Check axes must add up to the stated total.
    for slug, row in reg.DECKS.items():
        if row["cc"] is not None and row["cc_axes"] is not None:
            assert sum(row["cc_axes"]) == row["cc"], slug


def test_bottleneck_and_land_band_valid():
    for slug, row in reg.DECKS.items():
        assert row["bottleneck"] in AXES, slug
        assert row["min_lands"] <= row["max_lands"], slug
        for ax in (row.get("also") or []):
            assert ax in AXES, slug


def test_win_line_has_pieces_and_line():
    for slug, row in reg.DECKS.items():
        wl = row["win_line"]
        assert wl.get("pieces"), slug
        assert wl.get("line"), slug


def test_stems_unique():
    stems = [r["stem"] for r in reg.DECKS.values()]
    assert len(stems) == len(set(stems))


def test_no_active_stem_is_a_prefix_of_another_active_stem():
    # parse_deck prefix-matches the FIRST key a stem startswith; one active stem
    # being a prefix of another would route the longer deck to the wrong commander.
    stems = [r["stem"] for r in reg.DECKS.values()]
    for a in stems:
        for b in stems:
            if a != b:
                assert not b.startswith(a), f"{a!r} is a prefix of {b!r}"


def test_no_active_stem_prefixes_an_extra_stem():
    # Documented load-bearing invariant: actives are emitted first by
    # active_commanders(), so none may be a prefix of an EXTRA stem.
    actives = [r["stem"] for r in reg.DECKS.values()]
    for a in actives:
        for e in reg.EXTRA_COMMANDERS:
            assert not e.startswith(a), f"active {a!r} prefixes extra {e!r}"


def test_kill_tree_reg_slugs_resolve():
    for slug, spec in reg.KILL_TREES.items():
        assert spec["reg_slug"] in reg.DECKS, slug


def test_accessor_shapes_match_registry():
    assert set(reg.fb_decks()) == set(reg.DECKS)
    assert set(reg.win_lines()) == set(reg.DECKS)
    # only two-line decks (those with `also`) appear in also()
    assert set(reg.also()) == {s for s, r in reg.DECKS.items() if r.get("also")}
    # every active deck contributes a stem->commander row
    assert len(reg.active_commanders()) == len(reg.DECKS)
