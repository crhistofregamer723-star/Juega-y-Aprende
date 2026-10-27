from core_ing import *

# (inglés, español, nivel)  — frases de saludo y cortesía
PHR = [
 ("Hello", "Hola", 1), ("Hi", "Hola (informal)", 1), ("Goodbye", "Adiós", 1), ("Bye", "Chao", 1),
 ("Please", "Por favor", 1), ("Thank you", "Gracias", 1), ("Thanks", "Gracias (informal)", 1),
 ("Sorry", "Lo siento", 1), ("Yes", "Sí", 1), ("Good morning", "Buenos días", 1),
 ("Good afternoon", "Buenas tardes", 1), ("Good evening", "Buenas noches (al llegar)", 2),
 ("Good night", "Buenas noches (al despedirse)", 2), ("See you later", "Hasta luego", 1),
 ("See you tomorrow", "Hasta mañana", 1), ("Welcome", "Bienvenido", 1), ("You're welcome", "De nada", 1),
 ("Excuse me", "Con permiso", 2), ("Nice to meet you", "Mucho gusto", 1), ("How are you?", "¿Cómo estás?", 1),
 ("I'm fine, thank you", "Estoy bien, gracias", 1), ("And you?", "¿Y tú?", 1),
 ("What's your name?", "¿Cómo te llamas?", 1), ("Where are you from?", "¿De dónde eres?", 2),
 ("How old are you?", "¿Cuántos años tienes?", 2), ("Where do you live?", "¿Dónde vives?", 3),
 ("Do you speak English?", "¿Hablas inglés?", 3), ("I don't understand", "No entiendo", 2),
 ("Can you repeat that, please?", "¿Puedes repetirlo, por favor?", 3),
 ("Speak slowly, please", "Habla despacio, por favor", 3), ("What time is it?", "¿Qué hora es?", 2),
 ("Have a nice day", "Que tengas un buen día", 2), ("Good luck", "Buena suerte", 2),
 ("Happy birthday", "Feliz cumpleaños", 1), ("Merry Christmas", "Feliz Navidad", 1),
 ("Congratulations", "Felicidades", 2), ("Take care", "Cuídate", 2),
 ("I'm sorry I'm late", "Perdón por llegar tarde", 3), ("Pleased to meet you", "Encantado de conocerte", 3),
 ("How's it going?", "¿Cómo va todo?", 3), ("What's up?", "¿Qué tal?", 3),
 ("Long time no see", "Cuánto tiempo sin verte", 4), ("Make yourself at home", "Siéntete como en casa", 4),
 ("Can I help you?", "¿Puedo ayudarte?", 3), ("Let me introduce myself", "Permíteme presentarme", 4),
 ("This is my friend", "Este es mi amigo", 2), ("Would you like some water?", "¿Quieres un poco de agua?", 3),
 ("Cheers", "Salud (al brindar)", 3), ("Bless you", "Salud (al estornudar)", 3),
 ("I miss you", "Te extraño", 2), ("Don't worry", "No te preocupes", 2), ("No problem", "No hay problema", 2),
 ("It's a pleasure", "Es un placer", 3), ("With pleasure", "Con gusto", 3),
 ("How do you spell your name?", "¿Cómo se deletrea tu nombre?", 4),
 ("What's your phone number?", "¿Cuál es tu número de teléfono?", 3), ("What do you do?", "¿A qué te dedicas?", 4),
 ("I'm a student", "Soy estudiante", 2), ("I work at a hospital", "Trabajo en un hospital", 3),
 ("Where is the bathroom?", "¿Dónde está el baño?", 2), ("I'm lost", "Estoy perdido", 3),
 ("Could you help me, please?", "¿Podría ayudarme, por favor?", 4), ("Pardon?", "¿Perdón? (no escuché)", 3),
 ("I'm hungry", "Tengo hambre", 2), ("I'm thirsty", "Tengo sed", 2), ("I'm tired", "Estoy cansado", 2),
 ("I like it", "Me gusta", 2), ("I love you", "Te quiero", 2), ("Me too", "Yo también", 2),
 ("Of course", "Por supuesto", 2), ("I don't know", "No sé", 2), ("I think so", "Creo que sí", 3),
 ("What's your favorite color?", "¿Cuál es tu color favorito?", 3), ("How much is it?", "¿Cuánto cuesta?", 3),
 ("See you soon", "Nos vemos pronto", 2), ("Say hello to your family", "Saluda a tu familia", 4),
 ("Thank you very much", "Muchas gracias", 1), ("I'm happy to see you", "Me alegra verte", 3),
 ("Nice to see you again", "Gusto en verte de nuevo", 4), ("Enjoy your meal", "Buen provecho", 3),
 ("Get well soon", "Que te mejores pronto", 4), ("Sweet dreams", "Dulces sueños", 3),
 ("Safe travels", "Buen viaje", 3), ("I'm from Costa Rica", "Soy de Costa Rica", 2),
]
PHR_D = {1: 4, 2: 14, 3: 28, 4: 42}

NAMES = ['Ana', 'Carlos', 'Maria', 'Luis', 'Sofia', 'Pedro', 'Laura', 'David', 'Emma', 'Jack', 'Lucy', 'Tom', 'Daniela',
         'Mateo', 'Valeria', 'Diego', 'Camila', 'Andres', 'Paula', 'Jorge', 'Elena', 'Marcos', 'Rosa', 'Hugo', 'Nina',
         'Oscar', 'Julia', 'Pablo', 'Kevin', 'Mia', 'Sam', 'Anna', 'Leo', 'Eva', 'Mark', 'Alice', 'Peter', 'Sara', 'Ben', 'Lola']
COUNTRIES = [('México', 'Mexico'), ('Costa Rica', 'Costa Rica'), ('España', 'Spain'), ('Perú', 'Peru'),
             ('Chile', 'Chile'), ('Brasil', 'Brazil'), ('Canadá', 'Canada'), ('Japón', 'Japan'), ('Italia', 'Italy'),
             ('Francia', 'France'), ('Colombia', 'Colombia'), ('Argentina', 'Argentina'), ('Alemania', 'Germany'),
             ('China', 'China'), ('Panamá', 'Panama'), ('Ecuador', 'Ecuador'), ('Cuba', 'Cuba'), ('Uruguay', 'Uruguay'),
             ('Venezuela', 'Venezuela'), ('Guatemala', 'Guatemala'), ('Honduras', 'Honduras'), ('Nicaragua', 'Nicaragua'),
             ('Bolivia', 'Bolivia'), ('Paraguay', 'Paraguay'), ('Portugal', 'Portugal'), ('Inglaterra', 'England'),
             ('Irlanda', 'Ireland'), ('Rusia', 'Russia'), ('India', 'India'), ('Corea del Sur', 'South Korea'),
             ('Australia', 'Australia'), ('Egipto', 'Egypt'), ('Grecia', 'Greece'), ('Suiza', 'Switzerland'),
             ('Estados Unidos', 'the United States'), ('Turquía', 'Turkey'), ('Holanda', 'the Netherlands'),
             ('Suecia', 'Sweden'), ('Marruecos', 'Morocco'), ('Kenia', 'Kenya')]
FAM = [('madre', 'mother'), ('padre', 'father'), ('hermana', 'sister'), ('hermano', 'brother'), ('abuela', 'grandmother'),
       ('abuelo', 'grandfather'), ('tía', 'aunt'), ('tío', 'uncle'), ('prima', 'cousin'), ('amigo', 'friend'),
       ('esposa', 'wife'), ('esposo', 'husband'), ('hija', 'daughter'), ('hijo', 'son')]

def similar(correct, pool, k=12):
    cw = set(re.findall(r"[a-z']+", correct.lower()))
    sc = []
    for p in pool:
        if p == correct:
            continue
        pw = set(re.findall(r"[a-z']+", p.lower()))
        sc.append((-len(cw & pw), R.random(), p))
    sc.sort()
    return [p for _, _, p in sc[:k]]

def gen():
    C = 'ing1'
    ens = [p[0] for p in PHR]
    ess = [p[1] for p in PHR]
    # 1) traducción en ambos sentidos
    for en, es, lv in PHR:
        d = PHR_D[lv]
        add(C, f'¿Qué significa «{en}» en español?', es, similar_es(es, ess, en, ens), d, f'«{en}» se dice en español: «{es}».',
            acc=[es, es.lower(), re.sub(r'\s*\(.*\)', '', es), re.sub(r'\s*\(.*\)', '', es).lower()][:4])
        add(C, f'¿Cómo se dice «{es}» en inglés?', en, similar(en, ens), d + 2, f'«{es}» en inglés es «{en}».')
    # 2) completar una palabra de la frase
    for en, es, lv in PHR:
        ws = re.findall(r"[A-Za-z']+", en)
        if len(ws) < 2:
            continue
        pool_words = sorted({w.lower() for e in ens for w in re.findall(r"[A-Za-z']+", e) if len(w) > 2})
        idxs = list(range(len(ws)))
        R.shuffle(idxs)
        for i in idxs[:1]:
            w = ws[i]
            if len(w) < 3 or w.lower() in ('the', 'you', 'are'):
                continue
            blank = re.sub(r'\b' + re.escape(w) + r'\b', '___', en, count=1)
            cands = [x for x in pool_words if abs(len(x) - len(w)) <= 3 and x != w.lower()]
            R.shuffle(cands)
            correct = w if w[0].islower() or i > 0 else w
            fixed = [c.capitalize() if i == 0 else c for c in cands[:14]]
            add(C, f'Completa la frase «{blank}» (significa «{es}»).', correct, fixed, PHR_D[lv] + 8,
                f'La frase completa es «{en}».', acc=[correct, correct.lower()])
    # 3) Me llamo ...
    for i, nm in enumerate(NAMES):
        add(C, f'¿Cómo se dice «Me llamo {nm}» en inglés?', f'My name is {nm}',
            [f'I name is {nm}', f'My name are {nm}', f'Me name is {nm}', f'I called {nm}', f'My name {nm}'],
            10 + i * 0.25, f'Para presentarte: «My name is {nm}» (o «I\'m {nm}»).',
            acc=[f'My name is {nm}', f"I'm {nm}", f'I am {nm}', f'my name is {nm.lower()}'])
    # 4) Soy de ...
    for i, (es, en) in enumerate(COUNTRIES):
        add(C, f'¿Cómo se dice «Soy de {es}» en inglés?', f"I'm from {en}",
            [f'I from {en}', f"I'm of {en}", f"I'm at {en}", f'I are from {en}', f'My am from {en}', f'I be from {en}'],
            14 + i * 0.3, f'Para decir tu origen usa «from»: «I\'m from {en}».', acc=[f"I'm from {en}", f'I am from {en}'])
    # 5) Tengo N años
    for n in [5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 28, 30, 31, 35, 38, 40, 42, 45, 50, 55, 60, 65, 70, 75, 80]:
        add(C, f'¿Cómo se dice «Tengo {n} años» en inglés?', f"I'm {n} years old",
            [f'I have {n} years', f'I have {n} years old', f"I'm {n} years", f'I am have {n} years old', f"I'm {n} year old"],
            26 + n * 0.12, 'En inglés la edad se dice con el verbo «to be» (am), no con «have».',
            acc=[f"I'm {n} years old", f'I am {n} years old', f"I'm {n}", f'I am {n}'])
    # 6) Presentar a un familiar
    for es, en in FAM:
        add(C, f'Presentas a tu {es}: ¿qué dices? (Este es mi {es}…)'.replace('Este es mi', 'Esta es mi' if es in ('madre', 'hermana', 'abuela', 'tía', 'prima', 'esposa', 'hija') else 'Este es mi'),
            f'This is my {en}', [f'This are my {en}', f'These is my {en}', f'Here are my {en}', f'This is mine {en}', f'This my {en}'], 22,
            'Para presentar a una persona usa «This is my…».', acc=[f'This is my {en}', f'this is my {en}.'])
    # 7) Saludo según la hora
    for h12, ap, g in [(6, 'de la mañana', 'Good morning'), (7, 'de la mañana', 'Good morning'), (8, 'de la mañana', 'Good morning'),
                       (9, 'de la mañana', 'Good morning'), (10, 'de la mañana', 'Good morning'), (11, 'de la mañana', 'Good morning'),
                       (1, 'de la tarde', 'Good afternoon'), (2, 'de la tarde', 'Good afternoon'), (3, 'de la tarde', 'Good afternoon'),
                       (4, 'de la tarde', 'Good afternoon'), (5, 'de la tarde', 'Good afternoon'),
                       (6, 'de la noche', 'Good evening'), (7, 'de la noche', 'Good evening'), (8, 'de la noche', 'Good evening')]:
        add(C, f'Son las {h12}:00 {ap} y llegas a clase. ¿Qué saludo usas?', g,
            ['Good morning', 'Good afternoon', 'Good evening', 'Good night', 'Goodbye'], 18 if g != 'Good evening' else 30,
            {'Good morning': 'Good morning se usa desde el amanecer hasta el mediodía.',
             'Good afternoon': 'Good afternoon se usa desde el mediodía hasta el atardecer.',
             'Good evening': 'Good evening se usa para saludar al llegar en la noche.'}[g])
    for h12 in (10, 11):
        add(C, f'Son las {h12}:00 de la noche y te vas a dormir. ¿Qué dices al despedirte?', 'Good night',
            ['Good morning', 'Good afternoon', 'Good evening', 'Hello', 'Good day'], 32, 'Good night se usa para despedirse en la noche.')
    # 8) Situaciones
    SIT = [
     ('Alguien te da un regalo. ¿Qué dices?', 'Thank you', ['Sorry', 'Goodbye', 'Excuse me'], 8, 'Thank you = gracias.'),
     ('Pisas a alguien sin querer. ¿Qué dices?', 'Sorry', ['Thank you', 'Welcome', 'Congratulations'], 8, 'Sorry = lo siento.'),
     ('Te dan las gracias. ¿Qué respondes?', "You're welcome", ['Good night', 'Excuse me', 'Congratulations'], 12, "You're welcome = de nada."),
     ('Alguien cumple años. ¿Qué le dices?', 'Happy birthday', ['Good luck', 'Good night', 'Take care'], 8, 'Happy birthday = feliz cumpleaños.'),
     ('Tu amigo tiene un examen mañana. ¿Qué le deseas?', 'Good luck', ['Happy birthday', 'Welcome', 'Excuse me'], 14, 'Good luck = buena suerte.'),
     ('Quieres pasar entre dos personas. ¿Qué dices?', 'Excuse me', ['Good luck', 'Cheers', 'Congratulations'], 16, 'Excuse me = con permiso / disculpe.'),
     ('Alguien llega a tu casa por primera vez. ¿Qué le dices?', 'Welcome', ['Goodbye', 'Sorry', 'Good night'], 10, 'Welcome = bienvenido.'),
     ('Tu compañero ganó un premio. ¿Qué le dices?', 'Congratulations', ['Excuse me', 'Take care', 'Sorry'], 18, 'Congratulations = felicidades.'),
     ('Alguien estornuda. ¿Qué le dices?', 'Bless you', ['Good luck', 'Cheers', 'Welcome'], 26, 'Bless you se dice cuando alguien estornuda.'),
     ('Levantas un vaso para brindar. ¿Qué dices?', 'Cheers', ['Bless you', 'Sorry', 'Good morning'], 26, 'Cheers se usa al brindar.'),
     ('No oíste lo que dijo tu profesor. ¿Qué dices?', 'Pardon?', ['Welcome', 'Cheers', 'Good luck'], 28, 'Pardon? sirve para pedir que repitan algo.'),
     ('Te presentan a alguien por primera vez. ¿Qué dices?', 'Nice to meet you', ['See you later', 'Good night', "You're welcome"], 12, 'Nice to meet you = mucho gusto.'),
     ('Te despides de un amigo y lo verás más tarde hoy. ¿Qué dices?', 'See you later', ['Good morning', 'Welcome', 'Nice to meet you'], 10, 'See you later = hasta luego.'),
     ('Un amigo te cuenta que está enfermo. ¿Qué le deseas?', 'Get well soon', ['Happy birthday', 'Cheers', 'Welcome'], 40, 'Get well soon = que te mejores pronto.'),
     ('Alguien se va de viaje. ¿Qué le deseas?', 'Safe travels', ['Bless you', 'Sweet dreams', 'Welcome'], 40, 'Safe travels = buen viaje.'),
     ('Vas a comer con tu familia. ¿Qué dices antes de empezar?', 'Enjoy your meal', ['Good night', 'Excuse me', 'Take care'], 36, 'Enjoy your meal = buen provecho.'),
     ('Llegas tarde a clase. ¿Qué le dices al profesor?', "I'm sorry I'm late", ["You're welcome", 'Congratulations', 'Good luck'], 34, "I'm sorry I'm late = perdón por llegar tarde."),
     ('No entiendes una palabra. ¿Qué dices?', "I don't understand", ['I understand', 'I love you', "I'm fine"], 20, "I don't understand = no entiendo."),
     ('Necesitas que hablen más lento. ¿Qué dices?', 'Speak slowly, please', ['Speak loudly, please', 'Come here, please', 'Sit down, please'], 38, 'Speak slowly, please = habla despacio, por favor.'),
     ('Quieres saber el nombre de alguien. ¿Qué preguntas?', "What's your name?", ['Where are you from?', 'How old are you?', 'How are you?'], 10, "What's your name? = ¿cómo te llamas?"),
     ('Quieres saber de qué país es alguien. ¿Qué preguntas?', 'Where are you from?', ["What's your name?", 'How old are you?', 'What time is it?'], 14, 'Where are you from? = ¿de dónde eres?'),
     ('Quieres saber la edad de un niño. ¿Qué preguntas?', 'How old are you?', ['How are you?', 'Where are you from?', "What's your name?"], 14, 'How old are you? = ¿cuántos años tienes?'),
     ('Quieres saber cómo se siente alguien. ¿Qué preguntas?', 'How are you?', ['How old are you?', "What's your name?", 'Where do you live?'], 8, 'How are you? = ¿cómo estás?'),
     ('Quieres saber la hora. ¿Qué preguntas?', 'What time is it?', ['What is your name?', 'How much is it?', 'Where is the bathroom?'], 16, 'What time is it? = ¿qué hora es?'),
     ('Estás buscando el baño. ¿Qué preguntas?', 'Where is the bathroom?', ['What time is it?', 'How much is it?', 'Where are you from?'], 18, 'Where is the bathroom? = ¿dónde está el baño?'),
     ('En una tienda quieres saber el precio. ¿Qué preguntas?', 'How much is it?', ['What time is it?', 'How old is it?', 'Where is it?'], 22, 'How much is it? = ¿cuánto cuesta?'),
     ('Alguien te pregunta «How are you?». ¿Cuál es una buena respuesta?', "I'm fine, thank you", ['My name is Ana', "I'm ten years old", "I'm from Peru"], 12, "I'm fine, thank you = estoy bien, gracias."),
     ('Alguien te pregunta «What\'s your name?». ¿Cuál es una buena respuesta?', 'My name is Ana', ["I'm fine, thank you", "I'm ten years old", 'See you later'], 12, 'My name is… = me llamo…'),
     ('Alguien te pregunta «Where are you from?». ¿Cuál es una buena respuesta?', "I'm from Peru", ['My name is Ana', "I'm fine", "I'm ten years old"], 16, "I'm from… = soy de…"),
     ('Alguien te pregunta «How old are you?». ¿Cuál es una buena respuesta?', "I'm ten years old", ["I'm from Peru", 'My name is Ana', 'Nice to meet you'], 16, "I'm … years old = tengo … años."),
     ('Alguien te dice «Nice to meet you». ¿Qué respondes?', 'Nice to meet you too', ["You're welcome", 'Good night', 'I\'m sorry'], 18, 'Nice to meet you too = igualmente, mucho gusto.'),
     ('Alguien te dice «Thank you». ¿Qué respondes?', "You're welcome", ['Nice to meet you', 'Good morning', 'See you later'], 12, "You're welcome = de nada."),
     ('Alguien te dice «Good morning». ¿Qué respondes?', 'Good morning', ['Good night', 'Goodbye', 'Thank you'], 6, 'Se responde con el mismo saludo.'),
     ('Alguien te dice «See you tomorrow». ¿Qué respondes?', 'See you', ['Good morning', 'Nice to meet you', "You're welcome"], 20, 'Puedes responder «See you» o «See you tomorrow».'),
     ('Alguien te pregunta «Do you speak English?». ¿Cuál es una respuesta correcta?', 'Yes, a little', ['Yes, I am', 'No, I\'m fine', 'Yes, thank you very much'], 30, 'Yes, a little = sí, un poco.'),
     ('¿Cuál es la forma más formal de pedir ayuda?', 'Could you help me, please?', ['Help me!', 'Hey, you!', 'What\'s up?'], 44, 'Could you… es una forma cortés de pedir algo.'),
     ('¿Cuál saludo es más informal?', "What's up?", ['Good morning', 'How do you do?', 'Good evening'], 40, "What's up? se usa entre amigos."),
     ('¿Cuál saludo es más formal?', 'Good evening', ["What's up?", 'Hi', 'Hey'], 40, 'Good evening es más formal que Hi o Hey.'),
     ('¿Qué palabra usas para pedir algo de forma amable?', 'Please', ['Sorry', 'Welcome', 'Cheers'], 6, 'Please = por favor.'),
     ('¿Qué palabra usas para disculparte?', 'Sorry', ['Please', 'Welcome', 'Hello'], 6, 'Sorry = lo siento.'),
    ]
    for q, a, w, d, e in SIT:
        add(C, q, a, w, d, e)
    # 9) diálogos para completar
    DLG = [
     ('«Hello! ___ are you?» — «I\'m fine, thanks.»', 'How', ['What', 'Where', 'Who'], 10),
     ('«What ___ your name?» — «My name is Luis.»', 'is', ['are', 'am', 'be'], 14),
     ('«Where ___ you from?» — «I\'m from Chile.»', 'are', ['is', 'am', 'do'], 14),
     ('«___ old are you?» — «I\'m twelve.»', 'How', ['What', 'Where', 'Who'], 14),
     ('«Nice to ___ you.» — «Nice to meet you too.»', 'meet', ['see', 'meat', 'met'], 16),
     ('«Good ___, class!» (son las 8 a. m.)', 'morning', ['night', 'afternoon', 'evening'], 8),
     ('«See you ___!» (hasta mañana)', 'tomorrow', ['yesterday', 'morning', 'before'], 14),
     ('«Thank you!» — «You\'re ___.»', 'welcome', ['sorry', 'please', 'goodbye'], 12),
     ('«___ me, where is the library?»', 'Excuse', ['Sorry', 'Thank', 'Please'], 20),
     ('«Have a nice ___!» (que tengas un buen día)', 'day', ['night', 'morning', 'time'], 18),
     ('«My name ___ Ana and I ___ ten years old.»', 'is / am', ['is / is', 'am / am', 'are / are'], 30),
     ('«I ___ from Mexico. I ___ a student.»', 'am / am', ['is / is', 'am / are', 'are / am'], 28),
     ('«How ___ you today?» — «Great, thanks!»', 'are', ['is', 'am', 'do'], 12),
     ('«Hi, I\'m Tom. ___ your name?»', "What's", ['Who\'s', 'How\'s', 'Where\'s'], 14),
     ('«Goodbye! See you ___.» (más tarde)', 'later', ['before', 'last', 'ago'], 14),
     ('«I\'m ___ to meet you.» (Encantado de conocerte)', 'pleased', ['please', 'pleasing', 'pleasure'], 40),
     ('«Can you ___ that, please?» (repetirlo)', 'repeat', ['repair', 'respond', 'return'], 30),
     ('«I don\'t ___.» (No entiendo)', 'understand', ['understood', 'understanding', 'under'], 24),
     ('«___ is my friend Sara.» (Esta es…)', 'This', ['These', 'Those', 'They'], 22),
     ('«Long time no ___!» (cuánto tiempo sin verte)', 'see', ['saw', 'seen', 'look'], 44),
     ('«What\'s your phone ___?»', 'number', ['name', 'age', 'color'], 24),
     ('«Where do you ___?» (¿Dónde vives?)', 'live', ['lives', 'living', 'life'], 28),
     ('«Make yourself ___ home.»', 'at', ['in', 'on', 'to'], 46),
     ('«I\'m sorry ___ I\'m late.»', "that", ['for', 'to', 'at'], 40),
    ]
    for q, a, w, d in DLG:
        add(C, 'Completa el diálogo: ' + q, a, w, d, 'Revisa el saludo o la pregunta básica: «' + q.replace('___', a) + '».')
    # 10) frase equivocada
    BAD = [
     ('¿Cuál saludo es correcto?', 'Good morning', ['Good morn', 'Goods morning', 'Good mornings'], 10),
     ('¿Cuál está bien escrita?', 'Goodbye', ['Goodby', 'Good-bay', 'Godbye'], 12),
     ('¿Cuál está bien escrita?', 'Welcome', ['Wellcome', 'Welcom', 'Welkome'], 14),
     ('¿Cuál está bien escrita?', 'Please', ['Pleas', 'Pleese', 'Pliese'], 14),
     ('¿Cuál está bien escrita?', 'Thank you', ['Tank you', 'Thank yu', 'Thanc you'], 12),
     ('¿Cuál está bien escrita?', 'Excuse me', ['Excuze me', 'Exkuse me', 'Excus me'], 22),
     ('¿Cuál está bien escrita?', 'Nice to meet you', ['Nice to meat you', 'Nise to meet you', 'Nice too meet you'], 26),
     ('¿Cuál está bien escrita?', 'Congratulations', ['Congratulation', 'Congradulations', 'Congrachulations'], 40),
     ('¿Cuál oración es correcta?', 'How are you?', ['How is you?', 'How you are?', 'How am you?'], 16),
     ('¿Cuál oración es correcta?', 'What is your name?', ['What are your name?', 'What your name is?', 'Who is your name?'], 22),
     ('¿Cuál oración es correcta?', 'Where are you from?', ['Where you are from?', 'Where is you from?', 'From where you are?'], 26),
     ('¿Cuál oración es correcta?', "I'm fine, thank you.", ["I fine, thank you.", "I'm fine, thanks you.", "Me fine, thank you."], 22),
     ('¿Cuál oración es correcta?', 'Nice to meet you.', ['Nice to met you.', 'Nice meet you.', 'Nice to meeting you.'], 24),
     ('¿Cuál oración es correcta?', 'Do you speak English?', ['You speak English do?', 'Speak you English?', 'Are you speak English?'], 34),
     ('¿Cuál oración es correcta?', 'I don\'t understand.', ['I no understand.', 'I not understand.', 'I don\'t understanding.'], 34),
     ('¿Cuál oración es correcta?', 'See you tomorrow.', ['See you tomorow.', 'Saw you tomorrow.', 'See to you tomorrow.'], 24),
     ('¿Cuál oración es correcta?', 'Happy birthday!', ['Happy birth day!', 'Happy birthdai!', 'Happy bird day!'], 18),
     ('¿Cuál oración es correcta?', 'Where do you live?', ['Where you live?', 'Where does you live?', 'Where live you?'], 40),
     ('¿Cuál oración es correcta?', 'Can you repeat that, please?', ['Can you repeating that, please?', 'You can repeat that, please?', 'Can you to repeat that, please?'], 46),
     ('¿Cuál oración es correcta?', 'Let me introduce myself.', ['Let me introduce me.', 'Let me to introduce myself.', 'Let I introduce myself.'], 52),
    ]
    for q, a, w, d in BAD:
        add(C, q + ' (' + a[:3] + '…)' if False else q + ' «' + a[0] + '…»' if len(a) > 0 and False else q, a, w, d, 'La forma correcta es «' + a + '».')

def similar_es(es, ess, en, ens):
    base = [e for e in ess if e != es]
    R.shuffle(base)
    return base[:12]
