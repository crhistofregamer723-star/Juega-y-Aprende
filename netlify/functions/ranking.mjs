// Ranking global de "Juega y Aprende" como Netlify Function.
// Misma API que el servidor Java:
//   GET  /api/ranking?area=mat&modo=clasico  -> los 50 mejores de esa materia y modo
//   POST /api/ranking  {"jugador":"Ana","area":"mat","modo":"clasico","puntaje":760}
// Ranking por ÁREA (suma de todos los puntos de las categorías) y por NIVEL:
//   GET  /api/ranking?area=mat&orden=puntos|nivel   -> top 50 [{jugador,puntos,nivel,preguntas}]
//   GET  /api/ranking?jugador=Ana                   -> {jugador, areas:{mat:{puntos,nivel,preguntas},prog:{..},ing:{..}}}
//   POST /api/ranking {"jugador":"Ana","area":"mat","puntos":5200,"nivel":12,"preguntas":130}
// (También sigue aceptando el formato anterior por modo: area+modo+puntaje.)
// Los datos se guardan en Netlify Blobs (no hace falta base de datos ni claves).
import { getStore } from "@netlify/blobs";

const AREAS = new Set(["mat", "prog", "ing"]);
const MODOS = new Set(["clasico", "vf", "reloj", "vidas", "relampago", "escribir", "parejas"]);
const MAX_GUARDADOS = 100;
const MAX_DEVUELTOS = 50;
const MAX_PUNTAJE = 1_000_000;
const MAX_CUERPO = 4096;
const MAX_JUGADORES = 5000;
const MAX_PUNTOS = 100_000_000;
const MAX_NIVEL = 1000;
const MAX_POST_POR_MINUTO = 60;

export const config = { path: "/api/ranking" };

const CORS = {
  "Access-Control-Allow-Origin": "*",
  "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
  "Access-Control-Allow-Headers": "Content-Type",
  "Access-Control-Max-Age": "86400",
};

function json(data, status = 200) {
  return new Response(JSON.stringify(data), {
    status,
    headers: { "Content-Type": "application/json; charset=utf-8", "Cache-Control": "no-store", ...CORS },
  });
}
const error = (status, mensaje) => json({ error: mensaje }, status);

// Límite sencillo por IP (vale mientras la función siga "caliente"; frena abusos básicos).
const golpes = new Map();
function permitido(ip) {
  const ahora = Date.now();
  const lista = (golpes.get(ip) || []).filter((t) => ahora - t < 60_000);
  if (lista.length >= MAX_POST_POR_MINUTO) { golpes.set(ip, lista); return false; }
  lista.push(ahora);
  golpes.set(ip, lista);
  if (golpes.size > 5000) {
    for (const [k, v] of golpes) if (!v.length || ahora - v[v.length - 1] > 60_000) golpes.delete(k);
  }
  return true;
}

const ordenar = (a, b) => (b.puntaje - a.puntaje) || (a.creado - b.creado);

async function leer(store) {
  const datos = await store.get("ranking", { type: "json" });
  const filas = datos && Array.isArray(datos.ranking) ? datos.ranking : [];
  return filas.filter(
    (f) => f && typeof f.jugador === "string" && f.jugador && AREAS.has(f.area) && MODOS.has(f.modo) && Number.isFinite(f.puntaje)
  );
}

async function leerPerfiles(store) {
  const d = await store.get("perfiles", { type: "json" });
  return d && d.jugadores && typeof d.jugadores === "object" ? d.jugadores : {};
}
const entero = (v, max) => {
  v = typeof v === "string" ? Number(v.trim()) : v;
  return Number.isInteger(v) && v >= 0 && v <= max ? v : null;
};

export default async (req, context) => {
  try {
    if (req.method === "OPTIONS") return new Response(null, { status: 204, headers: CORS });

    const store = getStore({ name: "ranking", consistency: "strong" });

    if (req.method === "GET") {
      const q = new URL(req.url).searchParams;
      const jug = q.get("jugador"), orden = q.get("orden");
      if (jug !== null || orden !== null) {
        const perfiles = await leerPerfiles(store);
        if (jug !== null) {
          const p = perfiles[jug.trim().toLowerCase()];
          const areas = {};
          for (const a of AREAS) areas[a] = { puntos: p?.[a]?.puntos || 0, nivel: p?.[a]?.nivel || 1, preguntas: p?.[a]?.preguntas || 0 };
          return json({ jugador: p?.jugador || jug.trim(), areas });
        }
        const a = q.get("area");
        if (!AREAS.has(a)) return error(400, "Materia inválida");
        if (orden !== "puntos" && orden !== "nivel") return error(400, "Orden inválido");
        const filas = Object.values(perfiles)
          .filter((p) => p[a] && p[a].puntos > 0)
          .map((p) => ({ jugador: p.jugador, puntos: p[a].puntos, nivel: p[a].nivel || 1, preguntas: p[a].preguntas || 0 }))
          .sort((x, y) => orden === "nivel"
            ? (y.nivel - x.nivel) || (y.preguntas - x.preguntas) || (y.puntos - x.puntos)
            : (y.puntos - x.puntos) || (y.nivel - x.nivel))
          .slice(0, MAX_DEVUELTOS);
        return json(filas);
      }
      const area = q.get("area"), modo = q.get("modo");
      if (area !== null && !AREAS.has(area)) return error(400, "Materia inválida");
      if (modo !== null && !MODOS.has(modo)) return error(400, "Modo inválido");
      const filas = await leer(store);
      const out = filas
        .filter((f) => (area === null || f.area === area) && (modo === null || f.modo === modo))
        .sort(ordenar)
        .slice(0, MAX_DEVUELTOS)
        .map((f) => ({ jugador: f.jugador, puntaje: f.puntaje, area: f.area, modo: f.modo }));
      return json(out);
    }

    if (req.method === "POST") {
      const ip = context?.ip || req.headers.get("x-nf-client-connection-ip") || "desconocida";
      if (!permitido(ip)) return error(429, "Demasiados envíos, espera un momento");

      const texto = await req.text();
      if (new TextEncoder().encode(texto).length > MAX_CUERPO) return error(413, "Cuerpo demasiado grande");
      let d;
      try { d = JSON.parse(texto); } catch { return error(400, "JSON inválido"); }
      if (!d || typeof d !== "object" || Array.isArray(d)) return error(400, "JSON inválido");

      if (d.puntos !== undefined) {
        let nombre = typeof d.jugador === "string" ? d.jugador.trim() : "";
        if (!nombre || [...nombre].length > 24 || /[\u0000-\u001f\u007f-\u009f]/.test(nombre)) return error(400, "Nombre inválido");
        if (!AREAS.has(d.area)) return error(400, "Materia inválida");
        const puntos = entero(d.puntos, MAX_PUNTOS), nivel = entero(d.nivel, MAX_NIVEL), preguntas = entero(d.preguntas, 1_000_000);
        if (puntos === null || nivel === null || preguntas === null || nivel < 1) return error(400, "Datos inválidos");
        const perfiles = await leerPerfiles(store);
        const k = nombre.toLowerCase();
        const p = perfiles[k] || (perfiles[k] = { jugador: nombre });
        p.jugador = nombre;
        const a = p[d.area] || (p[d.area] = { puntos: 0, nivel: 1, preguntas: 0 });
        // Los totales solo suben (un envío repetido o atrasado no los baja).
        a.puntos = Math.max(a.puntos, puntos);
        a.nivel = Math.max(a.nivel, nivel);
        a.preguntas = Math.max(a.preguntas, preguntas);
        p.t = Date.now();
        const claves = Object.keys(perfiles);
        if (claves.length > MAX_JUGADORES) {
          claves.sort((x, y) => (perfiles[x].t || 0) - (perfiles[y].t || 0));
          for (const x of claves.slice(0, claves.length - MAX_JUGADORES)) delete perfiles[x];
        }
        await store.setJSON("perfiles", { jugadores: perfiles });
        return json({ status: "ok" });
      }

      const { area, modo } = d;
      let { jugador, puntaje } = d;
      if (typeof jugador !== "string" || typeof area !== "string" || typeof modo !== "string" || puntaje == null) {
        return error(400, "Faltan campos");
      }
      jugador = jugador.trim();
      if (!jugador || [...jugador].length > 24 || /[\u0000-\u001f\u007f-\u009f]/.test(jugador)) return error(400, "Nombre inválido");
      if (!AREAS.has(area)) return error(400, "Materia inválida");
      if (!MODOS.has(modo)) return error(400, "Modo inválido");
      puntaje = typeof puntaje === "string" ? Number(puntaje.trim()) : puntaje;
      if (!Number.isInteger(puntaje)) return error(400, "Puntaje inválido");
      if (puntaje < 1 || puntaje > MAX_PUNTAJE) return error(400, "Puntaje fuera de rango");

      const filas = await leer(store);
      const clave = jugador.toLowerCase();
      const existente = filas.find((f) => f.area === area && f.modo === modo && f.jugador.toLowerCase() === clave);
      if (existente) {
        if (puntaje <= existente.puntaje) return json({ status: "ok" });
        existente.puntaje = puntaje;
        existente.jugador = jugador;
        existente.creado = Date.now();
      } else {
        filas.push({ jugador, area, modo, puntaje, creado: Date.now() });
        const grupo = filas.filter((f) => f.area === area && f.modo === modo).sort(ordenar);
        if (grupo.length > MAX_GUARDADOS) {
          const sobran = new Set(grupo.slice(MAX_GUARDADOS));
          for (let i = filas.length - 1; i >= 0; i--) if (sobran.has(filas[i])) filas.splice(i, 1);
        }
      }
      await store.setJSON("ranking", { ranking: filas });
      return json({ status: "ok" });
    }

    return new Response(null, { status: 405, headers: CORS });
  } catch (e) {
    console.error("Error en ranking:", e);
    return error(500, "Error interno");
  }
};
