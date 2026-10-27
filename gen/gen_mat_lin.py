# -*- coding: utf-8 -*-
# Categoría ÁLGEBRA LINEAL (se ejecuta dentro del espacio de nombres de gen_mat.py)


def det2(M): return M[0][0] * M[1][1] - M[0][1] * M[1][0]


def det3(M):
    return (M[0][0] * (M[1][1] * M[2][2] - M[1][2] * M[2][1]) - M[0][1] * (M[1][0] * M[2][2] - M[1][2] * M[2][0])
            + M[0][2] * (M[1][0] * M[2][1] - M[1][1] * M[2][0]))


def mm(A, B):
    return [[sum(A[i][k] * B[k][j] for k in range(len(B))) for j in range(len(B[0]))] for i in range(len(A))]


def ms(M): return '[[' + '],['.join(','.join(nf(x) for x in row) for row in M) + ']]'


def msp(M): return '[[' + '], ['.join(', '.join(nf(x) for x in row) for row in M) + ']]'


def msm(M): return '; '.join(' '.join(nf(x) for x in row) for row in M)


def mq(M): return ms(M).replace('-', '−')


def vs(v): return '(' + ', '.join(nf(x) for x in v) + ')'


def vq(v): return vs(v).replace('-', '−')


def macc(M): return [msp(M), msm(M)]


def vacc(v): return [','.join(nf(x) for x in v), '(' + ','.join(nf(x) for x in v) + ')']


def mwrong(M):
    out = []
    n, m = len(M), len(M[0])
    Tm = [list(r) for r in zip(*M)]
    if Tm != [list(r) for r in M]: out.append(ms(Tm))
    cells = [(i, j) for i in range(n) for j in range(m)]
    R.shuffle(cells)
    for (i, j) in cells[:5]:
        M2 = [list(r) for r in M]; M2[i][j] = M2[i][j] + R.choice([1, -1]); out.append(ms(M2))
        M3 = [list(r) for r in M]; M3[i][j] = -M3[i][j]; out.append(ms(M3))
    return out


def vwrong(v):
    out = []
    n = len(v)
    for i in R.sample(range(n), n):
        v2 = list(v); v2[i] = v2[i] + R.choice([1, -1, 2]); out.append(vs(v2))
        v3 = list(v); v3[i] = -v3[i]; out.append(vs(v3))
    out.append(vs(v[::-1]))
    return out


def rmat(n, m, lo=-4, hi=6):
    return [[R.randint(lo, hi) for _ in range(m)] for _ in range(n)]


def rank_of(M):
    A = [[F(x) for x in r] for r in M]
    rk = 0
    rows, cols = len(A), len(A[0])
    for c in range(cols):
        piv = None
        for r in range(rk, rows):
            if A[r][c] != 0: piv = r; break
        if piv is None: continue
        A[rk], A[piv] = A[piv], A[rk]
        for r in range(rows):
            if r != rk and A[r][c] != 0:
                f = A[r][c] / A[rk][c]
                A[r] = [x - f * y for x, y in zip(A[r], A[rk])]
        rk += 1
    return rk


def l_vsum():
    n = R.choice([2, 2, 3]); u = [R.randint(-6, 9) for _ in range(n)]; v = [R.randint(-6, 9) for _ in range(n)]
    if R.random() < .6:
        s = [a + b for a, b in zip(u, v)]; op = '+'; w = [[a - b for a, b in zip(u, v)]]
    else:
        s = [a - b for a, b in zip(u, v)]; op = '−'; w = [[a + b for a, b in zip(u, v)]]
    ws = [vs(x) for x in w] + vwrong(s)
    return add('lin', f"Si u = {vq(u)} y v = {vq(v)}, ¿cuánto es u {op} v?", vs(s), ws, "Se opera componente a componente.", 4 + n * 2 + max(map(abs, u + v)) / 3, acc=vacc(s))


def l_vscal():
    n = R.choice([2, 3]); v = [R.randint(-6, 8) for _ in range(n)]; k = R.choice([2, 3, 4, 5, -1, -2, -3])
    s = [k * a for a in v]
    return add('lin', f"Si v = {vq(v)}, ¿cuánto es {k if k>0 else '('+str(k)+')'}v?".replace('(-', '(−'), vs(s), vwrong(s) + [vs([k + a for a in v])], "Se multiplica cada componente por el escalar.", 5 + n * 2 + abs(k), acc=vacc(s))


def l_vdot():
    n = R.choice([2, 3]); u = [R.randint(-5, 7) for _ in range(n)]; v = [R.randint(-5, 7) for _ in range(n)]
    s = sum(a * b for a, b in zip(u, v))
    ex_ = [sum(a + b for a, b in zip(u, v))]
    if n == 2: ex_.append(u[0] * v[1] + u[1] * v[0])
    return add('lin', f"¿Cuál es el producto punto de u = {vq(u)} y v = {vq(v)}?", s, numwrong(s, extra=ex_), "u·v = u₁v₁ + u₂v₂" + (" + u₃v₃." if n == 3 else "."), 10 + n * 4 + abs(s) / 20)


def l_vnorm():
    k = R.randint(0, 2)
    if k == 0:
        a, b, c = R.choice([(3, 4, 5), (5, 12, 13), (8, 15, 17), (7, 24, 25), (6, 8, 10), (9, 12, 15), (20, 21, 29), (12, 16, 20), (9, 40, 41), (12, 5, 13), (15, 8, 17)])
        a, b = a * R.choice([1, -1]), b * R.choice([1, -1])
        return add('lin', f"¿Cuál es la norma (longitud) del vector {vq([a, b])}?", c, numwrong(c, pos=True, extra=[abs(a) + abs(b), c * c]), f"‖v‖ = √({a*a} + {b*b}) = {c}.", 14 + c / 3)
    if k == 1:
        a, b, c, r = R.choice([(1, 2, 2, 3), (2, 3, 6, 7), (1, 4, 8, 9), (2, 6, 9, 11), (4, 4, 7, 9), (2, 10, 11, 15), (6, 6, 7, 11), (2, 2, 1, 3), (3, 6, 2, 7), (8, 1, 4, 9)])
        sg = [R.choice([1, -1]) for _ in range(3)]
        return add('lin', f"¿Cuál es la norma del vector {vq([a*sg[0], b*sg[1], c*sg[2]])}?", r, numwrong(r, pos=True, extra=[a + b + c, r * r]), f"‖v‖ = √({a*a} + {b*b} + {c*c}) = {r}.", 22 + r / 2)
    a, b = R.randint(1, 8), R.randint(1, 8)
    if int(math.isqrt(a * a + b * b)) ** 2 == a * a + b * b: return False
    return add('lin', f"¿Cuál es la norma del vector {vq([a, b])}?", f"√{a*a+b*b}", [f"{a+b}", f"√{a+b}", f"{a*a+b*b}", f"√{abs(a*a-b*b)}" if a != b else "√2"], f"‖v‖ = √({a}² + {b}²) = √{a*a+b*b}.", 20 + (a + b) / 2, acc=[f"sqrt({a*a+b*b})", f"raiz({a*a+b*b})"])


def l_vorth():
    a, b, c = R.randint(1, 6), R.randint(-6, 6), R.randint(-6, 6)
    if b * c == 0 or (b * c) % a: return False
    k = -b * c // a
    return add('lin', f"¿Qué valor de k hace ortogonales a u = {vq([a, b])} y v = {vq(['k', c]) if False else '(k, ' + str(c).replace('-', '−') + ')'}?", k, numwrong(k, extra=[-k, b * c]), f"u·v = {a}k + ({b})({c}) = 0 ⇒ k = {k}.", 36 + abs(k) / 2 + a)


def l_vproj():
    a, b, c = R.choice([(3, 4, 5), (5, 12, 13), (6, 8, 10), (8, 15, 17)])
    u = [R.randint(-6, 8), R.randint(-6, 8)]
    s = F(u[0] * a + u[1] * b, c)
    return add('lin', f"¿Cuál es la proyección escalar de u = {vq(u)} sobre v = {vq([a, b])}?", nf(s), [nf(F(u[0] * a + u[1] * b)), nf(F(u[0] * a + u[1] * b, c * c)), nf(s + 1), nf(-s) if s != 0 else '1'], f"comp = u·v/‖v‖ = {u[0]*a+u[1]*b}/{c}.", 58 + c / 3, acc=[best(s)])


def l_vcross():
    u = [R.randint(-4, 5) for _ in range(3)]; v = [R.randint(-4, 5) for _ in range(3)]
    w = [u[1] * v[2] - u[2] * v[1], u[2] * v[0] - u[0] * v[2], u[0] * v[1] - u[1] * v[0]]
    if not any(w): return False
    ws = vwrong(w) + [vs([-t for t in w])]
    return add('lin', f"¿Cuál es el producto cruz u × v si u = {vq(u)} y v = {vq(v)}?", vs(w), ws, "u × v = (u₂v₃ − u₃v₂, u₃v₁ − u₁v₃, u₁v₂ − u₂v₁).", 56 + (max(map(abs, w))) / 4, acc=vacc(w))


def l_varea():
    u = [R.randint(-5, 6), R.randint(-5, 6)]; v = [R.randint(-5, 6), R.randint(-5, 6)]
    dd = u[0] * v[1] - u[1] * v[0]
    if dd == 0: return False
    if R.random() < .5:
        return add('lin', f"¿Cuál es el área del paralelogramo formado por los vectores {vq(u)} y {vq(v)}?", abs(dd), numwrong(abs(dd), pos=True, extra=[u[0] * v[0] + u[1] * v[1] if u[0] * v[0] + u[1] * v[1] > 0 else abs(dd) + 3]), f"Área = |u₁v₂ − u₂v₁| = {abs(dd)}.", 52 + abs(dd) / 5)
    s = F(abs(dd), 2)
    return add('lin', f"¿Cuál es el área del triángulo con lados u = {vq(u)} y v = {vq(v)}?", nf(s), [nf(abs(dd)), nf(2 * abs(dd)), nf(s + 1), nf(F(abs(dd), 3))], "Área del triángulo = |u₁v₂ − u₂v₁|/2.", 56 + abs(dd) / 5, acc=[best(s)])


def l_vangle():
    a, b = R.randint(1, 5), R.randint(1, 5)
    cases = [([a, 0], [0, b], '90°'), ([a, 0], [b, 0], '0°'), ([a, 0], [-b, 0], '180°'), ([a, 0], [b, b], '45°'), ([a, 0], [-b, b], '135°'), ([0, a], [b, b], '45°'), ([a, a], [-b, b], '90°')]
    u, v, ans = R.choice(cases)
    return add('lin', f"¿Qué ángulo forman los vectores {vq(u)} y {vq(v)}?", ans, [x for x in ['0°', '45°', '90°', '135°', '180°', '60°'] if x != ans], "Se usa cos θ = u·v/(‖u‖‖v‖).", 34 + (6 if ans in ('45°', '135°') else 0), acc=[ans.replace('°', ''), ans.replace('°', ' grados')])


def l_madd():
    n, m = R.choice([(2, 2), (2, 2), (2, 3)]); A = rmat(n, m, -5, 8); B = rmat(n, m, -5, 8)
    if R.random() < .6: S = [[a + b for a, b in zip(r, q)] for r, q in zip(A, B)]; op = '+'; W = [[a - b for a, b in zip(r, q)] for r, q in zip(A, B)]
    else: S = [[a - b for a, b in zip(r, q)] for r, q in zip(A, B)]; op = '−'; W = [[a + b for a, b in zip(r, q)] for r, q in zip(A, B)]
    return add('lin', f"Si A = {mq(A)} y B = {mq(B)}, ¿cuánto es A {op} B?", ms(S), [ms(W)] + mwrong(S), "Se opera entrada por entrada.", 6 + n * m + max(abs(x) for r in A for x in r) / 3, acc=macc(S))


def l_mscal():
    A = rmat(2, 2, -5, 7); k = R.choice([2, 3, 4, -1, -2, 5])
    S = [[k * x for x in r] for r in A]
    return add('lin', f"Si A = {mq(A)}, ¿cuánto es {k if k>0 else '('+str(k)+')'}A?".replace('(-', '(−'), ms(S), mwrong(S) + [ms([[k + x for x in r] for r in A])], "Se multiplica cada entrada por el escalar.", 8 + abs(k) * 2, acc=macc(S))


def l_mmul():
    k = R.randint(0, 3)
    if k == 0:
        A = rmat(2, 2, -3, 4); B = rmat(2, 2, -3, 4)
        P = mm(A, B)
        w = [ms([[A[i][j] * B[i][j] for j in range(2)] for i in range(2)]), ms(mm(B, A))] + mwrong(P)
        return add('lin', f"Si A = {mq(A)} y B = {mq(B)}, ¿cuánto es AB?", ms(P), w, "Fila de A por columna de B.", 40 + max(abs(x) for r in P for x in r) / 3, acc=macc(P))
    if k == 1:
        A = rmat(2, 2, -3, 4); B = rmat(2, 2, -3, 4); i, j = R.randint(0, 1), R.randint(0, 1)
        P = mm(A, B)
        return add('lin', f"Si A = {mq(A)} y B = {mq(B)}, ¿cuál es el elemento de la fila {i+1}, columna {j+1} de AB?", P[i][j], numwrong(P[i][j], extra=[A[i][j] * B[i][j], mm(B, A)[i][j]]), f"Se multiplica la fila {i+1} de A por la columna {j+1} de B y se suma.", 34 + abs(P[i][j]) / 4)
    if k == 2:
        A = rmat(2, 3, -3, 4); B = rmat(3, 2, -3, 4); i, j = R.randint(0, 1), R.randint(0, 1)
        P = mm(A, B)
        return add('lin', f"Si A = {mq(A)} (2×3) y B = {mq(B)} (3×2), ¿cuál es el elemento de la fila {i+1}, columna {j+1} de AB?", P[i][j], numwrong(P[i][j], extra=[sum(A[i]) * 1 if False else A[i][0] * B[0][j]]), "Producto punto de la fila de A con la columna de B.", 46 + abs(P[i][j]) / 4)
    A = rmat(2, 2, -3, 5); v = [R.randint(-3, 5), R.randint(-3, 5)]
    r = [A[0][0] * v[0] + A[0][1] * v[1], A[1][0] * v[0] + A[1][1] * v[1]]
    return add('lin', f"Si A = {mq(A)} y v = {vq(v)}, ¿cuánto es Av?", vs(r), vwrong(r) + [vs([A[0][0] * v[0] + A[1][0] * v[1], A[0][1] * v[0] + A[1][1] * v[1]])], "Cada componente es la fila de A por v.", 34 + max(map(abs, r)) / 4, acc=vacc(r))


def l_mtrans():
    n, m = R.choice([(2, 2), (2, 3), (3, 2)]); A = rmat(n, m, -5, 9)
    Tm = [list(r) for r in zip(*A)]
    return add('lin', f"¿Cuál es la transpuesta de A = {mq(A)}?", ms(Tm), [ms(A)] + mwrong(Tm), "Las filas de A pasan a ser columnas.", 12 + n + m, acc=macc(Tm))


def l_mtrace():
    A = rmat(3, 3, -4, 9); t = A[0][0] + A[1][1] + A[2][2]
    return add('lin', f"¿Cuál es la traza de la matriz {mq(A)}?", t, numwrong(t, extra=[sum(sum(r) for r in A), A[0][2] + A[1][1] + A[2][0]]), "La traza es la suma de la diagonal principal.", 10 + abs(t) / 4)


def l_mdet2():
    A = rmat(2, 2, -6, 8); d = det2(A)
    return add('lin', f"¿Cuál es el determinante de {mq(A)}?", d, numwrong(d, extra=[A[0][0] * A[1][1] + A[0][1] * A[1][0], A[0][0] * A[1][1] - A[0][1] * A[1][0] + 2]), "det = ad − bc.", 22 + abs(d) / 8)


def l_mdet3():
    A = rmat(3, 3, -3, 5); d = det3(A)
    if sp: assert sp.Matrix(A).det() == d
    return add('lin', f"¿Cuál es el determinante de {mq(A)}?", d, numwrong(d, extra=[A[0][0] * A[1][1] * A[2][2] + A[0][1] * A[1][2] * A[2][0] + A[0][2] * A[1][0] * A[2][1]]), "Se usa la regla de Sarrus o la expansión por cofactores.", 66 + min(18, abs(d) / 6))


def l_minv():
    k = R.randint(0, 3)
    if k == 0:
        a, b = R.randint(-4, 4), R.randint(-4, 4)
        if a == 0 and b == 0: return False
        A = [[1 + a * b, a], [b, 1]]
        Iv = [[1, -a], [-b, 1 + a * b]]
        assert mm(A, Iv) == [[1, 0], [0, 1]]
        return add('lin', f"¿Cuál es la inversa de A = {mq(A)}?", ms(Iv), mwrong(Iv) + [ms([[-x for x in r] for r in A])], f"det A = 1, así que A⁻¹ = [[d, −b], [−c, a]].", 56 + (abs(a) + abs(b)) / 2, acc=macc(Iv))
    if k == 1:
        A = rmat(2, 2, -4, 6); d = det2(A)
        if d == 0: return False
        i, j = R.randint(0, 1), R.randint(0, 1)
        Iv = [[F(A[1][1], d), F(-A[0][1], d)], [F(-A[1][0], d), F(A[0][0], d)]]
        s = Iv[i][j]
        return add('lin', f"Si A = {mq(A)}, ¿cuál es el elemento de la fila {i+1}, columna {j+1} de A⁻¹?", nf(s), [nf(-s) if s != 0 else '1', nf(F(A[1 - i][1 - j]) if False else F(A[i][j], d)), nf(s * d) if d != 1 else nf(s + 1), nf(Iv[1 - i][1 - j]) if Iv[1 - i][1 - j] != s else nf(s + 2)],
                   f"A⁻¹ = (1/{d})·[[d, −b], [−c, a]].", 60 + abs(d) / 3, acc=[best(s)])
    if k == 2:
        d = R.choice([2, 3, 4, 5, 6, 8, 10, -2, -4, -5])
        n = R.choice([2, 3])
        return add('lin', f"Una matriz invertible {n}×{n} tiene det A = {d}. ¿Cuánto vale det(A⁻¹)?", nf(F(1, d)), [nf(F(d)), nf(F(-1, d)), nf(F(1, d ** 2)) if abs(d) != 1 else '2', nf(F(1, d) + 1)], "det(A⁻¹) = 1/det A.", 55 + abs(d) / 2, acc=[best(F(1, d))])
    a, b, c = R.randint(1, 4), R.randint(-5, 5), R.randint(-5, 5)
    if b * c == 0 or (b * c) % a: return False
    kk = b * c // a
    return add('lin', f"¿Qué valor de k hace que A = {mq([[a, b], [c, 'k']]) if False else '[[' + str(a) + ',' + str(b).replace('-', '−') + '],[' + str(c).replace('-', '−') + ',k]]'} no sea invertible?", kk, numwrong(kk, extra=[-kk, b + c]), f"det A = {a}k − ({b})({c}) = 0 ⇒ k = {kk}.", 58 + abs(kk) / 2)


def l_meig():
    k = R.randint(0, 4)
    if k == 0:
        a, d_, b = R.randint(-5, 6), R.randint(-5, 6), R.randint(-4, 5)
        if a == d_: return False
        A = [[a, b], [0, d_]]; ans = two_roots(a, d_)
        return add('lin', f"¿Cuáles son los autovalores de {mq(A)}?", ans[0], [f"{nf(-a)} y {nf(-d_)}", f"{nf(a + d_)} y {nf(a * d_)}", f"{nf(a)} y {nf(b)}", f"{nf(a + b)} y {nf(d_)}"], "En una matriz triangular los autovalores son los elementos de la diagonal.", 50 + (abs(a) + abs(d_)) / 3, acc=ans[1:])
    if k == 1:
        a, b = R.randint(-4, 6), R.randint(1, 5)
        A = [[a, b], [b, a]]; ans = two_roots(a + b, a - b)
        return add('lin', f"¿Cuáles son los autovalores de {mq(A)}?", ans[0], [f"{nf(a)} y {nf(b)}", f"{nf(a + b)} y {nf(b - a)}", f"{nf(2 * a)} y {nf(2 * b)}", f"{nf(a * a - b * b)} y {nf(a)}"], "Se resuelve det(A − λI) = 0: λ = a ± b.", 62 + b / 2, acc=ans[1:])
    if k == 2:
        l1, l2 = R.randint(-4, 6), R.randint(-4, 6)
        if l1 == l2: return False
        A = [[0, 1], [-l1 * l2, l1 + l2]]; ans = two_roots(l1, l2)
        return add('lin', f"¿Cuáles son los autovalores de {mq(A)}?", ans[0], [f"{nf(-l1)} y {nf(-l2)}", f"{nf(l1 + l2)} y {nf(l1 * l2)}", f"{nf(l1)} y {nf(-l2)}", f"{nf(l1 + 1)} y {nf(l2)}"], f"λ² − ({l1+l2})λ + ({l1*l2}) = 0.", 74 + (abs(l1) + abs(l2)) / 2, acc=ans[1:])
    if k == 3:
        l1, l2 = R.randint(-4, 7), R.randint(-4, 7)
        if l1 == l2: return False
        t, D = l1 + l2, l1 * l2; ans = two_roots(l1, l2)
        return add('lin', f"Una matriz 2×2 tiene traza {t} y determinante {D}. ¿Cuáles son sus autovalores?", ans[0], [f"{nf(-l1)} y {nf(-l2)}", f"{nf(t)} y {nf(D)}", f"{nf(l1 + 1)} y {nf(l2 - 1)}", f"{nf(l1)} y {nf(-l2)}"], "λ₁ + λ₂ = traza y λ₁λ₂ = determinante.", 70 + (abs(l1) + abs(l2)) / 2, acc=ans[1:])
    ls = sorted(R.sample(range(-3, 8), 3))
    A = [[ls[0], R.randint(-3, 4), R.randint(-3, 4)], [0, ls[1], R.randint(-3, 4)], [0, 0, ls[2]]]
    s = f"{ls[0]}, {ls[1]} y {ls[2]}"
    return add('lin', f"¿Cuáles son los autovalores de la matriz triangular {mq(A)}?", s, [f"{-ls[0]}, {-ls[1]} y {-ls[2]}", f"{ls[0]}, {ls[1]} y {ls[1] + ls[2]}", f"{sum(ls)}, {ls[0]*ls[1]*ls[2]} y 0", f"{ls[0]}, {ls[1]} y {A[0][1]}"], "En una matriz triangular se leen en la diagonal.", 62 + sum(map(abs, ls)) / 4, acc=[f"{ls[0]},{ls[1]},{ls[2]}", f"{ls[0]} {ls[1]} {ls[2]}"])


def l_meigv():
    k = R.randint(0, 2); a, b = R.randint(-4, 6), R.randint(1, 5)
    if k == 0:
        A = [[a, b], [b, a]]
        return add('lin', f"¿Cuál es un autovector de A = {mq(A)} para el autovalor λ = {a+b}?", "(1, 1)", ["(1, -1)", "(1, 0)", "(0, 1)", "(2, 1)"], f"(A − {a+b}I)v = 0 ⇒ v₁ = v₂.", 78 + b / 2, acc=['(1,1)', '1,1'])
    if k == 1:
        A = [[a, b], [b, a]]
        return add('lin', f"¿Cuál es un autovector de A = {mq(A)} para el autovalor λ = {a-b}?", "(1, -1)", ["(1, 1)", "(1, 0)", "(0, 1)", "(2, -1)"], f"(A − ({a-b})I)v = 0 ⇒ v₁ = −v₂.", 80 + b / 2, acc=['(1,-1)', '1,-1'])
    d_ = R.randint(-4, 6)
    if a == d_: return False
    A = [[a, 0], [0, d_]]
    return add('lin', f"¿Cuál es un autovector de A = {mq(A)} para el autovalor λ = {d_}?", "(0, 1)", ["(1, 0)", "(1, 1)", "(0, 0)", "(1, -1)"], "Para una matriz diagonal los autovectores son los vectores de la base.", 62 + abs(d_) / 2, acc=['(0,1)', '0,1'])


def l_rank():
    k = R.randint(0, 3)
    if k == 0:
        r1 = [R.randint(-3, 4) for _ in range(3)]
        if not any(r1): return False
        A = [r1, [2 * x for x in r1], [-x for x in r1]]; rk = 1
    elif k == 1:
        r1 = [R.randint(-3, 4) for _ in range(3)]; r2 = [R.randint(-3, 4) for _ in range(3)]
        A = [r1, r2, [a + b for a, b in zip(r1, r2)]]; rk = 2
    elif k == 2:
        A = rmat(3, 3, -3, 4); rk = None
    else:
        A = rmat(2, 3, -3, 4); rk = None
    calc = rank_of(A)
    if rk is not None and calc != rk: return False
    if sp: assert sp.Matrix(A).rank() == calc
    return add('lin', f"¿Cuál es el rango de la matriz {mq(A)}?", calc, [x for x in [0, 1, 2, 3, 4] if x != calc], "El rango es el número de filas linealmente independientes (pivotes).", 54 + calc * 6 + (6 if k == 1 else 0))


def l_sys():
    k = R.randint(0, 2)
    if k == 0:
        a, b = R.randint(1, 4), R.randint(1, 5); m = R.choice([2, 3, -1, -2]); c = R.randint(1, 9)
        kind = R.randint(0, 2)
        if kind == 0:
            d_ = R.randint(1, 5)
            if a * d_ == b * m * a: return False
            # a x + b y = c ; m a x + d y = e con d != m b
            dd = m * b + R.choice([1, 2, -1, -2, 3])
            e = R.randint(1, 9)
            ans = "Solución única"
            s1, s2 = f"{lexpr([(a,'x'),(b,'y')])} = {c}", f"{lexpr([(m*a,'x'),(dd,'y')])} = {e}"
        elif kind == 1:
            ans = "Infinitas soluciones"
            s1, s2 = f"{lexpr([(a,'x'),(b,'y')])} = {c}", f"{lexpr([(m*a,'x'),(m*b,'y')])} = {m*c}"
        else:
            ans = "Sin solución"
            s1, s2 = f"{lexpr([(a,'x'),(b,'y')])} = {c}", f"{lexpr([(m*a,'x'),(m*b,'y')])} = {m*c + R.choice([1, 2, 3, -1, -2])}"
        opts = ["Solución única", "Infinitas soluciones", "Sin solución", "Exactamente dos soluciones"]
        return add('lin', f"¿Cuántas soluciones tiene el sistema {s1.replace('= -', '= −')}; {s2.replace('= -', '= −')}?", ans, [o for o in opts if o != ans], "Se compara si las ecuaciones son proporcionales en coeficientes y en términos independientes.", 52 + (8 if kind else 0) + abs(m))
    if k == 1:
        while True:
            A = rmat(2, 2, -4, 5)
            if det2(A) != 0: break
        x = [R.randint(-5, 6), R.randint(-5, 6)]; b = [A[0][0] * x[0] + A[0][1] * x[1], A[1][0] * x[0] + A[1][1] * x[1]]
        j = R.randint(0, 1)
        sol = solve_lin(A, b); assert sol == x
        return add('lin', f"Resuelve Ax = b con A = {mq(A)} y b = {vq(b)}. ¿Cuánto vale {'x' if j==0 else 'y'}?", x[j], numwrong(x[j], extra=[x[1 - j]]), "Se resuelve por eliminación gaussiana o regla de Cramer.", 56 + abs(det2(A)) / 2)
    while True:
        A = rmat(3, 3, -3, 4)
        if det3(A) != 0: break
    x = [R.randint(-4, 5) for _ in range(3)]; b = [sum(A[i][j] * x[j] for j in range(3)) for i in range(3)]
    sol = solve_lin(A, b); assert sol == x
    j = R.randint(0, 2)
    return add('lin', f"Resuelve Ax = b con A = {mq(A)} y b = {vq(b)}. ¿Cuánto vale {'xyz'[j]}?", x[j], numwrong(x[j], extra=[x[(j + 1) % 3]]), "Eliminación gaussiana sobre la matriz aumentada.", 82 + min(10, abs(det3(A)) / 5))


def l_lt():
    k = R.randint(0, 6); x, y = R.randint(-6, 8), R.randint(-6, 8)
    if x == 0 or y == 0 or x == y: return False
    items = [
        (f"¿En qué punto se transforma ({x}, {y}) al reflejarlo respecto al eje x?", (x, -y), "La reflexión respecto al eje x cambia el signo de y.", 36),
        (f"¿En qué punto se transforma ({x}, {y}) al reflejarlo respecto al eje y?", (-x, y), "La reflexión respecto al eje y cambia el signo de x.", 36),
        (f"¿En qué punto se transforma ({x}, {y}) al girarlo 90° en sentido antihorario alrededor del origen?", (-y, x), "La rotación de 90° envía (x, y) a (−y, x).", 46),
        (f"¿En qué punto se transforma ({x}, {y}) al girarlo 180° alrededor del origen?", (-x, -y), "Una rotación de 180° cambia el signo de ambas coordenadas.", 38),
        (f"¿En qué punto se transforma ({x}, {y}) al reflejarlo respecto a la recta y = x?", (y, x), "La reflexión respecto a y = x intercambia las coordenadas.", 42),
        (f"¿En qué punto se transforma ({x}, {y}) al girarlo 90° en sentido horario alrededor del origen?", (y, -x), "La rotación horaria de 90° envía (x, y) a (y, −x).", 50),
    ]
    if k == 6:
        s = R.randint(2, 4)
        items.append((f"La transformación T(x, y) = ({s}x, {s}y) se aplica a ({x}, {y}). ¿Cuál es la imagen?", (s * x, s * y), f"Es un escalamiento por {s}.", 34))
    q, ans, e, d_ = items[k]
    w = vwrong(list(ans)) + [vs((x, y))]
    return add('lin', q.replace('-', '−') if False else q, vs(ans), w, e, d_ + abs(x) / 8, acc=vacc(ans))


def l_lt2():
    k = R.randint(0, 2)
    if k == 0:
        a = R.randint(1, 5); x, y = R.randint(-5, 6), R.randint(-5, 6)
        if y == 0: return False
        return add('lin', f"El corte (shear) T(x, y) = (x + {a}y, y) se aplica a ({x}, {y}). ¿Cuál es la imagen?", vs((x + a * y, y)), vwrong([x + a * y, y]) + [vs((x, y + a * x))], f"T = [[1, {a}], [0, 1]] aplicada al vector.", 50 + a)
    if k == 1:
        A = rmat(2, 2, -3, 5); d = det2(A)
        if d == 0: return False
        return add('lin', f"Una transformación lineal tiene matriz {mq(A)}. ¿Por qué factor multiplica las áreas (en valor absoluto)?", abs(d), numwrong(abs(d), pos=True, extra=[A[0][0] + A[1][1]]), "El factor de área es |det A|.", 58 + abs(d) / 3)
    a, b = R.randint(2, 5), R.randint(2, 5)
    return add('lin', f"La matriz diagonal diag({a}, {b}) transforma el cuadrado unitario en un rectángulo. ¿Cuál es su área?", a * b, numwrong(a * b, pos=True, extra=[a + b]), f"Área = |det| = {a}·{b}.", 44 + a + b)


def l_basis():
    k = R.randint(0, 2)
    if k == 0:
        a, b, c = R.randint(1, 4), R.randint(-5, 5), R.randint(1, 4)
        if b == 0: return False
        kk = F(c * b, a)
        if kk.denominator != 1: return False
        return add('lin', f"¿Qué valor de k hace linealmente dependientes a u = {vq([a, b])} y v = {vq([c, 'k']) if False else '(' + str(c) + ', k)'}?", nf(kk), numwrong(kk, extra=[-kk, b + c]), f"Dependientes ⇒ {a}k − {b}·{c} = 0 ⇒ k = {nf(kk)}.", 46 + a + c)
    if k == 1:
        m, n, r = R.randint(3, 6), R.randint(3, 7), R.randint(1, 3)
        if r > min(m, n): return False
        return add('lin', f"Una matriz {m}×{n} tiene rango {r}. ¿Cuál es la dimensión de su espacio nulo (nulidad)?", n - r, numwrong(n - r, pos=True, extra=[m - r, r]), "Teorema rango–nulidad: rango + nulidad = número de columnas.", 62 + n)
    n = R.randint(2, 7); r = R.randint(1, n - 1) if n > 1 else 1
    return add('lin', f"Un subespacio de ℝ^{n} está generado por {r+1} vectores, de los cuales solo {r} son linealmente independientes. ¿Cuál es su dimensión?", r, numwrong(r, pos=True, extra=[r + 1, n]), "La dimensión es el número de vectores independientes de una base.", 56 + n)


def l_detprop():
    k = R.randint(0, 3); n = R.choice([2, 3, 4]); d = R.choice([2, 3, 4, 5, -2, -3])
    if k == 0:
        c = R.choice([2, 3])
        return add('lin', f"Si A es {n}×{n} y det A = {d}, ¿cuánto vale det({c}A)?", c ** n * d, numwrong(c ** n * d, extra=[c * d]), f"det(cA) = cⁿ·det A = {c}^{n}·{d}.", 62 + n * 2 + c)
    if k == 1:
        e = R.choice([2, 3, 4, -2, -5])
        return add('lin', f"Si det A = {d} y det B = {e}, ¿cuánto vale det(AB)?", d * e, numwrong(d * e, extra=[d + e]), "det(AB) = det A · det B.", 52 + abs(d * e) / 3)
    if k == 2:
        return add('lin', f"Si det A = {d}, ¿cuánto vale det(Aᵀ)?", d, numwrong(d, extra=[1 / F(d) if False else 0]), "det(Aᵀ) = det A.", 44 + abs(d))
    p = R.choice([2, 3])
    return add('lin', f"Si det A = {d}, ¿cuánto vale det(A^{p})?" if p > 3 else f"Si det A = {d}, ¿cuánto vale det(A{sup(p)})?", d ** p, numwrong(d ** p, extra=[p * d]), f"det(Aᵖ) = (det A)ᵖ = {d**p}.", 54 + p * 2)


def l_comb():
    while True:
        u = [R.randint(-3, 4), R.randint(-3, 4)]; v = [R.randint(-3, 4), R.randint(-3, 4)]
        if u[0] * v[1] - u[1] * v[0] != 0: break
    al, be = R.randint(-4, 5), R.randint(-4, 5)
    w = [al * u[0] + be * v[0], al * u[1] + be * v[1]]
    sol = solve_lin([[u[0], v[0]], [u[1], v[1]]], w); assert sol == [al, be]
    return add('lin', f"Escribe w = {vq(w)} como α·u + β·v con u = {vq(u)} y v = {vq(v)}. ¿Cuál es (α, β)?", f"({al}, {be})", [f"({be}, {al})", f"({-al}, {be})" if al != 0 else "(1, 1)", f"({al}, {-be})" if be != 0 else "(2, 2)", f"({al+1}, {be-1})"], "Se resuelve el sistema α·u + β·v = w.", 62 + (abs(al) + abs(be)) / 2, acc=[f"{al},{be}"])


def l_plane():
    a, b, c = [R.randint(-4, 5) for _ in range(3)]
    if not (a or b or c): return False
    n = lexpr([(a, 'x'), (b, 'y'), (c, 'z')])
    if R.random() < .5:
        return add('lin', f"¿Cuál es la ecuación del plano que pasa por el origen y tiene vector normal {vq([a,b,c])}?", f"{lexpr([(a,'x'),(b,'y'),(c,'z')], '-')} = 0", [f"{lexpr([(a,'x'),(b,'y'),(c,'z')], '-')} = 1", f"{lexpr([(a,'x'),(b,'y'),(c,'z')], '-')} = {a+b+c}" if a + b + c not in (0, 1) else f"{lexpr([(a,'x'),(b,'y'),(c,'z')], '-')} = 2", f"{lexpr([(c,'x'),(b,'y'),(a,'z')], '-')} = 0" if (c, b, a) != (a, b, c) else f"{lexpr([(a,'x'),(b,'y'),(c,'z')], '-')} = 3", f"x + y + z = 0" if (a, b, c) != (1, 1, 1) else "x - y + z = 0"], "El plano es n·(x, y, z) = 0.", 60 + (abs(a) + abs(b) + abs(c)) / 3, acc=[f"{lexpr([(a,'x'),(b,'y'),(c,'z')], '-')}=0"])
    p = [R.randint(-3, 4) for _ in range(3)]
    dd = a * p[0] + b * p[1] + c * p[2]
    return add('lin', f"¿Cuál es la ecuación del plano con normal {vq([a,b,c])} que pasa por {vq(p)}?", f"{lexpr([(a,'x'),(b,'y'),(c,'z')], '-')} = {dd}", [f"{lexpr([(a,'x'),(b,'y'),(c,'z')], '-')} = {-dd}" if dd else f"{lexpr([(a,'x'),(b,'y'),(c,'z')], '-')} = 1", f"{lexpr([(a,'x'),(b,'y'),(c,'z')], '-')} = {dd+1}", f"{lexpr([(a,'x'),(b,'y'),(c,'z')], '-')} = {a+b+c}" if a + b + c != dd else f"{lexpr([(a,'x'),(b,'y'),(c,'z')], '-')} = {dd+2}", f"{lexpr([(p[0],'x'),(p[1],'y'),(p[2],'z')], '-')} = {dd}"], "n·(x − p) = 0 ⇒ ax + by + cz = n·p.", 66 + abs(dd) / 3)


def l_powers():
    k = R.randint(0, 2)
    if k == 0:
        a, b, n = R.randint(1, 4), R.randint(1, 4), R.randint(2, 4)
        if a == b: return False
        M = [[a ** n, 0], [0, b ** n]]
        return add('lin', f"¿Cuánto es {mq([[a, 0], [0, b]])}^{n}?" if n > 3 else f"¿Cuánto es {mq([[a, 0], [0, b]])}{sup(n)}?", ms(M), [ms([[a * n, 0], [0, b * n]]), ms([[a ** n, 0], [0, b]]), ms([[a ** n, b ** n], [b ** n, a ** n]]), ms([[a ** (n + 1), 0], [0, b ** (n + 1)]])], "Elevar una matriz diagonal es elevar cada entrada diagonal.", 40 + n * 2 + a, acc=macc(M))
    if k == 1:
        n = R.randint(2, 9); c = R.randint(1, 3)
        M = [[1, n * c], [0, 1]]
        return add('lin', f"¿Cuánto es {mq([[1, c], [0, 1]])}^{n}?", ms(M), [ms([[1, c], [0, 1]]), ms([[1, c ** n], [0, 1]]), ms([[n, c * n], [0, n]]), ms([[1, c + n], [0, 1]])], f"Se acumula la entrada superior: {n}·{c}.", 56 + n, acc=macc(M))
    n = R.randint(2, 6); a = R.randint(2, 5)
    return add('lin', f"Si A tiene autovalor λ = {a}, ¿qué autovalor tiene A^{n} para el mismo autovector?", a ** n, numwrong(a ** n, pos=True, extra=[a * n]), "Aᵏv = λᵏv.", 62 + n)


def l_eigprop():
    k = R.randint(0, 1)
    ls = [R.randint(-3, 6) for _ in range(3)]
    if k == 0:
        return add('lin', f"Una matriz 3×3 tiene autovalores {ls[0]}, {ls[1]} y {ls[2]}. ¿Cuál es su traza?".replace('-', '−'), sum(ls), numwrong(sum(ls), extra=[ls[0] * ls[1] * ls[2]]), "La traza es la suma de los autovalores.", 60 + sum(map(abs, ls)) / 4)
    return add('lin', f"Una matriz 3×3 tiene autovalores {ls[0]}, {ls[1]} y {ls[2]}. ¿Cuál es su determinante?".replace('-', '−'), ls[0] * ls[1] * ls[2], numwrong(ls[0] * ls[1] * ls[2], extra=[sum(ls)]), "El determinante es el producto de los autovalores.", 62 + sum(map(abs, ls)) / 4)


CONC_LIN = [
    ("¿Qué es un vector?", "Un objeto con magnitud y dirección", ["Un número sin dirección", "Una matriz cuadrada", "Una ecuación lineal"], "Se representa con componentes.", 6),
    ("¿Qué es un escalar?", "Un número real", ["Un vector unitario", "Una matriz diagonal", "Un sistema de ecuaciones"], "Multiplica vectores y matrices.", 4),
    ("¿Cómo se llama una matriz con el mismo número de filas y columnas?", "Cuadrada", ["Diagonal", "Nula", "Simétrica"], "Tiene tamaño n×n.", 8),
    ("¿Cómo se llama la matriz con 1 en la diagonal y 0 en el resto?", "Matriz identidad", ["Matriz nula", "Matriz transpuesta", "Matriz inversa"], "AI = IA = A.", 10),
    ("¿Qué es una matriz simétrica?", "Una matriz igual a su transpuesta", ["Una matriz con determinante 0", "Una matriz con todas las entradas iguales", "Una matriz triangular"], "A = Aᵀ.", 22),
    ("¿Es conmutativa la multiplicación de matrices?", "No, en general AB ≠ BA", ["Sí, siempre", "Solo para matrices 2×2", "Solo si son invertibles"], "El orden importa.", 30),
    ("¿Cuándo se pueden multiplicar dos matrices A (m×n) y B (p×q)?", "Cuando n = p", ["Cuando m = q", "Cuando m = p", "Siempre"], "Las columnas de A deben coincidir con las filas de B.", 26),
    ("Si A es m×n y B es n×p, ¿qué tamaño tiene AB?", "m×p", ["n×n", "m×n", "p×m"], "Se conservan filas de A y columnas de B.", 28),
    ("¿Qué significa que una matriz sea invertible?", "Que existe A⁻¹ tal que AA⁻¹ = I", ["Que tiene entradas enteras", "Que su traza es 0", "Que es simétrica"], "Equivale a det A ≠ 0.", 44),
    ("Si det A = 0, ¿qué se puede afirmar?", "A no es invertible", ["A es la identidad", "A es simétrica", "A tiene inversa"], "Es una matriz singular.", 42),
    ("¿Qué ocurre con el determinante si se intercambian dos filas?", "Cambia de signo", ["No cambia", "Se duplica", "Se vuelve 0"], "Es una propiedad del determinante.", 50),
    ("¿Qué ocurre con el determinante si una fila es múltiplo de otra?", "Vale 0", ["Vale 1", "Es negativo", "Se duplica"], "Las filas son dependientes.", 50),
    ("¿Cuál es el determinante de la matriz identidad?", "1", ["0", "−1", "n"], "det I = 1.", 26),
    ("¿Qué es un autovector de A?", "Un vector no nulo v con Av = λv", ["Un vector con norma 1", "Un vector perpendicular a A", "La fila de mayor suma"], "A solo lo estira o lo encoge.", 66),
    ("¿Cómo se obtienen los autovalores de A?", "Resolviendo det(A − λI) = 0", ["Resolviendo det A = λ", "Sumando las filas", "Invirtiendo A"], "Es la ecuación característica.", 64),
    ("¿Qué son vectores linealmente independientes?", "Ninguno es combinación lineal de los demás", ["Todos son perpendiculares", "Todos tienen igual norma", "Suman cero"], "Solo la combinación trivial da el vector nulo.", 48),
    ("¿Qué es una base de un espacio vectorial?", "Un conjunto independiente que genera el espacio", ["Cualquier conjunto de vectores", "Un conjunto de vectores unitarios", "Un conjunto con el vector nulo"], "Su tamaño es la dimensión.", 58),
    ("¿Cuál es la dimensión de ℝ³?", "3", ["2", "4", "9"], "Una base tiene 3 vectores.", 24),
    ("¿Qué es el espacio nulo (núcleo) de A?", "El conjunto de vectores x con Ax = 0", ["El conjunto de filas de A", "La imagen de A", "El conjunto de autovalores"], "Se denota Nul A o ker A.", 62),
    ("¿Qué indica un producto punto igual a cero?", "Que los vectores son ortogonales", ["Que son paralelos", "Que son iguales", "Que tienen norma 0"], "u·v = ‖u‖‖v‖cos θ.", 24),
    ("¿Qué indica un producto cruz igual al vector nulo?", "Que los vectores son paralelos", ["Que son perpendiculares", "Que son unitarios", "Que son independientes"], "‖u × v‖ = ‖u‖‖v‖sen θ.", 58),
    ("¿Qué dirección tiene u × v?", "Perpendicular a u y a v", ["Paralela a u", "Paralela a v", "Igual a u + v"], "Se obtiene con la regla de la mano derecha.", 54),
    ("¿Qué es un vector unitario?", "Un vector de norma 1", ["Un vector con componentes iguales", "Un vector nulo", "Un vector con una sola componente"], "Se obtiene dividiendo entre la norma.", 20),
    ("¿Qué es la traza de una matriz cuadrada?", "La suma de los elementos de su diagonal principal", ["El producto de la diagonal", "La suma de todas las entradas", "El mayor autovalor"], "tr(A) = Σ aᵢᵢ.", 18),
    ("¿Qué relación hay entre la traza y los autovalores?", "La traza es la suma de los autovalores", ["Es el producto de los autovalores", "Es el mayor autovalor", "Es el determinante"], "tr A = Σ λᵢ.", 62),
    ("¿Qué relación hay entre el determinante y los autovalores?", "El determinante es el producto de los autovalores", ["Es la suma de los autovalores", "Es el menor autovalor", "Es la traza"], "det A = Π λᵢ.", 64),
    ("¿Qué es el rango de una matriz?", "El número máximo de filas (o columnas) linealmente independientes", ["El número de filas", "El mayor elemento", "La suma de las columnas"], "Es la dimensión del espacio columna.", 46),
    ("¿Qué es una matriz ortogonal?", "Una matriz con AᵀA = I", ["Una matriz con det 0", "Una matriz con todas las entradas 1", "Una matriz triangular"], "Sus columnas son ortonormales.", 70),
    ("¿Qué es una matriz diagonalizable?", "Una matriz semejante a una matriz diagonal", ["Una matriz con ceros", "Una matriz sin inversa", "Una matriz con traza cero"], "A = PDP⁻¹.", 78),
    ("¿Qué es un sistema homogéneo?", "Un sistema de la forma Ax = 0", ["Un sistema con una sola ecuación", "Un sistema sin solución", "Un sistema con coeficientes iguales"], "Siempre tiene al menos la solución trivial.", 48),
    ("¿Qué es la eliminación gaussiana?", "Un método para escalonar una matriz mediante operaciones elementales de fila", ["Un método para derivar", "Un método para hallar autovalores", "Un método para multiplicar matrices"], "Sirve para resolver sistemas.", 40),
    ("¿Qué es una transformación lineal?", "Una función T con T(u + v) = T(u) + T(v) y T(cu) = cT(u)", ["Cualquier función entre vectores", "Una función que solo traslada", "Una función cuadrática"], "Preserva sumas y múltiplos escalares.", 56),
    ("¿Qué es el espacio columna de una matriz?", "El conjunto de todas las combinaciones lineales de sus columnas", ["El conjunto de sus filas", "El conjunto de sus autovalores", "El núcleo de la matriz"], "Es la imagen de la transformación.", 62),
    ("¿Cuál es la inversa de la matriz identidad?", "Ella misma", ["La matriz nula", "La matriz con −1", "No existe"], "II = I.", 20),
    ("¿Qué propiedad tiene (AB)ᵀ?", "(AB)ᵀ = BᵀAᵀ", ["(AB)ᵀ = AᵀBᵀ", "(AB)ᵀ = AB", "(AB)ᵀ = −AB"], "El orden se invierte.", 58),
    ("¿Qué propiedad tiene (AB)⁻¹?", "(AB)⁻¹ = B⁻¹A⁻¹", ["(AB)⁻¹ = A⁻¹B⁻¹", "(AB)⁻¹ = AB", "(AB)⁻¹ = BA"], "El orden se invierte.", 62),
]


def l_conc():
    for q, c, w, e, d_ in CONC_LIN:
        add('lin', q, c, w, e, d_)


def build_lin():
    plan = [(l_vsum, 26), (l_vscal, 18), (l_vdot, 36), (l_vnorm, 28), (l_vorth, 14), (l_vproj, 14), (l_vcross, 30), (l_varea, 18), (l_vangle, 12),
            (l_madd, 26), (l_mscal, 18), (l_mmul, 60), (l_mtrans, 18), (l_mtrace, 14), (l_mdet2, 34), (l_mdet3, 40), (l_minv, 44), (l_meig, 60), (l_meigv, 18),
            (l_rank, 30), (l_sys, 46), (l_lt, 22), (l_lt2, 18), (l_basis, 26), (l_detprop, 26), (l_comb, 22), (l_plane, 16), (l_powers, 20), (l_eigprop, 16)]
    for fn, n in plan: rep(n, fn)
    l_conc()
