from common import *
R = random.Random(202)
ri = R.randint
def X(src, d, top='', **k): return code('cpp', 'cpp', src, d, top=top, **k)
WS = ['Hola', 'Mundo', 'C++', 'codigo', 'hola mundo', 'Adios', 'Programar', 'Bienvenido']

def f1():
    w = R.choice(WS); a, b = ri(2, 30), ri(2, 9); k = R.randint(0, 11)
    forms = [
        ('cout << "%s";' % w, w, 0, [w.upper(), '"%s"' % w], 'cout imprime el texto sin las comillas.'),
        ('cout << %d + %d;' % (a, b), str(a + b), 3, ['%d%d' % (a, b), str(a * b)], '<< envía el resultado de la suma.'),
        ('cout << %d / %d;' % (a, b), str(a // b), 12, [str(round(a / b, 2)), str(a % b)], 'Con dos enteros, / hace división entera.'),
        ('cout << %d %% %d;' % (a, b), str(a % b), 14, [str(a // b), str(b)], '% devuelve el residuo.'),
        ('cout << %d / %d.0;' % (a, b), '%g' % (a / b), 22, [str(a // b), '%g' % (a / b + 1)], 'Si uno de los operandos es decimal, la división es decimal.'),
        ('cout << "%s" << " " << %d;' % (w, a), '%s %d' % (w, a), 8, ['%s%d' % (w, a), '%d %s' % (a, w)], 'Se encadenan varias salidas con <<.'),
        ('cout << %d << %d;' % (a, b), '%d%d' % (a, b), 10, ['%d %d' % (a, b), str(a + b)], 'cout no agrega espacios entre valores.'),
        ('cout << (%d > %d);' % (a, b), str(int(a > b)), 18, ['true' if a > b else 'false', str(int(a <= b))], 'Un bool se imprime como 1 o 0 por defecto.'),
        ('cout << \'A\' + %d;' % ri(0, 5), None, 30, [], 'Sumar a un char produce un entero (su código ASCII).'),
        ('cout << (char)(\'a\' + %d);' % ri(0, 5), None, 34, [], 'El cast a char muestra la letra correspondiente.'),
        ('cout << %d << "\\n" << %d;' % (a, b), '%d %d' % (a, b), 12, ['%d%d' % (a, b), '%d' % (a + b)], '"\\n" es un salto de línea.'),
        ('cout << 2 * %d + %d;' % (b, a), str(2 * b + a), 8, [str(2 * (b + a)), str(2 * b)], 'La multiplicación va antes que la suma.'),
    ]
    s, ans, d, al, why = forms[k]
    if ans is None: al = []
    return X(s, d + ri(0, 4), alts=al, why=why)
fam(40, f1)

def f2():
    a, b = ri(5, 30), ri(2, 7); k = R.randint(0, 5)
    forms = [
        ('int a = %d, b = %d;\ncout << a / b;' % (a, b), 14, [str(round(a / b, 1)), str(a % b)], 'int / int es división entera.'),
        ('double x = %d;\ncout << x / %d;' % (a, b), 20, [str(a // b)], 'x es double, así que la división es decimal.'),
        ('int x = %d;\nx += %d;\nx *= 2;\ncout << x;' % (a, b), 14, [str(a + b), str(a * 2 + b)], 'Primero x += %d y luego x *= 2.' % b),
        ('int x = %d;\nx = x %% %d;\ncout << x;' % (a, b), 16, [str(a // b), str(a)], '% deja el residuo.'),
        ('int n = %d;\nn /= %d;\ncout << n;' % (a, b), 18, [str(round(a / b, 1)), str(a % b)], '/= con enteros descarta decimales.'),
        ('int a = %d, b = %d;\nint t = a;\na = b;\nb = t;\ncout << a << " " << b;' % (a, b), 26, ['%d %d' % (a, b), '%d %d' % (a, a), '%d %d' % (b, b)], 'Se intercambian los valores usando una variable temporal.'),
    ]
    s, d, al, why = forms[k]
    return X(s, d + ri(0, 5), alts=al, why=why)
fam(22, f2)

def f3():
    i = ri(1, 9); k = R.randint(0, 5)
    forms = [
        ('int i = %d;\ncout << i++ << " " << i;' % i, 44, ['%d %d' % (i + 1, i + 1), '%d %d' % (i + 1, i), '%d %d' % (i, i)], 'i++ entrega el valor y luego incrementa.'),
        ('int i = %d;\ncout << ++i << " " << i;' % i, 46, ['%d %d' % (i, i + 1), '%d %d' % (i, i), '%d %d' % (i + 1, i)], '++i incrementa primero y luego entrega el valor.'),
        ('int i = %d;\ni++;\ni++;\ncout << i;' % i, 20, [str(i + 1), str(i + 3), str(i)], 'Cada i++ suma 1.'),
        ('int i = %d;\nint j = i--;\ncout << i << " " << j;' % i, 54, ['%d %d' % (i, i - 1), '%d %d' % (i, i), '%d %d' % (i - 1, i - 1)], 'j recibe el valor anterior y luego i disminuye.'),
        ('int a = %d;\nint b = a++ + 2;\ncout << a << " " << b;' % i, 58, ['%d %d' % (i, i + 2), '%d %d' % (i + 1, i + 3), '%d %d' % (i + 2, i + 2)], 'Se usa a (valor anterior) y después se incrementa.'),
        ('int x = %d;\nx -= 3;\nx++;\ncout << x;' % (i + 5), 24, [str(i + 2), str(i + 3), str(i + 1)], 'x -= 3 resta y x++ suma 1.'),
    ]
    s, d, al, why = forms[k]
    return X(s, d + ri(0, 4), alts=al, why=why)
fam(14, f3)

def f4():
    x = ri(1, 20); m = ri(1, 20); k = R.randint(0, 4)
    forms = [
        ('int x = %d;\nif (x > %d) cout << "A";\nelse cout << "B";' % (x, m), 16, ['B' if x > m else 'A', 'AB', '0'], 'Se evalúa x > %d con x = %d.' % (m, x)),
        ('int x = %d;\ncout << (x %% 2 == 0 ? "par" : "impar");' % x, 24, ['impar' if x % 2 == 0 else 'par', '1', '0'], 'El operador ternario elige según la condición.'),
        ('int x = %d;\nif (x < %d) cout << "A";\nelse if (x < %d) cout << "B";\nelse cout << "C";' % (x, m, m + 8), 30, ['A', 'B', 'C'], 'Se ejecuta la primera condición verdadera.'),
        ('int d = %d;\nswitch (d) {\n  case 1: cout << "uno"; break;\n  case 2: cout << "dos"; break;\n  default: cout << "otro";\n}' % ri(1, 3), 34, ['uno', 'dos', 'otro'], 'switch salta al case que coincide.'),
        ('int d = %d;\nswitch (d) {\n  case 1: cout << "a";\n  case 2: cout << "b"; break;\n  case 3: cout << "c";\n}' % ri(1, 3), 62, ['a', 'b', 'ab', 'c', 'abc'], 'Sin break, la ejecución continúa en el siguiente case.'),
    ]
    s, d, al, why = forms[k]
    return X(s, d + ri(0, 5), alts=al, why=why)
fam(18, f4)

def f5():
    n = ri(3, 7); k = R.randint(0, 8); m = ri(2, 4)
    forms = [
        ('for (int i = 0; i < %d; i++)\n    cout << i << " ";' % n, 14, [], 'Cuenta de 0 a %d (el límite no se incluye).' % (n - 1)),
        ('for (int i = 1; i <= %d; i++)\n    cout << i << " ";' % n, 14, [], 'Con <= el límite sí se incluye.'),
        ('int s = 0;\nfor (int i = 1; i <= %d; i++) s += i;\ncout << s;' % n, 22, [str(sum(range(1, n))), str(sum(range(0, n + 2)))], 'Suma de 1 hasta %d.' % n),
        ('int i = 0;\nwhile (i < %d) i += %d;\ncout << i;' % (n * 2, m), 24, [], 'El while termina cuando i ya no es menor que %d.' % (n * 2)),
        ('int i = %d;\ndo { cout << i; i++; } while (i < %d);' % (n + 2, n), 40, [], 'do-while ejecuta el cuerpo al menos una vez.'),
        ('for (int i = 0; i < %d; i++) {\n    if (i == %d) break;\n    cout << i;\n}' % (n + 3, m), 32, [], 'break sale del bucle.'),
        ('for (int i = 0; i < %d; i++) {\n    if (i == %d) continue;\n    cout << i;\n}' % (n + 1, m - 1), 36, [], 'continue salta la iteración actual.'),
        ('int c = 0;\nfor (int i = 0; i < %d; i++)\n    for (int j = 0; j < %d; j++) c++;\ncout << c;' % (n, m), 46, [str(n + m), str(n * m + 1), str(n * m - 1)], 'El bucle interno se repite por cada vuelta del externo: %d × %d.' % (n, m)),
        ('for (int i = %d; i > 0; i -= 2)\n    cout << i << " ";' % (n + 2), 28, [], 'Cuenta hacia atrás de 2 en 2.'),
    ]
    s, d, al, why = forms[k]
    return X(s, d + ri(0, 6), alts=al, why=why)
fam(24, f5)

def f6():
    a = [ri(1, 9) for _ in range(5)]; s = R.choice(['hola', 'mundo', 'codigo', 'programa']); k = R.randint(0, 9); i = ri(0, 4)
    arr = ', '.join(map(str, a))
    forms = [
        ('int a[] = {%s};\ncout << a[%d];' % (arr, i), str(a[i]), 8, [str(a[(i + 1) % 5]), str(i)], 'Los índices empiezan en 0.'),
        ('int a[] = {%s};\ncout << sizeof(a) / sizeof(a[0]);' % arr, '5', 40, ['20', '4', '6'], 'Tamaño total entre tamaño de un elemento = cantidad.'),
        ('int a[] = {%s};\nint s = 0;\nfor (int i = 0; i < 5; i++) s += a[i];\ncout << s;' % arr, str(sum(a)), 24, [str(sum(a) - a[0]), str(sum(a) + 1)], 'Recorre y suma todos los elementos.'),
        ('vector<int> v = {%s};\nv.push_back(%d);\ncout << v.size();' % (arr, ri(1, 9)), '6', 22, ['5', '7', '0'], 'push_back agrega un elemento.'),
        ('vector<int> v = {%s};\ncout << v.back();' % arr, str(a[-1]), 20, [str(a[0]), str(a[-2])], 'back() es el último elemento.'),
        ('string s = "%s";\ncout << s.size();' % s, str(len(s)), 10, [str(len(s) - 1), str(len(s) + 1)], 'size() devuelve el largo.'),
        ('string s = "%s";\ncout << s[0];' % s, s[0], 10, [s[1], s[-1]], 's[0] es el primer carácter.'),
        ('string s = "%s";\ncout << s.substr(1, 3);' % s, s[1:4], 36, [s[0:3], s[1:3] if len(s) > 3 else s[2:5], s[1:5]], 'substr(pos, largo) toma "largo" caracteres desde pos.'),
        ('string a = "%s", b = "%s";\ncout << a + " " + b;' % (s, 'ok'), s + ' ok', 18, [s + 'ok', 'ok ' + s], '+ concatena strings.'),
        ('string s = "%s";\nreverse(s.begin(), s.end());\ncout << s;' % s, s[::-1], 46, [s.upper(), s[1:]], 'reverse invierte el texto.'),
    ]
    s2, ans, d, al, why = forms[k]
    return X(s2, d + ri(0, 4), alts=al, why=why)
fam(30, f6)

def f7():
    x = ri(2, 9); y = ri(10, 20); k = R.randint(0, 6)
    forms = [
        ('int x = %d;\nint *p = &x;\ncout << *p;' % x, 58, [], '*p lee el valor al que apunta p.'),
        ('int x = %d;\nint *p = &x;\n*p = %d;\ncout << x;' % (x, y), 62, [str(x), '0'], 'Al escribir por el puntero se modifica x.'),
        ('int x = %d;\nint &r = x;\nr++;\ncout << x;' % x, 66, [str(x), str(x + 2)], 'r es otro nombre (referencia) de x.'),
        ('int a[] = {%d, %d, %d};\nint *p = a;\ncout << *(p + 1);' % (x, y, x + y), 72, [str(x), str(x + y)], 'p + 1 apunta al segundo elemento.'),
        ('int a = %d, b = %d;\nint *p = &a, *q = &b;\ncout << *p + *q;' % (x, y), 62, [str(x), str(y), str(x * y)], 'Se suman los valores apuntados.'),
        ('int x = %d;\nint *p = &x;\nint **pp = &p;\ncout << **pp;' % y, 84, [], 'Se desreferencia dos veces hasta llegar a x.'),
        ('int a[] = {%d, %d, %d};\nint *p = a + 2;\ncout << *p << " " << p[-1];' % (x, y, x + y), 88, [], 'p apunta al tercer elemento y p[-1] al segundo.'),
    ]
    s, d, al, why = forms[k]
    return X(s, d + ri(0, 6), alts=al, why=why)
fam(18, f7)

def f8():
    n = ri(2, 6); a = ri(2, 9); k = R.randint(0, 6)
    forms = [
        ('cout << dbl(%d);' % a, 'int dbl(int x) { return x * 2; }', 30, [str(a + 2), str(a * a)], 'La función devuelve el doble.'),
        ('cout << suma(%d, %d);' % (a, n), 'int suma(int a, int b) { return a + b; }', 28, [str(a * n)], 'Suma sus dos parámetros.'),
        ('int x = %d;\nsube(x);\ncout << x;' % a, 'void sube(int n) { n++; }', 52, [str(a + 1)], 'Se pasa una copia: x no cambia.'),
        ('int x = %d;\nsube(x);\ncout << x;' % a, 'void sube(int &n) { n++; }', 60, [str(a)], 'Se pasa por referencia: x cambia.'),
        ('cout << fact(%d);' % n, 'int fact(int n) { return n <= 1 ? 1 : n * fact(n - 1); }', 68, [], 'Factorial recursivo.'),
        ('cout << f(%d);' % (n + 2), 'int f(int n) { if (n < 2) return n; return f(n - 1) + f(n - 2); }', 82, [], 'Es la sucesión de Fibonacci recursiva.'),
        ('cout << cuadrado(%d) + 1;' % a, 'int cuadrado(int x) { return x * x; }', 32, [str(a * a), str((a + 1) * (a + 1))], 'Primero se calcula el cuadrado y luego se suma 1.'),
    ]
    s, top, d, al, why = forms[k]
    return X(s, d + ri(0, 5), top=top, alts=al, why=why)
fam(22, f8)

def f9():
    forms = [
        ('cout << sizeof(int);', 38, ['2', '8', '1'], 'En la mayoría de los sistemas modernos int ocupa 4 bytes.'),
        ('cout << sizeof(char);', 36, ['2', '4', '8'], 'char siempre mide 1 byte.'),
        ('cout << sizeof(double);', 40, ['4', '16', '2'], 'double ocupa normalmente 8 bytes.'),
        ('cout << (int)3.9;', 40, ['4', '3.9', '3.0'], 'El cast a int trunca los decimales.'),
        ('cout << -7 / 2;', 46, ['-4', '-3.5', '3'], 'La división entera trunca hacia cero.'),
        ('cout << -7 % 3;', 52, ['2', '1', '-2'], 'El residuo toma el signo del dividendo.'),
        ('cout << static_cast<double>(7) / 2;', 50, ['3', '4', '3.50'], 'Convertir uno a double hace decimal la división.'),
        ('cout << (5 > 3) + (2 > 8);', 48, ['2', '0', 'true'], 'true vale 1 y false vale 0.'),
        ('cout << (1 && 0) << (1 || 0);', 50, ['11', '00', '01 '], '&& da 0 y || da 1.'),
        ('cout << 7 / 2 * 2.0;', 56, ['7', '3', '3.5'], '7/2 es 3 (enteros) y luego se multiplica por 2.0.'),
        ('cout << 10 / 4 << " " << 10 %% 4;'.replace('%%', '%'), 40, ['2.5 2', '2 0', '3 2'], 'División entera y residuo.'),
        ('char c = \'A\';\nc += 2;\ncout << c;', 50, ['A', '67', 'C2'], 'Sumar a un char avanza en la tabla ASCII.'),
        ('cout << (int)\'a\';', 44, ['a', '65', '1'], 'El código ASCII de a es 97.'),
        ('cout << 1 / 2 + 1 / 2.0;', 60, ['1', '0', '1.5'], '1/2 es 0 y 1/2.0 es 0.5.'),
    ]
    s, d, al, why = R.choice(forms)
    return X(s, d + ri(0, 2), alts=al, why=why)
fam(14, f9)

def f10():
    a, b = ri(1, 9), ri(1, 9); k = R.randint(0, 3)
    forms = [
        ('Punto p = {%d, %d};\ncout << p.x + p.y;' % (a, b), 'struct Punto { int x; int y; };', 54, [str(a), str(b), str(a * b)], 'Se accede a los campos con el punto.'),
        ('Punto p = {%d, %d};\np.x = %d;\ncout << p.x << " " << p.y;' % (a, b, a + b), 'struct Punto { int x; int y; };', 60, [], 'Se cambia solo el campo x.'),
        ('Caja c(%d, %d);\ncout << c.area();' % (a, b), 'class Caja {\npublic:\n  int w, h;\n  Caja(int a, int b) : w(a), h(b) {}\n  int area() { return w * h; }\n};', 74, [str(a + b), str(2 * (a + b))], 'El constructor guarda w y h; area multiplica.'),
        ('Cont c;\nc.sube();\nc.sube();\ncout << c.n;', 'struct Cont { int n = %d; void sube() { n++; } };' % a, 70, [str(a), str(a + 1), str(a + 3)], 'Cada llamada a sube suma 1 al campo n.'),
    ]
    s, top, d, al, why = forms[k]
    return X(s, d + ri(0, 5), top=top, alts=al, why=why)
fam(10, f10)

# tabla: tipos y palabras reservadas
T = [('int', 'Número entero', 2), ('double', 'Número decimal de doble precisión', 8), ('char', 'Un solo carácter', 6), ('bool', 'Valor verdadero o falso', 6), ('string', 'Cadena de texto de la biblioteca estándar', 10),
     ('void', 'Función que no devuelve valor', 14), ('const', 'Declara que un valor no puede modificarse', 18), ('cin', 'Flujo para leer datos del teclado', 8), ('cout', 'Flujo para escribir en pantalla', 6),
     ('endl', 'Salto de línea y vaciado del flujo', 12), ('vector', 'Arreglo dinámico de la biblioteca estándar', 24), ('struct', 'Agrupa varios campos en un tipo propio', 30),
     ('class', 'Define un tipo con datos y métodos', 34), ('new', 'Reserva memoria dinámica en el heap', 66), ('delete', 'Libera memoria reservada con new', 66), ('nullptr', 'Puntero que no apunta a nada', 60),
     ('auto', 'Deja que el compilador deduzca el tipo', 44), ('namespace', 'Agrupa nombres para evitar colisiones', 40), ('template', 'Permite escribir código genérico para varios tipos', 80), ('virtual', 'Permite que un método sea sobrescrito en clases derivadas', 84),
     ('#include', 'Incorpora el contenido de otra cabecera', 6), ('return', 'Termina la función y devuelve un valor', 10), ('break', 'Sale del bucle o switch actual', 14), ('static', 'Hace que una variable conserve su valor entre llamadas', 56),
     ('unsigned', 'Tipo entero sin signo (no admite negativos)', 52), ('long long', 'Entero de al menos 64 bits', 46), ('enum', 'Define un conjunto de constantes con nombre', 44), ('sizeof', 'Devuelve el tamaño en bytes de un tipo o valor', 36),
     ('inline', 'Sugiere al compilador sustituir la llamada por el cuerpo', 78), ('explicit', 'Evita conversiones implícitas del constructor', 88), ('typedef', 'Crea un alias para un tipo', 58), ('goto', 'Salta a una etiqueta dentro de la función', 70)]
for i, (n, dsc, d) in enumerate(T):
    r2 = random.Random(i + 5); others = [t for j, t in enumerate(T) if j != i]
    row('cpp', 'En C++, ¿para qué sirve «%s»?' % n, dsc, [x[1] for x in r2.sample(others, 3)], d, '%s: %s.' % (n, dsc[0].lower() + dsc[1:]))
    row('cpp', 'En C++, ¿qué palabra o elemento %s?' % (dsc[0].lower() + dsc[1:]), n, [x[0] for x in r2.sample(others, 3)], d + 5, 'Es «%s».' % n)

C('cpp', r'''
0§¿Qué instrucción imprime texto en C++?§cout << "Hola";§print("Hola");§echo "Hola";§System.out.println("Hola");§
0§¿Con qué símbolo termina normalmente una instrucción en C++?§;§.§:§,§
1§¿Cuál es la función donde empieza a ejecutarse un programa C++?§main§start§init§run§
2§¿Qué línea incluye la biblioteca de entrada y salida?§#include <iostream>§import iostream§using iostream§#use <iostream>§
3§¿Cómo se escribe un comentario de una línea en C++?§// comentario§# comentario§-- comentario§<!-- comentario -->§
4§¿Qué tipo es adecuado para guardar 3.14?§double§int§char§bool§
5§¿Qué operador asigna un valor a una variable?§=§==§:=§=>§
6§¿Qué operador compara igualdad?§==§=§!=§===§C++ no tiene ===.
7§¿Qué significa int edad;?§Declara una variable entera llamada edad§Crea una función edad§Imprime edad§Define una constante§
8§¿Qué instrucción lee un número del teclado?§cin >> n;§cout >> n;§read(n);§input(n);§
10§¿Qué diferencia hay entre = y ==?§= asigna y == compara§= compara y == asigna§Son iguales§== declara variables§
12§¿Cómo se declara una constante entera?§const int N = 5;§int const = N 5;§constant int N = 5;§final int N = 5;§
14§¿Qué hace using namespace std;?§Permite usar nombres de std sin escribir el prefijo§Importa una librería de red§Declara la función main§Evita errores de memoria§
16§¿Cuál es el primer índice de un arreglo?§0§1§-1§Depende del tipo§
18§¿Qué operador representa «y lógico»?§&&§&§and§||§
18§¿Qué operador representa «o lógico»?§||§|§or§&&§
20§¿Qué hace la sentencia return 0; en main?§Indica que el programa terminó correctamente§Reinicia el programa§Imprime cero§Declara una variable§
22§¿Qué hace un bucle for (int i = 0; i < 5; i++)?§Repite 5 veces con i de 0 a 4§Repite 5 veces con i de 1 a 5§Repite 4 veces§Se repite infinitamente§
24§¿Qué indica la palabra void en una función?§No devuelve ningún valor§Devuelve cero§No tiene nombre§No tiene parámetros§
26§¿Qué es un parámetro?§Una variable que recibe la función§Un tipo de dato§Un operador§Un bucle§
28§¿Qué significa el operador ++?§Incrementa en 1§Duplica el valor§Suma dos variables§Compara dos valores§
30§¿Qué ocurre si accedes a a[10] en un arreglo de 5 elementos?§Comportamiento indefinido§Se crea el elemento§Devuelve siempre 0§El compilador corrige el índice§
32§¿Cómo se declara un vector de enteros?§vector<int> v;§int vector v;§vector v<int>;§vector(int) v;§
34§¿Qué hace v.size()?§Devuelve la cantidad de elementos del vector§Devuelve el último elemento§Reserva memoria§Ordena el vector§
36§¿Qué diferencia hay entre i++ y ++i como expresión?§i++ entrega el valor anterior y ++i el nuevo§Son exactamente iguales§++i es más lento§i++ no incrementa§
38§¿Qué es un compilador?§Un programa que traduce el código fuente a código máquina§Un editor de texto§Un depurador§Un sistema operativo§
40§¿Qué hace break en un switch?§Evita pasar al siguiente case§Reinicia el switch§Declara el default§Termina el programa§
42§¿Qué se necesita para que una función pueda llamarse antes de su definición?§Un prototipo (declaración)§Un puntero§Una variable global§Un namespace§
44§¿Qué es una referencia (int &r = x)?§Otro nombre para la misma variable§Una copia de x§Un puntero a un puntero§Una constante§
48§¿Qué diferencia hay entre pasar por valor y por referencia?§Por referencia la función puede modificar el original§Por valor es más rápido siempre§Por referencia crea una copia§No hay diferencia§
50§¿Qué es un puntero?§Una variable que guarda una dirección de memoria§Un tipo de bucle§Una función especial§Un número decimal§
52§¿Qué operador obtiene la dirección de una variable?§&§*§@§#§
54§¿Qué operador accede al valor al que apunta un puntero?§*§&§->§@§
56§¿Qué es un constructor?§Un método que se ejecuta al crear un objeto§Un método que elimina el objeto§Una función global§Un operador§
58§¿Qué significa private en una clase?§Solo se accede desde dentro de la clase§Se accede desde cualquier lugar§Solo se accede en main§Es de solo lectura§
60§¿Qué hace el operador -> ?§Accede a un miembro a través de un puntero§Compara dos punteros§Declara una función§Indica herencia§
62§¿Qué es la herencia?§Que una clase derive de otra reutilizando sus miembros§Copiar un archivo§Crear un arreglo§Declarar un namespace§
64§¿Qué ocurre si haces new sin delete?§Hay una fuga de memoria§El compilador libera la memoria§El programa no compila§Se borra el puntero y nada más§
66§¿Cuándo se llama al destructor?§Cuando el objeto deja de existir§Cuando se crea el objeto§Al compilar§Nunca§
68§¿Qué es la sobrecarga de funciones?§Varias funciones con el mismo nombre y distintos parámetros§Llamar a una función muchas veces§Una función muy larga§Una función recursiva§
70§¿Qué es un template?§Código genérico que funciona con distintos tipos§Un comentario§Un tipo de bucle§Un archivo de cabecera§
72§¿Qué es RAII?§Ligar la vida de un recurso a la vida de un objeto§Un tipo de puntero§Un algoritmo de ordenamiento§Una librería gráfica§
74§¿Qué ventaja tiene std::unique_ptr?§Libera automáticamente el objeto al salir de alcance§Permite varios dueños§Es más rápido que un entero§Evita todos los errores§
76§¿Qué es polimorfismo?§Tratar objetos derivados mediante la interfaz de la clase base§Tener varias variables§Usar muchos bucles§Compilar en varios sistemas§
78§¿Para qué sirve virtual en un método?§Para permitir sobrescritura con enlace dinámico§Para hacerlo privado§Para evitar herencia§Para compilarlo más rápido§
80§¿Qué complejidad tiene std::sort?§O(n log n)§O(n)§O(n²)§O(log n)§
84§¿Qué es un desbordamiento (overflow) de entero con signo?§Superar el rango del tipo; es comportamiento indefinido§Un error del compilador§Perder la conexión§Un error de sintaxis§
88§¿Qué hace std::move?§Convierte un objeto en rvalue para permitir mover recursos§Copia el objeto§Lo elimina§Lo envía a otro hilo§
92§¿Qué es un dangling pointer?§Un puntero a memoria que ya no es válida§Un puntero nulo§Un puntero constante§Un puntero a función§
''')
