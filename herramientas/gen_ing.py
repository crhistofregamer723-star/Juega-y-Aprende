from lib import *
B = Bank()
ri = R.randint
def sample_wrong(pool, ans, n=3, key=lambda x: x):
    c = [x for x in pool if key(x) != ans]
    return R.sample(c, n)

# ====================== ing1 · SALUDOS ======================
G1 = [  # (inglés, español, dificultad)
 ('Hello', 'Hola', 1), ('Hi', 'Hola (informal)', 2), ('Goodbye', 'Adiós', 2), ('Bye', 'Chao', 2), ('Yes', 'Sí', 1), ('No', 'No', 1),
 ('Please', 'Por favor', 3), ('Thank you', 'Gracias', 2), ('Thanks', 'Gracias (informal)', 3), ("You're welcome", 'De nada', 8), ('Sorry', 'Lo siento', 5),
 ('Excuse me', 'Disculpe', 8), ('Good morning', 'Buenos días', 3), ('Good afternoon', 'Buenas tardes', 5), ('Good evening', 'Buenas noches (al llegar)', 14),
 ('Good night', 'Buenas noches (al despedirse)', 8), ('See you later', 'Hasta luego', 8), ('See you tomorrow', 'Hasta mañana', 10), ('See you soon', 'Nos vemos pronto', 14),
 ('How are you?', '¿Cómo estás?', 6), ("I'm fine", 'Estoy bien', 8), ("I'm fine, thanks", 'Estoy bien, gracias', 10), ('And you?', '¿Y tú?', 8),
 ('Nice to meet you', 'Mucho gusto', 10), ('Pleased to meet you', 'Encantado de conocerte', 20), ("What's your name?", '¿Cómo te llamas?', 10), ('My name is Ana', 'Me llamo Ana', 8),
 ('Where are you from?', '¿De dónde eres?', 14), ("I'm from Costa Rica", 'Soy de Costa Rica', 14), ('How old are you?', '¿Cuántos años tienes?', 14), ("I'm twelve years old", 'Tengo doce años', 18),
 ('Welcome', 'Bienvenido', 8), ('Congratulations', 'Felicidades', 24), ('Good luck', 'Buena suerte', 18), ('Take care', 'Cuídate', 24), ('Have a nice day', 'Que tengas un buen día', 26),
 ("How's it going?", '¿Cómo te va?', 28), ("What's up?", '¿Qué tal? / ¿Qué hay?', 30), ('Long time no see', 'Tanto tiempo sin verte', 44), ("I don't understand", 'No entiendo', 22),
 ('Can you repeat that?', '¿Puedes repetirlo?', 30), ('Speak slowly, please', 'Habla despacio, por favor', 32), ('Maybe', 'Quizás', 14), ('Of course', 'Claro / Por supuesto', 20),
 ("I'm sorry I'm late", 'Perdón por llegar tarde', 36), ('Happy birthday', 'Feliz cumpleaños', 14), ('Merry Christmas', 'Feliz Navidad', 14), ('Happy New Year', 'Feliz Año Nuevo', 16),
 ('Cheers', '¡Salud! (al brindar)', 36), ('Bless you', 'Salud (al estornudar)', 40), ('I miss you', 'Te extraño', 24), ('I love you', 'Te quiero', 12), ('Good job', 'Buen trabajo', 16),
 ('No problem', 'No hay problema', 18), ('Never mind', 'No importa', 30), ('I agree', 'Estoy de acuerdo', 28), ('Where is the bathroom?', '¿Dónde está el baño?', 22),
 ('How much is it?', '¿Cuánto cuesta?', 24), ('Do you speak English?', '¿Hablas inglés?', 20), ("It's a pleasure", 'Es un placer', 40), ('Make yourself at home', 'Siéntete como en casa', 56),
 ('Break a leg', 'Mucha suerte (en el escenario)', 68), ('Pardon me', 'Perdón / Disculpe', 34), ("What's your phone number?", '¿Cuál es tu número de teléfono?', 40), ('Nice to see you again', 'Qué gusto verte otra vez', 46),
 ('Have a good weekend', 'Que tengas un buen fin de semana', 40), ('Safe travels', 'Buen viaje', 44), ('Get well soon', 'Que te mejores pronto', 52), ('Thank you very much', 'Muchas gracias', 12), ('Many thanks', 'Muchas gracias', 40),
]
for en, es, d in G1:
    others = [x for x in G1 if x[0] != en and x[1] != es]
    if len(others) >= 3:
        w = R.sample(others, 3)
        B.add('ing1', f'¿Cómo se dice «{es}» en inglés?', en, [x[0] for x in w], d, f'{en} significa «{es}».', [en, en.lower(), en.rstrip('?!.')])
for en, es, d in R.sample(G1, 55):
    others = [x for x in G1 if x[0] != en and x[1] != es]
    w = R.sample(others, 3)
    B.add('ing1', f'¿Qué significa «{en}»?', es, [x[1] for x in w], d + 3, f'{en} se traduce como «{es}».', [es, es.lower()])
for es_s, en_a, w, d in [
    ('Son las 8 de la mañana y saludas a tu maestra. ¿Qué dices?', 'Good morning', ['Good night', 'Goodbye', 'See you later'], 10),
    ('Alguien estornuda. ¿Qué le dices en inglés?', 'Bless you', ['Cheers', 'Sorry', 'Welcome'], 40),
    ('Te despides de tu amigo para verlo mañana. ¿Qué dices?', 'See you tomorrow', ['See you never', 'Good morning', 'Nice to meet you'], 12),
    ('Pisaste a alguien sin querer. ¿Qué dices?', 'Sorry', ['Welcome', 'Good luck', 'Cheers'], 6),
    ('Alguien te da un regalo. ¿Qué dices?', 'Thank you', ['Goodbye', 'Excuse me', 'Please'], 4),
    ('Conoces a alguien por primera vez. ¿Qué dices?', 'Nice to meet you', ['See you later', 'Good night', 'Happy birthday'], 12),
    ('Vas a dormir y te despides de tu familia. ¿Qué dices?', 'Good night', ['Good morning', 'Good afternoon', 'Hello'], 10),
    ('Quieres pasar entre una multitud. ¿Qué dices?', 'Excuse me', ['Cheers', 'Congratulations', 'Welcome'], 18),
    ('Tu amigo tiene examen mañana. ¿Qué le deseas?', 'Good luck', ['Take care', 'Bless you', 'Long time no see'], 18),
    ('Es el cumpleaños de tu hermana. ¿Qué le dices?', 'Happy birthday', ['Merry Christmas', 'Happy New Year', 'Good night'], 12),
    ('Alguien te da las gracias. ¿Qué respondes?', "You're welcome", ['Please', 'Excuse me', 'Goodbye'], 14),
    ('Llegas a una tienda a las 3 de la tarde. ¿Qué saludo usas?', 'Good afternoon', ['Good morning', 'Good night', 'Good luck'], 16),
    ('Quieres que alguien repita lo que dijo. ¿Qué dices?', 'Can you repeat that?', ['How old are you?', 'Where are you from?', 'Nice to meet you'], 34),
    ('Un amigo se enferma. ¿Qué le deseas?', 'Get well soon', ['Happy birthday', 'Good morning', 'Congratulations'], 52),
    ('Quieres preguntar el precio de algo. ¿Qué dices?', 'How much is it?', ['How old are you?', 'What is your name?', 'Where is it from?'], 26),
]:
    B.add('ing1', es_s, en_a, w, d, f'En esa situación se dice «{en_a}».', [en_a, en_a.lower()])

# ====================== ing2 · VERB TO BE ======================
SUBJ = [('I', 'am'), ('You', 'are'), ('He', 'is'), ('She', 'is'), ('It', 'is'), ('We', 'are'), ('They', 'are'),
        ('My brother', 'is'), ('My parents', 'are'), ('The dog', 'is'), ('The books', 'are'), ('Ana and Luis', 'are'), ('My teacher', 'is'), ('The children', 'are'), ('Maria', 'is'), ('Your shoes', 'are')]
COMP = ['happy', 'tired', 'at home', 'in the park', 'busy', 'hungry', 'late', 'ready', 'in the kitchen', 'at school', 'very nice', 'from Costa Rica', 'ten years old', 'in the garden']
COMP_NOUN = ['a student', 'my friend', 'a doctor', 'a teacher', 'a good player']
for _ in range(60):
    s, cop = R.choice(SUBJ)
    plural = cop == 'are' and s not in ('You',)
    comp = R.choice(COMP)
    q = f'Completa: {s} ___ {comp}.'
    B.add('ing2', q, cop, [x for x in ['am', 'is', 'are', 'be'] if x != cop], 6 + (0 if s in ('I', 'You', 'He', 'She') else 8) + ri(0, 6), f'Con «{s}» se usa «{cop}».', [cop])
for _ in range(14):
    s, cop = R.choice([x for x in SUBJ if x[0] not in ('You', 'We', 'They', 'My parents', 'The books', 'The children', 'Ana and Luis', 'Your shoes', 'The dog', 'It')])
    n = R.choice(COMP_NOUN)
    B.add('ing2', f'Completa: {s} ___ {n}.', cop, [x for x in ['am', 'is', 'are', 'be'] if x != cop], 8 + ri(0, 6), f'Con «{s}» se usa «{cop}».', [cop])
NEG = {'am': 'am not', 'is': "isn't", 'are': "aren't"}
for _ in range(20):
    s, cop = R.choice(SUBJ); comp = R.choice(COMP)
    ans = NEG[cop]
    w = [x for x in ["isn't", "aren't", 'am not', "don't", "doesn't"] if x != ans]
    B.add('ing2', f'Completa en negativo: {s} ___ {comp}.', ans, w[:3] if ans != 'am not' else ["isn't", "aren't", "don't"], 24 + ri(0, 10), f'Negativo de «{cop}»: {ans}.', [ans, ans.replace("n't", ' not')])
for s, cop in R.sample(SUBJ, 12):
    comp = R.choice(COMP)
    ok = f'{cop.capitalize()} {s[0].lower() + s[1:] if s != "I" else "I"} {comp}?'
    bad = [f'{s} {cop} {comp}?', f'Do {s[0].lower() + s[1:] if s != "I" else "I"} {comp}?', f'{s} {comp} {cop}?']
    B.add('ing2', f'¿Cuál es la pregunta correcta?', ok, bad, 34 + ri(0, 10), 'En preguntas con «to be», el verbo va antes del sujeto.', [ok])
for s in ['I', 'You', 'He', 'She', 'We', 'They', 'It']:
    cop = dict(SUBJ)[s]
    ct = {'I': "I'm", 'You': "You're", 'He': "He's", 'She': "She's", 'It': "It's", 'We': "We're", 'They': "They're"}[s]
    B.add('ing2', f'¿Cuál es la contracción de «{s} {cop}»?', ct, [x for x in ["I'm", "You're", "He's", "She's", "It's", "We're", "They're"] if x != ct][:3], 28 + ri(0, 8), f'{s} {cop} → {ct}.', [ct, ct.replace("'", '’')])
for es, en in [('Yo soy estudiante', 'I am a student'), ('Ella es mi amiga', 'She is my friend'), ('Ellos están cansados', 'They are tired'), ('Nosotros estamos en casa', 'We are at home'), ('Él es doctor', 'He is a doctor'), ('Tú eres amable', 'You are kind'), ('Es un gato', 'It is a cat'), ('Mi mamá está en la cocina', 'My mother is in the kitchen'), ('Los libros están en la mesa', 'The books are on the table'), ('Yo no estoy listo', 'I am not ready'), ('Ellas no son maestras', 'They are not teachers'), ('¿Eres feliz?', 'Are you happy?'), ('¿Está ella en casa?', 'Is she at home?')]:
    pool = [x[1] for x in [('', 'I am a student'), ('', 'She is my friend'), ('', 'They are tired'), ('', 'We are at home'), ('', 'He is a doctor'), ('', 'You are kind'), ('', 'It is a cat'), ('', 'My mother is in the kitchen'), ('', 'The books are on the table'), ('', 'I am not ready'), ('', 'They are not teachers'), ('', 'Are you happy?'), ('', 'Is she at home?')] if x[1] != en]
    B.add('ing2', f'¿Cómo se dice «{es}» en inglés?', en, R.sample(pool, 3), 18 + ri(0, 18), f'«{es}» se dice «{en}».', [en, en.lower()])
for _ in range(14):
    s = R.choice(['I', 'He', 'She', 'It', 'The dog', 'My brother', 'Maria']); 
    pl = R.choice(['You', 'We', 'They', 'The children', 'My parents'])
    one = s; was = 'was' if s != 'You' else 'were'
    if R.random() < .5:
        B.add('ing2', f'Completa en pasado: {s} ___ at home yesterday.', 'was', ['were', 'is', 'am'], 46 + ri(0, 10), 'Pasado de am/is: was.', ['was'])
    else:
        B.add('ing2', f'Completa en pasado: {pl} ___ at school yesterday.', 'were', ['was', 'are', 'be'], 48 + ri(0, 10), 'Pasado de are: were.', ['were'])
B.add('ing2', '¿Cuál oración es correcta?', 'She is my sister.', ['She am my sister.', 'She are my sister.', 'She be my sister.'], 12, 'Con she se usa is.', ['She is my sister.'])
B.add('ing2', '¿Cuál oración es correcta?', 'They are in the park.', ['They is in the park.', 'They am in the park.', 'They be in the park.'], 14, 'Con they se usa are.', ['They are in the park.'])
B.add('ing2', '¿Cuál oración es correcta?', 'I am not hungry.', ['I amn’t hungry.', 'I isn’t hungry.', 'I not am hungry.'], 40, 'No existe «amn’t» en inglés estándar: se dice «am not».', ['I am not hungry.'])
B.add('ing2', "¿Cuál es la respuesta corta correcta a «Are you tired?» (sí)?", 'Yes, I am.', ['Yes, I are.', 'Yes, I do.', 'Yes, I is.'], 36, 'Se repite el verbo to be.', ['Yes, I am.'])
B.add('ing2', "¿Cuál es la respuesta corta correcta a «Is she a teacher?» (no)?", "No, she isn't.", ["No, she doesn't.", "No, she aren't.", "No, she don't."], 38, 'Se repite el verbo to be en negativo.', ["No, she isn't."])

# ====================== ing3 · PRESENT SIMPLE ======================
V3 = [('work', 'works'), ('play', 'plays'), ('eat', 'eats'), ('read', 'reads'), ('live', 'lives'), ('run', 'runs'), ('drink', 'drinks'), ('sleep', 'sleeps'), ('walk', 'walks'), ('write', 'writes'), ('sing', 'sings'), ('cook', 'cooks'),
      ('go', 'goes'), ('do', 'does'), ('watch', 'watches'), ('teach', 'teaches'), ('fix', 'fixes'), ('wash', 'washes'), ('pass', 'passes'), ('kiss', 'kisses'), ('study', 'studies'), ('carry', 'carries'), ('try', 'tries'), ('fly', 'flies'), ('cry', 'cries'), ('have', 'has'), ('buy', 'buys'), ('say', 'says'), ('enjoy', 'enjoys'), ('finish', 'finishes'), ('catch', 'catches'), ('push', 'pushes')]
SUB3 = ['He', 'She', 'My brother', 'Ana', 'The cat', 'My mother', 'Carlos', 'The teacher', 'My dad', 'Our dog']
OBJ = {'work': 'every day', 'play': 'soccer', 'eat': 'rice', 'read': 'a book', 'live': 'in San José', 'run': 'in the park', 'drink': 'water', 'sleep': 'at night', 'walk': 'to school', 'write': 'letters', 'sing': 'songs', 'cook': 'dinner',
       'go': 'to school', 'do': 'her homework', 'watch': 'TV', 'teach': 'English', 'fix': 'computers', 'wash': 'the dishes', 'pass': 'the ball', 'kiss': 'his baby', 'study': 'math', 'carry': 'a bag', 'try': 'new food', 'fly': 'kites', 'cry': 'at sad movies', 'have': 'a pet', 'buy': 'bread', 'say': 'hello', 'enjoy': 'music', 'finish': 'early', 'catch': 'the bus', 'push': 'the door'}
for _ in range(70):
    b, s3 = R.choice(V3); sub = R.choice(SUB3)
    wr = [b, b + 'ing' if not b.endswith('e') else b[:-1] + 'ing', b + 'ed' if not b.endswith('e') else b + 'd']
    d = 12 + (0 if s3 == b + 's' else 16) + ri(0, 8)
    B.add('ing3', f'Completa: {sub} ___ ({b}) {OBJ[b]}.', s3, wr, d, f'Con he/she/it el verbo añade -s/-es: {s3}.', [s3])
for _ in range(24):
    b, s3 = R.choice(V3); pl = R.choice(['I', 'You', 'We', 'They', 'My friends'])
    B.add('ing3', f'Completa: {pl} ___ ({b}) {OBJ[b]}.', b, [s3, b + 'ing' if not b.endswith('e') else b[:-1] + 'ing', 'does ' + b], 10 + ri(0, 8), f'Con «{pl}» el verbo no cambia.', [b])
for _ in range(16):
    b, s3 = R.choice(V3); sub = R.choice(['He', 'She', 'My sister', 'The dog'])
    B.add('ing3', f'Completa en negativo: {sub} ___ {b} {OBJ[b]}.', f"doesn't", ["don't", "isn't", "didn't"], 30 + ri(0, 10), 'Con he/she/it el auxiliar negativo es «doesn’t» y el verbo queda en base.', ["doesn't", 'does not'])
for _ in range(12):
    b, s3 = R.choice(V3); sub = R.choice(['I', 'You', 'We', 'They'])
    B.add('ing3', f'Completa en negativo: {sub} ___ {b} {OBJ[b]}.', "don't", ["doesn't", "isn't", "aren't"], 28 + ri(0, 10), 'Con I/you/we/they el auxiliar negativo es «don’t».', ["don't", 'do not'])
for _ in range(14):
    b, s3 = R.choice(V3); sub = R.choice(['he', 'she', 'your brother', 'the teacher'])
    B.add('ing3', f'Completa la pregunta: ___ {sub} {b} {OBJ[b]}?', 'Does', ['Do', 'Is', 'Are'], 32 + ri(0, 10), 'Con he/she/it las preguntas usan «Does».', ['Does', 'does'])
for _ in range(12):
    b, s3 = R.choice(V3); sub = R.choice(['you', 'they', 'we', 'your friends'])
    B.add('ing3', f'Completa la pregunta: ___ {sub} {b} {OBJ[b]}?', 'Do', ['Does', 'Is', 'Are'], 30 + ri(0, 10), 'Con I/you/we/they las preguntas usan «Do».', ['Do', 'do'])
FREQ = [('always', 'siempre'), ('usually', 'normalmente'), ('often', 'a menudo'), ('sometimes', 'a veces'), ('never', 'nunca')]
for _ in range(10):
    f = R.choice(FREQ)[0]; b, s3 = R.choice(V3[:12])
    ok = f'She {f} {s3} {OBJ[b]}.'
    B.add('ing3', '¿Cuál oración tiene bien colocado el adverbio de frecuencia?', ok, [f'She {s3} {f} {OBJ[b]}.', f'She {s3} {OBJ[b]} {f}.', f'{f.capitalize()} {s3} she {OBJ[b]}.'], 50 + ri(0, 14), 'El adverbio de frecuencia va antes del verbo principal.', [ok])
for es, en in [('Ella trabaja', 'She works'), ('Él estudia', 'He studies'), ('Yo como arroz', 'I eat rice'), ('Ellos juegan fútbol', 'They play soccer'), ('Nosotros vivimos aquí', 'We live here'), ('Ella no come carne', "She doesn't eat meat"), ('¿Trabajas aquí?', 'Do you work here?'), ('Él ve televisión', 'He watches TV'), ('Mi mamá cocina', 'My mom cooks'), ('Yo no bebo café', "I don't drink coffee"), ('¿Él habla inglés?', 'Does he speak English?'), ('El perro duerme', 'The dog sleeps'), ('Ella tiene un gato', 'She has a cat'), ('Ellos van a la escuela', 'They go to school')]:
    pool = [x[1] for x in [('', 'She works'), ('', 'He studies'), ('', 'I eat rice'), ('', 'They play soccer'), ('', 'We live here'), ('', "She doesn't eat meat"), ('', 'Do you work here?'), ('', 'He watches TV'), ('', 'My mom cooks'), ('', "I don't drink coffee"), ('', 'Does he speak English?'), ('', 'The dog sleeps'), ('', 'She has a cat'), ('', 'They go to school')] if x[1] != en]
    B.add('ing3', f'¿Cómo se dice «{es}» en inglés?', en, R.sample(pool, 3), 26 + ri(0, 22), f'«{es}» se dice «{en}».', [en, en.lower()])
for b, s3 in R.sample(V3, 22):
    B.add('ing3', f'¿Cuál es la forma de «he/she/it» del verbo «{b}»?', s3, [b, b + 's' if s3 != b + 's' else b + 'es', b[:-1] + 'ies' if s3 != b[:-1] + 'ies' else b + 'ed'], 22 + (0 if s3 == b + 's' else 18) + ri(0, 6), f'{b} → {s3}.', [s3])

# ====================== ing4 · NÚMEROS Y COLORES ======================
ONES = ['zero', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine', 'ten', 'eleven', 'twelve', 'thirteen', 'fourteen', 'fifteen', 'sixteen', 'seventeen', 'eighteen', 'nineteen']
TENS = ['', '', 'twenty', 'thirty', 'forty', 'fifty', 'sixty', 'seventy', 'eighty', 'ninety']
def words(n):
    if n < 20: return ONES[n]
    if n < 100: return TENS[n // 10] + ('-' + ONES[n % 10] if n % 10 else '')
    if n < 1000: return ONES[n // 100] + ' hundred' + (' and ' + words(n % 100) if n % 100 else '')
    return words(n // 1000) + ' thousand' + ((' ' + ('and ' if n % 1000 < 100 else '') + words(n % 1000)) if n % 1000 else '')
def numq(n, d):
    w = words(n)
    cand = {words(n + 1), words(n - 1), words(n + 10) if n + 10 < 1000 else words(n + 2), words(n - 10) if n > 10 else words(n + 3), words(n + 100) if n < 900 else words(n - 100)}
    cand.discard(w)
    B.add('ing4', f'¿Cómo se escribe el número {n} en inglés?', w, sorted(cand)[:6], d, f'{n} = {w}.', [w, w.replace('-', ' ')])
for n in range(1, 21): numq(n, 2 + n // 2)
for n in R.sample(range(21, 100), 22): numq(n, 24 + ri(0, 16))
for n in R.sample(range(100, 1000), 8): numq(n, 56 + ri(0, 16))
for n in R.sample(range(1000, 10000), 4): numq(n, 72 + ri(0, 14))
for _ in range(24):
    a, b = ri(1, 12), ri(1, 12)
    op = R.choice(['plus', 'minus', 'times'])
    r = a + b if op == 'plus' else a - b if op == 'minus' else a * b
    if r < 0: continue
    ans = words(r)
    wr = [words(x) for x in {r + 1, r + 2, max(0, r - 1), r + 10} if x != r and x >= 0][:3]
    B.add('ing4', f'¿Cuál es el resultado? {words(a).capitalize()} {op} {words(b)} is …', ans, wr, 30 + ri(0, 22), f'{a} {"+" if op == "plus" else "−" if op == "minus" else "×"} {b} = {r}.', [ans, ans.replace('-', ' ')])
ORD = ['first', 'second', 'third', 'fourth', 'fifth', 'sixth', 'seventh', 'eighth', 'ninth', 'tenth', 'eleventh', 'twelfth', 'thirteenth', 'fourteenth', 'fifteenth', 'sixteenth', 'seventeenth', 'eighteenth', 'nineteenth', 'twentieth']
for i, o in enumerate(ORD):
    w = R.sample([x for x in ORD if x != o], 3)
    B.add('ing4', f'¿Cómo se dice «{i+1}.º» (ordinal) en inglés?', o, w, 36 + i * 2, f'{i+1}.º = {o}.', [o])
COLORS = [('red', 'rojo'), ('blue', 'azul'), ('green', 'verde'), ('yellow', 'amarillo'), ('black', 'negro'), ('white', 'blanco'), ('orange', 'anaranjado'), ('pink', 'rosado'), ('purple', 'morado'), ('brown', 'café'), ('gray', 'gris'), ('gold', 'dorado'), ('silver', 'plateado'), ('turquoise', 'turquesa'), ('beige', 'beige'), ('violet', 'violeta'), ('maroon', 'vino tinto'), ('navy blue', 'azul marino'), ('light blue', 'celeste'), ('dark green', 'verde oscuro')]
for en, es in COLORS:
    d = 4 + COLORS.index((en, es)) * 2
    B.add('ing4', f'¿Cómo se dice «{es}» en inglés?', en, [x[0] for x in R.sample([c for c in COLORS if c[0] != en], 3)], d, f'{en} significa «{es}».', [en])
    B.add('ing4', f'¿Qué color es «{en}»?', es, [x[1] for x in R.sample([c for c in COLORS if c[1] != es], 3)], d + 3, f'{en} = {es}.', [es])
for a, b, r, d in [('red and yellow', '', 'orange', 22), ('blue and yellow', '', 'green', 22), ('red and white', '', 'pink', 26), ('red and blue', '', 'purple', 24), ('black and white', '', 'gray', 24)]:
    B.add('ing4', f'¿Qué color se obtiene al mezclar {a}?', r, [x for x in ['orange', 'green', 'pink', 'purple', 'gray', 'brown'] if x != r][:3], d, f'{a} → {r}.', [r])
DAYS = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
DES = ['lunes', 'martes', 'miércoles', 'jueves', 'viernes', 'sábado', 'domingo']
for i, (en, es) in enumerate(zip(DAYS, DES)):
    B.add('ing4', f'¿Cómo se dice «{es}» en inglés?', en, [x for x in DAYS if x != en][:3] if False else R.sample([x for x in DAYS if x != en], 3), 12 + i, f'{es} = {en}.', [en])
    nxt = DAYS[(i + 1) % 7]
    B.add('ing4', f'¿Qué día viene después de {en}?', nxt, R.sample([x for x in DAYS if x != nxt], 3), 22 + i, f'Después de {en} viene {nxt}.', [nxt])
MON = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
MES = ['enero', 'febrero', 'marzo', 'abril', 'mayo', 'junio', 'julio', 'agosto', 'septiembre', 'octubre', 'noviembre', 'diciembre']
for i, (en, es) in enumerate(zip(MON, MES)):
    B.add('ing4', f'¿Cómo se dice «{es}» en inglés?', en, R.sample([x for x in MON if x != en], 3), 20 + i, f'{es} = {en}.', [en])
    k = ri(1, 12)
    B.add('ing4', f'¿Cuál es el mes número {i+1} del año en inglés?', en, R.sample([x for x in MON if x != en], 3), 34 + i, f'El mes {i+1} es {en}.', [en])
for en, es in [('spring', 'primavera'), ('summer', 'verano'), ('autumn', 'otoño'), ('winter', 'invierno')]:
    B.add('ing4', f'¿Cómo se dice «{es}» en inglés?', en, [x for x in ['spring', 'summer', 'autumn', 'winter', 'rainy season'] if x != en][:3], 30, f'{es} = {en}.', [en])

# ====================== ing5 · ARTÍCULOS Y PLURALES ======================
AAN = {'apple': 'an', 'banana': 'a', 'egg': 'an', 'dog': 'a', 'umbrella': 'an', 'hour': 'an', 'university': 'a', 'honest man': 'an', 'orange': 'an', 'car': 'a', 'elephant': 'an', 'book': 'a', 'owl': 'an', 'unicorn': 'a', 'ice cream': 'an', 'window': 'a', 'idea': 'an', 'European city': 'a', 'uncle': 'an', 'one-eyed cat': 'a', 'MBA': 'an', 'school': 'a', 'engineer': 'an', 'teacher': 'a', 'eagle': 'an', 'cat': 'a', 'island': 'an', 'useful tool': 'a', 'hour-long class': 'an', 'horse': 'a'}
dd = {'hour': 8, 'university': 8, 'honest man': 9, 'European city': 9, 'unicorn': 8, 'one-eyed cat': 10, 'MBA': 10, 'useful tool': 8, 'hour-long class': 9, 'uncle': 5, 'island': 4}
for w, art in AAN.items():
    other = 'a' if art == 'an' else 'an'
    B.add('ing5', f'Completa: I have ___ {w}.', art, [other, 'two', 'many'], 8 + dd.get(w, 0) * 5 + ri(0, 6), f'Se usa «{art}» por el sonido inicial de «{w}».', [art])
PL = [('cat', 'cats'), ('dog', 'dogs'), ('book', 'books'), ('table', 'tables'), ('house', 'houses'), ('pen', 'pens'), ('box', 'boxes'), ('bus', 'buses'), ('dish', 'dishes'), ('watch', 'watches'), ('class', 'classes'), ('glass', 'glasses'), ('brush', 'brushes'), ('fox', 'foxes'),
      ('baby', 'babies'), ('city', 'cities'), ('story', 'stories'), ('lady', 'ladies'), ('country', 'countries'), ('party', 'parties'), ('boy', 'boys'), ('day', 'days'), ('key', 'keys'), ('toy', 'toys'),
      ('knife', 'knives'), ('leaf', 'leaves'), ('wolf', 'wolves'), ('shelf', 'shelves'), ('wife', 'wives'), ('life', 'lives'), ('thief', 'thieves'), ('half', 'halves'),
      ('tomato', 'tomatoes'), ('potato', 'potatoes'), ('hero', 'heroes'), ('photo', 'photos'), ('piano', 'pianos'), ('radio', 'radios'),
      ('man', 'men'), ('woman', 'women'), ('child', 'children'), ('foot', 'feet'), ('tooth', 'teeth'), ('mouse', 'mice'), ('person', 'people'), ('goose', 'geese'), ('fish', 'fish'), ('sheep', 'sheep'), ('deer', 'deer')]
def plural_wrongs(b, p):
    c = [b + 's', b + 'es', (b[:-1] + 'ies') if b.endswith('y') else b + 'ies', (b[:-1] + 'ves') if b[-1] in 'fe' else b + 'ves', b + 'en', b + 'ed']
    out = []
    for x in c:
        if x != p and x not in out: out.append(x)
    return out
irreg = {'man', 'woman', 'child', 'foot', 'tooth', 'mouse', 'person', 'goose', 'fish', 'sheep', 'deer'}
for i, (b, p) in enumerate(PL):
    d = 4 + (0 if p == b + 's' else 16) + (24 if b in irreg else 0) + ri(0, 6)
    wr = plural_wrongs(b, p)
    if b in irreg: wr = [b + 's', b + 'es', b + 'en'] if p != b else [b + 's', b + 'es', b + 'ies']
    wr = [x for x in wr if x != p][:3]
    B.add('ing5', f'¿Cuál es el plural de «{b}»?', p, wr, d, f'El plural de {b} es {p}.', [p])
    if i % 2 == 0:
        B.add('ing5', f'Escribe el plural de «{b}».', p, wr, d + 4, f'El plural de {b} es {p}.', [p])
for sing, pl in [('This', 'These'), ('That', 'Those')]:
    for noun, p in R.sample(PL[:20], 5):
        B.add('ing5', f'Completa: ___ are my {p}.', pl, [sing, 'A', 'An'], 26 + ri(0, 8), f'Con plural se usa «{pl}».', [pl])
for noun, p in R.sample(PL[:30], 6):
    B.add('ing5', f'Completa: There ___ many {p} in the room.', 'are', ['is', 'am', 'be'], 30 + ri(0, 8), 'Con plural se usa «there are».', ['are'])
for noun, p in R.sample(PL[:30], 6):
    B.add('ing5', f'Completa: There ___ a {noun} on the table.', 'is', ['are', 'am', 'be'], 22 + ri(0, 8), 'Con singular se usa «there is».', ['is'])
for q, a, w, d in [
 ('Completa: ___ sun is very hot today.', 'The', ['A', 'An', 'Some'], 14), ('Completa: I play ___ guitar.', 'the', ['a', 'an', 'some'], 34), ('Completa: She is ___ best student in the class.', 'the', ['a', 'an', 'some'], 36),
 ('Completa: I like ___ music. (en general, sin artículo)', 'sin artículo', ['the', 'a', 'an'], 44), ('Completa: He wants ___ water.', 'some', ['a', 'an', 'many'], 40), ('Completa: Do you have ___ brothers?', 'any', ['a', 'an', 'the'], 46),
 ('Completa: We have ___ milk in the fridge.', 'a little', ['a few', 'many', 'a'], 56), ('Completa: She has ___ friends in the city.', 'a few', ['a little', 'much', 'an'], 56), ('Completa: How ___ money do you have?', 'much', ['many', 'few', 'a'], 52),
 ('Completa: How ___ apples are there?', 'many', ['much', 'little', 'a'], 52), ('Completa: Paris is ___ capital of France.', 'the', ['a', 'an', 'some'], 32), ('Completa: My sister is ___ engineer.', 'an', ['a', 'the', 'some'], 20),
 ('Completa: Look at ___ stars! They are beautiful.', 'the', ['a', 'an', 'much'], 38), ('Completa: He has no ___ in his bag.', 'books', ['book', 'a book', 'much book'], 48), ('Completa: She doesn’t have ___ time.', 'much', ['many', 'a few', 'an'], 54),
]:
    B.add('ing5', q, a, w, d, 'Regla de artículos y cuantificadores.', [a])

# ====================== ing6 · VOCABULARIO DIARIO ======================
VOC = {
 'familia': [('mother', 'madre'), ('father', 'padre'), ('sister', 'hermana'), ('brother', 'hermano'), ('grandmother', 'abuela'), ('grandfather', 'abuelo'), ('uncle', 'tío'), ('aunt', 'tía'), ('cousin', 'primo'), ('son', 'hijo'), ('daughter', 'hija'), ('husband', 'esposo'), ('wife', 'esposa'), ('nephew', 'sobrino'), ('niece', 'sobrina')],
 'comida': [('bread', 'pan'), ('water', 'agua'), ('milk', 'leche'), ('rice', 'arroz'), ('beans', 'frijoles'), ('chicken', 'pollo'), ('cheese', 'queso'), ('egg', 'huevo'), ('apple', 'manzana'), ('banana', 'banano'), ('orange', 'naranja'), ('soup', 'sopa'), ('salad', 'ensalada'), ('butter', 'mantequilla'), ('sugar', 'azúcar'), ('salt', 'sal'), ('pineapple', 'piña'), ('strawberry', 'fresa'), ('cucumber', 'pepino'), ('breakfast', 'desayuno'), ('lunch', 'almuerzo'), ('dinner', 'cena')],
 'casa': [('house', 'casa'), ('kitchen', 'cocina'), ('bedroom', 'dormitorio'), ('bathroom', 'baño'), ('door', 'puerta'), ('window', 'ventana'), ('table', 'mesa'), ('chair', 'silla'), ('bed', 'cama'), ('roof', 'techo'), ('floor', 'piso'), ('wall', 'pared'), ('garden', 'jardín'), ('stairs', 'escaleras'), ('living room', 'sala'), ('fridge', 'refrigerador'), ('mirror', 'espejo'), ('lamp', 'lámpara'), ('curtain', 'cortina'), ('key', 'llave')],
 'escuela': [('school', 'escuela'), ('book', 'libro'), ('pencil', 'lápiz'), ('pen', 'bolígrafo'), ('notebook', 'cuaderno'), ('teacher', 'maestro'), ('student', 'estudiante'), ('desk', 'pupitre'), ('homework', 'tarea'), ('exam', 'examen'), ('backpack', 'mochila'), ('eraser', 'borrador'), ('ruler', 'regla'), ('library', 'biblioteca'), ('classroom', 'aula'), ('lesson', 'lección'), ('grade', 'nota'), ('board', 'pizarra')],
 'cuerpo': [('head', 'cabeza'), ('hand', 'mano'), ('foot', 'pie'), ('eye', 'ojo'), ('ear', 'oreja'), ('nose', 'nariz'), ('mouth', 'boca'), ('arm', 'brazo'), ('leg', 'pierna'), ('finger', 'dedo'), ('knee', 'rodilla'), ('shoulder', 'hombro'), ('neck', 'cuello'), ('stomach', 'estómago'), ('back', 'espalda'), ('elbow', 'codo'), ('tooth', 'diente'), ('hair', 'cabello')],
 'ropa': [('shirt', 'camisa'), ('pants', 'pantalones'), ('shoes', 'zapatos'), ('socks', 'calcetines'), ('hat', 'sombrero'), ('dress', 'vestido'), ('jacket', 'chaqueta'), ('skirt', 'falda'), ('belt', 'cinturón'), ('gloves', 'guantes'), ('scarf', 'bufanda'), ('boots', 'botas'), ('sweater', 'suéter'), ('umbrella', 'paraguas'), ('glasses', 'anteojos')],
 'animales': [('dog', 'perro'), ('cat', 'gato'), ('bird', 'pájaro'), ('horse', 'caballo'), ('cow', 'vaca'), ('pig', 'cerdo'), ('rabbit', 'conejo'), ('monkey', 'mono'), ('lion', 'león'), ('elephant', 'elefante'), ('turtle', 'tortuga'), ('frog', 'rana'), ('snake', 'serpiente'), ('butterfly', 'mariposa'), ('sloth', 'perezoso'), ('whale', 'ballena'), ('spider', 'araña'), ('duck', 'pato')],
 'trabajos': [('doctor', 'doctor'), ('nurse', 'enfermera'), ('teacher', 'maestro'), ('engineer', 'ingeniero'), ('farmer', 'agricultor'), ('driver', 'conductor'), ('cook', 'cocinero'), ('police officer', 'policía'), ('firefighter', 'bombero'), ('lawyer', 'abogado'), ('dentist', 'dentista'), ('pilot', 'piloto'), ('artist', 'artista'), ('programmer', 'programador'), ('mechanic', 'mecánico')],
 'verbos': [('eat', 'comer'), ('drink', 'beber'), ('sleep', 'dormir'), ('run', 'correr'), ('walk', 'caminar'), ('read', 'leer'), ('write', 'escribir'), ('listen', 'escuchar'), ('speak', 'hablar'), ('open', 'abrir'), ('close', 'cerrar'), ('buy', 'comprar'), ('sell', 'vender'), ('learn', 'aprender'), ('teach', 'enseñar'), ('give', 'dar'), ('take', 'tomar'), ('wait', 'esperar'), ('forget', 'olvidar'), ('remember', 'recordar'), ('build', 'construir'), ('borrow', 'pedir prestado')],
 'adjetivos': [('big', 'grande'), ('small', 'pequeño'), ('tall', 'alto'), ('short', 'bajo / corto'), ('fast', 'rápido'), ('slow', 'lento'), ('hot', 'caliente'), ('cold', 'frío'), ('new', 'nuevo'), ('old', 'viejo'), ('happy', 'feliz'), ('sad', 'triste'), ('easy', 'fácil'), ('difficult', 'difícil'), ('cheap', 'barato'), ('expensive', 'caro'), ('strong', 'fuerte'), ('weak', 'débil'), ('brave', 'valiente'), ('lazy', 'perezoso'), ('generous', 'generoso'), ('shy', 'tímido')],
 'lugares': [('park', 'parque'), ('beach', 'playa'), ('hospital', 'hospital'), ('market', 'mercado'), ('church', 'iglesia'), ('bank', 'banco'), ('street', 'calle'), ('bridge', 'puente'), ('airport', 'aeropuerto'), ('farm', 'finca'), ('mountain', 'montaña'), ('river', 'río'), ('forest', 'bosque'), ('town', 'pueblo'), ('station', 'estación')],
}
base_d = {'familia': 4, 'comida': 6, 'casa': 10, 'escuela': 12, 'cuerpo': 14, 'ropa': 20, 'animales': 16, 'trabajos': 34, 'verbos': 24, 'adjetivos': 30, 'lugares': 36}
allw = [(g, en, es) for g, items in VOC.items() for en, es in items]
R.shuffle(allw)
for g, en, es in allw:
    items = VOC[g]
    idx = items.index((en, es)); d = base_d[g] + idx
    pool_en = [x[0] for x in items if x[0] != en]; pool_es = [x[1] for x in items if x[1] != es]
    if R.random() < .5:
        B.add('ing6', f'¿Cómo se dice «{es}» en inglés?', en, R.sample(pool_en, 3), d, f'{es} = {en}.', [en])
    else:
        B.add('ing6', f'¿Qué significa «{en}» en español?', es, R.sample(pool_es, 3), d + 2, f'{en} = {es}.', [es])
    if R.random() < .35:
        B.add('ing6', f'Escribe en inglés: «{es}».', en, R.sample(pool_en, 3), d + 8, f'{es} = {en}.', [en])
B.finish(os.path.join(HERE, 'out_ing.json'))
