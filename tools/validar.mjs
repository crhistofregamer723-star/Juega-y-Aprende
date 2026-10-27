// Uso: node tools/validar.mjs mat|prog|ing   (valida tools/out/<area>.json)
// Formato: { "<cat>": [ [pregunta, correcta, [x1,x2,x3], [aceptadas...], explicación, dificultad0a1], ... ] }
import fs from 'fs';
const MIN = { mat: { alg: 520, calc: 520, lin: 520, est: 520 },
  prog: { cpp: 265, py: 265, html: 265, js: 265, pseudo: 265, func: 265, bucles: 265, arr: 265 },
  ing: { ing1: 350, ing2: 350, ing3: 350, ing4: 350, ing5: 350, ing6: 350 } };
const area = process.argv[2];
if (!MIN[area]) { console.error('Área inválida'); process.exit(2); }
const norm = s => String(s).toLowerCase().normalize('NFD').replace(/[̀-ͯ]/g, '').replace(/\s+/g, ' ').replace(/[.¿?¡!]+$/g, '').trim();
const data = JSON.parse(fs.readFileSync(new URL(`./out/${area}.json`, import.meta.url), 'utf8'));
let errs = [], total = 0; const seenQ = new Map();
for (const [cat, min] of Object.entries(MIN[area])) {
  const rows = data[cat];
  if (!Array.isArray(rows)) { errs.push(`Falta la categoría ${cat}`); continue; }
  if (rows.length < min) errs.push(`${cat}: ${rows.length} preguntas, se piden ≥ ${min}`);
  total += rows.length;
  let conW = 0; const dec = new Array(10).fill(0);
  rows.forEach((r, i) => {
    const w = `${cat}#${i}`;
    if (!Array.isArray(r) || r.length !== 6) return errs.push(`${w}: debe tener 6 elementos`);
    const [q, a, x, acc, e, d] = r;
    if (typeof q !== 'string' || !q.trim() || q.length > 400) errs.push(`${w}: pregunta vacía o > 400 caracteres`);
    if (typeof a !== 'string' || !a.trim() || a.length > 90) errs.push(`${w}: correcta vacía o > 90 caracteres`);
    if (!Array.isArray(x) || x.length !== 3 || x.some(t => typeof t !== 'string' || !t.trim() || t.length > 90)) errs.push(`${w}: necesita 3 incorrectas (texto ≤ 90)`);
    else {
      const set = new Set([a, ...x].map(norm));
      if (set.size !== 4) errs.push(`${w}: opciones repetidas → ${JSON.stringify([a, ...x])}`);
    }
    if (!Array.isArray(acc) || acc.some(t => typeof t !== 'string' || !t.trim())) errs.push(`${w}: aceptadas inválidas`);
    else if (acc.length) { conW++; if (!acc.map(norm).includes(norm(a)) && !acc.length === 0) {} }
    if (typeof e !== 'string' || e.trim().length < 12 || e.length > 500) errs.push(`${w}: explicación ausente o fuera de 12–500 caracteres`);
    if (typeof d !== 'number' || !(d >= 0 && d <= 1)) errs.push(`${w}: dificultad debe estar en 0..1`);
    else dec[Math.min(9, Math.floor(d * 10))]++;
    const k = norm(q) + '||' + norm(a);
    const kq = norm(q);
    if (seenQ.has(kq)) errs.push(`${w}: pregunta repetida (también en ${seenQ.get(kq)})`); else seenQ.set(kq, w);
  });
  if (conW < rows.length * 0.5) errs.push(`${cat}: solo ${conW}/${rows.length} tienen respuestas aceptadas para el modo «Escribir» (se pide ≥ 50 %)`);
  const vac = dec.filter(n => n === 0).length;
  if (vac > 2) errs.push(`${cat}: la dificultad no cubre 0..1 (deciles vacíos: ${vac}) → ${dec.join(',')}`);
  console.log(`${cat.padEnd(7)} ${String(rows.length).padStart(4)} preguntas · con «Escribir» ${conW} · deciles de dificultad ${dec.join(',')}`);
}
console.log(`TOTAL ${area}: ${total}`);
if (errs.length) { console.log(`\n${errs.length} PROBLEMAS (primeros 40):\n` + errs.slice(0, 40).join('\n')); process.exit(1); }
console.log('VALIDACIÓN OK');
