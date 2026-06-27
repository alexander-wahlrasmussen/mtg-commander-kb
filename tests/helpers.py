"""Synthetic card data so the cores can be tested without the 176 MB Scryfall
bulk. The shape mirrors exactly what deck_sim.load_oracle_index() produces."""


def rec(cmc=2.0, type_line="Creature", color_identity=(), produced_mana=(),
        face_types=None, power=None):
    """One oracle index record (the dict deck_sim builds per card)."""
    return {
        "cmc": cmc,
        "type_line": type_line,
        "face_types": list(face_types) if face_types is not None else [type_line],
        "color_identity": tuple(color_identity),
        "produced_mana": tuple(produced_mana),
        "power": power,
    }


def land(produced=("U",), basic_type="Island"):
    tl = f"Basic Land — {basic_type}"
    return rec(type_line=tl, face_types=[tl], produced_mana=produced)


def toy_library(n_land=24, n_spell=36):
    """A parse_deck-shaped library: list of (name, record). Mono-U lands + cheap
    creatures — enough to drive simulate() across a 10-turn horizon."""
    lib = [("Island", land()) for _ in range(n_land)]
    lib += [(f"Spell{i}", rec(cmc=2, type_line="Creature — Bear")) for i in range(n_spell)]
    return lib
