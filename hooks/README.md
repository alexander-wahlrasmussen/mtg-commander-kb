# hooks/ — committed git hooks

Version-controlled git hooks, activated by pointing `core.hooksPath` here (so the
gate ships with the repo instead of living untracked in `.git/hooks`).

## Install (once per clone)

```bash
python scripts/install_hooks.py
```

That sets `git config core.hooksPath hooks` and marks `pre-commit` executable.

## pre-commit

A targeted, fast gate (Backlog #8.8) — it only does work when relevant files are
staged, so doc/markdown commits pass instantly:

| Staged | Runs | Blocks on |
|---|---|---|
| `decks/*.txt` (active) | `deck_doctor.py <file> --no-build` per file | size ≠ 100 · illegal/banned · off-colour · > 3 GC · singleton · MLD/house-rule |
| `decks/*.txt` or the GC/alias ref docs | `validate.py --no-oracle` | size · GC · **filename collision** in the sync set |
| `scripts/*.py` / `tests/*.py` | `pytest -q` (hermetic, ~1s) | any test failure |

Notes:
- **Bypass a single commit:** `git commit --no-verify` (e.g. a deliberate WIP).
- **Without the Scryfall bulk** (`collection/oracle-cards.json` absent), Deck
  Doctor skips legality/colour-identity/singleton-text checks but still gates
  size + GC; `validate.py --no-oracle` still gates filename collisions. The full
  legality sweep is the CI backstop (`.github/workflows/repo-health.yml`).
- The hook checks the **working tree** of staged files (it does not stash unstaged
  changes) — standard pre-commit behaviour; commit decklist edits wholesale.
- CI runs the same tools regardless, so a `--no-verify` slip is still caught on push.
