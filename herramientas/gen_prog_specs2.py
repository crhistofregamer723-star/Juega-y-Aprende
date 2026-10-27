from gen_prog_specs import *
PJ = '¿Qué muestra este código en la consola?'
# ---------------- JAVASCRIPT ----------------
for op, d in [('+', 4), ('-', 6), ('*', 8), ('/', 12), ('%', 24), ('**', 34)]:
    for _ in range(2):
        a, b = ri(4, 30), ri(2, 7)
        code = f'let a = {a};\nlet b = {b};\nconsole.log(a {op} b);'
        muts = [f'let a = {a};\nlet b = {b};\nconsole.log(a {o} b);' for o in ['+', '-', '*', '/', '%', '**'] if o != op]
        spec('js', 'js', code, muts, d + ri(0, 4), f'Con a = {a} y b = {b}, «{op}» da ese resultado.', pre=PJ)
for e, d in [('"5" + 3', 30), ('"5" - 3', 32), ('"5" * "2"', 34), ('true + 1', 40), ('[] + []', 62), ('typeof null', 56), ('typeof undefined', 36), ('typeof "hola"', 20), ('typeof 42', 18), ('typeof [1, 2]', 48), ('0.1 + 0.2 === 0.3', 60), ('"5" == 5', 38), ('"5" === 5', 38), ('NaN == NaN', 58), ('parseInt("12px")', 42), ('Number("abc")', 44), ('[1, 2, 3].length', 10), ('"hola".length', 10), ('"hola".toUpperCase()', 14), ('"hola mundo".split(" ").length', 28), ('[3, 1, 2].sort().join("")', 40), ('[1, 2, 3].includes(2)', 22), ('"abc".indexOf("c")', 24), ('"abc".slice(1)', 26), ('Math.max(4, 9, 2)', 16), ('Math.floor(7.8)', 18), ('Math.round(2.5)', 28), ('10 > 5 ? "sí" : "no"', 26), ('null ?? "x"', 64), ('!!"hola"', 52), ('[..."hi"].length', 50), ('"b" + "a" + +"a" + "a"', 78)]:
    spec('js', 'js', f'console.log({e});', [], d, f'En JavaScript, «{e}» se evalúa así (con conversión de tipos si hace falta).', pre=PJ)
for w in R.sample(WORDS, 4):
    code = f'const s = "{w}";\nconsole.log(s[0].toUpperCase() + s.slice(1));'
    spec('js', 'js', code, [code.replace('.slice(1)', ''), code.replace('s[0]', 's[1]'), code.replace('.toUpperCase()', ''), code.replace('slice(1)', 'slice(2)')], 34 + ri(0, 8), 'Se pone en mayúscula la primera letra y se une con el resto.', pre=PJ)
for _ in range(4):
    a, b = ri(1, 9), ri(1, 9)
    code = f'var x = {a};\nif (x > {b}) {{\n  console.log("A");\n}} else {{\n  console.log("B");\n}}'
    spec('js', 'js', code, [code.replace('>', '<'), code.replace('>', '>='), code.replace(f'x = {a}', f'x = {b}'), code.replace('"A"', '"C"')], 18 + ri(0, 8), 'Se evalúa la condición del if.', pre=PJ)
for _ in range(3):
    n = ri(2, 6)
    code = f'let c = 0;\nfor (let i = 0; i < {n}; i++) {{\n  c += i;\n}}\nconsole.log(c);'
    spec('js', 'js', code, [code.replace('i < ', 'i <= '), code.replace('c += i', 'c += 1'), code.replace('let c = 0', 'let c = 1'), code.replace(f'i < {n}', f'i < {n+1}')], 26 + n, 'El for suma 0, 1, …, n − 1.', pre=PJ)
for _ in range(3):
    n = ri(2, 5)
    code = f'const o = {{ a: {n}, b: {n*2} }};\nconsole.log(o.a + o.b);'
    spec('js', 'js', code, [code.replace('o.a + o.b', 'o.a * o.b'), code.replace('o.a + o.b', 'o.b - o.a'), code.replace('o.a + o.b', 'o.a'), code.replace('o.a + o.b', 'o.c')], 36 + ri(0, 8), 'Se accede a las propiedades del objeto.', pre=PJ)

# ---------------- C++ ----------------
PC = '¿Qué imprime este código en C++?'
for op, d in [('+', 4), ('-', 6), ('*', 8), ('/', 22), ('%', 26)]:
    for _ in range(2):
        a, b = ri(5, 40), ri(2, 7)
        code = f'int a = {a}, b = {b};\ncout << a {op} b;'
        muts = [f'int a = {a}, b = {b};\ncout << a {o} b;' for o in ['+', '-', '*', '/', '%'] if o != op]
        spec('cpp', 'cpp', code, muts, d + ri(0, 4), f'Con enteros, «{op}» da ese resultado (la división entera descarta decimales).', pre=PC)
for e, d, pre in [('7 / 2', 22, ''), ('7 % 2', 24, ''), ('7 / 2.0', 30, ''), ('(char)(\'a\' + 1)', 38, ''), ('(3 > 2)', 28, ''), ('(5 == 5) && (2 > 3)', 34, ''), ('10 / 3 * 3', 36, ''), ('2 + 3 * 4', 14, ''), ('(2 + 3) * 4', 16, ''), ('9 / 2', 22, ''), ('-7 / 2', 50, ''), ('5 > 3 || 1 > 2', 30, ''), ('int(3.99)', 28, ''), ('\'A\' + 1', 46, ''), ('sizeof(char)', 44, '')]:
    spec('cpp', 'cpp', f'cout << {e};', [], d, f'«{e}» se evalúa con las reglas de C++.', pre=PC)
for _ in range(5):
    n = ri(2, 9)
    code = f'int x = {n};\nx++;\ncout << x;'
    spec('cpp', 'cpp', code, [code.replace('x++', 'x--'), code.replace('x++', 'x += 2'), code.replace('x++;', ''), code.replace('x++', 'x *= 2')], 14 + ri(0, 8), 'x++ suma 1 a x.', pre=PC)
for _ in range(3):
    n = ri(2, 9)
    code = f'int x = {n};\ncout << x++ << " " << x;'
    spec('cpp', 'cpp', code, [f'int x = {n};\ncout << ++x << " " << x;', f'int x = {n};\ncout << x << " " << x++;', f'int x = {n};\ncout << x << " " << x;', f'int x = {n};\ncout << x-- << " " << x;'], 52 + ri(0, 8), 'x++ entrega el valor actual y luego incrementa.', pre=PC)
for w in R.sample(WORDS, 4):
    code = f'string s = "{w}";\ncout << s.length() << s[0];'
    spec('cpp', 'cpp', code, [code.replace('s.length()', 's.size() + 1'), code.replace('s[0]', 's[1]'), code.replace('s[0]', 's[s.length()-1]'), code.replace('<< s[0]', '')], 26 + ri(0, 8), 'length() devuelve la cantidad de caracteres; s[0] la primera letra.', pre=PC)
for _ in range(4):
    a, b = ri(1, 9), ri(1, 9)
    code = f'int x = {a};\nif (x > {b}) cout << "A";\nelse cout << "B";'
    spec('cpp', 'cpp', code, [code.replace('>', '<'), code.replace('>', '>='), code.replace(f'x = {a}', f'x = {b}'), code.replace('"A"', '"C"')], 18 + ri(0, 8), 'Se evalúa la condición del if.', pre=PC)
for _ in range(3):
    n = ri(2, 9)
    code = f'int x = {n};\nint *p = &x;\n*p = {n*2};\ncout << x;'
    spec('cpp', 'cpp', code, [code.replace('*p = ', 'p = (int*)').replace('(int*)', '') if False else code.replace(f'*p = {n*2}', f'*p = {n*3}'), code.replace('cout << x', 'cout << *p + 1'), code.replace(f'*p = {n*2};', ''), code.replace(f'*p = {n*2}', f'*p += {n}')], 66 + ri(0, 8), 'El puntero apunta a x; asignar con *p modifica x.', pre=PC)
for _ in range(3):
    n = ri(2, 6)
    code = f'int f = 1;\nfor (int i = 2; i <= {n}; i++) f *= i;\ncout << f;'
    spec('cpp', 'cpp', code, [code.replace('i <= ', 'i < '), code.replace('f *= i', 'f += i'), code.replace('int f = 1', 'int f = 0'), code.replace(f'<= {n}', f'<= {n+1}')], 40 + n * 2, 'Calcula el factorial con un for.', pre=PC)
for _ in range(3):
    a, b = ri(2, 9), ri(2, 9)
    code = f'int suma(int x, int y) {{ return x + y; }}\nint main2() {{ return 0; }}\ncout << suma({a}, {b});'
    code = f'cout << ({a} + {b}) * 2;'
    spec('cpp', 'cpp', code, [f'cout << {a} + {b} * 2;', f'cout << ({a} - {b}) * 2;', f'cout << {a} + {b};', f'cout << ({a} + {b}) / 2;'], 20 + ri(0, 8), 'Los paréntesis cambian el orden de las operaciones.', pre=PC)

# ---------------- PSEUDOCÓDIGO ----------------
PP = 'Según este pseudocódigo, ¿qué se escribe en pantalla?'
def pseudo(lines): return 'Inicio\n' + '\n'.join('  ' + l for l in lines) + '\nFin'
for _ in range(7):
    a, b = ri(2, 15), ri(2, 9); k = R.choice(['+', '-', '*'])
    ps = pseudo([f'x ← {a}', f'y ← {b}', f'x ← x {k} y', 'Escribir x'])
    py = f'x={a}\ny={b}\nx=x {k} y\nprint(x)'
    muts = [f'x={a}\ny={b}\nx=x {o} y\nprint(x)' for o in '+-*' if o != k] + [f'x={a}\ny={b}\nx=x {k} y\nprint(y)', f'x={a}\ny={b}\nprint(x {k} y + y)']
    spec('pseudo', 'py', py, muts, 8 + ri(0, 10), 'Se ejecuta cada instrucción en orden.', pre=PP, show=ps)
for _ in range(6):
    a, t = ri(1, 15), ri(1, 15)
    if a == t: continue
    ps = pseudo([f'n ← {a}', f'Si n > {t} Entonces', '  Escribir "Mayor"', 'SiNo', '  Escribir "Menor o igual"', 'FinSi'])
    py = f'n={a}\nif n>{t}:\n    print("Mayor")\nelse:\n    print("Menor o igual")'
    muts = [py.replace('>', '<'), py.replace('>', '>='), py.replace(f'n={a}', f'n={t}'), py.replace('"Mayor"', '"Igual"')]
    spec('pseudo', 'py', py, muts, 16 + ri(0, 10), 'Se evalúa la condición y se escribe la rama que corresponde.', pre=PP, show=ps)
for n in [3, 4, 5, 6, 7, 8]:
    ps = pseudo(['s ← 0', f'Para i ← 1 Hasta {n} Hacer', '  s ← s + i', 'FinPara', 'Escribir s'])
    py = f's=0\nfor i in range(1,{n+1}):\n    s=s+i\nprint(s)'
    muts = [py.replace(f'{n+1}', f'{n}'), py.replace('s=s+i', 's=s+1'), py.replace('s=0', 's=1'), py.replace('s=s+i', 's=s*i').replace('s=0', 's=1'), py.replace('range(1,', 'range(0,')]
    spec('pseudo', 'py', py, muts, 22 + n, 'Suma los enteros de 1 hasta n.', pre=PP, show=ps)
for k in [2, 3, 4]:
    n = ri(6, 12)
    ps = pseudo(['x ← 0', f'Mientras x < {n} Hacer', f'  x ← x + {k}', 'FinMientras', 'Escribir x'])
    py = f'x=0\nwhile x<{n}:\n    x=x+{k}\nprint(x)'
    muts = [py.replace(f'x<{n}', f'x<={n}'), py.replace(f'+{k}', '+1'), py.replace('x=0', 'x=1'), py.replace(f'x<{n}', f'x<{n-2}')]
    spec('pseudo', 'py', py, muts, 30 + k * 2, 'Se repite mientras la condición sea verdadera.', pre=PP, show=ps)
for _ in range(4):
    a, b = ri(1, 9), ri(10, 20)
    ps = pseudo([f'a ← {a}', f'b ← {b}', 't ← a', 'a ← b', 'b ← t', 'Escribir a, b'])
    py = f'a={a}\nb={b}\nt=a\na=b\nb=t\nprint(a,b)'
    muts = [f'a={a}\nb={b}\nprint(a,b)', f'a={a}\nb={b}\na=b\nb=a\nprint(a,b)', f'a={a}\nb={b}\nt=a\na=b\nb=t\nprint(b,a)', f'a={a}\nb={b}\nprint(a+b,b)']
    spec('pseudo', 'py', py, muts, 36 + ri(0, 8), 'Se intercambian los valores usando una variable auxiliar.', pre=PP, show=ps)
for n in [2, 3, 4, 5]:
    ps = pseudo(['c ← 0', f'Repetir', '  c ← c + 1', f'Hasta que c = {n}', 'Escribir c'])
    py = f'c=0\nwhile True:\n    c=c+1\n    if c=={n}: break\nprint(c)'
    spec('pseudo', 'py', py, [py.replace('c==' + str(n), f'c=={n+1}'), py.replace('c=c+1', 'c=c+2').replace(f'c=={n}', f'c>={n}'), py.replace('c=0', 'c=1'), f'print({n-1})'], 34 + n, 'Repetir…Hasta que ejecuta el bloque al menos una vez.', pre=PP, show=ps)
for _ in range(4):
    n = ri(3, 6)
    ps = pseudo([f'Para i ← 1 Hasta {n} Hacer', '  Si i MOD 2 = 0 Entonces', '    Escribir i', '  FinSi', 'FinPara'])
    py = f'r=[]\nfor i in range(1,{n+1}):\n    if i%2==0: r.append(i)\nprint(*r)'
    muts = [py.replace('==0', '==1'), py.replace(f'{n+1}', f'{n}'), py.replace('i%2', 'i%3'), py.replace('r.append(i)', 'r.append(i*2)')]
    spec('pseudo', 'py', py, muts, 42 + n, 'MOD es el residuo: solo se escriben los pares.', pre=PP, show=ps)
