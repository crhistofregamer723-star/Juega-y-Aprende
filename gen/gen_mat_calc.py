# -*- coding: utf-8 -*-
# Categoría CÁLCULO (se ejecuta dentro del espacio de nombres de gen_mat.py)
X = sp.Symbol('x') if sp else None


def rat(f):
    f = F(f)
    return sp.Rational(f.numerator, f.denominator)


def sy(p):
    return sum(rat(v) * X ** k for k, v in p.items())


def chk(a, b):
    if sp is not None:
        assert sp.simplify(a - b) == 0, (a, b)


def pw(n):
    return '' if n == 0 else 'x' if n == 1 else 'x' + sup(n)


def cf(m, top):
    """Coeficiente entero m por la expresión top (texto)."""
    if top.startswith('1/'):
        if m == 1: return top
        if m == -1: return '-' + top
        return f"{m}/{top[2:]}"
    if m == 1: return top
    if m == -1: return '-' + top
    if top.startswith('e^') or top.startswith('x'): return f"{m}{top}"
    return f"{m} {top}"


def ex(n):
    return '' if n == 1 else sup(n)


# ------------------------------------------------------------------ límites
def c_lim_sub():
    a = R.randint(-4, 5)
    p = {2: R.randint(0, 4), 1: R.randint(-5, 5), 0: R.randint(-6, 6)}
    p = {k: v for k, v in p.items() if v}
    if len(p) < 2: return False
    s = peval(p, a)
    if sp: assert sp.limit(sy(p), X, a) == rat(s)
    q = T(["¿Cuánto vale lim(x→{a}) ({p})?", "Calcula el límite cuando x tiende a {a} de {p}."], (a, len(p), sum(p.values())), a=a, p=Q(p))
    return add('calc', q, nf(s), numwrong(s, extra=[nf(peval(p, 0))]), "Al ser un polinomio, basta sustituir x por el valor al que tiende.", 5 + abs(a) + len(p) * 2 + abs(s) / 10)


def c_lim_fac():
    k = R.randint(0, 3)
    a, b = R.randint(-6, 7), R.randint(-6, 7)
    if a == b: return False
    den = Q({1: 1, 0: -a})
    if k <= 1:
        num = {2: 1, 1: -(a + b), 0: a * b}; s = a - b; d = 34 + abs(s) / 2
        e = f"El numerador es (x − {a})(x − {b}); al simplificar queda x − {b}, que tiende a {s}."
    elif k == 2:
        if a == 0: return False
        num = {3: 1, 0: -a ** 3}; s = 3 * a * a; d = 55 + abs(a)
        e = f"x³ − {a**3} = (x − {a})(x² + {a}x + {a*a}); al sustituir queda 3·{a}² = {s}."
    else:
        if a == 0: return False
        num = {2: 1, 0: -a * a}; s = 2 * a; d = 36 + abs(a)
        e = f"x² − {a*a} = (x − {a})(x + {a}); el límite es 2·{a} = {s}."
    if sp: assert sp.limit(sy(num) / (X - a), X, a) == s
    q = T(["¿Cuánto vale lim(x→{a}) ({n})/({d})?", "Calcula lim(x→{a}) de ({n})/({d})."], (a, b, k), a=a, n=Q(num), d=den)
    return add('calc', q, s, numwrong(s, extra=[0, 'No existe']), e, d)


def c_lim_inf():
    k = R.randint(0, 3)
    a, d_ = R.choice([-5, -4, -3, -2, -1, 1, 2, 3, 4, 5, 6]), R.randint(1, 6)
    b, c, e_, f = [R.randint(-5, 5) for _ in range(4)]
    if k == 0:
        num, den = {2: a, 1: b, 0: c}, {2: d_, 1: e_, 0: f}; s = F(a, d_)
        ans = nf(s); w = [nf(F(d_, a)), '0', '∞', nf(F(a + d_, 1))]; d = 44 + abs(a) + d_ / 2
        ex_ = "Grados iguales: el límite es el cociente de los coeficientes principales."
    elif k == 1:
        num, den = {1: a, 0: b}, {2: d_, 1: e_, 0: f}; ans = '0'; w = ['1', '∞', nf(F(a, d_)), '-∞'] if a != d_ else ['1', '∞', '2', '-∞']; d = 44 + d_ / 2
        ex_ = "El grado del denominador es mayor, así que el cociente tiende a 0."
    elif k == 2:
        num, den = {3: a, 0: c}, {2: d_, 1: e_, 0: f}; ans = '∞' if a > 0 else '-∞'; w = ['0', nf(F(a, d_)), '-∞' if a > 0 else '∞', '1']; d = 50 + abs(a) / 2
        ex_ = "El grado del numerador es mayor: el cociente crece sin límite con el signo de a/d."
    else:
        e2 = R.choice([x for x in range(-5, 6) if x]); num, den = {1: a, 0: b}, {1: d_, 0: e2}; s = F(a, d_)
        ans = nf(s); w = [nf(F(d_, a)), '0', '∞', nf(F(b, e2))]; d = 40 + abs(a)
        ex_ = "Se divide entre x y se evalúa: queda a/d."
    q = f"¿Cuánto vale lim(x→∞) ({Q(num)})/({Q(den)})?"
    return add('calc', q, ans, w, ex_, d, acc=['infinito', 'inf', '-infinito'] if ans in ('∞', '-∞') else ())


def c_lim_tr():
    k = R.randint(0, 4); a, b = R.randint(1, 9), R.randint(1, 9)
    s = F(a, b)
    if k == 0: f_, e = f"sin({a}x)/{b}x" if b != 1 else f"sin({a}x)/x", "Se usa lim sin(u)/u = 1: queda a/b."
    elif k == 1: f_, e = f"tan({a}x)/{b}x" if b != 1 else f"tan({a}x)/x", "tan(u)/u → 1 cuando u → 0."
    elif k == 2: f_, e = f"(e^({a}x) − 1)/{b}x" if b != 1 else f"(e^({a}x) − 1)/x", "(e^u − 1)/u → 1 cuando u → 0."
    elif k == 3: f_, e = f"ln(1 + {a}x)/{b}x" if b != 1 else f"ln(1 + {a}x)/x", "ln(1 + u)/u → 1 cuando u → 0."
    else: f_, e = f"sin({a}x)/sin({b}x)", "sin(ax)/sin(bx) → a/b cuando x → 0."
    if a == 1 and k in (0, 1) and b == 1: return False
    return add('calc', f"¿Cuánto vale lim(x→0) {f_}?", nf(s), [nf(F(b, a)), nf(F(a * b)), '1', '0'], e, 56 + (a + b) / 2, acc=[best(s)])


def c_lim_sqrt():
    a = R.randint(2, 9)
    if R.random() < .5:
        if sp: assert sp.limit((sp.sqrt(X + a * a) - a) / X, X, 0) == sp.Rational(1, 2 * a)
        s = F(1, 2 * a)
        return add('calc', f"¿Cuánto vale lim(x→0) (√(x + {a*a}) − {a})/x?", nf(s), [nf(F(1, a)), nf(F(a, 2)), nf(F(2, a)), '0'], f"Se multiplica por el conjugado: queda 1/(√(x+{a*a}) + {a}) → 1/{2*a}.", 76 + a / 2, acc=[dec(s, 4)])
    if sp: assert sp.limit((X - a * a) / (sp.sqrt(X) - a), X, a * a) == 2 * a
    return add('calc', f"¿Cuánto vale lim(x→{a*a}) (x − {a*a})/(√x − {a})?", 2 * a, numwrong(2 * a, pos=True, extra=[a, a * a]), f"x − {a*a} = (√x − {a})(√x + {a}); el límite es 2·{a}.", 74 + a / 2)


def c_cont():
    a = R.randint(1, 6); t = R.randint(-4, 6)
    b = a * t; k = a + t
    return add('calc', f"Sea f(x) = x² {'+' if b>=0 else '−'} {abs(b)} si x < {a}, y f(x) = kx si x ≥ {a}. ¿Qué valor de k hace continua a f en x = {a}?", k, numwrong(k, extra=[a * a + b, b]) if False else numwrong(k), f"Se iguala el límite lateral {a*a+b} con {a}k, entonces k = {k}.", 66 + a + abs(t) / 2) if b != 0 else False


# ---------------------------------------------------------------- derivadas
def c_der_pow():
    n = R.randint(1, 9); a = R.choice([1, 1, 1, 2, 3, 4, 5, 6, -2, -3, 7, 8])
    p = {n: a}
    ws = [poly({n: a * n}), poly({n - 1: a}), poly({n + 1: F(a, n + 1)}), poly({n - 1: a * (n - 1)}), poly({n: a})]
    return add('calc', f"¿Cuál es la derivada de f(x) = {Q(p)}?", poly(pder(p)), ws, "Regla de la potencia: (axⁿ)′ = a·n·xⁿ⁻¹.", 3 + n * 1.5 + (0 if a == 1 else 2))


def wr_der(p):
    dp = pder(p)
    w = [poly({k - 1: v for k, v in p.items() if k > 0}), poly({k: v * k for k, v in p.items() if k > 0}), poly(pint(p))]
    if 0 in p: w.append(poly(padd(dp, {0: p[0]})))
    return w + pert(dp)


def rand_poly(deg, lo=-9, hi=9):
    p = {}
    for k in range(deg, -1, -1):
        if k == deg or R.random() < .65: p[k] = R.choice([c for c in range(lo, hi + 1) if c])
    return p


def c_der_poly():
    deg = R.randint(2, 5); p = rand_poly(deg)
    if len(p) < 2: return False
    dp = pder(p)
    chk(sp.diff(sy(p), X), sy(dp)) if sp else None
    q = T(["Deriva f(x) = {p}.", "¿Cuál es f′(x) si f(x) = {p}?", "Calcula la derivada de {p}."], (deg, len(p), sum(p.values())), p=Q(p))
    return add('calc', q, poly(dp), wr_der(p), "Se deriva término a término con la regla de la potencia; la constante desaparece.", 10 + deg * 4 + len(p) * 2)


def c_der_val():
    deg = R.randint(2, 3); p = rand_poly(deg, -7, 7); a = R.randint(-3, 4)
    if len(p) < 2: return False
    s = peval(pder(p), a)
    return add('calc', f"Si f(x) = {Q(p)}, ¿cuánto vale f′({a})?", nf(s), numwrong(s, extra=[nf(peval(p, a))]), f"f′(x) = {poly(pder(p))}; al evaluar en {a} da {nf(s)}.", 26 + deg * 4 + abs(a))


TRIG = [('sin x', 1, 'cos x', [(-1, 'cos x'), (1, 'sin x'), (-1, 'sin x')]),
        ('cos x', -1, 'sin x', [(1, 'sin x'), (1, 'cos x'), (-1, 'cos x')]),
        ('e^x', 1, 'e^x', [(1, 'xe^(x-1)'), (1, 'e^(x-1)'), (1, 'x e^x')]),
        ('ln x', 1, '1/x', [(1, 'x'), (-1, '1/x²'), (1, '1/x²')]),
        ('tan x', 1, 'sec²x', [(1, 'sec x'), (-1, 'sec²x'), (1, '1/cos x')])]


def c_der_trig():
    f_, k, top, wl = R.choice(TRIG)
    c = R.choice([1, 2, 3, 4, 5, 6, -2, -3, -4, 7])
    fq = cf(c, f_) if f_ != 'ln x' or True else f_
    if c == 1: fq = f_
    ans = cf(c * k, top)
    w = [cf(c * kk, tt) for kk, tt in wl]
    return add('calc', f"¿Cuál es la derivada de f(x) = {fq.replace('-', '−')}?", ans, w, f"(sin x)′ = cos x, (cos x)′ = −sin x, (eˣ)′ = eˣ, (ln x)′ = 1/x, (tan x)′ = sec²x; el coeficiente se conserva.", 20 + abs(c) + (6 if f_ == 'tan x' else 0))


def c_der_trig2():
    a, b = R.randint(1, 6), R.randint(1, 6)
    k = R.randint(0, 2)
    if k == 0:
        return add('calc', f"Deriva f(x) = {cf(a,'sin x') if a>1 else 'sin x'} + {cf(b,'cos x') if b>1 else 'cos x'}.", f"{cf(a,'cos x') if a>1 else 'cos x'} - {cf(b,'sin x') if b>1 else 'sin x'}",
                   [f"{cf(a,'cos x') if a>1 else 'cos x'} + {cf(b,'sin x') if b>1 else 'sin x'}", f"-{cf(a,'cos x') if a>1 else 'cos x'} + {cf(b,'sin x') if b>1 else 'sin x'}", f"{cf(a,'cos x') if a>1 else 'cos x'} - {cf(b,'cos x') if b>1 else 'cos x'}", f"-{cf(a,'cos x') if a>1 else 'cos x'} - {cf(b,'sin x') if b>1 else 'sin x'}"],
                   "La derivada de la suma es la suma de derivadas.", 30 + a + b)
    if k == 1:
        n = R.randint(2, 6)
        return add('calc', f"Deriva f(x) = e^x + {pw(n) if a==1 else str(a)+pw(n)}.", f"e^x + {str(a*n) if a*n != 1 else ''}{pw(n-1) or ''}".replace('+ ', '+ ') if n > 1 else 'e^x', [f"e^x + {a}{pw(n)}", f"x e^(x-1) + {a*n}{pw(n-1)}", f"e^x + {a*n}{pw(n)}", f"e^x + {a}{pw(n-1)}"],
                   "La derivada de eˣ es eˣ y la de axⁿ es a·n·xⁿ⁻¹.", 30 + n + a) if False else False
    n = R.randint(2, 7)
    return add('calc', f"Deriva f(x) = ln x + {a}x{sup(n)}." if n > 1 else '', f"1/x + {a*n}{pw(n-1)}", [f"1/x + {a}{pw(n)}", f"x + {a*n}{pw(n-1)}", f"ln x + {a*n}{pw(n-1)}", f"-1/x² + {a*n}{pw(n-1)}"], "(ln x)′ = 1/x y (axⁿ)′ = a·n·xⁿ⁻¹.", 32 + n + a)


def c_der_special():
    k = R.randint(0, 2)
    if k == 0:
        n = R.randint(2, 9)
        return add('calc', f"¿Cuál es la derivada de f(x) = 1/x{sup(n)}?", f"-{n}/x{sup(n+1)}", [f"{n}/x{sup(n+1)}", f"-{n}/{pw(n-1)}", f"-1/x{sup(n+1)}", f"-{n+1}/x{sup(n+1)}"], f"1/xⁿ = x⁻ⁿ, cuya derivada es −n·x⁻ⁿ⁻¹.", 38 + n)
    if k == 1:
        a = R.randint(1, 9)
        return add('calc', f"¿Cuál es la derivada de f(x) = {a if a>1 else ''}√x?", f"{a}/(2√x)", [f"{a}/√x", f"{a}√x/2", f"{2*a}/√x", f"{a}/(2x)"], "√x = x^(1/2), derivada (1/2)x^(−1/2).", 42 + a / 2)
    a = R.choice([2, 3, 5, 10])
    return add('calc', f"¿Cuál es la derivada de f(x) = {a}^x?", f"{a}^x ln {a}", [f"x·{a}^(x-1)", f"{a}^x", f"{a}^x/ln {a}", f"{a}^x ln x"], "(aˣ)′ = aˣ·ln a.", 46 + a / 2, acc=[f"{a}^x*ln({a})", f"{a}^x ln({a})"])


def c_der_prod():
    k = R.randint(0, 3)
    if k == 0:
        m, n = R.randint(1, 4), R.randint(1, 4); b, d_ = R.choice([-4, -3, -2, -1, 1, 2, 3, 4, 5]), R.choice([-5, -3, -2, -1, 1, 2, 3, 4])
        p1, p2 = {m: 1, 0: b}, {n: 1, 0: d_}
        pr = pmul(p1, p2); dp = pder(pr)
        chk(sp.diff(sy(p1) * sy(p2), X), sy(dp)) if sp else None
        w = [poly(pmul(pder(p1), pder(p2))), poly(padd(pmul(pder(p1), p2), pmul(p1, pder(p2)), -1)), poly(pmul(pder(p1), p2))] + pert(dp)
        return add('calc', f"Deriva f(x) = ({Q(p1)})({Q(p2)}) (puedes expandir el resultado).", poly(dp), w, "Regla del producto: (uv)′ = u′v + uv′.", 54 + (m + n) * 2 + (abs(b) + abs(d_)) / 3)
    if k == 1:
        a, n = R.randint(1, 4), R.randint(1, 4)
        inner = {n: a, n - 1: a * n} if n > 1 else {1: a, 0: a}
        ans = f"({poly(inner)})e^x"
        if sp: chk(sp.diff(a * X ** n * sp.exp(X), X), (sy(inner)) * sp.exp(X))
        w = [f"({poly({n - 1: a * n})})e^x", f"({poly({n: a})})e^x", f"({poly({n: a * n, n - 1: a})})e^x" if n > 1 else f"({poly({1: a + 1, 0: a})})e^x", f"({poly({n - 1: a * n})})e^(x-1)"]
        return add('calc', f"Deriva f(x) = {Q({n: a})}·e^x.", ans, w, "(uv)′ = u′v + uv′ con u = axⁿ y v = eˣ; se factoriza eˣ.", 60 + n * 2 + a)
    if k == 2:
        n = R.randint(1, 4); fn = R.choice(['sin', 'cos'])
        if fn == 'sin':
            first = ('' if n == 1 else cf(n, pw(n - 1)) if n > 1 else '')
            ans = f"{(str(n) if n>1 else '')}{pw(n-1)}sin x + {pw(n)}cos x".replace('x sin', 'x sin') if n > 1 else "sin x + x cos x"
            w = [f"{(str(n) if n>1 else '')}{pw(n-1)}cos x" if n > 1 else "cos x", f"{pw(n)}cos x", f"{(str(n) if n>1 else '')}{pw(n-1)}sin x - {pw(n)}cos x" if n > 1 else "sin x - x cos x", f"{(str(n) if n>1 else '')}{pw(n-1)}cos x + {pw(n)}sin x" if n > 1 else "cos x + x sin x"]
            if sp: chk(sp.diff(X ** n * sp.sin(X), X), n * X ** (n - 1) * sp.sin(X) + X ** n * sp.cos(X))
            return add('calc', f"Deriva f(x) = {pw(n)} sin x.", ans.replace('xsin', 'x sin'), [s.replace('xsin', 'x sin').replace('xcos', 'x cos') for s in w], "(uv)′ = u′v + uv′ con u = xⁿ, v = sin x.", 62 + n * 2)
        ans = f"{(str(n) if n>1 else '')}{pw(n-1)}cos x - {pw(n)}sin x" if n > 1 else "cos x - x sin x"
        w = [f"{(str(n) if n>1 else '')}{pw(n-1)}cos x + {pw(n)}sin x" if n > 1 else "cos x + x sin x", f"-{pw(n)}sin x", f"{(str(n) if n>1 else '')}{pw(n-1)}sin x - {pw(n)}cos x" if n > 1 else "sin x - x cos x", f"{pw(n)}sin x - {(str(n) if n>1 else '')}{pw(n-1)}cos x" if n > 1 else "x sin x - cos x"]
        if sp: chk(sp.diff(X ** n * sp.cos(X), X), n * X ** (n - 1) * sp.cos(X) - X ** n * sp.sin(X))
        return add('calc', f"Deriva f(x) = {pw(n)} cos x.", ans.replace('xsin', 'x sin').replace('xcos', 'x cos'), [s.replace('xsin', 'x sin').replace('xcos', 'x cos') for s in w], "(uv)′ = u′v + uv′ con u = xⁿ, v = cos x.", 64 + n * 2)
    n = R.randint(1, 5)
    if n == 1: ans, w = "ln x + 1", ["1/x", "ln x", "x/x + 1", "1 + 1/x"]
    else: ans, w = f"{n}{pw(n-1)} ln x + {pw(n-1)}", [f"{n}{pw(n-1)}/x", f"{pw(n-1)}", f"{n}{pw(n-1)} ln x", f"{n}{pw(n-1)} ln x + {pw(n)}"]
    if sp: chk(sp.diff(X ** n * sp.log(X), X), n * X ** (n - 1) * sp.log(X) + X ** (n - 1))
    return add('calc', f"Deriva f(x) = {pw(n)} ln x.", ans, w, "(uv)′ = u′v + uv′ con u = xⁿ y v = ln x.", 68 + n * 2)


def c_der_quot():
    k = R.randint(0, 2)
    if k == 0:
        p, q_, r, s = R.randint(1, 6), R.randint(-7, 7), R.randint(1, 4), R.randint(-6, 7)
        kk = p * s - q_ * r
        if kk == 0 or s == 0: return False
        den = poly({1: r, 0: s}); num = poly({1: p, 0: q_})
        chk(sp.diff((p * X + q_) / (r * X + s), X), kk / (r * X + s) ** 2) if sp else None
        ans = f"{kk}/({den})²" if kk != 1 else f"1/({den})²"
        w = [f"{-kk}/({den})²", f"{p}/({den})²" if p != kk else f"{p+1}/({den})²", f"{kk}/({den})", f"{p * s + q_ * r}/({den})²" if p * s + q_ * r != kk else f"{kk+2}/({den})²"]
        return add('calc', f"Deriva f(x) = ({Q({1: p, 0: q_})})/({Q({1: r, 0: s})}).", ans.replace('-', '-'), w, "Regla del cociente: (u/v)′ = (u′v − uv′)/v².", 66 + (p + r) + (abs(q_) + abs(s)) / 3, acc=[ans.replace('²', '^2')])
    if k == 1:
        a = R.randint(1, 9)
        ans = f"1 - {a}/x²"
        chk(sp.diff((X ** 2 + a) / X, X), 1 - a / X ** 2) if sp else None
        return add('calc', f"Deriva f(x) = ({Q({2: 1, 0: a})})/x.", ans, [f"1 + {a}/x²", f"2x - {a}/x²", f"1 - {a}/x", f"x - {a}/x²"], "(x² + a)/x = x + a/x, cuya derivada es 1 − a/x².", 62 + a / 2)
    a = R.randint(1, 9)
    ans = f"({a} - x²)/(x² + {a})²"
    chk(sp.diff(X / (X ** 2 + a), X), (a - X ** 2) / (X ** 2 + a) ** 2) if sp else None
    return add('calc', f"Deriva f(x) = x/({Q({2: 1, 0: a})}).", ans, [f"({a} + x²)/(x² + {a})²", f"(x² - {a})/(x² + {a})²", f"1/(2x)", f"({a} - x²)/(x² + {a})"], "(u′v − uv′)/v² = ((x² + a) − 2x²)/(x² + a)².", 76 + a / 2, acc=[ans.replace('²', '^2')])


def c_der_chain():
    k = R.randint(0, 17)
    a, b, n = R.randint(2, 7), R.choice([-5, -3, -2, -1, 1, 2, 3, 4]), R.randint(2, 6)
    lin = poly({1: a, 0: b}); linq = Q({1: a, 0: b})
    if k == 0:
        chk(sp.diff((a * X + b) ** n, X), n * a * (a * X + b) ** (n - 1)) if sp else None
        ans = f"{n*a}({lin}){ex(n-1)}"
        return add('calc', f"Deriva f(x) = ({linq}){sup(n)}." if n <= 3 else f"Deriva f(x) = ({linq})^{n}.", ans, [f"{n}({lin}){ex(n-1)}", f"{n*a}({lin}){ex(n)}", f"{a}({lin}){ex(n-1)}", f"{n}({lin}){ex(n)}"], "Regla de la cadena: n·(u)ⁿ⁻¹·u′ con u′ = a.", 52 + n * 2 + a)
    if k == 1:
        c = R.choice([1, 2, 3, 4, 5]); n = R.randint(2, 5)
        chk(sp.diff((X ** 2 + c) ** n, X), 2 * n * X * (X ** 2 + c) ** (n - 1)) if sp else None
        base = poly({2: 1, 0: c})
        return add('calc', f"Deriva f(x) = ({Q({2: 1, 0: c})})^{n}.".replace('^2', '²') if n == 2 else f"Deriva f(x) = ({Q({2: 1, 0: c})}){sup(n)}.", f"{2*n}x({base}){ex(n-1)}", [f"{n}({base}){ex(n-1)}", f"{2*n}x({base}){ex(n)}", f"{n}x({base}){ex(n-1)}", f"{2}x({base}){ex(n-1)}"], "Cadena: n·u^(n−1)·u′ con u′ = 2x.", 62 + n * 2 + c / 2)
    if k == 2:
        chk(sp.diff(sp.sin(a * X), X), a * sp.cos(a * X)) if sp else None
        return add('calc', f"Deriva f(x) = sin({a}x).", f"{a}cos({a}x)", [f"cos({a}x)", f"-{a}cos({a}x)", f"{a}sin({a}x)", f"-{a}sin({a}x)"], "(sin u)′ = cos u · u′.", 46 + a)
    if k == 3:
        chk(sp.diff(sp.cos(a * X), X), -a * sp.sin(a * X)) if sp else None
        return add('calc', f"Deriva f(x) = cos({a}x).", f"-{a}sin({a}x)", [f"{a}sin({a}x)", f"-sin({a}x)", f"{a}cos({a}x)", f"-{a}cos({a}x)"], "(cos u)′ = −sin u · u′.", 48 + a)
    if k == 4:
        chk(sp.diff(sp.exp(a * X), X), a * sp.exp(a * X)) if sp else None
        return add('calc', f"Deriva f(x) = e^({a}x).", f"{a}e^({a}x)", [f"e^({a}x)", f"e^({a}x)/{a}", f"{a}xe^({a}x)", f"{a}e^x"], "(e^u)′ = e^u · u′.", 46 + a)
    if k == 5:
        chk(sp.diff(sp.log(a * X + b), X), a / (a * X + b)) if sp else None
        return add('calc', f"Deriva f(x) = ln({linq}).", f"{a}/({lin})", [f"1/({lin})", f"{a}/({lin})²", f"{a}ln({lin})", f"({lin})/{a}"], "(ln u)′ = u′/u.", 56 + a)
    if k == 6:
        c = R.randint(1, 5)
        chk(sp.diff(sp.sin(c * X ** 2), X), 2 * c * X * sp.cos(c * X ** 2)) if sp else None
        cc = '' if c == 1 else str(c)
        return add('calc', f"Deriva f(x) = sin({cc}x²).", f"{2*c}x cos({cc}x²)", [f"cos({cc}x²)", f"{2*c}x sin({cc}x²)", f"-{2*c}x cos({cc}x²)", f"{c}x cos({cc}x²)" if c != 2 else f"3x cos({cc}x²)"], "(sin u)′ = cos u · u′ con u′ = 2cx.", 66 + c)
    if k == 7:
        c = R.randint(1, 5); cc = '' if c == 1 else str(c)
        chk(sp.diff(sp.exp(c * X ** 2), X), 2 * c * X * sp.exp(c * X ** 2)) if sp else None
        return add('calc', f"Deriva f(x) = e^({cc}x²).", f"{2*c}x e^({cc}x²)", [f"e^({cc}x²)", f"{c}x e^({cc}x²)" if c != 2 else "3x e^(2x²)", f"{2*c}x e^({cc}x)", f"{cc}x² e^({cc}x²)"], "(e^u)′ = e^u · u′ con u′ = 2cx.", 68 + c)
    if k == 8:
        c = R.randint(1, 5); cc = '' if c == 1 else str(c)
        chk(sp.diff(sp.cos(c * X ** 2), X), -2 * c * X * sp.sin(c * X ** 2)) if sp else None
        return add('calc', f"Deriva f(x) = cos({cc}x²).", f"-{2*c}x sin({cc}x²)", [f"{2*c}x sin({cc}x²)", f"-sin({cc}x²)", f"-{2*c}x cos({cc}x²)", f"-{c}x sin({cc}x²)" if c != 2 else "-3x sin(2x²)"], "(cos u)′ = −sin u · u′.", 70 + c)
    if k == 9:
        c = R.randint(1, 9)
        chk(sp.diff(sp.log(X ** 2 + c), X), 2 * X / (X ** 2 + c)) if sp else None
        return add('calc', f"Deriva f(x) = ln({Q({2: 1, 0: c})}).", f"2x/({poly({2: 1, 0: c})})", [f"1/({poly({2: 1, 0: c})})", f"2x/({poly({2: 1, 0: c})})²", f"2x ln({poly({2: 1, 0: c})})", f"x/({poly({2: 1, 0: c})})"], "(ln u)′ = u′/u con u′ = 2x.", 70 + c / 2)
    if k == 10:
        c = R.randint(2, 9)
        chk(sp.diff(sp.sqrt(a * X + c), X), a / (2 * sp.sqrt(a * X + c))) if sp else None
        l2 = poly({1: a, 0: c})
        return add('calc', f"Deriva f(x) = √({Q({1: a, 0: c})}).", f"{a}/(2√({l2}))", [f"1/(2√({l2}))", f"{a}/√({l2})", f"{a}√({l2})/2", f"{2*a}/√({l2})"], "(√u)′ = u′/(2√u).", 74 + a / 2)
    if k == 11:
        m = R.randint(2, 5)
        if m == 2:
            chk(sp.diff(sp.sin(X) ** 2, X), 2 * sp.sin(X) * sp.cos(X)) if sp else None
            return add('calc', "Deriva f(x) = sin²x.", "2sin x cos x", ["2sin x", "2cos x", "sin x cos x", "-2sin x cos x"], "Cadena: 2·sin x · cos x.", 72, acc=['2 sin x cos x', 'sin(2x)', 'sin 2x'])
        chk(sp.diff(sp.sin(X) ** m, X), m * sp.sin(X) ** (m - 1) * sp.cos(X)) if sp else None
        return add('calc', f"Deriva f(x) = sin{sup(m)}x.", f"{m}sin{sup(m-1)}x cos x", [f"{m}sin{sup(m-1)}x", f"{m}cos{sup(m-1)}x", f"sin{sup(m-1)}x cos x", f"-{m}sin{sup(m-1)}x cos x"], "Cadena: n·sinⁿ⁻¹x·cos x.", 72 + m, acc=[f"{m} sin{sup(m-1)}x cos x"])
    if k == 12:
        chk(sp.diff(sp.exp(sp.sin(X)), X), sp.cos(X) * sp.exp(sp.sin(X))) if sp else None
        return add('calc', "Deriva f(x) = e^(sin x).", "cos x e^(sin x)", ["e^(sin x)", "sin x e^(sin x)", "-cos x e^(sin x)", "cos x e^(cos x)"], "(e^u)′ = e^u · u′ con u = sin x.", 76, acc=['cos x·e^(sin x)', 'e^(sin x)cos x'])
    if k == 13:
        chk(sp.diff(sp.log(sp.sin(X)), X), sp.cos(X) / sp.sin(X)) if sp else None
        return add('calc', "Deriva f(x) = ln(sin x).", "cos x/sin x", ["1/sin x", "sin x/cos x", "-cos x/sin x", "cos x ln x"], "(ln u)′ = u′/u = cos x/sin x = cot x.", 76, acc=['cot x'])
    if k == 14:
        chk(sp.diff(sp.sin(sp.exp(X)), X), sp.exp(X) * sp.cos(sp.exp(X))) if sp else None
        return add('calc', "Deriva f(x) = sin(e^x).", "e^x cos(e^x)", ["cos(e^x)", "e^x sin(e^x)", "-e^x cos(e^x)", "cos(e^x)e^(x-1)"], "(sin u)′ = cos u · u′ con u = eˣ.", 74, acc=['cos(e^x)e^x'])
    if k == 15:
        c = R.randint(1, 9)
        chk(sp.diff(sp.sqrt(X ** 2 + c), X), X / sp.sqrt(X ** 2 + c)) if sp else None
        return add('calc', f"Deriva f(x) = √({Q({2: 1, 0: c})}).", f"x/√({poly({2: 1, 0: c})})", [f"1/(2√({poly({2: 1, 0: c})}))", f"2x/√({poly({2: 1, 0: c})})", f"x√({poly({2: 1, 0: c})})", f"x/({poly({2: 1, 0: c})})"], "(√u)′ = u′/(2√u) = 2x/(2√u) = x/√u.", 80 + c / 2)
    if k == 16:
        chk(sp.diff(sp.tan(a * X), X), a / sp.cos(a * X) ** 2) if sp else None
        return add('calc', f"Deriva f(x) = tan({a}x).", f"{a}sec²({a}x)", [f"sec²({a}x)", f"{a}sec({a}x)", f"{a}tan({a}x)", f"-{a}sec²({a}x)"], "(tan u)′ = sec²u · u′.", 60 + a)
    c = R.randint(2, 6)
    chk(sp.diff(sp.exp(a * X + b), X), a * sp.exp(a * X + b)) if sp else None
    return add('calc', f"Deriva f(x) = e^({linq}).", f"{a}e^({lin})", [f"e^({lin})", f"({lin})e^({lin})", f"{a}e^({a})", f"e^({a})"], "(e^u)′ = e^u · u′ con u′ = a.", 58 + a)


def c_implicit():
    k = R.randint(0, 3); r = R.randint(2, 15)
    if k == 0:
        return add('calc', f"Si x² + y² = {r*r}, ¿cuánto vale dy/dx (derivación implícita)?", "-x/y", ["x/y", "-y/x", "y/x", "-2x/y²" if False else "-x/(2y)"], "2x + 2y·y′ = 0 ⇒ y′ = −x/y.", 88 + r / 8)
    if k == 1:
        return add('calc', f"Si xy = {r}, ¿cuánto vale dy/dx?", "-y/x", ["y/x", "-x/y", f"{r}/x", f"-{r}/x" if False else "x/y"], "y + x·y′ = 0 ⇒ y′ = −y/x.", 88 + r / 8)
    if k == 2:
        return add('calc', f"Si y² = {r}x, ¿cuánto vale dy/dx?", f"{r}/(2y)", [f"{r}/y", f"2y/{r}", f"{r}/(2x)", f"{r}y/2"], f"2y·y′ = {r} ⇒ y′ = {r}/(2y).", 89 + r / 8)
    return add('calc', f"Si x³ + y³ = {r}, ¿cuánto vale dy/dx?", "-x²/y²", ["x²/y²", "-y²/x²", "-x/y", "-x²/y"], "3x² + 3y²·y′ = 0 ⇒ y′ = −x²/y².", 91 + r / 8)


def c_tangent():
    deg = R.randint(2, 3); p = rand_poly(deg, -6, 6); a = R.randint(-3, 3)
    if len(p) < 2: return False
    m = peval(pder(p), a); y0 = peval(p, a); b = y0 - m * a
    k = R.randint(0, 2)
    if k == 0:
        return add('calc', f"¿Cuál es la pendiente de la recta tangente a f(x) = {Q(p)} en x = {a}?", nf(m), numwrong(m, extra=[nf(y0)]), f"Es f′({a}) = {nf(m)}.", 44 + deg * 4 + abs(a))
    if k == 1:
        ans = "y = " + poly({1: m, 0: b})
        w = ["y = " + poly({1: m, 0: y0}), "y = " + poly({1: -m, 0: b}), "y = " + poly({1: m, 0: -b}), "y = " + poly({1: y0, 0: b})]
        return add('calc', f"¿Cuál es la ecuación de la recta tangente a f(x) = {Q(p)} en x = {a}?", ans, w, f"m = f′({a}) = {nf(m)}, f({a}) = {nf(y0)}; y − {nf(y0)} = {nf(m)}(x − {a}).", 60 + deg * 4 + abs(a), acc=[ans.replace(' ', '')])
    if m == 0: return False
    s = -1 / m
    return add('calc', f"¿Cuál es la pendiente de la recta normal a f(x) = {Q(p)} en x = {a}?", nf(s), [nf(m), nf(-m), nf(1 / m), nf(s + 1)], f"La normal es perpendicular a la tangente: −1/f′({a}) = {nf(s)}.", 70 + deg * 3 + abs(a), acc=[best(s)])


def c_crit():
    k = R.randint(0, 5)
    if k == 0:
        a = R.choice([1, 2, 3, -1, -2]); h = R.randint(-6, 7); c = R.randint(-9, 9)
        if h == 0: return False
        p = {2: a, 1: -2 * a * h, 0: c}
        return add('calc', f"¿En qué valor de x tiene f(x) = {Q(p)} su punto crítico?", h, numwrong(h, extra=[-h, 2 * h]), f"f′(x) = {poly(pder(p))} = 0 ⇒ x = {h}.", 40 + abs(a) * 3 + abs(h) / 2)
    if k == 1:
        a = R.choice([1, 2, 3, 4]); h = R.randint(-5, 6); c = R.randint(-9, 9)
        p = {2: a, 1: -2 * a * h, 0: c}; v = peval(p, h)
        return add('calc', f"¿Cuál es el valor mínimo de f(x) = {Q(p)}?", nf(v), numwrong(v, extra=[nf(h), nf(c)]), f"El mínimo ocurre en x = {h} y vale f({h}) = {nf(v)}.", 56 + a * 2 + abs(h) / 2)
    if k == 2:
        m = R.randint(1, 5)
        p = {3: 1, 1: -3 * m * m}
        return add('calc', f"¿En qué valor de x tiene f(x) = {Q(p)} un máximo local?", -m, [m, 0, -m - 1, m * m], f"f′(x) = 3x² − {3*m*m} = 0 ⇒ x = ±{m}; f″(x) = 6x < 0 en x = {-m}.", 62 + m * 2)
    if k == 3:
        m = R.randint(1, 5)
        p = {3: 1, 1: -3 * m * m}
        return add('calc', f"¿En qué valor de x tiene f(x) = {Q(p)} un mínimo local?", m, [-m, 0, m + 1, m * m], f"f′(x) = 3x² − {3*m*m} = 0 ⇒ x = ±{m}; f″({m}) = {6*m} > 0.", 62 + m * 2)
    if k == 4:
        bb = R.choice([-9, -6, -3, 3, 6, 9]); cc, dd = R.randint(-6, 6), R.randint(-8, 8)
        p = {3: 1, 2: bb, 1: cc, 0: dd}
        return add('calc', f"¿En qué valor de x tiene f(x) = {Q(p)} su punto de inflexión?", nf(F(-bb, 3)), numwrong(F(-bb, 3), extra=[nf(F(bb, 3)), nf(-bb)]), f"f″(x) = 6x + {2*bb} = 0 ⇒ x = {nf(F(-bb,3))}.", 74 + abs(bb) / 3)
    h = R.randint(-6, 7); c = R.randint(-9, 9)
    if h == 0: return False
    p = {2: 1, 1: -2 * h, 0: c}
    return add('calc', f"¿Para qué valores de x es creciente f(x) = {Q(p)}?", f"x > {h}", [f"x < {h}", f"x > {-h}", f"x < {-h}", f"x > {2*h}"], f"f′(x) = 2x − {2*h} > 0 ⇒ x > {h}.", 50 + abs(h) / 2, acc=[f"x>{h}"])


def c_rates():
    k = R.randint(0, 4)
    if k == 0:
        a, b, c, t = R.randint(1, 5), R.randint(-6, 8), R.randint(0, 9), R.randint(1, 6)
        s = 2 * a * t + b
        return add('calc', f"La posición de una partícula es s(t) = {Q({2: a, 1: b, 0: c})}. ¿Cuál es su velocidad en t = {t}?", s, numwrong(s, extra=[peval({2: a, 1: b, 0: c}, t)]), f"v(t) = s′(t) = {2*a}t + ({b}); v({t}) = {s}.", 40 + a * 2 + t)
    if k == 1:
        a, b, c = R.randint(1, 6), R.randint(-6, 8), R.randint(0, 9)
        return add('calc', f"La posición de una partícula es s(t) = {Q({2: a, 1: b, 0: c})}. ¿Cuál es su aceleración?", 2 * a, numwrong(2 * a, pos=True, extra=[a, b]), f"a(t) = s″(t) = {2*a}.", 46 + a)
    if k == 2:
        m = R.randint(1, 6)
        return add('calc', f"La posición es s(t) = {Q({3: 1, 1: -3 * m * m})} para t ≥ 0. ¿En qué instante t > 0 se detiene la partícula (v = 0)?", m, [m + 1, -m, m * m, 3 * m], f"v(t) = 3t² − {3*m*m} = 0 ⇒ t = {m}.", 58 + m * 2)
    if k == 3:
        r, rp = R.randint(2, 9), R.randint(1, 4)
        return add('calc', f"El radio de un círculo crece a {rp} cm/s. ¿Con qué rapidez crece el área cuando r = {r} cm?", f"{2*r*rp}π", [f"{r*rp}π", f"{r*r*rp}π", f"{2*r*r*rp}π", f"{2*r}π"], "A = πr² ⇒ dA/dt = 2πr·dr/dt.", 82 + r / 2, acc=[f"{2*r*rp}pi", f"{2*r*rp} pi"])
    s_, sr = R.randint(2, 8), R.randint(1, 3)
    return add('calc', f"La arista de un cubo crece a {sr} cm/s. ¿Con qué rapidez crece el volumen cuando la arista mide {s_} cm?", 3 * s_ * s_ * sr, numwrong(3 * s_ * s_ * sr, pos=True, extra=[s_ ** 3 * sr, 3 * s_ * sr]), "V = s³ ⇒ dV/dt = 3s²·ds/dt.", 82 + s_ / 2)


def c_opt():
    k = R.randint(0, 3)
    if k == 0:
        P = 4 * R.randint(3, 40)
        return add('calc', f"Con {P} m de cerca se encierra un terreno rectangular. ¿Cuál es el área máxima posible en m²?", (P // 4) ** 2, numwrong((P // 4) ** 2, pos=True, extra=[P * P // 8]), f"El máximo es un cuadrado de lado {P//4}: {(P//4)**2}.", 78 + P / 40)
    if k == 1:
        S = 2 * R.randint(3, 30)
        return add('calc', f"Dos números positivos suman {S}. ¿Cuál es el máximo valor posible de su producto?", (S // 2) ** 2, numwrong((S // 2) ** 2, pos=True, extra=[S * S // 2]), f"x(S − x) es máximo en x = S/2: {(S//2)**2}.", 72 + S / 20)
    if k == 2:
        b = 2 * R.randint(1, 8); c = R.randint(-9, 9)
        p = {2: -1, 1: b, 0: c}; v = c + (b * b) // 4
        return add('calc', f"¿Cuál es el valor máximo de f(x) = {Q(p)}?", v, numwrong(v, extra=[b // 2, c]), f"El máximo ocurre en x = {b//2} y vale {v}.", 62 + b / 2)
    P = 4 * R.randint(2, 20)
    A = P * P // 8
    return add('calc', f"Se dispone de {P} m de cerca para un corral rectangular junto a un río (el lado del río no necesita cerca). ¿Cuál es el área máxima en m²?", A, numwrong(A, pos=True, extra=[(P // 4) ** 2, P * P // 16]), f"A = x({P} − 2x) es máximo en x = {P//4}: A = {A}.", 84 + P / 20)


# ---------------------------------------------------------------- integrales
def cpoly(p):
    return poly(pint(p)) + " + C"


def c_int_basic():
    k = R.randint(0, 4)
    if k == 0:
        n = R.randint(1, 9); p = {n: 1}
        ans = cpoly(p)
        w = [poly({n - 1: n}) + " + C", poly({n + 1: 1}) + " + C", poly({n + 1: F(1, n)}) + " + C", poly({n: F(1, n)}) + " + C", poly({n + 1: F(1, n + 1)})]
        chk(sp.diff(sy(pint(p)), X), sy(p)) if sp else None
        return add('calc', f"¿Cuál es la integral indefinida de {Q(p)} dx?", ans, w, "∫xⁿ dx = xⁿ⁺¹/(n + 1) + C.", 14 + n * 2, acc=[ans.replace(' + C', '+C'), ans.replace(' + C', '')])
    if k == 1:
        n = R.randint(1, 6); a = R.choice([2, 3, 4, 5, 6, 8, -2, -3])
        p = {n: a}; ans = cpoly(p)
        w = [poly({n - 1: a * n}) + " + C", poly({n + 1: a}) + " + C", poly({n + 1: F(1, n + 1)}) + " + C", poly({n + 1: F(a, n)}) + " + C"]
        return add('calc', f"¿Cuál es la integral indefinida de {Q(p)} dx?", ans, w, "Se integra la potencia y se conserva el coeficiente.", 22 + n * 2 + abs(a))
    if k == 2:
        deg = R.randint(2, 4); p = rand_poly(deg, -8, 8)
        if len(p) < 2: return False
        chk(sp.diff(sy(pint(p)), X), sy(p)) if sp else None
        ans = cpoly(p)
        w = [poly(pder(p)) + " + C", poly(pint(p)), poly({k_ + 1: v for k_, v in p.items()}) + " + C"] + [x + " + C" for x in pert(pint(p))]
        return add('calc', f"Calcula ∫({Q(p)}) dx.", ans, w, "Se integra término a término y se suma la constante C.", 30 + deg * 4 + len(p) * 2)
    if k == 3:
        c = R.randint(2, 15)
        return add('calc', f"¿Cuál es la integral indefinida de {c} dx?", f"{c}x + C", [f"{c} + C", "x + C", f"{c}x² + C", f"{c}/x + C"], "La integral de una constante c es cx + C.", 10 + c / 3, acc=[f"{c}x+C"])
    j = R.randint(0, 5)
    tab = [("e^x", "e^x + C", ["e^x", "x e^x + C", "e^(x+1) + C"], 22), ("cos x", "sin x + C", ["-sin x + C", "cos x + C", "-cos x + C"], 22), ("sin x", "-cos x + C", ["cos x + C", "sin x + C", "-sin x + C"], 22),
           ("1/x", "ln|x| + C", ["1/x² + C", "-1/x² + C", "x ln x + C"], 28), ("sec²x", "tan x + C", ["sec x + C", "-tan x + C", "cot x + C"], 38), ("1/x²", "-1/x + C", ["1/x + C", "ln x² + C", "-2/x³ + C"], 36)]
    f_, ans, w, d = tab[j]
    return add('calc', f"¿Cuál es la integral indefinida de {f_} dx?", ans, w, "Es una integral básica de tabla.", d, acc=[ans.replace(' ', '')])


def c_int_def():
    k = R.randint(0, 2)
    deg = R.randint(1, 3); p = rand_poly(deg, -6, 6)
    a = R.randint(-3, 2); b = a + R.randint(1, 4)
    P = pint(p); val = peval(P, b) - peval(P, a)
    if sp: assert sp.integrate(sy(p), (X, a, b)) == rat(val)
    if k == 0:
        return add('calc', f"¿Cuánto vale la integral definida de {a} a {b} de ({Q(p)}) dx?", nf(val), [nf(peval(P, b)), nf(peval(P, a) - peval(P, b)), nf(peval(P, b) + peval(P, a)), nf(peval(p, b) - peval(p, a))], f"Se evalúa la antiderivada: F({b}) − F({a}) = {nf(val)}.", 38 + deg * 5 + (b - a) * 2, acc=[best(val)])
    if k == 1:
        n = R.randint(1, 4); bb = R.randint(1, 5)
        v = F(bb ** (n + 1), n + 1)
        return add('calc', f"¿Cuál es el área bajo la curva y = {Q({n: 1})} entre x = 0 y x = {bb}?", nf(v), [nf(F(bb ** n)), nf(F(bb ** (n + 1))), nf(F(bb ** (n + 1), n)), nf(F(bb ** (n + 1), n + 1) + 1)], f"∫₀^{bb} xⁿ dx = {bb}^{n+1}/{n+1} = {nf(v)}.", 40 + n * 4 + bb, acc=[best(v)])
    a2 = R.choice([2, 3, 4, 5, 6]); b2 = R.randint(1, 6)
    v = F(a2 * b2 * b2, 2)
    return add('calc', f"¿Cuánto vale la integral definida de 0 a {b2} de {a2}x dx?", nf(v), [nf(F(a2 * b2)), nf(F(a2 * b2 * b2)), nf(F(a2 * b2 * b2, 3)), nf(v + a2)], f"∫₀^{b2} {a2}x dx = {a2}·{b2}²/2.", 34 + a2 + b2, acc=[best(v)])


def c_int_ea():
    k = R.randint(0, 4); a = R.randint(2, 9); b = R.choice([-5, -3, -2, 1, 2, 3, 4]); n = R.randint(2, 5)
    lin = poly({1: a, 0: b})
    if k == 0:
        chk(sp.diff(sp.exp(a * X) / a, X), sp.exp(a * X)) if sp else None
        return add('calc', f"¿Cuál es la integral indefinida de e^({a}x) dx?", f"e^({a}x)/{a} + C", [f"{a}e^({a}x) + C", f"e^({a}x) + C", f"e^({a}x)/{a+1} + C" if a < 9 else "e^(9x)/8 + C", f"x e^({a}x) + C"], "∫e^(ax) dx = e^(ax)/a + C.", 58 + a)
    if k == 1:
        return add('calc', f"¿Cuál es la integral indefinida de cos({a}x) dx?", f"sin({a}x)/{a} + C", [f"{a}sin({a}x) + C", f"-sin({a}x)/{a} + C", f"sin({a}x) + C", f"-{a}sin({a}x) + C"], "∫cos(ax) dx = sin(ax)/a + C.", 60 + a)
    if k == 2:
        return add('calc', f"¿Cuál es la integral indefinida de sin({a}x) dx?", f"-cos({a}x)/{a} + C", [f"cos({a}x)/{a} + C", f"-{a}cos({a}x) + C", f"-cos({a}x) + C", f"{a}cos({a}x) + C"], "∫sin(ax) dx = −cos(ax)/a + C.", 62 + a)
    if k == 3:
        chk(sp.diff((a * X + b) ** (n + 1) / (a * (n + 1)), X), (a * X + b) ** n) if sp else None
        return add('calc', f"¿Cuál es la integral indefinida de ({Q({1: a, 0: b})})^{n} dx?" if n > 3 else f"¿Cuál es la integral indefinida de ({Q({1: a, 0: b})}){sup(n)} dx?", f"({lin}){sup(n+1) if n+1<=3 else '^'+str(n+1)}/{a*(n+1)} + C", [f"({lin}){sup(n+1) if n+1<=3 else '^'+str(n+1)}/{n+1} + C", f"({lin}){sup(n+1) if n+1<=3 else '^'+str(n+1)} + C", f"{n+1}({lin}){sup(n) if n<=3 else '^'+str(n)} + C", f"({lin}){sup(n+1) if n+1<=3 else '^'+str(n+1)}/{a} + C"], "Se integra la potencia y se divide entre la derivada de la expresión interior.", 70 + n + a / 2)
    chk(sp.diff(sp.log(sp.Abs(a * X + b)) / a, X), 1 / (a * X + b)) if False else None
    return add('calc', f"¿Cuál es la integral indefinida de 1/({Q({1: a, 0: b})}) dx?", f"ln|{lin}|/{a} + C", [f"ln|{lin}| + C", f"{a}ln|{lin}| + C", f"-1/({lin})² + C", f"1/{a}({lin})² + C" if False else f"-{a}/({lin})² + C"], "∫1/(ax + b) dx = ln|ax + b|/a + C.", 68 + a / 2)


def c_int_sub():
    k = R.randint(0, 5)
    if k == 0:
        a, n = R.randint(1, 8), R.randint(2, 6)
        m = n + 1  # ∫ 2(n+1) x (x²+a)^n = (x²+a)^(n+1)
        base = poly({2: 1, 0: a})
        ans = f"({base})^{n+1} + C"
        return add('calc', f"Calcula ∫ {2*m}x({Q({2: 1, 0: a})})^{n} dx.", ans, [f"({base})^{n+1}/{n+1} + C", f"{2*m}({base})^{n+1} + C", f"({base})^{n} + C", f"{m}({base})^{n+1} + C"], f"Con u = x² + {a}, du = 2x dx: ∫{m}·u^{n} du = u^{n+1}.", 78 + n * 2, acc=[f"({base})^{n+1}+C"])
    if k == 1:
        a = R.randint(1, 6)
        cc = '' if a == 1 else str(a)
        return add('calc', f"Calcula ∫ {2*a}x e^({cc}x²) dx.", f"e^({cc}x²) + C", [f"{2*a}e^({cc}x²) + C", f"x e^({cc}x²) + C", f"e^({cc}x²)/{2*a} + C", f"{a}e^({cc}x²) + C"], f"Con u = {cc}x², du = {2*a}x dx.", 78 + a)
    if k == 2:
        a = R.randint(1, 9)
        return add('calc', f"Calcula ∫ 2x/({Q({2: 1, 0: a})}) dx.", f"ln({poly({2: 1, 0: a})}) + C", [f"1/({poly({2: 1, 0: a})}) + C", f"2x ln({poly({2: 1, 0: a})}) + C", f"ln|x| + C", f"x²ln({poly({2: 1, 0: a})}) + C"], f"Con u = x² + {a}, la integral es ∫du/u.", 80 + a / 2, acc=[f"ln|{poly({2: 1, 0: a})}| + C"])
    if k == 3:
        n = R.randint(1, 5)
        return add('calc', f"Calcula ∫ cos x·(sin x)^{n} dx." if n > 3 else f"Calcula ∫ cos x · sin{sup(n)}x dx." if n > 1 else "Calcula ∫ cos x · sin x dx.", f"sin{sup(n+1) if n+1<=3 else '^'+str(n+1)}x/{n+1} + C", [f"sin{sup(n+1) if n+1<=3 else '^'+str(n+1)}x + C", f"-sin{sup(n+1) if n+1<=3 else '^'+str(n+1)}x/{n+1} + C", f"cos{sup(n+1) if n+1<=3 else '^'+str(n+1)}x/{n+1} + C", f"sin{sup(n) if n<=3 else '^'+str(n)}x/{n} + C"], "Con u = sin x, du = cos x dx.", 76 + n * 2)
    if k == 4:
        n = R.randint(1, 4)
        return add('calc', f"Calcula ∫ sin x cos{sup(n)}x dx." if n > 1 else "Calcula ∫ sin x cos x dx.", f"-cos{sup(n+1) if n+1<=3 else '^'+str(n+1)}x/{n+1} + C", [f"cos{sup(n+1) if n+1<=3 else '^'+str(n+1)}x/{n+1} + C", f"-cos{sup(n+1) if n+1<=3 else '^'+str(n+1)}x + C", f"sin{sup(n+1) if n+1<=3 else '^'+str(n+1)}x/{n+1} + C", f"-cos{sup(n) if n<=3 else '^'+str(n)}x/{n} + C"], "Con u = cos x, du = −sin x dx.", 78 + n * 2)
    a = R.randint(2, 6)
    return add('calc', f"Calcula ∫ e^x cos(e^x) dx." if a == 2 else f"Calcula ∫ {a}e^x cos(e^x) dx.", "sin(e^x) + C" if a == 2 else f"{a}sin(e^x) + C", ["cos(e^x) + C", "-sin(e^x) + C", "e^x sin(e^x) + C"] + ([f"sin(e^x)/{a} + C"] if a != 2 else ["sin(x) + C"]), "Con u = eˣ, du = eˣ dx.", 80 + a)


def c_int_parts():
    k = R.randint(0, 8); c = R.randint(1, 8); K = '' if c == 1 else str(c)
    items = [
        ("x e^x", f"{K}(x - 1)e^x + C", [f"{K}(x + 1)e^x + C", f"{K}x e^x + C", f"{K}x²e^x/2 + C", f"{K}(x - 1)e^(x-1) + C"]),
        ("x cos x", f"{K}(x sin x + cos x) + C", [f"{K}(x sin x - cos x) + C", f"{K}(-x sin x + cos x) + C", f"{K}x sin x + C", f"{K}(x cos x + sin x) + C"]),
        ("x sin x", f"{K}(sin x - x cos x) + C", [f"{K}(sin x + x cos x) + C", f"{K}(x cos x - sin x) + C", f"-{K}x cos x + C", f"{K}(cos x - x sin x) + C"]),
        ("ln x", f"{K}(x ln x - x) + C", [f"{K}(x ln x + x) + C", f"{K}ln x/x + C", f"{K}(1/x) + C", f"{K}x ln x + C"]),
        ("x ln x", f"{K}(x²ln x/2 - x²/4) + C", [f"{K}(x²ln x/2 + x²/4) + C", f"{K}(x²ln x - x²) + C", f"{K}x²ln x/2 + C", f"{K}(ln x/2 - x/4) + C"]),
        ("x² e^x", f"{K}(x² - 2x + 2)e^x + C", [f"{K}(x² + 2x + 2)e^x + C", f"{K}(x² - 2x)e^x + C", f"{K}x³e^x/3 + C", f"{K}(x² - 2x + 2)e^(x²) + C"]),
        ("x e^(-x)", f"-{K}(x + 1)e^(-x) + C", [f"{K}(x + 1)e^(-x) + C", f"-{K}(x - 1)e^(-x) + C", f"-{K}x e^(-x) + C", f"{K}(x - 1)e^(-x) + C"]),
    ]
    if k <= 6:
        f_, ans, w = items[k]
        fx = f"{K}{f_}" if K else f_
        fq = (f"{c}·{f_}" if c > 1 else f_)
        return add('calc', f"Calcula ∫ {fq} dx (integración por partes).", ans, w, "Se usa ∫u dv = uv − ∫v du con una elección adecuada de u y dv.", 84 + k + c / 2)
    a = R.randint(2, 5)
    if k == 7:
        return add('calc', f"Calcula ∫ {a*a}x e^({a}x) dx.", f"({a}x - 1)e^({a}x) + C", [f"({a}x + 1)e^({a}x) + C", f"{a}x e^({a}x) + C", f"({a}x - 1)e^({a}x)/{a} + C", f"({a*a}x - 1)e^({a}x) + C"], "Por partes: ∫x e^(ax) dx = (ax − 1)e^(ax)/a².", 92 + a)
    return add('calc', f"Calcula ∫ x e^({a}x) dx.", f"({a}x - 1)e^({a}x)/{a*a} + C", [f"({a}x + 1)e^({a}x)/{a*a} + C", f"({a}x - 1)e^({a}x)/{a} + C", f"x e^({a}x)/{a} + C", f"({a}x - 1)e^({a}x) + C"], "Por partes: ∫x e^(ax) dx = (ax − 1)e^(ax)/a².", 94 + a)


def c_area():
    k = R.randint(0, 4)
    if k == 0:
        kk = R.randint(1, 8)
        return add('calc', f"¿Cuál es el área encerrada entre y = {kk}x y y = x²?", nf(F(kk ** 3, 6)), [nf(F(kk ** 3, 3)), nf(F(kk ** 2, 2)), nf(F(kk ** 3, 2)), nf(F(kk ** 3, 6) + 1)], f"∫₀^{kk} ({kk}x − x²) dx = {kk}³/2 − {kk}³/3 = {nf(F(kk**3,6))}.", 80 + kk, acc=[best(F(kk ** 3, 6))])
    if k == 1:
        kk = R.randint(1, 6)
        v = F(4 * kk ** 3, 3)
        return add('calc', f"¿Cuál es el área entre y = {kk*kk} − x² y el eje x?", nf(v), [nf(F(2 * kk ** 3, 3)), nf(F(kk ** 3, 3)), nf(F(4 * kk ** 3, 3) + kk), nf(F(8 * kk ** 3, 3))], f"∫ de −{kk} a {kk} de ({kk*kk} − x²) dx = 4·{kk}³/3.", 82 + kk, acc=[best(v)])
    if k == 2:
        n = R.randint(1, 4); b = R.randint(1, 4); a = R.randint(1, 5)
        v = F(a * b ** (n + 1), n + 1)
        return add('calc', f"¿Cuál es el área bajo y = {Q({n: a})} entre x = 0 y x = {b}?", nf(v), [nf(F(a * b ** n)), nf(F(a * b ** (n + 1))), nf(F(b ** (n + 1), n + 1)), nf(v + a)], f"∫₀^{b} {a}xⁿ dx = {nf(v)}.", 58 + n * 3 + b, acc=[best(v)])
    if k == 3:
        b = R.randint(2, 5)
        return add('calc', f"¿Cuánto vale la integral definida de x³ entre 0 y {b}?", nf(F(b ** 4, 4)), [nf(F(b ** 3, 3)), nf(F(b ** 4)), nf(F(b ** 4, 3)), nf(F(b ** 4, 4) + b)], f"{b}⁴/4 = {nf(F(b**4,4))}.", 48 + b * 2, acc=[best(F(b ** 4, 4))])
    return add('calc', "¿Cuánto vale ∫ de 0 a π de sin x dx?", 2, ['0', '1', '-2', 'π'], "−cos π + cos 0 = 1 + 1 = 2.", 72) if R.random() < 0.02 else False


def c_ftc():
    k = R.randint(0, 3)
    if k == 0:
        b = R.randint(1, 9)
        return add('calc', f"¿Cuál es el valor promedio de f(x) = x² en el intervalo [0, {b}]?", nf(F(b * b, 3)), [nf(F(b * b, 2)), nf(F(b ** 3, 3)), nf(F(b * b)), nf(F(b, 3))], f"(1/{b})·∫₀^{b} x² dx = {b}²/3.", 76 + b / 2, acc=[best(F(b * b, 3))])
    if k == 1:
        a = R.randint(0, 6); b = a + 2 * R.randint(1, 5)
        return add('calc', f"¿Cuál es el valor promedio de f(x) = x en el intervalo [{a}, {b}]?", nf(F(a + b, 2)), [nf(F(a + b)), nf(F(b - a, 2)), nf(F(b * b - a * a, 2)), nf(F(a + b, 2) + 1)], "El promedio es (1/(b−a))·∫x dx = (a + b)/2.", 70 + b / 2, acc=[best(F(a + b, 2))])
    if k == 2:
        n = R.randint(2, 6)
        return add('calc', f"Si F(x) = ∫ de 0 a x de t^{n} dt, ¿cuánto vale F′(x)?" if n > 3 else f"Si F(x) = ∫ de 0 a x de t{sup(n)} dt, ¿cuánto vale F′(x)?", f"x{sup(n)}" if n <= 3 else f"x^{n}", [f"x{sup(n+1)}/{n+1}" if n + 1 <= 3 else f"x^{n+1}/{n+1}", f"{n}x{sup(n-1)}" if n - 1 > 1 else f"{n}x", "0"] + [f"t{sup(n)}" if n <= 3 else f"t^{n}"], "Teorema fundamental del cálculo: F′(x) = f(x).", 74 + n)
    m = R.randint(1, 8)
    return add('calc', f"¿Cuánto vale la integral definida de −{m} a {m} de x³ dx?", 0, [f"{m**4//2}" if m ** 4 % 2 == 0 else f"{m**4}", f"{m**4}", f"{2*m**4}", f"-{m**4}"], "x³ es impar y el intervalo es simétrico, así que la integral es 0.", 62 + m / 2)


def c_lhop():
    k = R.randint(0, 4); a = R.randint(2, 9)
    if k == 0:
        if sp: assert sp.limit((sp.exp(a * X) - 1) / X, X, 0) == a
        return add('calc', f"Usando L'Hôpital, ¿cuánto vale lim(x→0) (e^({a}x) − 1)/x?", a, numwrong(a, pos=True, extra=[1, 0]), f"Derivando: a·e^(ax)/1 → {a}.", 66 + a / 2)
    if k == 1:
        if sp: assert sp.limit((1 - sp.cos(a * X)) / X ** 2, X, 0) == sp.Rational(a * a, 2)
        s = F(a * a, 2)
        return add('calc', f"¿Cuánto vale lim(x→0) (1 − cos({a}x))/x²?", nf(s), [nf(F(a, 2)), nf(F(a * a)), '0', nf(F(1, 2))], f"Dos veces L'Hôpital: a²/2 = {nf(s)}.", 78 + a, acc=[best(s)])
    if k == 2:
        if sp: assert sp.limit((sp.sin(a * X) - a * X) / X ** 3, X, 0) == sp.Rational(-a ** 3, 6)
        s = F(-a ** 3, 6)
        return add('calc', f"¿Cuánto vale lim(x→0) (sin({a}x) − {a}x)/x³?", nf(s), [nf(-s), nf(F(a ** 3, 3)), '0', nf(F(-a, 6))], "Se aplica L'Hôpital tres veces (o la serie de Taylor).", 90 + a / 3, acc=[best(s)])
    if k == 3:
        if sp: assert sp.limit(sp.log(1 + a * X) / X, X, 0) == a
        return add('calc', f"Usando L'Hôpital, ¿cuánto vale lim(x→0) ln(1 + {a}x)/x?", a, numwrong(a, pos=True, extra=[1, 0]), f"Derivando: a/(1 + ax) → {a}.", 66 + a / 2)
    n = R.randint(2, 5)
    return add('calc', f"¿Cuánto vale lim(x→∞) x{sup(n)}/e^x?" if n <= 3 else f"¿Cuánto vale lim(x→∞) x^{n}/e^x?", '0', ['1', '∞', f'{n}', '-∞'], "La exponencial crece más rápido que cualquier potencia.", 74 + n)


def c_series():
    k = R.randint(0, 3); n = R.randint(2, 7)
    if k == 0:
        s = F(1, math.factorial(n))
        return add('calc', f"¿Cuál es el coeficiente de x^{n} en la serie de Maclaurin de e^x?" if n > 3 else f"¿Cuál es el coeficiente de x{sup(n)} en la serie de Maclaurin de e^x?", nf(s), [nf(F(1, n)), nf(F(1, math.factorial(n + 1))), nf(F(n)), nf(F(1, math.factorial(n - 1)))], "eˣ = Σ xⁿ/n!, así que el coeficiente es 1/n!.", 72 + n * 2)
    if k == 1:
        m = R.randint(1, 3); e_ = 2 * m + 1
        s = F((-1) ** m, math.factorial(e_))
        return add('calc', f"¿Cuál es el coeficiente de x^{e_} en la serie de Maclaurin de sin x?" if e_ > 3 else f"¿Cuál es el coeficiente de x{sup(e_)} en la serie de Maclaurin de sin x?", nf(s), [nf(-s), nf(F(1, e_)), nf(F((-1) ** m, math.factorial(e_ - 1))), nf(F((-1) ** m, math.factorial(e_ + 1)))], "sin x = x − x³/3! + x⁵/5! − …", 76 + e_ * 2)
    if k == 2:
        m = R.randint(1, 3); e_ = 2 * m
        s = F((-1) ** m, math.factorial(e_))
        return add('calc', f"¿Cuál es el coeficiente de x^{e_} en la serie de Maclaurin de cos x?" if e_ > 3 else f"¿Cuál es el coeficiente de x{sup(e_)} en la serie de Maclaurin de cos x?", nf(s), [nf(-s), nf(F(1, e_)), nf(F((-1) ** m, math.factorial(e_ + 1))), nf(F((-1) ** (m + 1), math.factorial(e_ - 1)))], "cos x = 1 − x²/2! + x⁴/4! − …", 76 + e_ * 2)
    s = F((-1) ** (n + 1), n)
    return add('calc', f"¿Cuál es el coeficiente de x^{n} en la serie de Maclaurin de ln(1 + x)?" if n > 3 else f"¿Cuál es el coeficiente de x{sup(n)} en la serie de Maclaurin de ln(1 + x)?", nf(s), [nf(-s), nf(F(1, math.factorial(n))), nf(F((-1) ** (n + 1), math.factorial(n))), nf(F(1, n + 1))], "ln(1 + x) = x − x²/2 + x³/3 − …", 78 + n * 2)


CONC_CALC = [
    ("¿Qué mide la derivada de una función en un punto?", "La pendiente de la recta tangente en ese punto", ["El área bajo la curva", "El valor de la función", "El máximo de la función"], "Es la razón de cambio instantánea.", 16),
    ("¿Cuál es la derivada de una constante?", "0", ["1", "La constante misma", "x"], "Una constante no cambia.", 8),
    ("¿Cuál es la derivada de x?", "1", ["0", "x", "2x"], "(x)′ = 1.", 6),
    ("¿Qué es la regla de la cadena?", "Una regla para derivar funciones compuestas", ["Una regla para derivar sumas", "Una regla para integrar potencias", "Una regla para hallar límites"], "(f∘g)′ = f′(g)·g′.", 50),
    ("¿Qué establece la regla del producto?", "(uv)′ = u′v + uv′", ["(uv)′ = u′v′", "(uv)′ = u′ + v′", "(uv)′ = uv′ − u′v"], "No se deriva factor por factor.", 52),
    ("¿Qué establece la regla del cociente?", "(u/v)′ = (u′v − uv′)/v²", ["(u/v)′ = u′/v′", "(u/v)′ = (u′v + uv′)/v²", "(u/v)′ = (uv′ − u′v)/v²"], "El orden del numerador importa.", 62),
    ("Si f′(x) > 0 en un intervalo, ¿cómo es f ahí?", "Creciente", ["Decreciente", "Constante", "Cóncava hacia abajo"], "Derivada positiva implica crecimiento.", 28),
    ("Si f′(x) < 0 en un intervalo, ¿cómo es f ahí?", "Decreciente", ["Creciente", "Constante", "Cóncava hacia arriba"], "Derivada negativa implica decrecimiento.", 28),
    ("¿Qué indica f″(x) > 0?", "La gráfica es cóncava hacia arriba", ["La gráfica es cóncava hacia abajo", "La función es decreciente", "Hay un máximo"], "La segunda derivada mide la concavidad.", 54),
    ("¿Qué es un punto crítico?", "Un punto donde f′(x) = 0 o no existe", ["Un punto donde f(x) = 0", "Un punto donde f″(x) = 0", "El punto de mayor valor de x"], "Allí pueden ocurrir máximos o mínimos.", 44),
    ("¿Qué es un punto de inflexión?", "Un punto donde cambia la concavidad", ["Un punto donde f(x) = 0", "Un máximo local", "Un punto de discontinuidad"], "f″ cambia de signo.", 62),
    ("¿Qué es una función continua en x = a?", "Una función cuyo límite en a coincide con f(a)", ["Una función sin derivada", "Una función que no tiene raíces", "Una función creciente"], "lim f(x) = f(a).", 34),
    ("¿Es toda función derivable en un punto también continua ahí?", "Sí", ["No, nunca", "Solo si es polinómica", "Solo si es creciente"], "La derivabilidad implica continuidad.", 52),
    ("¿Es toda función continua también derivable?", "No, por ejemplo |x| en x = 0", ["Sí, siempre", "Sí, si es creciente", "Solo las trigonométricas"], "|x| tiene un pico en 0.", 56),
    ("¿Qué es una integral definida?", "El área neta bajo la curva entre dos límites", ["La derivada de una función", "Una función sin constante", "El valor máximo de la función"], "∫ de a a b f(x) dx.", 40),
    ("¿Qué significa la constante C en una integral indefinida?", "Que hay infinitas antiderivadas que difieren en una constante", ["Que la integral es cero", "Que la función es constante", "Que el límite no existe"], "La derivada de una constante es 0.", 36),
    ("¿Qué dice el Teorema Fundamental del Cálculo?", "Derivación e integración son operaciones inversas", ["Toda función tiene derivada", "La integral siempre es positiva", "Los límites siempre existen"], "∫f′ = f(b) − f(a).", 60),
    ("¿Qué es una antiderivada de f?", "Una función F tal que F′ = f", ["Una función tal que F = f′", "La inversa de f", "El límite de f"], "También se llama primitiva.", 34),
    ("¿Cuánto vale lim(x→0) sin x / x?", "1", ["0", "∞", "No existe"], "Es un límite notable.", 42),
    ("¿Cuánto vale lim(x→∞) 1/x?", "0", ["1", "∞", "No existe"], "El denominador crece sin límite.", 22),
    ("¿Qué indica la regla de L'Hôpital?", "Que para formas 0/0 o ∞/∞ se pueden derivar numerador y denominador", ["Que todo límite vale cero", "Que se debe integrar el numerador", "Que el denominador debe ser constante"], "lim f/g = lim f′/g′ si el segundo existe.", 64),
    ("¿Cuál es la derivada de eˣ?", "eˣ", ["x·eˣ⁻¹", "eˣ⁻¹", "ln x"], "Es su propia derivada.", 24),
    ("¿Cuál es la derivada de ln x?", "1/x", ["x", "ln x/x", "eˣ"], "(ln x)′ = 1/x.", 24),
    ("¿Qué teorema garantiza un valor intermedio para una función continua en [a, b]?", "El teorema del valor intermedio", ["El teorema de Pitágoras", "El teorema del binomio", "El teorema del residuo"], "Una función continua toma todos los valores entre f(a) y f(b).", 70),
    ("¿Qué asegura el teorema de Rolle?", "Si f(a) = f(b), hay un c con f′(c) = 0", ["Que f es siempre creciente", "Que f tiene una integral", "Que f no tiene máximos"], "Requiere continuidad y derivabilidad.", 72),
    ("¿Qué asegura el teorema del valor medio?", "Existe c con f′(c) = (f(b) − f(a))/(b − a)", ["f′ es siempre cero", "f es una recta", "f tiene dos raíces"], "La pendiente media se alcanza en algún punto.", 76),
    ("¿Qué es una asíntota vertical?", "Una recta x = a cerca de la cual la función crece sin límite", ["El valor máximo de f", "Un punto de inflexión", "La raíz de f"], "Ocurre, por ejemplo, en 1/x cuando x → 0.", 46),
    ("¿Qué es una asíntota horizontal?", "Una recta y = L a la que se acerca f cuando x → ±∞", ["Una recta paralela al eje y", "El punto más alto de f", "Una raíz doble"], "lim f(x) = L.", 44),
    ("¿Cuál es la integral de 1/x?", "ln|x| + C", ["1/x² + C", "x ln x + C", "−1/x² + C"], "Es la única potencia que no sigue la regla general.", 38),
    ("¿Qué mide la integral de una velocidad respecto al tiempo?", "El desplazamiento", ["La aceleración", "La fuerza", "La masa"], "∫v dt = s.", 48),
    ("¿Qué mide la derivada de la posición respecto al tiempo?", "La velocidad", ["La aceleración", "La distancia total", "La masa"], "v = s′.", 30),
    ("¿Qué mide la derivada de la velocidad respecto al tiempo?", "La aceleración", ["La posición", "La fuerza", "El desplazamiento"], "a = v′ = s″.", 32),
    ("¿Qué condición debe cumplirse en un máximo local de una función derivable?", "f′(x) = 0", ["f(x) = 0", "f″(x) > 0", "f′(x) > 0"], "La tangente es horizontal.", 40),
    ("¿Qué es una suma de Riemann?", "Una aproximación del área mediante rectángulos", ["Una derivada numérica", "Un tipo de límite infinito", "Una función exponencial"], "Su límite define la integral definida.", 58),
    ("¿Qué indica un límite que vale ∞?", "Que la función crece sin cota", ["Que el límite existe como número", "Que la función es continua", "Que es una integral"], "Es una divergencia infinita.", 50),
]


def c_conc():
    for q, c, w, e, d_ in CONC_CALC:
        add('calc', q, c, w, e, d_)


def build_calc():
    plan = [(c_lim_sub, 24), (c_lim_fac, 34), (c_lim_inf, 34), (c_lim_tr, 24), (c_lim_sqrt, 16), (c_cont, 10),
            (c_der_pow, 42), (c_der_poly, 56), (c_der_val, 34), (c_der_trig, 36), (c_der_trig2, 12), (c_der_special, 16), (c_der_prod, 44), (c_der_quot, 36),
            (c_der_chain, 90), (c_implicit, 12), (c_tangent, 36), (c_crit, 38), (c_rates, 34), (c_opt, 28),
            (c_int_basic, 56), (c_int_def, 44), (c_int_ea, 40), (c_int_sub, 34), (c_int_parts, 40), (c_area, 28), (c_ftc, 20), (c_lhop, 22), (c_series, 22)]
    for fn, n in plan: rep(n, fn)
    c_conc()
