# -*- coding: utf-8 -*-
"""Utilidades comunes para los generadores de preguntas de matemáticas."""
import re, unicodedata, random, math
from fractions import Fraction as F

_SUP = dict(zip("0123456789-+()n", "⁰¹²³⁴⁵⁶⁷⁸⁹⁻⁺⁽⁾ⁿ"))
_SUB = dict(zip("0123456789", "₀₁₂₃₄₅₆₇₈₉"))

def sup(x):
    return "".join(_SUP[c] for c in str(x).replace("−", "-"))

def sub(x):
    return "".join(_SUB[c] for c in str(x))

def num(x):
    x = F(x)
    s = str(abs(x.numerator)) if x.denominator == 1 else f"{abs(x.numerator)}/{x.denominator}"
    return ("−" if x < 0 else "") + s

def big(n):
    """Entero con espacio fino para miles (>= 5 dígitos), signo Unicode."""
    n = int(n)
    s = str(abs(n))
    if len(s) >= 5:
        s = "{:,}".format(abs(n)).replace(",", " ")
    return ("−" if n < 0 else "") + s

def dec(x, nd=4):
    """Decimal con coma."""
    s = f"{float(x):.{nd}f}".rstrip("0").rstrip(".")
    if s in ("", "-0"): s = "0"
    return s.replace(".", ",").replace("-", "−")

def sc(t, lo, hi):
    return int(round(lo + t * (hi - lo)))

def term_pow(c, p, v="x"):
    pass

def poly(cs, v="x"):
    """cs: coeficientes de mayor a menor grado."""
    n = len(cs) - 1
    out = ""
    for i, c in enumerate(cs):
        p = n - i
        c = F(c)
        if c == 0: continue
        a = abs(c)
        if p == 0:
            body = num(a)
        else:
            if a == 1: coef = ""
            elif a.denominator == 1: coef = str(a.numerator)
            else: coef = f"({num(a)})"
            body = coef + v + (sup(p) if p > 1 else "")
        if not out: out = ("−" if c < 0 else "") + body
        else: out += (" − " if c < 0 else " + ") + body
    return out or "0"

def lin_str(m, b, v="x"):
    """Recta y = mx + b con fracciones tipo 2x/3."""
    m = F(m); b = F(b)
    if m == 0: body = num(b)
    else:
        a = abs(m)
        if a.denominator == 1:
            t = ("" if a == 1 else str(a.numerator)) + v
        else:
            t = (str(a.numerator) if a.numerator != 1 else "") + v + "/" + str(a.denominator)
        body = ("−" if m < 0 else "") + t
        if b != 0: body += (" − " if b < 0 else " + ") + num(abs(b))
    return "y = " + body

def norm(s):
    s = str(s).lower()
    s = unicodedata.normalize("NFD", s)
    s = re.sub(r"[̀-ͯ]", "", s)
    s = re.sub(r"\s+", " ", s)
    s = re.sub(r"[.¿?¡!]+$", "", s)
    return s.strip()

_REV_SUP = {v: k for k, v in _SUP.items()}

def ascii_var(s):
    out = ""
    i = 0
    while i < len(s):
        c = s[i]
        if c in _REV_SUP and c not in "⁻":
            j = i
            while j < len(s) and (s[j] in _REV_SUP):
                j += 1
            seg = "".join(_REV_SUP[k] for k in s[i:j])
            out += "^" + (seg if re.fullmatch(r"-?\d+", seg) else "(" + seg + ")")
            i = j
            continue
        out += c
        i += 1
    out = (out.replace("−", "-").replace("·", "*").replace("×", "x").replace("√", "sqrt")
              .replace("π", "pi").replace("≤", "<=").replace("≥", ">=").replace("≠", "!=")
              .replace("∞", "inf").replace("⁻", "-"))
    return out

def variants(ans, extra=()):
    v = [ans, ans.replace(" ", "")]
    a = ascii_var(ans)
    v += [a, a.replace(" ", "")]
    for x in list(v):
        if "," in x and re.search(r"\d,\d", x): v.append(re.sub(r"(\d),(\d)", r"\1.\2", x))
    v += list(extra)
    seen, out = set(), []
    for x in v:
        k = norm(x)
        if k not in seen:
            seen.add(k); out.append(x)
    return out

def mk(q, ans, wrong, expl, acc="auto", extra=()):
    """Devuelve [q, ans, wrong3, acc, expl] (sin dificultad)."""
    ans = str(ans)
    ws, seen = [], {norm(ans)}
    for w in wrong:
        w = str(w)
        if norm(w) in seen: continue
        seen.add(norm(w)); ws.append(w)
        if len(ws) == 3: break
    if len(ws) < 3:
        raise ValueError("faltan distractores: " + q)
    if len(q) > 250: raise ValueError("pregunta larga: " + q)
    for o in [ans] + ws:
        if len(o) > 60: raise ValueError("opción larga: " + o)
    if acc == "auto": accl = variants(ans, extra)
    elif acc is None: accl = []
    else: accl = list(acc)
    return [q, ans, ws, accl, expl]

def nw(r, v, *mist):
    """Distractores numéricos: errores típicos primero, luego variaciones aleatorias."""
    v = F(v)
    seen = {v}
    out = []
    for m in mist:
        m = F(m)
        if m not in seen:
            seen.add(m); out.append(num(m))
    gen = [v + 1, v - 1, -v, v + 2, v - 2, 2 * v, v + 3, v - 3, v * 3, v + 10, v - 10]
    if v % 2 == 0: gen.append(v / 2)
    r.shuffle(gen)
    for g in gen:
        if g not in seen:
            seen.add(g); out.append(num(g))
    return out

def rnz(r, lo, hi):
    while True:
        x = r.randint(lo, hi)
        if x != 0: return x

def pick(r, *opts):
    return r.choice(opts)

def cx(a, b):
    """Complejo a + bi con Fraction."""
    a = F(a); b = F(b)
    if b == 0: return num(a)
    bi = ("" if abs(b) == 1 else num(abs(b))) + "i"
    if a == 0: return ("−" if b < 0 else "") + bi
    return num(a) + (" − " if b < 0 else " + ") + bi
