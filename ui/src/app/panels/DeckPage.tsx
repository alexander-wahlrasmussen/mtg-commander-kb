import { useMemo, useState } from "react";
import { LineChart, SegmentedControl } from "../../components";
import { getDeck } from "../data";
import type { DeckPage as DeckPageData, KillKind, KillLine, MullHand } from "../data";
import { usePageData } from "../hooks";
import { Pips } from "../pagekit";
import s from "../pages.module.css";

const COMP_TONES = ["var(--ink)", "var(--acc)", "var(--ink2)", "var(--ink3)", "var(--gold)", "#6f5577", "#076678", "#4f6b1e", "#a8662e", "#b57614"];
const BOTTLENECK: Record<string, string> = { FINDING: "finds a combo piece", MANA: "hits its mana", BOARD: "develops a board" };

/** Derive "how it loses" bullets from the structured data (no fragile prose scrape). */
function openings(d: DeckPageData): string[] {
  const out: string[] = [];
  if (d.axes.length) {
    const low = d.axes.reduce((a, b) => (b.score < a.score ? b : a));
    out.push(`Weakest axis — ${low.label} (${low.score}/5): the judges' soft spot.`);
  }
  if (d.keep.mixed) out.push(d.keep.mixed[0].toUpperCase() + d.keep.mixed.slice(1) + ".");
  if (d.clock.never?.[0]) out.push(`Decap never-closes in ${d.clock.never[0]}% of goldfish games — a grind risk.`);
  if (d.clock.never?.[1]) out.push(`Tables (all three) never-closes ${d.clock.never[1]}% of the time.`);
  return out.slice(0, 4);
}

function keepCriteria(d: DeckPageData): string[] {
  const k = d.keep;
  const out: string[] = [];
  if (k.minLands != null) out.push(`${k.minLands}–${k.maxLands} mana sources`);
  if (k.bottleneck) out.push(BOTTLENECK[k.bottleneck] ?? k.bottleneck.toLowerCase());
  out.push("interaction (ideal)");
  return out;
}

/** The full 100-card list, grouped by the Summary's functional buckets (same
 *  buckets as the composition bar above) — the pick-up-and-play reference. */
function Curve({ curve }: { curve: { cmc: string; n: number }[] }) {
  const max = Math.max(1, ...curve.map((b) => b.n));
  return (
    <div className={s.curve}>
      <div className={s.curveTitle}>Mana curve <span>· nonland</span></div>
      <div className={s.curveBars}>
        {curve.map((b) => (
          <div key={b.cmc} className={s.curveCol}>
            <span className={s.curveN}>{b.n || ""}</span>
            <div className={s.curveTrack}>
              <div className={s.curveBar} style={{ height: `${(b.n / max) * 100}%` }} />
            </div>
            <span className={s.curveX}>{b.cmc}</span>
          </div>
        ))}
      </div>
    </div>
  );
}

function Decklist({ d, compColor }: { d: DeckPageData; compColor: Record<string, string> }) {
  const dl = d.decklist;
  const [copied, setCopied] = useState(false);
  const [view, setView] = useState<"role" | "type">("role");
  if (!dl) return null;

  const byType = view === "type" && dl.groupsByType ? dl.groupsByType : dl.groups;
  const groupColor = (name: string, i: number) =>
    view === "type" ? COMP_TONES[i % COMP_TONES.length] : compColor[name] ?? "var(--ink3)";

  const copy = () => {
    navigator.clipboard?.writeText(dl.text).then(
      () => { setCopied(true); setTimeout(() => setCopied(false), 1600); },
      () => { /* clipboard blocked (e.g. insecure context) — no-op */ },
    );
  };

  return (
    <div style={{ marginTop: "var(--s5)" }}>
      <div className={s.subHead}>
        <span className={s.subTick} />
        <span className={s.subTitle}>The Decklist</span>
        <span className={s.subHint}>{dl.total} cards · pick up &amp; play</span>
        <div className={s.dlControls}>
          {dl.groupsByType && (
            <SegmentedControl
              aria-label="group the decklist"
              options={[{ value: "role", label: "By role" }, { value: "type", label: "By type" }]}
              value={view}
              onChange={(v) => setView(v as "role" | "type")}
            />
          )}
          <button className={s.copyBtn} onClick={copy}>{copied ? "copied ✓" : "copy list"}</button>
        </div>
      </div>

      <div className={s.dlCommander}>
        <span className={s.dlCmdTag}>Commander</span>
        <span className={s.dlCmdName}>{dl.commander.n}</span>
        {dl.commander.gc && <span className={s.dlGc}>GC</span>}
      </div>

      {dl.curve && <Curve curve={dl.curve} />}

      <div className={s.dlColumns}>
        {byType.map((g, i) => (
          <div key={`${view}-${i}`} className={s.dlGroup}>
            <div className={s.dlGroupHead}>
              <span className={s.dlSwatch} style={{ background: groupColor(g.name, i) }} />
              <span className={s.dlGroupName}>{g.name}</span>
              <span className={s.dlGroupCount}>{g.count}</span>
            </div>
            {g.cards.map((c, j) => (
              <div key={j} className={s.dlCard}>
                <span className={s.dlCardName}>{c.n}</span>
                {c.gc && <span className={s.dlGc}>GC</span>}
              </div>
            ))}
          </div>
        ))}
      </div>
    </div>
  );
}

/** Trusted KB strings carry `<br/>` line breaks — render them as real breaks. */
function brk(text: string) {
  return text.split(/<br\s*\/?>/i).map((part, i, a) => (
    <span key={i}>{part}{i < a.length - 1 && <br />}</span>
  ));
}

const KILL_KIND_LABEL: Record<KillKind, string> = {
  combo: "combo", table: "table drain", combat: "decap", enabler: "enabler",
};

/** The deck's kill LINES as a cheapest-first ladder (hand-rolled, no diagram lib):
 *  try the top line; if its pieces aren't up, fall to the next. Mirrors kill_tree.py. */
function KillTree({ d }: { d: DeckPageData }) {
  const kt = d.killTree;
  if (!kt) return null;
  return (
    <div style={{ marginTop: "var(--s5)" }}>
      <div className={s.subHead}>
        <span className={s.subTick} />
        <span className={s.subTitle}>Kill Tree</span>
        <span className={s.subHint}>cheapest line first · fall to the next if pieces aren't up</span>
      </div>
      <div className={s.ktRoot}>{brk(kt.root)}</div>
      <div className={s.ktLines}>
        {kt.lines.map((l: KillLine, i: number) => (
          <div key={l.id} className={s.ktLine} data-kind={l.kind}>
            <span className={s.ktIdx}>{i === kt.lines.length - 1 ? "↳" : String(i + 1).padStart(2, "0")}</span>
            <div className={s.ktNeed}>{brk(l.need)}</div>
            <span className={s.ktArrow}>→</span>
            <div className={s.ktKill}>
              <div className={s.ktKillText}>{brk(l.kill)}</div>
              <div className={s.ktMeta}>
                <span className={s.ktKindTag} data-kind={l.kind}>{KILL_KIND_LABEL[l.kind]}</span>
                <span className={s.ktClock}>⏱ {l.clock}</span>
              </div>
            </div>
          </div>
        ))}
      </div>
      {kt.background && (
        <div className={`${s.ktLine} ${s.ktBg}`} data-kind={kt.background.kind}>
          <span className={s.ktIdx}>∞</span>
          <div className={s.ktNeed}>{brk(kt.background.need)}</div>
          <span className={s.ktArrow}>→</span>
          <div className={s.ktKill}>
            <div className={s.ktKillText}>{brk(kt.background.kill)}</div>
            <div className={s.ktMeta}>
              <span className={s.ktKindTag} data-kind={kt.background.kind}>always on</span>
              <span className={s.ktClock}>⏱ {kt.background.clock}</span>
            </div>
          </div>
        </div>
      )}
      <div className={s.ktStall}><span className={s.ktStallTag}>when nothing's up</span> {brk(kt.stall)}</div>
      <div className={s.clockLabRef}>{kt.src}</div>
    </div>
  );
}

/** Keep-or-mull drill on baked hands. The verdict is the AUTHORITATIVE deck_sim
 *  keep_hand, computed in Python and baked — the client only reveals + scores it. */
function MulliganDrill({ d }: { d: DeckPageData }) {
  const m = d.mulligan;
  // stable shuffle of hand order so the drill isn't always the same sequence,
  // without a backend: a fixed permutation keyed off the deck slug.
  const order = useMemo(() => {
    const n = m?.hands.length ?? 0;
    const idx = Array.from({ length: n }, (_, i) => i);
    let seed = 0;
    for (const ch of d.slug) seed = (seed * 31 + ch.charCodeAt(0)) >>> 0;
    for (let i = n - 1; i > 0; i--) { seed = (seed * 1103515245 + 12345) >>> 0; const j = seed % (i + 1); [idx[i], idx[j]] = [idx[j], idx[i]]; }
    return idx;
  }, [m, d.slug]);

  const [pos, setPos] = useState(0);
  const [guess, setGuess] = useState<boolean | null>(null);
  const [score, setScore] = useState({ agree: 0, seen: 0 });
  if (!m || m.hands.length === 0) return null;

  const hand: MullHand = m.hands[order[pos % order.length]];
  const answer = (keep: boolean) => {
    if (guess !== null) return;
    setGuess(keep);
    setScore((sc) => ({ agree: sc.agree + (keep === hand.keep ? 1 : 0), seen: sc.seen + 1 }));
  };
  const next = () => { setGuess(null); setPos((p) => p + 1); };
  const axes = [m.bottleneck, ...m.also];

  return (
    <div style={{ marginTop: "var(--s5)" }}>
      <div className={s.subHead}>
        <span className={s.subTick} />
        <span className={s.subTitle}>Mulligan Trainer</span>
        <span className={s.subHint}>keep or mull? — score yourself vs the plan-keep model</span>
      </div>
      <div className={s.mtMeta}>
        plan axis <strong>{axes.join(" + ")}</strong> · land band {m.minLands}–{m.maxLands} · the model is a heuristic, not an oracle
      </div>

      <div className={s.mtHand}>
        {hand.cards.map((c, i) => (
          <div key={i} className={s.mtCard} data-land={c.land || undefined}>
            <span className={s.mtCmc}>{c.land ? "▦" : c.cmc}</span>
            <span className={s.mtCardName}>{c.n}</span>
            {c.tags.filter((t) => t !== "LAND").map((t) => (
              <span key={t} className={s.mtTag}>{t}</span>
            ))}
          </div>
        ))}
      </div>

      {guess === null ? (
        <div className={s.mtBtns}>
          <button className={s.mtKeep} onClick={() => answer(true)}>Keep</button>
          <button className={s.mtMull} onClick={() => answer(false)}>Mulligan</button>
        </div>
      ) : (
        <div className={s.mtReveal}>
          <div className={s.mtVerdictRow}>
            <span className={s.mtVerdict} data-keep={hand.keep}>model: {hand.keep ? "KEEP" : "MULL"}</span>
            <span className={s.mtJudge} data-ok={guess === hand.keep}>
              {guess === hand.keep ? "✓ you agreed" : `✗ you said ${guess ? "KEEP" : "MULL"}`}
            </span>
            <button className={s.mtNext} onClick={next}>next hand →</button>
          </div>
          <ul className={s.mtReasons}>
            {hand.reasons.map((r, i) => <li key={i}>{r}</li>)}
          </ul>
        </div>
      )}

      {score.seen > 0 && (
        <div className={s.mtScore}>agreed {score.agree}/{score.seen} ({Math.round((100 * score.agree) / score.seen)}%)</div>
      )}
    </div>
  );
}

export function DeckPage({ slug, onBack }: { slug: string; onBack: () => void }) {
  const { data: d, error } = usePageData<DeckPageData>(() => getDeck(slug), [slug]);
  if (error) return <div className={s.error}>error: {error}</div>;
  if (!d) return <div className={s.loading}>loading deck…</div>;

  const hasClock = d.clock.grid.length > 0;
  const compTotal = d.composition.reduce((sum, b) => sum + b.count, 0) || 1;
  // share the composition bar's colours with the decklist groups (matched by name)
  const compColor: Record<string, string> = {};
  d.composition.forEach((b, i) => { compColor[b.name] = COMP_TONES[i % COMP_TONES.length]; });

  return (
    <div className={s.deckPage}>
      <button className={s.back} onClick={onBack}>← roster</button>

      <div className={s.hero}>
        <div style={{ minWidth: 0 }}>
          <div className={s.heroKicker}>In the {d.colors} corner · No. {d.score ?? "—"}/20</div>
          <h1 className={s.heroTitle}>{d.name}</h1>
          <div className={s.heroMeta}>
            <Pips letters={d.pips} size={16} />
            <span>{d.commander} · {d.archetype}</span>
          </div>
        </div>
        {d.gamePlan && (
          <div className={s.gamePlanBox}>
            <div className={s.gamePlanHead}>The Game Plan</div>
            <div className={s.gamePlanBody}>{d.gamePlan}</div>
          </div>
        )}
      </div>

      {/* ===== Tale of the tape — measured kill-clock ===== */}
      <div className={s.tapeBar}>
        <span className={s.tapeBarTitle}>Tale of the Tape</span>
        <span className={s.tapeBarRule} />
        <span className={s.tapeBarHint}>Measured kill-clock — what actually wins</span>
      </div>
      <div style={{ paddingTop: "var(--s4)" }}>
        <div className={s.clockBox}>
          <div className={s.clockCol}>
            <div className={s.clockColLabel}>Decap · one opponent</div>
            <div className={`${s.clockBig} ${s.clockBigAcc}`}>{d.clock.decap ?? "—"}</div>
            <div className={s.clockSub}>median kill</div>
          </div>
          <div className={s.vs}>VS</div>
          <div className={s.clockCol}>
            <div className={s.clockColLabel}>Table · all three</div>
            <div className={s.clockBig}>{d.clock.table ?? "—"}</div>
            <div className={s.clockSub}>median kill</div>
          </div>
        </div>
        {d.clock.src && <div className={s.clockLabRef}>{d.clock.src}</div>}
        {hasClock && (
          <div style={{ marginTop: 10 }}>
            <LineChart
              height={210}
              xLabel="turn"
              yLabel="cum P(kill) %"
              refLineY={50}
              series={[
                { name: "Decap (1 opp)", color: "#c63a1b", points: d.clock.grid.map((x, i) => ({ x, y: d.clock.decapCurve[i] })) },
                { name: "Table (all 3)", color: "#5b544a", points: d.clock.grid.map((x, i) => ({ x, y: d.clock.tableCurve[i] })) },
              ]}
            />
          </div>
        )}
      </div>

      {/* ===== Finishers / openings ===== */}
      <div className={s.twoCol}>
        <div className={s.twoColLeft}>
          <div className={s.subHead}>
            <span className={s.subTick} />
            <span className={s.subTitle}>Finishers</span>
            <span className={s.subHint}>how it wins</span>
          </div>
          {(d.finishers.length ? d.finishers : [{ name: d.winLine, tag: "", note: "" }]).map((f, i) => (
            <div key={i} className={s.finisher}>
              <span className={s.finIdx}>{String(i + 1).padStart(2, "0")}</span>
              <div>
                <div className={s.finTop}>
                  <span className={s.finName}>{f.name}</span>
                  {f.tag && <span className={s.finTag}>{f.tag}</span>}
                </div>
                {f.note && <div className={s.finNote}>{f.note}</div>}
              </div>
            </div>
          ))}
        </div>
        <div className={s.twoColRight}>
          <div className={s.subHead}>
            <span className={s.subTickHollow} />
            <span className={s.subTitle}>Openings</span>
            <span className={s.subHint}>how it loses</span>
          </div>
          {openings(d).map((w, i) => (
            <div key={i} className={s.openRow}>
              <span className={s.openArrow}>→</span>
              <span>{w}</span>
            </div>
          ))}
        </div>
      </div>

      {/* ===== Kill tree — the cheapest-first ladder (4 encoded decks) ===== */}
      <KillTree d={d} />

      {/* ===== For the record — composition + judges' card ===== */}
      <div className={s.recordBar}>
        <span className={s.recordKicker}>For the record</span>
        <span style={{ flex: 1, height: 1, background: "var(--hair)" }} />
        <span className={s.recordKicker}>100 cards · what's in the deck</span>
      </div>
      <div className={s.recordGrid}>
        <div className={s.recordLeft}>
          <div className={s.kpiLabel} style={{ marginBottom: 6 }}>Composition</div>
          {d.composition.length > 0 ? (
            <>
              <div className={s.compBar}>
                {d.composition.map((b, i) => (
                  <div key={i} className={s.compSeg} style={{ width: `${(b.count / compTotal) * 100}%`, background: COMP_TONES[i % COMP_TONES.length] }} />
                ))}
              </div>
              <div className={s.compLegend}>
                {d.composition.map((b, i) => (
                  <span key={i} className={s.compItem}>
                    <span className={s.compSwatch} style={{ background: COMP_TONES[i % COMP_TONES.length] }} />
                    {b.name} <span className={s.compCount}>{b.count}</span>
                  </span>
                ))}
              </div>
            </>
          ) : (
            <div className={s.awardNote}>No composition breakdown in the Summary.</div>
          )}
        </div>
        <div className={s.recordRight}>
          <div className={s.kpiLabel} style={{ marginBottom: 11 }}>The Judges' Card · {d.score ?? "—"}/20</div>
          <div className={s.axes}>
            {d.axes.map((a, i) => (
              <div key={i} className={s.axis}>
                <div className={s.axisLabel}>{a.label}</div>
                <div className={s.axisScore}>{a.score}<span style={{ fontFamily: "var(--mono)", fontSize: 10, color: "var(--ink3)", fontWeight: 400 }}>/5</span></div>
                <div className={s.axisBar}><span className={s.axisBarFill} style={{ width: `${(a.score / 5) * 100}%` }} /></div>
              </div>
            ))}
          </div>
          <div className={s.kpiLabel} style={{ marginBottom: 10 }}>Game Changers · {d.gc.length}/3</div>
          {d.gc.map((g, i) => (
            <div key={i} className={s.gcRow}><span className={s.gcBadge}>GC</span>{g}</div>
          ))}
        </div>
      </div>

      {/* ===== The decklist — the composition bar expanded into actual cards ===== */}
      <Decklist d={d} compColor={compColor} />

      {/* ===== The keep ===== */}
      <div style={{ marginTop: "var(--s5)" }}>
        <div className={s.subHead}>
          <span className={s.subTick} />
          <span className={s.subTitle}>The Keep</span>
          <span className={s.subHint}>reading a 7-card opener</span>
        </div>
        <div className={s.keepCriteria}>
          {keepCriteria(d).map((c, i) => (
            <span key={i} className={s.crit}>{c}</span>
          ))}
        </div>
      </div>

      {/* ===== Mulligan trainer — keep/mull drill on baked hands ===== */}
      <MulliganDrill d={d} />

      {/* ===== Don't-miss rulings — the card-text gotchas that lose games ===== */}
      {d.rulings?.length > 0 && (
        <div style={{ marginTop: "var(--s5)" }}>
          <div className={s.subHead}>
            <span className={s.subTick} />
            <span className={s.subTitle}>Don't-miss rulings</span>
            <span className={s.subHint}>gotchas that lose games when missed</span>
          </div>
          {d.rulings.map((r, i) => (
            <div key={i} className={s.openRow}>
              <span className={s.openArrow}>§</span>
              <span>{r.name && <strong>{r.name}</strong>}{r.name && r.note ? " — " : ""}{r.note}</span>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
