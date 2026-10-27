from gen_prog_specs2 import *
# ---- más bucles (Python), con parámetros aleatorios ----
for _ in range(10):
    a, b, st = ri(0, 4), ri(6, 14), ri(2, 3)
    code = f'for i in range({a}, {b}, {st}):\n    print(i, end=" ")'
    muts = [code.replace(f', {st})', ', 1)'), code.replace(f'{b}, ', f'{b+1}, '), code.replace(f'range({a}, ', f'range({a+1}, '), f'for i in range({a}, {b}):\n    print(i, end=" ")', f'for i in range({b}, {a}, -{st}):\n    print(i, end=" ")']
    spec('bucles', 'py', code, muts, 24 + ri(0, 14), 'range(inicio, fin, paso): el fin no se incluye.')
for _ in range(8):
    n, f = ri(5, 40), ri(2, 3)
    code = f'x = {n}\nc = 0\nwhile x > 1:\n    x = x // {f}\n    c += 1\nprint(c)'
    muts = [code.replace('c += 1', 'c += 2'), code.replace('x > 1', 'x > 0') if f > 1 and False else code.replace('x > 1', 'x >= 1'), code.replace(f'// {f}', f'- {f}'), code.replace('c = 0', 'c = 1'), code.replace('x > 1', 'x > 2')]
    spec('bucles', 'py', code, muts, 46 + ri(0, 14), f'Se divide entre {f} hasta llegar a 1 y se cuenta cuántas veces.')
for _ in range(8):
    n, k = ri(8, 20), ri(2, 4)
    code = f's = 0\nfor i in range({n}):\n    if i % {k} == 0:\n        s += i\nprint(s)'
    muts = [code.replace(f'% {k} == 0', f'% {k} == 1'), code.replace(f'range({n})', f'range({n+1})'), code.replace('s += i', 's += 1'), code.replace('s = 0', 's = 1'), code.replace(f'% {k}', f'% {k+1}')]
    spec('bucles', 'py', code, muts, 38 + ri(0, 14), f'Suma solo los múltiplos de {k} menores que {n}.')
for _ in range(6):
    n = ri(3, 6)
    code = f'for i in range(1, {n+1}):\n    print("*" * i)' if False else f'r = ""\nfor i in range(1, {n+1}):\n    r += str(i)\nprint(r)'
    muts = [code.replace(f'{n+1}', f'{n}'), code.replace('str(i)', 'str(i * 2)'), code.replace('range(1,', 'range(0,'), code.replace('r += str(i)', 'r = str(i) + r'), code.replace('r += str(i)', 'r = str(i)')]
    spec('bucles', 'py', code, muts, 30 + ri(0, 14), 'Se concatenan los números como texto.')
for _ in range(7):
    n = ri(3, 5)
    code = f'c = 0\nfor i in range({n}):\n    for j in range(i):\n        c += 1\nprint(c)'
    muts = [code.replace('range(i)', 'range(i + 1)'), code.replace('range(i)', f'range({n})'), code.replace('c += 1', 'c += i'), code.replace('c = 0', 'c = 1'), f'c = 0\nfor i in range({n}):\n    c += 1\nprint(c)']
    spec('bucles', 'py', code, muts, 56 + n * 3 + ri(0, 6), 'El bucle interno hace i vueltas en la iteración i.')
for _ in range(7):
    lst = [ri(1, 12) for _ in range(6)]; t = ri(5, 9)
    code = f'datos = {lst}\nc = 0\nfor x in datos:\n    if x > {t}:\n        c += 1\nprint(c)'
    muts = [code.replace('x > ', 'x >= '), code.replace('x > ', 'x < '), code.replace('c += 1', 'c += x'), code.replace('c = 0', 'c = 1'), f'datos = {lst}\nprint(len(datos))']
    spec('bucles', 'py', code, muts, 36 + ri(0, 14), 'Cuenta cuántos elementos superan el umbral.')
for _ in range(6):
    n = ri(10, 30)
    code = f'for i in range({n}):\n    if i * i > {n}:\n        print(i)\n        break'
    muts = [code.replace('>', '>='), code.replace('break', 'pass'), code.replace('print(i)', 'print(i * i)'), code.replace('i * i', 'i + i'), f'print({n})']
    spec('bucles', 'py', code, muts, 52 + ri(0, 12), 'Se detiene en el primer i cuyo cuadrado supera el valor.')
for _ in range(6):
    n = ri(3, 8)
    code = f'let c = 0;\nlet i = {n};\nwhile (i > 0) {{\n  c += i;\n  i -= 2;\n}}\nconsole.log(c);'
    muts = [code.replace('i > 0', 'i >= 0'), code.replace('i -= 2', 'i -= 1'), code.replace('c += i', 'c += 1'), code.replace('let c = 0', 'let c = 1'), code.replace(f'let i = {n}', f'let i = {n+1}')]
    spec('bucles', 'js', code, muts, 34 + ri(0, 14), 'Cuenta hacia atrás de dos en dos mientras i sea positivo.', pre=PJ)
# ---- más pseudocódigo con dificultad creciente ----
for _ in range(8):
    n = ri(3, 6)
    ps = pseudo(['f ← 1', f'Para i ← 2 Hasta {n} Hacer', '  f ← f * i', 'FinPara', 'Escribir f'])
    py = f'f=1\nfor i in range(2,{n+1}):\n    f=f*i\nprint(f)'
    muts = [py.replace(f'{n+1}', f'{n}'), py.replace('f=f*i', 'f=f+i'), py.replace('f=1', 'f=0'), py.replace('range(2,', 'range(1,') + '', f'f=1\nfor i in range(2,{n+2}):\n    f=f*i\nprint(f)']
    spec('pseudo', 'py', py, muts, 44 + n * 2 + ri(0, 5), 'Calcula el factorial de n.', pre=PP, show=ps)
for _ in range(8):
    a, b = ri(5, 40), ri(2, 9)
    ps = pseudo([f'n ← {a}', f'r ← n MOD {b}', 'Escribir r'])
    py = f'n={a}\nr=n%{b}\nprint(r)'
    muts = [f'n={a}\nr=n//{b}\nprint(r)', f'n={a}\nr=n/{b}\nprint(r)', f'n={a}\nr={b}%n\nprint(r)', f'n={a}\nprint(n+{b})']
    spec('pseudo', 'py', py, muts, 20 + ri(0, 12), 'MOD devuelve el residuo de la división entera.', pre=PP, show=ps)
for _ in range(8):
    n = ri(10, 99)
    ps = pseudo([f'n ← {n}', 'c ← 0', 'Mientras n > 0 Hacer', '  c ← c + 1', '  n ← n DIV 10', 'FinMientras', 'Escribir c'])
    py = f'n={n}\nc=0\nwhile n>0:\n    c+=1\n    n=n//10\nprint(c)'
    muts = [py.replace('n>0', 'n>9'), py.replace('//10', '//2'), py.replace('c+=1', 'c+=2'), py.replace('c=0', 'c=1'), f'print({n})']
    spec('pseudo', 'py', py, muts, 58 + ri(0, 14), 'Cuenta los dígitos dividiendo entre 10 (DIV es división entera).', pre=PP, show=ps)
for _ in range(7):
    L = [ri(1, 20) for _ in range(5)]
    ps = pseudo([f'A ← {L}'.replace('[', '[').replace(']', ']'), 'm ← A[0]', 'Para i ← 1 Hasta 4 Hacer', '  Si A[i] > m Entonces', '    m ← A[i]', '  FinSi', 'FinPara', 'Escribir m'])
    py = f'A={L}\nm=A[0]\nfor i in range(1,5):\n    if A[i]>m:\n        m=A[i]\nprint(m)'
    muts = [py.replace('>m', '<m'), py.replace('range(1,5)', 'range(1,4)'), py.replace('m=A[i]', 'm=i'), f'print(min({L}))', f'print(sum({L}))']
    spec('pseudo', 'py', py, muts, 54 + ri(0, 14), 'Busca el mayor elemento del arreglo.', pre=PP, show=ps)
for _ in range(7):
    L = [ri(1, 9) for _ in range(5)]
    ps = pseudo([f'A ← {L}', 's ← 0', 'Para i ← 0 Hasta 4 Hacer', '  s ← s + A[i]', 'FinPara', 'Escribir s / 5'])
    py = f'A={L}\ns=0\nfor i in range(5):\n    s=s+A[i]\nprint(s/5)'
    muts = [py.replace('s/5', 's//5'), py.replace('s/5', 's'), py.replace('s=s+A[i]', 's=s+i'), py.replace('range(5)', 'range(4)'), py.replace('s/5', 's/4')]
    spec('pseudo', 'py', py, muts, 46 + ri(0, 10), 'Calcula el promedio de los elementos.', pre=PP, show=ps)
# ---- más funciones y JS/C++ con parámetros aleatorios ----
for _ in range(8):
    a, b, c = ri(1, 9), ri(1, 9), ri(1, 9)
    code = f'def f(x, y=2, z=1):\n    return x * y + z\nprint(f({a}), f({a}, {b}), f({a}, {b}, {c}))'
    muts = [code.replace('x * y + z', 'x + y * z'), code.replace('y=2', 'y=1'), code.replace('z=1', 'z=0'), code.replace(f'f({a}, {b}, {c})', f'f({c}, {b}, {a})'), code.replace('x * y + z', 'x * (y + z)')]
    spec('func', 'py', code, muts, 56 + ri(0, 14), 'Los valores por defecto se usan solo cuando falta el argumento.')
for _ in range(8):
    n = ri(2, 6)
    code = f'def suma(n):\n    if n == 0:\n        return 0\n    return n + suma(n - 1)\nprint(suma({n}))'
    muts = [code.replace('return 0', 'return 1'), code.replace('n + suma', 'n * suma'), f'def suma(n):\n    if n == 0:\n        return 0\n    return n + suma(n - 1)\nprint(suma({n+1}))', code.replace('n - 1', 'n - 2').replace('n == 0', 'n <= 0'), f'print({n})']
    spec('func', 'py', code, muts, 64 + ri(0, 14), 'Recursión: suma n + (n−1) + … + 1.')
for _ in range(5):
    a, b = ri(2, 8), ri(2, 8)
    code = f'def f(a, b):\n    return a // b, a % b\nq, r = f({a * b + ri(1, b-1) if b > 1 else a}, {b})\nprint(q, r)'
    spec('func', 'py', code, [code.replace('//', '/'), code.replace('a % b', 'a * b'), code.replace('q, r = f', 'r, q = f'), code.replace('a // b, a % b', 'a % b, a // b')], 58 + ri(0, 14), 'Una función puede devolver varios valores (una tupla).')
for _ in range(6):
    a = ri(2, 7)
    code = f'function f(n) {{\n  return n <= 1 ? 1 : n * f(n - 1);\n}}\nconsole.log(f({a}));'
    spec('func', 'js', code, [code.replace('n * f', 'n + f'), code.replace('? 1', '? 0'), code.replace('n <= 1', 'n <= 2'), code.replace(f'f({a})', f'f({a+1})')], 60 + ri(0, 14), 'Factorial recursivo en JavaScript.', pre=PJ)
for _ in range(8):
    a, b = ri(2, 15), ri(2, 9)
    code = f'int f(int x) {{ return x * 2; }}\n'
    code = f'int x = {a};\nint y = {b};\nint t = x;\nx = y;\ny = t;\ncout << x << " " << y;'
    spec('cpp', 'cpp', code, [code.replace('x = y;\ny = t;', ''), code.replace('int t = x;', 'int t = y;'), f'cout << {a} << " " << {b};', code.replace('y = t', 'y = x')], 30 + ri(0, 10), 'Se intercambian los valores con una variable auxiliar.', pre=PC)
for _ in range(8):
    n = ri(3, 8)
    code = f'int s = 0;\nfor (int i = 0; i < {n}; i++) {{\n    if (i % 2 == 0) s += i;\n}}\ncout << s;'
    spec('cpp', 'cpp', code, [code.replace('== 0', '== 1'), code.replace('i < ', 'i <= '), code.replace('s += i', 's += 1'), code.replace('s = 0', 's = 1')], 40 + n + ri(0, 6), 'Suma los números pares menores que n.', pre=PC)
for _ in range(8):
    L = [ri(1, 9) for _ in range(4)]
    code = f'int a[] = {{{", ".join(map(str, L))}}};\nint m = a[0];\nfor (int i = 1; i < 4; i++) if (a[i] > m) m = a[i];\ncout << m;'
    spec('cpp', 'cpp', code, [code.replace('>', '<'), code.replace('i = 1', 'i = 0') + '', code.replace('m = a[i]', 'm = i'), code.replace('i < 4', 'i < 3')], 50 + ri(0, 14), 'Encuentra el mayor del arreglo.', pre=PC)
for _ in range(8):
    a = ri(2, 9)
    code = f'const arr = [{a}, {a+1}, {a+2}];\nconst r = arr.reduce((s, x) => s + x, 0);\nconsole.log(r);'
    spec('js', 'js', code, [code.replace('s + x', 's * x'), code.replace(', 0)', ', 10)'), code.replace('reduce((s, x) => s + x, 0)', 'length'), code.replace('s + x', 's - x')], 62 + ri(0, 14), 'reduce acumula los elementos en un solo valor.', pre=PJ)
for _ in range(8):
    a = ri(2, 9)
    code = f'const a = [{a}, {a+3}, {a+1}, {a+5}];\nconsole.log(a.filter(x => x > {a+1}).length);'
    spec('js', 'js', code, [code.replace('>', '>='), code.replace('.length', '[0]'), code.replace('filter', 'map').replace('x > ' + str(a+1), 'x'), code.replace(f'x > {a+1}', f'x > {a}')], 54 + ri(0, 14), 'filter conserva los elementos que cumplen la condición.', pre=PJ)
