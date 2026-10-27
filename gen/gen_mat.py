#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Generador de preguntas de Matemáticas (alg, calc, lin, est) para Juega y Aprende.
Todas las respuestas numéricas se calculan en código. Salida: gen/out_mat.json
Fila: [pregunta, correcta, [3 incorrectas], [aceptadas al escribir], explicación, dificultad 0-100]
"""
import random, json, math, os, sys, itertools
from fractions import Fraction as F
try:
    import sympy as sp
except Exception:
    sp = None

R = random.Random(20261020)
OUT = {'alg': [], 'calc': [], 'lin': [], 'est': []}
SEEN = set()


# ------------------------------------------------------------------ utilidades
def nf(x):
    x = F(x)
    return str(x.numerator) if x.denominator == 1 else f"{x.numerator}/{x.denominator}"


def term_dec(x):
    d = F(x).denominator
    while d % 2 == 0: d //= 2
    while d % 5 == 0: d //= 5
    return d == 1


def dec(x, nd=3):
    s = f"{float(x):.{nd}f}"
    if '.' in s: s = s.rstrip('0').rstrip('.')
    return s


def best(x):
    """Decimal exacto si termina (≤3 decimales); si no, fracción."""
    x = F(x)
    if x.denominator == 1: return str(x.numerator)
    if term_dec(x) and x.denominator <= 1000: return dec(x, 3)
    return nf(x)


def hk(*p):
    h = 7
    for x in p: h = h * 31 + int(x)
    return h


def T(lst, key, **kw):
    if not isinstance(key, tuple): key = (key,)
    return lst[hk(*key) % len(lst)].format(**kw)


def sup(p):
    return '²' if p == 2 else '³' if p == 3 else f'^{p}'


def term(c, p, first, var='x', m='-'):
    c = F(c)
    a = abs(c)
    sg = (m if c < 0 else '') if first else (f' {m} ' if c < 0 else ' + ')
    if p == 0:
        body = nf(a)
    else:
        v = var + ('' if p == 1 else sup(p))
        if a.denominator != 1:
            body = ('' if a.numerator == 1 else str(a.numerator)) + v + '/' + str(a.denominator)
        else:
            body = ('' if a == 1 else str(a.numerator)) + v
    return sg + body


def poly(d, var='x', m='-'):
    s = ''
    first = True
    for p in sorted(d, reverse=True):
        if d[p] == 0: continue
        s += term(d[p], p, first, var, m)
        first = False
    return s or '0'


def Q(d, var='x'):
    return poly(d, var, '−')


def pmul(a, b):
    r = {}
    for i, x in a.items():
        for j, y in b.items():
            r[i + j] = r.get(i + j, 0) + x * y
    return {k: v for k, v in r.items() if v != 0}


def pder(a):
    return {k - 1: v * k for k, v in a.items() if k > 0 and v != 0}


def pint(a):
    return {k + 1: F(v) / (k + 1) for k, v in a.items()}


def peval(a, x):
    return sum(F(v) * F(x) ** k for k, v in a.items())


def padd(a, b, s=1):
    r = dict(a)
    for k, v in b.items(): r[k] = r.get(k, 0) + s * v
    return {k: v for k, v in r.items() if v != 0}


def lexpr(pairs, m='−'):
    s = ''
    first = True
    for c, v in pairs:
        if c == 0: continue
        a = abs(c)
        body = ('' if (a == 1 and v) else str(a)) + v
        if first: s += (m if c < 0 else '') + body
        else: s += (f' {m} ' if c < 0 else ' + ') + body
        first = False
    return s or '0'


def ascii_of(s):
    t = s.replace(' ', '')
    t = t.replace('²', '^2').replace('³', '^3').replace('−', '-').replace('√', 'sqrt').replace('±', '+-')
    t = t.replace('π', 'pi').replace('∞', 'inf')
    return t


def variants(s):
    out = [s, s.replace(' ', ''), ascii_of(s)]
    t = s.replace(' ', '')
    if t and all(ch.isdigit() or ch in '.-' for ch in t) and '.' in t:
        out.append(t.replace('.', ','))
    return out


def add(cat, q, ans, wrongs, expl, d, acc=()):
    ans = str(ans)
    q = q.strip()
    if q in SEEN or len(ans) > 40: return False
    accl = []
    for v in [ans] + [str(a) for a in acc] + variants(ans):
        if v and v not in accl: accl.append(v)
    ws = []
    for w in wrongs:
        w = str(w)
        if w != ans and w not in ws and w not in accl and len(w) <= 44: ws.append(w)
    if len(ws) < 3: return False
    if len(ws) > 3:
        head = ws[:6]
        ws = R.sample(head, 3)
    SEEN.add(q)
    OUT[cat].append([q, ans, ws, accl, expl, max(0, min(100, int(round(d))))])
    return True


def numwrong(c, f=None, pos=False, extra=()):
    f = f or nf
    c = F(c)
    pool = list(extra)
    cs = [c + 1, c - 1, c + 2, c - 2, c + 3, c - 3, c * 2, -c, c + 10, c - 10, c + 5, c - 5, c + 4, c - 4]
    if c.denominator == 1 and c % 2 == 0 and c != 0: cs.append(c / 2)
    cs.sort(key=lambda x: abs(x - c) + R.random() * 3)
    for x in cs:
        if pos and x < 0: continue
        if x == c: continue
        pool.append(f(x))
    return pool


def rep(n, fn, mult=60):
    ok = 0
    t = 0
    while ok < n and t < n * mult:
        t += 1
        if fn(): ok += 1
    return ok


def two_roots(a, b):
    a, b = sorted((F(a), F(b)))
    return [f"{nf(a)} y {nf(b)}", f"{nf(b)} y {nf(a)}", f"{nf(a)},{nf(b)}", f"{nf(b)},{nf(a)}", f"{nf(a)} o {nf(b)}",
            f"{nf(b)} o {nf(a)}", f"x={nf(a)}, x={nf(b)}"]


def pert(p, var='x'):
    """Variantes plausibles (incorrectas) de un polinomio dado como dict."""
    out = []
    ks = [k for k in p if p[k] != 0]
    for k in ks:
        for ch in (-1, 1):
            q = dict(p); q[k] = F(q[k]) + ch
            out.append(q)
        q = dict(p); q[k] = -F(q[k]); out.append(q)
    for k in ks:
        if len(ks) > 1:
            q = dict(p); q[k] = 0; out.append(q)
    R.shuffle(out)
    res = []
    for q in out:
        s = poly({a: b for a, b in q.items() if b != 0})
        if s not in res and s != poly(p): res.append(s)
    return res


def conj(items, d):
    """items: (pregunta, correcta, [incorrectas], explicación, dificultad)"""
    return None


# =================================================================== ÁLGEBRA
def a_sum():
    a, b = R.randint(1, 20), R.randint(1, 20); s = a + b
    q = T(["¿Cuánto es {a} + {b}?", "Calcula {a} + {b}.", "Suma: {a} + {b} = ?"], (a, b), a=a, b=b)
    return add('alg', q, s, numwrong(s, pos=True), f"{a} + {b} = {s}.", s / 6)


def a_sub():
    a = R.randint(4, 40); b = R.randint(1, a - 1); s = a - b
    q = T(["¿Cuánto es {a} − {b}?", "Calcula {a} − {b}.", "Resta: {a} − {b} = ?"], (a, b), a=a, b=b)
    return add('alg', q, s, numwrong(s, pos=True), f"{a} − {b} = {s}.", 1 + a / 9)


def a_mul():
    a, b = R.randint(2, 12), R.randint(2, 12); s = a * b
    q = T(["¿Cuánto es {a} × {b}?", "Calcula {a} × {b}.", "Si cada caja tiene {a} lápices y hay {b} cajas, ¿cuántos lápices hay?"], (a, b), a=a, b=b)
    return add('alg', q, s, numwrong(s, pos=True, extra=[a + b, s + a, s - b]), f"{a} × {b} = {s}.", 2 + s / 18)


def a_div():
    b, c = R.randint(2, 12), R.randint(2, 12); a = b * c
    q = T(["¿Cuánto es {a} ÷ {b}?", "Calcula {a} ÷ {b}.", "Reparte {a} dulces en partes iguales entre {b} niños. ¿Cuántos recibe cada uno?"], (a, b), a=a, b=b)
    return add('alg', q, c, numwrong(c, pos=True, extra=[b, a - b]), f"{a} ÷ {b} = {c}, porque {b} × {c} = {a}.", 4 + a / 20)


def a_neg():
    a, b = R.randint(1, 15), R.randint(1, 15)
    fi = R.randint(0, 4)
    if fi == 0: q, s = f"¿Cuánto es −{a} + {b}?", -a + b
    elif fi == 1: q, s = f"¿Cuánto es {a} − {b}?", a - b
    elif fi == 2: q, s = f"¿Cuánto es (−{a}) × {b}?", -a * b
    elif fi == 3: q, s = f"¿Cuánto es (−{a}) × (−{b})?", a * b
    else: q, s = f"¿Cuánto es {a} − (−{b})?", a + b
    if fi == 1 and a > b: return False
    return add('alg', q, s, numwrong(s, extra=[abs(s), -s]), f"Se aplican las reglas de signos: el resultado es {s}.", 9 + (abs(s) / 20) + fi)


def a_order():
    a, b, c, d = [R.randint(2, 9) for _ in range(4)]
    fi = R.randint(0, 4)
    if fi == 0: q, s, w = f"{a} + {b} × {c}", a + b * c, [(a + b) * c]
    elif fi == 1: q, s, w = f"({a} + {b}) × {c}", (a + b) * c, [a + b * c]
    elif fi == 2: q, s, w = f"{a} × {b} − {c} × {d}", a * b - c * d, [(a * b - c) * d]
    elif fi == 3: q, s, w = f"{a} + {b}² − {c}", a + b * b - c, [(a + b) ** 2 - c]
    else: q, s, w = f"{a * b} ÷ {b} + {c} × {d}", a + c * d, [(a + c) * d, a * b // b + c + d]
    return add('alg', "Aplicando el orden de las operaciones, ¿cuánto es " + q + "?", s, numwrong(s, extra=w),
               "Primero potencias y paréntesis, luego × y ÷, y al final + y −.", 11 + fi * 2 + abs(s) / 40)


def a_pow():
    k = R.randint(0, 7)
    if k == 0:
        a = R.randint(2, 20); q, s, e = f"¿Cuánto es {a}²?", a * a, f"{a}² = {a} × {a} = {a*a}."; d = 5 + a / 3
    elif k == 1:
        a = R.randint(2, 9); q, s, e = f"¿Cuánto es {a}³?", a ** 3, f"{a}³ = {a}·{a}·{a} = {a**3}."; d = 12 + a
    elif k == 2:
        n = R.randint(2, 12); q, s, e = f"¿Cuánto es 2 elevado a la {n}?", 2 ** n, f"2^{n} = {2**n}."; d = 9 + n
    elif k == 3:
        a = R.randint(2, 20); q, s, e = f"¿Cuál es la raíz cuadrada de {a*a}?", a, f"√{a*a} = {a}, porque {a}² = {a*a}."; d = 6 + a / 2
    elif k == 4:
        a = R.randint(2, 9); q, s, e = f"¿Cuánto es (−{a})² y cuánto es −{a}²? Da el valor de (−{a})² − (−{a}²).", 2 * a * a, f"(−{a})² = {a*a} y −{a}² = −{a*a}; la resta da {2*a*a}."; d = 30 + a
    elif k == 5:
        a = R.randint(2, 15); q, s, e = f"¿Cuánto es {a}⁰?", 1, "Todo número distinto de 0 elevado a la 0 vale 1."; d = 14
    else:
        a, n = R.randint(2, 5), R.randint(1, 3)
        s = F(1, a ** n); q = f"¿Cuánto es {a}^(−{n})?"; e = f"{a}^(−{n}) = 1/{a**n}."; d = 36 + a + n * 2
        return add('alg', q, nf(s), [nf(-a ** n), nf(F(a ** n)), nf(F(-1, a ** n)), nf(F(1, a * n))], e, d)
    return add('alg', q, s, numwrong(s, pos=True), e, d)


def a_frac():
    k = R.randint(0, 4)
    dn = [2, 3, 4, 5, 6, 8, 10, 12]
    q1, q2 = R.choice(dn), R.choice(dn)
    p1, p2 = R.randint(1, q1 - 1) if q1 > 1 else 1, R.randint(1, q2 - 1)
    f1, f2 = F(p1, q1), F(p2, q2)
    if k == 0:
        s = f1 + f2
        return add('alg', f"¿Cuánto es {p1}/{q1} + {p2}/{q2}? (fracción reducida)", nf(s),
                   [nf(F(p1 + p2, q1 + q2)), nf(f1 * f2), nf(f1 - f2), nf(s + F(1, q1))], "Se busca un denominador común y se suman los numeradores.",
                   22 + (q1 * q2) / 6, acc=[best(s)])
    if k == 1:
        if f1 <= f2: return False
        s = f1 - f2
        return add('alg', f"¿Cuánto es {p1}/{q1} − {p2}/{q2}? (fracción reducida)", nf(s),
                   [nf(F(p1 - p2, q1 - q2) if q1 != q2 else F(1, 2)), nf(f1 + f2), nf(s + F(1, q1)), nf(f2 - f1)], "Se usa denominador común y se restan los numeradores.",
                   24 + (q1 * q2) / 6, acc=[best(s)])
    if k == 2:
        s = f1 * f2
        return add('alg', f"¿Cuánto es {p1}/{q1} × {p2}/{q2}? (fracción reducida)", nf(s),
                   [nf(f1 + f2), nf(f1 / f2), nf(F(p1 * q2, q1 * p2) + 0 if False else f1 + f2 + F(1, 7)), nf(s * 2)], "Se multiplican numeradores y denominadores y se simplifica.",
                   20 + (q1 * q2) / 12, acc=[best(s)])
    if k == 3:
        s = f1 / f2
        return add('alg', f"¿Cuánto es ({p1}/{q1}) ÷ ({p2}/{q2})? (fracción reducida)", nf(s),
                   [nf(f1 * f2), nf(f2 / f1), nf(f1 + f2), nf(F(p1 * p2, q1 * q2) + F(1, 3))], "Dividir es multiplicar por el inverso de la segunda fracción.",
                   30 + (q1 * q2) / 10, acc=[best(s)])
    g = R.randint(2, 9); n, m = p1 * g, q1 * g
    if math.gcd(p1, q1) != 1: return False
    return add('alg', f"Simplifica la fracción {n}/{m}.", nf(f1), [f"{n // g if False else n // 1}/{m // 1}" if False else nf(F(n, m * 2)), nf(F(n + 1, m)), nf(F(n, m + g)), nf(F(p1, q1 + 1))],
               f"Se divide numerador y denominador entre {g}: {p1}/{q1}.", 14 + g)


def a_fdec():
    n, d_ = R.choice([(1, 2), (1, 4), (3, 4), (1, 5), (2, 5), (3, 5), (4, 5), (1, 8), (3, 8), (1, 10), (7, 10), (1, 20), (3, 20), (7, 20), (9, 25), (3, 25)])
    s = dec(F(n, d_))
    return add('alg', f"¿Cuál es {n}/{d_} escrito como decimal?", s, [dec(F(n, d_) * 10), dec(F(d_, n)), dec(F(n, d_) / 2) if F(n, d_) / 2 != F(n, d_) else '0.1', dec(F(n + 1, d_))],
               f"{n} ÷ {d_} = {s}.", 14 + d_ / 4, acc=[s.replace('.', ',')])


def a_pct():
    k = R.randint(0, 2)
    if k == 0:
        p = R.choice([5, 10, 15, 20, 25, 30, 40, 50, 60, 75, 80]); n = R.choice([20, 40, 60, 80, 100, 120, 160, 200, 240, 300, 400, 500])
        s = F(p * n, 100)
        if s.denominator != 1: return False
        return add('alg', f"¿Cuánto es el {p}% de {n}?", nf(s), numwrong(s, pos=True, extra=[nf(F(n, p)) if (F(n, p)).denominator == 1 else nf(n - s)]), f"{p}% de {n} = {n} × {p}/100 = {nf(s)}.", 10 + p / 8 + n / 120)
    if k == 1:
        p = R.choice([10, 15, 20, 25, 30, 40, 50]); n = R.choice([20, 40, 60, 80, 100, 120, 200, 240, 400])
        s = F(n * (100 - p), 100)
        if s.denominator != 1: return False
        return add('alg', f"Un artículo cuesta {n} y tiene {p}% de descuento. ¿Cuál es el precio final?", nf(s), numwrong(s, pos=True, extra=[nf(F(n * p, 100)), nf(n + F(n * p, 100))]), f"Descuento = {nf(F(n*p,100))}; precio final = {n} − {nf(F(n*p,100))} = {nf(s)}.", 18 + p / 6)
    a = R.choice([20, 40, 50, 80, 100, 200, 250]); pc = R.choice([10, 20, 25, 30, 40, 50, 60, 75, 100, 150])
    b = F(a * (100 + pc), 100)
    if b.denominator != 1: return False
    return add('alg', f"Un valor pasa de {a} a {nf(b)}. ¿Qué porcentaje aumentó?", f"{pc}%", [f"{pc + 10}%", f"{pc * 2}%", f"{max(pc - 10, 5)}%", f"{pc + 5}%"],
               f"Aumento = {nf(b - a)}; {nf(b-a)}/{a} = {pc}%.", 26 + pc / 10)


def a_gcd():
    g = R.randint(2, 9); p, q = R.sample([2, 3, 4, 5, 6, 7, 8, 9, 10, 11], 2)
    if math.gcd(p, q) != 1: return False
    a, b = g * p, g * q
    if R.random() < .5:
        return add('alg', f"¿Cuál es el máximo común divisor (MCD) de {a} y {b}?", g, numwrong(g, pos=True, extra=[a * b // g, min(p, q)]), f"El mayor número que divide a ambos es {g}.", 14 + g / 2)
    l = a * b // g
    return add('alg', f"¿Cuál es el mínimo común múltiplo (mcm) de {a} y {b}?", l, numwrong(l, pos=True, extra=[a * b, g, a + b]), f"mcm = {a}·{b}/MCD = {l}.", 18 + l / 30)


def a_eval():
    k = R.randint(0, 2)
    if k == 0:
        a, b, x = R.randint(2, 9), R.randint(-9, 9), R.randint(1, 9)
        if b == 0: return False
        s = a * x + b
        return add('alg', f"Si x = {x}, ¿cuánto vale {Q({1: a, 0: b})}?", s, numwrong(s, extra=[a + x + b, a * (x + b)]), f"Se sustituye x = {x}: {a}·{x} + ({b}) = {s}.", 8 + abs(s) / 15)
    a, b, c, x = R.randint(1, 4), R.randint(-6, 6), R.randint(-8, 8), R.randint(-4, 5)
    p = {2: a, 1: b, 0: c}
    s = peval(p, x)
    return add('alg', f"Si f(x) = {Q(p)}, ¿cuánto vale f({x})?", nf(s), numwrong(s, extra=[nf(a * x * 2 + b * x + c)]), f"f({x}) = {a}·({x})² + ({b})·({x}) + ({c}) = {nf(s)}.", 20 + abs(x) * 2 + abs(a))


def a_eq1():
    k = R.randint(0, 3); s = R.randint(-9, 15); a = R.randint(2, 12); b = R.randint(1, 20)
    if k == 0: q, e = f"x + {b} = {s + b}", f"Se resta {b} en ambos lados: x = {s}."
    elif k == 1: q, e = f"x − {b} = {s - b}", f"Se suma {b} en ambos lados: x = {s}."
    elif k == 2: q, e = f"{a}x = {a * s}", f"Se divide entre {a}: x = {s}."
    else: q, e = f"x/{a} = {s}", f"Se multiplica por {a}: x = {a * s}."; s = a * s
    return add('alg', "Resuelve: " + q.replace('-', '−') + ". ¿Cuánto vale x?", s, numwrong(s), e, 4 + k * 2 + abs(s) / 8)


def a_eq2():
    a = R.choice([2, 3, 4, 5, 6, 7, 8, 9, -2, -3, -4, -5]); b = R.randint(-15, 15); s = R.randint(-9, 12)
    if b == 0: return False
    c = a * s + b
    return add('alg', f"Resuelve: {Q({1: a, 0: b})} = {c}".replace('= -', '= −') + ". ¿Cuánto vale x?", s, numwrong(s, extra=[nf(F(c + b, a)) if (c + b) % a == 0 else (c - b) // a + 1, nf(F(c, a))]),
               f"Se pasa {b} al otro lado y se divide entre {a}: x = ({c} − ({b}))/{a} = {s}.", 15 + abs(a) + abs(b) / 3)


def a_eq3():
    a, c = R.randint(2, 9), R.randint(1, 8)
    if a == c: return False
    b = R.randint(-9, 9); s = R.randint(-8, 10); d_ = (a - c) * s + b
    return add('alg', f"Resuelve: {Q({1: a, 0: b})} = {Q({1: c, 0: d_})}. ¿Cuánto vale x?", s, numwrong(s, extra=[nf(F(d_ - b, a + c)) if (d_ - b) % (a + c) == 0 else s + 3]),
               f"Se agrupan las x a un lado: ({a} − {c})x = {d_} − ({b}), entonces x = {s}.", 30 + abs(a - c) + abs(s) / 4)


def a_eqp():
    a, b, s = R.randint(2, 7), R.choice([-6, -5, -4, -3, -2, -1, 1, 2, 3, 4, 5, 6]), R.randint(-8, 9)
    c = a * (s + b)
    bs = f"+ {b}" if b > 0 else f"− {-b}"
    return add('alg', f"Resuelve: {a}(x {bs}) = {c}".replace('= -', '= −') + ". ¿Cuánto vale x?", s, numwrong(s, extra=[nf(F(c, a) + b) if c % a == 0 else s + 1, s + 2 * b]),
               f"Se divide entre {a}: x {bs} = {c//a}; luego x = {s}.", 30 + abs(a) + abs(b) / 2)


def a_eqf():
    k = R.randint(0, 2)
    if k == 0:
        a, b, c = R.randint(2, 6), R.randint(-5, 8), R.randint(-4, 8); s = a * (c - b)
        return add('alg', f"Resuelve: x/{a} {'+' if b >= 0 else '−'} {abs(b)} = {c}".replace('= -', '= −') + ". ¿Cuánto vale x?", s, numwrong(s, extra=[a * c + b, nf(F(c - b, a))]),
                   f"x/{a} = {c} − ({b}) = {c-b}; x = {s}.", 32 + a)
    if k == 1:
        a, b, c = R.randint(-6, 8), R.randint(2, 6), R.randint(-5, 7); s = b * c - a
        return add('alg', f"Resuelve: (x {'+' if a >= 0 else '−'} {abs(a)})/{b} = {c}".replace('= -', '= −') + ". ¿Cuánto vale x?", s, numwrong(s, extra=[b * c + a, c - a]),
                   f"Se multiplica por {b}: x {'+' if a>=0 else '−'} {abs(a)} = {b*c}; x = {s}.", 33 + b)
    p, q = R.choice([(1, 2), (2, 3), (3, 4), (3, 5), (2, 5), (4, 5), (5, 6), (1, 3)]), None
    p, q = p
    r = R.randint(1, 9); s = F(r * q, p)
    return add('alg', f"Resuelve: ({p}/{q})x = {r}. ¿Cuánto vale x?", nf(s), [nf(F(r * p, q)), nf(F(r, q + p)), nf(F(r + p, q)), nf(F(q, p))], f"Se multiplica por {q}/{p}: x = {r}·{q}/{p} = {nf(s)}.", 36 + q, acc=[best(s)])


def a_like():
    k = R.randint(0, 1)
    if k == 0:
        a, b, c, d_ = R.randint(1, 9), R.randint(-9, 9), R.randint(-6, 9), R.randint(-9, 9)
        if c == 0 or b == 0: return False
        p = {1: a + c, 0: b + d_}
        q = f"Reduce los términos semejantes: {Q({1: a, 0: b})} + ({Q({1: c, 0: d_})})"
        return add('alg', q, poly(p), pert(p), "Se suman por separado los términos con x y los términos independientes.", 14 + abs(b) / 3 + abs(c))
    a, b, c, d_ = R.randint(1, 6), R.randint(1, 8), R.randint(-4, 6), R.randint(-7, 9)
    if c == 0: return False
    p = {2: a + c, 1: b + d_}
    return add('alg', f"Simplifica: {Q({2: a, 1: b})} + ({Q({2: c, 1: d_})})".replace("+ (-", "+ (−"), poly(p), pert(p), "Solo se suman los términos con la misma potencia de x.", 22 + abs(a))


def fac(*parts):
    return ''.join(parts)


def a_expand():
    k = R.randint(0, 4)
    if k == 0:
        a, b = R.randint(-9, 9), R.randint(-9, 9)
        if a == 0 or b == 0: return False
        p = {2: 1, 1: a + b, 0: a * b}
        q = f"Desarrolla: (x {'+' if a>0 else '−'} {abs(a)})(x {'+' if b>0 else '−'} {abs(b)})"
        return add('alg', q, poly(p), pert(p), f"Se multiplica término a término: x² + ({a}+{b})x + ({a})({b}).", 34 + (abs(a) + abs(b)) / 2)
    if k == 1:
        a = R.randint(1, 9) * R.choice([1, -1])
        p = {2: 1, 1: 2 * a, 0: a * a}
        return add('alg', f"Desarrolla: (x {'+' if a>0 else '−'} {abs(a)})²", poly(p), [poly({2: 1, 0: a * a}), poly({2: 1, 1: a, 0: a * a}), poly({2: 1, 1: 2 * a, 0: -a * a}), poly({2: 1, 1: 2 * a, 0: a})],
                   "Cuadrado de un binomio: (x + a)² = x² + 2ax + a².", 36 + abs(a) / 2)
    if k == 2:
        a = R.randint(2, 12)
        p = {2: 1, 0: -a * a}
        return add('alg', f"Desarrolla: (x + {a})(x − {a})", poly(p), [poly({2: 1, 0: a * a}), poly({2: 1, 1: 2 * a, 0: -a * a}), poly({2: 1, 1: -2 * a, 0: a * a}), poly({2: 1, 1: a, 0: -a * a})],
                   "Diferencia de cuadrados: (x + a)(x − a) = x² − a².", 33 + a / 3)
    if k == 3:
        a, b, c, d_ = R.randint(2, 5), R.randint(-7, 7), R.randint(1, 4), R.randint(-7, 7)
        if b == 0 or d_ == 0: return False
        p = {2: a * c, 1: a * d_ + b * c, 0: b * d_}
        q = f"Desarrolla: ({Q({1: a, 0: b})})({Q({1: c, 0: d_})})"
        return add('alg', q, poly(p), pert(p), "Se aplica la propiedad distributiva a los cuatro productos.", 50 + a + c + (abs(b) + abs(d_)) / 3)
    a, b, c = R.randint(2, 9), R.randint(1, 8), R.randint(-9, 9)
    if c == 0: return False
    p = {2: a, 1: a * b, 0: a * c} if False else {2: a, 1: a * b, 0: a * c}
    q = f"Desarrolla: {a}(x² {'+' if b>0 else '−'} {abs(b)}x {'+' if c>0 else '−'} {abs(c)})"
    return add('alg', q, poly(p), pert(p), f"Se multiplica {a} por cada término del paréntesis.", 18 + a + abs(c) / 3)


def a_factor():
    k = R.randint(0, 3)
    if k == 0:
        a, b = R.randint(-9, 9), R.randint(-9, 9)
        if a == 0 or b == 0 or a == b: return False
        p = {2: 1, 1: a + b, 0: a * b}
        f1, f2 = f"(x {'+' if a>0 else '-'} {abs(a)})", f"(x {'+' if b>0 else '-'} {abs(b)})"
        ans = f1 + f2
        alt = f2 + f1
        w = [f"(x {'-' if a>0 else '+'} {abs(a)})(x {'+' if b>0 else '-'} {abs(b)})", f"(x {'-' if a>0 else '+'} {abs(a)})(x {'-' if b>0 else '+'} {abs(b)})",
             f"(x {'+' if a>0 else '-'} {abs(a+b)})(x {'+' if a>0 else '-'} 1)" if False else f"(x {'+' if a>0 else '-'} {abs(a * b)})(x {'+' if a>0 else '-'} 1)", f"(x {'+' if a>0 else '-'} {abs(a)})(x {'-' if b>0 else '+'} {abs(b)})"]
        return add('alg', f"Factoriza: {Q(p)}", ans, w, f"Se buscan dos números con producto {a*b} y suma {a+b}: {a} y {b}.", 40 + (abs(a) + abs(b)) / 2, acc=[alt, alt.replace(' ', '')])
    if k == 1:
        a = R.randint(2, 15)
        ans = f"(x - {a})(x + {a})"
        return add('alg', f"Factoriza: {Q({2: 1, 0: -a * a})}", ans, [f"(x - {a})²", f"(x + {a})²", f"(x - {a * a})(x + 1)", f"(x - {a})(x - {a})"], f"Diferencia de cuadrados: x² − {a*a} = (x − {a})(x + {a}).", 38 + a / 3,
                   acc=[f"(x + {a})(x - {a})", f"(x+{a})(x-{a})"])
    if k == 2:
        g, a, b = R.randint(2, 9), R.randint(1, 7), R.randint(1, 9)
        if math.gcd(a, b) != 1: return False
        ans = f"{g}({a}x + {b})" if a != 1 else f"{g}(x + {b})"
        w = [f"{g}({a}x - {b})", f"{g}({a}x + {g*b})", f"({g}x)({a}x + {b})", f"{a}({g}x + {b})"]
        return add('alg', f"Factoriza sacando factor común: {Q({1: g * a, 0: g * b})}", ans, w, f"El factor común de {g*a} y {g*b} es {g}.", 25 + g)
    a = R.randint(1, 10)
    ans = f"(x + {a})²"
    return add('alg', f"Factoriza el trinomio cuadrado perfecto: {Q({2: 1, 1: 2 * a, 0: a * a})}", ans, [f"(x - {a})²", f"(x + {a})(x - {a})", f"(x + {2*a})²", f"(x + {a*a})²"], f"x² + {2*a}x + {a*a} = (x + {a})².", 45 + a / 2)


def a_quad():
    k = R.randint(0, 2)
    r1, r2 = R.randint(-9, 9), R.randint(-9, 9)
    if r1 == r2 or r1 == 0 or r2 == 0: return False
    if k == 0:
        p = {2: 1, 1: -(r1 + r2), 0: r1 * r2}
        ans = two_roots(r1, r2)
        w = [f"{nf(-r1)} y {nf(-r2)}" if r1 + r2 != 0 else f"{r1+1} y {r2}", f"{r1 * r2} y {r1 + r2}", f"{nf(r1)} y {nf(-r2)}", f"{nf(-r1)} y {nf(r2)}"]
        w = [x for x in w if x not in ans]
        return add('alg', f"¿Cuáles son las soluciones de {Q(p)} = 0?", ans[0], w + [f"{nf(r1+1)} y {nf(r2)}"], f"Factorizando: (x − {r1})(x − {r2}) = 0, así que x = {r1} o x = {r2}.", 44 + (abs(r1) + abs(r2)) / 3, acc=ans[1:])
    if k == 1:
        g = R.randint(2, 4)
        p = {2: g, 1: -g * (r1 + r2), 0: g * r1 * r2}
        ans = two_roots(r1, r2)
        return add('alg', f"¿Cuáles son las soluciones de {Q(p)} = 0?", ans[0], [f"{nf(-r1)} y {nf(-r2)}", f"{nf(g*r1)} y {nf(g*r2)}", f"{nf(r1)} y {nf(F(r2, g))}", f"{nf(r1+g)} y {nf(r2)}"],
                   f"Se divide entre {g} y se factoriza: x² − ({r1+r2})x + ({r1*r2}) = 0.", 50 + g * 2 + (abs(r1) + abs(r2)) / 4, acc=ans[1:])
    a, b = R.randint(2, 4), R.randint(1, 7)
    if math.gcd(a, b) != 1: return False
    c, d_ = R.randint(1, 5), R.randint(-6, 6)
    if d_ == 0: return False
    # (a x + b)(c x + d)
    p = {2: a * c, 1: a * d_ + b * c, 0: b * d_}
    roots = [F(-b, a), F(-d_, c)]
    if roots[0] == roots[1]: return False
    ans = two_roots(*roots)
    return add('alg', f"¿Cuáles son las soluciones de {Q(p)} = 0?", ans[0], [f"{nf(F(b, a))} y {nf(F(d_, c))}", f"{nf(-b)} y {nf(-d_)}", f"{nf(F(-b, a))} y {nf(F(d_, c))}", f"{nf(F(b,a))} y {nf(F(-d_,c))}"],
               f"Se factoriza como ({a}x + {b})({c}x + {d_}) = 0.", 68 + (a + c) * 2 + abs(d_) / 3, acc=ans[1:])


def a_disc():
    a, b, c = R.randint(1, 5), R.randint(-9, 9), R.randint(-9, 9)
    if b == 0 or c == 0: return False
    D = b * b - 4 * a * c
    p = {2: a, 1: b, 0: c}
    if R.random() < .5:
        return add('alg', f"¿Cuál es el discriminante de {Q(p)}?", D, [b * b + 4 * a * c, -b * b - 4 * a * c if D != -b*b-4*a*c else D+3, b * b - 2 * a * c, 4 * a * c - b * b], f"Δ = b² − 4ac = {b*b} − 4·{a}·({c}) = {D}.", 48 + abs(D) / 12)
    ans = "Dos soluciones reales" if D > 0 else "Una solución real doble" if D == 0 else "Ninguna solución real"
    opts = ["Dos soluciones reales", "Una solución real doble", "Ninguna solución real", "Infinitas soluciones"]
    return add('alg', f"Sin resolverla, ¿cuántas soluciones reales tiene {Q(p)} = 0?", ans, [o for o in opts if o != ans], f"Δ = {b*b} − 4·{a}·({c}) = {D}; {'Δ>0' if D>0 else 'Δ=0' if D==0 else 'Δ<0'}.", 52 + abs(D) / 30)


def a_irr():
    p, k = R.randint(-6, 6), R.choice([2, 3, 5, 6, 7, 10, 11, 13])
    if p == 0: return False
    b = -2 * p; c = p * p - k
    ans = f"{p}±√{k}"
    return add('alg', f"Con la fórmula general, ¿cuáles son las soluciones de {Q({2: 1, 1: b, 0: c})} = 0?", ans, [f"{-p}±√{k}", f"{p}±√{k+1}", f"{2*p}±√{k}", f"{p}±{k}"],
               f"Δ = {b*b-4*c} = 4·{k}, y x = ({-b} ± 2√{k})/2 = {p} ± √{k}.", 66 + k / 2, acc=[f"{p} ± √{k}", f"{p}+-√{k}"])


def a_vertex():
    a, h, k = R.choice([1, 1, 2, 3, -1, -2]), R.randint(-6, 7), R.randint(-9, 9)
    if h == 0: return False
    p = {2: a, 1: -2 * a * h, 0: a * h * h + k}
    ans = f"({h}, {k})"
    return add('alg', f"¿Cuál es el vértice de la parábola y = {Q(p)}?", ans, [f"({-h}, {k})", f"({h}, {-k})", f"({2*h}, {k})", f"({h}, {p[0]})" if p[0] != k else f"({h+1}, {k})"],
               f"x = −b/(2a) = {h}; y = {k}.", 56 + abs(a) * 2 + abs(h) / 2, acc=[f"({h},{k})"])


def a_sumprod():
    r1, r2 = R.randint(-8, 9), R.randint(-8, 9)
    if r1 == 0 or r2 == 0 or r1 == r2: return False
    p = {2: 1, 1: -(r1 + r2), 0: r1 * r2}
    if R.random() < .5:
        return add('alg', f"Sin resolver {Q(p)} = 0, ¿cuánto suman sus dos soluciones?", r1 + r2, numwrong(r1 + r2, extra=[r1 * r2]), "La suma de las raíces es −b/a.", 62 + abs(r1 + r2) / 3)
    return add('alg', f"Sin resolver {Q(p)} = 0, ¿cuánto vale el producto de sus dos soluciones?", r1 * r2, numwrong(r1 * r2, extra=[r1 + r2]), "El producto de las raíces es c/a.", 62 + abs(r1 * r2) / 8)


def a_line():
    k = R.randint(0, 6)
    x1, y1 = R.randint(-6, 6), R.randint(-6, 6)
    x2, y2 = R.randint(-6, 6), R.randint(-6, 6)
    if x1 == x2: return False
    m = F(y2 - y1, x2 - x1)
    if k == 0:
        return add('alg', f"¿Cuál es la pendiente de la recta que pasa por ({x1}, {y1}) y ({x2}, {y2})?", nf(m), [nf(-m), nf(1 / m) if m != 0 else '1', nf(F(x2 - x1, y2 - y1)) if y2 != y1 else '2', nf(F(y2 + y1, x2 + x1)) if x1 + x2 != 0 else '3'],
                   "m = (y₂ − y₁)/(x₂ − x₁).", 28 + abs(x2 - x1), acc=[best(m)])
    if k == 1:
        mm, b = R.randint(-6, 6), R.randint(-9, 9)
        if mm == 0 or b == 0: return False
        return add('alg', f"¿Cuál es la ordenada al origen (corte con el eje y) de y = {Q({1: mm, 0: b})}?", b, numwrong(b, extra=[-b, mm]), "Es el valor de y cuando x = 0.", 18 + abs(mm))
    if k == 2:
        mm, b = R.randint(-6, 6), R.randint(-12, 12)
        if mm == 0 or b % mm != 0 or b == 0: return False
        return add('alg', f"¿En qué valor de x corta la recta y = {Q({1: mm, 0: b})} al eje x?", -b // mm if b % mm == 0 else 0, numwrong(-b // mm, extra=[b // mm if b // mm != -b // mm else 7, b, mm]), "Se resuelve mx + b = 0.", 30 + abs(mm))
    if k == 3:
        mm = R.randint(-8, 8)
        if mm == 0: return False
        return add('alg', f"Una recta tiene pendiente {mm}. ¿Cuál es la pendiente de otra recta paralela a ella?", mm, numwrong(mm, extra=[nf(F(-1, mm))]), "Las rectas paralelas tienen la misma pendiente.", 22 + abs(mm) / 2)
    if k == 4:
        mm = R.choice([2, 3, 4, 5, 6, -2, -3, -4, -5, F(1, 2), F(2, 3), F(-3, 4), F(3, 5), F(-1, 3)])
        s = -1 / F(mm)
        return add('alg', f"Una recta tiene pendiente {nf(mm)}. ¿Cuál es la pendiente de una recta perpendicular a ella?", nf(s), [nf(-F(mm)), nf(1 / F(mm)), nf(F(mm)), nf(F(mm) + 1)], "Las pendientes de rectas perpendiculares son inversas y de signo contrario.", 42 + abs(float(mm)))
    if k == 5:
        mm, x0, y0 = R.choice([-4, -3, -2, 2, 3, 4, 5]), R.randint(-5, 5), R.randint(-8, 8)
        b = y0 - mm * x0
        ans = "y = " + poly({1: mm, 0: b})
        w = ["y = " + poly({1: mm, 0: y0 + mm * x0}), "y = " + poly({1: -mm, 0: b}), "y = " + poly({1: mm, 0: -b}), "y = " + poly({1: mm, 0: y0})]
        return add('alg', f"¿Cuál es la ecuación de la recta con pendiente {mm} que pasa por ({x0}, {y0})?", ans, w, f"b = y₀ − m·x₀ = {y0} − ({mm})({x0}) = {b}.", 42 + abs(mm) + abs(x0) / 2)
    # distancia/punto medio
    trip = R.choice([(3, 4, 5), (6, 8, 10), (5, 12, 13), (8, 15, 17), (9, 12, 15), (7, 24, 25)])
    xa, ya = R.randint(-5, 5), R.randint(-5, 5)
    sx, sy = R.choice([1, -1]), R.choice([1, -1])
    if R.random() < .5:
        return add('alg', f"¿Cuál es la distancia entre ({xa}, {ya}) y ({xa + sx*trip[0]}, {ya + sy*trip[1]})?", trip[2], numwrong(trip[2], pos=True, extra=[trip[0] + trip[1]]), f"d = √({trip[0]}² + {trip[1]}²) = {trip[2]}.", 40 + trip[2] / 3)
    mx, my = F(2 * xa + sx * trip[0], 2), F(2 * ya + sy * trip[1], 2)
    ans = f"({nf(mx)}, {nf(my)})"
    return add('alg', f"¿Cuál es el punto medio entre ({xa}, {ya}) y ({xa + sx*trip[0]}, {ya + sy*trip[1]})?", ans,
               [f"({nf(mx+1)}, {nf(my)})", f"({nf(F(xa+sx*trip[0]))}, {nf(F(ya+sy*trip[1]))})", f"({nf(2*mx)}, {nf(2*my)})", f"({nf(my)}, {nf(mx)})"], "Se promedian las coordenadas.", 30 + trip[0] / 2)


def solve_lin(A, b):
    n = len(A)
    M = [[F(x) for x in row] + [F(bb)] for row, bb in zip(A, b)]
    for i in range(n):
        piv = None
        for r in range(i, n):
            if M[r][i] != 0: piv = r; break
        if piv is None: return None
        M[i], M[piv] = M[piv], M[i]
        M[i] = [x / M[i][i] for x in M[i]]
        for r in range(n):
            if r != i and M[r][i] != 0:
                f = M[r][i]
                M[r] = [x - f * y for x, y in zip(M[r], M[i])]
    return [M[i][n] for i in range(n)]


def a_sys2():
    k = R.randint(0, 1)
    if k == 0:
        s, dd = R.randint(4, 20), R.randint(1, 3)
        x = F(s + dd, 2); y = F(s - dd, 2)
        if x.denominator != 1: return False
        return add('alg', f"Dos números suman {s} y su diferencia es {dd}. ¿Cuál es el mayor?", nf(x), numwrong(x, pos=True, extra=[nf(y)]), f"x + y = {s} y x − y = {dd}; sumando, 2x = {s+dd}.", 34 + s / 5)
    x, y = R.randint(-6, 6), R.randint(-6, 6)
    while True:
        a, b, c, d_ = [R.choice([-4, -3, -2, -1, 1, 2, 3, 4, 5]) for _ in range(4)]
        if a * d_ - b * c != 0 and abs(a * d_ - b * c) > 0: break
    sol = solve_lin([[a, b], [c, d_]], [a * x + b * y, c * x + d_ * y])
    assert sol == [x, y]
    q = f"Resuelve el sistema: {lexpr([(a,'x'),(b,'y')])} = {a*x+b*y}; {lexpr([(c,'x'),(d_,'y')])} = {c*x+d_*y}. ¿Cuál es (x, y)?"
    return add('alg', q.replace('= -', '= −'), f"({x}, {y})", [f"({y}, {x})", f"({x}, {-y})" if y != 0 else f"({x+1}, {y})", f"({-x}, {y})" if x != 0 else f"({x}, {y+1})", f"({x+1}, {y-1})"],
               "Se resuelve por eliminación o sustitución.", 50 + (abs(a) + abs(b) + abs(c) + abs(d_)) * 1.5 + (abs(x) + abs(y)) / 3, acc=[f"{x},{y}", f"({x},{y})"])


def a_sys3():
    while True:
        A = [[R.randint(-3, 3) for _ in range(3)] for _ in range(3)]
        det = (A[0][0] * (A[1][1] * A[2][2] - A[1][2] * A[2][1]) - A[0][1] * (A[1][0] * A[2][2] - A[1][2] * A[2][0]) + A[0][2] * (A[1][0] * A[2][1] - A[1][1] * A[2][0]))
        if det != 0 and all(any(r) for r in A): break
    x = [R.randint(-4, 4) for _ in range(3)]
    b = [sum(A[i][j] * x[j] for j in range(3)) for i in range(3)]
    sol = solve_lin(A, b)
    assert sol == x
    eqs = '; '.join(f"{lexpr([(A[i][0],'x'),(A[i][1],'y'),(A[i][2],'z')])} = {b[i]}" for i in range(3)).replace('= -', '= −')
    return add('alg', f"Resuelve el sistema 3×3: {eqs}. ¿Cuál es (x, y, z)?", f"({x[0]}, {x[1]}, {x[2]})",
               [f"({x[1]}, {x[0]}, {x[2]})", f"({x[0]}, {x[2]}, {x[1]})", f"({x[0]+1}, {x[1]}, {x[2]-1})", f"({-x[0]}, {-x[1]}, {-x[2]})" if any(x) else "(1, 1, 1)", f"({x[0]}, {x[1]+1}, {x[2]})"],
               "Se elimina una variable para llegar a un sistema 2×2 y luego se sustituye.", 86 + min(10, (abs(det)) / 4) + sum(abs(t) for t in x) / 8, acc=[f"{x[0]},{x[1]},{x[2]}"])


def a_ineq():
    k = R.randint(0, 2)
    if k == 0:
        a = R.choice([2, 3, 4, 5, 6, -2, -3, -4, -5]); b = R.randint(-9, 9); c = R.randint(-12, 12)
        op = R.choice(['<', '>', '≤', '≥'])
        val = F(c - b, a)
        flip = {'<': '>', '>': '<', '≤': '≥', '≥': '≤'}
        res = flip[op] if a < 0 else op
        ans = f"x {res} {nf(val)}"
        wrong_op = op if a < 0 else flip[op]
        return add('alg', f"Resuelve: {Q({1: a, 0: b})} {op} {c}".replace('= -', '= −') if False else f"Resuelve la inecuación: {Q({1: a, 0: b})} {op} {c}", ans, [f"x {wrong_op} {nf(val)}", f"x {res} {nf(-val)}" if val != 0 else f"x {res} 1", f"x {res} {nf(F(c + b, a))}" if F(c + b, a) != val else f"x {res} {nf(val+1)}", f"x {wrong_op} {nf(-val)}" if val != 0 else f"x {wrong_op} 2"],
                   "Al multiplicar o dividir por un número negativo se invierte el sentido de la desigualdad." if a < 0 else "Se despeja x como en una ecuación.", 34 + (12 if a < 0 else 0) + abs(a) / 2, acc=[f"x{res}{nf(val)}"])
    if k == 1:
        a, b, c = R.randint(1, 4), R.randint(-6, 3), R.randint(4, 12)
        lo, hi = F(-c - b, a), F(c - b, a)
        # -c < a x + b < c
        ans = f"{nf(lo)} < x < {nf(hi)}"
        return add('alg', f"Resuelve la inecuación doble: −{c} < {Q({1: a, 0: b})} < {c}", ans, [f"{nf(hi)} < x < {nf(lo)}", f"{nf(F(-c+b,a))} < x < {nf(F(c+b,a))}", f"x < {nf(lo)} o x > {nf(hi)}", f"{nf(lo)} < x < {nf(hi+1)}"],
                   "Se resta b en las tres partes y se divide entre a.", 58 + c / 2, acc=[f"{nf(lo)}<x<{nf(hi)}"])
    a, b = R.randint(-6, 6), R.randint(1, 9)
    ans = f"{a-b} < x < {a+b}"
    return add('alg', f"Resuelve: |x {'+' if -a>0 else '−'} {abs(a)}| < {b}".replace('+ 0', '').replace('− 0', '') if a != 0 else f"Resuelve: |x| < {b}", ans if a != 0 else f"{-b} < x < {b}", [f"x < {a-b} o x > {a+b}", f"{-a-b} < x < {-a+b}" if a != 0 else '0', f"{a+b} < x < {a-b}", f"x < {a+b}"],
               "|x − a| < b equivale a a − b < x < a + b.", 56 + b / 2) if a != 0 else False


def a_abs():
    a, b = R.randint(-8, 8), R.randint(1, 9)
    if a == 0: return False
    ans = two_roots(a - b, a + b)
    return add('alg', f"Resuelve: |x {'−' if a>0 else '+'} {abs(a)}| = {b}", ans[0], [f"{a+b} y {a+b+1}", f"{-a-b} y {-a+b}" if (-a - b, -a + b) != (a - b, a + b) and sorted([-a - b, -a + b]) != sorted([a - b, a + b]) else f"{a+b+2} y {a-b}", f"{a+b} y {-a+b}", f"{a-b} y {-a-b}"],
               f"x − ({a}) = ±{b}; así x = {a-b} o x = {a+b}.", 46 + b / 2, acc=ans[1:])


def a_log():
    k = R.randint(0, 5)
    if k == 0:
        b, n = R.choice([2, 3, 4, 5, 10]), R.randint(2, 6)
        if b == 10 and n > 5: return False
        return add('alg', f"¿Cuánto es log_{b}({b**n})?", n, numwrong(n, pos=True, extra=[b ** n, b]), f"Porque {b}^{n} = {b**n}.", 44 + n + b / 2)
    if k == 1:
        b, m, n = R.choice([2, 3, 5]), R.randint(1, 4), R.randint(1, 4)
        return add('alg', f"¿Cuánto es log_{b}({b**m}) + log_{b}({b**n})?", m + n, numwrong(m + n, pos=True, extra=[m * n, b ** (m + n)]), f"log(ab) = log a + log b: {m} + {n} = {m+n}.", 52 + b + m + n)
    if k == 2:
        b, m, n = R.choice([2, 3, 5]), R.randint(3, 6), R.randint(1, 2)
        return add('alg', f"¿Cuánto es log_{b}({b**m}) − log_{b}({b**n})?", m - n, numwrong(m - n, pos=True, extra=[F(m, n) if m % n == 0 else m + n]), f"log(a/b) = log a − log b: {m} − {n} = {m-n}.", 54 + b + m)
    if k == 3:
        b, n = R.choice([2, 3, 4, 5]), R.randint(2, 4)
        return add('alg', f"Resuelve: log_{b}(x) = {n}. ¿Cuánto vale x?", b ** n, numwrong(b ** n, pos=True, extra=[b * n, n ** b]), f"x = {b}^{n} = {b**n}.", 52 + n * 3 + b)
    if k == 4:
        b, n = R.choice([2, 3, 5]), R.randint(2, 7)
        if b ** n > 5000: return False
        return add('alg', f"Resuelve: {b}^x = {b**n}. ¿Cuánto vale x?", n, numwrong(n, pos=True, extra=[b ** n, b * n]), f"Se igualan exponentes: x = {n}.", 44 + n + b)
    b, n, c = R.choice([2, 3]), R.randint(2, 5), R.randint(1, 3)
    return add('alg', f"Resuelve: {b}^(x + {c}) = {b**(n+c)}. ¿Cuánto vale x?", n, numwrong(n, pos=True, extra=[n + c, n * c, b ** n]), f"x + {c} = {n+c}, entonces x = {n}.", 62 + n * 2 + b)


def a_seq():
    k = R.randint(0, 5)
    a1, d_ = R.randint(-5, 12), R.randint(2, 9)
    if k == 0:
        seq = [a1 + i * d_ for i in range(4)]
        return add('alg', f"¿Qué número sigue en la sucesión {', '.join(map(str,seq))}, …?", a1 + 4 * d_, numwrong(a1 + 4 * d_, extra=[a1 + 5 * d_, a1 + 3 * d_ + 1]), f"Se suma {d_} cada vez.", 10 + d_)
    if k == 1:
        n = R.randint(8, 30)
        s = a1 + (n - 1) * d_
        return add('alg', f"En una progresión aritmética con a₁ = {a1} y razón {d_}, ¿cuánto vale el término número {n}?", s, numwrong(s, extra=[a1 + n * d_, a1 * n + d_, a1 + (n - 2) * d_]), f"aₙ = a₁ + (n − 1)d = {a1} + {n-1}·{d_} = {s}.", 40 + n / 3)
    if k == 2:
        n = R.randint(5, 20)
        s = n * (2 * a1 + (n - 1) * d_)
        if s % 2: return False
        s //= 2
        return add('alg', f"¿Cuánto suman los primeros {n} términos de la progresión aritmética con a₁ = {a1} y razón {d_}?", s, numwrong(s, extra=[n * (2 * a1 + n * d_) // 2, n * a1 + d_ * n]), f"S = n(2a₁ + (n−1)d)/2 = {s}.", 56 + n / 2)
    r = R.choice([2, 3, 4, 5])
    g1 = R.randint(1, 5)
    if k == 3:
        seq = [g1 * r ** i for i in range(4)]
        return add('alg', f"¿Qué número sigue en la sucesión {', '.join(map(str,seq))}, …?", g1 * r ** 4, numwrong(g1 * r ** 4, extra=[g1 * r ** 3 + r, g1 * r ** 3 * 2]), f"Se multiplica por {r} cada vez.", 20 + r * 2)
    if k == 4:
        n = R.randint(4, 8)
        s = g1 * r ** (n - 1)
        return add('alg', f"En una progresión geométrica con a₁ = {g1} y razón {r}, ¿cuánto vale el término número {n}?", s, numwrong(s, extra=[g1 * r ** n, g1 * r * n, g1 + r * (n - 1)]), f"aₙ = a₁·r^(n−1) = {g1}·{r}^{n-1} = {s}.", 46 + n * 2)
    n = R.randint(3, 6)
    s = g1 * (r ** n - 1) // (r - 1)
    return add('alg', f"¿Cuánto suman los primeros {n} términos de la progresión geométrica con a₁ = {g1} y razón {r}?", s, numwrong(s, extra=[g1 * r ** n, g1 * (r ** n + 1) // (r + 1) if (g1 * (r ** n + 1)) % (r + 1) == 0 else s + 2]), f"S = a₁(rⁿ − 1)/(r − 1) = {s}.", 68 + n * 2)


def a_inf():
    r = R.choice([F(1, 2), F(1, 3), F(1, 4), F(2, 3), F(1, 5), F(3, 4)])
    a1 = R.randint(1, 9)
    s = a1 / (1 - r)
    return add('alg', f"¿A qué valor converge la serie geométrica {a1} + {nf(a1*r)} + {nf(a1*r*r)} + …?", nf(s), [nf(a1 / r), nf(a1 * (1 + r)), nf(s + 1), nf(a1 * r)], f"S = a₁/(1 − r) = {a1}/{nf(1-r)} = {nf(s)}.", 76 + a1 / 2, acc=[best(s)])


def cstr(re, im):
    re, im = F(re), F(im)
    if im == 0: return nf(re)
    if im == 1: ims = 'i'
    elif im == -1: ims = '-i'
    else: ims = nf(im) + 'i'
    if re == 0: return ims
    return nf(re) + (' + ' + ims if im > 0 else ' - ' + ims.lstrip('-'))


def a_cplx():
    k = R.randint(0, 5)
    a, b, c, d_ = [R.randint(-7, 7) for _ in range(4)]
    if b == 0 or d_ == 0: return False
    z, w = cstr(a, b), cstr(c, d_)
    if k == 0:
        s = cstr(a + c, b + d_)
        return add('alg', f"¿Cuánto es ({z}) + ({w})?", s, [cstr(a + c, b - d_), cstr(a - c, b + d_), cstr(a + c, b * d_), cstr(b + d_, a + c)], "Se suman partes reales entre sí y partes imaginarias entre sí.", 48 + (abs(a) + abs(c)) / 4)
    if k == 1:
        s = cstr(a * c - b * d_, a * d_ + b * c)
        return add('alg', f"¿Cuánto es ({z})({w})?", s, [cstr(a * c + b * d_, a * d_ + b * c), cstr(a * c, b * d_), cstr(a * c - b * d_, a * d_ - b * c), cstr(a * c - b * d_, b * c)], "Se distribuye y se usa i² = −1.", 62 + (abs(a) + abs(b) + abs(c) + abs(d_)) / 4)
    if k == 2:
        n = R.randint(2, 60)
        s = ['1', 'i', '-1', '-i'][n % 4]
        return add('alg', f"¿Cuánto vale i^{n}?", s, [x for x in ['1', 'i', '-1', '-i'] if x != s], "Las potencias de i se repiten cada 4: 1, i, −1, −i.", 52 + (n % 4) + n / 12)
    if k == 3:
        tr = R.choice([(3, 4, 5), (6, 8, 10), (5, 12, 13), (8, 15, 17)]); sg = R.choice([1, -1])
        return add('alg', f"¿Cuál es el módulo del número complejo {cstr(tr[0]*sg, tr[1])}?", tr[2], numwrong(tr[2], pos=True, extra=[tr[0] + tr[1], tr[2] * tr[2]]), f"|a + bi| = √(a² + b²) = {tr[2]}.", 60 + tr[2] / 4)
    if k == 4:
        return add('alg', f"¿Cuál es el conjugado de {z}?", cstr(a, -b), [cstr(-a, b), cstr(-a, -b), cstr(b, a), z.replace('+', '*') if False else cstr(a, b + 1)], "El conjugado cambia el signo de la parte imaginaria.", 46 + abs(a) / 4)
    p, qq = R.randint(-5, 5), R.randint(-5, 5)
    if qq == 0 or (c == 0 and d_ == 0): return False
    num = ((p + qq * 1j) * (c + d_ * 1j))
    nr, ni = int(round(num.real)), int(round(num.imag))
    return add('alg', f"¿Cuánto es ({cstr(nr, ni)}) / ({w})?", cstr(p, qq), [cstr(p, -qq), cstr(qq, p), cstr(-p, qq), cstr(p + 1, qq)], "Se multiplica numerador y denominador por el conjugado del denominador.", 80 + (abs(p) + abs(qq)) / 3)


def a_rad():
    k = R.randint(0, 2)
    if k == 0:
        a, m = R.randint(2, 9), R.choice([2, 3, 5, 6, 7, 10])
        return add('alg', f"Simplifica √{a*a*m}.", f"{a}√{m}", [f"{m}√{a}", f"{a*m}", f"√{a}·√{m*a}" if False else f"{a*a}√{m}", f"{a}√{m+1}"], f"√{a*a*m} = √({a*a}·{m}) = {a}√{m}.", 46 + a)
    if k == 1:
        a, b = R.choice([(2, 8), (3, 12), (2, 18), (5, 20), (2, 50), (3, 27), (6, 24), (2, 32), (7, 28)])
        s = int(math.isqrt(a * b))
        return add('alg', f"¿Cuánto es √{a} · √{b}?", s, numwrong(s, pos=True, extra=[a + b, a * b]), f"√{a}·√{b} = √{a*b} = {s}.", 46 + s / 3)
    a, b = R.randint(1, 9), R.choice([2, 3, 5, 7])
    return add('alg', f"Racionaliza el denominador de {a}/√{b}.", f"{a}√{b}/{b}", [f"{a}/{b}", f"{a}√{b}", f"√{b}/{a}", f"{a}√{b}/{b+1}"], f"Se multiplica arriba y abajo por √{b}.", 66 + b)


def a_rexp():
    b, p, q = R.choice([(4, 1, 2), (9, 1, 2), (8, 1, 3), (27, 1, 3), (8, 2, 3), (27, 2, 3), (16, 1, 4), (16, 3, 4), (25, 3, 2), (4, 3, 2), (9, 3, 2), (36, 1, 2), (64, 1, 3), (64, 2, 3), (125, 2, 3), (81, 3, 4), (32, 3, 5), (32, 2, 5)])
    s = round(b ** (p / q))
    return add('alg', f"¿Cuánto es {b}^({p}/{q})?", s, numwrong(s, pos=True, extra=[b * p // q if (b * p) % q == 0 else b + p, round(b ** (1 / q)) if round(b ** (1 / q)) != s else s + 1]), f"{b}^({p}/{q}) = ({q}-ésima raíz de {b})^{p} = {s}.", 56 + p * 3 + q * 2)


def a_expr():
    k = R.randint(0, 3)
    a, b = R.randint(2, 9), R.randint(2, 6)
    if k == 0:
        return add('alg', f"Simplifica x^{a} · x^{b}.", f"x^{a+b}", [f"x^{a*b}", f"x^{a-b}" if a != b else f"x^{a+1}", f"2x^{a+b}", f"x^{a+b+1}"], "Al multiplicar potencias de igual base se suman los exponentes.", 20 + a / 2, acc=[f"x{sup(a+b)}"])
    if k == 1:
        return add('alg', f"Simplifica (x^{a})^{b}.", f"x^{a*b}", [f"x^{a+b}", f"x^{a**b}" if a ** b != a * b else f"x^{a+b+1}", f"x^{a-b}" if a != b else f"x^{a+2}", f"{b}x^{a}"], "Una potencia de potencia multiplica los exponentes.", 24 + b)
    if k == 2:
        if a <= b: a, b = b + 1, a
        return add('alg', f"Simplifica x^{a} / x^{b}.", f"x^{a-b}", [f"x^{a+b}", f"x^{a*b}", f"x^{a//b if a % b == 0 else a+1}" if a // b != a - b else f"x^{a-b+1}", f"{a-b}x"], "Al dividir potencias de igual base se restan los exponentes.", 26 + a / 2)
    c = R.randint(2, 4)
    return add('alg', f"Simplifica ({c}x^{a})^{b}.", f"{c**b}x^{a*b}", [f"{c*b}x^{a*b}", f"{c}x^{a*b}", f"{c**b}x^{a+b}", f"{c**b}x^{a**b}" if a ** b != a * b else f"{c**b}x^{a*b+1}"], "Se eleva el coeficiente y se multiplican los exponentes.", 40 + c + b * 2)


def a_rem():
    a = R.randint(-4, 5)
    if a == 0: return False
    co = {3: 1, 2: R.randint(-5, 5), 1: R.randint(-6, 6), 0: R.randint(-9, 9)}
    s = peval(co, a)
    return add('alg', f"¿Cuál es el residuo de dividir {Q(co)} entre (x {'−' if a>0 else '+'} {abs(a)})?", nf(s), numwrong(s, extra=[nf(peval(co, -a))]), f"Por el teorema del residuo es P({a}) = {nf(s)}.", 70 + abs(a) + abs(s) / 25)


def a_factorth():
    a = R.choice([-3, -2, -1, 1, 2, 3, 4]); kk = R.randint(-7, 7)
    c = -a * a - kk * a
    if kk == 0 or c == 0: return False
    return add('alg', f"¿Para qué valor de k es (x {'−' if a>0 else '+'} {abs(a)}) un factor de {Q({2: 1, 1: kk, 0: c})}? Aquí el coeficiente de x es {kk} y el término independiente es {c}; con k = {kk} es factor. ¿Cuál es el valor de P({a}) cuando k = {kk}?", 0, [1, -1, c], "Si (x − a) es factor, P(a) = 0.", 72) if False else False


def a_rootfind():
    rs = R.sample([-4, -3, -2, -1, 1, 2, 3, 4, 5], 3)
    p = {3: 1, 2: -sum(rs), 1: rs[0] * rs[1] + rs[0] * rs[2] + rs[1] * rs[2], 0: -rs[0] * rs[1] * rs[2]}
    r = R.choice(rs)
    cands = [x for x in range(-6, 7) if x != 0 and peval(p, x) != 0]
    cands.sort(key=lambda x: abs(abs(x) - abs(r)))
    return add('alg', f"¿Cuál de estos valores es raíz de P(x) = {Q(p)}?", r, cands[:5], f"P({r}) = 0 al sustituir.", 82 + abs(r))


def a_word():
    k = R.randint(0, 5)
    if k == 0:
        x = R.randint(5, 20)
        return add('alg', f"Ana tiene el doble de la edad de Luis y juntos suman {3*x} años. ¿Cuántos años tiene Luis?", x, numwrong(x, pos=True, extra=[2 * x]), f"x + 2x = {3*x}, entonces x = {x}.", 30 + x / 3)
    if k == 1:
        w, extra = R.randint(3, 15), R.randint(2, 8)
        return add('alg', f"El largo de un rectángulo mide {extra} cm más que su ancho y su perímetro es {4*w+2*extra} cm. ¿Cuánto mide el ancho?", w, numwrong(w, pos=True, extra=[w + extra]), f"2(w + w + {extra}) = {4*w+2*extra}, entonces w = {w}.", 38 + w / 3)
    if k == 2:
        v, t = R.randint(30, 90), R.randint(2, 6)
        return add('alg', f"Un auto viaja a {v} km/h durante {t} horas. ¿Qué distancia recorre?", v * t, numwrong(v * t, pos=True, extra=[v + t]), f"d = v·t = {v}·{t} = {v*t} km.", 14 + t * 2)
    if k == 3:
        pr, n = R.randint(2, 15), R.randint(3, 12)
        return add('alg', f"Si {n} cuadernos cuestan {pr*n}, ¿cuánto cuestan {n+4} cuadernos?", pr * (n + 4), numwrong(pr * (n + 4), pos=True, extra=[pr * n + 4]), f"Cada cuaderno cuesta {pr}; {n+4}·{pr} = {pr*(n+4)}.", 16 + n / 2)
    if k == 4:
        b, h = R.randint(3, 20), R.randint(2, 15)
        return add('alg', f"¿Cuál es el área de un triángulo de base {b} cm y altura {2*h} cm?", b * h, numwrong(b * h, pos=True, extra=[b * 2 * h, b + 2 * h]), f"Área = base·altura/2 = {b}·{2*h}/2 = {b*h} cm².", 20 + b / 4)
    x = R.randint(3, 14); y = R.randint(2, 9)
    return add('alg', f"En un corral hay gallinas (2 patas) y conejos (4 patas): {x+y} animales en total y {2*x+4*y} patas. ¿Cuántos conejos hay?", y, numwrong(y, pos=True, extra=[x]), f"Con g + c = {x+y} y 2g + 4c = {2*x+4*y} se obtiene c = {y}.", 52 + x / 2)


def a_growth():
    k = R.randint(0, 2)
    if k == 0:
        p0, r, t = R.choice([100, 200, 500, 1000, 2000]), R.choice([5, 10, 20, 25]), R.randint(2, 3)
        s = F(p0) * F(100 + r, 100) ** t
        if s.denominator != 1: return False
        return add('alg', f"Una inversión de {p0} crece {r}% cada año (interés compuesto). ¿Cuánto hay después de {t} años?", nf(s), [nf(p0 + p0 * r * t // 100) if (p0 * r * t) % 100 == 0 else nf(s + 10), nf(F(p0) * F(100 + r, 100) ** (t + 1)) if False else nf(s + p0 * r // 100) if (p0 * r) % 100 == 0 else nf(s + 7), nf(F(p0) * r * t), nf(s - 15)],
                   f"Monto = P(1 + r)^t = {p0}·{nf(F(100+r,100))}^{t} = {nf(s)}.", 58 + t * 3 + r / 5)
    if k == 1:
        a0, n = R.choice([80, 160, 240, 320, 480, 640, 960]), R.randint(2, 5)
        s = F(a0, 2 ** n)
        if s.denominator != 1: return False
        return add('alg', f"Una sustancia de {a0} g reduce a la mitad su masa cada hora. ¿Cuántos gramos quedan después de {n} horas?", nf(s), numwrong(s, pos=True, extra=[a0 // 2 if n != 1 else 3, a0 - n * (a0 // 2)]), f"{a0}·(1/2)^{n} = {nf(s)}.", 48 + n * 2)
    a0, n = R.choice([3, 5, 7, 10, 25]), R.randint(2, 6)
    return add('alg', f"Un cultivo de {a0} bacterias duplica su cantidad cada hora. ¿Cuántas habrá después de {n} horas?", a0 * 2 ** n, numwrong(a0 * 2 ** n, pos=True, extra=[a0 * 2 * n, a0 + 2 * n]), f"{a0}·2^{n} = {a0*2**n}.", 46 + n * 3)


def a_func():
    k = R.randint(0, 4)
    a, b, c, d_ = R.randint(1, 5), R.randint(-6, 6), R.randint(1, 4), R.randint(-6, 6)
    if b == 0 or d_ == 0: return False
    if k == 0:
        x = R.randint(-4, 5)
        s = a * (c * x + d_) + b
        return add('alg', f"Si f(x) = {Q({1: a, 0: b})} y g(x) = {Q({1: c, 0: d_})}, ¿cuánto vale f(g({x}))?", s, numwrong(s, extra=[c * (a * x + b) + d_]), f"g({x}) = {c*x+d_}; f({c*x+d_}) = {s}.", 40 + abs(a) + abs(c))
    if k == 1:
        ans = f"(x {'+' if -b>0 else '-'} {abs(b)})/{a}" if a != 1 else f"x {'+' if -b>0 else '-'} {abs(b)}"
        if a == 1: return False
        return add('alg', f"¿Cuál es la función inversa de f(x) = {Q({1: a, 0: b})}?", ans, [f"(x {'-' if -b>0 else '+'} {abs(b)})/{a}", f"{a}x {'-' if b>0 else '+'} {abs(b)}", f"(x {'+' if -b>0 else '-'} {abs(b)})·{a}", f"{a}/(x {'+' if -b>0 else '-'} {abs(b)})"], "Se despeja x en y = ax + b y se intercambian las variables.", 58 + a * 2, acc=[ans.replace('(', '').replace(')', '') if False else ans])
    if k == 2:
        h = R.randint(-8, 8)
        if h == 0: return False
        return add('alg', f"¿Cuál es el dominio de f(x) = √(x {'−' if h>0 else '+'} {abs(h)})?", f"x ≥ {h}", [f"x ≤ {h}", f"x > {h}", f"x ≥ {-h}", f"x ≠ {h}"], "El radicando debe ser mayor o igual que cero.", 44 + abs(h) / 4, acc=[f"x>={h}", f"x >= {h}"])
    if k == 3:
        h = R.randint(-8, 8)
        if h == 0: return False
        return add('alg', f"¿Qué valor de x no pertenece al dominio de f(x) = 1/(x {'−' if h>0 else '+'} {abs(h)})?", h, [-h, 0, h + 1] if h != 0 else [1], "El denominador no puede ser cero.", 40 + abs(h) / 4)
    kk = R.randint(-9, 9)
    return add('alg', f"¿Cuál es el rango de f(x) = x² {'+' if kk>=0 else '−'} {abs(kk)}?", f"y ≥ {kk}", [f"y ≤ {kk}", f"y ≥ {-kk}", "Todos los reales", f"y > {kk}"], "x² es siempre ≥ 0, así que f(x) ≥ k.", 52 + abs(kk) / 4, acc=[f"y>={kk}", f"y >= {kk}"])


CONC_ALG = [
    ("En una expresión como 5x + 2, ¿cómo se llama el número 5?", "Coeficiente", ["Exponente", "Constante", "Variable"], "El coeficiente multiplica a la variable.", 6),
    ("¿Qué es una variable en álgebra?", "Un símbolo que representa un valor que puede cambiar", ["Un número que nunca cambia", "Una operación entre dos números", "El resultado de una suma"], "Las letras como x representan cantidades desconocidas o variables.", 3),
    ("¿Qué diferencia a una ecuación de una expresión algebraica?", "La ecuación tiene un signo igual", ["La ecuación no tiene letras", "La expresión siempre tiene un resultado", "No hay diferencia"], "Una ecuación afirma una igualdad.", 7),
    ("¿Qué propiedad dice que a + b = b + a?", "Conmutativa", ["Asociativa", "Distributiva", "Identidad"], "Conmutativa: el orden no altera la suma.", 4),
    ("¿Qué propiedad dice que a(b + c) = ab + ac?", "Distributiva", ["Conmutativa", "Asociativa", "Inverso"], "La multiplicación se distribuye sobre la suma.", 9),
    ("¿Qué propiedad dice que (a + b) + c = a + (b + c)?", "Asociativa", ["Conmutativa", "Distributiva", "Modulativa"], "La forma de agrupar no cambia el resultado.", 9),
    ("¿Cuál es el elemento neutro de la suma?", "0", ["1", "−1", "10"], "a + 0 = a.", 4),
    ("¿Cuál es el elemento neutro de la multiplicación?", "1", ["0", "−1", "10"], "a × 1 = a.", 5),
    ("¿Cuánto es cualquier número multiplicado por 0?", "0", ["El mismo número", "1", "No está definido"], "a × 0 = 0.", 2),
    ("¿Qué ocurre al dividir entre cero?", "No está definido", ["Da 0", "Da 1", "Da infinito exacto"], "La división entre cero no está definida en los reales.", 15),
    ("¿Cuál es el inverso aditivo de 7?", "−7", ["1/7", "7", "0"], "7 + (−7) = 0.", 6),
    ("¿Cuál es el inverso multiplicativo de 4?", "1/4", ["−4", "4", "0"], "4 × 1/4 = 1.", 10),
    ("¿Cómo se llama un polinomio con tres términos?", "Trinomio", ["Binomio", "Monomio", "Cuatrinomio"], "Tri = tres.", 13),
    ("¿Cómo se llama un polinomio con dos términos?", "Binomio", ["Trinomio", "Monomio", "Polinomio nulo"], "Bi = dos.", 10),
    ("¿Cuál es el grado del polinomio 3x⁴ + 2x − 1?", "4", ["3", "2", "5"], "El grado es el mayor exponente.", 18),
    ("¿Qué representa la gráfica de una función lineal?", "Una recta", ["Una parábola", "Una circunferencia", "Una hipérbola"], "y = mx + b es una recta.", 18),
    ("¿Qué forma tiene la gráfica de y = x²?", "Una parábola", ["Una recta", "Una hipérbola", "Una circunferencia"], "Es una función cuadrática.", 28),
    ("En y = mx + b, ¿qué representa m?", "La pendiente", ["La ordenada al origen", "El dominio", "La raíz"], "m mide la inclinación de la recta.", 25),
    ("¿Cuál es el valor absoluto de −9?", "9", ["−9", "0", "1/9"], "|−9| = 9.", 8),
    ("¿Qué significa que dos rectas sean perpendiculares?", "Se cortan formando un ángulo de 90°", ["Nunca se cortan", "Tienen la misma pendiente", "Coinciden"], "El producto de sus pendientes es −1.", 38),
    ("¿Qué son rectas paralelas?", "Rectas que nunca se cortan", ["Rectas que se cruzan en 90°", "Rectas con pendientes opuestas", "Rectas con igual ordenada"], "Tienen la misma pendiente.", 24),
    ("¿Qué es una raíz o cero de una función?", "Un valor de x donde f(x) = 0", ["El valor de f(0)", "El máximo de la función", "La pendiente"], "Es donde la gráfica corta el eje x.", 30),
    ("En el trinomio ax² + bx + c, ¿qué indica el signo de a?", "Si la parábola abre hacia arriba o hacia abajo", ["Si hay raíces reales", "La posición del vértice en y", "El grado del polinomio"], "a>0 abre hacia arriba; a<0 hacia abajo.", 54),
    ("Si el discriminante es negativo, ¿qué ocurre con las raíces reales?", "No existen", ["Hay dos distintas", "Hay una doble", "Hay tres"], "Δ<0 produce raíces complejas.", 46),
    ("¿Cuál es la fórmula general para ax² + bx + c = 0?", "x = (−b ± √(b² − 4ac)) / 2a", ["x = (b ± √(b² + 4ac)) / 2a", "x = −b / a", "x = (−b ± √(b² − 4ac)) / a"], "Es la fórmula cuadrática.", 55),
    ("¿Qué es el logaritmo de base b de x?", "El exponente al que se eleva b para obtener x", ["El producto de b por x", "La raíz b-ésima de x", "El doble de x"], "log_b(x) = y significa b^y = x.", 52),
    ("¿Cuánto vale log_b(1) para cualquier base b válida?", "0", ["1", "b", "No existe"], "Porque b⁰ = 1.", 50),
    ("¿Cuánto vale log_b(b)?", "1", ["0", "b", "−1"], "Porque b¹ = b.", 48),
    ("¿Qué propiedad cumple log(a·b)?", "log a + log b", ["log a · log b", "log a − log b", "(log a)/(log b)"], "El log de un producto es la suma de logs.", 55),
    ("¿Cómo se llama la unidad imaginaria i?", "La raíz cuadrada de −1", ["La raíz cuadrada de 1", "Igual a −1", "Igual a 0"], "i² = −1.", 50),
    ("¿Qué distingue a una progresión aritmética?", "La diferencia entre términos consecutivos es constante", ["El cociente entre términos consecutivos es constante", "Todos los términos son iguales", "Los términos son siempre pares"], "Se suma siempre el mismo número.", 32),
    ("¿Qué distingue a una progresión geométrica?", "El cociente entre términos consecutivos es constante", ["La diferencia entre términos consecutivos es constante", "Los términos son cuadrados", "Los términos siempre aumentan"], "Se multiplica siempre por el mismo número.", 36),
    ("¿Qué indica el teorema del residuo?", "El residuo de dividir P(x) entre (x − a) es P(a)", ["El residuo siempre es cero", "P(a) siempre es positivo", "El grado baja en 2"], "Evaluar el polinomio en a da el residuo.", 72),
    ("Al multiplicar ambos lados de una desigualdad por un número negativo, ¿qué ocurre?", "El sentido de la desigualdad se invierte", ["Se mantiene igual", "Se vuelve una igualdad", "Se anula"], "Por ejemplo 2 < 3, pero −2 > −3.", 33),
    ("¿Qué es una función inyectiva?", "Una función donde valores distintos de x dan valores distintos de y", ["Una función constante", "Una función con dominio vacío", "Una función que siempre es creciente"], "No repite imágenes.", 66),
    ("¿Cuál es el dominio de f(x) = x²?", "Todos los números reales", ["x ≥ 0", "x > 0", "x ≠ 0"], "No hay restricciones para elevar al cuadrado.", 30),
    ("¿Qué significa factorizar un polinomio?", "Escribirlo como producto de factores", ["Sumar sus términos", "Calcular su derivada", "Evaluarlo en cero"], "Es expresarlo como multiplicación.", 28),
    ("¿Qué significa simplificar una fracción algebraica?", "Dividir numerador y denominador por sus factores comunes", ["Sumar numerador y denominador", "Eliminar el denominador", "Elevar al cuadrado"], "Se cancelan factores comunes.", 40),
    ("¿Cuál es la identidad notable (a + b)²?", "a² + 2ab + b²", ["a² + b²", "a² − 2ab + b²", "a² + ab + b²"], "El doble producto no se puede olvidar.", 35),
    ("¿Cuál es la identidad notable (a + b)(a − b)?", "a² − b²", ["a² + b²", "a² − 2ab + b²", "2a − 2b"], "Diferencia de cuadrados.", 34),
    ("¿Qué indica el signo de la pendiente de una recta?", "Positiva: la recta sube; negativa: baja", ["Positiva: la recta baja", "Negativa: es vertical", "No indica nada"], "Se lee de izquierda a derecha.", 27),
    ("¿Cuál es la pendiente de una recta horizontal?", "0", ["1", "No está definida", "−1"], "No hay cambio vertical.", 22),
    ("¿Cuál es la pendiente de una recta vertical?", "No está definida", ["0", "1", "−1"], "El cambio en x es cero.", 30),
]


def a_conc():
    for q, c, w, e, d_ in CONC_ALG:
        add('alg', q, c, w, e, d_)


def build_alg():
    plan = [(a_sum, 22), (a_sub, 22), (a_mul, 36), (a_div, 26), (a_neg, 34), (a_order, 38), (a_pow, 46), (a_frac, 62), (a_fdec, 16), (a_pct, 34),
            (a_gcd, 24), (a_eval, 28), (a_eq1, 36), (a_eq2, 38), (a_eq3, 28), (a_eqp, 24), (a_eqf, 30), (a_like, 24), (a_expand, 46), (a_factor, 40),
            (a_quad, 46), (a_disc, 24), (a_irr, 22), (a_vertex, 24), (a_sumprod, 16), (a_line, 62), (a_sys2, 44), (a_sys3, 30), (a_ineq, 36), (a_abs, 24),
            (a_log, 40), (a_seq, 46), (a_inf, 10), (a_cplx, 46), (a_rad, 34), (a_rexp, 14), (a_expr, 30), (a_rem, 22), (a_rootfind, 12), (a_word, 36), (a_growth, 18), (a_func, 36)]
    for fn, n in plan: rep(n, fn)
    a_conc()


# ======================================================================= CÁLCULO
exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'gen_mat_calc.py'), encoding='utf-8').read())
exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'gen_mat_lin.py'), encoding='utf-8').read())
exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'gen_mat_est.py'), encoding='utf-8').read())


def main():
    build_alg()
    build_calc()
    build_lin()
    build_est()
    for cat in OUT:
        R.shuffle(OUT[cat])
        OUT[cat].sort(key=lambda r: r[5])
    here = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(here, 'out_mat.json'), 'w', encoding='utf-8') as f:
        json.dump(OUT, f, ensure_ascii=False, separators=(',', ':'))
    for cat, rows in OUT.items():
        ds = [r[5] for r in rows]
        print(cat, len(rows), 'd:', min(ds), '-', max(ds))
    print('total', sum(len(v) for v in OUT.values()))


if __name__ == '__main__':
    main()
