// Deck scouting report — the Pod Gauntlet "Deck Page" design (DeckPage.dc.html),
// ported to React and driven by the baked per-deck payload (getDeck). One
// inverted-pyramid spine with a Brief/Full toggle persisted to localStorage:
//   BRIEF  (returning player) — vital signs, the kill lines that win, the mulligan
//          heuristic + one sample keep hand, the top don't-miss rulings.
//   FULL   (first-timer)      — Tale-of-the-Tape band clock, How It Kills (ladder /
//          vectors / beatdown), openings, composition + Judges' Card, the full
//          decklist + mana curve, the interactive Mulligan Trainer, all rulings.
// All deck-specific content comes from the data layer; nothing is hardcoded here.
import { useMemo, useState } from "react";
import { SegmentedControl } from "../../components";
import { getDeck } from "../data";
import type { DeckPage as DeckPageData, KillTree, MullHand } from "../data";
import { usePageData } from "../hooks";
import s from "../pages.module.css";

const MODE_KEY = "pg_deckpage_mode";

// round newsprint mana pips (the design's hero pips)
const PIP: Record<string, string> = { W: "#e8e0c8", U: "#0a6c87", B: "#3a3340", R: "#b8331f", G: "#4f6b1e", C: "#8b8273" };
// composition legend — red marks the wincon bucket, everything else a muted ramp
const MUTED = ["var(--spot)", "#946112", "#6f5577", "#08505f", "#4f6b1e", "#a8662e", "#5b544a", "#0a6c87", "#8b8273", "#b57614", "#7a6f5c", "#2a251d"];

/** Trusted KB strings carry `<br/>` line breaks — render them as real breaks. */
function brk(text: string) {
  return text.split(/<br\s*\/?>/i).map((part, i, a) => (
    <span key={i}>{part}{i < a.length - 1 && <br />}</span>
  ));
}

/** Card hover preview — the baked name → Scryfall-image map (d.images) rendered as
 *  a floating card next to the cursor. bind(name) returns the pointer handlers for
 *  any element showing a card name; it returns {} when no image exists (bulk absent
 *  at bake time, or an unresolved spelling), so previews degrade silently. Mouse =
 *  hover; touch = tap to toggle. */
type PreviewState = { src: string; x: number; y: number } | null;
type Bind = (name: string) => React.HTMLAttributes<HTMLElement>;

function useCardPreview(images: Record<string, string> | null | undefined): { bind: Bind; preview: PreviewState } {
  const [preview, setPreview] = useState<PreviewState>(null);
  const bind: Bind = (name) => {
    const src = images?.[name];
    if (!src) return {};
    return {
      style: { cursor: "zoom-in" },
      onPointerEnter: (e) => { if (e.pointerType === "mouse") setPreview({ src, x: e.clientX, y: e.clientY }); },
      onPointerMove: (e) => { if (e.pointerType === "mouse") setPreview({ src, x: e.clientX, y: e.clientY }); },
      onPointerLeave: () => setPreview(null),
      onPointerDown: (e) => {
        if (e.pointerType !== "mouse") setPreview((p) => (p?.src === src ? null : { src, x: e.clientX, y: e.clientY }));
      },
    };
  };
  return { bind, preview };
}

function CardPreview({ p }: { p: PreviewState }) {
  if (!p) return null;
  const W = 250, H = Math.round(W * 1.395), pad = 10, off = 18;   // Scryfall 'normal' is 488×680
  const right = p.x + off + W <= window.innerWidth - pad;
  const x = right ? p.x + off : Math.max(pad, p.x - off - W);
  const y = Math.min(Math.max(pad, p.y - H / 2), Math.max(pad, window.innerHeight - H - pad));
  return (
    <img src={p.src} alt="" width={W} height={H}
      style={{ position: "fixed", left: x, top: y, width: W, height: H, zIndex: 60, pointerEvents: "none",
               borderRadius: 12, background: "var(--ink)", boxShadow: "0 10px 28px rgba(22,19,15,.45)" }} />
  );
}

function Pips({ letters, size = 15 }: { letters: string[]; size?: number }) {
  return (
    <span style={{ display: "flex", gap: 5 }}>
      {letters.map((p, i) => (
        <i key={i} style={{ width: size, height: size, borderRadius: "50%", border: "1.5px solid var(--ink)", background: PIP[p] ?? PIP.C, display: "inline-block" }} />
      ))}
    </span>
  );
}

function Chip({ text, primary }: { text: string; primary?: boolean }) {
  const c = primary ? "var(--acc)" : "var(--spot)";
  if (!text) return null;
  return (
    <span style={{ fontFamily: "var(--mono)", fontSize: 8.5, letterSpacing: ".06em", textTransform: "uppercase", color: c, border: `1px solid ${c}`, padding: "1px 6px" }}>{text}</span>
  );
}

/** The Tale-of-the-Tape band chart: decap / table medians (or ranges) on a turn axis. */
function ClockChart({ clock }: { clock: DeckPageData["clock"] }) {
  const mL = 50, mR = 728;
  const span = clock.axisTo - clock.axisFrom || 1;
  const x = (t: number) => mL + ((t - clock.axisFrom) / span) * (mR - mL);
  const kindColor = (k: string) => (k === "table" ? "var(--acc)" : "var(--spot2)");
  const rowY: Record<string, number> = { decap: 30, table: 70 };
  const rowH = 28;
  if (!clock.bands.length) return null;
  return (
    <svg viewBox="0 0 760 140" style={{ width: "100%", height: "auto", display: "block" }}>
      <line x1={mL} y1={112} x2={mR} y2={112} stroke="#16130f" strokeWidth={1} />
      {clock.ticks.map((t, i) => (
        <g key={`t${i}`}>
          <line x1={x(t)} y1={109} x2={x(t)} y2={115} stroke="#8b8273" strokeWidth={0.8} />
          <text x={x(t)} y={130} fontSize={10} fontFamily="'IBM Plex Mono',monospace" fill="#8b8273" textAnchor="middle">T{t}</text>
        </g>
      ))}
      {clock.bands.map((b, i) => {
        const y = rowY[b.kind] ?? 30;
        const col = kindColor(b.kind);
        return (
          <g key={`b${i}`}>
            <text x={mL - 8} y={y + rowH / 2 + 4} fontSize={11} fontFamily="'Oswald',sans-serif" fontWeight={600} fill="#16130f" textAnchor="end">{b.label.toUpperCase()}</text>
            {b.from === b.to ? (
              <>
                <line x1={x(b.from)} y1={y} x2={x(b.from)} y2={112} stroke={col} strokeWidth={1} strokeDasharray="2 3" opacity={0.5} />
                <circle cx={x(b.from)} cy={y + rowH / 2} r={8} fill={col} />
                <text x={x(b.from) + 14} y={y + rowH / 2 + 4} fontSize={12} fontFamily="'Oswald',sans-serif" fontWeight={700} fill={col}>T{b.from}</text>
              </>
            ) : (
              <>
                <rect x={x(b.from)} y={y} width={x(b.to) - x(b.from)} height={rowH} fill={col} opacity={0.92} />
                <text x={(x(b.from) + x(b.to)) / 2} y={y + rowH / 2 + 4} fontSize={11} fontFamily="'IBM Plex Mono',monospace" fill="#f1ecdf" textAnchor="middle">T{b.from}–{b.to}</text>
                {b.typical != null && (
                  <>
                    <line x1={x(b.typical)} y1={y - 4} x2={x(b.typical)} y2={y + rowH + 4} stroke="#16130f" strokeWidth={1.5} />
                    <text x={x(b.typical)} y={y - 7} fontSize={9} fontFamily="'IBM Plex Mono',monospace" fill="#16130f" textAnchor="middle">typ T{b.typical}</text>
                  </>
                )}
              </>
            )}
          </g>
        );
      })}
    </svg>
  );
}

function ClockCell({ c }: { c: DeckPageData["clock"]["headline"][number] }) {
  return (
    <div style={{ padding: "14px 18px", textAlign: "center" }}>
      <div style={{ fontFamily: "var(--mono)", fontSize: 9.5, letterSpacing: ".12em", textTransform: "uppercase", color: "var(--ink2)" }}>{c.label}</div>
      <div style={{ fontFamily: "var(--disp)", fontWeight: 700, fontSize: 40, lineHeight: 1, marginTop: 4, color: c.kind === "table" ? "var(--acc)" : "var(--ink)" }}>{c.value}</div>
      <div style={{ fontFamily: "var(--mono)", fontSize: 9.5, color: "var(--ink3)", marginTop: 2, textTransform: "uppercase" }}>{c.sub}</div>
    </div>
  );
}

/** Beatdown board-power → alpha curve (Eldrazi): area curve vs a lethal reference line. */
function KillCurve({ kt }: { kt: KillTree }) {
  const c = kt.curve;
  if (!c || !c.length || kt.lethalAt == null) return null;
  const mL = 46, mR = 712, t0 = c[0].t, t1 = c[c.length - 1].t;
  const yMax = Math.max(kt.lethalAt, ...c.map((p) => p.p)) * 1.14;
  const base = 74, top = 12;
  const x = (t: number) => mL + ((t - t0) / (t1 - t0 || 1)) * (mR - mL);
  const y = (p: number) => base - (p / yMax) * (base - top);
  let d = `M ${x(t0)} ${base}`;
  c.forEach((p) => (d += ` L ${x(p.t)} ${y(p.p)}`));
  d += ` L ${x(t1)} ${base} Z`;
  const ly = y(kt.lethalAt);
  return (
    <svg viewBox="0 0 760 94" style={{ width: "100%", height: "auto", display: "block" }}>
      <path d={d} fill="var(--spot)" opacity={0.13} />
      <line x1={mL} y1={base} x2={mR} y2={base} stroke="#16130f" strokeWidth={1} />
      <line x1={mL} y1={ly} x2={mR} y2={ly} stroke="var(--acc)" strokeWidth={1} strokeDasharray="4 3" />
      <text x={mR} y={ly - 4} fontSize={9} fontFamily="'IBM Plex Mono',monospace" fill="var(--acc)" textAnchor="end">{kt.lethalLabel ?? "lethal"}</text>
      <polyline points={c.map((p) => `${x(p.t)},${y(p.p)}`).join(" ")} fill="none" stroke="var(--spot2)" strokeWidth={2} />
      {c.map((p, i) => (
        <g key={i}>
          <circle cx={x(p.t)} cy={y(p.p)} r={2.8} fill="var(--spot2)" />
          <text x={x(p.t)} y={base + 14} fontSize={9} fontFamily="'IBM Plex Mono',monospace" fill="#8b8273" textAnchor="middle">T{p.t}</text>
        </g>
      ))}
    </svg>
  );
}

/** The how-it-kills index glyph flips with the kill module's mode. */
function KillIdx({ mode, i }: { mode: string; i: number }) {
  if (mode === "vectors") return <span style={{ fontFamily: "var(--disp)", fontWeight: 700, fontSize: 17, color: "var(--spot)" }}>↗</span>;
  if (mode === "beatdown") {
    return (
      <svg width={18} height={16} viewBox="0 0 18 16" style={{ display: "block" }}>
        <rect x={0} y={9} width={4} height={7} fill="var(--spot)" />
        <rect x={6} y={5} width={4} height={11} fill="var(--spot)" />
        <rect x={12} y={0} width={4} height={16} fill="var(--acc)" />
      </svg>
    );
  }
  return <span style={{ fontFamily: "var(--disp)", fontWeight: 700, fontSize: 16, color: "var(--ink3)" }}>{String(i + 1).padStart(2, "0")}</span>;
}

const SectionBand = ({ id, title, hint, paper2 }: { id?: string; title: string; hint?: string; paper2?: boolean }) => (
  <div id={id} className={s.scoutBand} style={paper2 ? { background: "var(--paper2)" } : undefined}>
    <span className={s.scoutTick} />
    <span className={s.scoutBandTitle}>{title}</span>
    {hint && <span className={s.scoutBandHint}>{hint}</span>}
  </div>
);

const KickerBand = ({ id, kicker, hint, paper2 }: { id?: string; kicker: string; hint?: string; paper2?: boolean }) => (
  <div id={id} className={s.scoutBand} style={paper2 ? { background: "var(--paper2)" } : undefined}>
    <span className={s.scoutKicker}>{kicker}</span>
    <span style={{ flex: 1, height: 1, background: "var(--hair)" }} />
    {hint && <span className={s.scoutBandHint}>{hint}</span>}
  </div>
);

/** Keep-or-mull drill on baked hands. The verdict is the AUTHORITATIVE deck_sim
 *  keep_hand, computed in Python and baked — the client only reveals + scores it. */
function MulliganTrainer({ d, bind }: { d: DeckPageData; bind: Bind }) {
  const m = d.mulligan;
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

  return (
    <>
      <SectionBand id="mulligan" title="Mulligan Trainer" hint="keep or mull?" paper2 />
      <div style={{ background: "var(--paper2)", padding: "16px 26px 6px" }}>
        <div style={{ fontFamily: "var(--mono)", fontSize: 10.5, color: "var(--ink2)", marginBottom: 14, letterSpacing: ".02em" }}>
          Score yourself vs the deck_sim plan-keep model · plan axis <strong style={{ color: "var(--ink)" }}>{m.axisGloss[m.bottleneck] ?? m.bottleneck}</strong> · land band <strong style={{ color: "var(--ink)" }}>{m.minLands}–{m.maxLands}</strong>
        </div>
        <div style={{ display: "grid", gridTemplateColumns: "repeat(7,1fr)", gap: 6, marginBottom: 14 }}>
          {hand.cards.map((c, i) => (
            <div key={i} className={s.scoutHandCard} {...bind(c.n)}>
              <span style={{ fontFamily: "var(--mono)", fontSize: 11, fontWeight: 600, color: "var(--spot)" }}>{c.land ? "▦" : c.cmc ?? "—"}</span>
              <span style={{ fontFamily: "var(--disp)", fontWeight: 500, fontSize: 10.5, lineHeight: 1.08, textTransform: "uppercase", flex: 1 }}>{c.n}</span>
              <span style={{ display: "flex", flexWrap: "wrap", gap: 3 }}>
                {c.tags.filter((t) => t !== "LAND").map((t) => (
                  <span key={t} style={{ fontFamily: "var(--mono)", fontSize: 7.5, letterSpacing: ".04em", color: "var(--ink3)", border: "1px solid var(--hair)", padding: "1px 3px" }}>{t}</span>
                ))}
              </span>
            </div>
          ))}
        </div>
        <div style={{ fontFamily: "var(--mono)", fontSize: 9.5, letterSpacing: ".06em", textTransform: "uppercase", color: "var(--ink3)", marginBottom: 12 }}>{hand.lands} lands in hand</div>
        {guess === null ? (
          <div style={{ display: "flex", gap: 10 }}>
            <button onClick={() => answer(true)} style={{ flex: 1, fontFamily: "var(--disp)", fontWeight: 600, fontSize: 15, letterSpacing: ".1em", textTransform: "uppercase", padding: 11, background: "var(--good)", color: "var(--paper)", border: "none", cursor: "pointer" }}>Keep</button>
            <button onClick={() => answer(false)} style={{ flex: 1, fontFamily: "var(--disp)", fontWeight: 600, fontSize: 15, letterSpacing: ".1em", textTransform: "uppercase", padding: 11, background: "transparent", color: "var(--ink)", border: "1.5px solid var(--ink)", cursor: "pointer" }}>Mulligan</button>
          </div>
        ) : (
          <div style={{ border: "1.5px solid var(--ink)", padding: "13px 15px" }}>
            <div style={{ display: "flex", alignItems: "center", gap: 12, flexWrap: "wrap", marginBottom: 9 }}>
              <span style={{ fontFamily: "var(--disp)", fontWeight: 700, fontSize: 15, letterSpacing: ".08em", textTransform: "uppercase", color: hand.keep ? "var(--good)" : "var(--acc)" }}>model: {hand.keep ? "KEEP" : "MULL"}</span>
              <span style={{ fontFamily: "var(--mono)", fontSize: 11, fontWeight: 600, color: guess === hand.keep ? "var(--good)" : "var(--acc)" }}>{guess === hand.keep ? "✓ you agreed" : `✗ you said ${guess ? "KEEP" : "MULL"}`}</span>
              <button onClick={next} style={{ marginLeft: "auto", fontFamily: "var(--mono)", fontSize: 11, textTransform: "uppercase", letterSpacing: ".06em", background: "var(--ink)", color: "var(--paper)", border: "none", padding: "7px 13px", cursor: "pointer" }}>next hand →</button>
            </div>
            <div style={{ display: "flex", flexDirection: "column", gap: 5 }}>
              {hand.reasons.map((r, i) => (
                <div key={i} style={{ display: "grid", gridTemplateColumns: "auto 1fr", gap: 8, fontSize: 12.5, lineHeight: 1.4, color: "var(--ink2)" }}>
                  <span style={{ fontFamily: "var(--mono)", color: "var(--ink3)" }}>·</span><span>{r}</span>
                </div>
              ))}
            </div>
          </div>
        )}
        {score.seen > 0 && (
          <div style={{ fontFamily: "var(--mono)", fontSize: 10, letterSpacing: ".06em", textTransform: "uppercase", color: "var(--ink3)", marginTop: 11 }}>
            agreed {score.agree}/{score.seen} · {Math.round((100 * score.agree) / score.seen)}%
          </div>
        )}
      </div>
    </>
  );
}

/** The full 100-card list grouped by the Summary's functional buckets, with a
 *  role/type toggle, copy button, and the mana curve — the pick-up-and-play reference. */
function Decklist({ d, bind }: { d: DeckPageData; bind: Bind }) {
  const dl = d.decklist;
  const [copied, setCopied] = useState(false);
  const [view, setView] = useState<"role" | "type">("role");
  if (!dl) return null;
  const cb = bind(dl.commander.n);
  const buckets = view === "type" && dl.groupsByType ? dl.groupsByType : dl.groups;
  const gcSet = new Set(d.gc);
  const curveMax = Math.max(1, ...(dl.curve ?? []).map((c) => c.n));
  const copy = () => navigator.clipboard?.writeText(dl.text).then(
    () => { setCopied(true); setTimeout(() => setCopied(false), 1600); },
    () => {},
  );
  return (
    <>
      <SectionBand id="decklist" title="The Decklist" hint={`${dl.total} cards · ${d.images ? "hover a name to preview" : "pick up & play"}`} />
      <div style={{ padding: "18px 26px 8px" }}>
        <div className={s.scoutDlControls}>
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
        {dl.curve && (
          <div style={{ display: "flex", alignItems: "flex-end", gap: 8, marginBottom: 16 }}>
            <div style={{ fontFamily: "var(--mono)", fontSize: 9, letterSpacing: ".08em", textTransform: "uppercase", color: "var(--ink2)", writingMode: "vertical-rl", transform: "rotate(180deg)", alignSelf: "stretch", display: "flex", alignItems: "center" }}>Mana curve</div>
            <div style={{ display: "flex", alignItems: "flex-end", gap: 7, height: 74, flex: 1 }}>
              {dl.curve.map((b) => (
                <div key={b.cmc} style={{ flex: 1, display: "flex", flexDirection: "column", alignItems: "center", gap: 4, height: "100%", justifyContent: "flex-end" }}>
                  <span style={{ fontFamily: "var(--mono)", fontSize: 9.5, color: "var(--ink2)" }}>{b.n || ""}</span>
                  <div style={{ width: "100%", height: `${(b.n / curveMax) * 100}%`, background: "var(--ink2)", minHeight: 2 }} />
                  <span style={{ fontFamily: "var(--mono)", fontSize: 9, color: "var(--ink3)" }}>{b.cmc}</span>
                </div>
              ))}
            </div>
          </div>
        )}
        <div style={{ fontFamily: "var(--mono)", fontSize: 10, letterSpacing: ".06em", textTransform: "uppercase", color: "var(--ink)", borderBottom: "1.5px solid var(--ink)", paddingBottom: 7, marginBottom: 12 }}>
          Commander · <span {...cb} style={{ fontWeight: 600, ...cb.style }}>{dl.commander.n}</span>{dl.commander.gc && <span className={s.dlGc}>GC</span>}
        </div>
        <div style={{ columnCount: 2, columnGap: 26 }}>
          {buckets.map((g, i) => (
            <div key={`${view}-${i}`} style={{ breakInside: "avoid", marginBottom: 15 }}>
              <div style={{ display: "flex", alignItems: "baseline", gap: 8, borderBottom: "1px solid var(--hair)", paddingBottom: 5, marginBottom: 6 }}>
                <span style={{ fontFamily: "var(--disp)", fontWeight: 600, fontSize: 12.5, letterSpacing: ".06em", textTransform: "uppercase" }}>{g.name}</span>
                <span style={{ fontFamily: "var(--mono)", fontSize: 10, color: "var(--ink3)", marginLeft: "auto" }}>{g.count}</span>
              </div>
              {g.cards.map((c, j) => (
                <div key={j} style={{ display: "flex", alignItems: "center", gap: 7, fontSize: 12.5, lineHeight: 1.5, color: "var(--ink)" }}>
                  <span {...bind(c.n)}>{c.n}</span>{(c.gc || gcSet.has(c.n)) && <span className={s.dlGc}>GC</span>}
                </div>
              ))}
            </div>
          ))}
        </div>
      </div>
    </>
  );
}

/** How It Kills — the kill module, flipping ladder / vectors / beatdown by mode. */
function HowItKills({ d }: { d: DeckPageData }) {
  const kt = d.killTree;
  // fall back to the Summary finishers for any deck without a registry kill tree
  const lines = kt
    ? kt.lines.map((l, i) => ({ tag: l.tag, primary: l.primary, need: l.need, kill: l.kill, clock: l.clock, i }))
    : d.finishers.map((f, i) => ({ tag: f.tag, primary: i === 0, need: f.name, kill: f.note, clock: "", i }));
  const mode = kt?.mode ?? "ladder";
  return (
    <>
      <SectionBand id="kills" title="How It Kills" hint={kt?.caption ?? "how it wins"} />
      <div style={{ padding: "18px 26px 8px" }}>
        {kt && (
          <div style={{ display: "grid", gridTemplateColumns: "auto 1fr", gap: 11, alignItems: "start", marginBottom: 14 }}>
            <span style={{ fontFamily: "var(--mono)", fontSize: 8.5, letterSpacing: ".08em", textTransform: "uppercase", color: "var(--spot)", border: "1px solid var(--spot)", padding: "3px 6px", whiteSpace: "nowrap", marginTop: 1 }}>The engine</span>
            <span style={{ fontFamily: "var(--serif)", fontSize: 13, lineHeight: 1.45, color: "var(--ink2)" }}>{brk(kt.root)}</span>
          </div>
        )}
        {kt?.curve && (
          <div style={{ margin: "2px 0 15px" }}>
            <div style={{ fontFamily: "var(--mono)", fontSize: 9, letterSpacing: ".08em", textTransform: "uppercase", color: "var(--ink3)", marginBottom: 5 }}>Board power → alpha · goldfish</div>
            <KillCurve kt={kt} />
          </div>
        )}
        <div style={{ display: "flex", flexDirection: "column", gap: 9 }}>
          {lines.map((l) => (
            <div key={l.i} style={{ display: "grid", gridTemplateColumns: "30px 1fr auto 1.25fr", gap: 11, alignItems: "center", borderTop: "1px solid var(--hair2)", paddingTop: 9 }}>
              <KillIdx mode={mode} i={l.i} />
              <span style={{ fontFamily: "var(--serif)", fontSize: 12.5, lineHeight: 1.4, color: "var(--ink2)" }}>{brk(l.need)}</span>
              <span style={{ fontFamily: "var(--mono)", color: "var(--ink3)", fontSize: 13 }}>→</span>
              <div>
                <div style={{ fontFamily: "var(--serif)", fontSize: 12.5, lineHeight: 1.35 }}>{brk(l.kill)}</div>
                <div style={{ display: "flex", gap: 9, alignItems: "center", marginTop: 3 }}>
                  <Chip text={l.tag} primary={l.primary} />
                  {l.clock && <span style={{ fontFamily: "var(--mono)", fontSize: 9.5, color: "var(--ink3)" }}>⏱ {l.clock}</span>}
                </div>
              </div>
            </div>
          ))}
        </div>
        {kt && (
          <>
            <div style={{ display: "flex", gap: 10, alignItems: "baseline", marginTop: 12, paddingTop: 10, borderTop: "1px solid var(--hair)", fontSize: 12, lineHeight: 1.45, color: "var(--ink2)" }}>
              <span style={{ fontFamily: "var(--mono)", fontSize: 8.5, letterSpacing: ".08em", textTransform: "uppercase", color: "var(--ink)", flex: "none" }}>{kt.stallLabel}</span>
              <span>{brk(kt.stall)}</span>
            </div>
            <div style={{ fontFamily: "var(--mono)", fontSize: 9, color: "var(--ink3)", marginTop: 6 }}>{kt.src}</div>
          </>
        )}
        {/* openings */}
        <div style={{ display: "flex", alignItems: "baseline", gap: 10, margin: "20px 0 8px" }}>
          <span style={{ width: 8, height: 8, border: "1.5px solid var(--ink)" }} />
          <span style={{ fontFamily: "var(--disp)", fontWeight: 600, fontSize: 13, letterSpacing: ".14em", textTransform: "uppercase" }}>Openings</span>
          <span style={{ fontFamily: "var(--mono)", fontSize: 9, textTransform: "uppercase", color: "var(--ink3)" }}>how it loses</span>
        </div>
        <div style={{ display: "flex", flexDirection: "column", gap: 7, paddingBottom: 6 }}>
          {d.openings.map((w, i) => (
            <div key={i} style={{ display: "grid", gridTemplateColumns: "auto 1fr", gap: 10, fontSize: 12.5, lineHeight: 1.42, color: "var(--ink)" }}>
              <span style={{ fontFamily: "var(--mono)", fontSize: 11, color: "var(--ink3)" }}>→</span><span>{w}</span>
            </div>
          ))}
        </div>
      </div>
    </>
  );
}

const NAV = [
  ["#clock", "Clock"], ["#kills", "Kills"], ["#build", "Build"],
  ["#decklist", "Decklist"], ["#mulligan", "Mulligan"], ["#rulings", "Rulings"],
];

export function DeckPage({ slug, onBack }: { slug: string; onBack: () => void }) {
  const { data: d, error } = usePageData<DeckPageData>(() => getDeck(slug), [slug]);
  const { bind, preview } = useCardPreview(d?.images);
  const [mode, setModeState] = useState<"brief" | "full">(() => {
    try { return localStorage.getItem(MODE_KEY) === "full" ? "full" : "brief"; } catch { return "brief"; }
  });
  const setMode = (m: "brief" | "full") => {
    setModeState(m);
    try { localStorage.setItem(MODE_KEY, m); } catch { /* storage blocked */ }
  };

  if (error) return <div className={s.error}>error: {error}</div>;
  if (!d) return <div className={s.loading}>loading deck…</div>;

  const isFull = mode === "full";
  const compTotal = d.composition.reduce((sum, b) => sum + b.count, 0) || 1;
  const lowAxis = d.axes.length ? Math.min(...d.axes.map((a) => a.score)) : 0;
  // the brief sample keep: a real baked keep-hand + the model's own reasons (card-accurate)
  const sample = d.mulligan?.hands.find((h) => h.keep) ?? null;

  const modeBtn = (m: "brief" | "full", label: string, last: boolean) => (
    <button onClick={() => setMode(m)} style={{ fontFamily: "var(--mono)", fontSize: 10.5, letterSpacing: ".1em", textTransform: "uppercase", padding: "5px 13px", cursor: "pointer", border: "1.5px solid var(--ink)", borderRight: last ? "1.5px solid var(--ink)" : "none", background: mode === m ? "var(--ink)" : "transparent", color: mode === m ? "var(--paper)" : "var(--ink)" }}>{label}</button>
  );

  return (
    <article className={s.scout} style={{ ["--spot" as string]: "#0b6478", ["--spot2" as string]: "#08505f" } as React.CSSProperties}>
      <CardPreview p={preview} />
      {/* top strip */}
      <div className={s.scoutTop}>
        <button className={s.scoutBack} onClick={onBack}>← Roster · Scouting Report</button>
        <span>{d.corner}</span>
      </div>

      {/* sticky nav · Brief/Full toggle */}
      <div className={s.scoutNav}>
        <div style={{ display: "flex" }}>{modeBtn("brief", "Brief", false)}{modeBtn("full", "Full", true)}</div>
        {isFull ? (
          <span style={{ marginLeft: "auto", display: "flex", gap: 2, flexWrap: "wrap" }}>
            {NAV.map(([href, label]) => (
              <a key={href} className={s.nv} href={href}>{label}</a>
            ))}
          </span>
        ) : (
          <span style={{ marginLeft: "auto", fontFamily: "var(--mono)", fontSize: 9.5, letterSpacing: ".1em", textTransform: "uppercase", color: "var(--ink3)" }}>Returning-player refresher</span>
        )}
      </div>

      {/* hero */}
      <div id="overview" className={s.scoutHero}>
        <div style={{ minWidth: 0 }}>
          <div style={{ fontFamily: "var(--mono)", fontSize: 11, letterSpacing: ".2em", textTransform: "uppercase", color: "var(--ink2)", marginBottom: 10 }}>{d.kicker}</div>
          <h1 className={s.scoutTitle}>{d.name}</h1>
          <div style={{ display: "flex", alignItems: "center", gap: 11, flexWrap: "wrap" }}>
            <Pips letters={d.pips} />
            <span style={{ fontFamily: "var(--mono)", fontSize: 12.5, color: "var(--ink2)" }}>{d.commander} · {d.archetype}</span>
          </div>
        </div>
        <div className={s.scoutIdea}>
          <div className={s.scoutIdeaHead}>The Idea</div>
          <div style={{ fontSize: 13, lineHeight: 1.5, padding: "11px 14px 13px" }}>{d.idea}</div>
        </div>
      </div>

      {isFull ? (
        <>
          {/* clock */}
          <div id="clock" className={s.scoutClockBar}>
            <span style={{ fontFamily: "var(--disp)", fontWeight: 600, fontSize: 18, letterSpacing: ".24em", textTransform: "uppercase", whiteSpace: "nowrap" }}>Tale of the Tape</span>
            <span style={{ flex: 1, height: 1, background: "var(--paper)", opacity: 0.4 }} />
            <span style={{ fontFamily: "var(--mono)", fontSize: 10, letterSpacing: ".1em", textTransform: "uppercase", opacity: 0.85 }}>{d.clock.sub}</span>
          </div>
          <div style={{ padding: "20px 26px 24px" }}>
            <div style={{ display: "grid", gridTemplateColumns: "1fr 56px 1fr", alignItems: "stretch", border: "1.5px solid var(--ink)", marginBottom: 14 }}>
              {d.clock.headline[0] && <ClockCell c={d.clock.headline[0]} />}
              <div style={{ display: "flex", alignItems: "center", justifyContent: "center", fontFamily: "var(--disp)", fontWeight: 700, fontSize: 18, color: "var(--paper)", background: "var(--ink)" }}>VS</div>
              {d.clock.headline[1] && <ClockCell c={d.clock.headline[1]} />}
            </div>
            {d.clock.note && (
              <div style={{ display: "grid", gridTemplateColumns: "auto 1fr", gap: 10, alignItems: "start", marginBottom: 14 }}>
                <span style={{ fontFamily: "var(--mono)", fontSize: 8.5, letterSpacing: ".06em", textTransform: "uppercase", color: "var(--acc)", border: "1px solid var(--acc)", padding: "3px 6px", whiteSpace: "nowrap", marginTop: 1 }}>{d.clock.noteLabel}</span>
                <span style={{ fontSize: 12.5, lineHeight: 1.45, color: "var(--ink2)" }}>{d.clock.note}</span>
              </div>
            )}
            <ClockChart clock={d.clock} />
            <div style={{ fontSize: 12.5, lineHeight: 1.45, color: "var(--ink2)", marginTop: 8 }}>{d.clock.caption} <span style={{ fontFamily: "var(--mono)", fontSize: 10, color: "var(--ink3)" }}>{d.clock.src}</span></div>
          </div>

          <HowItKills d={d} />

          {/* for the record */}
          <KickerBand id="build" kicker="For the record" hint="100 cards · the build" paper2 />
          <div style={{ display: "grid", gridTemplateColumns: "1.45fr 1fr", background: "var(--paper2)", color: "var(--ink2)" }}>
            <div style={{ padding: "18px 22px 22px 26px", borderRight: "1px solid var(--hair)" }}>
              <div style={{ fontFamily: "var(--mono)", fontSize: 10, letterSpacing: ".1em", textTransform: "uppercase", color: "var(--ink2)", marginBottom: 9 }}>Composition</div>
              <div style={{ display: "flex", height: 30, border: "1.5px solid var(--ink)" }}>
                {d.composition.map((b, i) => (
                  <div key={i} style={{ width: `${(b.count / compTotal) * 100}%`, background: b.win ? "var(--acc)" : MUTED[i % MUTED.length] }} />
                ))}
              </div>
              <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: "5px 22px", marginTop: 12 }}>
                {d.composition.map((b, i) => (
                  <span key={i} style={{ display: "grid", gridTemplateColumns: "auto 1fr auto", alignItems: "center", gap: 7, fontFamily: "var(--mono)", fontSize: 9.5, letterSpacing: ".02em", textTransform: "uppercase", color: "var(--ink2)", minWidth: 0 }}>
                    <span style={{ width: 10, height: 10, background: b.win ? "var(--acc)" : MUTED[i % MUTED.length], border: "1px solid var(--ink)", flex: "none", display: "inline-block" }} />
                    <span style={{ overflow: "hidden", textOverflow: "ellipsis", whiteSpace: "nowrap" }}>{b.name}</span>
                    <span style={{ color: "var(--ink)", fontWeight: 600 }}>{b.count}</span>
                  </span>
                ))}
              </div>
            </div>
            <div style={{ padding: "18px 26px 22px 22px" }}>
              <div style={{ fontFamily: "var(--mono)", fontSize: 10, letterSpacing: ".1em", textTransform: "uppercase", color: "var(--ink2)", marginBottom: 11 }}>The Judges' Card · {d.axesTotal}</div>
              <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 9, marginBottom: 15 }}>
                {d.axes.map((a, i) => {
                  const lc = a.score === lowAxis ? "var(--ink2)" : "var(--ink)";
                  return (
                    <div key={i} style={{ border: "1px solid var(--hair)", padding: "9px 11px" }}>
                      <div style={{ fontFamily: "var(--mono)", fontSize: 9, letterSpacing: ".04em", textTransform: "uppercase", color: "var(--ink2)" }}>{a.label}</div>
                      <div style={{ fontFamily: "var(--disp)", fontWeight: 700, fontSize: 21, lineHeight: 1, margin: "5px 0 6px", color: lc }}>{a.score}<span style={{ fontFamily: "var(--mono)", fontSize: 10, color: "var(--ink3)", fontWeight: 400 }}>/5</span></div>
                      <div style={{ height: 7, background: "var(--hair2)" }}><span style={{ display: "block", height: "100%", width: `${(a.score / 5) * 100}%`, background: lc }} /></div>
                    </div>
                  );
                })}
              </div>
              <div style={{ fontFamily: "var(--mono)", fontSize: 10, letterSpacing: ".1em", textTransform: "uppercase", color: "var(--ink2)", marginBottom: 9 }}>Game Changers · {d.gc.length}/3</div>
              <div style={{ display: "flex", flexDirection: "column", gap: 7 }}>
                {d.gc.map((g, i) => (
                  <div key={i} style={{ display: "flex", alignItems: "center", gap: 9, fontSize: 13, color: "var(--ink2)" }}>
                    <span style={{ fontFamily: "var(--mono)", fontWeight: 600, fontSize: 9, letterSpacing: ".06em", color: "var(--gold)", border: "1.5px solid var(--gold)", padding: "2px 5px", flex: "none" }}>GC</span>{g}
                  </div>
                ))}
              </div>
            </div>
          </div>

          <Decklist d={d} bind={bind} />
          <MulliganTrainer d={d} bind={bind} />

          {/* rulings */}
          {d.rulings.length > 0 && (
            <>
              <KickerBand id="rulings" kicker="Don't Miss" hint="rulings that decide games" />
              <div style={{ padding: "18px 26px 8px", display: "grid", gridTemplateColumns: "1fr 1fr", gap: "13px 22px" }}>
                {d.rulings.map((r, i) => (
                  <div key={i} style={{ display: "grid", gridTemplateColumns: "auto 1fr", gap: 10 }}>
                    <span style={{ width: 8, height: 8, background: "var(--spot)", flex: "none", marginTop: 5 }} />
                    <div>
                      {r.name && <div style={{ fontFamily: "var(--disp)", fontWeight: 600, fontSize: 13.5, textTransform: "uppercase", letterSpacing: ".01em" }}>{r.name}</div>}
                      <div style={{ fontSize: 12.5, lineHeight: 1.45, color: "var(--ink2)", marginTop: 2 }}>{r.note}</div>
                    </div>
                  </div>
                ))}
              </div>
            </>
          )}
        </>
      ) : (
        <>
          {/* ===== BRIEF ===== */}
          {/* vital signs */}
          <div className={s.scoutVitals}>
            {d.vitals.map((v, i) => (
              <div key={i} className={s.scoutVital}>
                <div style={{ fontFamily: "var(--mono)", fontSize: 9, letterSpacing: ".14em", textTransform: "uppercase", color: "var(--ink3)", marginBottom: 7 }}>{v.label}</div>
                <div style={{ fontFamily: "var(--disp)", fontWeight: 700, fontSize: i === 0 ? 30 : 22, lineHeight: i === 0 ? 1 : 1.04, textTransform: i === 0 ? "none" : "uppercase", color: v.accent ? "var(--acc)" : "var(--ink)" }}>{v.value}</div>
                <div style={{ fontFamily: "var(--mono)", fontSize: 9, color: "var(--ink3)", marginTop: 6, letterSpacing: ".03em" }}>{v.sub}</div>
              </div>
            ))}
          </div>

          {/* kill lines */}
          <SectionBand title="Kill Lines" hint={d.briefKillsCaption} />
          <div style={{ padding: "16px 26px 20px", display: "flex", flexDirection: "column", gap: 13 }}>
            {d.briefKills.map((l, i) => (
              <div key={i} style={{ display: "grid", gridTemplateColumns: "26px 1fr", gap: 12, alignItems: "start" }}>
                <span style={{ fontFamily: "var(--disp)", fontWeight: 700, fontSize: 20, color: "var(--ink3)", lineHeight: 1.1 }}>{l.idx}</span>
                <div>
                  <div style={{ fontFamily: "var(--serif)", fontSize: 14, lineHeight: 1.4 }}>{l.line}</div>
                  <div style={{ display: "flex", gap: 9, alignItems: "center", marginTop: 5 }}>
                    <Chip text={l.tag} primary={l.primary} />
                    {l.clock && <span style={{ fontFamily: "var(--mono)", fontSize: 9.5, color: "var(--ink3)" }}>⏱ {l.clock}</span>}
                  </div>
                </div>
              </div>
            ))}
          </div>

          {/* mulligan heuristic + sample keep */}
          <SectionBand title="Mulligan" hint="the keep heuristic" paper2 />
          <div style={{ background: "var(--paper2)", padding: "16px 26px 20px" }}>
            <div style={{ fontFamily: "var(--serif)", fontSize: 14, lineHeight: 1.5, marginBottom: 16 }}>{d.mull.strategy}</div>
            {sample && (
              <>
                <div style={{ display: "flex", alignItems: "baseline", gap: 10, marginBottom: 9 }}>
                  <span style={{ fontFamily: "var(--mono)", fontSize: 9, letterSpacing: ".1em", textTransform: "uppercase", color: "var(--ink)" }}>Sample keep</span>
                  <span style={{ fontFamily: "var(--mono)", fontSize: 9, color: "var(--ink3)" }}>{sample.lands} lands</span>
                </div>
                <div style={{ display: "grid", gridTemplateColumns: "repeat(7,1fr)", gap: 6, marginBottom: 11 }}>
                  {sample.cards.map((c, i) => {
                    const cb = bind(c.n);
                    return (
                    <div key={i} className={s.scoutHandCard} {...cb} style={{ background: "var(--paper)", ...cb.style }}>
                      <span style={{ fontFamily: "var(--mono)", fontSize: 11, fontWeight: 600, color: "var(--spot)" }}>{c.land ? "▦" : c.cmc ?? "—"}</span>
                      <span style={{ fontFamily: "var(--disp)", fontWeight: 500, fontSize: 10.5, lineHeight: 1.08, textTransform: "uppercase", flex: 1 }}>{c.n}</span>
                      <span style={{ display: "flex", flexWrap: "wrap", gap: 3 }}>
                        {c.tags.filter((t) => t !== "LAND").map((t) => (
                          <span key={t} style={{ fontFamily: "var(--mono)", fontSize: 7.5, letterSpacing: ".04em", color: "var(--ink3)", border: "1px solid var(--hair)", padding: "1px 3px" }}>{t}</span>
                        ))}
                      </span>
                    </div>
                    );
                  })}
                </div>
                <div style={{ display: "flex", gap: 10, alignItems: "baseline", fontFamily: "var(--serif)", fontSize: 13, lineHeight: 1.45, color: "var(--ink2)" }}>
                  <span style={{ fontFamily: "var(--mono)", fontSize: 9, letterSpacing: ".08em", textTransform: "uppercase", color: "var(--ink)", flex: "none" }}>Why keep</span>
                  <span>{sample.reasons.join(" · ")}</span>
                </div>
              </>
            )}
          </div>

          {/* don't miss */}
          <KickerBand kicker="Don't Miss" hint="rulings that decide games" />
          <div style={{ padding: "16px 26px 20px", display: "flex", flexDirection: "column", gap: 12 }}>
            {d.rulings.slice(0, 3).map((r, i) => (
              <div key={i} style={{ display: "grid", gridTemplateColumns: "auto 1fr", gap: 11 }}>
                <span style={{ width: 8, height: 8, background: "var(--spot)", flex: "none", marginTop: 5 }} />
                <div>
                  {r.name && <div style={{ fontFamily: "var(--disp)", fontWeight: 600, fontSize: 14, textTransform: "uppercase", letterSpacing: ".01em" }}>{r.name}</div>}
                  <div style={{ fontSize: 13, lineHeight: 1.45, color: "var(--ink2)", marginTop: 2 }}>{r.note}</div>
                </div>
              </div>
            ))}
          </div>

          <div style={{ display: "flex", justifyContent: "center", padding: "6px 26px 22px" }}>
            <button onClick={() => setMode("full")} style={{ fontFamily: "var(--mono)", fontSize: 11, letterSpacing: ".1em", textTransform: "uppercase", color: "var(--ink)", background: "transparent", border: "1.5px solid var(--ink)", padding: "9px 18px", cursor: "pointer" }}>Full scouting report →</button>
          </div>
        </>
      )}

      {/* footer */}
      <div className={s.scoutFoot}>
        <span>{d.tagline}</span>
        <span style={{ flex: "none" }}>{d.colorLine}</span>
      </div>
    </article>
  );
}
