# -*- coding: utf-8 -*-
import random
from lib import *

TIPOS = ['int', 'float', 'str', 'bool', 'list', 'tuple', 'dict', 'set', 'NoneType']
WORDS = ['sol', 'luna', 'mar', 'pan', 'casa', 'gato', 'río', 'flor', 'uva', 'tren', 'nube', 'lápiz']
BIG = ['programa', 'python', 'computadora', 'teclado', 'algoritmo', 'variable', 'pantalla', 'archivo', 'funcion',
       'lenguaje', 'memoria', 'servidor', 'internet', 'ratón']

def build(B):
    rng = random.Random(11)
    def O(fam, d, code, muts=(), **k):
        return OUT(B, fam, d, 'py', code, muts, **k)

    # 1. print
    for i in range(12):
        w1, w2 = WORDS[i], WORDS[(i + 5) % 12]; t = i % 4; d = spread(i, 12, 3, 14)
        if t == 0:
            O('print', d, f'print("{w1}", "{w2}")', [f'print("{w1}" + "{w2}")', f'print("{w1}", "{w2}", sep=",")', f'print("{w2}", "{w1}")'],
              expl='print separa con un espacio los valores que recibe como argumentos.')
        elif t == 1:
            c = f'print("{w1}", end="-")\nprint("{w2}")'
            O('print', d, c, [('end="-"', 'end=""'), ('end="-"', 'end=" "'), ('end="-"', 'end="+"')],
              expl='El parámetro end reemplaza el salto de línea final, por eso el segundo print continúa en la misma línea.')
        elif t == 2:
            c = f'print("{w1}", "{w2}", sep="*")'
            O('print', d, c, [('sep="*"', 'sep=""'), ('sep="*"', 'sep=" "'), ('sep="*"', 'sep="-"')],
              expl='sep define lo que se coloca entre los argumentos; aquí es un asterisco.')
        else:
            n = 2 + i % 3
            O('print', d, f'print("{w1}" * {n})', [f'print("{w1}" + "{n}")', f'print("{w1}", {n})', f'print("{w1}" * {n + 1})'],
              expl='Multiplicar un texto por un entero lo repite esa cantidad de veces.')

    # 2. tipos
    ex = [('5', 3), ('5.0', 4), ('"5"', 4), ('True', 5), ('[1, 2]', 6), ('(1, 2)', 8), ('{1, 2}', 9), ('{"a": 1}', 9), ('None', 10),
          ('7 / 7', 11), ('7 // 2', 12), ('"a" * 3', 12), ('2 ** 3', 13), ('1 + 2.0', 13), ('5 > 3', 14), ('len("ab")', 14),
          ('str(5)', 15), ('round(2.6)', 16), ('round(2.6, 1)', 17), ('"hola".split()', 18), ('{}', 20), ('3 == 3.0', 18)]
    for i, (e, d) in enumerate(ex):
        nm = run_py(f'print(type({e}).__name__)')
        ws = pickw(rng, nm, TIPOS)
        B.add('tipos', d, f'¿Qué tipo de dato (clase) tiene el valor de {e} en Python?', nm, ws, [nm],
              f'type({e}) devuelve la clase {nm}: así evalúa Python esa expresión.')

    # 3. aritmética
    ops = ['+', '-', '*', '/', '//', '%', '**']
    pairs = [(17, 5), (9, 2), (20, 4), (13, 3), (8, 3), (25, 7), (6, 4), (30, 8), (14, 5), (11, 2), (22, 6), (40, 9), (7, 3), (19, 4)]
    for i, (a, b) in enumerate(pairs):
        op = ops[(i * 3 + i // 7) % 7]
        if op == '**': a, b = a % 6 + 2, b % 4 + 2
        muts = [f'print({a} {o} {b})' for o in ops if o != op]
        exps = {'+': 'La suma de ambos números.', '-': 'La resta del segundo al primero.', '*': 'El producto de ambos números.',
                '/': 'La división con / siempre da un float, aunque sea exacta.', '//': 'La división entera // descarta la parte decimal.',
                '%': 'El operador % da el residuo de la división.', '**': 'El operador ** eleva el primer número a la potencia del segundo.'}
        O('aritmetica', spread(i, 14, 6, 20), f'print({a} {op} {b})', muts, expl=exps[op])

    # 4. precedencia
    pre = [
        ('x = 2 + 3 * 4\nprint(x)', 'La multiplicación se evalúa antes que la suma.'),
        ('print((2 + 3) * 4)', 'Los paréntesis cambian el orden: primero se suma.'),
        ('x = 10\nx += 5\nx *= 2\nprint(x)', 'x pasa de 10 a 15 y luego a 30.'),
        ('print(10 - 4 - 3)', 'La resta se asocia de izquierda a derecha: (10-4)-3.'),
        ('print(2 * 3 ** 2)', 'Primero la potencia (9) y luego el producto.'),
        ('print(2 ** 3 ** 2)', 'La potencia se asocia de derecha a izquierda: 2 ** 9.'),
        ('a = 7\na //= 2\nprint(a)', 'a //= 2 equivale a a = a // 2.'),
        ('print(10 / 4 * 2)', '10 / 4 da 2.5 y luego se multiplica por 2.'),
        ('x = 5\nx -= 2\nx **= 2\nprint(x)', 'x vale 3 tras la resta y 9 tras elevar al cuadrado.'),
        ('print(-7 // 2)', 'La división entera redondea hacia abajo: -3.5 pasa a -4.'),
        ('print(-7 % 3)', 'En Python el residuo toma el signo del divisor: -7 = 3*(-3) + 2.'),
        ('print(7 % 2 == 1)', '7 % 2 vale 1, así que la comparación es verdadera.'),
        ('a, b = 3, 4\na, b = b, a + b\nprint(a, b)', 'La asignación múltiple evalúa la derecha antes de asignar: a=4, b=7.'),
        ('x = 4\nprint(x * x - x // 2)', 'x*x vale 16 y x//2 vale 2.'),
    ]
    for i, (c, e) in enumerate(pre):
        O('precedencia', spread(i, len(pre), 12, 36), c, expl=e)

    # 5. strings: índices y rebanadas
    st = [('s[0]', 'El primer carácter está en el índice 0.'), ('s[-1]', 'El índice -1 es el último carácter.'),
          ('s[1:4]', 'La rebanada llega hasta el índice 4 sin incluirlo.'), ('s[:3]', 'Toma desde el inicio hasta el índice 3 sin incluirlo.'),
          ('s[2:]', 'Toma desde el índice 2 hasta el final.'), ('s[::-1]', 'El paso -1 invierte el texto.'),
          ('s[::2]', 'El paso 2 toma un carácter sí y otro no.'), ('len(s)', 'len cuenta todos los caracteres.'),
          ('s[-3:]', 'Toma los últimos tres caracteres.'), ('s[1:-1]', 'Quita el primer y el último carácter.'),
          ('s[3]', 'Los índices comienzan en 0.'), ('s[-2]', 'El índice -2 es el penúltimo carácter.')]
    for i, (e, ex_) in enumerate(st):
        w = BIG[(i * 5) % len(BIG)]
        alt = {'s[0]': ['s[1]', 's[-1]', 's[:2]'], 's[-1]': ['s[0]', 's[-2]', 's[len(s)]'], 's[1:4]': ['s[1:3]', 's[0:4]', 's[1:5]'],
               's[:3]': ['s[:2]', 's[:4]', 's[3:]'], 's[2:]': ['s[3:]', 's[1:]', 's[:2]'], 's[::-1]': ['s[::2]', 's[-1]', 's[1:]'],
               's[::2]': ['s[1::2]', 's[::3]', 's[::-1]'], 'len(s)': ['len(s) - 1', 'len(s) + 1', 's.count("a")'],
               's[-3:]': ['s[-2:]', 's[:3]', 's[-4:]'], 's[1:-1]': ['s[1:]', 's[:-1]', 's[2:-2]'], 's[3]': ['s[2]', 's[4]', 's[-3]'],
               's[-2]': ['s[-1]', 's[-3]', 's[2]']}[e]
        c = f's = "{w}"\nprint({e})'
        O('strings_idx', spread(i, 12, 18, 34), c, [(e, a) for a in alt], expl=ex_)

    # 6. métodos de str
    mt = [('"hola".upper()', 'upper() convierte todo a mayúsculas.', ['"hola".lower()', '"hola".title()']),
          ('"Hola Mundo".lower()', 'lower() pasa todo a minúsculas.', ['"Hola Mundo".upper()', '"Hola Mundo".swapcase()']),
          ('"banana".count("a")', 'count cuenta cuántas veces aparece el fragmento.', ['"banana".count("an")', '"banana".find("a")']),
          ('"casa".replace("a", "o")', 'replace cambia todas las apariciones.', ['"casa".replace("a", "o", 1)', '"casa".replace("o", "a")']),
          ('"python".find("t")', 'find devuelve el índice de la primera aparición.', ['"python".find("y")', '"python".find("z")']),
          ('"  hola  ".strip()', 'strip quita los espacios de ambos extremos.', ['"  hola  ".lstrip()', '"  hola  ".rstrip()']),
          ('"a-b-c".split("-")', 'split devuelve una lista con los fragmentos.', ['"a-b-c".split()', '"a-b-c".split("-", 1)']),
          ('"-".join(["x", "y", "z"])', 'join une los elementos usando el separador.', ['"".join(["x", "y", "z"])', '"-".join("xyz"[:2])']),
          ('"python".startswith("py")', 'startswith comprueba el inicio del texto.', ['"python".endswith("py")', '"python".startswith("th")']),
          ('"hola mundo".capitalize()', 'capitalize pone en mayúscula solo la primera letra.', ['"hola mundo".title()', '"hola mundo".upper()']),
          ('"abc".isalpha()', 'isalpha es True si todo son letras.', ['"ab1".isalpha()', '"abc".isdigit()']),
          ('"ana".replace("a", "")', 'Reemplazar por una cadena vacía elimina los caracteres.', ['"ana".replace("n", "")', '"ana".replace("a", " ")']),
          ('"Python".swapcase()', 'swapcase invierte mayúsculas y minúsculas.', ['"Python".lower()', '"Python".upper()']),
          ('"7".zfill(3)', 'zfill rellena con ceros a la izquierda hasta el ancho dado.', ['"7".ljust(3)', '"7".zfill(2)'])]
    for i, (e, ex_, mm) in enumerate(mt):
        O('str_metodos', spread(i, len(mt), 24, 40), f'print({e})', [f'print({m})' for m in mm], expl=ex_)

    # 7. conversiones
    cv = [('print(int("7") + 3)', 'int convierte el texto en número antes de sumar.'),
          ('print("7" + "3")', 'Con textos, + concatena en lugar de sumar.'),
          ('print("ab" * 3)', 'Un texto multiplicado por 3 se repite tres veces.'),
          ('print(str(5) + "1")', 'str(5) es "5"; concatenado con "1" da "51".'),
          ('print(float("2.5") * 2)', 'float convierte el texto y el producto es decimal.'),
          ('print(int(3.9))', 'int trunca la parte decimal, no redondea.'),
          ('print(round(3.5))', 'round(3.5) da 4 (el vecino par).'),
          ('print(round(2.5))', 'Python redondea los .5 al entero par más cercano: 2.'),
          ('print(len(str(1234)))', 'str(1234) es "1234", que tiene 4 caracteres.'),
          ('print(bool(0), bool(7))', 'El 0 es falso y cualquier otro número es verdadero.'),
          ('print(bool(""), bool("0"))', 'Un texto vacío es falso; "0" es un texto no vacío, así que es verdadero.'),
          ('print(int("12") * 2)', 'Se convierte "12" a 12 y se multiplica.'),
          ('print(abs(-4) + max(2, 9))', 'abs(-4) vale 4 y max(2, 9) vale 9.'),
          ('print(int(True) + int(False))', 'True vale 1 y False vale 0 al convertirlos a int.'),
          ('print(10 / 5)', 'La división / siempre produce un float.')]
    for i, (c, e) in enumerate(cv):
        O('conversion', spread(i, len(cv), 18, 36), c, expl=e)

    # 8. if / elif
    tp = [
        ('n = {n}\nif n % 2 == 0:\n    print("par")\nelif n > 10:\n    print("grande")\nelse:\n    print("chico")', [15, 4, 7, 12, 21, 9], 'Se ejecuta solo la primera rama cuya condición sea verdadera.'),
        ('nota = {n}\nif nota >= 90:\n    print("A")\nelif nota >= 70:\n    print("B")\nelse:\n    print("C")', [95, 72, 50, 70, 89, 90], 'Las condiciones se revisan en orden y gana la primera verdadera.'),
        ('x = {n}\nif x > 5:\n    print("a", end=" ")\nif x > 8:\n    print("b", end=" ")\nprint("fin")', [3, 6, 9, 5, 8, 10], 'Son dos if independientes: pueden cumplirse ambos.'),
    ]
    cnt = 0
    for ti, (t, vals, e) in enumerate(tp):
        for j, v in enumerate(vals[:4]):
            c = t.format(n=v)
            others = [x for x in vals if x != v][:5]
            O('condicionales', spread(cnt, 12, 26, 42), c, [(f'= {v}\n', f'= {x}\n') for x in others], expl=e)
            cnt += 1

    # 9. lógicos
    lg = [('print(3 > 2 and 5 < 4)', 'and exige que ambas condiciones sean verdaderas.'),
          ('print(3 > 2 or 5 < 4)', 'or basta con que una condición sea verdadera.'),
          ('print(not (4 == 4))', 'not invierte el valor lógico.'),
          ('x = 7\nprint(1 < x < 10)', 'Python permite comparaciones encadenadas.'),
          ('print("a" in "casa")', 'in revisa si el fragmento está dentro del texto.'),
          ('print(0 or "vacío")', 'or devuelve el primer operando verdadero.'),
          ('print(5 and 8)', 'and devuelve el último valor si todos son verdaderos.'),
          ('print([] or "sin datos")', 'Una lista vacía es falsa, así que or devuelve el segundo valor.'),
          ('print(None == 0)', 'None no es igual a 0.'),
          ('print(not 0 and not "")', '0 y "" son falsos; not los vuelve verdaderos.'),
          ('a = 5\nprint(a != 5 or a >= 5)', 'a != 5 es falso, pero a >= 5 es verdadero.'),
          ('print(True + True)', 'True equivale a 1, por eso la suma da 2.'),
          ('print("b" > "a" and 10 > 9)', 'Las letras se comparan por orden alfabético (código).'),
          ('print(3 == 3.0, 3 is 3.0)'.replace(', 3 is 3.0', ', "3" == 3'), '3 == 3.0 es True; "3" == 3 es False.')]
    for i, (c, e) in enumerate(lg):
        O('logicos', spread(i, len(lg), 28, 44), c, expl=e, wr=['True', 'False', 'None', '0'])

    # 10. for/range
    fr = []
    for (a, b, s) in [(1, 6, 1), (0, 10, 3), (2, 12, 2), (5, 0, -1), (1, 5, 1), (3, 15, 4)]:
        fr.append((f'total = 0\nfor i in range({a}, {b}, {s}):\n    total += i\nprint(total)',
                   [(f'range({a}, {b}, {s})', f'range({a}, {b + 1}, {s})'), (f'range({a}, {b}, {s})', f'range({a + 1}, {b}, {s})'),
                    (f'range({a}, {b}, {s})', f'range({a}, {b - s}, {s})')], 'range excluye el valor final; la suma recorre cada valor generado.'))
    for n in (4, 6):
        fr.append((f'for i in range({n}):\n    print(i, end=" ")', [(f'range({n})', f'range(1, {n})'), (f'range({n})', f'range({n + 1})'), (f'range({n})', f'range(1, {n + 1})')], 'range(n) genera de 0 a n-1.'))
    for w in ('python', 'casa', 'hola'):
        fr.append((f'for c in "{w}":\n    print(c, end="-")', [('end="-"', 'end=""'), ('end="-"', 'end=" "'), (f'"{w}"', f'"{w[::-1]}"')], 'Recorrer un texto entrega un carácter por vuelta.'))
    fr.append(('n = 0\nfor i in range(3):\n    for j in range(4):\n        n += 1\nprint(n)', [('range(4)', 'range(3)'), ('range(4)', 'range(5)'), ('range(3)', 'range(4)')], 'El bucle interno se repite completo en cada vuelta del externo: 3 × 4.'))
    fr.append(('print(len(range(2, 11, 3)))', [('2, 11, 3', '2, 11, 2'), ('2, 11, 3', '2, 12, 3'), ('2, 11, 3', '1, 11, 3')], 'range(2, 11, 3) genera 2, 5, 8.'))
    for i, (c, mm, e) in enumerate(fr):
        O('for_range', spread(i, len(fr), 30, 46), c, mm, expl=e)

    # 11. while
    wh = [('n = 27\nc = 0\nwhile n > 1:\n    n //= 2\n    c += 1\nprint(c)', 'Cuenta cuántas veces se puede dividir entre 2 hasta llegar a 1.'),
          ('x = 1\nwhile x < 100:\n    x *= 3\nprint(x)', 'x se triplica hasta superar 100.'),
          ('n = 4321\ns = 0\nwhile n > 0:\n    s += n % 10\n    n //= 10\nprint(s)', 'Suma los dígitos extrayendo el último con % 10.'),
          ('i = 10\nwhile i > 0:\n    i -= 3\nprint(i)', 'Termina cuando i deja de ser positivo.'),
          ('f = 1\nk = 5\nwhile k > 1:\n    f *= k\n    k -= 1\nprint(f)', 'Calcula 5 × 4 × 3 × 2.'),
          ('a, b = 0, 1\nwhile b < 30:\n    a, b = b, a + b\nprint(a)', 'Recorre la sucesión de Fibonacci mientras b < 30.'),
          ('n = 0\nwhile n < 5:\n    n += 1\n    if n == 3:\n        continue\n    print(n, end=" ")', 'continue salta el print cuando n vale 3.'),
          ('n = 0\nwhile True:\n    n += 2\n    if n > 7:\n        break\nprint(n)', 'break sale en cuanto n supera 7.'),
          ('x = 100\ncount = 0\nwhile x >= 10:\n    x /= 2\n    count += 1\nprint(count)', 'x pasa por 50, 25, 12.5 y 6.25; son 4 divisiones hasta que x < 10.'),
          ('s = 0\ni = 1\nwhile i <= 20:\n    s += i\n    i += 5\nprint(s)', 'Suma 1, 6, 11 y 16.'),
          ('n = 12\nr = ""\nwhile n > 0:\n    r = str(n % 2) + r\n    n //= 2\nprint(r)', 'Convierte 12 a binario con divisiones sucesivas.'),
          ('p = 1\nwhile p < 50:\n    p = p * 2 + 1\nprint(p)', 'p vale 1, 3, 7, 15, 31 y 63.')]
    for i, (c, e) in enumerate(wh):
        O('while', spread(i, len(wh), 34, 52), c, expl=e)


def build2(B):
    rng = random.Random(12)
    def O(fam, d, code, muts=(), **k):
        return OUT(B, fam, d, 'py', code, muts, **k)
    def LST(fam, lo, hi, rows, **k):
        for i, r in enumerate(rows):
            c, e = r[0], r[1]
            muts = r[2] if len(r) > 2 else ()
            O(fam, spread(i, len(rows), lo, hi), c, muts, expl=e, **k)

    # 13. listas: índices y rebanadas
    L1 = [[4, 8, 15, 16, 23, 42], [3, 1, 4, 1, 5, 9], [10, 20, 30, 40, 50], [7, 14, 21, 28, 35, 42]]
    rows = []
    for j, ls in enumerate(L1):
        rows += [(f'lst = {ls}\nprint(lst[-1])', 'El índice -1 apunta al último elemento.', [('lst[-1]', 'lst[-2]'), ('lst[-1]', 'lst[0]')]),
                 (f'lst = {ls}\nprint(lst[1:3])', 'La rebanada incluye los índices 1 y 2 (el 3 queda fuera).', [('[1:3]', '[1:4]'), ('[1:3]', '[0:3]'), ('[1:3]', '[2:4]')]),
                 (f'lst = {ls}\nprint(lst[::-1])', 'El paso -1 recorre la lista al revés.', [('[::-1]', '[::2]'), ('[::-1]', '[1:]')]),
                 ]
    rows += [(f'lst = {L1[2]}\nprint(len(lst), lst[len(lst) - 1])', 'El último índice es len(lst) - 1.', [('lst[len(lst) - 1]', 'lst[len(lst)]')]) if False else
             (f'lst = {L1[2]}\nprint(lst[::2])', 'El paso 2 toma un elemento sí y otro no.', [('[::2]', '[1::2]'), ('[::2]', '[::3]')]),
             (f'lst = {L1[0]}\nprint(sum(lst[:3]))', 'Se suman los tres primeros elementos.', [('[:3]', '[:2]'), ('[:3]', '[1:4]')]),
             (f'lst = {L1[1]}\nprint(lst.index(4), 5 in lst)', 'index da la posición; in comprueba pertenencia.', [('index(4)', 'index(1)'), ('5 in lst', '7 in lst')])]
    LST('lista_idx', 38, 54, rows)

    # 14. métodos de lista
    base = [5, 3, 8, 1]
    LST('lista_met', 44, 58, [
        ('lst = [5, 3, 8, 1]\nlst.append(9)\nprint(lst)', 'append agrega al final.', [('append(9)', 'insert(0, 9)'), ('append(9)', 'extend([9, 9])')]),
        ('lst = [5, 3, 8, 1]\nlst.insert(1, 7)\nprint(lst)', 'insert(i, x) coloca x en la posición i y corre el resto.', [('insert(1, 7)', 'insert(2, 7)'), ('insert(1, 7)', 'append(7)')]),
        ('lst = [5, 3, 8, 1]\nprint(lst.pop(), lst)', 'pop() quita y devuelve el último elemento.', [('lst.pop()', 'lst.pop(0)'), ('lst.pop()', 'lst.pop(1)')]),
        ('lst = [5, 3, 8, 1]\nlst.remove(8)\nprint(lst)', 'remove borra la primera aparición del valor.', [('remove(8)', 'remove(3)'), ('remove(8)', 'pop(8 - 6)')]),
        ('lst = [5, 3, 8, 1]\nlst.sort()\nprint(lst)', 'sort ordena la lista de menor a mayor.', [('lst.sort()', 'lst.sort(reverse=True)'), ('lst.sort()', 'lst.reverse()')]),
        ('lst = [5, 3, 8, 1]\nlst.reverse()\nprint(lst)', 'reverse invierte el orden actual, no ordena.', [('lst.reverse()', 'lst.sort()'), ('lst.reverse()', 'lst.sort(reverse=True)')]),
        ('lst = [1, 2]\nlst.extend([3, 4])\nprint(lst)', 'extend agrega cada elemento del iterable.', [('extend([3, 4])', 'append([3, 4])'), ('extend([3, 4])', 'insert(0, 3)')]),
        ('lst = [1, 2]\nlst.append([3, 4])\nprint(len(lst))', 'append agrega la lista completa como un solo elemento.', [('append([3, 4])', 'extend([3, 4])'), ('append([3, 4])', 'append(3)')]),
        ('lst = [2, 7, 2, 2, 9]\nprint(lst.count(2))', 'count cuenta las apariciones de un valor.', [('count(2)', 'count(7)'), ('count(2)', 'index(9)')]),
        ('lst = [3, 1, 2]\nr = sorted(lst)\nprint(lst, r)', 'sorted crea una lista nueva y no modifica la original.', [('sorted(lst)', 'lst.sort()'), ('sorted(lst)', 'sorted(lst, reverse=True)')]),
        ('lst = [3, 1, 2]\nr = lst.sort()\nprint(r)', 'sort modifica la lista y devuelve None.', [('r = lst.sort()', 'r = sorted(lst)'), ('r = lst.sort()', 'r = lst.reverse()')]),
        ('lst = [1, 2, 3, 4]\ndel lst[1]\nprint(lst)', 'del elimina el elemento del índice 1.', [('lst[1]', 'lst[0]'), ('del lst[1]', 'del lst[1:3]')]),
        ('lst = [1, 2, 3, 4, 5]\nlst[1:3] = [9]\nprint(lst)', 'Una rebanada se puede reemplazar por otra lista de distinto tamaño.', [('[9]', '[9, 9]'), ('lst[1:3]', 'lst[1:2]')]),
    ])

    # 15. tuplas y conjuntos
    LST('tupla_set', 48, 62, [
        ('t = (4, 5, 6)\nprint(t[1], len(t))', 'Las tuplas se indexan como las listas.', [('t[1]', 't[0]'), ('t[1]', 't[-1]')]),
        ('a, b, c = (1, 2, 3)\nprint(b + c)', 'El desempaquetado asigna cada valor a una variable.', [('b + c', 'a + c'), ('b + c', 'a + b')]),
        ('s = {1, 2, 2, 3, 3, 3}\nprint(len(s))', 'Un conjunto descarta los elementos repetidos.', [('3, 3, 3}', '3}'), ('len(s)', 'sum(s)')]),
        ('a = {1, 2, 3}\nb = {2, 3, 4}\nprint(a & b)', '& calcula la intersección.', [('a & b', 'a | b'), ('a & b', 'a - b'), ('a & b', 'a ^ b')]),
        ('a = {1, 2, 3}\nb = {2, 3, 4}\nprint(a | b)', '| calcula la unión.', [('a | b', 'a & b'), ('a | b', 'a - b')]),
        ('a = {1, 2, 3}\nb = {2, 3, 4}\nprint(a - b)', 'a - b deja lo que está en a y no en b.', [('a - b', 'b - a'), ('a - b', 'a ^ b')]),
        ('print(len(set([5, 5, 7, 7, 7, 9])))', 'set elimina duplicados: quedan 5, 7 y 9.', [('7, 7, 7', '7, 7'), ('len(set(', 'len((')]),
        ('print(sorted(set([3, 1, 3, 2, 1])))', 'set quita duplicados y sorted devuelve una lista ordenada.', [('sorted(set(', 'list(('), ('sorted(set([3, 1, 3, 2, 1]))', 'sorted([3, 1, 3, 2, 1])')]),
        ('t = (1, 2, 3)\nt[0] = 9\nprint(t)', 'Las tuplas son inmutables: asignar un elemento da TypeError.', []) if False else
        ('t = (7,)\nprint(len(t), type(t).__name__)', 'La coma crea la tupla de un elemento: (7,).', [('(7,)', '(7)'), ('(7,)', '[7]')]),
        ('x, y = 5, 9\nx, y = y, x\nprint(x, y)', 'El intercambio por tuplas no necesita variable auxiliar.', [('x, y = y, x', 'x = y'), ('x, y = y, x', 'y = x')]),
        ('print((1, 2) + (3,))', 'Concatenar tuplas crea una nueva tupla.', [('(1, 2) + (3,)', '(1, 2) * 2'), ('(1, 2) + (3,)', '(1, 2, 3)[::-1]')]),
        ('s = {1, 2}\ns.add(2)\ns.add(5)\nprint(s)', 'add ignora los valores que ya existen.', [('s.add(5)', 's.discard(1)'), ('s.add(5)', 's.add(3)')]),
    ])

    # 16. diccionarios
    D = 'd = {"a": 1, "b": 2, "c": 3}\n'
    LST('dict', 52, 66, [
        (D + 'print(d["b"])', 'Se accede al valor mediante su clave.', [('d["b"]', 'd["a"]'), ('d["b"]', 'd["c"]')]),
        (D + 'print(d.get("z", 0))', 'get devuelve el valor por defecto si la clave no existe.', [('"z", 0', '"z", -1'), ('"z", 0', '"a", 0')]),
        (D + 'print(len(d), "a" in d)', 'in revisa claves, no valores.', [('"a" in d', '1 in d'), ('len(d)', 'len(d) + 1')]),
        (D + 'd["d"] = 4\nprint(list(d.keys()))', 'Asignar a una clave nueva la agrega al final.', [('d["d"] = 4', 'd["a"] = 4'), ('d.keys()', 'd.values()')]),
        (D + 'print(sum(d.values()))', 'values() entrega los valores para sumarlos.', [('d.values()', 'd.keys()') if False else ('sum(d.values())', 'len(d.values())'), ('sum(d.values())', 'max(d.values())')]),
        (D + 'd["a"] = 10\nprint(d)', 'Asignar a una clave existente reemplaza el valor.', [('d["a"] = 10', 'd["z"] = 10'), ('d["a"] = 10', 'd.pop("a")')]),
        (D + 'print(d.pop("b"), d)', 'pop quita la clave y devuelve su valor.', [('d.pop("b")', 'd.pop("a")'), ('d.pop("b")', 'd.get("b")')]),
        (D + 'del d["a"]\nprint(len(d))', 'del elimina la pareja clave-valor.', [('del d["a"]', 'del d["a"], d["b"]'), ('len(d)', 'len(d) + 1')]),
        (D + 'for k, v in d.items():\n    print(k * v, end=" ")', 'items entrega pares (clave, valor).', [('k * v', 'k + str(v)'), ('d.items()', 'sorted(d.items(), reverse=True)')]),
        (D + 'd.update({"b": 20, "e": 5})\nprint(d["b"], len(d))', 'update sobrescribe claves existentes y agrega las nuevas.', [('"b": 20', '"b": 2'), ('"e": 5', '"a": 5')]),
        ('c = {}\nfor ch in "mama":\n    c[ch] = c.get(ch, 0) + 1\nprint(c)', 'Patrón clásico para contar frecuencias con get.', [('"mama"', '"papa"'), ('"mama"', '"mamama"')]),
        ('d = {"x": 1}\nd2 = d\nd2["y"] = 2\nprint(len(d))', 'd2 es otro nombre para el mismo diccionario.', [('d2 = d', 'd2 = d.copy()'), ('d2["y"] = 2', 'd2["x"] = 2')]),
        ('d = {1: "a", 2: "b"}\nprint(d[2] + d[1])', 'Las claves pueden ser números.', [('d[2] + d[1]', 'd[1] + d[2]'), ('d[2] + d[1]', 'd.get(3, "z")')]),
    ])

    # 17. comprensiones
    LST('comprension', 58, 72, [
        ('print([x * 2 for x in range(5)])', 'Genera el doble de cada x de 0 a 4.', [('range(5)', 'range(1, 5)'), ('x * 2', 'x + 2'), ('x * 2', 'x ** 2')]),
        ('print([x for x in range(10) if x % 3 == 0])', 'La condición filtra los múltiplos de 3.', [('% 3 == 0', '% 3 == 1'), ('range(10)', 'range(1, 10)'), ('range(10)', 'range(9)')]),
        ('print([c.upper() for c in "abc"])', 'Aplica upper() a cada carácter.', [('c.upper()', 'c * 2'), ('"abc"', '"abcd"')]),
        ('print({x: x * x for x in range(1, 4)})', 'Comprensión de diccionario con clave y valor.', [('range(1, 4)', 'range(4)'), ('x * x', 'x + x')]),
        ('print(sum(x * x for x in range(4)))', 'Expresión generadora: 0 + 1 + 4 + 9.', [('range(4)', 'range(5)'), ('x * x', 'x * 2')]),
        ('print([(a, b) for a in range(2) for b in "xy"])', 'El for externo es a y el interno es b.', [('range(2)', 'range(3)'), ('"xy"', '"x"')]),
        ('print(len({n % 4 for n in range(20)}))', 'Un conjunto por comprensión no repite residuos.', [('% 4', '% 5'), ('range(20)', 'range(3)')]),
        ('print([x if x % 2 else 0 for x in range(5)])', 'La expresión condicional va antes del for.', [('x % 2 else 0', 'x % 2 else 1'), ('range(5)', 'range(6)')]),
        ('m = [[1, 2], [3, 4]]\nprint([f for r in m for f in r])', 'Aplana la matriz recorriendo filas y luego elementos.', [('for r in m for f in r', 'for f in m for r in f') if False else ('[f for', '[r for'), ('[[1, 2], [3, 4]]', '[[1], [3, 4]]')]),
        ('words = ["sol", "mar", "isla"]\nprint([len(w) for w in words])', 'Crea la lista de longitudes.', [('len(w)', 'len(w) - 1'), ('"isla"', '"islas"')]),
        ('print([i * j for i in range(1, 4) for j in range(1, 3)])', 'Cada i se combina con cada j.', [('range(1, 4)', 'range(1, 3)'), ('range(1, 3)', 'range(1, 4)')]),
        ('nums = [3, 8, 5, 10]\nprint([n for n in nums if n > 4 and n % 2 == 0])', 'Ambas condiciones deben cumplirse.', [('and n % 2 == 0', 'or n % 2 == 0'), ('n > 4', 'n > 8')]),
        ('print(dict(zip("abc", range(3))))', 'zip empareja letras y números.', [('range(3)', 'range(1, 4)'), ('"abc"', '"abcd"')]),
    ])

    # 18. funciones
    LST('funciones', 62, 76, [
        ('def f(a, b=2):\n    return a * b\nprint(f(5))', 'b usa su valor por defecto cuando no se pasa.', [('f(5)', 'f(5, 3)'), ('a * b', 'a + b')]),
        ('def f(a, b=2):\n    return a * b\nprint(f(b=4, a=3))', 'Los argumentos por nombre pueden ir en cualquier orden.', [('f(b=4, a=3)', 'f(3)'), ('a * b', 'a - b')]),
        ('def f(*args):\n    return len(args)\nprint(f(1, 2, 3, 4))', '*args agrupa los argumentos posicionales en una tupla.', [('1, 2, 3, 4', '1, 2'), ('len(args)', 'sum(args)')]),
        ('def f(x):\n    x = x + 1\nprint(f(5))', 'Sin return la función devuelve None.', [('x = x + 1', 'return x + 1'), ('x + 1', 'x * 2')]),
        ('def mm(a, b):\n    return b, a\nx, y = mm(1, 2)\nprint(x, y)', 'Devolver varios valores crea una tupla que se desempaqueta.', [('return b, a', 'return a, b'), ('mm(1, 2)', 'mm(2, 1)')]),
        ('def fact(n):\n    if n <= 1:\n        return 1\n    return n * fact(n - 1)\nprint(fact(5))', 'Recursión: 5! = 5 × 4 × 3 × 2 × 1.', [('fact(5)', 'fact(4)'), ('n <= 1', 'n <= 2')]),
        ('def f(n):\n    if n == 0:\n        return 0\n    return n + f(n - 1)\nprint(f(4))', 'Suma de 1 a n por recursión.', [('f(4)', 'f(5)'), ('n + f', '1 + f')]),
        ('x = 10\ndef f():\n    x = 3\n    return x\nprint(f(), x)', 'La x de la función es local y no cambia la global.', [('x = 3', 'x = 4'), ('print(f(), x)', 'print(x, f())')]),
        ('x = 10\ndef f():\n    global x\n    x += 1\nf()\nprint(x)', 'global permite modificar la variable de afuera.', [('x += 1', 'x += 5'), ('f()\nprint', 'f()\nf()\nprint')]),
        ('def f(a, b):\n    return a // b\nprint(f(17, 5), f(5, 17))', 'El orden de los argumentos posicionales importa.', [('f(17, 5), f(5, 17)', 'f(17, 5), f(17, 17)'), ('a // b', 'a % b')]),
        ('def sq(n):\n    return n * n\nprint(sq(sq(2)))', 'Primero se evalúa la llamada interna: sq(2) = 4, luego sq(4).', [('sq(sq(2))', 'sq(2)'), ('sq(sq(2))', 'sq(sq(3))')]),
        ('def f(n):\n    return n if n < 2 else f(n - 1) + f(n - 2)\nprint(f(7))', 'Fibonacci recursivo: f(7) = 13.', [('f(7)', 'f(6)'), ('f(7)', 'f(8)')]),
        ('def f(a, *, b=1):\n    return a + b\nprint(f(1, b=5))', 'Tras * los parámetros son solo por nombre.', [('b=5', 'b=2'), ('a + b', 'a * b')]),
    ])

    # 19. lambda / map / filter / sorted
    LST('lambda', 66, 80, [
        ('f = lambda x: x + 3\nprint(f(4))', 'lambda crea una función anónima de una expresión.', [('x + 3', 'x * 3'), ('f(4)', 'f(5)')]),
        ('print(list(map(lambda x: x * x, [1, 2, 3])))', 'map aplica la función a cada elemento.', [('x * x', 'x + x'), ('[1, 2, 3]', '[2, 3, 4]')]),
        ('print(list(filter(lambda x: x > 2, [1, 2, 3, 4])))', 'filter conserva los elementos para los que la función da True.', [('x > 2', 'x >= 2'), ('x > 2', 'x < 3')]),
        ('print(sorted(["pera", "uva", "kiwi"], key=len))', 'key=len ordena por longitud de cada texto.', [('key=len', 'reverse=True'), ('key=len', 'key=lambda s: s[-1]')]),
        ('print(sorted([3, 1, 2], reverse=True))', 'reverse=True ordena de mayor a menor.', [('reverse=True', 'key=lambda x: -x * 0'), ('[3, 1, 2]', '[3, 1, 20]')]),
        ('print(max([3, 9, 4], key=lambda x: -x))', 'La clave negativa hace que gane el menor.', [('-x', 'x'), ('max(', 'min(')]),
        ('print(any(x > 5 for x in [1, 2, 7]), all(x > 5 for x in [1, 2, 7]))', 'any pide al menos uno; all pide todos.', [('any(x > 5', 'all(x > 5'), ('[1, 2, 7]', '[6, 7, 8]')]),
        ('print(list(zip([1, 2, 3], "ab")))', 'zip se detiene en la secuencia más corta.', [('"ab"', '"abc"'), ('[1, 2, 3]', '[1]')]),
        ('print(list(enumerate("xy", start=1)))', 'enumerate entrega pares (índice, elemento).', [('start=1', 'start=0'), ('"xy"', '"xyz"')]),
        ('from functools import reduce\nprint(reduce(lambda a, b: a * b, [1, 2, 3, 4]))', 'reduce acumula el producto: 1×2×3×4.', [('a * b', 'a + b'), ('[1, 2, 3, 4]', '[1, 2, 3]')]),
        ('words = ["b", "aa", "c"]\nprint(sorted(words, key=lambda w: (len(w), w)))', 'Se ordena por longitud y, en empate, alfabéticamente.', [('(len(w), w)', '(w, len(w))'), ('(len(w), w)', '(-len(w), w)')]),
        ('print(list(map(str.upper, ["a", "b"])))', 'Un método también puede pasarse como función a map.', [('str.upper', 'str.title'), ('["a", "b"]', '["a"]')]),
        ('print(sum(map(int, "1234")))', 'map(int, ...) convierte cada carácter en entero.', [('"1234"', '"12345"'), ('sum(', 'max(')]),
    ])

    # 20. clases
    LST('clases', 70, 84, [
        ('class A:\n    def __init__(self, n):\n        self.n = n\na = A(5)\nprint(a.n)', '__init__ inicializa el atributo del objeto.', [('A(5)', 'A(6)'), ('print(a.n)', 'print(a.n + 1)')]),
        ('class P:\n    def __init__(self, x):\n        self.x = x\n    def dup(self):\n        return self.x * 2\nprint(P(4).dup())', 'Un método usa self para leer los atributos.', [('self.x * 2', 'self.x + 2'), ('P(4)', 'P(7)')]),
        ('class C:\n    n = 0\n    def __init__(self):\n        C.n += 1\nC(); C(); C()\nprint(C.n)', 'Un atributo de clase se comparte entre todas las instancias.', [('C(); C(); C()', 'C(); C()'), ('C.n += 1', 'C.n += 2')]),
        ('class A:\n    def hi(self):\n        return "A"\nclass B(A):\n    pass\nprint(B().hi())', 'B hereda el método hi de A.', [('return "A"', 'return "B"'), ('class B(A)', 'class B')]) if False else
        ('class A:\n    def hi(self):\n        return "A"\nclass B(A):\n    def hi(self):\n        return "B"\nprint(B().hi())', 'B redefine hi: se usa la versión de la subclase.', [('return "B"', 'return super().hi()'), ('B().hi()', 'A().hi()')]),
        ('class A:\n    def hi(self):\n        return "A"\nclass B(A):\n    def hi(self):\n        return super().hi() + "B"\nprint(B().hi())', 'super() llama al método de la clase padre.', [('super().hi() + "B"', '"B" + super().hi()'), ('B().hi()', 'A().hi()')]),
        ('class V:\n    def __init__(self, a):\n        self.a = a\n    def __str__(self):\n        return f"V({self.a})"\nprint(V(3))', '__str__ define cómo se muestra el objeto con print.', [('V({self.a})', 'V{self.a}'), ('V(3)', 'V(8)')]),
        ('class A:\n    def __init__(self):\n        self.l = []\na, b = A(), A()\na.l.append(1)\nprint(len(b.l))', 'Cada instancia tiene su propia lista.', [('self.l = []', 'pass') if False else ('a.l.append(1)', 'a.l.append(1); b.l.append(2)'), ('len(b.l)', 'len(a.l)')]),
        ('class A:\n    l = []\na, b = A(), A()\na.l.append(1)\nprint(len(b.l))', 'La lista es un atributo de clase compartido por todas las instancias.', [('l = []', 'l = [0]'), ('len(b.l)', 'len(a.l) - 1')]),
        ('class Cta:\n    def __init__(self, s):\n        self.s = s\n    def dep(self, m):\n        self.s += m\n        return self\nprint(Cta(10).dep(5).dep(3).s)', 'Devolver self permite encadenar llamadas.', [('dep(5).dep(3)', 'dep(5)'), ('Cta(10)', 'Cta(0)')]),
        ('class A:\n    @staticmethod\n    def f(x):\n        return x * 2\nprint(A.f(6))', 'Un método estático no recibe self ni la instancia.', [('x * 2', 'x * 3'), ('A.f(6)', 'A.f(7)')]),
        ('class A:\n    def __init__(self):\n        self.v = 1\nclass B(A):\n    def __init__(self):\n        super().__init__()\n        self.v += 1\nprint(B().v)', 'El constructor de B llama primero al de A y luego suma 1.', [('self.v += 1', 'self.v += 2'), ('super().__init__()\n', '')]),
        ('class A:\n    def __len__(self):\n        return 7\nprint(len(A()))', '__len__ permite que len() funcione con el objeto.', [('return 7', 'return 8'), ('len(A())', 'len(A()) + 1')]),
    ])

    # 21. excepciones (flujo)
    LST('excepciones', 66, 80, [
        ('try:\n    print(10 / 0)\nexcept ZeroDivisionError:\n    print("no")', 'La división entre cero lanza ZeroDivisionError y se captura.', [('10 / 0', '10 / 2'), ('"no"', '"sí"')]),
        ('try:\n    x = int("abc")\nexcept ValueError:\n    x = -1\nprint(x)', 'int("abc") lanza ValueError y se asigna el valor de respaldo.', [('"abc"', '"12"'), ('x = -1', 'x = 0')]),
        ('try:\n    print("a", end=" ")\nfinally:\n    print("b")', 'finally se ejecuta siempre.', [('"a"', '"z"'), ('print("b")', 'print("c")')]),
        ('try:\n    print("a", end=" ")\nexcept Exception:\n    print("b", end=" ")\nelse:\n    print("c", end=" ")\nfinally:\n    print("d")', 'else solo corre si no hubo excepción.', [('print("a", end=" ")', '1 / 0'), ('else:', 'else:')]),
        ('def f():\n    try:\n        return 1\n    finally:\n        print("f", end=" ")\nprint(f())', 'finally se ejecuta incluso antes de que el return salga.', [('return 1', 'return 2'), ('print("f", end=" ")', 'print("g", end=" ")')]),
        ('try:\n    l = [1, 2]\n    print(l[5])\nexcept IndexError:\n    print("fuera")', 'Un índice inexistente lanza IndexError.', [('l[5]', 'l[1]'), ('"fuera"', '"dentro"')]),
        ('try:\n    d = {"a": 1}\n    print(d["b"])\nexcept KeyError as e:\n    print(e)', 'KeyError muestra la clave que no se encontró.', [('d["b"]', 'd["a"]'), ('"b"', '"c"')]),
        ('def f(x):\n    if x < 0:\n        raise ValueError("neg")\n    return x\ntry:\n    f(-1)\nexcept ValueError as e:\n    print(e)', 'raise lanza la excepción con un mensaje.', [('f(-1)', 'f(-5)'), ('"neg"', '"bad"')]),
        ('try:\n    try:\n        1 / 0\n    except ValueError:\n        print("v")\nexcept ZeroDivisionError:\n    print("z")', 'El except interno no coincide, así que la excepción sube al externo.', [('ZeroDivisionError:', 'ZeroDivisionError:\n        print("z2")') if False else ('"z"', '"zz"'), ('1 / 0', 'int("x")')]),
        ('def f():\n    try:\n        raise KeyError\n    except KeyError:\n        return "k"\n    finally:\n        print("fin", end=" ")\nprint(f())', 'finally corre antes de entregar el valor devuelto.', [('"k"', '"j"'), ('"fin"', '"cierre"')]),
    ])
    for i in range(1):
        pass

    # 22. tipos de error
    ERRS = ['NameError', 'TypeError', 'IndexError', 'KeyError', 'ZeroDivisionError', 'ValueError', 'AttributeError', 'SyntaxError', 'IndentationError', 'RecursionError']
    erows = [
        ('print(total)', 'total no fue definida antes de usarse.', 12),
        ('print("edad: " + 5)', 'No se puede concatenar str con int sin convertir.', 14),
        ('l = [1, 2, 3]\nprint(l[3])', 'El último índice válido es 2.', 15),
        ('d = {"a": 1}\nprint(d["b"])', 'La clave "b" no existe en el diccionario.', 16),
        ('print(5 % 0)', 'El residuo con divisor cero también falla.', 17),
        ('n = int("3.5")', 'int no acepta textos con punto decimal.', 18),
        ('x = 5\nx.append(3)', 'Un int no tiene el método append.', 19),
        ('if 3 > 2\n    print("ok")', 'Falta el signo de dos puntos tras la condición.', 20),
        ('def f():\nprint("hola")', 'El cuerpo de la función no está indentado.', 21),
        ('def f(n):\n    return f(n + 1)\nf(0)', 'La recursión sin caso base supera el límite de profundidad.', 22),
        ('print(len(5))', 'len necesita un objeto con longitud, no un int.', 23),
        ('t = (1, 2)\nt[0] = 5', 'Las tuplas no permiten asignación de elementos.', 24),
        ('s = "hola"\nprint(s.push("a"))', 'Los str no tienen un método llamado push.', 25),
        ('print(int(None))', 'int(None) no es una conversión válida (TypeError).', 26),
        ('import modulo_inexistente_xyz', 'El módulo no existe.', None),
    ]
    for i, (c, e, _) in enumerate(erows):
        if i == 14:
            B.add('errores', 58, '¿Qué error produce este código en Python al ejecutarse?\n' + c, 'ModuleNotFoundError', ['NameError', 'ImportWarning', 'FileNotFoundError'], ['ModuleNotFoundError'], e)
            continue
        ERR(B, 'errores', spread(i, 14, 40, 62), 'py', c, ERRS, expl=e)

    # 23. alias, copia, mutabilidad
    LST('alias', 72, 86, [
        ('a = [1, 2]\nb = a\nb.append(3)\nprint(a)', 'b y a apuntan a la misma lista.', [('b = a', 'b = a.copy()'), ('b.append(3)', 'b.append(4)')]),
        ('a = [1, 2]\nb = a.copy()\nb.append(3)\nprint(a)', 'copy crea una lista nueva e independiente.', [('a.copy()', 'a'), ('b.append(3)', 'a.append(3)')]),
        ('a = [1, 2]\nb = a[:]\nb[0] = 9\nprint(a, b)', 'La rebanada completa copia la lista.', [('a[:]', 'a'), ('b[0] = 9', 'b[1] = 9')]),
        ('a = [[0] * 2] * 2\na[0][0] = 1\nprint(a)', 'Las dos filas son la misma lista repetida.', [('[[0] * 2] * 2', '[[0] * 2 for _ in range(2)]'), ('a[0][0] = 1', 'a[1][1] = 1')]),
        ('a = [[0] * 2 for _ in range(2)]\na[0][0] = 1\nprint(a)', 'La comprensión crea una fila distinta en cada vuelta.', [('for _ in range(2)]', '] * 2'), ('a[0][0] = 1', 'a[1][0] = 1')]),
        ('a = [1, 2, 3]\nb = [1, 2, 3]\nprint(a == b, a is b)', '== compara contenido; is compara identidad.', [('a is b', 'a is a'), ('b = [1, 2, 3]', 'b = a')]),
        ('def f(l):\n    l.append(0)\nx = [1]\nf(x)\nprint(x)', 'La función recibe la referencia y modifica la lista original.', [('l.append(0)', 'l = l + [0]'), ('x = [1]', 'x = []')]),
        ('def f(l):\n    l = l + [0]\nx = [1]\nf(x)\nprint(x)', 'l + [0] crea una lista nueva; la original queda igual.', [('l = l + [0]', 'l += [0]'), ('x = [1]', 'x = [2]')]),
        ('def f(x, l=[]):\n    l.append(x)\n    return l\nf(1)\nprint(f(2))', 'El valor por defecto mutable se crea una sola vez y se comparte.', [('f(1)\n', ''), ('l=[]', 'l=None) if False else (')]) if False else
        ('def f(x, l=[]):\n    l.append(x)\n    return l\nf(1)\nprint(f(2))', 'El valor por defecto mutable se crea una sola vez y se comparte.', [('f(1)\nprint(f(2))', 'print(f(2))'), ('f(1)\n', 'f(1)\nf(1)\n')]),
        ('s = "hola"\nt = s.upper()\nprint(s, t)', 'Los str son inmutables: upper devuelve uno nuevo.', [('s.upper()', 's.lower()'), ('print(s, t)', 'print(t, s)')]),
        ('a = 5\nb = a\nb += 1\nprint(a, b)', 'Los números son inmutables: b += 1 crea un valor nuevo.', [('b += 1', 'b += 2'), ('print(a, b)', 'print(b, a)')]),
        ('import copy\na = [[1], [2]]\nb = copy.deepcopy(a)\nb[0].append(9)\nprint(a)', 'deepcopy copia también las listas internas.', [('copy.deepcopy(a)', 'a.copy()'), ('b[0].append(9)', 'a[0].append(9)')]),
        ('a = [[1], [2]]\nb = a.copy()\nb[0].append(9)\nprint(a)', 'copy es superficial: las listas internas se comparten.', [('a.copy()', 'a[:] + []') if False else ('b[0].append(9)', 'b.append(9)'), ('a.copy()', 'list(map(list, a))')]),
    ])

    # 24. generadores / iteradores
    LST('generadores', 76, 90, [
        ('def g():\n    yield 1\n    yield 2\nprint(list(g()))', 'yield produce valores uno a uno.', [('yield 2', 'yield 3'), ('list(g())', 'sum(g())')]),
        ('def g():\n    yield 1\n    yield 2\nx = g()\nprint(next(x), next(x))', 'Cada next reanuda el generador hasta el siguiente yield.', [('next(x), next(x)', 'next(x), next(g())'), ('yield 2', 'yield 5')]),
        ('def cuenta(n):\n    i = 0\n    while i < n:\n        yield i\n        i += 1\nprint(list(cuenta(4)))', 'Un generador con while produce 0, 1, 2 y 3.', [('i < n', 'i <= n'), ('cuenta(4)', 'cuenta(3)')]),
        ('g = (x * x for x in range(4))\nprint(next(g), next(g), sum(g))', 'sum consume lo que queda del generador (4 + 9).', [('range(4)', 'range(5)'), ('next(g), next(g)', 'next(g)')]),
        ('g = (x for x in range(3))\nprint(list(g), list(g))', 'Un generador se agota: la segunda lista queda vacía.', [('range(3)', 'range(2)'), ('(x for x in', '[x for x in')]),
        ('it = iter([10, 20])\nprint(next(it), next(it))', 'iter crea un iterador sobre la lista.', [('[10, 20]', '[10, 30]'), ('next(it), next(it)', 'next(it)')]),
        ('def g():\n    n = 0\n    while True:\n        yield n\n        n += 2\nx = g()\nnext(x); next(x)\nprint(next(x))', 'Un generador infinito entrega 0, 2, 4...', [('n += 2', 'n += 3'), ('next(x); next(x)', 'next(x)')]),
        ('def g():\n    yield from [1, 2]\n    yield 3\nprint(list(g()))', 'yield from cede cada elemento del iterable.', [('[1, 2]', '[5, 6]'), ('yield 3', 'yield 4')]),
        ('print(list(reversed(range(3))), list(range(3))[::-1])', 'reversed devuelve un iterador; list lo materializa.', [('range(3)', 'range(4)')]),
        ('import itertools\nprint(list(itertools.islice(itertools.count(5), 3)))', 'count genera infinitamente; islice toma 3 elementos.', [('count(5)', 'count(2)'), ('), 3)', '), 4)')]),
        ('g = (c for c in "abc")\nfor x in g:\n    print(x, end="")\nprint(sum(1 for _ in g))', 'Tras el for el generador queda agotado, por eso cuenta 0.', [('"abc"', '"abcd"'), ('end=""', 'end="-"')]),
    ])

    # 25. closures, decoradores, scope
    LST('closures', 80, 94, [
        ('def mk(n):\n    def f(x):\n        return x + n\n    return f\nprint(mk(3)(4))', 'La función interna recuerda n (cierre).', [('mk(3)(4)', 'mk(4)(3)') if False else ('mk(3)(4)', 'mk(5)(4)'), ('x + n', 'x * n')]),
        ('def cont():\n    c = 0\n    def inc():\n        nonlocal c\n        c += 1\n        return c\n    return inc\nf = cont()\nf(); f()\nprint(f())', 'nonlocal permite modificar c, que vive en la función externa.', [('f(); f()', 'f()'), ('c += 1', 'c += 2')]),
        ('def deco(fn):\n    def w():\n        return fn() + 1\n    return w\n@deco\ndef a():\n    return 5\nprint(a())', '@deco equivale a a = deco(a).', [('+ 1', '+ 2'), ('return 5', 'return 6')]),
        ('def deco(fn):\n    def w(*a):\n        return fn(*a) * 2\n    return w\n@deco\ndef s(x, y):\n    return x + y\nprint(s(1, 2))', 'El wrapper duplica el resultado de la función decorada.', [('* 2', '* 3'), ('s(1, 2)', 's(2, 3)')]),
        ('fs = [lambda: i for i in range(3)]\nprint([f() for f in fs])', 'Las tres lambdas ven la misma i, que termina valiendo 2.', [('range(3)', 'range(4)'), ('lambda: i', 'lambda i=i: i')]),
        ('fs = [lambda i=i: i for i in range(3)]\nprint([f() for f in fs])', 'El valor por defecto captura i en cada vuelta.', [('lambda i=i: i', 'lambda: i'), ('range(3)', 'range(2)')]),
        ('x = "g"\ndef f():\n    x = "l"\n    def h():\n        return x\n    return h()\nprint(f(), x)', 'h ve la x de f (local de la función envolvente), no la global.', [('x = "l"', 'x = "m"'), ('print(f(), x)', 'print(x, f())')]),
        ('def f():\n    print(x)\n    x = 1\nf()', '', []) if False else
        ('def mult(n):\n    return lambda x: x * n\nd, t = mult(2), mult(3)\nprint(d(5), t(5))', 'Cada cierre conserva su propio n.', [('mult(2), mult(3)', 'mult(3), mult(2)'), ('x * n', 'x + n')]),
        ('def reg(fn):\n    reg.n = getattr(reg, "n", 0) + 1\n    return fn\n@reg\ndef a(): pass\n@reg\ndef b(): pass\nprint(reg.n)', 'Cada uso de @reg ejecuta reg una vez.', [('@reg\ndef b(): pass\n', ''), ('reg.n + 1', 'reg.n + 2')]) if False else
        ('def deco(fn):\n    print("D", end=" ")\n    return fn\n@deco\ndef f():\n    print("F")\nf()\nf()', 'El decorador corre una vez al definir; la función, en cada llamada.', [('f()\nf()', 'f()'), ('"D"', '"E"')]),
        ('def f(n=[]):\n    n = n + [1]\n    return len(n)\nf(); f()\nprint(f())', 'n + [1] crea una lista nueva, así que no se acumula.', [('n = n + [1]', 'n.append(1)'), ('f(); f()', 'f()')]),
        ('def a():\n    x = 1\n    def b():\n        x = 2\n    b()\n    return x\nprint(a())', 'Sin nonlocal, b crea su propia x local.', [('x = 2\n', 'nonlocal x\n        x = 2\n'), ('x = 1', 'x = 3')]),
    ])


def build3(B):
    pass

_b1 = build
def build(B):
    _b1(B)
    build2(B)
    build3(B)
