// Acceso del administrador de "Juega y Aprende".
//   POST /api/admin {"action":"login","user":"..","pass":".."}   -> 200 ok | 401
//   POST /api/admin {"action":"forgot"}                           -> envía un enlace de un solo uso al correo del administrador
//   POST /api/admin {"action":"reset","token":"..","user":"..","pass":".."} -> guarda la contraseña nueva
//
// Variables de entorno (Netlify → Site configuration → Environment variables):
//   ADMIN_EMAIL     correo que recibe el enlace
//   RESEND_API_KEY  clave de API de resend.com
//   MAIL_FROM       (opcional) remitente; por defecto "Juega y Aprende <onboarding@resend.dev>"
import { getStore } from "@netlify/blobs";
import crypto from "node:crypto";
import { promisify } from "node:util";

const scrypt = promisify(crypto.scrypt);

// Credencial inicial (se usa hasta que el administrador restablezca su contraseña).
const SALT = "jya-2026-a7c1f9";
const ROUNDS = 20000;
const INITIAL_HASH = "e8bb73e8432210249ffb6ebdb0abb7e60bf42c9c1e811963eef5e3b2f6600527";

const TOKEN_MINUTOS = 15;
const MIN_PASS = 8;
const MAX_CUERPO = 2048;

export const config = { path: "/api/admin" };

const json = (data, status = 200) =>
  new Response(JSON.stringify(data), {
    status,
    headers: { "Content-Type": "application/json; charset=utf-8", "Cache-Control": "no-store" },
  });

const sha = (x) => crypto.createHash("sha256").update(x, "utf8").digest("hex");
const safeEq = (a, b) => {
  const x = Buffer.from(String(a)), y = Buffer.from(String(b));
  return x.length === y.length && crypto.timingSafeEqual(x, y);
};
const normUser = (u) => String(u).trim().toLowerCase();

function hashInicial(user, pass) {
  let h = sha(`${SALT}|${normUser(user)}|${pass}`);
  for (let i = 1; i < ROUNDS; i++) h = sha(h + SALT);
  return h;
}

// Límites sencillos en memoria (frenan intentos repetidos mientras la función siga activa).
const fallos = new Map();
function bloqueado(ip) {
  const ahora = Date.now();
  const l = (fallos.get(ip) || []).filter((t) => ahora - t < 10 * 60_000);
  fallos.set(ip, l);
  return l.length >= 8;
}
const anotarFallo = (ip) => fallos.set(ip, [...(fallos.get(ip) || []), Date.now()]);
let ultimoCorreo = 0;

async function verificar(store, user, pass) {
  const cred = await store.get("cred", { type: "json" });
  if (cred && cred.user && cred.salt && cred.hash) {
    if (normUser(user) !== cred.user) return false;
    const h = (await scrypt(pass, Buffer.from(cred.salt, "hex"), 64)).toString("hex");
    return safeEq(h, cred.hash);
  }
  return safeEq(hashInicial(user, pass), INITIAL_HASH);
}

async function enviarCorreo(para, enlace) {
  const r = await fetch("https://api.resend.com/emails", {
    method: "POST",
    headers: { Authorization: `Bearer ${process.env.RESEND_API_KEY}`, "Content-Type": "application/json" },
    body: JSON.stringify({
      from: process.env.MAIL_FROM || "Juega y Aprende <onboarding@resend.dev>",
      to: [para],
      subject: "Restablecer tu contraseña · Juega y Aprende",
      html:
        `<p>Pediste restablecer la contraseña del administrador de Juega y Aprende.</p>` +
        `<p><a href="${enlace}">Elegir una contraseña nueva</a></p>` +
        `<p>El enlace funciona una sola vez y vence en ${TOKEN_MINUTOS} minutos. ` +
        `Si no lo pediste tú, ignora este correo: tu contraseña actual sigue igual.</p>`,
      text: `Elige una contraseña nueva aquí (una sola vez, ${TOKEN_MINUTOS} minutos): ${enlace}`,
    }),
  });
  if (!r.ok) throw new Error(`Resend respondió ${r.status}: ${await r.text()}`);
}

export default async (req, context) => {
  try {
    if (req.method !== "POST") return new Response(null, { status: 405 });
    const texto = await req.text();
    if (new TextEncoder().encode(texto).length > MAX_CUERPO) return json({ error: "Cuerpo demasiado grande" }, 413);
    let d;
    try { d = JSON.parse(texto); } catch { return json({ error: "JSON inválido" }, 400); }
    if (!d || typeof d !== "object" || Array.isArray(d)) return json({ error: "JSON inválido" }, 400);

    const ip = context?.ip || req.headers.get("x-nf-client-connection-ip") || "desconocida";
    const store = getStore({ name: "admin", consistency: "strong" });

    if (d.action === "login") {
      if (typeof d.user !== "string" || typeof d.pass !== "string" || d.user.length > 64 || d.pass.length > 200) {
        return json({ error: "Datos inválidos" }, 400);
      }
      if (bloqueado(ip)) return json({ error: "Demasiados intentos" }, 429);
      if (await verificar(store, d.user, d.pass)) return json({ status: "ok" });
      anotarFallo(ip);
      return json({ error: "Usuario o contraseña incorrectos" }, 401);
    }

    if (d.action === "forgot") {
      if (!process.env.ADMIN_EMAIL || !process.env.RESEND_API_KEY) return json({ error: "Correo no configurado" }, 503);
      if (Date.now() - ultimoCorreo < 60_000) return json({ status: "ok" }); // no reenviar seguido
      ultimoCorreo = Date.now();
      const token = crypto.randomBytes(32).toString("base64url");
      await store.setJSON("reset", { hash: sha(token), exp: Date.now() + TOKEN_MINUTOS * 60_000 });
      const enlace = `${new URL(req.url).origin}/Juega_y_Aprende_admin.html#reset=${token}`;
      try {
        await enviarCorreo(process.env.ADMIN_EMAIL, enlace);
      } catch (e) {
        console.error("No se pudo enviar el correo:", e);
        await store.delete("reset");
        return json({ error: "No se pudo enviar el correo" }, 502);
      }
      return json({ status: "ok" });
    }

    if (d.action === "reset") {
      if (typeof d.token !== "string" || typeof d.user !== "string" || typeof d.pass !== "string") {
        return json({ error: "Datos inválidos" }, 400);
      }
      if (bloqueado(ip)) return json({ error: "Demasiados intentos" }, 429);
      const user = normUser(d.user);
      if (!user || user.length > 64) return json({ error: "Usuario inválido" }, 400);
      if (d.pass.length < MIN_PASS || d.pass.length > 200) return json({ error: `La contraseña debe tener al menos ${MIN_PASS} caracteres` }, 400);
      const guardado = await store.get("reset", { type: "json" });
      if (!guardado || Date.now() > guardado.exp || !safeEq(sha(d.token), guardado.hash)) {
        anotarFallo(ip);
        return json({ error: "Enlace inválido o vencido" }, 410);
      }
      const salt = crypto.randomBytes(16);
      const hash = (await scrypt(d.pass, salt, 64)).toString("hex");
      await store.setJSON("cred", { user, salt: salt.toString("hex"), hash });
      await store.delete("reset"); // un solo uso
      return json({ status: "ok" });
    }

    return json({ error: "Acción inválida" }, 400);
  } catch (e) {
    console.error("Error en admin:", e);
    return json({ error: "Error interno" }, 500);
  }
};
