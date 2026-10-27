// Biblioteca común del generador de preguntas de matemáticas (juega-y-aprende).
// PRNG determinista, fracciones exactas, polinomios, formateo y banco de filas.

export function mulberry32(a) {
  return function () {
    a |= 0; a = (a + 0x6D2B79F5) | 0;
    let t = Math.imul(a ^ (a >>> 15), 1 | a);
    t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
}
export class RNG {
  constructor(seed) { this.f = mulberry32(seed); }
  next() { return this.f(); }
  int(a, b) { return a + Math.floor(this.f() * (b - a + 1)); }
  nz(a, b) { let v = 0; while (v === 0) v = this.int(a, b); return v; }
  /** entero distinto de cero con signo aleatorio y módulo en [a,b] */
  sgn(a, b) { const v = this.int(a, b); return this.f() < 0.5 ? -v : v; }
  pick(arr) { return arr[Math.floor(this.f() * arr.length)]; }
  chance(p) { return this.f() < p; }
  shuffle(arr) { const a = arr.slice(); for (let i = a.length - 1; i > 0; i--) { const j = Math.floor(this.f() * (i + 1)); [a[i], a[j]] = [a[j], a[i]]; } return a; }
}

export const gcd = (a, b) => { a = Math.abs(a); b = Math.abs(b); while (b) [a, b] = [b, a % b]; return a; };
export const lcm = (a, b) => Math.abs(a * b) / gcd(a, b);

const SUP = { '0': '⁰', '1': '¹', '2': '²', '3': '³', '4': '⁴', '5': '⁵', '6': '⁶', '7': '⁷', '8': '⁸', '9': '⁹', '-': '⁻' };
const SUB = { '0': '₀', '1': '₁', '2': '₂', '3': '₃', '4': '₄', '5': '₅', '6': '₆', '7': '₇', '8': '₈', '9': '₉' };
export const sup = n => String(n).replace(/[0-9-]/g, c => SUP[c]);
export const sub = n => String(n).replace(/[0-9]/g, c => SUB[c]);
const UNSUP = Object.fromEntries(Object.entries(SUP).map(([k, v]) => [v, k]));

export class Fr {
  constructor(n, d = 1) {
    if (d === 0) throw new Error('denominador 0');
    if (d < 0) { n = -n; d = -d; }
    const g = gcd(n, d) || 1;
    this.n = n / g; this.d = d / g;
    if (!Number.isSafeInteger(this.n) || !Number.isSafeInteger(this.d)) throw new Error('overflow');
  }
  add(o) { o = F(o); return new Fr(this.n * o.d + o.n * this.d, this.d * o.d); }
  sub(o) { o = F(o); return new Fr(this.n * o.d - o.n * this.d, this.d * o.d); }
  mul(o) { o = F(o); return new Fr(this.n * o.n, this.d * o.d); }
  div(o) { o = F(o); return new Fr(this.n * o.d, this.d * o.n); }
  neg() { return new Fr(-this.n, this.d); }
  pow(k) { let r = F(1); for (let i = 0; i < k; i++) r = r.mul(this); return r; }
  isInt() { return this.d === 1; }
  isZero() { return this.n === 0; }
  eq(o) { o = F(o); return this.n === o.n && this.d === o.d; }
  val() { return this.n / this.d; }
  sign() { return Math.sign(this.n); }
  abs() { return new Fr(Math.abs(this.n), this.d); }
  toString() { return (this.n < 0 ? '−' : '') + Math.abs(this.n) + (this.d !== 1 ? '/' + this.d : ''); }
}
export const F = (n, d = 1) => (n instanceof Fr ? n : new Fr(n, d));
export const fs = x => F(x).toString();
/** entero con signo tipográfico */
export const I = n => (n < 0 ? '−' : '') + Math.abs(n);
/** " + 5" / " − 5" para términos intermedios */
export const sgn = n => (n < 0 ? ' − ' : ' + ') + Math.abs(n);
/** decimal con coma opcional */
export function dec(v, maxd = 4) {
  let s = String(Math.round(v * 10 ** maxd) / 10 ** maxd);
  if (s === '-0') s = '0';
  return s;
}
export const decS = v => dec(v).replace('-', '−');

// ---------- Polinomios ----------
export class Poly {
  constructor(c) { this.c = c.map(F); while (this.c.length > 1 && this.c[this.c.length - 1].isZero()) this.c.pop(); }
  get deg() { return this.c.length - 1; }
  add(o) { const n = Math.max(this.c.length, o.c.length); const r = []; for (let i = 0; i < n; i++) r.push((this.c[i] || F(0)).add(o.c[i] || F(0))); return new Poly(r); }
  sub(o) { return this.add(o.scale(-1)); }
  scale(k) { return new Poly(this.c.map(x => x.mul(k))); }
  mul(o) { const r = new Array(this.c.length + o.c.length - 1).fill(0).map(() => F(0)); this.c.forEach((a, i) => o.c.forEach((b, j) => { r[i + j] = r[i + j].add(a.mul(b)); })); return new Poly(r); }
  pow(k) { let r = new Poly([1]); for (let i = 0; i < k; i++) r = r.mul(this); return r; }
  d() { return new Poly(this.c.slice(1).map((x, i) => x.mul(i + 1))); }
  integ() { return new Poly([0, ...this.c.map((x, i) => x.div(i + 1))]); }
  ev(x) { x = F(x); let r = F(0); for (let i = this.c.length - 1; i >= 0; i--) r = r.mul(x).add(this.c[i]); return r; }
  str(v = 'x') { return polyStr(this.c, v); }
}
export function varPow(v, k) { return k === 0 ? '' : k === 1 ? v : v + sup(k); }
export function polyStr(coefs, v = 'x') {
  const c = coefs.map(F);
  let out = '';
  for (let k = c.length - 1; k >= 0; k--) {
    const a = c[k]; if (a.isZero()) continue;
    const neg = a.n < 0; const ab = a.abs();
    let t;
    const vp = varPow(v, k);
    if (k === 0) t = ab.toString();
    else if (ab.d === 1) t = (ab.n === 1 ? '' : String(ab.n)) + vp;
    else t = (ab.n === 1 ? '' : String(ab.n)) + vp + '/' + ab.d;
    if (!out) out = (neg ? '−' : '') + t; else out += (neg ? ' − ' : ' + ') + t;
  }
  return out || '0';
}
/** término a·x^k suelto (a entero) */
export function mono(a, v = 'x', k = 1) { return polyStr([...new Array(k).fill(0), a], v); }

// ---------- Normalización y aceptadas ----------
export const norm = s => String(s).toLowerCase().normalize('NFD').replace(/[̀-ͯ]/g, '').replace(/\s+/g, ' ').replace(/[.¿?¡!]+$/g, '').trim();

export function ascii(s) {
  return s.replace(/−/g, '-').replace(/[⁰¹²³⁴⁵⁶⁷⁸⁹⁻]+/g, m => '^' + [...m].map(c => UNSUP[c]).join(''))
    .replace(/·/g, '*').replace(/×/g, '*').replace(/÷/g, '/').replace(/π/g, 'pi').replace(/≥/g, '>=').replace(/≤/g, '<=')
    .replace(/√\(/g, 'sqrt(').replace(/√(\w+)/g, 'sqrt($1)').replace(/∞/g, 'inf');
}
export function variants(s) {
  const out = new Set();
  const add = x => { if (x && x.trim()) { out.add(x.trim()); out.add(x.replace(/\s+/g, '')); } };
  add(s);
  const a = ascii(s); add(a);
  if (/\d\.\d/.test(a)) { add(a.replace(/(\d)\.(\d)/g, '$1,$2')); }
  if (/\d,\d/.test(s) === false && /\d\.\d/.test(s)) add(s.replace(/(\d)\.(\d)/g, '$1,$2'));
  return [...out];
}
/** expande y deduplica una lista de aceptadas */
export function A(...list) {
  const out = new Map();
  for (const s of list.flat()) { if (s == null) continue; for (const v of variants(String(s))) { const k = norm(v); if (k && !out.has(k)) out.set(k, v); } }
  return [...out.values()];
}
/** aceptadas para "x = valor" (solo valor, y con prefijo) */
export function eqAcc(v, val) { const s = typeof val === 'string' ? val : fs(val); return A(s, `${v}=${s}`, `${v} = ${s}`); }
/** aceptadas numéricas con posible decimal */
export function numAcc(x) {
  const f = F(x); const l = [fs(f)];
  const v = f.val();
  if (!f.isInt() && Math.abs(v * 1e4 - Math.round(v * 1e4)) < 1e-9) l.push(decS(v));
  return A(l);
}

// ---------- Banco ----------
export class Bank {
  constructor() { this.cats = {}; this.seen = new Set(); this.tcount = {}; this.skipped = {}; this.specs = []; }
  add(cat, tpl, q, ans, wrongs, acc, expl, d, spec) {
    q = String(q); ans = String(ans);
    const nk = norm(q);
    if (this.seen.has(nk)) { this.skipped[tpl] = (this.skipped[tpl] || 0) + 1; return false; }
    // distractores únicos
    const used = new Set([norm(ans)]); const w = [];
    for (const x of wrongs) {
      if (x == null) continue; const s = String(x).replace(/\s+/g, ' ').trim();
      if (!s || s.length > 90) continue;
      const k = norm(s); if (used.has(k)) continue; used.add(k); w.push(s); if (w.length === 3) break;
    }
    if (w.length < 3) { this.skipped[tpl] = (this.skipped[tpl] || 0) + 1; return false; }
    if (q.length > 400) throw new Error(`pregunta larga (${tpl}): ${q}`);
    if (ans.length > 90) throw new Error(`respuesta larga (${tpl}): ${ans}`);
    if (expl.length < 12 || expl.length > 500) throw new Error(`explicación fuera de rango (${tpl}): ${expl}`);
    const wn = new Set(w.map(norm));
    const accl = (acc || []).filter(s => !wn.has(norm(s)));
    d = Math.max(0, Math.min(1, Math.round(d * 1000) / 1000));
    this.seen.add(nk);
    (this.cats[cat] ||= []).push([q, ans, w, accl, expl, d]);
    this.tcount[cat + ':' + tpl] = (this.tcount[cat + ':' + tpl] || 0) + 1;
    if (spec) this.specs.push({ q, ...spec });
    return true;
  }
  /** genera hasta n filas con fn(t, rng) donde t∈[0,1) crece con el avance */
  gen(cat, tpl, n, r, fn, lo, hi) {
    let made = 0, tries = 0;
    const self = this;
    while (made < n && tries < n * 12) {
      tries++;
      const t = made / n;
      const ctx = {
        t, r, d: (dd = 0) => lo + (hi - lo) * Math.min(1, Math.max(0, t + dd)),
        add(q, ans, wrongs, acc, expl, dd = 0, spec) { return self.add(cat, tpl, q, ans, wrongs, acc, expl, lo + (hi - lo) * Math.min(1, Math.max(0, t + dd)), spec); },
      };
      if (fn(ctx)) made++;
    }
    if (made < n) console.warn(`  [aviso] ${cat}:${tpl} solo ${made}/${n}`);
    return made;
  }
  /** pregunta escrita a mano */
  hand(cat, q, ans, wrongs, acc, expl, d, spec) { return this.add(cat, 'manual', q, ans, wrongs, acc, expl, d, spec); }
  finish() {
    const out = {};
    for (const [c, rows] of Object.entries(this.cats)) {
      out[c] = rows.map((r, i) => ({ r, i })).sort((a, b) => a.r[5] - b.r[5] || a.i - b.i).map(x => x.r);
    }
    return out;
  }
}

export const uniq = arr => { const s = new Set(); return arr.filter(x => { const k = norm(x); if (s.has(k)) return false; s.add(k); return true; }); };
