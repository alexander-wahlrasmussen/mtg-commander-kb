// Data layer — mirrors the vanilla dashboard: probe /api; if a live server answers
// use it, else fall back to precomputed /data/*.json (static mode). ?live / ?static override.

// Newsprint palette — inks / earth tones that read on cream paper (SVG fill needs real hex).
export const PALETTE = [
  "#c63a1b", "#5b544a", "#946112", "#6f5577", "#4f6b1e", "#076678", "#a8662e", "#8f3f71",
  "#427b58", "#b57614", "#9d0006", "#7c6f64", "#3a5e6b", "#79740e", "#af3a03", "#5b6c8f",
];

export interface ClockDeck {
  slug: string; name: string; score: number | null;
  grid: number[]; decap: number[]; table: number[]; med: [string, string]; never: [number, number]; src: string;
}
export interface ClocksData { horizon: number; decks: ClockDeck[]; }

export interface GauntletRow {
  slug: string; name: string; score: number | null;
  decap_med: string; table_med: string; pure: number; disruption: number;
  win: number; grind: number; band: number[]; measured: boolean;
}
export interface GauntletData {
  params: { a: number; pod: string; strict: boolean; trials: number; which: string; a_sweep: number[] };
  rows: GauntletRow[];
}

export interface LockCell { piece: string; lift: number; owned: boolean; }
export interface LockRow { slug: string; name: string; cur: number; cells: LockCell[]; }
export interface LocksData {
  params: { a: number; r: number; strict: boolean; trials: number; pod: string; which: string };
  locks: string[]; abbr: Record<string, string>; rows: LockRow[];
}

export interface SeasonRow { seed: number; slug: string; name: string; table_med: string; never: number; dura: number; pwin: number; swap: boolean; }
export interface ChampSeat { slug: string; name: string; seed: number; share: number; advances?: boolean; medal?: string; }
export interface ChampData {
  params: { trials: number; season_trials: number; t_grind: number; swapped: boolean };
  season: SeasonRow[];
  groups: { pod: string; seats: ChampSeat[] }[];
  final: ChampSeat[];
  champion: { slug: string; name: string; seed: number };
  notes: { runner_up: { name: string; seed: number }; upset: boolean; cinderella: { name: string; seed: number } | null; changed: string[] };
}

export interface Manifest {
  generated: string;
  gauntlet: { pod: string[]; strict: number[]; a: number[]; trials: number };
  locks: { pod: string[]; strict: number[]; a: number[]; r: number[]; trials: number };
  championship: { t_grind: number[]; swapped: number[]; trials: number; season_trials: number };
}

async function getJSON<T>(url: string): Promise<T> {
  const r = await fetch(url);
  if (!r.ok) throw new Error("HTTP " + r.status);
  const j = await r.json();
  if (j && j.error) throw new Error(j.error);
  return j as T;
}

const params = new URLSearchParams(location.search);
const FORCE_LIVE = params.has("live");
const FORCE_STATIC = params.has("static");

export const mode = { static: false, manifest: null as Manifest | null };
const _bundles: Record<string, unknown> = {};
const nearest = (v: number, arr: number[]) =>
  arr.reduce((a, b) => (Math.abs(b - v) < Math.abs(a - v) ? b : a));

export async function initMode(): Promise<void> {
  if (FORCE_LIVE) return;
  if (!FORCE_STATIC) {
    try { await getJSON("/api/clocks"); return; } catch { /* no API */ }
  }
  try { mode.manifest = await getJSON<Manifest>("data/manifest.json"); mode.static = true; } catch { mode.static = false; }
}

async function bundle<T>(name: string): Promise<T> {
  if (!_bundles[name]) _bundles[name] = await getJSON(`data/${name}.json`);
  return _bundles[name] as T;
}

export async function getClocks(): Promise<ClocksData> {
  return mode.static ? bundle<ClocksData>("clocks") : getJSON<ClocksData>("/api/clocks");
}

export async function getGauntlet(p: { a: number; pod: string; strict: boolean; trials: number }): Promise<GauntletData> {
  if (!mode.static) {
    return getJSON(`/api/gauntlet?a=${p.a}&pod=${p.pod}&strict=${p.strict ? 1 : 0}&trials=${p.trials}`);
  }
  const m = mode.manifest!.gauntlet;
  const key = `${p.pod}|${p.strict ? 1 : 0}|${nearest(p.a, m.a).toFixed(2)}`;
  const hit = (await bundle<Record<string, GauntletData>>("gauntlet"))[key];
  if (!hit) throw new Error(`no baked scenario (gauntlet ${key})`);
  return hit;
}

export async function getLocks(p: { a: number; r: number; strict: boolean; pod: string; trials: number }): Promise<LocksData> {
  if (!mode.static) {
    return getJSON(`/api/lock_sweep?a=${p.a}&r=${p.r}&strict=${p.strict ? 1 : 0}&pod=${p.pod}&trials=${p.trials}`);
  }
  const m = mode.manifest!.locks;
  const key = `${p.pod}|${p.strict ? 1 : 0}|${nearest(p.a, m.a).toFixed(2)}|${nearest(p.r, m.r).toFixed(2)}`;
  const hit = (await bundle<Record<string, LocksData>>("locks"))[key];
  if (!hit) throw new Error(`no baked scenario (locks ${key})`);
  return hit;
}

export async function getChampionship(p: { trials: number; season_trials: number; t_grind: number; swapped: boolean }): Promise<ChampData> {
  if (!mode.static) {
    return getJSON(`/api/championship?trials=${p.trials}&season_trials=${p.season_trials}&t_grind=${p.t_grind}&swapped=${p.swapped ? 1 : 0}`);
  }
  const m = mode.manifest!.championship;
  const key = `${nearest(p.t_grind, m.t_grind)}|${p.swapped ? 1 : 0}`;
  const hit = (await bundle<Record<string, ChampData>>("championship"))[key];
  if (!hit) throw new Error(`no baked scenario (championship ${key})`);
  return hit;
}

/* -------------------------------------------------------------------------- *
 * Content pages (KB markdown / CSV / Scryfall — single payloads, no scenario
 * grid). Live: /api/<name>; static: data/<name>.json (decks/<slug>.json).
 * -------------------------------------------------------------------------- */

export interface RosterDeck {
  slug: string; name: string; commander: string; colors: string; pips: string[];
  score: number | null; archetype: string; tier: string; status: string;
  decap: string | null; table: string | null; gc: number | null;
}
export interface RosterData { decks: RosterDeck[]; }

export interface HomeData {
  kpis: { label: string; value: string; sub: string }[];
  champion: { name: string; seed: number; note: string };
  clockSeries: { name: string; grid: number[]; decap: number[] }[];
  roster: { name: string; commander: string; score: number | null; slug: string; decap: string | null; table: string | null; tier: string }[];
  pod: { name: string; pct: number }[];
  awards: { label: string; winner: string; note: string }[];
}

export interface WishlistData {
  builds: { name: string; theme: string; clock: string; gc: string; acquire: number | null; cost: string; gate: boolean }[];
  swaps: { deck: string; change: string; out: string; into: string; cost: string; gate: boolean; applied: boolean }[];
  buys: { card: string; qty: string; unlocks: string; note: string }[];
  counts: { free: number; small: number; builds: number; gates: number };
}

export interface CollectionCard {
  name: string; set: string; color: string; cost: string; cmc: number; rarity: string; role: string; qty: number;
}
export interface CollectionData {
  count: number; cards: CollectionCard[];
  facets: { color: Record<string, number>; role: Record<string, number>; rarity: Record<string, number> };
}

export interface DeckPage {
  slug: string; name: string; commander: string; colors: string; pips: string[];
  archetype: string; status: string; bracket: number; score: number | null;
  axes: { label: string; score: number }[]; gc: string[];
  clock: { decap: string | null; table: string | null; grid: number[]; decapCurve: number[]; tableCurve: number[]; never: number[]; src: string };
  gamePlan: string; winLine: string;
  finishers: { name: string; tag: string; note: string }[];
  composition: { name: string; count: number }[];
  decklist: {
    total: number; grouped: boolean;
    commander: { n: string; gc: boolean };
    groups: { name: string; count: number; cards: { n: string; gc: boolean }[] }[];
    text: string;
  } | null;
  keep: { bottleneck: string | null; minLands: number | null; maxLands: number | null; mixed: string | null };
}

export async function getRoster(): Promise<RosterData> {
  return mode.static ? bundle<RosterData>("roster") : getJSON<RosterData>("/api/roster");
}
export async function getHome(): Promise<HomeData> {
  return mode.static ? bundle<HomeData>("home") : getJSON<HomeData>("/api/home");
}
export async function getWishlist(): Promise<WishlistData> {
  return mode.static ? bundle<WishlistData>("wishlist") : getJSON<WishlistData>("/api/wishlist");
}
export async function getCollection(): Promise<CollectionData> {
  return mode.static ? bundle<CollectionData>("collection") : getJSON<CollectionData>("/api/collection");
}
export async function getDeck(slug: string): Promise<DeckPage> {
  return mode.static ? bundle<DeckPage>(`decks/${slug}`) : getJSON<DeckPage>(`/api/deck?slug=${encodeURIComponent(slug)}`);
}
