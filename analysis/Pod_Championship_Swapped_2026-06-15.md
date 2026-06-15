# The Pod Championship — ALL PROPOSED SWAPS APPLIED (2026-06-15)

*Companion to `Pod_Championship_2026-06-15.md`: the same tournament re-run with every proposed
swap from `Build_And_Swap_Tracker.md` §2 (encoded in `pod_gauntlet.SWAPS`) applied. Reproduce:
`python scripts/pod_championship.py --swapped`.*

## TL;DR — the crown does not move

**The Genome Project is still champion** — across all 5 seeds and the full `T_grind` sweep, in
both the fast and grindy metas. Applying the swaps changes **one thing**: the Calamity Tax
grind-fortress rebuild promotes it into the medals.

## Why almost nothing changes: the tournament races the *table* clock

The championship decides each game on the **table-close** clock. Of the five proposed swaps,
only one carries a new table curve:

| Swap | What it does | Table-clock effect | Effect on this tournament |
|---|---|---|---|
| **Calamity Tax** — grind-fortress rebuild | table T10→**T9**, never 14%→**4%**, dura 0.78→**0.83** | **moves** | **the only mover** — promotes Calamity |
| Grand Design — ramp + finisher | decap T10→T9 only | none (table unchanged) | inert here |
| Exile's Return — +Drannith / +Kiki | resilience + disruption | none | inert here |
| Replication Crisis — +Kiki line | resilience (~5% goldfish) | none | inert here |
| Diminishing Returns — +Deathmantle/Grave Titan | combo resilience | none | inert here |

The other four add **decap speed or resilience the table goldfish can't score** — exactly the
"reliability/resilience upgrades the goldfish can't see" finding from the swap analysis. They're
genuinely applied in the `--swapped` run; they just don't register on this metric. (To see the
decap/disruption swaps pay off, look at the anti-pod gauntlet — `pod_gauntlet.py --swapped` —
not this table-clock tournament.)

## What *does* change: Calamity Tax crashes the podium

| | Baseline | All swaps applied | Δ |
|---|---|---|---|
| Calamity seed | #4 (36%) | **#3 (45%)** | ▲ +1 seed, +9pp |
| Calamity finish | group stage (lost Pod D to Exile) | **🥉 Final Four (11.7%)** | ▲ onto the podium |
| Pushed off the podium | — | The Exile's Return (was 4th) | ▼ out of the Final Four |
| Champion | The Genome Project | **The Genome Project** | = unchanged |
| Runner-up | Zero-Sum Game | **Zero-Sum Game** | = unchanged |

The reseed (Calamity #4→#3) bumps Radiation Sickness to #4; in the new snake bracket Calamity
takes Pod C (58.9%) and Radiation takes Pod D (45.0%), so **both** reach the Final Four while
**Exile's Return drops out**. Net podium change: Exile (4th) → Calamity (🥉).

## The swapped bracket

Source: `pod-championship-2026-06-15-swapped-bracket.mmd` (validated via Mermaid Chart). Purple
= the swapped deck.

```mermaid
flowchart LR
    classDef champ fill:#fabd2f,color:#1d2021,stroke:#d79921,stroke-width:4px;
    classDef adv fill:#b8e6a0,color:#1d2021,stroke:#689d6e,stroke-width:2px;
    classDef out fill:#d5c4a1,color:#3c3836,stroke:#928374,stroke-width:1px;
    classDef fin fill:#aed1f0,color:#1d2021,stroke:#458588,stroke-width:2px;
    classDef swap fill:#d3a3e0,color:#1d2021,stroke:#8f3f9f,stroke-width:2px;

    subgraph PA["POD A"]
        direction TB
        A1["Genome Project · #1<br/>91.9% ➜"]:::adv
        A2["Replication Crisis · #9<br/>4.9%"]:::out
        A3["Dark Lord's Army · #8<br/>3.1%"]:::out
        A4["Grand Design · #16<br/>0.2%"]:::out
    end
    subgraph PB["POD B"]
        direction TB
        B1["Zero-Sum Game · #2<br/>55.9% ➜"]:::adv
        B2["Earthbend the Meta · #10<br/>21.9%"]:::out
        B3["Curse of the Scarab · #7<br/>19.4%"]:::out
        B4["Diminishing Returns · #15<br/>2.8%"]:::out
    end
    subgraph PC["POD C"]
        direction TB
        C1["Calamity Tax · #3 swap<br/>58.9% ➜"]:::swap
        C2["Lorehold Spirits · #6<br/>33.4%"]:::out
        C3["Lightning War · #14<br/>3.8%"]:::out
        C4["Ms. Bumbleflower · #11<br/>3.8%"]:::out
    end
    subgraph PD["POD D"]
        direction TB
        D1["Radiation Sickness · #4<br/>45.0% ➜"]:::adv
        D2["Exile's Return · #5<br/>35.3%"]:::out
        D3["Crystal Sickness · #12<br/>11.1%"]:::out
        D4["Eldrazi Stampede · #13<br/>8.7%"]:::out
    end

    subgraph FF["THE FINAL FOUR"]
        direction TB
        F1["🥇 Genome Project<br/>48.0%"]:::champ
        F2["🥈 Zero-Sum Game<br/>34.0%"]:::fin
        F3["🥉 Calamity Tax swap<br/>11.7%"]:::swap
        F4["Radiation Sickness<br/>6.3%"]:::fin
    end

    A1 --> F1
    B1 --> F2
    C1 --> F3
    D1 --> F4
    F1 --> CH["🏆 CHAMPION<br/>The Genome Project<br/>seed #1"]:::champ
```

## Robustness (swapped)

| `T_grind` | Champion | Runner-up |
|---:|---|---|
| 6–7 | The Dark Lord's Army | **The Calamity Tax (#2)** |
| 8 | The Genome Project | The Calamity Tax (#3) |
| 9–14 | The Genome Project | Zero-Sum Game |

Same shape as baseline — Genome for `T_grind ≥ 8`, Dark Lord's Army at the extreme-grind edge.
The swap's mark: in the grind meta Calamity climbs to the **#2 seed** and becomes the clear
runner-up, but its durability (0.83) still falls short of Dark Lord's (0.86), so the grind king
keeps the throne. Genome's crown is untouched by the swaps at every pace and seed tested.

## Verdict

The proposed swaps are **correctly aimed** — Calamity's rebuild does exactly what it was built
to do (it goes from a non-factor to a Final-Four / grind-runner-up deck). But they are **not
a title threat**: nothing in the swap slate closes the table faster than Genome's T8 hit-all
clock. If the goal is to dethrone the champion, the lever isn't on the swap list — it's a deck
that closes a 3-seat table by T7–T8. (Caveats inherited from the base championship: goldfish
table ceilings, soft durability/`T_grind` judgment.)
