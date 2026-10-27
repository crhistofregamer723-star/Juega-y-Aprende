# -*- coding: utf-8 -*-
import math
import sympy as sp
from lib import *

X = sp.Symbol("x")

def xs(v): return f"x = {num(v)}"

# ---------- familias paramétricas ----------
def f_eval(r, t):
    if t < 0.5:
        a = r.randint(2, sc(t, 5, 9)); b = r.randint(1, sc(t, 9, 20)); k = r.randint(1, sc(t, 6, 9)); s = r.choice([1, -1])
        e = poly([a, s * b]); v = a * k + s * b
        q = r.choice([f"Si x = {k}, ¿cuánto vale {e}?", f"Evalúa {e} cuando x = {k}.", f"¿Qué valor toma {e} si x vale {k}?"])
        w = nw(r, v, a * k - s * b, a + k + s * b, a * (k + s * b))
        ex = f"Se sustituye x = {k}: {a}·{k} {'+' if s>0 else '−'} {b} = {v}."
    else:
        a = r.randint(1, 4); b = r.randint(-6, 6); c = r.randint(-9, 9); k = r.randint(-4, -1)
        e = poly([a, b, c]); v = a * k * k + b * k + c
        q = r.choice([f"Evalúa {e} cuando x = {num(k)}.", f"Si x = {num(k)}, ¿cuánto vale {e}?"])
        w = nw(r, v, -a * k * k + b * k + c, a * k * k - b * k + c, a * k * k + b * k - c)
        ex = f"Al sustituir x = {num(k)} el cuadrado es positivo: {a}·{k*k} + ({b})·({k}) + ({c}) = {v}."
    return mk(q, num(v), w, ex)

def f_order(r, t):
    if t < 0.35:
        a, b, c, d = r.randint(1, 9), r.randint(2, 9), r.randint(2, 9), r.randint(1, 9)
        q = f"¿Cuánto vale {a} + {b}·{c} − {d}?"; v = a + b * c - d
        w = nw(r, v, (a + b) * c - d, a + b * (c - d)); ex = "Primero se multiplica y luego se suma y resta: " + f"{a} + {b*c} − {d} = {v}."
    elif t < 0.7:
        a, b, c, d = r.randint(2, 6), r.randint(5, 12), r.randint(1, 4), r.randint(2, 5)
        q = f"Calcula {a}·({b} − {c}) + {d}²."; v = a * (b - c) + d * d
        w = nw(r, v, a * b - c + d * d, a * (b - c) + 2 * d, a * (b - c + d) ** 2 if False else a * (b - c) + d)
        ex = f"Paréntesis: {b-c}; potencia: {d*d}; luego {a}·{b-c} + {d*d} = {v}."
    else:
        a, b, c = r.randint(2, 6), r.randint(2, 6), r.randint(2, 6)
        q = f"¿Cuánto vale −{a}² + {b}·(−{c})?"; v = -a * a - b * c
        w = nw(r, v, a * a - b * c, -a * a + b * c, a * a + b * c)
        ex = f"−{a}² es −{a*a} (el signo no se eleva) y {b}·(−{c}) = −{b*c}; total {v}."
    return mk(q, num(v), w, ex)

def f_onestep(r, t):
    k = r.randint(2, sc(t, 9, 30)); v = r.randint(2, sc(t, 12, 40)); typ = r.choice("sraqd")
    if typ == "s":
        q = f"Resuelve x + {k} = {v+k}."; w = nw(r, v, v + 2 * k, v + k + k + 1 if False else v - k)
        ex = f"Se resta {k} a ambos lados: x = {v+k} − {k} = {v}."
    elif typ == "r":
        q = f"Resuelve x − {k} = {v}."; ans = v + k; w = nw(r, ans, v - k, k - v)
        ex = f"Se suma {k} a ambos lados: x = {v} + {k} = {ans}."; v = ans
    elif typ == "a":
        q = f"Resuelve {k}x = {k*v}."; w = nw(r, v, k * v - k, k * v + k, k * v * k)
        ex = f"Se divide entre {k} ambos lados: x = {k*v}/{k} = {v}."
    elif typ == "q":
        q = f"Resuelve x/{k} = {v}."; ans = k * v; w = nw(r, ans, v - k, v // 1 + k, F(v, k))
        ex = f"Se multiplica por {k} ambos lados: x = {v}·{k} = {ans}."; v = ans
    else:
        q = r.choice([f"¿Qué valor de x cumple {k} + x = {k+v}?", f"¿Cuál es el valor de x en x + {k} = {k+v}?"])
        w = nw(r, v, k + v + k, k + v); ex = f"x = {k+v} − {k} = {v}."
    return mk(q, xs(v), [f"x = {w_}" for w_ in w], ex, extra=[str(v)])

def f_twostep(r, t):
    a = rnz(r, -sc(t, 5, 12), sc(t, 5, 12)) if t > 0.4 else r.randint(2, 6)
    v = rnz(r, -sc(t, 5, 10), sc(t, 7, 12)); b = rnz(r, -sc(t, 9, 25), sc(t, 9, 25))
    typ = r.choice("abc") if t > 0.5 else r.choice("ab")
    if typ == "a":
        c = a * v + b
        q = f"Resuelve {poly([a, b])} = {num(c)}."
        w = nw(r, v, F(c + b, a), F(c, a) - b, c - b - a if False else F(c - b, -a))
        ex = f"Se resta {num(b)} y se divide entre {a}: x = ({num(c)} − ({num(b)}))/{a} = {v}."
    elif typ == "b":
        c = a * (v + b)
        q = f"Resuelve {num(a)}(x + {b}) = {c}." if b > 0 else f"Resuelve {num(a)}(x − {abs(b)}) = {c}."
        w = nw(r, v, F(c, a) + b, c - b, F(c, a))
        ex = f"Se divide entre {num(a)}: x {'+' if b>0 else '−'} {abs(b)} = {num(F(c,a))}, así x = {v}."
    else:
        d = rnz(r, -9, 9) ; m = rnz(r, 2, 6)
        c = v * a // 1  # x/m + d = c  -> choose v multiple of m
        v = m * v; c = v // m + d
        q = f"Resuelve x/{m} + ({num(d)}) = {num(c)}." if d < 0 else f"Resuelve x/{m} + {d} = {num(c)}."
        w = nw(r, v, m * (c + d), c - d, F(c - d, m))
        ex = f"Se pasa {num(d)} restando: x/{m} = {num(c-d)} y se multiplica por {m}: x = {v}."
    return mk(q, xs(v), [f"x = {w_}" for w_ in w], ex, extra=[num(v)])

def f_bothsides(r, t):
    a = r.randint(2, sc(t, 6, 12)); c = r.randint(-sc(t, 4, 9), a - 1); 
    if c == a: c = a - 1
    v = rnz(r, -sc(t, 6, 10), sc(t, 8, 12)); b = r.randint(-12, 12)
    d = a * v + b - c * v
    q = f"Resuelve {poly([a, b])} = {poly([c, d])}."
    w = nw(r, v, F(d + b, a - c), F(d - b, a + c), F(b - d, a - c))
    ex = f"Se agrupan las x: ({a} − {num(c)})x = {num(d)} − ({num(b)}), de donde x = {v}."
    return mk(q, xs(v), [f"x = {w_}" for w_ in w], ex, extra=[num(v)])

def f_expnum(r, t):
    typ = r.choice("pnzmr") if t > 0.4 else r.choice("pnm")
    if typ == "p":
        b, e = r.randint(2, sc(t, 5, 9)), r.randint(2, sc(t, 5, 4 if False else 6)); v = b ** e
        q = f"¿Cuánto vale {b}{sup(e)}?"; w = nw(r, v, b * e, b ** (e - 1), b ** (e + 1)); ex = f"Es {b} multiplicado por sí mismo {e} veces: {big(v)}."
        return mk(q, big(v), [big(int(F(x))) if '/' not in x else x for x in w] , ex)
    if typ == "m":
        b = r.randint(2, 5); e = r.choice([2, 3, 4]); v = (-b) ** e
        q = f"¿Cuánto vale (−{b}){sup(e)}?"; w = nw(r, v, -v, -b * e, b * e); ex = f"Hay {e} factores negativos; el resultado es {'positivo' if e%2==0 else 'negativo'}: {num(v)}."
        return mk(q, num(v), w, ex)
    if typ == "n":
        b, e = r.randint(2, 6), r.choice([2, 4]); v = -(b ** e)
        q = f"¿Cuánto vale −{b}{sup(e)}?"; w = nw(r, v, b ** e, b * e, -b * e); ex = f"La potencia se aplica solo al {b}, y luego se pone el signo: −{b**e}."
        return mk(q, num(v), w, ex)
    if typ == "z":
        b = r.randint(2, 99); q = f"¿Cuánto vale {b}⁰?"; ex = "Todo número distinto de cero elevado a 0 es 1."
        return mk(q, "1", ["0", str(b), "No está definido"], ex)
    b, e = r.randint(2, 5), r.randint(1, 4); v = F(1, b ** e)
    q = f"¿Cuánto vale {b}{sup(-e)}?"; w = nw(r, v, -b ** e, F(-1, b ** e) if False else -e * b, b ** e, F(1, b * e)); ex = f"Un exponente negativo invierte la base: {b}⁻{e} = 1/{b**e}."
    return mk(q, num(v), w, ex)

def mono(c, e, v="x"):
    if e == 0: return num(c)
    return ("" if c == 1 else "−" if c == -1 else num(c)) + v + (sup(e) if e != 1 else "")

def f_exprules(r, t):
    typ = r.choice("mdpq") if t < 0.5 else r.choice("pqnd")
    if typ == "m":
        a, b = r.randint(2, sc(t, 6, 9)), r.randint(2, sc(t, 6, 9))
        q = f"Simplifica x{sup(a)} · x{sup(b)}."; ans = f"x{sup(a+b)}"; w = [f"x{sup(a*b)}", f"x{sup(a)}{sup(b)}" if False else f"2x{sup(a+b)}", f"x{sup(abs(a-b)) if a!=b else 2}"]
        ex = "Al multiplicar potencias de igual base se suman los exponentes."
    elif typ == "d":
        a, b = r.randint(4, 9), r.randint(1, 3); q = f"Simplifica x{sup(a)} / x{sup(b)}."; ans = f"x{sup(a-b)}" if a - b != 1 else "x"
        w = [f"x{sup(a+b)}", f"x{sup(a*b)}" if a * b != a - b else "x0", f"x{sup(F(a,b).numerator) if a%b==0 else a-b+1}"]
        ex = "Al dividir potencias de igual base se restan los exponentes."
    elif typ == "p":
        a, b = r.randint(2, 4), r.randint(2, 5); q = f"Simplifica (x{sup(a)}){sup(b)}."; ans = f"x{sup(a*b)}"
        w = [f"x{sup(a+b)}", f"x{sup(a**b)}" if a ** b != a * b else "x1", f"x{sup(a)}{b}" if False else f"{b}x{sup(a)}"]
        ex = "Una potencia de potencia multiplica los exponentes."
    elif typ == "q":
        a, b, c = r.randint(2, 4), r.randint(2, 4), r.randint(2, 3); k = r.randint(2, 3)
        q = f"Simplifica ({k}x{sup(a)}y{sup(b)}){sup(c)}."; ans = f"{k**c}x{sup(a*c)}y{sup(b*c)}"
        w = [f"{k*c}x{sup(a*c)}y{sup(b*c)}", f"{k**c}x{sup(a+c)}y{sup(b+c)}", f"{k}x{sup(a*c)}y{sup(b*c)}"]
        ex = f"El exponente {c} afecta al coeficiente {k} y a cada variable: {k}{sup(c)} = {k**c}."
    else:
        a, b = r.randint(2, 6), r.randint(2, 6)
        q = f"Simplifica x{sup(a)} · x{sup(-b)}."; e = a - b; ans = (f"x{sup(e)}" if e not in (0, 1) else ("1" if e == 0 else "x"))
        w = [f"x{sup(a+b)}", f"x{sup(-a*b)}", f"x{sup(b-a)}" if b - a not in (0, 1) else "x2"]
        ex = "Se suman los exponentes: a + (−b) = a − b."
        if e == 0: return f_exprules(r, t)
    return mk(q, ans, w, ex, extra=[ascii_var(ans)])

def f_fractions(r, t):
    op = r.choice("+−·÷") if t > 0.4 else r.choice("+−")
    while True:
        b, d = r.randint(2, sc(t, 6, 12)), r.randint(2, sc(t, 6, 12)); a, c = r.randint(1, b + 3), r.randint(1, d + 3)
        if math.gcd(a, b) == 1 and math.gcd(c, d) == 1 and b != d: break
    x, y = F(a, b), F(c, d)
    v = {"+": x + y, "−": x - y, "·": x * y, "÷": x / y}[op]
    q = r.choice([f"¿Cuánto es {a}/{b} {op} {c}/{d}?", f"Calcula {a}/{b} {op} {c}/{d} y simplifica."])
    mist = {"+": F(a + c, b + d), "−": F(a - c, b - d) if b != d else 0, "·": F(a * d, b * c), "÷": F(a * c, b * d)}[op]
    w = nw(r, v, mist, {"+": x * y, "−": y - x, "·": x + y, "÷": y / x}[op])
    ex = {"+": "Se usa común denominador y se suman los numeradores.", "−": "Se usa común denominador y se restan los numeradores.", "·": "Se multiplican numeradores entre sí y denominadores entre sí.", "÷": "Dividir es multiplicar por el inverso de la segunda fracción."}[op]
    return mk(q, num(v), w, ex)

def f_slope(r, t):
    x1, y1 = r.randint(-sc(t, 4, 8), sc(t, 4, 8)), r.randint(-6, 6)
    dx = rnz(r, -sc(t, 3, 6), sc(t, 4, 7)); m = F(rnz(r, -4, 4), r.choice([1, 1, 2]) if t > .5 else 1)
    dy = m * dx
    if dy.denominator != 1: dx *= 2; dy = m * dx
    x2, y2 = x1 + dx, y1 + int(dy)
    q = r.choice([f"¿Cuál es la pendiente de la recta que pasa por ({x1}, {y1}) y ({x2}, {y2})?".replace("(-", "(−"), f"Halla la pendiente del segmento entre ({x1}, {y1}) y ({x2}, {y2}).".replace("(-", "(−")])
    q = q.replace(", -", ", −")
    w = nw(r, m, -m, F(1, 1) / m if m != 0 else 5, F(x2 - x1, y2 - y1) if y2 != y1 else 0)
    ex = f"m = (y₂ − y₁)/(x₂ − x₁) = ({y2} − ({y1}))/({x2} − ({x1})) = {num(m)}."
    return mk(q, num(m), w, ex)

def f_lineeq(r, t):
    typ = r.choice("abcd")
    m = rnz(r, -5, 5); b = r.randint(-9, 9)
    if typ == "a":
        q = f"¿Cuál es la ecuación de la recta con pendiente {num(m)} que corta al eje y en {num(b)}?"
        ans = lin_str(m, b); w = [lin_str(m, -b) if b else lin_str(-m, b), lin_str(b, m) if b != m else lin_str(m, 1), lin_str(-m, b)]
        ex = "Es la forma pendiente-ordenada y = mx + b con m = " + num(m) + " y b = " + num(b) + "."
    elif typ == "b":
        x1 = r.randint(-4, 4); x2 = x1 + rnz(r, -4, 4); y1 = m * x1 + b; y2 = m * x2 + b
        q = f"¿Cuál es la ecuación de la recta que pasa por ({num(x1)}, {num(y1)}) y ({num(x2)}, {num(y2)})?"
        ans = lin_str(m, b); w = [lin_str(m, -b) if b else lin_str(m, 1), lin_str(-m, b) if b else lin_str(-m, 2), lin_str(m, y1)]
        ex = f"La pendiente es {num(m)}; con el punto ({num(x1)}, {num(y1)}) se obtiene b = {num(b)}."
    elif typ == "c":
        x1 = r.randint(-4, 4); y1 = r.randint(-6, 6); bb = y1 - m * x1; b0 = r.randint(-5, 5)
        q = f"¿Cuál es la recta paralela a {lin_str(m, b0)} que pasa por ({num(x1)}, {num(y1)})?"
        ans = lin_str(m, bb); w = [lin_str(F(-1, m), y1 + x1 * F(1, m)) if False else lin_str(-m, y1 + m * x1), lin_str(m, b0), lin_str(m, y1 + m * x1)]
        ex = f"Una recta paralela conserva la pendiente {num(m)}; con el punto dado b = {num(bb)}."
    else:
        q = f"Una recta tiene pendiente {num(m)}. ¿Cuál es la pendiente de una recta perpendicular a ella?"
        ans = num(F(-1, 1) / m); w = [num(m), num(-m), num(F(1, 1) / m)]
        ex = "Las pendientes de rectas perpendiculares cumplen m₁·m₂ = −1, así que m₂ = −1/m."
    return mk(q, ans, w, ex)

def f_expand(r, t):
    typ = r.choice("abcd") if t > 0.4 else r.choice("abc")
    a, b = rnz(r, -sc(t, 5, 9), sc(t, 5, 9)), rnz(r, -sc(t, 5, 9), sc(t, 5, 9))
    def s(c): return f"x + {c}" if c > 0 else f"x − {abs(c)}"
    if typ == "a":
        e = sp.Poly(sp.expand((X + a) * (X + b)), X).all_coeffs(); q = f"Desarrolla ({s(a)})({s(b)})."
        ans = poly(e); w = [poly([1, a + b, 0 if False else a * b + 1]), poly([1, a - b if a != b else a + b + 1, a * b]), poly([1, a * b, a + b])]
        ex = "Se distribuye cada término: x² + (a + b)x + ab."
    elif typ == "b":
        e = sp.Poly(sp.expand((X + a) ** 2), X).all_coeffs(); q = f"Desarrolla ({s(a)})²."
        ans = poly(e); w = [poly([1, 0, a * a]), poly([1, a, a * a]), poly([1, 2 * a, -a * a])]
        ex = f"(x + a)² = x² + 2ax + a², aquí con a = {num(a)}."
    elif typ == "c":
        a = abs(a); e = sp.Poly(sp.expand((X + a) * (X - a)), X).all_coeffs(); q = f"Desarrolla (x + {a})(x − {a})."
        ans = poly(e); w = [poly([1, 0, a * a]), poly([1, -2 * a, a * a]), poly([1, 2 * a, a * a])]
        ex = "Es suma por diferencia: x² − a²; los términos centrales se cancelan."
    else:
        m, n = r.randint(2, 4), r.randint(2, 3)
        e = sp.Poly(sp.expand((m * X + a) * (n * X + b)), X).all_coeffs(); q = f"Desarrolla ({m}x {'+' if a>0 else '−'} {abs(a)})({n}x {'+' if b>0 else '−'} {abs(b)})."
        ans = poly(e); w = [poly([m * n, a * m + b * n if False else m * b + n * a + 1, a * b]), poly([m * n, m * b - n * a, a * b]), poly([m * n, m * b + n * a, -a * b])]
        ex = f"Primeros: {m*n}x²; centrales: {m}·{num(b)}x + {n}·{num(a)}x; últimos: {num(a*b)}."
    return mk(q, ans, w, ex)

def f_factor(r, t):
    typ = r.choice("abcd") if t > 0.45 else "a"
    if typ == "a":
        p, qq = rnz(r, -sc(t, 5, 9), sc(t, 5, 9)), rnz(r, -sc(t, 5, 9), sc(t, 5, 9))
        e = poly([1, p + qq, p * qq]); f = lambda k: f"(x {'+' if k>0 else '−'} {abs(k)})"
        q = r.choice([f"Factoriza {e}.", f"¿Cómo se factoriza {e}?"]); ans = f(p) + f(qq)
        w = [f(-p) + f(-qq), f(p) + f(-qq) if p != -qq else f(p + 1) + f(qq), f(p + qq) + "x" if False else f(p * qq) + f(1)]
        ex = f"Se buscan dos números con suma {num(p+qq)} y producto {num(p*qq)}: {num(p)} y {num(qq)}."
        return mk(q, ans, w, ex, extra=[f(qq) + f(p)])
    if typ == "b":
        m, n = r.randint(1, 3), r.randint(1, 3); p, qq = rnz(r, -5, 5), rnz(r, -5, 5)
        if m == 1 and n == 1: m = 2
        e = poly([m * n, m * qq + n * p, p * qq]); f = lambda a, k: f"({'' if a==1 else a}x {'+' if k>0 else '−'} {abs(k)})"
        ans = f(m, p) + f(n, qq); w = [f(m, qq) + f(n, p), f(m, -p) + f(n, -qq), f(m, p) + f(n, -qq)]
        if m * qq == n * p and False: pass
        q = f"Factoriza {e}."; ex = f"Se prueba con factores de {m*n} y de {num(p*qq)} hasta que el término central sea {num(m*qq+n*p)}x."
        return mk(q, ans, w, ex, extra=[f(n, qq) + f(m, p)])
    if typ == "c":
        k = r.randint(2, 12); q = f"Factoriza x² − {k*k}."; ans = f"(x − {k})(x + {k})"
        w = [f"(x − {k})²", f"(x + {k})²", f"(x − {k*k})(x + 1)"]; ex = "Es una diferencia de cuadrados: a² − b² = (a − b)(a + b)."
        return mk(q, ans, w, ex, extra=[f"(x + {k})(x − {k})"])
    a, b = r.randint(2, 6), r.randint(2, 6)
    q = f"Saca el factor común de {a*b}x² + {a*(b+1)}x."; ans = f"{a}x({b}x + {b+1})"
    w = [f"{a*b}x({a}x + {b+1})", f"x({a*b}x + {a*(b+1)})", f"{a}({b}x² + {b+1}x)"]
    ex = f"El máximo factor común es {a}x; al dividir cada término queda {b}x + {b+1}."
    return mk(q, ans, w, ex, acc=[ans])

def sol_pair(p, q_):
    a, b = sorted([p, q_]); return a, b

def f_quadroots(r, t):
    p, qq = sol_pair(rnz(r, -sc(t, 5, 9), sc(t, 5, 9)), rnz(r, -sc(t, 5, 9), sc(t, 5, 9)))
    typ = "v" if r.random() < 0.3 else "r"
    if typ == "r":
        if p == qq:
            q = f"Resuelve {poly([1, -2 * p, p * p])} = 0."; ans = xs(p); w = [xs(-p), f"x = {num(p)} y x = {num(-p)}", xs(p * p)]
            return mk(q, ans, w, f"Es el cuadrado (x − {num(p)})² = 0, con una sola solución (raíz doble).", extra=[num(p)])
        q = r.choice([f"Resuelve {poly([1, -(p+qq), p*qq])} = 0.", f"¿Cuáles son las soluciones de {poly([1, -(p+qq), p*qq])} = 0?"])
        ans = f"x = {num(p)} y x = {num(qq)}"; w = [f"x = {num(-p)} y x = {num(-qq)}", f"x = {num(p+1)} y x = {num(qq-1)}" if (p + 1, qq - 1) not in ((p, qq), (qq, p)) else f"x = {num(p)} y x = {num(-qq)}", f"x = {num(p)} y x = {num(-qq)}" if p != -qq and p != qq else "x = 0 y x = 1"]
        ex = f"Se factoriza (x − ({num(p)}))(x − ({num(qq)})) = 0, y cada factor da una raíz."
        return mk(q, ans, w, ex, extra=[f"{num(p)} y {num(qq)}", f"{num(p)}, {num(qq)}", f"x = {num(p)}, x = {num(qq)}", f"x={num(p)}, x={num(qq)}", f"x = {num(p)} o x = {num(qq)}"])
    q = r.choice([f"¿Cuánto suman las raíces de {poly([1, -(p+qq), p*qq])} = 0?", f"¿Cuánto vale el producto de las raíces de {poly([1, -(p+qq), p*qq])} = 0?"])
    if "suman" in q:
        v = p + qq; w = nw(r, v, -v, p * qq); ex = "Por Vieta, la suma de las raíces es −b/a."
    else:
        v = p * qq; w = nw(r, v, -v, p + qq); ex = "Por Vieta, el producto de las raíces es c/a."
    return mk(q, num(v), w, ex)

def f_disc(r, t):
    a = rnz(r, -3, 4); b = rnz(r, -9, 9); c = rnz(r, -8, 8); D = b * b - 4 * a * c
    e = poly([a, b, c])
    if r.random() < 0.5:
        q = f"¿Cuánto vale el discriminante de {e}?"
        w = nw(r, D, b * b + 4 * a * c, -b * b - 4 * a * c, b * b - 2 * a * c)
        return mk(q, num(D), w, f"Δ = b² − 4ac = {b*b} − 4·({a})·({c}) = {D}.")
    q = r.choice([f"¿Cuántas soluciones reales tiene {e} = 0?", f"Según su discriminante, ¿cuántas raíces reales tiene {e} = 0?"])
    ans = "Dos distintas" if D > 0 else "Una (doble)" if D == 0 else "Ninguna"
    w = [o for o in ["Dos distintas", "Una (doble)", "Ninguna", "Infinitas"] if o != ans]
    return mk(q, ans, w, f"El discriminante es {D}: {'positivo, dos raíces' if D>0 else 'cero, una raíz doble' if D==0 else 'negativo, sin raíces reales'}.", acc=[ans] + ({"Dos distintas": ["2", "dos"], "Una (doble)": ["1", "una"], "Ninguna": ["0", "ninguna", "cero"]}[ans]))

def f_vertex(r, t):
    a = rnz(r, -4, 4); h = rnz(r, -6, 6); k = rnz(r, -9, 9)
    b = -2 * a * h; c = a * h * h + k; e = poly([a, b, c])
    typ = r.choice("pxk")
    if typ == "p":
        q = f"¿Cuál es el vértice de la parábola y = {e}?"; ans = f"({num(h)}, {num(k)})"
        w = [f"({num(-h)}, {num(k)})", f"({num(h)}, {num(-k)})", f"({num(h)}, {num(c)})"]
        ex = f"x = −b/2a = {num(h)}; al sustituir, y = {num(k)}."
        return mk(q, ans, w, ex, extra=[f"{num(h)},{num(k)}"])
    if typ == "x":
        q = f"¿En qué valor de x alcanza su extremo la parábola y = {e}?"; w = nw(r, h, -h, b, F(b, a) if h != F(b, a) else 7)
        return mk(q, num(h), w, f"x = −b/2a = {num(-b)}/{2*a} = {num(h)}.")
    q = f"¿Cuál es el valor {'mínimo' if a>0 else 'máximo'} de y = {e}?"; w = nw(r, k, -k, c, h)
    return mk(q, num(k), w, f"Con a {'>' if a>0 else '<'} 0 la parábola abre hacia {'arriba' if a>0 else 'abajo'}; en x = {num(h)} el valor es {num(k)}.")

def f_system(r, t):
    while True:
        x, y = rnz(r, -sc(t, 4, 8), sc(t, 5, 9)), rnz(r, -sc(t, 4, 8), sc(t, 5, 9))
        a1, b1, a2, b2 = [r.randint(1, sc(t, 2, 5)) * r.choice([1, -1] if t > .4 else [1]) for _ in range(4)]
        if a1 * b2 - a2 * b1 != 0 and x != y: break
    c1, c2 = a1 * x + b1 * y, a2 * x + b2 * y
    def eq(a, b, c): return f"{poly([a, 0])[:-0 or None] if False else ''}{'' if a==1 else '−' if a==-1 else a}x {'+' if b>0 else '−'} {'' if abs(b)==1 else abs(b)}y = {num(c)}"
    q = r.choice([f"Resuelve el sistema {eq(a1,b1,c1)}, {eq(a2,b2,c2)}.", f"¿Cuál es la solución del sistema {eq(a1,b1,c1)} y {eq(a2,b2,c2)}?"])
    ans = f"x = {num(x)} y y = {num(y)}"
    cands = [(y, x), (-x, y), (x, -y), (x + 1, y), (x, y + 1)]
    w = []
    for (u, v) in cands:
        assert not (a1 * u + b1 * v == c1 and a2 * u + b2 * v == c2)
        w.append(f"x = {num(u)} y y = {num(v)}")
    ex = f"Por sustitución o eliminación se obtiene x = {num(x)}, y = {num(y)}; al reemplazar se verifican ambas ecuaciones."
    return mk(q, ans, w, ex, extra=[f"({num(x)}, {num(y)})", f"{num(x)}, {num(y)}", f"x={num(x)}, y={num(y)}", f"x = {num(x)}, y = {num(y)}"])

def f_ineq(r, t):
    typ = r.choice("abc") if t > 0.4 else r.choice("ab")
    op = r.choice(["<", ">", "≤", "≥"]); flip = {"<": ">", ">": "<", "≤": "≥", "≥": "≤"}
    v = rnz(r, -sc(t, 5, 9), sc(t, 6, 10))
    if typ == "a":
        a = r.randint(2, 6); b = r.randint(-9, 9); c = a * v + b
        q = f"Resuelve {poly([a, b])} {op} {num(c)}."; ans = f"x {op} {num(v)}"; w = [f"x {flip[op]} {num(v)}", f"x {op} {num(F(c+b, a))}", f"x {flip[op]} {num(F(c+b, a))}"]
        ex = f"Se resta {num(b)} y se divide entre {a} (positivo): x {op} {num(v)}."
    elif typ == "b":
        a = -r.randint(2, 6); b = r.randint(-9, 9); c = a * v + b
        q = f"Resuelve {poly([a, b])} {op} {num(c)}."; ans = f"x {flip[op]} {num(v)}"; w = [f"x {op} {num(v)}", f"x {op} {num(F(c+b, a)*-1)}", f"x {flip[op]} {num(F(c+b, -a))}"]
        ex = f"Al dividir entre {a} (negativo) el sentido se invierte: x {flip[op]} {num(v)}."
    else:
        a = r.randint(2, 4); b = r.randint(-5, 5); lo = a * v + b; hi = lo + a * r.randint(2, 6); u = F(hi - b, a)
        q = f"Resuelve {num(lo)} < {poly([a, b])} ≤ {num(hi)}."; ans = f"{num(v)} < x ≤ {num(u)}"
        w = [f"{num(v)} ≤ x < {num(u)}", f"{num(lo)} < x ≤ {num(hi)}", f"{num(u)} < x ≤ {num(v)}"]
        ex = f"Se resta {num(b)} y se divide entre {a} en los tres miembros."
    return mk(q, ans, w, ex)

def f_abs(r, t):
    typ = "e" if r.random() < 0.6 else "d"
    a = r.randint(1, 4); v1 = rnz(r, -8, 8); c = r.randint(1, 6) * a
    if typ == "e":
        b = -a * v1 + 0; b = r.randint(-8, 8); h = F(c, a); p = (-b + c) / F(a); qq = (-b - c) / F(a)
        if (-b + c) % a: b = a * r.randint(-5, 5)
        p = F(-b + c, a); qq = F(-b - c, a); p, qq = sorted([p, qq])
        e = poly([a, b]); q = f"Resuelve |{e}| = {c}."; ans = f"x = {num(p)} o x = {num(qq)}"
        w = [f"Solo x = {num(qq)}", f"x = {num(-p)} o x = {num(-qq)}" if p != -qq else f"x = {num(p)}", f"x = {num(F(c - b, a))} o x = {num(F(-c + b, a))}"]
        ex = f"Se separan los casos {e} = {c} y {e} = {-c}."
        return mk(q, ans, w, ex, extra=[f"{num(p)} y {num(qq)}", f"{num(p)}, {num(qq)}", f"x = {num(p)} y x = {num(qq)}"])
    k = r.randint(2, 7); h = rnz(r, -6, 6)
    q = f"Resuelve |x {'−' if h>0 else '+'} {abs(h)}| < {k}."; ans = f"{num(h-k)} < x < {num(h+k)}"
    w = [f"x < {num(h-k)} o x > {num(h+k)}", f"{num(-h-k)} < x < {num(-h+k)}", f"x < {num(h+k)}"]
    return mk(q, ans, w, f"|x − ({num(h)})| < {k} equivale a {num(h)} − {k} < x < {num(h)} + {k}.")

def f_logs(r, t):
    typ = r.choice("abcde")
    if typ == "a":
        b = r.choice([2, 3, 4, 5, 10]); e = r.randint(1, 5 if b < 5 else 3); n = b ** e
        q = f"¿Cuánto vale log{sub(b)} {big(n)}?" if b != 10 else f"¿Cuánto vale log {big(n)} (base 10)?"
        w = nw(r, e, n // b, e + 1, b); ex = f"{b}{sup(e)} = {big(n)}, por lo tanto el logaritmo es {e}."
        return mk(q, str(e), w, ex, extra=[["cero","uno","dos","tres","cuatro","cinco"][e]])
    if typ == "b":
        b = r.choice([2, 3, 5]); e = r.randint(1, 4); q = f"¿Cuánto vale log{sub(b)}(1/{b**e})?"; v = -e
        w = nw(r, v, e, F(1, e), -b ** e); return mk(q, num(v), w, f"1/{b**e} = {b}{sup(-e)}, entonces el logaritmo es −{e}.")
    if typ == "c":
        b = r.choice([2, 3]); m, n = r.randint(1, 4), r.randint(1, 4); q = f"Calcula log{sub(b)} {b**m} + log{sub(b)} {b**n}."; v = m + n
        w = nw(r, v, m * n, b ** m + b ** n, v + b); return mk(q, str(v), w, f"Suma de logaritmos = logaritmo del producto: log{sub(b)} {b**v} = {v}.")
    if typ == "d":
        b = r.choice([2, 3, 5]); m, n = r.randint(3, 6), r.randint(1, 2); q = f"Calcula log{sub(b)} {b**m} − log{sub(b)} {b**n}."; v = m - n
        w = nw(r, v, F(m, n), m + n, b ** m - b ** n); return mk(q, str(v), w, f"Resta de logaritmos = logaritmo del cociente: log{sub(b)} {b**v} = {v}.")
    b = r.choice([2, 3, 5]); k = r.randint(2, 4); n = r.randint(2, 4); q = f"Si log{sub(b)} 5 = a (aprox.), ¿a qué es igual log{sub(b)} 5{sup(n)}?" if False else f"¿Cuánto vale log{sub(b)} ({b}{sup(k)}){sup(n)}?"
    v = k * n; w = nw(r, v, k + n, b ** k * n if False else k ** n, n); return mk(q, str(v), w, f"log(aⁿ) = n·log a, así que da {n}·{k} = {v}.")

def f_expeq(r, t):
    typ = r.choice("abcd")
    if typ == "a":
        b = r.randint(2, 5); v = r.randint(2, 5); q = f"Resuelve {b}ˣ = {big(b**v)}."; w = nw(r, v, b ** v // b, F(b ** v, b), v + 1)
        return mk(q, xs(v), [f"x = {z}" for z in w], f"Como {b}{sup(v)} = {big(b**v)}, x = {v}.", extra=[str(v)])
    if typ == "b":
        b = r.choice([2, 3]); k = r.randint(3, 6); c = r.randint(1, 3); q = f"Resuelve {b}{sup('(x+'+str(c)+')')} = {b**k}."; v = k - c
        w = nw(r, v, k + c, F(k, c), k); return mk(q, xs(v), [f"x = {z}" for z in w], f"Se igualan exponentes: x + {c} = {k}.", extra=[str(v)])
    if typ == "c":
        b, k = r.choice([(2, 4), (3, 9), (4, 8), (9, 27), (8, 4), (4, 32)]); 
        v = F(math.log(k, b)).limit_denominator(10); q = f"Resuelve {b}ˣ = {k}."
        w = nw(r, v, F(k, b), F(b, k), k - b); return mk(q, xs(v), [f"x = {z}" for z in w], f"Se escribe todo en base 2 o 3 y se igualan los exponentes: x = {num(v)}.", extra=[num(v)])
    b = r.choice([2, 3]); k = r.randint(2, 4); q = f"Resuelve ({'1/' if True else ''}{b})ˣ = {b**k}."; v = -k
    w = nw(r, v, k, F(1, k), b ** k); return mk(q, xs(v), [f"x = {z}" for z in w], f"(1/{b})ˣ = {b}⁻ˣ; así −x = {k}, x = {-k}.", extra=[str(v)])

def f_ap(r, t):
    a1, d = r.randint(-5, 12), rnz(r, -5, 8); n = r.randint(8, sc(t, 15, 40))
    seq = ", ".join(num(a1 + i * d) for i in range(4)) + ", …"
    typ = r.choice("abc")
    if typ == "a":
        v = a1 + (n - 1) * d; q = f"En la progresión aritmética {seq} ¿cuál es el término {n}?"; w = nw(r, v, a1 + n * d, a1 * n + d, a1 + (n - 2) * d)
        return mk(q, num(v), w, f"aₙ = a₁ + (n − 1)d = {num(a1)} + {n-1}·({num(d)}) = {num(v)}.")
    if typ == "b":
        v = n * (2 * a1 + (n - 1) * d) // 2; q = f"¿Cuánto suman los primeros {n} términos de {seq}?"
        w = nw(r, v, n * (2 * a1 + n * d) // 2, n * (a1 + (n - 1) * d), n * (a1 + a1 + (n - 1) * d) // 4 if False else v + n)
        return mk(q, big(v), [big(int(F(z))) if "/" not in z else z for z in w], f"S = n(a₁ + aₙ)/2, con aₙ = {num(a1+(n-1)*d)}: {big(v)}.")
    q = f"En una progresión aritmética el 3.º término es {num(a1+2*d)} y el 7.º es {num(a1+6*d)}. ¿Cuál es la diferencia común?"
    w = nw(r, d, -d, F(4, 1) * d if False else 4 * d, d + 1); return mk(q, num(d), w, f"Hay 4 saltos entre los términos: d = ({num(a1+6*d)} − ({num(a1+2*d)}))/4 = {num(d)}.")

def f_gp(r, t):
    a1 = r.randint(1, 5); rr = r.choice([2, 3, -2, 4]); n = r.randint(4, sc(t, 6, 9))
    seq = ", ".join(num(a1 * rr ** i) for i in range(4)) + ", …"
    typ = r.choice("abc")
    if typ == "a":
        v = a1 * rr ** (n - 1); q = f"En la progresión geométrica {seq} ¿cuál es el término {n}?"
        return mk(q, big(v), [big(a1 * rr ** n), big(a1 * rr * (n - 1)), big(a1 * (rr * n))], f"aₙ = a₁·rⁿ⁻¹ = {a1}·({rr}){sup(n-1)} = {big(v)}.")
    if typ == "b":
        v = a1 * (rr ** n - 1) // (rr - 1); q = f"¿Cuánto suman los primeros {n} términos de {seq}?"
        return mk(q, big(v), [big(a1 * (rr ** n + 1) // (rr + 1) if (rr ** n + 1) % (rr + 1) == 0 else v + 1), big(a1 * (rr ** (n - 1) - 1) // (rr - 1)), big(v + a1 * rr ** n)], f"S = a₁(rⁿ − 1)/(r − 1) = {a1}·({rr}{sup(n)} − 1)/({rr} − 1) = {big(v)}.")
    p = r.choice([2, 3, 4, 5]); a = r.randint(1, 5) * p * 1; q = f"¿Cuánto suma la serie geométrica infinita {a} + {F(a,p)} + {F(a,p*p)} + …?" if False else f"¿Cuánto suma la serie infinita {a*p} + {a} + {F(a,p)} + {F(a,p*p)} + …?"
    v = F(a * p, 1) / (1 - F(1, p)); w = nw(r, v, F(a * p, 1) * (1 + F(1, p)), a * p + a, "")if False else nw(r, v, a * p * p, a * p + a)
    return mk(q, num(v), w, f"S = a₁/(1 − r) = {a*p}/(1 − 1/{p}) = {num(v)}.")

def f_radicals(r, t):
    typ = r.choice("abcd")
    if typ == "a":
        k = r.randint(2, sc(t, 6, 12)); m = r.choice([2, 3, 5, 6, 7]); q = f"Simplifica √{k*k*m}."; ans = f"{k}√{m}"
        w = [f"{k*m}√{m}" if False else f"{k+m}", f"{k*k}√{m}", f"{m}√{k}"]; return mk(q, ans, w, f"{k*k*m} = {k}²·{m}, y se saca {k} de la raíz.", extra=[f"{k}sqrt({m})", f"{k}*sqrt({m})", f"{k}raiz de {m}"])
    if typ == "b":
        a, b, m = r.randint(2, 9), r.randint(2, 9), r.choice([2, 3, 5, 7]); q = f"Calcula {a}√{m} + {b}√{m}."; ans = f"{a+b}√{m}"
        w = [f"{a*b}√{m}", f"{a+b}√{m*2}", f"√{m*(a+b)}"]; return mk(q, ans, w, "Son términos semejantes: se suman los coeficientes y la raíz queda igual.", extra=[f"{a+b}sqrt({m})", f"{a+b}*sqrt({m})"])
    if typ == "c":
        a, b = r.choice([(2, 8), (3, 12), (2, 18), (5, 20), (6, 24), (3, 27)]); v = int(math.isqrt(a * b)); q = f"¿Cuánto vale √{a} · √{b}?"
        w = nw(r, v, a + b, a * b, v + 2); return mk(q, str(v), w, f"√a·√b = √(ab) = √{a*b} = {v}.")
    k = r.randint(2, 9); q = f"Racionaliza {k}/√{k}." if False else f"Racionaliza 1/√{k}." ; 
    if int(math.isqrt(k)) ** 2 == k: return f_radicals(r, t)
    return mk(q, f"√{k} / {k}", [f"√{k}", f"1/{k}", f"{k}√{k}"], "Se multiplica numerador y denominador por √" + str(k) + ".", extra=[f"√{k}/{k}", f"sqrt({k})/{k}"])

def f_rational(r, t):
    typ = r.choice("abcd")
    a = r.randint(2, 9)
    if typ == "a":
        q = f"¿Cuál es el dominio de f(x) = 1/(x − {a})?"; ans = f"Todos los reales excepto x = {a}"
        w = [f"Todos los reales excepto x = {-a}", f"x > {a}", f"Todos los reales excepto x = 0"]; return mk(q, ans, w, "El denominador no puede ser cero: x − " + str(a) + " ≠ 0.", acc=None)
    if typ == "b":
        q = f"¿Para qué valores de x está definida f(x) = √(x − {a})?"; ans = f"x ≥ {a}"; w = [f"x > {a}", f"x ≤ {a}", f"x ≥ {-a}"]
        return mk(q, ans, w, "La expresión bajo la raíz debe ser mayor o igual que 0.")
    if typ == "c":
        v = r.randint(-6, 8); c = r.randint(1, 4); b = r.randint(1, 5); k = c * (v + b)  # k/(x+b) = c
        q = f"Resuelve {k}/(x + {b}) = {c}."; w = nw(r, v, F(k, c) + b, F(k, c), -v - 2 * b)
        return mk(q, xs(v), [f"x = {z}" for z in w], f"Se multiplica por (x + {b}): {k} = {c}(x + {b}), de donde x = {v}.", extra=[num(v)])
    k = r.randint(2, 9); q = f"Simplifica (x² − {k*k})/(x − {k})."; ans = f"x + {k}"
    return mk(q, ans, [f"x − {k}", f"x² + {k}", f"x + {k*k}"], "Se factoriza el numerador: (x − " + str(k) + ")(x + " + str(k) + ") y se cancela x − " + str(k) + ".")

def f_remthm(r, t):
    a, b, c, d = rnz(r, -3, 3), rnz(r, -5, 5), rnz(r, -6, 6), rnz(r, -9, 9); k = rnz(r, -3, 4)
    e = poly([a, b, c, d]); v = a * k ** 3 + b * k ** 2 + c * k + d
    typ = r.choice("ab")
    if typ == "a":
        q = f"¿Cuál es el residuo de dividir {e} entre (x {'−' if k>0 else '+'} {abs(k)})?"
        pv = lambda z: a * z ** 3 + b * z ** 2 + c * z + d
        w = nw(r, v, pv(-k), pv(k) + k, -v)
        return mk(q, num(v), w, f"Por el teorema del residuo es P({num(k)}) = {num(v)}.")
    m = rnz(r, -4, 4); k = rnz(r, 1, 3); P0 = lambda mm: k ** 3 + mm * k * k - 2 * k + 5
    # (x - k) factor de x^3 + m x^2 - 2x + 5 + n  -> encontrar n: n = -P0(m)
    n = -P0(m); cs = [1, m, -2, 5 + n]
    q = f"¿Cuánto debe valer n para que (x − {k}) sea factor de {poly(cs)}? (aquí n es el término independiente)" if False else f"Si x = {k} es raíz de {poly([1, m, -2, 5 + n])}, ¿cuál es el valor de P({k})?" if False else f"¿Qué valor de m hace que x = {k} sea raíz de x³ + m·x² − 2x + 5 + ({n})? Resuelve para m." if False else None
    mm = m; q = f"Si x = {k} es raíz de x³ + m·x² − 2x + {num(5 + n)}, ¿cuánto vale m?"
    ans = num(mm); w = nw(r, mm, -mm, mm + 1, F(n, k * k))
    return mk(q, ans, w, f"Se sustituye x = {k}: {k**3} + {k*k}m − {2*k} + {num(5+n)} = 0, y se despeja m = {num(mm)}.")

def cmul(a, b, c, d): return (a * c - b * d, a * d + b * c)

def f_complex(r, t):
    typ = r.choice("abcde") if t > .4 else r.choice("abc")
    a, b, c, d = rnz(r, -6, 6), rnz(r, -6, 6), rnz(r, -6, 6), rnz(r, -6, 6)
    if typ == "a":
        q = f"Calcula ({cx(a,b)}) + ({cx(c,d)})."; v = (a + c, b + d); w = [cx(a + c, b - d), cx(a - c, b - d), cx(a + c, 0) if b + d else cx(a + c, 1)]
        return mk(q, cx(*v), w, "Se suman por separado las partes reales y las imaginarias.")
    if typ == "b":
        n = r.randint(5, 60); res = {0: "1", 1: "i", 2: "−1", 3: "−i"}[n % 4]
        q = f"¿Cuánto vale i{sup(n)}?"; w = [o for o in ["1", "i", "−1", "−i"] if o != res]
        return mk(q, res, w, f"Las potencias de i se repiten cada 4; {n} mod 4 = {n%4}.")
    if typ == "c":
        v = cmul(a, b, c, d); q = f"Calcula ({cx(a,b)})({cx(c,d)})."; w = [cx(a * c + b * d, a * d + b * c), cx(a * c - b * d, a * d - b * c), cx(a * c, b * d)]
        return mk(q, cx(*v), w, "Se distribuye y se usa i² = −1: parte real ac − bd, parte imaginaria ad + bc.")
    if typ == "d":
        a, b = r.choice([(3, 4), (5, 12), (6, 8), (8, 15), (9, 12)]); a *= r.choice([1, -1]); b *= r.choice([1, -1]); v = int(math.isqrt(a * a + b * b))
        q = f"¿Cuál es el módulo de {cx(a,b)}?"; w = nw(r, v, a + b if a + b > 0 else abs(a) + abs(b), a * a + b * b, abs(a) + abs(b)); return mk(q, str(v), w, f"|z| = √(a² + b²) = √{a*a+b*b} = {v}.")
    p, qq = rnz(r, -4, 4), rnz(r, -4, 4); z = cmul(c, d, p, qq)
    q = f"Calcula ({cx(*z)}) / ({cx(c,d)})."; w = [cx(p, -qq), cx(-p, qq), cx(qq, p)]
    return mk(q, cx(p, qq), w, f"Se multiplica numerador y denominador por el conjugado de {cx(c,d)}; el resultado es {cx(p,qq)}.")

def f_polydiv(r, t):
    a = rnz(r, -4, 4); 
    if r.random() < 0.5:
        p = rnz(r, -5, 5); e = sp.Poly(sp.expand((X - a) * (X + p)), X).all_coeffs(); q = f"¿Cuál es el cociente de ({poly(e)}) ÷ (x {'−' if a>0 else '+'} {abs(a)})?"
        ans = f"x {'+' if p>0 else '−'} {abs(p)}"; w = [f"x {'−' if p>0 else '+'} {abs(p)}", f"x {'+' if a>0 else '−'} {abs(a)}" if (a != p and not (a == -p)) else f"x + {abs(p)+1}", f"x {'+' if p*a>0 else '−'} {abs(p*a)}"]
        return mk(q, ans, w, f"La división es exacta: ({num(a)}) es raíz, así que se factoriza como (x − ({num(a)}))(x + ({num(p)})).")
    m, n = rnz(r, -3, 3), rnz(r, -4, 4); quo = [1, m, n]; e = sp.Poly(sp.expand((X - a) * (X ** 2 + m * X + n)), X).all_coeffs()
    q = f"¿Cuál es el cociente de ({poly(e)}) ÷ (x {'−' if a>0 else '+'} {abs(a)})?"
    ans = poly(quo); w = [poly([1, m + a, n]), poly([1, -m, n]), poly([1, m, -n])]
    return mk(q, ans, w, f"Con división sintética por {num(a)} se obtienen los coeficientes {', '.join(map(num, quo))} y residuo 0.")

def f_funcs(r, t):
    a, b, c, d = rnz(r, -4, 4), r.randint(-6, 6), rnz(r, 1, 3), r.randint(-5, 5)
    f = lambda z: a * z + b; g = lambda z: c * z * z + d
    typ = r.choice("abcd")
    fs, gs = f"f(x) = {poly([a,b])}", f"g(x) = {poly([c,0,d])}"
    if typ == "a":
        k = rnz(r, -3, 3); v = f(g(k)); q = f"Si {fs} y {gs}, ¿cuánto vale f(g({num(k)}))?"
        w = nw(r, v, g(f(k)), f(k) * g(k) , f(k) + g(k)); return mk(q, num(v), w, f"g({num(k)}) = {num(g(k))} y f({num(g(k))}) = {num(v)}.")
    if typ == "b":
        k = rnz(r, -3, 3); v = g(f(k)); q = f"Si {fs} y {gs}, ¿cuánto vale (g∘f)({num(k)})?"
        w = nw(r, v, f(g(k)), f(k) * g(k), g(k) + f(k)); return mk(q, num(v), w, f"f({num(k)}) = {num(f(k))} y g({num(f(k))}) = {num(v)}.")
    if typ == "c":
        cs = sp.Poly(sp.expand(a * (c * X ** 2 + d) + b), X).all_coeffs(); q = f"Si {fs} y {gs}, ¿cuál es (f∘g)(x)?"
        w = [poly(sp.Poly(sp.expand(c * (a * X + b) ** 2 + d), X).all_coeffs()), poly([a * c, 0, d + b]) if a * d != 0 or True else "", poly([a + c, 0, b + d])]
        return mk(q, poly(cs), w, "Se reemplaza g(x) dentro de f: a·g(x) + b.")
    q = f"¿Cuál es la función inversa de {fs}?"; ans = f"f⁻¹(x) = (x {'−' if b>0 else '+'} {abs(b)})/{num(a)}" if b != 0 else f"f⁻¹(x) = x/{num(a)}"
    if b == 0: return f_funcs(r, t)
    w = [f"f⁻¹(x) = (x {'+' if b>0 else '−'} {abs(b)})/{num(a)}", f"f⁻¹(x) = {num(a)}x {'−' if b>0 else '+'} {abs(b)}", f"f⁻¹(x) = 1/({poly([a,b])})"]
    return mk(q, ans, w, f"Se despeja x de y = {poly([a,b])}: x = (y − ({num(b)}))/{num(a)}.")

def f_quadform(r, t):
    h = rnz(r, -6, 6); k = r.choice([2, 3, 5, 6, 7, 10, 11, 13]); b = -2 * h; c = h * h - k
    q = f"Resuelve {poly([1, b, c])} = 0."; ans = f"x = {num(h)} ± √{k}"
    w = [f"x = {num(-h)} ± √{k}", f"x = {num(h)} ± {k}", f"x = {num(h)} ± √{h*h+k}"]
    return mk(q, ans, w, f"Δ = {b*b - 4*c} y x = ({num(-b)} ± √{b*b-4*c})/2 = {num(h)} ± √{k}.", extra=[f"{num(h)} ± √{k}", f"x = {num(h)} +- sqrt({k})", f"{num(h)}±√{k}", f"x = {num(h)}±√{k}"])

SOLS = []
for b_ in (2, 3, 5):
    for m_ in range(1, 5):
        for s_ in range(3, 40):
            if (b_ ** m_) % s_ == 0:
                c_ = s_ - b_ ** m_ // s_
                if c_ > 0: SOLS.append((b_, m_, s_, c_))

def f_logeq(r, t):
    if r.random() < 0.5:
        b = r.choice([2, 3, 5]); k = r.randint(1, 3); a = r.randint(1, 9); v = b ** k - a
        q = f"Resuelve log{sub(b)}(x + {a}) = {k}."; w = nw(r, v, b * k - a, k - a, b ** k + a)
        return mk(q, xs(v), [f"x = {z}" for z in w], f"x + {a} = {b}{sup(k)} = {b**k}, así x = {v}.", extra=[num(v)])
    b, m, s, c = r.choice(SOLS); q = f"Resuelve log{sub(b)} x + log{sub(b)}(x − {c}) = {m}. ¿Qué valor de x es válido?"
    other = F(c, 1) - s  # raíz negativa de x(x-c)=b^m: x2 = c - s
    w = [f"x = {num(other)}", f"x = {num(s)} y x = {num(other)}", f"x = {num(b**m)}"]
    return mk(q, xs(s), w, f"x(x − {c}) = {b**m} da x = {s} o x = {num(other)}; solo {s} mantiene positivos los argumentos.", extra=[str(s)])

def f_percent(r, t):
    typ = r.choice("abcd")
    if typ == "a":
        p = r.choice([10, 15, 20, 25, 30, 40, 50]); P = r.choice([40, 60, 80, 120, 200, 240, 400, 600]); v = F(P * (100 - p), 100)
        q = f"Un artículo cuesta ${big(P)} y tiene {p} % de descuento. ¿Cuánto se paga?"; w = nw(r, v, P - p, F(P * p, 100), F(P * (100 + p), 100))
        return mk(q, "$" + num(v), ["$" + z for z in w], f"El descuento es {num(F(P*p,100))}; se paga {P} − {num(F(P*p,100))} = {num(v)}.", extra=[num(v)])
    if typ == "b":
        p = r.choice([5, 10, 20, 25, 50]); P = r.choice([20, 40, 80, 120, 200]); v = P * p // 100 if P * p % 100 == 0 else F(P * p, 100)
        q = f"¿Cuánto es el {p} % de {P}?"; w = nw(r, v, F(P, p), P - v, p * 2) ; return mk(q, num(v), w, f"{p}/100 · {P} = {num(v)}.")
    if typ == "c":
        a = r.randint(2, 6); b = r.randint(2, 5); k = r.randint(2, 9); v = a * k * b // 1
        q = f"Si {a} cuadernos cuestan ${a*k}, ¿cuánto cuestan {a*b} cuadernos?"; w = nw(r, a * k * b, a * k + b, k * b * 2, k + a * b); return mk(q, f"${a*k*b // a if False else k*a*b // 1 // 1}" if False else "$" + num(k * a * b // a * 1 if False else k * a * b // a), ["$" + z for z in nw(r, k * a * b // a, k * a * b, k + a * b, a * k + b)], f"Cada cuaderno cuesta ${k}; {a*b} cuadernos cuestan {k*a*b//a}.") if False else mk(q, "$" + str(k * b * a), ["$" + z for z in nw(r, k * b * a, k * b, k + a * b, a * k + b)], f"Cada cuaderno cuesta ${k}; {a*b} cuadernos cuestan ${k*b*a}.", extra=[str(k * b * a)])
    P = r.choice([50, 80, 120, 200]); p = r.choice([10, 20, 25]); v = F(P * (100 + p), 100)
    q = f"Un sueldo de ${big(P*10)} aumenta {p} %. ¿Cuál es el nuevo sueldo?"; v = F(P * 10 * (100 + p), 100)
    return mk(q, "$" + big(v), ["$" + big(int(z)) for z in [P * 10 * (100 - p) // 100, P * 10 + p, P * 10 * p // 100]], f"Se multiplica por 1,{p:02d}: {big(P*10)}·{dec(1+F(p,100))} = {big(v)}.", extra=[str(int(v))])

def f_word(r, t):
    typ = r.choice("abc")
    if typ == "a":
        k = r.randint(2, 4); v = r.randint(5, 20); tot = v + k * v; q = f"Ana tiene {k} veces la edad de Luis y juntos suman {tot} años. ¿Cuántos años tiene Luis?"
        w = nw(r, v, k * v, tot - k, F(tot, k)); return mk(q, str(v), w, f"x + {k}x = {tot} → {k+1}x = {tot}, x = {v}.")
    if typ == "b":
        n = r.randint(3, 30); q = f"La suma de tres enteros consecutivos es {3*n}. ¿Cuál es el menor?"; v = n - 1
        w = nw(r, v, n, n + 1, F(3 * n, 3) - 2); return mk(q, str(v), w, f"x + (x + 1) + (x + 2) = {3*n} → 3x + 3 = {3*n}, x = {v}.")
    l = r.randint(4, 15); w_ = r.randint(2, l - 1) if l > 3 else 2; P = 2 * (l + w_); q = f"Un rectángulo tiene perímetro {P} cm y su largo mide {l} cm. ¿Cuánto mide su ancho?"
    w = nw(r, w_, P - l, F(P, 2), P - 2 * l - 2); return mk(q, f"{w_} cm", [z + " cm" for z in w], f"2l + 2a = {P} → a = {P}/2 − {l} = {w_}.", extra=[str(w_)])

def f_ratexp(r, t):
    b, n, m = r.choice([(8, 3, 2), (27, 3, 2), (16, 4, 3), (4, 2, 3), (9, 2, 3), (32, 5, 2), (8, 3, 4), (81, 4, 3), (125, 3, 2)]); neg = r.random() < 0.4
    v = F(round(b ** (1 / n)) ** m); tx = f"{b}{sup('(' + ('-' if neg else '') + str(m) + '/' + str(n) + ')')}"
    if neg: v = 1 / v
    q = f"¿Cuánto vale {b}^({'−' if neg else ''}{m}/{n})?"; w = nw(r, v, F(1, 1) / v if v != 0 else 5, F(b, n) ** 1 if False else b ** m // n, -v if False else b * m)
    return mk(q, num(v), w, f"La raíz índice {n} de {b} es {round(b**(1/n))}; luego se eleva a {m}" + (" y se invierte por el signo negativo." if neg else "."))

def f_quadineq(r, t):
    p, qq = sol_pair(rnz(r, -6, 6), rnz(r, -6, 6))
    if p == qq: return f_quadineq(r, t)
    less = r.random() < 0.5; op = r.choice(["<", "≤"] if less else [">", "≥"])
    e = poly([1, -(p + qq), p * qq]); q = f"Resuelve {e} {op} 0."
    inc = "≤" if "=" in op or op in ("≤", "≥") else "<"
    if less: ans = f"{num(p)} {inc} x {inc} {num(qq)}"; w = [f"x {inc} {num(p)} o x {inc.replace('<','>').replace('≤','≥')} {num(qq)}", f"{num(-qq)} {inc} x {inc} {num(-p)}", f"x {inc} {num(qq)}"]
    else: ans = f"x {inc.replace('<','>').replace('≤','≥')} {num(qq)} o x {inc} {num(p)}"; ans = f"x {'<' if op=='>' else '≤'} {num(p)} o x {op} {num(qq)}"; w = [f"{num(p)} {'<' if op=='>' else '≤'} x {'<' if op=='>' else '≤'} {num(qq)}", f"x {op} {num(p)}", f"x {'<' if op=='>' else '≤'} {num(-p)} o x {op} {num(-qq)}"]
    return mk(q, ans, w, f"Las raíces son {num(p)} y {num(qq)}; la parábola abre hacia arriba, así que {'es negativa entre ellas' if less else 'es positiva fuera de ellas'}.")

def f_binom(r, t):
    n = r.randint(3, sc(t, 5, 8)); a = r.randint(1, 3); k = r.randint(1, n - 1); typ = r.choice("abc")
    if typ == "a":
        v = math.comb(n, k) * a ** k; q = f"¿Cuál es el coeficiente de x{sup(k)} en (x + {a}){sup(n)}?" if k < n - 1 or True else ""
        # x^k y a^(n-k): coeficiente = C(n,k) a^(n-k)
        v = math.comb(n, k) * a ** (n - k)
        w = nw(r, v, math.comb(n, k), math.comb(n, k) * a ** k, a ** (n - k)); return mk(q, str(v), w, f"Término general: C({n}, {k})·x{sup(k)}·{a}{sup(n-k)} → {math.comb(n,k)}·{a**(n-k)} = {v}.")
    if typ == "b":
        q = f"¿Cuántos términos tiene el desarrollo de (x + y){sup(n)}?"; w = nw(r, n + 1, n, 2 * n, n - 1); return mk(q, str(n + 1), w, f"Tiene n + 1 términos, de x{sup(n)} a y{sup(n)}.")
    q = f"¿Cuánto suman los coeficientes del desarrollo de (x + 1){sup(n)}?"; v = 2 ** n; w = nw(r, v, n * 2, n ** 2, 2 ** n - 1); return mk(q, str(v), w, f"Se evalúa en x = 1: (1 + 1){sup(n)} = {v}.")

def f_growth(r, t):
    typ = r.choice("ab")
    if typ == "a":
        P = r.choice([100, 200, 500, 800]); h = r.choice([2, 3, 4, 6]); k = r.randint(2, 5); T = h * k; v = P * 2 ** k
        q = f"Una colonia de {P} bacterias se duplica cada {h} horas. ¿Cuántas habrá a las {T} horas?"; w = nw(r, v, P * k * 2, P * T, P * 2 ** (k + 1)); return mk(q, big(v), [big(int(F(z))) if "/" not in z else z for z in w], f"Hay {k} duplicaciones: {P}·2{sup(k)} = {big(v)}.")
    P = r.choice([1000, 2000, 5000]); rt = r.choice([10, 20]); n = r.randint(2, 3); v = F(P) * F(100 + rt, 100) ** n
    q = f"Se invierten ${big(P)} al {rt} % anual compuesto. ¿Cuánto hay después de {n} años?"; w = [big(P + P * rt * n // 100), big(P * (100 + rt) // 100 * n), big(P * (1 + F(rt, 100)) ** (n + 1))]
    return mk(q, "$" + big(int(v)) if v.denominator == 1 else "$" + dec(v), ["$" + z for z in w], f"A = P(1 + r){sup(n)} = {big(P)}·{dec(1+F(rt,100))}{sup(n)} = {dec(v)}.", extra=[str(int(v))] if v.denominator == 1 else [])

def f_sigma(r, t):
    a, b, n = r.randint(1, 5), r.randint(-3, 5), r.randint(4, 10)
    v = sum(a * k + b for k in range(1, n + 1)); q = f"Calcula Σ (de k = 1 a {n}) de ({poly([a,b],'k')})."
    w = nw(r, v, a * n + b, a * n * (n + 1) // 2, v + b * n); return mk(q, num(v), w, f"Σ k = {n*(n+1)//2}; entonces {a}·{n*(n+1)//2} + {num(b)}·{n} = {v}.")

def f_geom(r, t):
    if r.random() < .5:
        a, b = r.choice([(3, 4), (5, 12), (6, 8), (8, 15)]); x1, y1 = r.randint(-5, 5), r.randint(-5, 5); q = f"¿Cuál es la distancia entre ({x1}, {y1}) y ({x1+a}, {y1+b})?".replace("(-", "(−").replace(", -", ", −")
        v = int(math.isqrt(a * a + b * b)); w = nw(r, v, a + b, a * a + b * b, abs(b - a)); return mk(q, str(v), w, f"d = √({a}² + {b}²) = √{a*a+b*b} = {v}.")
    x1, y1, x2, y2 = [2 * r.randint(-5, 5) for _ in range(4)]; q = f"¿Cuál es el punto medio entre ({num(x1)}, {num(y1)}) y ({num(x2)}, {num(y2)})?"
    ans = f"({num(F(x1+x2,2))}, {num(F(y1+y2,2))})"; w = [f"({num(x1+x2)}, {num(y1+y2)})", f"({num(F(x1-x2,2))}, {num(F(y1-y2,2))})", f"({num(F(y1+y2,2))}, {num(F(x1+x2,2))})"]
    return mk(q, ans, w, "Se promedian las coordenadas: ((x₁ + x₂)/2, (y₁ + y₂)/2).", extra=[ans.replace(" ", "")])

FAMILIES = [
    ("eval", f_eval, 14, 1, 14), ("orden", f_order, 14, 3, 22), ("un_paso", f_onestep, 16, 4, 12), ("dos_pasos", f_twostep, 24, 10, 28),
    ("ambos_lados", f_bothsides, 22, 20, 36), ("potencias_num", f_expnum, 20, 6, 30), ("reglas_exp", f_exprules, 20, 16, 38),
    ("fracciones", f_fractions, 20, 12, 34), ("pendiente", f_slope, 16, 16, 32), ("recta", f_lineeq, 20, 24, 46), ("desarrollo", f_expand, 22, 26, 48),
    ("factorizar", f_factor, 26, 30, 58), ("raices_cuad", f_quadroots, 26, 34, 58), ("discriminante", f_disc, 18, 40, 56), ("vertice", f_vertex, 18, 46, 64),
    ("sistemas", f_system, 28, 40, 64), ("desigualdades", f_ineq, 22, 30, 54), ("valor_abs", f_abs, 16, 38, 58), ("logaritmos", f_logs, 22, 46, 72),
    ("exp_ecuacion", f_expeq, 18, 42, 66), ("prog_arit", f_ap, 18, 36, 62), ("prog_geo", f_gp, 18, 46, 74), ("radicales", f_radicals, 18, 28, 52),
    ("racionales", f_rational, 16, 36, 60), ("residuo", f_remthm, 16, 58, 78), ("complejos", f_complex, 24, 56, 80), ("div_poli", f_polydiv, 16, 60, 80),
    ("funciones", f_funcs, 22, 42, 68), ("form_general", f_quadform, 14, 56, 74), ("log_ecuacion", f_logeq, 14, 64, 88), ("porcentajes", f_percent, 14, 8, 30),
    ("problemas", f_word, 14, 18, 40), ("exp_racional", f_ratexp, 14, 54, 72), ("desig_cuad", f_quadineq, 14, 60, 80), ("binomio", f_binom, 14, 66, 88),
    ("crecimiento", f_growth, 12, 50, 72), ("sumatoria", f_sigma, 10, 40, 60), ("geometria_analitica", f_geom, 12, 24, 44),
]
