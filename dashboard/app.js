/* ============================================================================
   Pod Gauntlet dashboard — front-end logic.
   Talks to the stdlib server's JSON API; renders with Plotly. All chart styling
   reads the CSS theme tokens (cssvar) so the look stays editable in style.css.
   Three independent modules: Gauntlet, Clocks, Championship.
   ========================================================================== */
const $ = (sel) => document.querySelector(sel);
const cssvar = (n) => getComputedStyle(document.documentElement).getPropertyValue(n).trim();
const pct = (x) => (x * 100).toFixed(0) + "%";
const kfmt = (n) => (n >= 1000 ? (n / 1000) + "k" : "" + n);

async function getJSON(url) {
  const r = await fetch(url);
  const j = await r.json();
  if (j.error) throw new Error(j.error);
  return j;
}
function debounce(fn, ms) {
  let t; return (...a) => { clearTimeout(t); t = setTimeout(() => fn(...a), ms); };
}
function setBadge(el, text, cls) {
  el.textContent = text;
  el.className = "badge" + (cls ? " " + cls : "");
}

/* loading affordances: a global top progress bar (ref-counted for concurrent
   fetches) + a per-panel dim while its request is in flight. */
let _inflight = 0;
function setLoading(panelId, on) {
  _inflight = Math.max(0, _inflight + (on ? 1 : -1));
  $("#progress").classList.toggle("on", _inflight > 0);
  if (panelId) $(panelId).classList.toggle("loading", on);
}

/* ---- shared Plotly config -------------------------------------------------*/
const PLOT_CONFIG = { responsive: true, displayModeBar: false };
function baseLayout(extra) {
  return Object.assign({
    paper_bgcolor: "rgba(0,0,0,0)",
    plot_bgcolor: "rgba(0,0,0,0)",
    font: { color: cssvar("--text"), family: cssvar("--font"), size: 12 },
    margin: { l: 150, r: 16, t: 8, b: 42 },
    hovermode: "closest",
    legend: { font: { size: 11 }, bgcolor: "rgba(0,0,0,0)" },
    xaxis: { gridcolor: cssvar("--line"), zerolinecolor: cssvar("--line"), linecolor: cssvar("--line") },
    yaxis: { gridcolor: cssvar("--line"), zerolinecolor: cssvar("--line"), linecolor: cssvar("--line") },
  }, extra || {});
}
// a roomy categorical palette for the multi-deck line charts
const PALETTE = ["#5ad1ff","#ffb454","#46d39a","#ff6b6b","#b48cff","#ffd24a","#6fd3c7","#f48fb1",
                 "#9ccc65","#4fc3f7","#ff8a65","#ba68c8","#dce775","#4db6ac","#e57373","#7986cb"];

/* ===========================================================================
   TAB SWITCHING
   ========================================================================= */
const loaded = { gauntlet: false, clocks: false, championship: false };
function showTab(name) {
  document.querySelectorAll(".tab").forEach((b) => b.classList.toggle("is-active", b.dataset.tab === name));
  document.querySelectorAll(".panel").forEach((p) => p.classList.toggle("hidden", p.id !== "panel-" + name));
  onShow(name);
}
function onShow(name) {
  if (name === "gauntlet" && !loaded.gauntlet) { loaded.gauntlet = true; runGauntlet(); }
  if (name === "clocks" && !loaded.clocks) { loaded.clocks = true; initClocks(); }
  // championship is explicit (Run button); just resize if already drawn
  setTimeout(() => document.querySelectorAll("#panel-" + name + " .plot").forEach((el) => {
    if (el.data) Plotly.Plots.resize(el);
  }), 30);
}
$("#tabs").addEventListener("click", (e) => {
  const b = e.target.closest(".tab"); if (b) showTab(b.dataset.tab);
});

/* segmented-control helper: returns the chosen value, wires click -> callback */
function wireSeg(id, onChange) {
  const seg = $(id);
  seg.addEventListener("click", (e) => {
    const b = e.target.closest("button"); if (!b) return;
    seg.querySelectorAll("button").forEach((x) => x.classList.toggle("on", x === b));
    seg.dataset.value = b.dataset.v;
    onChange(b.dataset.v);
  });
  return () => seg.dataset.value;
}

/* ===========================================================================
   GAUNTLET
   ========================================================================= */
const gPod = wireSeg("#podSeg", () => runGauntletDebounced());
const gStrict = wireSeg("#strictSeg", () => runGauntletDebounced());
$("#aSlider").addEventListener("input", (e) => { $("#aOut").textContent = (+e.target.value).toFixed(2); runGauntletDebounced(); });
$("#trialsSlider").addEventListener("input", (e) => { $("#trialsOut").textContent = kfmt(+e.target.value); runGauntletDebounced(); });

async function runGauntlet() {
  const a = $("#aSlider").value;
  const pod = gPod();
  const strict = gStrict() === "table" ? 1 : 0;
  const trials = $("#trialsSlider").value;
  const st = $("#gauntletStatus");
  setBadge(st, "running…", "busy");
  setLoading("#panel-gauntlet", true);
  try {
    const d = await getJSON(`/api/gauntlet?a=${a}&pod=${pod}&strict=${strict}&trials=${trials}`);
    $("#gauntletClk").textContent = d.params.which === "table"
      ? "· TABLE clock (did we close the game?)"
      : "· DECAP clock (neutralise the archenemy)";
    drawGauntletBars(d);
    drawGauntletSweep(d);
    drawGauntletTable(d);
    setBadge(st, `${d.rows.length} decks · ${kfmt(d.params.trials)} trials`, "ok");
  } catch (err) {
    setBadge(st, "error: " + err.message, "err");
  } finally {
    setLoading("#panel-gauntlet", false);
  }
}
const runGauntletDebounced = debounce(runGauntlet, 220);

function drawGauntletBars(d) {
  const rows = d.rows.slice().reverse();         // best deck on top
  const y = rows.map((r) => r.name);
  const win = rows.map((r) => +(r.win * 100).toFixed(1));
  const pure = rows.map((r) => +(r.pure * 100).toFixed(1));
  const traces = [
    { x: win, y, name: "P(WIN)", type: "bar", orientation: "h",
      marker: { color: cssvar("--accent") }, text: win.map((v) => v + "%"),
      textposition: "auto", insidetextfont: { color: "#06121a" } },
    { x: pure, y, name: "PURE RACE", type: "bar", orientation: "h",
      marker: { color: cssvar("--accent-2") }, opacity: 0.9 },
  ];
  Plotly.react("gauntletBars", traces, baseLayout({
    barmode: "group", bargap: 0.25,
    xaxis: { range: [0, 100], ticksuffix: "%", gridcolor: cssvar("--line") },
    legend: { orientation: "h", y: 1.04, x: 0 },
  }), PLOT_CONFIG);
}

function drawGauntletSweep(d) {
  const xs = d.params.a_sweep;
  const traces = d.rows.map((r, i) => ({
    x: xs, y: r.band.map((b) => +(b * 100).toFixed(1)),
    name: r.name, mode: "lines+markers", type: "scatter",
    line: { color: PALETTE[i % PALETTE.length], width: 2 },
    marker: { size: 5 },
  }));
  Plotly.react("gauntletSweep", traces, baseLayout({
    margin: { l: 48, r: 16, t: 8, b: 42 },
    xaxis: { title: "P(Abolisher out)", gridcolor: cssvar("--line") },
    yaxis: { title: "P(win) %", range: [0, 100], gridcolor: cssvar("--line") },
  }), PLOT_CONFIG);
}

function drawGauntletTable(d) {
  const head = ["Deck", "Sc", "decap", "table", "pure", "D@a", "P(WIN)"];
  let html = "<thead><tr>" + head.map((h) => `<th>${h}</th>`).join("") + "</tr></thead><tbody>";
  for (const r of d.rows) {
    const w = (r.win * 100).toFixed(0);
    html += "<tr>"
      + `<td>${r.name}${r.measured ? ' <span class="hint">*</span>' : ""}</td>`
      + `<td class="num">${r.score ?? ""}</td>`
      + `<td class="num">${r.decap_med}</td>`
      + `<td class="num">${r.table_med}</td>`
      + `<td class="num">${(r.pure * 100).toFixed(0)}%</td>`
      + `<td class="num">${(r.disruption * 100).toFixed(0)}%</td>`
      + `<td class="num bar-cell"><span class="fill" style="width:${w}%"></span><span>${w}%</span></td>`
      + "</tr>";
  }
  html += "</tbody>";
  $("#gauntletTable").innerHTML = html;
}

/* ===========================================================================
   CLOCKS / LABS
   ========================================================================= */
let CLOCKS = null;
const clockSel = new Set();
const cWhich = wireSeg("#clockWhich", () => drawClocks());

async function initClocks() {
  try {
    CLOCKS = await getJSON("/api/clocks");
  } catch (err) { return; }
  // default selection: the three race leaders + a slow fortress, for contrast
  const defaults = ["radiation_sickness", "genome_project", "replication_crisis", "grand_design"];
  const chips = $("#clockChips");
  chips.innerHTML = "";
  CLOCKS.decks.forEach((dk, i) => {
    const on = defaults.includes(dk.slug);
    if (on) clockSel.add(dk.slug);
    const c = document.createElement("button");
    c.className = "chip" + (on ? " on" : "");
    c.textContent = dk.name;
    c.style.borderColor = PALETTE[i % PALETTE.length];
    if (on) c.style.background = PALETTE[i % PALETTE.length];
    c.dataset.slug = dk.slug; c.dataset.i = i;
    c.addEventListener("click", () => {
      if (clockSel.has(dk.slug)) { clockSel.delete(dk.slug); c.classList.remove("on"); c.style.background = ""; }
      else { clockSel.add(dk.slug); c.classList.add("on"); c.style.background = PALETTE[i % PALETTE.length]; }
      drawClocks();
    });
    chips.appendChild(c);
  });
  drawClocks();
}

function drawClocks() {
  if (!CLOCKS) return;
  const which = cWhich();
  const traces = [];
  CLOCKS.decks.forEach((dk, i) => {
    if (!clockSel.has(dk.slug)) return;
    traces.push({
      x: dk.grid, y: dk[which], name: dk.name,
      mode: "lines+markers", type: "scatter",
      line: { color: PALETTE[i % PALETTE.length], width: 2.5, shape: "spline" },
      marker: { size: 6 },
      hovertemplate: `${dk.name}<br>T%{x}: %{y}%<extra></extra>`,
    });
  });
  Plotly.react("clockPlot", traces, baseLayout({
    margin: { l: 52, r: 16, t: 8, b: 44 },
    xaxis: { title: "turn", dtick: 1, gridcolor: cssvar("--line") },
    yaxis: { title: `cum P(${which} ≤ turn) %`, range: [0, 100], gridcolor: cssvar("--line") },
    shapes: [{ type: "line", x0: 0, x1: 16, y0: 50, y1: 50, line: { color: cssvar("--faint"), width: 1, dash: "dot" } }],
  }), PLOT_CONFIG);
}

/* ===========================================================================
   CHAMPIONSHIP
   ========================================================================= */
$("#champTrials").addEventListener("input", (e) => $("#champTrialsOut").textContent = kfmt(+e.target.value));
$("#seasonTrials").addEventListener("input", (e) => $("#seasonTrialsOut").textContent = kfmt(+e.target.value));
$("#tGrind").addEventListener("input", (e) => $("#tGrindOut").textContent = e.target.value);
const champSwap = wireSeg("#swapSeg", () => {});
$("#runChamp").addEventListener("click", runChampionship);

async function runChampionship() {
  const st = $("#champStatus");
  setBadge(st, "simulating…", "busy");
  setLoading("#panel-championship", true);
  const q = new URLSearchParams({
    trials: $("#champTrials").value,
    season_trials: $("#seasonTrials").value,
    t_grind: $("#tGrind").value,
    swapped: champSwap() === "1" ? 1 : 0,
  });
  try {
    const d = await getJSON("/api/championship?" + q.toString());
    $("#champEmpty").classList.add("hidden");
    $("#seasonCard").classList.remove("hidden");
    drawChampion(d);
    drawBracket(d);
    drawSeason(d);
    setBadge(st, "done", "ok");
  } catch (err) {
    setBadge(st, "error: " + err.message, "err");
  } finally {
    setLoading("#panel-championship", false);
  }
}

function drawChampion(d) {
  const b = $("#champBanner");
  const c = d.champion;
  let note = `Runner-up: ${d.notes.runner_up.name} (#${d.notes.runner_up.seed}).`;
  if (d.notes.upset) note += `  ⚡ UPSET — the #${c.seed} seed took the crown.`;
  if (d.notes.cinderella) note += `  ✨ Cinderella: ${d.notes.cinderella.name} (#${d.notes.cinderella.seed}).`;
  if (d.params.swapped && d.notes.changed.length) note += `  Swaps applied: ${d.notes.changed.join(", ")}.`;
  b.innerHTML = `<div class="trophy">🏆</div><div><h2>${c.name}</h2>`
    + `<p>Champion · seed #${c.seed}</p><p>${note}</p></div>`;
  b.classList.remove("hidden");
}

function seatRow(s, maxShare, extraClass) {
  const w = maxShare > 0 ? (s.share / maxShare) * 100 : 0;
  const medal = { gold: "🥇", silver: "🥈", bronze: "🥉" }[extraClass] || "";
  return `<div class="seat ${extraClass || ""} ${s.advances ? "adv" : ""}">`
    + `<span class="seatfill" style="width:${w}%"></span>`
    + (medal ? `<span class="medal">${medal}</span>` : "")
    + `<span class="nm">${s.name}</span><span class="sd">#${s.seed}</span>`
    + `<span class="pct">${(s.share * 100).toFixed(1)}%</span></div>`;
}

function drawBracket(d) {
  const wrap = $("#bracket");
  let html = "";
  for (const g of d.groups) {
    const maxShare = Math.max(...g.seats.map((s) => s.share));
    html += `<div class="pod"><h3><span>Pod ${g.pod}</span><span class="hint">win share</span></h3>`
      + g.seats.map((s) => seatRow(s, maxShare)).join("") + "</div>";
  }
  const fmax = Math.max(...d.final.map((s) => s.share));
  html += `<div class="pod final"><h3><span>The Final Four</span><span class="hint">group winners</span></h3>`
    + d.final.map((s) => seatRow(s, fmax, s.medal)).join("") + "</div>";
  wrap.innerHTML = html;
}

function drawSeason(d) {
  const head = ["Seed", "Deck", "table", "never", "dura", "P(win)"];
  let html = "<thead><tr>" + head.map((h) => `<th>${h}</th>`).join("") + "</tr></thead><tbody>";
  const maxp = Math.max(...d.season.map((s) => s.pwin));
  for (const s of d.season) {
    html += "<tr>"
      + `<td class="num">#${s.seed}</td>`
      + `<td>${s.name}${s.swap ? ' <span class="hint">←swap</span>' : ""}</td>`
      + `<td class="num">${s.table_med}</td>`
      + `<td class="num">${s.never}%</td>`
      + `<td class="num">${s.dura.toFixed(2)}</td>`
      + `<td class="num bar-cell"><span class="fill" style="width:${(s.pwin / maxp) * 100}%"></span><span>${s.pwin.toFixed(0)}%</span></td>`
      + "</tr>";
  }
  html += "</tbody>";
  $("#seasonTable").innerHTML = html;
}

/* ===========================================================================
   LOCKS — deck × lock lift heatmap (heavy compute; explicit Run)
   ========================================================================= */
$("#lockA").addEventListener("input", (e) => $("#lockAOut").textContent = (+e.target.value).toFixed(2));
$("#lockR").addEventListener("input", (e) => $("#lockROut").textContent = (+e.target.value).toFixed(2));
$("#lockTrials").addEventListener("input", (e) => $("#lockTrialsOut").textContent = kfmt(+e.target.value));
const lockStrict = wireSeg("#lockStrict", () => {});
const lockPod = wireSeg("#lockPod", () => {});
$("#runLocks").addEventListener("click", runLocks);

async function runLocks() {
  const st = $("#lockStatus");
  setBadge(st, "measuring…", "busy");
  setLoading("#panel-locks", true);
  const q = new URLSearchParams({
    a: $("#lockA").value, r: $("#lockR").value,
    strict: lockStrict() === "table" ? 1 : 0,
    pod: lockPod(), trials: $("#lockTrials").value,
  });
  try {
    const d = await getJSON("/api/lock_sweep?" + q.toString());
    $("#lockEmpty").classList.add("hidden");
    $("#lockCard").classList.remove("hidden");
    drawHeatmap(d);
    setBadge(st, `${d.rows.length} decks · ${kfmt(d.params.trials)} trials · ${d.params.which}`, "ok");
  } catch (err) {
    setBadge(st, "error: " + err.message, "err");
  } finally {
    setLoading("#panel-locks", false);
  }
}

function drawHeatmap(d) {
  const rows = d.rows.slice().reverse();             // highest baseline P(win) at top
  const y = rows.map((r) => `${r.name}  ·  ${(r.cur * 100).toFixed(0)}%`);
  const x = d.locks.map((l) => d.abbr[l] || l);
  const z = rows.map((r) => r.cells.map((c) => +c.lift.toFixed(1)));
  const text = rows.map((r) => r.cells.map((c) => {
    const v = c.lift;
    const s = v >= 0.5 ? "+" + v.toFixed(0) : (v > -0.5 ? "·" : v.toFixed(0));
    return s + (c.owned ? "*" : "");
  }));
  const maxabs = Math.max(3, ...z.flat().map((v) => Math.abs(v)));
  const trace = {
    z, x, y, text, texttemplate: "%{text}", textfont: { size: 11, color: cssvar("--text") },
    type: "heatmap", xgap: 3, ygap: 3, zmid: 0, zmin: -maxabs, zmax: maxabs,
    colorscale: [[0, "#ff6b6b"], [0.5, "#141a23"], [1, "#43dca0"]],
    hovertemplate: "%{y}<br>%{x}: %{z} pts<extra></extra>",
    colorbar: { title: { text: "pts", side: "right" }, thickness: 12, outlinewidth: 0,
                tickfont: { color: cssvar("--muted"), size: 10 } },
  };
  Plotly.react("lockHeatmap", [trace], baseLayout({
    margin: { l: 205, r: 28, t: 10, b: 38 },
    xaxis: { side: "top", gridcolor: "rgba(0,0,0,0)", linecolor: "rgba(0,0,0,0)" },
    yaxis: { gridcolor: "rgba(0,0,0,0)", linecolor: "rgba(0,0,0,0)", automargin: true },
  }), PLOT_CONFIG);
}

/* ---- boot ----------------------------------------------------------------*/
showTab("gauntlet");
