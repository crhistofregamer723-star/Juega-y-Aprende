from gen_prog_code import *
ri = R.randint
def distinct(lo, hi, n): return R.sample(range(lo, hi), n)

# ---------------- PYTHON ----------------
ops = [('+', 4), ('-', 6), ('*', 8), ('//', 22), ('%', 26), ('**', 34)]
for op, d in ops:
    for _ in range(2):
        a, b = ri(5, 20), ri(2, 6)
        code = f'a = {a}\nb = {b}\nprint(a {op} b)'
        muts = [f'a = {a}\nb = {b}\nprint(a {o} b)' for o, _ in ops if o != op]
        spec('py', 'py', code, muts, d + ri(0, 4), f'Con a = {a} y b = {b}, la operación «{op}» da el resultado mostrado.')
smeth = [('s.upper()', 10), ('s[0]', 12), ('s[-1]', 16), ('len(s)', 8), ('s[1:3]', 24), ('s * 2', 18), ('s + "!"', 12), ('s.capitalize()', 16), ('s[::-1]', 36), ('s.count("a")', 30), ('s.find("a")', 34), ('s.title()', 18)]
for expr, d in smeth:
    for w in R.sample(WORDS, 2):
        code = f's = "{w}"\nprint({expr})'
        muts = [f's = "{w}"\nprint({e})' for e, _ in smeth if e != expr]
        R.shuffle(muts)
        spec('py', 'py', code, muts[:6], d + ri(0, 4), f'Se aplica «{expr}» a la cadena "{w}".')
for _ in range(5):
    n = ri(1, 20); t = ri(1, 20)
    if n == t: continue
    code = f'x = {n}\nif x > {t}:\n    print("mayor")\nelse:\n    print("menor o igual")'
    mut = [code.replace('>', '<'), code.replace('>', '>='), code.replace(f'x = {n}', f'x = {t}'), code.replace('"mayor"', '"x"')]
    spec('py', 'py', code, mut, 18 + ri(0, 8), 'Se evalúa la condición y se ejecuta la rama correspondiente.')
for e, d in [('7 / 2', 20), ('7 // 2', 22), ('7 % 2', 24), ('2 ** 3', 24), ('10 / 5', 24), ('abs(-5)', 14), ('round(3.7)', 24), ('int(3.9)', 22), ('max(3, 9, 5)', 12), ('min(3, 9, 5)', 12), ('len([1, 2, 3])', 10), ('str(5) + "3"', 28), ('"5" * 3', 30), ('int("5") + 3', 26), ('bool(0)', 34), ('type(3.0).__name__', 38), ('3 == 3.0', 36), ('"a" < "b"', 40), ('not True', 20), ('True and False', 22), ('True or False', 22), ('10 > 3 and 2 > 5', 32)]:
    spec('py', 'py', f'print({e})', [], d, f'«{e}» se evalúa en Python.')
for _ in range(4):
    a, b = ri(2, 9), ri(2, 9)
    code = f'nombre = "Ana"\nprint(f"{{nombre}} tiene {{{a} * {b}}} puntos")'
    spec('py', 'py', code, [code.replace('*', '+'), code.replace('{nombre}', 'nombre'), code.replace('"Ana"', '"Luis"'), code.replace('puntos', 'años')], 34 + ri(0, 8), 'Las llaves {} de un f-string se evalúan.')
for _ in range(5):
    k, v = R.sample(['a', 'b', 'c', 'x', 'y'], 2); n1, n2 = ri(1, 9), ri(10, 99)
    code = f'd = {{"{k}": {n1}, "{v}": {n2}}}\nprint(d["{v}"])'
    muts = [f'd = {{"{k}": {n1}, "{v}": {n2}}}\nprint({e})' for e in [f'd["{k}"]', 'len(d)', f'd.get("z", 0)', f'd["{k}"] + d["{v}"]', 'list(d.keys())']]
    spec('py', 'py', code, muts, 38 + ri(0, 10), 'Se accede al valor por su clave.')
for n in [3, 4, 5, 6]:
    code = f'print([x * 2 for x in range({n})])'
    muts = [f'print([x + 2 for x in range({n})])', f'print([x * 2 for x in range(1, {n})])', f'print([x ** 2 for x in range({n})])', f'print(sum([x * 2 for x in range({n})]))']
    spec('py', 'py', code, muts, 46 + n, 'Una lista por comprensión aplica la expresión a cada elemento.')
for n in [4, 5, 6, 8]:
    code = f'print([x for x in range({n}) if x % 2 == 0])'
    muts = [f'print([x for x in range({n}) if x % 2 == 1])', f'print([x for x in range(1, {n}) if x % 2 == 0])', f'print(len([x for x in range({n}) if x % 2 == 0]))', f'print(sum(range({n})))']
    spec('py', 'py', code, muts, 52 + n, 'Se filtran los pares.')

# ---------------- FUNCIONES (Python y JS) ----------------
for _ in range(7):
    a, b = ri(2, 12), ri(2, 12)
    k = R.choice(['+', '*', '-'])
    code = f'def f(x, y):\n    return x {k} y\nprint(f({a}, {b}))'
    muts = [code.replace(f'x {k} y', f'x {o} y') for o in '+-*' if o != k] + [f'def f(x, y):\n    return x {k} y\nprint(f({b}, {a}))', f'def f(x, y):\n    x {k} y\nprint(f({a}, {b}))']
    spec('func', 'py', code, muts, 14 + ri(0, 14), 'La función devuelve el resultado de la operación con return.')
for _ in range(5):
    a = ri(2, 9); dflt = ri(2, 5)
    code = f'def potencia(base, exp={dflt}):\n    return base ** exp\nprint(potencia({a}))'
    muts = [f'def potencia(base, exp={dflt}):\n    return base ** exp\nprint(potencia({a}, 1))', f'def potencia(base, exp={dflt}):\n    return base * exp\nprint(potencia({a}))', f'def potencia(base, exp={dflt}):\n    return base ** exp\nprint(potencia({a}, 2))']
    spec('func', 'py', code, muts, 30 + ri(0, 10), 'Si no se pasa el argumento, se usa el valor por defecto.')
for n in [3, 4, 5, 6]:
    code = f'def fact(n):\n    if n <= 1:\n        return 1\n    return n * fact(n - 1)\nprint(fact({n}))'
    muts = [code.replace('n * fact', 'n + fact'), code.replace('return 1', 'return 0'), f'def fact(n):\n    if n <= 1:\n        return 1\n    return n * fact(n - 1)\nprint(fact({n+1}))', f'def fact(n):\n    if n <= 1:\n        return 1\n    return n * fact(n - 1)\nprint(fact({n-1}))']
    spec('func', 'py', code, muts, 62 + n * 2, 'Función recursiva: cada llamada multiplica por la del valor anterior.')
for n in [5, 6, 7, 8]:
    code = f'def fib(n):\n    if n < 2:\n        return n\n    return fib(n - 1) + fib(n - 2)\nprint(fib({n}))'
    muts = [f'def fib(n):\n    if n < 2:\n        return n\n    return fib(n - 1) + fib(n - 2)\nprint(fib({n+1}))', f'def fib(n):\n    if n < 2:\n        return n\n    return fib(n - 1) + fib(n - 2)\nprint(fib({n-1}))', code.replace('return n\n', 'return 1\n'), code.replace('+ fib', '* fib')]
    spec('func', 'py', code, muts, 70 + n, 'Fibonacci: cada término es la suma de los dos anteriores.')
for _ in range(4):
    a = ri(2, 9)
    code = f'x = {a}\ndef cambia():\n    x = {a*2}\ncambia()\nprint(x)'
    muts = [code.replace('cambia()\nprint', 'print').replace('print(x)', f'print({a*2})'), f'x = {a}\ndef cambia():\n    global x\n    x = {a*2}\ncambia()\nprint(x)', code.replace('x = ' + str(a*2), 'x = 0'), f'print({a+1})']
    spec('func', 'py', code, muts, 54 + ri(0, 8), 'La x de dentro es una variable local; la global no cambia.')
for _ in range(4):
    a, b = ri(2, 9), ri(2, 9)
    code = f'cuadrado = lambda n: n * n\nprint(cuadrado({a}) + cuadrado({b}))'
    spec('func', 'py', code, [f'cuadrado = lambda n: n * n\nprint(cuadrado({a} + {b}))', f'cuadrado = lambda n: n + n\nprint(cuadrado({a}) + cuadrado({b}))', f'cuadrado = lambda n: n * n\nprint(cuadrado({a}))', f'print({a} + {b})'], 50 + ri(0, 8), 'Una lambda es una función anónima de una línea.')
for _ in range(5):
    a, b = ri(2, 9), ri(2, 9)
    code = f'function suma(a, b) {{\n  return a + b;\n}}\nconsole.log(suma({a}, {b}));'
    muts = [code.replace('a + b', 'a * b'), code.replace('a + b', 'a - b'), code.replace('return a + b;', 'a + b;'), f'function suma(a, b) {{\n  return a + b;\n}}\nconsole.log(suma("{a}", {b}));']
    spec('func', 'js', code, muts, 16 + ri(0, 14), 'En JavaScript, return devuelve el valor; sin return se obtiene undefined.', pre='¿Qué muestra este código en la consola?')
for _ in range(4):
    a = ri(2, 9)
    code = f'const doble = (n) => n * 2;\nconsole.log(doble({a}) + 1);'
    spec('func', 'js', code, [code.replace('n * 2', 'n + 2'), code.replace('doble(' + str(a) + ') + 1', f'doble({a} + 1)'), code.replace('+ 1', '* 1'), code.replace('n * 2', 'n * 3')], 32 + ri(0, 10), 'Función flecha: n => n * 2.', pre='¿Qué muestra este código en la consola?')

# ---------------- BUCLES ----------------
for n in [3, 4, 5, 6, 8, 10]:
    code = f'total = 0\nfor i in range({n}):\n    total += i\nprint(total)'
    muts = [code.replace(f'range({n})', f'range(1, {n})'), code.replace(f'range({n})', f'range({n+1})'), code.replace('+= i', '+= 1'), code.replace('total = 0', 'total = 1'), code.replace('+= i', '+= i * 2')]
    spec('bucles', 'py', code, muts, 14 + n, 'range(n) recorre 0, 1, …, n − 1.')
for n in [3, 4, 5, 7]:
    code = f'i = 0\nwhile i < {n}:\n    i += 2\nprint(i)'
    muts = [code.replace('i < ' + str(n), 'i <= ' + str(n)), code.replace('+= 2', '+= 1'), code.replace('+= 2', '+= 3'), code.replace('i = 0', 'i = 1')]
    spec('bucles', 'py', code, muts, 20 + n, 'Se repite mientras la condición sea verdadera.')
for n in [3, 4, 5]:
    code = f'cont = 0\nfor i in range({n}):\n    for j in range({n}):\n        cont += 1\nprint(cont)'
    muts = [code.replace('cont += 1', 'cont += 2'), f'cont = 0\nfor i in range({n}):\n    for j in range({n+1}):\n        cont += 1\nprint(cont)', f'cont = 0\nfor i in range({n}):\n    cont += 1\nprint(cont)', code.replace('cont = 0', 'cont = 1')]
    spec('bucles', 'py', code, muts, 42 + n * 2, 'El bucle interno se ejecuta completo por cada vuelta del externo.')
for n in [5, 6, 8, 10]:
    k = ri(2, n-2)
    code = f'for i in range({n}):\n    if i == {k}:\n        break\nprint(i)'
    muts = [code.replace('break', 'continue'), code.replace(f'== {k}', f'== {k+1}'), code.replace(f'range({n})', f'range({k})'), f'print({n})']
    spec('bucles', 'py', code, muts, 34 + ri(0, 8), 'break termina el bucle; i conserva el valor en que se detuvo.')
for n in [5, 6, 8]:
    code = f's = 0\nfor i in range({n}):\n    if i % 2 == 0:\n        continue\n    s += i\nprint(s)'
    muts = [code.replace('continue', 'break'), code.replace('% 2 == 0', '% 2 == 1'), code.replace('s += i', 's += 1'), f's = 0\nfor i in range({n}):\n    s += i\nprint(s)']
    spec('bucles', 'py', code, muts, 44 + ri(0, 8), 'continue salta a la siguiente vuelta; solo se suman los impares.')
for n in [3, 4, 5]:
    code = f'print(*[i for i in range({n})])'
    spec('bucles', 'py', code, [f'print(*[i for i in range(1, {n})])', f'print(*[i for i in range({n+1})])', f'print(*[i * 2 for i in range({n})])', f'print({n})'], 24 + n, 'print(*lista) muestra los elementos separados por espacios.')
for n in [4, 5, 6]:
    code = f'let s = 1;\nfor (let i = 1; i <= {n}; i++) {{\n  s *= i;\n}}\nconsole.log(s);'
    muts = [code.replace('i <= ', 'i < '), code.replace('s *= i', 's += i'), code.replace('let s = 1', 'let s = 0'), code.replace(f'<= {n}', f'<= {n+1}')]
    spec('bucles', 'js', code, muts, 40 + n * 2, 'El bucle acumula el producto de 1 a n.', pre='¿Qué muestra este código en la consola?')
for n in [3, 4, 5]:
    code = f'int s = 0;\nfor (int i = 1; i <= {n}; i++) {{\n    s += i;\n}}\ncout << s;'
    muts = [code.replace('i <= ', 'i < '), code.replace('s += i', 's += 1'), code.replace('int i = 1', 'int i = 0').replace('s += i', 's += i + 1'), code.replace(f'<= {n}', f'<= {n+1}')]
    spec('bucles', 'cpp', code, muts, 22 + n * 2, 'El for suma los números de 1 a n.', pre='¿Qué imprime este código en C++?')

# ---------------- ARREGLOS (listas) ----------------
for _ in range(6):
    L = [ri(1, 30) for _ in range(5)]; i = ri(0, 4)
    code = f'a = {L}\nprint(a[{i}])'
    muts = [f'a = {L}\nprint(a[{(i+1)%5}])', f'a = {L}\nprint(a[{i-5}])' if i != 0 else f'a = {L}\nprint(a[-1])', f'a = {L}\nprint(len(a))', f'a = {L}\nprint(a[{(i+2)%5}])', f'a = {L}\nprint(a[{(i+3)%5}])']
    spec('arr', 'py', code, muts, 6 + i * 2, 'Los índices empiezan en 0.')
for expr, d in [('sum(a)', 14), ('max(a)', 12), ('min(a)', 12), ('len(a)', 8), ('sorted(a)', 28), ('a[1:3]', 26), ('a[::-1]', 36), ('a[-2:]', 34), ('sum(a) / len(a)', 32), ('a.index(%d)', 30), ('a.count(%d)', 30), ('[x for x in a if x > 10]', 44)]:
    for _ in range(2):
        L = [ri(1, 20) for _ in range(5)]
        e = expr % L[2] if '%d' in expr else expr
        code = f'a = {L}\nprint({e})'
        alts = ['sum(a)', 'max(a)', 'min(a)', 'len(a)', 'sorted(a)', 'a[1:3]', 'a[::-1]', 'a[-2:]', 'a[0]', 'a[-1]', 'a[1:4]', 'a[:2]']
        muts = [f'a = {L}\nprint({x})' for x in alts if x != e]
        R.shuffle(muts)
        spec('arr', 'py', code, muts[:6], d + ri(0, 4), f'Se evalúa «{e}» sobre la lista.')
for _ in range(5):
    L = [ri(1, 9) for _ in range(3)]; n = ri(10, 20)
    code = f'a = {L}\na.append({n})\nprint(a)'
    muts = [f'a = {L}\na.insert(0, {n})\nprint(a)', f'a = {L}\na.append({n})\nprint(len(a))', f'a = {L}\na.pop()\nprint(a)', f'a = {L}\na.remove({L[0]})\nprint(a)', f'a = {L}\na.append({n})\nprint(a[-1])']
    spec('arr', 'py', code, muts, 18 + ri(0, 8), 'append agrega al final de la lista.')
for _ in range(4):
    L = [ri(1, 9) for _ in range(4)]
    code = f'a = {L}\na.pop()\nprint(a)'
    muts = [f'a = {L}\na.pop(0)\nprint(a)', f'a = {L}\nprint(a.pop())', f'a = {L}\na.reverse()\nprint(a)', f'a = {L}\na.clear()\nprint(a)']
    spec('arr', 'py', code, muts, 26 + ri(0, 8), 'pop() elimina el último elemento.')
for _ in range(4):
    m = [[ri(1, 9) for _ in range(3)] for _ in range(2)]; i, j = ri(0, 1), ri(0, 2)
    code = f'm = {m}\nprint(m[{i}][{j}])'
    muts = [f'm = {m}\nprint(m[{j%2}][{i}])', f'm = {m}\nprint(m[{1-i}][{j}])', f'm = {m}\nprint(len(m))', f'm = {m}\nprint(len(m[0]))', f'm = {m}\nprint(m[{i}])']
    spec('arr', 'py', code, muts, 44 + ri(0, 10), 'Se indexa primero la fila y luego la columna.')
for _ in range(4):
    L = [ri(1, 20) for _ in range(4)]
    code = f'const a = {L};\nconsole.log(a.map(x => x * 2));'
    muts = [code.replace('x * 2', 'x + 2'), code.replace('.map(x => x * 2)', '.length'), code.replace('map', 'filter').replace('x * 2', 'x > 10'), code.replace('.map(x => x * 2)', '.reverse()')]
    spec('arr', 'js', code, muts, 40 + ri(0, 10), 'map crea un arreglo nuevo aplicando la función a cada elemento.', pre='¿Qué muestra este código en la consola?')
for _ in range(3):
    L = [ri(1, 9) for _ in range(5)]
    code = f'int a[] = {{{", ".join(map(str, L))}}};\ncout << a[{ri(0,4)}];'
    muts = [code.replace('cout << a[', 'cout << a[4-').replace('[4-', '[0+') if False else code.replace(code[-4:-2], '0]') ]
    spec('arr', 'cpp', code, [f'int a[] = {{{", ".join(map(str, L))}}};\ncout << a[{k}];' for k in range(5)], 10 + ri(0, 6), 'En C++ los arreglos también empiezan en el índice 0.', pre='¿Qué imprime este código en C++?')
