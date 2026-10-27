from lib import *
from fractions import Fraction as F
from math import comb, perm, factorial, gcd, isqrt, sqrt
B = Bank()

def want(n, cat, fn, tries=400):
    have = lambda: len(B.cats.get(cat, []))
    target = have() + n
    t = 0
    while have() < target and t < tries:
        fn(); t += 1

def sgn(n):  # '+ 3' / '− 3'
    return f'+ {n}' if n >= 0 else f'− {-n}'
def lin_expr(a, b):  # 'ax + b'
    return poly([a, b])

# ================= ÁLGEBRA =================
def a_add():
    a, b = R.randint(1, 9), R.randint(1, 9)
    B.add('alg', f'¿Cuánto es {a} + {b}?', a+b, near_int(a+b), R.randint(0, 3), f'{a} + {b} = {a+b}.', [str(a+b)])
def a_sub():
    a = R.randint(6, 20); b = R.randint(1, a-1)
    B.add('alg', f'¿Cuánto es {a} − {b}?', a-b, near_int(a-b), R.randint(2, 6), f'{a} − {b} = {a-b}.', [str(a-b)])
def a_mul():
    a, b = R.randint(2, 9), R.randint(2, 9)
    B.add('alg', f'¿Cuánto es {a} × {b}?', a*b, near_int(a*b, [a*b+a, a*b-b]), R.randint(5, 12), f'{a} × {b} = {a*b}.', [str(a*b)])
def a_div():
    b = R.randint(2, 9); q = R.randint(2, 12); a = b*q
    B.add('alg', f'¿Cuánto es {a} ÷ {b}?', q, near_int(q), R.randint(8, 16), f'{a} ÷ {b} = {q}, porque {b} × {q} = {a}.', [str(q)])
def a_order():
    a, b, c = R.randint(2, 9), R.randint(2, 9), R.randint(2, 6)
    r = a + b*c
    B.add('alg', f'Calcula respetando el orden de las operaciones: {a} + {b} × {c}', r, near_int(r, [(a+b)*c]), R.randint(12, 24), 'Primero la multiplicación y luego la suma.', [str(r)])
def a_order2():
    a, b, c = R.randint(2, 6), R.randint(2, 8), R.randint(2, 5)
    r = (a+b)*c
    B.add('alg', f'Calcula: ({a} + {b}) × {c}', r, near_int(r, [a+b*c]), R.randint(14, 26), 'Los paréntesis se resuelven primero.', [str(r)])
def a_eq1():
    x = R.randint(1, 15); a = R.randint(1, 12); k = R.choice([0, 1, 2, 3])
    if k == 0: q, s = f'Resuelve: x + {a} = {x+a}', 'Se resta '+str(a)+' a ambos lados.'
    elif k == 1: q, s = f'Resuelve: x − {a} = {x-a}', 'Se suma '+str(a)+' a ambos lados.'
    elif k == 2: a = R.randint(2, 9); q, s = f'Resuelve: {a}x = {a*x}', 'Se divide entre '+str(a)+' a ambos lados.'
    else: a = R.randint(2, 9); q, s = f'Resuelve: x/{a} = {x}', 'Se multiplica por '+str(a)+' a ambos lados.'; x = x*a
    ans = x
    B.add('alg', q, f'x = {ans}', [f'x = {w}' for w in pick_near(ans)], R.randint(14, 24), s, [str(ans), f'x={ans}'])
def a_eq2():
    x = R.randint(-6, 12); a = R.randint(2, 9); b = R.randint(1, 15)
    c = a*x + b
    B.add('alg', f'Resuelve: {a}x + {b} = {c}', f'x = {x}', [f'x = {w}' for w in pick_near(x, [ (c+b)//a if a else 0, (c-b)//a + 1 ])], R.randint(24, 38), f'{a}x = {c-b}, entonces x = {x}.', [str(x), f'x={x}'])
def a_eq3():
    x = R.randint(-5, 10); a = R.randint(3, 9); c = R.randint(1, a-1); b = R.randint(-8, 12)
    d = a*x + b - c*x
    q = f'Resuelve: {cf(a)}x {sgn(b)} = {cf(c)}x {sgn(d)}'
    B.add('alg', q, f'x = {x}', [f'x = {w}' for w in pick_near(x)], R.randint(32, 46), 'Se juntan las x a un lado y los números al otro.', [str(x), f'x={x}'])
def a_frac():
    a, b, c, d = R.randint(1, 5), R.randint(2, 8), R.randint(1, 5), R.randint(2, 8)
    k = R.choice(['+', '−', '×'])
    x = F(a, b); y = F(c, d)
    r = x + y if k == '+' else x - y if k == '−' else x * y
    ex = [fr(F(a+c, b+d)), fr(F(a*c, b+d)) if k != '×' else fr(F(a+c, b*d))]
    ans = fr(r)
    wr = [w for w in ex if w != ans] + near_fr(r)
    B.add('alg', f'Calcula {a}/{b} {k} {c}/{d} (simplifica el resultado)', ans, wr, R.randint(30, 48), 'Se busca denominador común (suma/resta) o se multiplican numeradores y denominadores.', [ans])
def a_pct():
    p = R.choice([10, 20, 25, 50, 5, 15, 30, 40, 75]); n = R.choice([20, 40, 60, 80, 100, 120, 200, 240, 400])
    r = F(p*n, 100)
    ans = fr(r)
    B.add('alg', f'¿Cuánto es el {p}% de {n}?', ans, (pick_near(int(r), [n-int(r), p]) if r.denominator == 1 else near_fr(r)), R.randint(24, 40), f'{p}% de {n} = {n} × {p}/100 = {ans}.', [ans])
def a_pow():
    a = R.randint(2, 5); m, n = R.randint(2, 6), R.randint(2, 6)
    k = R.choice([0, 1, 2, 3])
    if k == 0:
        q = f'{a}{pw(m)} × {a}{pw(n)} = {a}^?'; ans = m+n; w = [m*n, m+n+1, abs(m-n)]
        e = 'Al multiplicar potencias de la misma base se suman los exponentes.'
    elif k == 1:
        mm, nn = max(m, n)+1, min(m, n)
        q = f'{a}^{mm} ÷ {a}^{nn} = {a}^?'; ans = mm-nn; w = [mm+nn, mm*nn, mm-nn+1]
        e = 'Al dividir potencias de la misma base se restan los exponentes.'
    elif k == 2:
        q = f'({a}{pw(m)})^{n} = {a}^?'; ans = m*n; w = [m+n, m**n, m*n+1]
        e = 'Potencia de una potencia: se multiplican los exponentes.'
    else:
        q = f'¿Cuánto vale {a}^{m}?'; ans = a**m; w = [a*m, a**(m+1), a**m - a]
        e = f'{a}^{m} = {" × ".join([str(a)]*m)} = {ans}.'
    B.add('alg', q, ans, [x for x in w], R.randint(30, 50), e, [str(ans)])
def a_sqrt():
    n = R.randint(2, 15); sq = n*n
    B.add('alg', f'¿Cuál es la raíz cuadrada de {sq}?', n, near_int(n, [n*2, sq//2]), R.randint(14, 28), f'{n} × {n} = {sq}.', [str(n), f'√{sq}'])
def a_expand():
    p, q = R.randint(-7, 8), R.randint(-7, 8)
    if p == 0 or q == 0: return
    ans = poly([1, p+q, p*q])
    w = [poly([1, p+q, -p*q]), poly([1, p*q, p+q]), poly([1, p-q, p*q])]
    B.add('alg', f'Desarrolla: (x {sgn(p)})(x {sgn(q)})', ans, w, R.randint(42, 62), 'x² + (p + q)x + pq.', plain(ans))
def a_factor():
    p, q = R.randint(-7, 8), R.randint(-7, 8)
    if p == 0 or q == 0 or p == q: return
    expr = poly([1, p+q, p*q])
    ans = f'(x {sgn(p)})(x {sgn(q)})'
    w = [f'(x {sgn(-p)})(x {sgn(q)})', f'(x {sgn(p)})(x {sgn(-q)})', f'(x {sgn(-p)})(x {sgn(-q)})']
    B.add('alg', f'Factoriza: {expr}', ans, w, R.randint(50, 70), f'Se buscan dos números que sumen {p+q} y multipliquen {p*q}.', plain(ans))
def a_quad():
    p, q = R.randint(-8, 8), R.randint(-8, 8)
    if p == q or p == 0 or q == 0: return
    lo, hi = sorted([p, q])
    expr = poly([1, -(p+q), p*q])
    ans = f'{lo} y {hi}'
    w = [f'{-lo} y {-hi}', f'{lo} y {-hi}', f'{-lo} y {hi}']
    B.add('alg', f'¿Cuáles son las soluciones de {expr} = 0?', ans, w, R.randint(55, 76), 'Se factoriza y se iguala cada factor a cero.', [ans, f'{lo},{hi}', f'{lo} {hi}', f'{lo} y {hi}'])
def a_disc():
    a, b, c = R.randint(1, 4), R.randint(-8, 8), R.randint(-6, 6)
    if b == 0: return
    D = b*b - 4*a*c
    B.add('alg', f'Calcula el discriminante de {poly([a, b, c])} = 0', D, pick_near(D, [b*b+4*a*c, b*b-2*a*c]), R.randint(58, 74), 'Δ = b² − 4ac.', [str(D)])
def a_sys():
    x, y = R.randint(-6, 9), R.randint(-6, 9)
    s, t = x+y, x-y
    ans = f'x = {x}, y = {y}'
    w = [f'x = {y}, y = {x}', f'x = {x+1}, y = {y-1}', f'x = {-x}, y = {-y}']
    B.add('alg', f'Resuelve el sistema: x + y = {s}  y  x − y = {t}', ans, w, R.randint(46, 66), 'Sumando las dos ecuaciones sale 2x.', [ans, f'{x},{y}', f'x={x},y={y}', f'{x} {y}'])
def a_log():
    b = R.choice([2, 3, 5, 10]); k = R.randint(2, 5)
    n = b**k
    B.add('alg', f'¿Cuánto vale log base {b} de {n}?', k, pick_near(k, [k+1]), R.randint(60, 82), f'{b}^{k} = {n}, así que el logaritmo es {k}.', [str(k)])
def a_seq():
    a1, d, n = R.randint(1, 9), R.randint(2, 7), R.randint(5, 12)
    an = a1 + (n-1)*d
    seq = ', '.join(str(a1+i*d) for i in range(4))
    B.add('alg', f'En la sucesión {seq}, … ¿cuál es el término número {n}?', an, pick_near(an, [an+d, an-d]), R.randint(46, 66), f'aₙ = a₁ + (n − 1)d = {a1} + {n-1}·{d} = {an}.', [str(an)])
def a_sumseq():
    n = R.choice([10, 20, 50, 100]); s = n*(n+1)//2
    B.add('alg', f'¿Cuánto suman los números del 1 al {n}?', s, pick_near(s, [s+n, n*n]), R.randint(55, 72), 'Fórmula de Gauss: n(n + 1)/2.', [str(s)])
def a_ineq():
    a = R.randint(2, 6); b = R.randint(1, 9); x = R.randint(1, 8)
    c = a*x + b
    op = R.choice(['>', '<'])
    flip = {'>': '<', '<': '>'}[op]
    ans = f'x {op} {x}'
    B.add('alg', f'Resuelve la inecuación: {a}x + {b} {op} {c}', ans, [f'x {flip} {x}', f'x {op} {x+1}', f'x {op} {c-b}'], R.randint(48, 66), 'Se despeja igual que una ecuación; el signo solo cambia al multiplicar o dividir por un negativo.', [ans, ans.replace(' ', '')])
def a_abs():
    a, b = R.randint(1, 8), R.randint(1, 7)
    lo, hi = a-b, a+b
    ans = f'{lo} y {hi}'
    B.add('alg', f'¿Cuáles son las soluciones de |x − {a}| = {b}?', ans, [f'{-lo} y {-hi}', f'{a} y {b}', f'{lo} y {-hi}'], R.randint(52, 70), 'x − a puede ser b o −b.', [ans, f'{lo},{hi}'])
def a_simplify():
    a, b = R.randint(2, 9), R.randint(2, 9)
    x = a*b
    B.add('alg', f'Simplifica: {a}x + {b}x', f'{a+b}x', [f'{a*b}x', f'{a+b}x²', f'{abs(a-b)}x'], R.randint(14, 26), 'Se suman los coeficientes de términos semejantes.', [f'{a+b}x'])
def a_subst():
    a, b, x = R.randint(2, 6), R.randint(-5, 9), R.randint(2, 7)
    v = a*x + b
    B.add('alg', f'Si f(x) = {lin_expr(a, b)}, ¿cuánto vale f({x})?', v, pick_near(v, [a+x+b, a*(x+b)]), R.randint(22, 36), f'f({x}) = {a}·{x} {sgn(b)} = {v}.', [str(v)])
def a_slope():
    x1, y1 = R.randint(0, 4), R.randint(0, 6); m = R.randint(-4, 5)
    if m == 0: return
    dx = R.randint(1, 4); x2, y2 = x1+dx, y1+m*dx
    ans = m
    B.add('alg', f'¿Cuál es la pendiente de la recta que pasa por ({x1}, {y1}) y ({x2}, {y2})?', ans, pick_near(ans, [-ans, dx]), R.randint(44, 62), 'm = (y₂ − y₁)/(x₂ − x₁).', [str(ans)])

want(8, 'alg', a_add); want(7, 'alg', a_sub); want(9, 'alg', a_mul); want(7, 'alg', a_div)
want(6, 'alg', a_order); want(5, 'alg', a_order2); want(8, 'alg', a_simplify); want(8, 'alg', a_sqrt)
want(10, 'alg', a_eq1); want(8, 'alg', a_subst); want(10, 'alg', a_eq2); want(8, 'alg', a_pct)
want(8, 'alg', a_eq3); want(9, 'alg', a_frac); want(8, 'alg', a_pow); want(6, 'alg', a_seq)
want(6, 'alg', a_slope); want(6, 'alg', a_ineq); want(6, 'alg', a_sys); want(6, 'alg', a_abs)
want(8, 'alg', a_expand); want(8, 'alg', a_factor); want(6, 'alg', a_sumseq); want(8, 'alg', a_quad)
want(5, 'alg', a_disc); want(5, 'alg', a_log)
conc = [
 ('¿Qué es una variable en álgebra?', 'Un símbolo que representa un número desconocido', ['Un número que nunca cambia', 'Una operación entre fracciones', 'Un tipo de gráfica'], 6, 'Letras como x o y representan valores que pueden variar o que se quieren encontrar.'),
 ('¿Cuál es el resultado de cualquier número multiplicado por cero?', '0', ['El mismo número', '1', 'No está definido'], 4, 'Todo número por 0 da 0.'),
 ('¿Qué propiedad dice que a + b = b + a?', 'Conmutativa', ['Asociativa', 'Distributiva', 'Identidad'], 16, 'La suma no cambia al intercambiar el orden.'),
 ('¿Qué propiedad dice que a(b + c) = ab + ac?', 'Distributiva', ['Conmutativa', 'Asociativa', 'Inversa'], 22, 'La multiplicación se distribuye sobre la suma.'),
 ('¿Cuánto es cualquier número distinto de cero elevado a la 0?', '1', ['0', 'El mismo número', 'No existe'], 38, 'a⁰ = 1 si a ≠ 0.'),
 ('¿Qué tipo de gráfica tiene una función cuadrática?', 'Una parábola', ['Una recta', 'Una circunferencia', 'Una hipérbola'], 40, 'f(x) = ax² + bx + c se dibuja como parábola.'),
 ('En y = mx + b, ¿qué representa b?', 'La ordenada al origen', ['La pendiente', 'La raíz de la función', 'El área bajo la recta'], 34, 'Es el valor de y cuando x = 0.'),
 ('¿Cuántas soluciones reales tiene una ecuación cuadrática con discriminante negativo?', 'Ninguna', ['Una', 'Dos', 'Infinitas'], 60, 'Si Δ < 0 no hay raíces reales.'),
 ('¿Qué se obtiene al factorizar la diferencia de cuadrados a² − b²?', '(a + b)(a − b)', ['(a − b)²', '(a + b)²', 'a(a − b)'], 56, 'Producto notable: a² − b² = (a + b)(a − b).'),
 ('¿Qué es el inverso aditivo de 7?', '−7', ['1/7', '7', '0'], 12, 'Es el número que sumado a 7 da 0.'),
 ('¿Qué es el inverso multiplicativo de 4?', '1/4', ['−4', '4', '0'], 18, 'Es el número que multiplicado por 4 da 1.'),
 ('¿Cuál es el logaritmo de 1 en cualquier base válida?', '0', ['1', 'La base', 'No existe'], 66, 'Porque b⁰ = 1.'),
]
for q, a, w, d, e in conc: B.add('alg', q, a, w, d, e, [a])

# ================= CÁLCULO =================
def c_lim_lin():
    a, b, x = R.randint(1, 6), R.randint(-6, 9), R.randint(-4, 6)
    v = a*x + b
    B.add('calc', f'Calcula el límite cuando x → {x} de ({lin_expr(a, b)})', v, pick_near(v), R.randint(6, 18), 'En una función continua el límite es el valor de la función.', [str(v)])
def c_lim_poly():
    a, x = R.randint(1, 4), R.randint(1, 4)
    b, c = R.randint(-5, 6), R.randint(-6, 8)
    v = a*x*x + b*x + c
    B.add('calc', f'Calcula: límite cuando x → {x} de ({poly([a, b, c])})', v, pick_near(v), R.randint(14, 28), 'Se sustituye x por el valor, pues el polinomio es continuo.', [str(v)])
def c_lim_ind():
    a = R.randint(1, 9)
    B.add('calc', f'Calcula el límite cuando x → {a} de (x² − {a*a})/(x − {a})', 2*a, pick_near(2*a, [a, a*a]), R.randint(34, 52), f'Se factoriza: (x − {a})(x + {a})/(x − {a}) = x + {a}, que vale {2*a}.', [str(2*a)])
def c_lim_inf():
    a, b = R.randint(1, 6), R.randint(1, 6); c, d = R.randint(1, 6), R.randint(1, 6)
    v = F(a, c)
    B.add('calc', f'Calcula el límite cuando x → ∞ de ({cf(a)}x² + {cf(b)}x)/({cf(c)}x² + {d})', fr(v), near_fr(v, [fr(F(b, d))]), R.randint(50, 66), 'Con el mismo grado arriba y abajo, el límite es el cociente de los coeficientes principales.', [fr(v)])
def c_d_pow():
    n = R.randint(2, 7)
    ans = f'{n}x{pw(n-1)}' if n > 2 else '2x'
    ans = ans if n != 2 else '2x'
    xp = lambda k: ('x' + (pw(k) if k > 1 else '')) if k >= 1 else '1'
    ans = f'{n}{xp(n-1)}' if n-1 >= 1 else f'{n}'
    w = [f'{n-1}{xp(n-2)}' if n-2 >= 1 else f'{n-1}', f'{xp(n-1)}', f'{n}{xp(n)}']
    B.add('calc', f'¿Cuál es la derivada de f(x) = x{pw(n)}?', ans, w, R.randint(5, 16), 'Regla de la potencia: (xⁿ)′ = n·xⁿ⁻¹.', plain(ans))
def c_d_cx():
    c, n = R.randint(2, 8), R.randint(2, 6)
    xp = lambda k: ('x' + (pw(k) if k > 1 else '')) if k >= 1 else ''
    ans = f'{c*n}{xp(n-1)}'
    w = [f'{c*(n-1)}{xp(n-1)}', f'{c+n}{xp(n-1)}', f'{c}{xp(n-1)}']
    B.add('calc', f'Deriva f(x) = {c}x{pw(n)}', ans, w, R.randint(12, 26), 'Se multiplica el coeficiente por el exponente y se baja un grado.', plain(ans))
def c_d_poly():
    a, b, c = R.randint(1, 6), R.randint(-7, 8), R.randint(-6, 9)
    if b == 0: return
    f = poly([a, b, c]); ans = poly([2*a, b]); 
    w = [poly([2*a, b, c]), poly([a, b]), poly([2*a, 2*b])]
    B.add('calc', f'Deriva f(x) = {f}', ans, w, R.randint(22, 38), 'La derivada de una constante es 0.', plain(ans))
def c_d_cubic():
    a, b, c, d = R.randint(1, 4), R.randint(-5, 6), R.randint(-6, 7), R.randint(-5, 9)
    if b == 0 or c == 0: return
    f = poly([a, b, c, d]); ans = poly([3*a, 2*b, c])
    w = [poly([3*a, 2*b, c, d]), poly([3*a, b, c]), poly([a, 2*b, c])]
    B.add('calc', f'Deriva f(x) = {f}', ans, w, R.randint(30, 46), 'Se aplica la regla de la potencia a cada término.', plain(ans))
def c_d_point():
    a, b, x = R.randint(1, 4), R.randint(-5, 6), R.randint(-3, 4)
    v = 2*a*x + b
    B.add('calc', f'Si f(x) = {poly([a, b, R.randint(1, 5)])}, ¿cuánto vale f′({x})?', v, pick_near(v, [a*x*x + b*x]), R.randint(34, 50), f'f′(x) = {poly([2*a, b])}; en x = {x} da {v}.', [str(v)])
def c_d_trig():
    k = R.randint(2, 7); f = R.choice(['sin', 'cos', 'e', 'ln'])
    if f == 'sin': q, ans, w = f'Deriva f(x) = {k}sen(x)', f'{k}cos(x)', [f'−{k}cos(x)', f'{k}sen(x)', f'cos(x)']
    elif f == 'cos': q, ans, w = f'Deriva f(x) = {k}cos(x)', f'−{k}sen(x)', [f'{k}sen(x)', f'−sen(x)', f'{k}cos(x)']
    elif f == 'e': q, ans, w = f'Deriva f(x) = {k}eˣ', f'{k}eˣ', [f'{k}xeˣ⁻¹', f'eˣ', f'{k-1}eˣ']
    else: q, ans, w = f'Deriva f(x) = {k}ln(x)', f'{k}/x', [f'{k}x', f'1/x', f'{k}ln(x)/x']
    B.add('calc', q, ans, w, R.randint(30, 46), 'Derivadas básicas de funciones trascendentes.', [ans, ans.replace('sen', 'sin')])
def c_d_prod():
    a, b, x = R.randint(1, 5), R.randint(1, 5), R.randint(1, 4)
    f = lambda t: (t+a)*(t+b)
    v = (x+b) + (x+a)
    B.add('calc', f'Con f(x) = (x + {a})(x + {b}), ¿cuánto vale f′({x})?', v, pick_near(v, [f(x), 1]), R.randint(52, 68), 'Regla del producto: (uv)′ = u′v + uv′.', [str(v)])
def c_d_chain():
    a, b, n = R.randint(2, 5), R.randint(1, 6), R.randint(2, 5)
    base = f'({a}x + {b})'
    k = a*n
    ans = f'{k}{base}{pw(n-1)}' if n-1 > 1 else f'{k}{base}'
    w = [f'{n}{base}{pw(n-1)}' if n-1 > 1 else f'{n}{base}', f'{a}{base}{pw(n-1)}' if n-1 > 1 else f'{a}{base}', f'{k}{base}{pw(n)}']
    B.add('calc', f'Deriva f(x) = {base}{pw(n)}', ans, w, R.randint(58, 76), 'Regla de la cadena: n·(interior)ⁿ⁻¹ por la derivada del interior.', plain(ans))
def c_d_chain2():
    a = R.randint(2, 9); f = R.choice(['sin', 'cos', 'e'])
    if f == 'sin': q, ans, w = f'Deriva f(x) = sen({a}x)', f'{a}cos({a}x)', [f'cos({a}x)', f'−{a}cos({a}x)', f'{a}sen({a}x)']
    elif f == 'cos': q, ans, w = f'Deriva f(x) = cos({a}x)', f'−{a}sen({a}x)', [f'{a}sen({a}x)', f'−sen({a}x)', f'{a}cos({a}x)']
    else: q, ans, w = f'Deriva f(x) = e^({a}x)', f'{a}e^({a}x)', [f'e^({a}x)', f'{a}xe^({a}x)', f'e^({a})']
    B.add('calc', q, ans, w, R.randint(62, 80), 'Se multiplica por la derivada de la función interior.', [ans, ans.replace('sen', 'sin')])
def c_crit():
    b = R.choice([2, 4, 6, 8, 10, 12, -2, -4, -6, -8]); c = R.randint(0, 9)
    x = F(b, 2)*-1
    f = poly([1, b, c]); 
    B.add('calc', f'¿En qué valor de x tiene un punto crítico f(x) = {f}?', f'x = {x.numerator}', [f'x = {w}' for w in pick_near(int(x), [-int(x), b])], R.randint(52, 70), 'Se resuelve f′(x) = 0.', [str(int(x)), f'x={int(x)}'])
def c_minval():
    h, k = R.randint(1, 6), R.randint(1, 9)
    f = poly([1, -2*h, h*h+k])
    B.add('calc', f'¿Cuál es el valor mínimo de f(x) = {f}?', k, pick_near(k, [h*h+k, h]), R.randint(60, 76), f'Se completa el cuadrado: (x − {h})² + {k}.', [str(k)])
def c_int():
    n = R.randint(1, 6)
    xp = lambda k: 'x' + (pw(k) if k > 1 else '')
    ans = f'{xp(n+1)}/{n+1} + C'
    w = [f'{xp(n)}/{n+1} + C', f'{n}{xp(n-1)} + C' if n > 1 else '1 + C', f'{xp(n+1)} + C']
    B.add('calc', f'Calcula la integral de x{pw(n) if n > 1 else ""} dx', ans, w, R.randint(18, 34), '∫xⁿ dx = xⁿ⁺¹/(n + 1) + C.', [ans, ans.replace(' ', '')])
def c_int_c():
    c, n = R.randint(2, 6), R.choice([1, 2, 3])
    k = F(c, n+1)
    xp = lambda m: 'x' + (pw(m) if m > 1 else '')
    ans = (f'({fr(k)}){xp(n+1)} + C' if k.denominator != 1 else f'{k.numerator}{xp(n+1)} + C')
    w = [f'{c}{xp(n+1)} + C', f'{c*(n+1)}{xp(n+1)} + C', f'({fr(k)}){xp(n)} + C' if k.denominator != 1 else f'{k.numerator}{xp(n)} + C']
    B.add('calc', f'Calcula la integral de {c}x{pw(n) if n > 1 else ""} dx', ans, w, R.randint(28, 44), 'Se integra la potencia y se conserva el coeficiente.', [ans, ans.replace(' ', '')])
def c_defint():
    a, b = R.randint(1, 6), R.randint(0, 8); n = R.randint(1, 4)
    v = F(a*n*n, 2) + b*n
    B.add('calc', f'Calcula la integral definida de 0 a {n} de ({cf(a)}x + {b}) dx', fr(v), near_fr(v, [fr(F(a*n+b))]), R.randint(40, 58), 'Se integra y se evalúa: (a·n²/2 + b·n).', [fr(v)])
def c_defint2():
    n = R.randint(1, 4); k = R.randint(1, 3)
    m = R.randint(1, 3)
    v = F(k*n**(m+1), m+1)
    B.add('calc', f'Calcula la integral definida de 0 a {n} de {cf(k)}x{pw(m) if m>1 else ""} dx', fr(v), near_fr(v, [fr(F(k*n**m))]), R.randint(46, 64), 'Se evalúa la antiderivada en los extremos.', [fr(v)])
def c_int_exp():
    a = R.randint(2, 7); f = R.choice(['exp', 'cos', 'inv'])
    if f == 'exp': q, ans, w = f'Calcula la integral de e^({a}x) dx', f'e^({a}x)/{a} + C', [f'e^({a}x) + C', f'{a}e^({a}x) + C', f'e^({a}x)/{a+1} + C']
    elif f == 'cos': q, ans, w = f'Calcula la integral de cos({a}x) dx', f'sen({a}x)/{a} + C', [f'−sen({a}x)/{a} + C', f'sen({a}x) + C', f'{a}sen({a}x) + C']
    else: q, ans, w = f'Calcula la integral de {a}/x dx', f'{a}ln|x| + C', [f'ln|x|/{a} + C', f'{a}/x² + C', f'ln|{a}x|² + C']
    B.add('calc', q, ans, w, R.randint(64, 84), 'Se compensa con el factor de la derivada interna.', [ans, ans.replace('sen', 'sin'), ans.replace(' ', '')])
def c_subst():
    n = R.randint(2, 5)
    q = f'Calcula la integral de {2*n}x(x² + 1)^{n-1} dx' if n > 2 else f'Calcula la integral de 4x(x² + 1) dx'
    ans = f'(x² + 1){pw(n)} + C'
    w = [f'(x² + 1){pw(n)}/{n} + C', f'{2*n}x(x² + 1){pw(n)} + C', f'(x² + 1){pw(n-1)} + C' if n-1 > 1 else '(x² + 1) + C']
    if n == 2: ans, w = '(x² + 1)² + C', ['(x² + 1)²/2 + C', '4x(x² + 1)² + C', '(x² + 1) + C']
    B.add('calc', q, ans, w, R.randint(78, 92), 'Con u = x² + 1, du = 2x dx.', [ans, ans.replace('²', '^2').replace('³', '^3')])
def c_d2():
    n = R.randint(3, 6); c = R.randint(1, 5)
    xp = lambda k: 'x' + (pw(k) if k > 1 else '') if k >= 1 else ''
    ans = f'{c*n*(n-1)}{xp(n-2)}' if n-2 >= 1 else f'{c*n*(n-1)}'
    w = [f'{c*n}{xp(n-1)}', f'{c*(n-1)}{xp(n-2)}' if n-2 >= 1 else f'{c*(n-1)}', f'{c*n*(n-1)}{xp(n-1)}']
    B.add('calc', f'¿Cuál es la segunda derivada de f(x) = {cf(c)}x{pw(n)}?', ans, w, R.randint(46, 62), 'Se deriva dos veces seguidas.', plain(ans))
def c_tan():
    a, b = R.randint(1, 3), R.randint(-4, 5); x = R.randint(1, 3)
    m = 2*a*x + b; y = a*x*x + b*x
    B.add('calc', f'¿Cuál es la pendiente de la recta tangente a f(x) = {poly([a, b])[:-0] if False else poly([a, b, 0])} en x = {x}?', m, pick_near(m, [y]), R.randint(46, 62), 'La pendiente de la tangente es f′(x).', [str(m)])
want(8, 'calc', c_lim_lin); want(8, 'calc', c_lim_poly); want(8, 'calc', c_d_pow); want(8, 'calc', c_d_cx)
want(8, 'calc', c_int); want(8, 'calc', c_d_poly); want(6, 'calc', c_lim_ind); want(8, 'calc', c_int_c)
want(8, 'calc', c_d_point); want(6, 'calc', c_d_trig); want(8, 'calc', c_d_cubic); want(8, 'calc', c_defint)
want(6, 'calc', c_defint2); want(6, 'calc', c_tan); want(6, 'calc', c_d2); want(6, 'calc', c_crit)
want(5, 'calc', c_lim_inf); want(6, 'calc', c_d_prod); want(6, 'calc', c_d_chain); want(6, 'calc', c_d_chain2)
want(5, 'calc', c_minval); want(6, 'calc', c_int_exp); want(4, 'calc', c_subst)
conc = [
 ('¿Qué representa la derivada de una función en un punto?', 'La pendiente de la recta tangente', ['El área bajo la curva', 'El valor máximo', 'El límite en infinito'], 14, 'Mide la razón de cambio instantánea.'),
 ('¿Cuál es la derivada de una constante?', '0', ['1', 'La constante', 'x'], 4, 'Una constante no cambia.'),
 ('¿Qué representa una integral definida?', 'El área bajo la curva', ['La pendiente en un punto', 'La raíz de la función', 'El valor máximo'], 24, 'Acumula el valor de la función en un intervalo.'),
 ('¿Qué enuncia el Teorema Fundamental del Cálculo?', 'Derivar e integrar son operaciones inversas', ['Toda función es continua', 'Todo límite existe', 'La derivada es siempre positiva'], 62, 'Conecta la derivada con la integral.'),
 ('Si f′(x) > 0 en un intervalo, la función es:', 'Creciente', ['Decreciente', 'Constante', 'Discontinua'], 36, 'Derivada positiva implica que la función sube.'),
 ('Si f″(x) > 0 en un punto, la gráfica es:', 'Cóncava hacia arriba', ['Cóncava hacia abajo', 'Una recta', 'Discontinua'], 54, 'La segunda derivada positiva indica concavidad hacia arriba.'),
 ('¿Cuánto vale el límite de sen(x)/x cuando x → 0?', '1', ['0', '∞', 'No existe'], 58, 'Es un límite notable.'),
 ('¿Cuál es el valor de e aproximadamente?', '2,718', ['3,141', '1,618', '1,414'], 30, 'El número de Euler.'),
 ('¿Qué indica una derivada que cambia de positiva a negativa?', 'Un máximo local', ['Un mínimo local', 'Una asíntota', 'Un cero de la función'], 56, 'La función deja de subir y empieza a bajar.'),
 ('¿Qué significa que una función sea continua en x = a?', 'El límite en a coincide con f(a)', ['La derivada vale 0', 'La gráfica es una recta', 'f(a) no existe'], 44, 'Sin saltos ni huecos en ese punto.'),
]
for q, a, w, d, e in conc: B.add('calc', q, a, w, d, e, [a])

# ================= ÁLGEBRA LINEAL =================
def mat(m): return '[[' + '], ['.join(', '.join(str(x) for x in r) for r in m) + ']]'
def l_vsum():
    a = [R.randint(-5, 9), R.randint(-5, 9)]; b = [R.randint(-5, 9), R.randint(-5, 9)]
    s = [a[0]+b[0], a[1]+b[1]]
    ans = f'({s[0]}, {s[1]})'
    B.add('lin', f'Calcula ({a[0]}, {a[1]}) + ({b[0]}, {b[1]})', ans, [f'({a[0]-b[0]}, {a[1]-b[1]})', f'({s[1]}, {s[0]})', f'({a[0]*b[0]}, {a[1]*b[1]})'], R.randint(4, 14), 'Se suma componente a componente.', [ans, ans.replace(' ', '')])
def l_vsc():
    k = R.randint(2, 6); a = [R.randint(-4, 7), R.randint(-4, 7), R.randint(-4, 7)]
    s = [k*x for x in a]
    ans = f'({s[0]}, {s[1]}, {s[2]})'
    B.add('lin', f'Calcula {k}·({a[0]}, {a[1]}, {a[2]})', ans, [f'({a[0]+k}, {a[1]+k}, {a[2]+k})', f'({s[0]}, {s[1]}, {s[2]+1})', f'({-s[0]}, {s[1]}, {s[2]})'], R.randint(8, 18), 'Se multiplica cada componente por el escalar.', [ans, ans.replace(' ', '')])
def l_dot():
    n = R.choice([2, 3]); a = [R.randint(-4, 7) for _ in range(n)]; b = [R.randint(-4, 7) for _ in range(n)]
    v = sum(x*y for x, y in zip(a, b))
    ta = '(' + ', '.join(map(str, a)) + ')'; tb = '(' + ', '.join(map(str, b)) + ')'
    B.add('lin', f'Calcula el producto punto {ta} · {tb}', v, pick_near(v, [sum(a)+sum(b), sum(x+y for x, y in zip(a, b))]), R.randint(18, 34), 'Se multiplican componentes y se suma.', [str(v)])
def l_norm():
    t = R.choice([(3, 4, 5), (5, 12, 13), (6, 8, 10), (8, 15, 17), (7, 24, 25), (9, 12, 15)])
    B.add('lin', f'¿Cuál es la norma (longitud) del vector ({t[0]}, {t[1]})?', t[2], pick_near(t[2], [t[0]+t[1], t[0]*t[1]]), R.randint(24, 40), 'Teorema de Pitágoras: √(a² + b²).', [str(t[2])])
def l_madd():
    A = [[R.randint(-4, 8) for _ in range(2)] for _ in range(2)]; C = [[R.randint(-4, 8) for _ in range(2)] for _ in range(2)]
    S = [[A[i][j]+C[i][j] for j in range(2)] for i in range(2)]
    ans = mat(S)
    wr = [mat([[A[i][j]-C[i][j] for j in range(2)] for i in range(2)]), mat([[A[i][j]*C[i][j] for j in range(2)] for i in range(2)]), mat([[S[0][0], S[1][0]], [S[0][1], S[1][1]]]) if S[0][1] != S[1][0] else mat([[S[0][0]+1, S[0][1]], [S[1][0], S[1][1]]])]
    B.add('lin', f'Suma las matrices {mat(A)} + {mat(C)}', ans, wr, R.randint(18, 32), 'Se suman las entradas en la misma posición.', [ans, ans.replace(' ', '')])
def l_trace():
    n = R.choice([2, 3]); A = [[R.randint(-5, 9) for _ in range(n)] for _ in range(n)]
    t = sum(A[i][i] for i in range(n))
    B.add('lin', f'¿Cuál es la traza de la matriz {mat(A)}?', t, pick_near(t, [sum(A[i][n-1-i] for i in range(n)), sum(sum(r) for r in A)]), R.randint(20, 34), 'La traza es la suma de la diagonal principal.', [str(t)])
def l_det2():
    A = [[R.randint(-5, 9) for _ in range(2)] for _ in range(2)]
    d = A[0][0]*A[1][1] - A[0][1]*A[1][0]
    B.add('lin', f'Calcula el determinante de {mat(A)}', d, pick_near(d, [A[0][0]*A[1][1]+A[0][1]*A[1][0], A[0][0]*A[1][1]]), R.randint(28, 44), 'det = ad − bc.', [str(d)])
def l_transp():
    A = [[R.randint(1, 9) for _ in range(3)] for _ in range(2)]
    T = [[A[0][0], A[1][0]], [A[0][1], A[1][1]], [A[0][2], A[1][2]]]
    ans = mat(T)
    wr = [mat(A), mat([[A[0][2], A[1][2]], [A[0][1], A[1][1]], [A[0][0], A[1][0]]]), mat([[A[1][0], A[0][0]], [A[1][1], A[0][1]], [A[1][2], A[0][2]]])]
    B.add('lin', f'¿Cuál es la transpuesta de {mat(A)}?', ans, wr, R.randint(24, 38), 'Las filas pasan a ser columnas.', [ans, ans.replace(' ', '')])
def l_mmul():
    A = [[R.randint(-3, 5) for _ in range(2)] for _ in range(2)]; C = [[R.randint(-3, 5) for _ in range(2)] for _ in range(2)]
    P = [[sum(A[i][k]*C[k][j] for k in range(2)) for j in range(2)] for i in range(2)]
    Q = [[sum(C[i][k]*A[k][j] for k in range(2)) for j in range(2)] for i in range(2)]
    ent = [[A[i][j]*C[i][j] for j in range(2)] for i in range(2)]
    ans = mat(P)
    wr = [mat(Q), mat(ent), mat([[P[0][0]+1, P[0][1]], [P[1][0], P[1][1]]])]
    B.add('lin', f'Multiplica {mat(A)} · {mat(C)}', ans, wr, R.randint(46, 64), 'Fila por columna.', [ans, ans.replace(' ', '')])
def l_mvec():
    A = [[R.randint(-3, 5) for _ in range(2)] for _ in range(2)]; v = [R.randint(-3, 5), R.randint(-3, 5)]
    r = [A[0][0]*v[0]+A[0][1]*v[1], A[1][0]*v[0]+A[1][1]*v[1]]
    ans = f'({r[0]}, {r[1]})'
    wr = [f'({A[0][0]*v[0]+A[1][0]*v[1]}, {A[0][1]*v[0]+A[1][1]*v[1]})', f'({r[1]}, {r[0]})', f'({A[0][0]*v[0]}, {A[1][1]*v[1]})']
    B.add('lin', f'Calcula {mat(A)} · ({v[0]}, {v[1]})', ans, wr, R.randint(40, 56), 'Cada resultado es una fila por el vector.', [ans, ans.replace(' ', '')])
def l_inv():
    A = [[R.randint(-3, 6) for _ in range(2)] for _ in range(2)]
    d = A[0][0]*A[1][1] - A[0][1]*A[1][0]
    inv = d != 0
    B.add('lin', f'¿La matriz {mat(A)} es invertible?', 'Sí' if inv else 'No', ['No' if inv else 'Sí', 'Solo si es simétrica', 'Solo si tiene unos en la diagonal'], R.randint(34, 52), f'Su determinante es {d}; es invertible solo si el determinante no es 0.', ['si' if inv else 'no', 'sí' if inv else 'no'])
def l_det3():
    A = [[R.randint(-3, 5) for _ in range(3)] for _ in range(3)]
    d = (A[0][0]*(A[1][1]*A[2][2]-A[1][2]*A[2][1]) - A[0][1]*(A[1][0]*A[2][2]-A[1][2]*A[2][0]) + A[0][2]*(A[1][0]*A[2][1]-A[1][1]*A[2][0]))
    B.add('lin', f'Calcula el determinante de {mat(A)}', d, pick_near(d, [d+A[0][0], -d]), R.randint(66, 84), 'Se desarrolla por cofactores de la primera fila.', [str(d)])
def l_cross():
    a = [R.randint(-3, 4) for _ in range(3)]; b = [R.randint(-3, 4) for _ in range(3)]
    c = [a[1]*b[2]-a[2]*b[1], a[2]*b[0]-a[0]*b[2], a[0]*b[1]-a[1]*b[0]]
    ans = f'({c[0]}, {c[1]}, {c[2]})'
    B.add('lin', f'Calcula el producto cruz ({a[0]}, {a[1]}, {a[2]}) × ({b[0]}, {b[1]}, {b[2]})', ans, [f'({-c[0]}, {-c[1]}, {-c[2]})', f'({c[1]}, {c[0]}, {c[2]})', f'({a[0]*b[0]}, {a[1]*b[1]}, {a[2]*b[2]})'], R.randint(68, 84), 'Se usa el determinante simbólico con i, j, k.', [ans, ans.replace(' ', '')])
def l_cramer():
    x, y = R.randint(-4, 6), R.randint(-4, 6); a, b, c, d = [R.randint(1, 5) for _ in range(4)]
    if a*d - b*c == 0: return
    e, f = a*x+b*y, c*x+d*y
    ans = f'x = {x}, y = {y}'
    B.add('lin', f'Resuelve el sistema: {cf(a)}x + {cf(b)}y = {e}  y  {cf(c)}x + {cf(d)}y = {f}', ans, [f'x = {y}, y = {x}', f'x = {x+1}, y = {y}', f'x = {x}, y = {y+1}'], R.randint(54, 72), 'Se puede resolver por reducción o por la regla de Cramer.', [ans, f'{x},{y}', f'x={x},y={y}'])
def l_eig():
    l1, l2 = R.randint(-4, 6), R.randint(-4, 6)
    if l1 == l2: return
    a, d = R.randint(-3, 6), 0
    t = l1 + l2; d = t - a
    # need b*c = a*d - l1*l2
    p = a*d - l1*l2
    if p == 0: b, c = 0, R.randint(-3, 3)
    else:
        divs = [k for k in range(1, abs(p)+1) if p % k == 0]
        b = R.choice(divs); c = p // b
    A = [[a, b], [c, d]]
    lo, hi = sorted([l1, l2])
    ans = f'{lo} y {hi}'
    B.add('lin', f'¿Cuáles son los valores propios de {mat(A)}?', ans, [f'{-lo} y {-hi}', f'{lo} y {hi+1}', f'{t} y {a*d-b*c}'], R.randint(74, 94), 'Suman la traza y multiplican el determinante.', [ans, f'{lo},{hi}', f'{lo} {hi}'])
def l_eigtri():
    a, d, b = R.randint(-3, 6), R.randint(-3, 6), R.randint(1, 5)
    if a == d: return
    lo, hi = sorted([a, d])
    ans = f'{lo} y {hi}'
    B.add('lin', f'¿Cuáles son los valores propios de {mat([[a, b], [0, d]])}?', ans, [f'{lo} y {hi+b}', f'{b} y {a}', f'{-lo} y {-hi}'], R.randint(62, 78), 'En una matriz triangular son los elementos de la diagonal.', [ans, f'{lo},{hi}', f'{lo} {hi}'])
def l_angle():
    a, b = R.randint(1, 5), R.randint(1, 5)
    B.add('lin', f'¿Son perpendiculares los vectores ({a}, {b}) y ({-b}, {a})?', 'Sí', ['No', 'Solo si miden lo mismo', 'Solo en 3D'], R.randint(40, 56), f'Su producto punto es {-a*b + a*b} = 0.', ['si', 'sí'])
def l_dep():
    a, b, k = R.randint(1, 5), R.randint(1, 5), R.randint(2, 4)
    B.add('lin', f'¿Son linealmente dependientes ({a}, {b}) y ({k*a}, {k*b})?', 'Sí', ['No', 'Solo si a = b', 'Depende de la base'], R.randint(46, 62), 'Uno es múltiplo escalar del otro.', ['si', 'sí'])
def l_scalmat():
    k = R.randint(2, 5); A = [[R.randint(-3, 6) for _ in range(2)] for _ in range(2)]
    S = [[k*x for x in r] for r in A]; ans = mat(S)
    B.add('lin', f'Calcula {k}·{mat(A)}', ans, [mat([[x+k for x in r] for r in A]), mat([[k*A[0][0], A[0][1]], [A[1][0], k*A[1][1]]]), mat([[-x for x in r] for r in S])], R.randint(14, 26), 'Se multiplica cada entrada por el escalar.', [ans, ans.replace(' ', '')])
def l_ident():
    n = R.choice([2, 3]); A = [[R.randint(1, 8) for _ in range(n)] for _ in range(n)]
    B.add('lin', f'¿Qué resulta de multiplicar la matriz {mat(A)} por la matriz identidad de su mismo tamaño?', 'La misma matriz', ['La matriz cero', 'Su transpuesta', 'Su inversa'], R.randint(30, 44), 'La identidad es el elemento neutro del producto.', ['la misma matriz'])
want(8, 'lin', l_vsum); want(7, 'lin', l_vsc); want(8, 'lin', l_dot); want(6, 'lin', l_norm)
want(7, 'lin', l_madd); want(6, 'lin', l_scalmat); want(6, 'lin', l_trace); want(8, 'lin', l_det2)
want(6, 'lin', l_transp); want(6, 'lin', l_ident); want(7, 'lin', l_inv); want(7, 'lin', l_mvec)
want(6, 'lin', l_angle); want(5, 'lin', l_dep); want(7, 'lin', l_mmul); want(6, 'lin', l_cramer)
want(5, 'lin', l_eigtri); want(5, 'lin', l_det3); want(5, 'lin', l_cross); want(5, 'lin', l_eig)
conc = [
 ('¿Qué es un vector?', 'Un objeto con magnitud y dirección', ['Un número sin signo', 'Una ecuación de segundo grado', 'Una gráfica circular'], 6, 'Se representa con una lista de componentes.'),
 ('¿Cómo se llama la matriz con unos en la diagonal y ceros fuera?', 'Matriz identidad', ['Matriz nula', 'Matriz transpuesta', 'Matriz escalar'], 20, 'Actúa como el 1 en la multiplicación de matrices.'),
 ('¿Qué indica un determinante igual a cero?', 'La matriz no es invertible', ['La matriz es identidad', 'La matriz es simétrica', 'La matriz es ortogonal'], 40, 'Sus filas son linealmente dependientes.'),
 ('¿El producto de matrices es conmutativo en general?', 'No', ['Sí, siempre', 'Solo si son cuadradas', 'Solo si son 2×2'], 38, 'En general AB ≠ BA.'),
 ('¿Qué es una matriz simétrica?', 'Una que es igual a su transpuesta', ['Una con determinante 1', 'Una con todas las entradas iguales', 'Una sin ceros'], 36, 'Aᵀ = A.'),
 ('¿Qué mide el rango de una matriz?', 'El número de filas o columnas linealmente independientes', ['La suma de sus entradas', 'Su tamaño', 'Su determinante'], 58, 'Es la dimensión del espacio generado por sus filas.'),
 ('Si Av = λv con v ≠ 0, λ se llama:', 'Valor propio', ['Determinante', 'Traza', 'Rango'], 66, 'Y v es el vector propio asociado.'),
 ('¿Qué forman los vectores que generan todo el plano y son independientes?', 'Una base', ['Un núcleo', 'Una traza', 'Una diagonal'], 56, 'Una base es un conjunto independiente que genera el espacio.'),
 ('¿Qué dimensión tiene el espacio ℝ³?', '3', ['2', '1', '9'], 34, 'Una base tiene 3 vectores.'),
 ('¿Qué da el producto punto de dos vectores perpendiculares?', '0', ['1', '−1', 'La longitud de uno'], 44, 'Es la condición de ortogonalidad.'),
]
for q, a, w, d, e in conc: B.add('lin', q, a, w, d, e, [a])

# ================= ESTADÍSTICA Y PROBABILIDAD =================
def e_mean():
    n = R.choice([3, 4, 5]); xs = [R.randint(1, 15) for _ in range(n)]
    s = sum(xs)
    if s % n: xs[-1] += n - (s % n); s = sum(xs)
    m = s // n
    B.add('est', f'¿Cuál es la media de {", ".join(map(str, xs))}?', m, pick_near(m, [max(xs), min(xs)]), R.randint(6, 18), f'{s} ÷ {n} = {m}.', [str(m)])
def e_median():
    n = R.choice([5, 7]); xs = R.sample(range(1, 30), n)
    med = sorted(xs)[n//2]
    B.add('est', f'¿Cuál es la mediana de {", ".join(map(str, xs))}?', med, pick_near(med, [xs[n//2], sum(xs)//n]), R.randint(12, 26), 'Se ordenan los datos y se toma el valor central.', [str(med)])
def e_median2():
    xs = sorted(R.sample(range(1, 30), 6)); R.shuffle(xs)
    s = sorted(xs); med = F(s[2]+s[3], 2)
    ans = fr(med)
    B.add('est', f'¿Cuál es la mediana de {", ".join(map(str, xs))}?', ans, near_fr(med, [s[2], s[3]]), R.randint(24, 38), 'Con cantidad par de datos, se promedian los dos centrales.', [ans, ans.replace('/', ',')] )
def e_mode():
    m = R.randint(1, 9); xs = [m, m, m] + R.sample([x for x in range(1, 12) if x != m], 4); R.shuffle(xs)
    B.add('est', f'¿Cuál es la moda de {", ".join(map(str, xs))}?', m, pick_near(m), R.randint(6, 16), 'La moda es el dato que más se repite.', [str(m)])
def e_range():
    xs = R.sample(range(1, 40), 6); r = max(xs) - min(xs)
    B.add('est', f'¿Cuál es el rango de {", ".join(map(str, xs))}?', r, pick_near(r, [max(xs), sum(xs)//6]), R.randint(8, 20), 'Rango = máximo − mínimo.', [str(r)])
def e_prob_dice():
    k = R.choice([0, 1, 2, 3])
    if k == 0: q, p = '¿Cuál es la probabilidad de sacar un 6 con un dado normal?', F(1, 6)
    elif k == 1: q, p = '¿Cuál es la probabilidad de sacar un número par con un dado normal?', F(1, 2)
    elif k == 2:
        n = R.randint(2, 5); q, p = f'¿Cuál es la probabilidad de sacar un número mayor que {n} con un dado normal?', F(6-n, 6)
    else:
        n = R.randint(2, 6); q, p = f'¿Cuál es la probabilidad de sacar un número menor o igual a {n} con un dado normal?', F(n, 6)
    B.add('est', q, fr(p), near_fr(p, [fr(1-p)], prob=True), R.randint(14, 30), 'Casos favorables entre casos posibles.', [fr(p)])
def e_prob_coin():
    n = R.randint(2, 4); p = F(1, 2**n)
    B.add('est', f'Al lanzar una moneda {n} veces, ¿cuál es la probabilidad de obtener {n} caras?', fr(p), near_fr(p, [fr(F(1, 2*n)), fr(F(1, 2**(n-1)))], prob=True), R.randint(24, 40), 'Eventos independientes: se multiplican las probabilidades.', [fr(p)])
def e_prob_urn():
    r, b = R.randint(2, 8), R.randint(2, 8)
    p = F(r, r+b)
    B.add('est', f'Una bolsa tiene {r} bolas rojas y {b} azules. ¿Cuál es la probabilidad de sacar una roja?', fr(p), near_fr(p, [fr(F(b, r+b)), fr(F(r, b))], prob=True), R.randint(14, 30), 'Rojas entre el total de bolas.', [fr(p)])
def e_cards():
    k = R.choice([('un corazón', F(13, 52)), ('un as', F(4, 52)), ('una figura (J, Q o K)', F(12, 52)), ('una carta roja', F(26, 52))])
    B.add('est', f'De una baraja de 52 cartas, ¿cuál es la probabilidad de sacar {k[0]}?', fr(k[1]), near_fr(k[1], [fr(1-k[1])], prob=True), R.randint(24, 40), 'Casos favorables entre 52.', [fr(k[1])])
def e_comb():
    n = R.randint(4, 9); k = R.randint(2, n-2)
    v = comb(n, k)
    B.add('est', f'¿Cuántas formas hay de elegir {k} elementos de {n} sin importar el orden? (C({n},{k}))', v, pick_near(v, [perm(n, k), n*k]), R.randint(38, 56), 'C(n,k) = n!/(k!(n − k)!).', [str(v)])
def e_perm():
    n = R.randint(4, 8); k = R.randint(2, 3)
    v = perm(n, k)
    B.add('est', f'¿De cuántas maneras se pueden ordenar {k} personas elegidas de {n}? (P({n},{k}))', v, pick_near(v, [comb(n, k), n**k]), R.randint(40, 58), 'P(n,k) = n!/(n − k)!.', [str(v)])
def e_fact():
    n = R.randint(3, 8)
    v = factorial(n)
    B.add('est', f'¿Cuánto es {n}! (factorial de {n})?', v, pick_near(v, [v//n, v+n]), R.randint(28, 44), f'{n}! = {" × ".join(str(i) for i in range(n, 0, -1))}.', [str(v)])
def e_ev():
    k = R.randint(2, 4); vals = R.sample(range(1, 7), k)
    p = F(1, k); ev = sum(F(v) for v in vals) * p
    prem = ', '.join(map(str, vals))
    B.add('est', f'Un juego da con igual probabilidad uno de estos premios: {prem}. ¿Cuál es el valor esperado?', fr(ev), near_fr(ev, [fr(F(sum(vals)))]), R.randint(52, 68), 'Valor esperado = suma de (valor × probabilidad).', [fr(ev)])
def e_var():
    base = R.randint(2, 8); d = R.choice([1, 2, 3])
    xs = [base-d, base, base+d]
    var = F(2*d*d, 3)
    ans = fr(var)
    B.add('est', f'¿Cuál es la varianza poblacional de {xs[0]}, {xs[1]}, {xs[2]}?', ans, near_fr(var, [fr(F(d*d)), fr(F(2*d*d, 2))]), R.randint(58, 74), 'Promedio de los cuadrados de las desviaciones respecto de la media.', [ans])
def e_std():
    m = R.randint(5, 12); s = R.choice([1, 2, 3, 4])
    xs = [m-s, m-s, m+s, m+s]
    B.add('est', f'¿Cuál es la desviación estándar poblacional de {", ".join(map(str, xs))}?', s, pick_near(s, [s*s, 2*s]), R.randint(58, 76), 'Es la raíz cuadrada de la varianza.', [str(s)])
def e_z():
    mu, sg, z = R.randint(50, 100), R.randint(2, 10), R.randint(-3, 3)
    x = mu + z*sg
    B.add('est', f'En una distribución con media {mu} y desviación estándar {sg}, ¿cuál es el puntaje z de {x}?', z, pick_near(z, [x-mu, sg]), R.randint(46, 62), 'z = (x − μ)/σ.', [str(z)])
def e_cond():
    r, b = R.randint(3, 7), R.randint(3, 7)
    p = F(r, r+b) * F(r-1, r+b-1)
    ans = fr(p)
    B.add('est', f'Una bolsa tiene {r} bolas rojas y {b} azules. Si se sacan 2 sin devolver, ¿cuál es la probabilidad de que ambas sean rojas?', ans, near_fr(p, [fr(F(r, r+b)**2)], prob=True), R.randint(62, 80), 'P(1ª roja) × P(2ª roja | 1ª roja).', [ans])
def e_binom():
    n = R.randint(3, 5); k = R.randint(1, n-1)
    p = F(comb(n, k), 2**n)
    ans = fr(p)
    B.add('est', f'Al lanzar una moneda {n} veces, ¿cuál es la probabilidad de obtener exactamente {k} cara(s)?', ans, near_fr(p, [fr(F(1, 2**n)), fr(F(k, n))], prob=True), R.randint(68, 86), 'C(n,k)/2ⁿ.', [ans])
def e_bayes():
    pa = R.choice([F(1, 100), F(1, 50), F(1, 20)]); sens = F(9, 10); fp = F(1, 10)
    pos = pa*sens + (1-pa)*fp
    p = pa*sens/pos
    ans = fr(p)
    B.add('est', f'Una enfermedad afecta a {fr(pa)} de la población. Una prueba detecta al 90% de los enfermos y da falso positivo al 10% de los sanos. Si alguien da positivo, ¿cuál es la probabilidad de que esté enfermo?', ans, near_fr(p, [fr(sens), fr(pa)], prob=True), R.randint(88, 100), 'Teorema de Bayes.', [ans])
def e_normal():
    k = R.choice([(1, '68%'), (2, '95%'), (3, '99,7%')])
    B.add('est', f'En una distribución normal, ¿qué porcentaje aproximado de los datos queda a menos de {k[0]} desviación(es) estándar de la media?', k[1], [x for x in ['68%', '95%', '99,7%', '50%', '75%'] if x != k[1]][:3], R.randint(40, 56), 'Regla empírica 68–95–99,7.', [k[1], k[1].replace(',', '.')])
def e_pct_freq():
    n = R.choice([20, 25, 40, 50, 80, 100]); f = R.randint(1, n//2)
    r = F(f*100, n)
    ans = f'{fr(r)}%' if r.denominator == 1 else f'{float(r):.1f}%'.replace('.', ',')
    wr = [f'{fr(F(f, n))}', f'{f}%', f'{n-f}%']
    B.add('est', f'En una encuesta de {n} personas, {f} respondieron «sí». ¿Qué porcentaje es?', ans, wr, R.randint(18, 32), f'{f}/{n} × 100.', [ans, ans.replace('%', '')])
want(6, 'est', e_mean); want(6, 'est', e_median); want(6, 'est', e_mode); want(6, 'est', e_range)
want(7, 'est', e_prob_dice); want(5, 'est', e_prob_urn); want(5, 'est', e_pct_freq); want(5, 'est', e_prob_coin)
want(5, 'est', e_median2); want(5, 'est', e_cards); want(6, 'est', e_fact); want(6, 'est', e_comb)
want(5, 'est', e_perm); want(5, 'est', e_normal); want(5, 'est', e_z); want(5, 'est', e_ev)
want(5, 'est', e_var); want(5, 'est', e_std); want(5, 'est', e_cond); want(5, 'est', e_binom); want(4, 'est', e_bayes)
conc = [
 ('¿Qué mide la media aritmética?', 'El promedio de los datos', ['El dato más repetido', 'El dato central', 'La diferencia entre máximo y mínimo'], 8, 'Suma de datos entre cantidad de datos.'),
 ('¿Qué es una variable cualitativa?', 'La que describe cualidades, como el color', ['La que toma valores numéricos medibles', 'La que siempre es entera', 'La que tiene media cero'], 24, 'Ejemplos: color, sexo, país.'),
 ('¿Qué es una variable cuantitativa discreta?', 'La que toma valores contables, como el número de hijos', ['La que mide estaturas', 'La que describe colores', 'La que no tiene unidad'], 30, 'Solo toma valores aislados.'),
 ('¿Qué representa una probabilidad de 1?', 'Un evento seguro', ['Un evento imposible', 'Un evento que ocurre a la mitad de las veces', 'Un evento raro'], 20, 'Las probabilidades van de 0 a 1.'),
 ('¿Qué es el error tipo I?', 'Rechazar H₀ siendo verdadera', ['No rechazar H₀ siendo falsa', 'Calcular mal la media', 'Usar una muestra pequeña'], 70, 'Es un falso positivo.'),
 ('Un p-valor pequeño (menor que α) indica:', 'Evidencia contra la hipótesis nula', ['Que la hipótesis nula es cierta', 'Que la muestra es pequeña', 'Que no hay variabilidad'], 76, 'Se rechaza H₀ al nivel α.'),
 ('¿Qué mide la desviación estándar?', 'La dispersión de los datos respecto a la media', ['El valor central', 'El dato más frecuente', 'El total de datos'], 46, 'Mientras mayor es, más dispersos están los datos.'),
 ('¿Qué dice la ley de los grandes números?', 'El promedio muestral se acerca al valor esperado al aumentar la muestra', ['Todos los datos son iguales', 'La media siempre vale cero', 'La varianza es siempre 1'], 66, 'Con más datos, el promedio se estabiliza.'),
 ('¿Qué es una muestra aleatoria?', 'Un subconjunto elegido al azar de la población', ['Toda la población', 'Los datos más grandes', 'Un dato repetido'], 28, 'Cada individuo tiene la misma oportunidad de ser elegido.'),
 ('Si dos eventos son independientes, P(A y B) es:', 'P(A) × P(B)', ['P(A) + P(B)', 'P(A) − P(B)', 'P(A)/P(B)'], 52, 'La ocurrencia de uno no afecta al otro.'),
]
for q, a, w, d, e in conc: B.add('est', q, a, w, d, e, [a])

B.finish(os.path.join(HERE, 'out_mat.json'))
