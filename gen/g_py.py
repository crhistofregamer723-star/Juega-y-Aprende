from common import *
R = random.Random(101)
ri = R.randint
def P(src, d, **k): return code('py', 'py', src, d, **k)
W = ['Hola', 'Python', 'mundo', 'casa', 'sol', 'luna', 'perro', 'gato', 'código', 'clase', 'dato', 'nube', 'río', 'mar', 'pan', 'café', 'árbol', 'libro']
WORDS = ['python', 'banana', 'ordenador', 'teclado', 'programa', 'variable', 'bucle', 'lista', 'cadena', 'funcion', 'sistema', 'datos']

def fa():
    w = R.choice(W); k = R.randint(0, 3)
    if k == 0: return P('print("%s")' % w, ri(0, 2), alts=[w.upper(), '"%s"' % w, w[::-1]], why='print muestra el texto sin las comillas.')
    if k == 1: return P('print("%s" * 2)' % w, ri(2, 5), alts=[w + ' ' + w, '"%s"' % (w * 2), w], why='Multiplicar un texto por un entero lo repite.')
    if k == 2: return P('print("%s", "%s")' % (w, W[(W.index(w) + 3) % len(W)]), ri(2, 5), alts=[w + W[(W.index(w) + 3) % len(W)], w, W[(W.index(w) + 3) % len(W)]], why='print separa los argumentos con un espacio.')
    return P('print(len("%s"))' % w, ri(2, 6), why='len cuenta los caracteres.')
fam(14, fa)

def fa2():
    a, b = ri(1, 9), ri(1, 9); k = R.randint(0, 3)
    if k == 0: return P('print(%d + %d)' % (a, b), ri(0, 3), alts=['%d%d' % (a, b), str(a * b)], why='Con números, + suma.')
    if k == 1: return P('print("%d" + "%d")' % (a, b), ri(4, 9), alts=[str(a + b), '%d %d' % (a, b), str(a * b)], why='Con textos, + concatena.')
    if k == 2: return P('print(%d * %d)' % (a, b), ri(1, 4), alts=[str(a + b), '%d%d' % (a, b)], why='* multiplica.')
    return P('print(%d - %d)' % (a, b), ri(1, 4), alts=[str(b - a) if b != a else '1', str(a + b)], why='- resta.')
fam(14, fa2)

def fb():
    op = R.choice(['+', '-', '*', '//', '%', '**'])
    if op == '**': a, b = ri(2, 9), ri(2, 4)
    elif op in ('//', '%'): b = ri(2, 9); a = ri(b + 1, 70)
    else: a, b = ri(2, 40), ri(2, 12)
    d = {'+': 3, '-': 4, '*': 6, '//': 14, '%': 16, '**': 20}[op] + (3 if max(a, b) > 20 else 0) + ri(0, 3)
    alts = {'+': [a - b, a * b], '-': [b - a, a + b], '*': [a + b, a * b + a], '//': [round(a / b, 1), a % b, a // b + 1],
            '%': [a // b, a % b + 1, round(a / b, 1)], '**': [a * b, a + b, b ** a]}[op]
    why = {'//': 'La división entera // descarta la parte decimal.', '%': '% devuelve el residuo de la división.', '**': '** es la potencia.'}.get(op, '')
    return P('print(%d %s %d)' % (a, op, b), d, alts=[str(x) for x in alts], why=why)
fam(40, fb)

def fc():
    a, b, c = ri(2, 9), ri(2, 9), ri(2, 9); k = R.randint(0, 4)
    srcs = [('%d + %d * %d' % (a, b, c), a + b * c, [(a + b) * c], 'La multiplicación se evalúa antes que la suma.'),
            ('(%d + %d) * %d' % (a, b, c), (a + b) * c, [a + b * c], 'Los paréntesis se evalúan primero.'),
            ('%d - %d - %d' % (a + b + c, b, c), a, [a + b + c - (b - c)], 'La resta se evalúa de izquierda a derecha.'),
            ('%d ** 2 + %d' % (a, b), a * a + b, [(a + b) ** 2, a * 2 + b], 'Primero la potencia y luego la suma.'),
            ('%d + %d %% %d' % (a, b + c, c), a + (b + c) % c, [(a + b + c) % c], 'El % tiene prioridad sobre la suma.')]
    e, v, al, why = srcs[k]
    return P('print(%s)' % e, 12 + k * 3 + ri(0, 4), alts=[str(x) for x in al], why=why)
fam(18, fc)

def fd():
    b = ri(2, 8); k = ri(1, 9); a = b * k + R.choice([0, 0, b // 2 if b % 2 == 0 else 0, 1])
    if a == 0: return False
    return P('print(%d / %d)' % (a, b), ri(10, 22), alts=[str(a // b), str(a % b)], why='La división / siempre devuelve un número decimal (float).')
fam(10, fd)

def fe():
    a, b = ri(2, 20), ri(2, 9); k = R.randint(0, 4)
    if k == 0: return P('x = %d\ny = %d\nx = x + y\nprint(x)' % (a, b), ri(5, 12), alts=[str(b), str(a), str(a * b)], why='x se actualiza con la suma x + y.')
    if k == 1: return P('x = %d\nx += %d\nx *= 2\nprint(x)' % (a, b), ri(8, 16), alts=[str(a + b), str(a + b * 2), str(a * 2 + b)], why='Primero x += %d y luego x *= 2.' % b)
    if k == 2: return P('a = %d\nb = %d\na, b = b, a\nprint(a, b)' % (a, b), ri(14, 24), alts=['%d %d' % (a, b), '%d %d' % (a, a), '%d %d' % (b, b)], why='La asignación múltiple intercambia los valores.')
    if k == 3: return P('x = %d\ny = x\nx = %d\nprint(y)' % (a, b), ri(14, 24), alts=[str(b), '%d %d' % (a, b), str(a + b)], why='y guardó una copia del valor antiguo de x.')
    return P('n = %d\nn -= %d\nprint(n * 2)' % (a + 10, b), ri(6, 14), alts=[str(a + 10 - b), str((a + 10) * 2), str((a + 10 + b) * 2)], why='Primero se resta y después se multiplica.')
fam(18, fe)

def ff():
    w = R.choice(WORDS); n = len(w); k = R.randint(0, 13)
    i = ri(1, n - 3); j = ri(i + 1, n - 1)
    forms = [
        ('print(len("%s"))' % w, str(n), 3, [str(n - 1), str(n + 1)], 'len cuenta todos los caracteres.'),
        ('print("%s".upper())' % w, w.upper(), 4, [w.capitalize(), w], 'upper() convierte a mayúsculas.'),
        ('print("%s"[0])' % w, w[0], 5, [w[1], w[-1]], 'El primer índice es 0.'),
        ('print("%s"[-1])' % w, w[-1], 10, [w[-2], w[0]], 'El índice -1 es el último carácter.'),
        ('print("%s"[%d:%d])' % (w, i, j), w[i:j], 18, [w[i:j + 1], w[i - 1:j], w[i + 1:j]], 'El corte [a:b] incluye a y excluye b.'),
        ('print("%s"[::-1])' % w, w[::-1], 22, [w.upper(), w[1:]], 'El paso -1 recorre al revés.'),
        ('print("%s".count("%s"))' % (w, w[1]), str(w.count(w[1])), 14, [str(w.count(w[1]) + 1), '1'], 'count cuenta las apariciones.'),
        ('print("%s".find("%s"))' % (w, w[i]), str(w.find(w[i])), 17, [str(w.find(w[i]) + 1), '-1'], 'find devuelve el primer índice donde aparece.'),
        ('print("%s".replace("%s", "-"))' % (w, w[1]), w.replace(w[1], '-'), 20, [w.replace(w[1], '-', 1), w.replace(w[1], '')], 'replace cambia todas las apariciones.'),
        ('print("%s".title())' % w, w.title(), 9, [w.upper(), w], 'title() pone en mayúscula la primera letra.'),
        ('print("%s" + "%s")' % (w[:3], w[3:]), w, 8, [w[:3] + ' ' + w[3:], w[3:] + w[:3]], '+ concatena textos.'),
        ('print("-".join("%s"))' % w[:4], '-'.join(w[:4]), 26, [w[:4], ' '.join(w[:4])], 'join une los elementos con el separador.'),
        ('print("%s"[::2])' % w, w[::2], 28, [w[1::2], w[::-2]], 'El paso 2 toma un carácter sí y otro no.'),
        ('print("%s"[-3:])' % w, w[-3:], 24, [w[:3], w[-4:]], '[-3:] toma los tres últimos caracteres.'),
    ]
    s, a, d, al, why = forms[k]
    return P(s, d + ri(0, 3), alts=al, why=why)
fam(48, ff)

def fg():
    L = [ri(1, 20) for _ in range(ri(3, 5))]; n = len(L); k = R.randint(0, 11); i = ri(0, n - 1)
    ls = str(L); l2 = sorted(L)
    forms = [
        ('print(len(%s))' % ls, str(n), 5, [str(n + 1), str(n - 1)], 'len cuenta los elementos.'),
        ('lst = %s\nprint(lst[%d])' % (ls, i), str(L[i]), 6, [str(L[(i + 1) % n]), str(i)], 'Los índices empiezan en 0.'),
        ('lst = %s\nprint(lst[-1])' % ls, str(L[-1]), 9, [str(L[0]), str(L[-2])], 'El índice -1 es el último elemento.'),
        ('lst = %s\nlst.append(%d)\nprint(lst)' % (ls, 99), str(L + [99]), 8, [str([99] + L), str(L)], 'append agrega al final.'),
        ('print(sum(%s))' % ls, str(sum(L)), 7, [str(sum(L) + 1), str(max(L))], 'sum suma los elementos.'),
        ('print(max(%s) - min(%s))' % (ls, ls), str(max(L) - min(L)), 14, [str(max(L)), str(min(L))], 'Se resta el menor del mayor.'),
        ('print(sorted(%s))' % ls, str(l2), 12, [str(L[::-1]), str(sorted(L, reverse=True))], 'sorted devuelve una lista ordenada ascendente.'),
        ('lst = %s\nprint(lst.pop())' % ls, str(L[-1]), 14, [str(L[0]), str(L[:-1])], 'pop() quita y devuelve el último elemento.'),
        ('lst = %s\nprint(lst.index(%d))' % (ls, L[i]), str(L.index(L[i])), 15, [str(L.index(L[i]) + 1), str(L[i])], 'index devuelve la posición del primer elemento igual.'),
        ('print(%s * 2)' % ls, str(L * 2), 18, [str([x * 2 for x in L]), str(L + [2])], 'Multiplicar una lista la repite.'),
        ('print(%d in %s)' % (L[i] + R.choice([0, 1]), ls), str((L[i] + 0) in L), 11, [], 'in comprueba si el valor está en la lista.'),
        ('lst = %s\nlst.insert(0, 0)\nprint(len(lst))' % ls, str(n + 1), 16, [str(n), str(n + 2)], 'insert agrega un elemento, así que la longitud crece en 1.'),
    ]
    s, a, d, al, why = forms[k]
    if k == 10:
        v = L[i] + R.choice([0, 1]); a2 = str(v in L)
        return P('print(%d in %s)' % (v, ls), d + ri(0, 3), alts=['True' if a2 == 'False' else 'False', 'None', '-1'], why=why)
    return P(s, d + ri(0, 4), alts=al, why=why)
fam(40, fg)

def fh():
    ks = R.sample(['a', 'b', 'c', 'x', 'y', 'z', 'uno', 'dos'], 3); v = [ri(1, 9) for _ in ks]
    ds = '{' + ', '.join('"%s": %d' % (k, x) for k, x in zip(ks, v)) + '}'
    k = R.randint(0, 6)
    forms = [
        ('d = %s\nprint(d["%s"])' % (ds, ks[1]), str(v[1]), 18, [str(v[0]), ks[1]], 'Se accede al valor por su clave.'),
        ('d = %s\nprint(len(d))' % ds, '3', 20, ['2', str(sum(v))], 'len cuenta los pares clave-valor.'),
        ('d = %s\nprint(d.get("q", 0))' % ds, '0', 26, ['None', 'KeyError'], 'get devuelve el valor por defecto si la clave no existe.'),
        ('d = %s\nprint("%s" in d)' % (ds, ks[2]), 'True', 24, ['False', str(v[2])], 'in en un diccionario revisa las claves.'),
        ('d = %s\nprint(sum(d.values()))' % ds, str(sum(v)), 28, [str(sum(v) + 1), '3'], 'values() son los valores; sum los suma.'),
        ('d = %s\nd["%s"] = 100\nprint(d["%s"])' % (ds, ks[0], ks[0]), '100', 26, [str(v[0]), 'None'], 'Asignar a una clave existente reemplaza su valor.'),
        ('d = %s\nprint(list(d.keys()))' % ds, str(ks), 30, [str(v), str(list(zip(ks, v)))], 'keys() devuelve las claves en orden de inserción.'),
    ]
    s, a, d, al, why = forms[k]
    return P(s, d + ri(0, 5), alts=al, why=why)
fam(16, fh)

def fi():
    x, m = ri(1, 20), ri(1, 20); k = R.randint(0, 3)
    if k == 0: return P('x = %d\nif x > %d:\n    print("grande")\nelse:\n    print("pequeño")' % (x, m), ri(10, 20), alts=['pequeño' if x > m else 'grande', 'grande pequeño', 'x'], why='Se evalúa x > %d con x = %d.' % (m, x))
    if k == 1: return P('n = %d\nprint("par" if n %% 2 == 0 else "impar")' % x, ri(14, 24), alts=['impar' if x % 2 == 0 else 'par', 'True', 'cero'], why='n %% 2 == 0 indica un número par.')
    if k == 2: return P('x = %d\nif x < %d:\n    print("A")\nelif x < %d:\n    print("B")\nelse:\n    print("C")' % (x, m, m + 6), ri(22, 34), alts=[c for c in 'ABC'], why='Se ejecuta el primer bloque cuya condición sea verdadera.')
    return P('a, b = %d, %d\nif a > 0 and b > 0:\n    print("ambos")\nelse:\n    print("alguno no")' % (x - 10, m), ri(24, 36), alts=['ambos' if x <= 10 else 'alguno no', 'True', 'False'], why='and exige que las dos condiciones sean verdaderas.')
fam(14, fi)

TYPES = [('3', 'int'), ('3.0', 'float'), ('"3"', 'str'), ('True', 'bool'), ('[3]', 'list'), ('(3,)', 'tuple'), ('{3}', 'set'), ('{"a": 3}', 'dict'), ('None', 'NoneType'), ('2 + 3j', 'complex'), ('7 / 2', 'float'), ('7 // 2', 'int'), ('"a" * 3', 'str'), ('3 > 2', 'bool'), ('range(3)', 'range'), ('len("ab")', 'int')]
def fj():
    e, t = R.choice(TYPES); pool = [x[1] for x in TYPES if x[1] != t]
    return P('print(type(%s))' % e, 14 + (4 if t in ('NoneType', 'complex', 'range') else 0) + ri(0, 6), alts=["<class '%s'>" % x for x in set(pool)], acc=[t, "<class '%s'>" % t], why='type() devuelve la clase del valor.')
    # (el resultado real <class 'x'> lo calcula Python)
fam(16, fj)

def fk():
    n = R.choice(['Ana', 'Luis', 'Eva', 'Marta', 'Pablo']); a, b = ri(2, 9), ri(2, 9); x = round(ri(100, 999) / 100 * ri(1, 9), 3); k = R.randint(0, 5)
    forms = [
        ('nombre = "%s"\nprint(f"Hola {nombre}")' % n, 'Hola ' + n, 12, ['Hola {nombre}', 'Hola nombre', n], 'La f-string reemplaza {nombre} por su valor.'),
        ('print(f"{%d}+{%d}={%d + %d}")' % (a, b, a, b), '%d+%d=%d' % (a, b, a + b), 18, ['%d+%d=%d' % (a, b, a * b), '%d + %d = %d' % (a, b, a + b)], 'Dentro de {} se calculan expresiones.'),
        ('print("{} y {}".format(%d, %d))' % (a, b), '%d y %d' % (a, b), 16, ['%d y %d' % (b, a), '{} y {}'], 'format rellena las llaves en orden.'),
        ('print(round(%s, 1))' % x, str(round(x, 1)), 20, [str(round(x, 2)), str(int(x))], 'round(x, 1) deja un decimal.'),
        ('print(f"{%s:.2f}")' % x, '%.2f' % x, 26, ['%.1f' % x, str(x)], '.2f muestra dos decimales.'),
        ('print(int("%d") + %d)' % (a, b), str(a + b), 16, ['%d%d' % (a, b), 'TypeError'], 'int convierte el texto a número antes de sumar.'),
    ]
    s, a2, d, al, why = forms[k]
    return P(s, d + ri(0, 5), alts=al, why=why)
fam(16, fk)

def fl():
    n, m = ri(3, 7), ri(2, 4); L = [ri(1, 15) for _ in range(6)]; k = R.randint(0, 5)
    forms = [
        ('print([x * %d for x in range(%d)])' % (m, n), [x * m for x in range(n)], 34, 'La comprensión aplica x * %d a cada elemento.' % m),
        ('print([x for x in %s if x %% 2 == 0])' % L, [x for x in L if x % 2 == 0], 38, 'Se conservan solo los pares.'),
        ('print(sum(x * x for x in range(%d)))' % n, sum(x * x for x in range(n)), 42, 'Suma los cuadrados de 0 a %d.' % (n - 1)),
        ('print([c.upper() for c in "%s"])' % 'abc'[:m], [c.upper() for c in 'abc'[:m]], 36, 'Cada carácter se pasa a mayúscula.'),
        ('print([x + y for x, y in zip(%s, %s)])' % (L[:3], L[3:]), [x + y for x, y in zip(L[:3], L[3:])], 52, 'zip empareja elementos por posición.'),
        ('print(len([x for x in range(%d) if x %% %d == 0]))' % (n * 4, m), len([x for x in range(n * 4) if x % m == 0]), 48, 'Cuenta los múltiplos de %d menores que %d.' % (m, n * 4)),
    ]
    s, v, d, why = forms[k]
    return P(s, d + ri(0, 8), why=why)
fam(18, fl)

def fm():
    L = [ri(1, 9) for _ in range(4)]; m = ri(2, 5); ws = R.sample(WORDS, 3); k = R.randint(0, 3)
    forms = [
        ('print(list(map(lambda x: x * %d, %s)))' % (m, L), 52, 'map aplica la función a cada elemento.'),
        ('print(list(filter(lambda x: x > %d, %s)))' % (m, L), 54, 'filter conserva los que cumplen la condición.'),
        ('print(sorted(%s, key=len))' % ws, 58, 'key=len ordena por longitud (estable ante empates).'),
        ('f = lambda a, b: a * b + %d\nprint(f(%d, %d))' % (m, L[0], L[1]), 46, 'La lambda calcula a * b + %d.' % m),
    ]
    s, d, why = forms[k]
    return P(s, d + ri(0, 10), why=why)
fam(14, fm)

def fn():
    L = [ri(1, 6) for _ in range(6)]; A = set(ri(1, 8) for _ in range(5)); B = set(ri(1, 8) for _ in range(5)); k = R.randint(0, 3)
    forms = [
        ('print(len(set(%s)))' % L, 32, 'set elimina los repetidos.'),
        ('print(sorted({%s} & {%s}))' % (', '.join(map(str, sorted(A))), ', '.join(map(str, sorted(B)))), 44, '& es la intersección de conjuntos.'),
        ('print(sorted({%s} | {%s}))' % (', '.join(map(str, sorted(A))), ', '.join(map(str, sorted(B)))), 44, '| es la unión de conjuntos.'),
        ('t = %s\nprint(t[1] + t[-1])' % str(tuple(L[:4])), 30, 'Las tuplas se indexan igual que las listas.'),
    ]
    s, d, why = forms[k]
    return P(s, d + ri(0, 8), why=why)
fam(12, fn)

def fo():
    exprs = ['bool([])', 'bool("0")', 'bool(0)', 'bool(" ")', 'bool(None)', 'not 0', '"a" and "b"', '0 or 5', '[] or "x"', '5 and 0', 'None == False', 'bool("")', '1 == 1.0', '"a" or "b"', 'bool([0])', 'not None', 'None is None', '3 > 2 > 1', '0 == False', 'bool(0.0)']
    e = R.choice(exprs)
    return P('print(%s)' % e, 36 + ri(0, 22), alts=['True', 'False', 'None', '0', '5', 'a', 'b'], why='En Python los valores vacíos o cero son falsos y los demás verdaderos.')
fam(18, fo)

def fp():
    k = R.randint(0, 6); n = ri(1, 5); m = ri(6, 9)
    forms = [
        ('a = [1, 2]\nb = a\nb.append(%d)\nprint(a)' % n, 56, 'b y a son el mismo objeto, así que la lista cambia en ambas.'),
        ('a = [1, 2]\nb = a.copy()\nb.append(%d)\nprint(a)' % n, 52, 'copy crea una lista nueva: a no cambia.'),
        ('a = [1, 2]\nb = a\nb = b + [%d]\nprint(a)' % n, 66, 'b + [x] crea una lista nueva; a sigue igual.'),
        ('a = [1, 2, 3]\nb = a\nprint(a is b, a == [1, 2, 3])', 62, 'is compara identidad y == compara valores.'),
        ('a = "hola"\nb = a.upper()\nprint(a)', 40, 'Las cadenas son inmutables; upper devuelve una nueva.'),
        ('x = [0] * %d\nx[0] = %d\nprint(x)' % (n + 2, m), 44, 'Solo se cambia el primer elemento.'),
        ('m = [[0] * 2] * 2\nm[0][0] = %d\nprint(m)' % m, 88, 'Las dos filas son el mismo objeto, por eso cambian juntas.'),
    ]
    s, d, why = forms[k]
    return P(s, d + ri(0, 6), why=why)
fam(14, fp)

def fq():
    forms = [
        ('print(%d / 0)', 'ZeroDivisionError', 26, 'No se puede dividir entre cero.', lambda: ri(1, 9)),
        ('lst = [1, 2, 3]\nprint(lst[%d])', 'IndexError', 30, 'El índice está fuera del rango de la lista.', lambda: ri(3, 9)),
        ('d = {"a": 1}\nprint(d["%s"])', 'KeyError', 34, 'La clave no existe en el diccionario.', lambda: R.choice('bcxyz')),
        ('print("a" + %d)', 'TypeError', 32, 'No se puede sumar texto con número.', lambda: ri(1, 9)),
        ('print(int("%s"))', 'ValueError', 36, 'El texto no representa un entero.', lambda: R.choice(['abc', 'hola', '3.5x', 'uno'])),
        ('print(%s)', 'NameError', 28, 'La variable no está definida.', lambda: R.choice(['total', 'valor', 'resultado', 'edad'])),
        ('s = "hola"\nprint(s.%s())', 'AttributeError', 46, 'Las cadenas no tienen ese método.', lambda: R.choice(['push', 'append', 'size', 'length'])),
        ('t = (1, 2, 3)\nt[0] = %d', 'TypeError', 44, 'Las tuplas son inmutables.', lambda: ri(5, 9)),
    ]
    s, e, d, why, g = R.choice(forms)
    return P(s % g(), d + ri(0, 8), mode='err', why=why)
fam(16, fq)

def fr():
    k = R.randint(0, 3); n = ri(2, 9)
    forms = [
        ('try:\n    print(%d / 0)\nexcept ZeroDivisionError:\n    print("error")' % n, 52, 'La excepción se captura y se imprime "error".'),
        ('try:\n    int("x")\nexcept ValueError:\n    print("v")\nfinally:\n    print("f")', 60, 'finally siempre se ejecuta.'),
        ('try:\n    print([1, 2][%d])\nexcept IndexError:\n    print("fuera")' % (n % 2 + 2), 54, 'Acceder fuera del rango lanza IndexError.'),
        ('try:\n    x = %d\nexcept:\n    print("no")\nelse:\n    print("sí")' % n, 70, 'else se ejecuta si no hubo excepción.'),
    ]
    s, d, why = forms[k]
    return P(s, d + ri(0, 8), why=why)
fam(10, fr)

def fs():
    n = ri(3, 8); a = ri(0, 3); k = R.randint(0, 5)
    forms = [
        ('print(list(range(%d, %d)))' % (a, a + n), 28, 'range excluye el límite superior.'),
        ('print(list(range(%d, %d, %d)))' % (a, a + n * 2, 2), 34, 'El tercer argumento es el paso.'),
        ('print(list(range(%d, %d, -1)))' % (n, a), 40, 'Con paso negativo cuenta hacia atrás.'),
        ('print(list(zip([1, 2, 3], "ab")))', 50, 'zip se detiene en la secuencia más corta.'),
        ('print(list(enumerate("ab", %d)))' % ri(1, 4), 52, 'enumerate numera los elementos desde el inicio dado.'),
        ('print(dict(zip("ab", [%d, %d])))' % (n, a), 56, 'zip + dict arma un diccionario.'),
    ]
    s, d, why = forms[k]
    return P(s, d + ri(0, 6), why=why)
fam(14, fs)

TRICKS = ['0.1 + 0.2 == 0.3', 'round(2.5)', 'round(3.5)', '7 // -2', '-7 % 3', 'int(-2.7)', '"10" < "9"', '[1, 2] < [1, 3]', '2 ** 3 ** 2', 'True + True', '"ab" < "b"', 'abs(-3) ** 2', 'divmod(17, 5)', '10 // 3 * 3 + 10 % 3', 'max("a", "B")', 'bool("False")', '5 // 2 * 2.0', '1_000 + 1', '3 * "ab" + "c"', 'len([[]])', 'sum([[1], [2]], [])', '"%d%%" % 50', 'min(3, 3.0)', 'int("7") + int(7.9)', '0.5 + 0.5 == 1', '4 > 3 == True', 'not 1 + 1', '"5" * 2 == "55"', 'sorted("hello")[0]', 'any([0, "", 3])', 'all([])', 'any([])', '2 ** -1', '9 // 2 ** 2', "'a' in 'banana'", '[1, 2, 3][::-1][0]', 'list("abc") == ["a", "b", "c"]', 'type(1 / 1) == float']
def ft():
    e = R.choice(TRICKS)
    return P('print(%s)' % e, 48 + ri(0, 40), why='Es una expresión con reglas propias de Python: conviene memorizar el caso.')
fam(40, ft)

# ---- tabla: funciones y métodos (nombre -> qué hace) ----
BUILT = [
 ('print()', 'Muestra valores en pantalla', 1), ('input()', 'Lee texto escrito por el usuario', 3), ('len()', 'Devuelve la cantidad de elementos', 3),
 ('int()', 'Convierte un valor a entero', 4), ('float()', 'Convierte un valor a número decimal', 5), ('str()', 'Convierte un valor a texto', 5),
 ('type()', 'Indica la clase de un valor', 8), ('range()', 'Genera una secuencia de números', 9), ('sum()', 'Suma los elementos de un iterable', 9),
 ('max()', 'Devuelve el mayor valor', 9), ('min()', 'Devuelve el menor valor', 9), ('abs()', 'Devuelve el valor absoluto', 8),
 ('round()', 'Redondea un número', 12), ('sorted()', 'Devuelve una lista ordenada sin modificar la original', 18), ('list.append()', 'Agrega un elemento al final de la lista', 8),
 ('list.pop()', 'Quita y devuelve un elemento de la lista', 14), ('list.sort()', 'Ordena la lista en el mismo lugar', 18), ('list.reverse()', 'Invierte la lista en el mismo lugar', 18),
 ('list.insert()', 'Inserta un elemento en una posición dada', 16), ('list.remove()', 'Elimina la primera aparición de un valor', 20), ('list.extend()', 'Añade todos los elementos de otro iterable', 24),
 ('str.split()', 'Divide un texto en una lista de partes', 18), ('str.join()', 'Une elementos de una lista en un solo texto', 24), ('str.strip()', 'Quita espacios al inicio y al final', 16),
 ('str.lower()', 'Convierte el texto a minúsculas', 8), ('str.startswith()', 'Indica si el texto comienza con un prefijo', 22), ('str.isdigit()', 'Indica si el texto solo tiene dígitos', 22),
 ('dict.keys()', 'Devuelve las claves del diccionario', 22), ('dict.items()', 'Devuelve los pares clave-valor', 26), ('dict.get()', 'Busca una clave con un valor por defecto opcional', 26),
 ('enumerate()', 'Entrega pares (índice, elemento)', 34), ('zip()', 'Empareja elementos de varios iterables', 36), ('map()', 'Aplica una función a cada elemento', 44),
 ('filter()', 'Conserva los elementos que cumplen una condición', 44), ('isinstance()', 'Comprueba si un objeto es de cierta clase', 40), ('any()', 'Indica si algún elemento es verdadero', 42),
 ('all()', 'Indica si todos los elementos son verdaderos', 42), ('set()', 'Crea una colección sin elementos repetidos', 26), ('reversed()', 'Devuelve un iterador que recorre al revés', 36),
 ('open()', 'Abre un archivo para leerlo o escribirlo', 40), ('chr()', 'Devuelve el carácter de un código Unicode', 46), ('ord()', 'Devuelve el código Unicode de un carácter', 46),
 ('divmod()', 'Devuelve cociente y residuo juntos', 50), ('pow()', 'Eleva un número a una potencia', 28), ('dir()', 'Lista los atributos de un objeto', 60),
]
def fz():
    return False
for i, (n, dsc, d) in enumerate(BUILT):
    others = [b for j, b in enumerate(BUILT) if j != i]
    r2 = random.Random(i)
    w = [x[1] for x in r2.sample(others, 3)]
    row('py', '¿Qué hace %s en Python?' % n, dsc, w, d, '%s: %s.' % (n, dsc.lower()))
    w2 = [x[0] for x in r2.sample(others, 3)]
    row('py', 'En Python, ¿qué función o método %s?' % (dsc[0].lower() + dsc[1:]), n, w2, d + 6, 'Es %s.' % n)

C('py', r'''
0§En Python, ¿qué símbolo inicia un comentario de una línea?§#§//§--§/*
0§¿Cuál es la extensión habitual de un archivo Python?§.py§.pt§.python§.pyt§Los scripts de Python usan .py.
1§¿Qué función muestra texto en pantalla?§print()§echo()§show()§write()
2§¿Cuál es un nombre de variable válido en Python?§mi_edad§2edad§mi-edad§mi edad§Los nombres no pueden empezar con número, llevar guiones ni espacios.
3§¿Qué tipo de dato es "123" (entre comillas)?§str§int§float§list§Lo que va entre comillas es texto.
4§¿Qué operador compara si dos valores son iguales?§==§=§=>§!=§= asigna; == compara.
5§¿Cómo se delimita un bloque de código en Python?§Con sangría (indentación)§Con llaves { }§Con punto y coma§Con paréntesis§Python usa la sangría para agrupar instrucciones.
6§¿Cuál es el resultado de 10 // 3?§3§3.33§4§1§// es división entera.
6§¿Qué palabra clave define una función?§def§function§fun§define§
8§¿Qué estructura de datos usa pares clave-valor?§Diccionario§Lista§Tupla§Conjunto§
8§¿Cuál de estas estructuras es inmutable?§Tupla§Lista§Diccionario§Conjunto§Las tuplas no se pueden modificar después de creadas.
9§¿Qué valor representa «ausencia de valor» en Python?§None§Null§Nil§Void§
10§¿Qué operador representa la potencia?§**§^§^^§pow§En Python ^ es XOR, no potencia.
12§¿Qué hace la instrucción break dentro de un bucle?§Sale del bucle§Salta a la siguiente iteración§Reinicia el bucle§Termina el programa§
12§¿Qué hace la instrucción continue dentro de un bucle?§Pasa a la siguiente iteración§Sale del bucle§Termina el programa§Reinicia la variable§
14§¿Qué tipo devuelve input()?§str§int§float§bool§input siempre devuelve texto; hay que convertirlo.
15§¿Cómo se importa el módulo math?§import math§include math§using math§require math§
16§¿Qué palabra clave se usa para manejar errores?§try / except§catch / throw§error / handle§try / catch§Python usa try y except.
18§¿Qué hace "if __name__ == '__main__':"?§Ejecuta el bloque solo si el archivo se corre directamente§Importa el módulo principal§Define la función main§Evita errores de sintaxis§
20§¿Qué diferencia hay entre una lista y una tupla?§La lista es mutable y la tupla no§La tupla es más lenta§La lista no admite repetidos§La tupla solo guarda números§
22§¿Qué hace la palabra clave pass?§No hace nada; sirve de marcador§Sale de la función§Pasa un argumento§Salta la iteración§
24§¿Qué significa PEP 8?§La guía de estilo de código de Python§El intérprete de Python§Una biblioteca de matemáticas§Un tipo de dato§
26§¿Qué es una f-string?§Un texto con expresiones entre llaves§Una función de archivos§Un tipo de número§Un comentario especial§
28§¿Qué devuelve una función sin return?§None§0§Una cadena vacía§Un error§
30§¿Qué es una comprensión de listas?§Una forma compacta de crear listas§Un tipo de bucle infinito§Un método de ordenamiento§Una función recursiva§
32§¿Para qué sirve with open("a.txt") as f?§Cerrar el archivo automáticamente al terminar el bloque§Crear el archivo en blanco§Leerlo en memoria dos veces§Bloquear el archivo para siempre§
34§¿Qué hace el método .strip()?§Quita espacios del inicio y del final§Divide el texto§Convierte a mayúsculas§Elimina todos los espacios§
36§¿Qué significa que Python sea de tipado dinámico?§El tipo se decide al ejecutar según el valor§Hay que declarar el tipo siempre§No existen tipos§Los tipos no pueden cambiar§
38§¿Cuál es la diferencia entre == e is?§== compara valores; is compara identidad§Son idénticos§is compara valores; == identidad§is solo sirve con números§
40§¿Qué es un módulo en Python?§Un archivo .py que se puede importar§Una función especial§Un tipo de bucle§Una clase abstracta§
42§¿Qué significa *args en una definición de función?§Recibir cantidad variable de argumentos posicionales§Elevar a potencia§Recibir solo un argumento§Crear un puntero§
44§¿Qué significa **kwargs?§Recibir argumentos con nombre en un diccionario§Elevar al cuadrado§Recibir solo listas§Desempaquetar tuplas§
46§¿Qué es un generador (yield)?§Una función que entrega valores uno a uno§Una función que genera clases§Un módulo de números aleatorios§Un tipo de lista§
48§¿Qué hace el método __init__ de una clase?§Inicializa el objeto al crearlo§Elimina el objeto§Imprime el objeto§Hereda de otra clase§
50§¿Qué es la herencia en programación orientada a objetos?§Que una clase reutilice y extienda a otra§Copiar un archivo§Importar un módulo§Crear una lista de objetos§
52§¿Qué hace el decorador @staticmethod?§Define un método que no recibe self§Hace la clase estática§Congela los atributos§Evita la herencia§
54§¿Qué es el GIL en CPython?§Un bloqueo que permite ejecutar un solo hilo de bytecode a la vez§Un módulo de gráficos§Un recolector de listas§Una licencia§
56§¿Qué diferencia hay entre copy y deepcopy?§deepcopy copia también los objetos anidados§copy es más profundo§No hay diferencia§deepcopy solo sirve con números§
58§¿Qué es una excepción personalizada?§Una clase que hereda de Exception§Un error del sistema§Una función sin nombre§Un módulo importado§
60§¿Qué hace el método __str__?§Define cómo se convierte el objeto a texto§Convierte texto a objeto§Compara dos objetos§Borra el objeto§
62§¿Cómo se llama el mecanismo que libera memoria de objetos sin referencias?§Recolección de basura§Compilación§Interpolación§Serialización§
64§¿Qué complejidad tiene buscar un elemento en una lista con "in"?§O(n)§O(1)§O(log n)§O(n²)§
66§¿Qué complejidad promedio tiene buscar una clave en un diccionario?§O(1)§O(n)§O(log n)§O(n log n)§Los diccionarios usan tablas hash.
68§¿Qué hace @property?§Permite usar un método como si fuera un atributo§Hace privado un atributo§Crea una constante§Evita la herencia§
70§¿Qué es un decorador?§Una función que envuelve a otra para modificar su comportamiento§Un comentario especial§Un tipo de clase§Un bucle§
74§¿Qué hace yield from?§Delegar la generación de valores a otro iterable§Cerrar un generador§Convertir una lista en tupla§Importar un generador§
78§¿Qué problema tiene usar una lista vacía como argumento por defecto?§Se comparte entre llamadas§Es más lenta§No se puede modificar§Lanza SyntaxError§
82§¿Qué es un context manager?§Un objeto con __enter__ y __exit__ usado con with§Un tipo de lista§Un decorador de clases§Un archivo de configuración§
86§¿Qué ventaja tiene __slots__ en una clase?§Reduce memoria al evitar el diccionario de atributos§Permite herencia múltiple§Hace los atributos privados§Acelera la importación§
90§¿Qué es la MRO en herencia múltiple?§El orden en que Python busca los métodos§Un módulo de recursos§Un tipo de decorador§Una función de memoria§
94§¿Qué hace asyncio.gather?§Ejecuta varias corrutinas de forma concurrente§Une listas§Cierra el bucle de eventos§Crea hilos del sistema§
''')
