// Uso: node validar.mjs <area> <archivo.json>
// El JSON es { cat: [ [pregunta, correcta, [3 incorrectas], [aceptadas], explicacion, dificultad], ... ] }
import fs from "node:fs";
const MIN = { mat: { alg: 520, calc: 520, lin: 520, est: 520 },
  prog: { cpp: 260, py: 260, html: 260, js: 260, pseudo: 260, func: 260, bucles: 260, arr: 260 },
  ing: { ing1: 335, ing2: 335, ing3: 335, ing4: 335, ing5: 335, ing6: 335 } };
const [area, file] = process.argv.slice(2);
const norm = (s) => String(s).toLowerCase().normalize("NFD").replace(/[̀-ͯ]/g, "").replace(/\s+/g, " ").replace(/[.¿?¡!]+$/g, "").trim();
const data = JSON.parse(fs.readFileSync(file, "utf8"));
const errs = []; let total = 0; const seen = new Map();
for (const [cat, min] of Object.entries(MIN[area])) {
  const rows = data[cat];
  if (!Array.isArray(rows)) { errs.push(`${cat}: falta la categoría`); continue; }
  if (rows.length < min) errs.push(`${cat}: ${rows.length} preguntas (mínimo ${min})`);
  total += rows.length;
  let prevD = -Infinity, withAcc = 0; const pref = new Map();
  rows.forEach((r, i) => {
    const w = `${cat}#${i}`;
    if (!Array.isArray(r) || r.length < 6) return errs.push(`${w}: formato`);
    const [q, a, x, acc, e, d] = r;
    if (typeof q !== "string" || q.length < 8 || q.length > 600) errs.push(`${w}: pregunta con largo inválido`);
    if (typeof a !== "string" || !a.length || a.length > 90) errs.push(`${w}: correcta inválida`);
    if (!Array.isArray(x) || x.length !== 3) errs.push(`${w}: deben ser 3 incorrectas`);
    else {
      const set = new Set([norm(a), ...x.map(norm)]);
      if (set.size !== 4) errs.push(`${w}: opciones repetidas (${a} | ${x.join(" | ")})`);
      x.forEach((t) => { if (typeof t !== "string" || !t.length || t.length > 90) errs.push(`${w}: incorrecta inválida`); });
    }
    if (!Array.isArray(acc)) errs.push(`${w}: aceptadas debe ser arreglo`);
    else if (acc.length) { withAcc++; if (!acc.map(norm).includes(norm(a))) errs.push(`${w}: aceptadas no incluye la correcta`); }
    if (typeof e !== "string" || e.length < 12 || e.length > 500) errs.push(`${w}: explicación inválida`);
    if (typeof d !== "number" || !Number.isFinite(d)) errs.push(`${w}: dificultad inválida`);
    else { if (d < prevD) errs.push(`${w}: dificultad ${d} menor que la anterior ${prevD} (debe ir de fácil a difícil)`); prevD = d; }
    const k = norm(q); if (seen.has(k)) errs.push(`${w}: pregunta repetida (también en ${seen.get(k)})`); else seen.set(k, w);
    const p = norm(q).replace(/\d+/g, "#").split(" ").slice(0, 4).join(" "); pref.set(p, (pref.get(p) || 0) + 1);
    if (/resuelve el ejercicio \d+/i.test(q)) errs.push(`${w}: texto con número de ejercicio`);
  });
  const top = [...pref.entries()].sort((a, b) => b[1] - a[1])[0];
  const share = top ? top[1] / rows.length : 0;
  if (share > 0.30) errs.push(`${cat}: demasiado repetitivo, el comienzo «${top[0]}» está en ${(share * 100).toFixed(0)}%`);
  console.log(`${cat}: ${rows.length} preguntas · con respuestas escritas ${(100 * withAcc / rows.length).toFixed(0)}% · comienzo más común ${(share * 100).toFixed(0)}% «${top ? top[0] : ""}»`);
  if (withAcc / rows.length < 0.5) errs.push(`${cat}: menos del 50% tiene respuestas aceptadas para el modo Escribir`);
}
console.log(`TOTAL ${area}: ${total}`);
if (errs.length) { console.log(`${errs.length} PROBLEMAS`); console.log(errs.slice(0, 60).join("\n")); process.exit(1); }
console.log("OK");
