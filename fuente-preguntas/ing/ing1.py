# -*- coding: utf-8 -*-
import random
from common import *

# (en, es, tema, grupo, aceptadas_en_extra, es_alt, explicación)
LEX = [
("Hello","Hola","greet","hello",["hi"],[],"Hello es el saludo estándar; Hi es la versión informal."),
("Good morning","Buenos días","greet","gm",[],[],"Good morning se usa desde que amanece hasta el mediodía."),
("Good afternoon","Buenas tardes","greet","ga",[],[],"Good afternoon se usa después del mediodía y hasta el atardecer."),
("Good evening","Buenas noches (como saludo al llegar de noche)","greet","ge",[],["buenas noches"],"Good evening es un saludo para la noche; no se usa para despedirse."),
("Good night","Buenas noches (para despedirse e ir a dormir)","bye","gn",[],["buenas noches"],"Good night es una despedida; se dice antes de dormir o al irse de noche."),
("How are you?","¿Cómo estás?","greet","how",["how are you"],[],"Es la pregunta más común para saludar. Se responde I am fine, thank you."),
("How are you doing?","¿Cómo te va?","greet","how",[],[],"How are you doing? es una variante un poco más informal de How are you?"),
("How is it going?","¿Cómo va todo?","greet","how",["how's it going"],[],"How is it going? es una forma informal de preguntar cómo estás."),
("Welcome","Bienvenido","greet","welc",[],["bienvenida","bienvenidos","bienvenido"],"Welcome se usa para recibir a alguien."),
("Nice to see you","Qué gusto verte","greet","see",["good to see you"],[],"Nice to see you se dice a alguien que ya conoces."),
("Long time no see","Cuánto tiempo sin verte","greet","ltns",[],[],"Es una frase informal para saludar a alguien que no ves hace mucho."),
("Nice to meet you","Mucho gusto","meet","meet",["pleased to meet you"],["encantado","encantada"],"Nice to meet you se dice al conocer a alguien por primera vez."),
("Nice to meet you, too","Igualmente, mucho gusto","meet","meet",["pleased to meet you too","nice to meet you too"],[],"Too significa «también» y va al final de la frase."),
("Goodbye","Adiós","bye","bye",["bye"],[],"Goodbye es la despedida estándar; Bye es la forma corta."),
("Bye","Chao","bye","bye",["goodbye"],["adiós","chau"],"Bye es la despedida corta e informal."),
("See you later","Hasta luego","bye","seeyou",["see you"],[],"Se usa al despedirte de alguien que verás pronto."),
("See you soon","Hasta pronto","bye","seeyou",[],[],"Soon significa «pronto»."),
("See you tomorrow","Hasta mañana","bye","tomorrow",[],[],"Tomorrow significa «mañana» (el día siguiente)."),
("See you next week","Nos vemos la próxima semana","bye","nextweek",[],["hasta la próxima semana"],"Next week significa «la próxima semana»."),
("Have a nice day","Que tengas un buen día","bye","nice",["have a good day"],[],"Se dice al despedirte, deseando un buen día."),
("Have a good weekend","Que tengas un buen fin de semana","bye","wkend",[],[],"Weekend significa «fin de semana»."),
("Take care","Cuídate","bye","care",[],["cuídese"],"Take care se usa al despedirse de alguien con cariño."),
("Thank you","Gracias","polite","thx",["thanks"],[],"Thanks es la versión corta e informal."),
("Thank you very much","Muchas gracias","polite","thx",["thanks a lot","thank you so much"],[],"Very much refuerza el agradecimiento."),
("Thanks a lot","Muchísimas gracias","polite","thx",["thank you very much","thank you so much"],[],"A lot refuerza el agradecimiento de forma informal."),
("Please","Por favor","polite","please",[],[],"Please se usa para pedir algo con cortesía."),
("You are welcome","De nada","polite","welcome2",["you're welcome","your welcome"],[],"Es la respuesta habitual a Thank you."),
("Sorry","Lo siento","polite","apol",["i am sorry","i'm sorry"],["perdón","perdona"],"Sorry sirve para pedir disculpas."),
("Excuse me","Con permiso","polite","apol",[],["disculpe","disculpa","perdón"],"Excuse me se usa para llamar la atención o pasar entre personas."),
("That is OK","No importa","polite","ok",["that's ok","it's ok","its ok","it is ok","that's okay"],["está bien"],"Se responde así cuando alguien se disculpa."),
("Don't worry","No te preocupes","polite","ok",["do not worry","dont worry"],["no se preocupe"],"Don't worry tranquiliza a la otra persona."),
("Good luck","Buena suerte","wish","luck",[],[],"Good luck se dice antes de un examen o un reto."),
("Happy birthday","Feliz cumpleaños","wish","bday",[],[],"Se dice el día del cumpleaños."),
("Congratulations","Felicitaciones","wish","congrats",["congrats"],["felicidades"],"Se usa para felicitar por un logro."),
("Merry Christmas","Feliz Navidad","wish","xmas",[],[],"Merry es una palabra propia de la Navidad."),
("Happy New Year","Feliz Año Nuevo","wish","ny",[],[],"Se dice alrededor del 1 de enero."),
("Get well soon","Que te mejores pronto","wish","well",[],["que te recuperes pronto"],"Se dice a alguien que está enfermo."),
("Enjoy your meal","Buen provecho","wish","meal",["enjoy your food"],[],"Se dice a quien va a comer."),
("Bless you","Salud (cuando alguien estornuda)","wish","bless",[],["salud"],"Bless you se dice después de un estornudo."),
]
SURV = [
("I don't understand","No entiendo","nu",["i do not understand","i dont understand"],[],"Don't es la forma corta de do not."),
("I don't know","No sé","nk",["i do not know","i dont know"],[],"I don't know es la respuesta cuando no tienes la información."),
("Can you repeat that, please?","¿Puedes repetir eso, por favor?","rep",["can you repeat that please","could you repeat that please"],[],"Repeat significa «repetir»."),
("Please speak slowly","Habla despacio, por favor","slow",["speak slowly please","please speak slowly"],[],"Slowly significa «despacio»."),
("Do you speak English?","¿Hablas inglés?","sp1",["do you speak english"],[],"Las preguntas con speak empiezan con Do you."),
("Do you speak Spanish?","¿Hablas español?","sp2",["do you speak spanish"],[],"Spanish es español; los idiomas llevan mayúscula en inglés."),
("I speak a little English","Hablo un poco de inglés","sp3",["i speak a little english","i speak some english"],[],"A little significa «un poco»."),
("Where is the bathroom?","¿Dónde está el baño?","bath",["where is the bathroom","where is the restroom","where's the bathroom"],[],"Bathroom es baño; en EE. UU. también se dice restroom."),
("Where is the bank?","¿Dónde está el banco?","bank",["where is the bank","where's the bank"],[],"Where is... sirve para preguntar por un lugar."),
("Where is the bus stop?","¿Dónde está la parada de autobús?","bus",["where is the bus stop","where's the bus stop"],[],"Bus stop es parada de autobús."),
("I need help","Necesito ayuda","help1",["i need help"],[],"Need significa «necesitar»."),
("Can you help me, please?","¿Puedes ayudarme, por favor?","help2",["can you help me please","could you help me please"],[],"Help me significa «ayúdame»."),
("How much is it?","¿Cuánto cuesta?","price",["how much is it","how much does it cost"],[],"How much is it? se usa para preguntar el precio."),
("I am lost","Estoy perdido","lost",["i'm lost","i am lost","im lost"],["estoy perdida"],"Lost significa «perdido»."),
("What time is it?","¿Qué hora es?","time",["what time is it","what's the time"],[],"What time is it? pregunta la hora."),
("How do you spell your name?","¿Cómo se escribe tu nombre?","spell",["how do you spell your name"],[],"Spell significa «deletrear»."),
("What does this word mean?","¿Qué significa esta palabra?","mean",["what does this word mean"],[],"Mean significa «significar»."),
("Can I have some water, please?","¿Me das un poco de agua, por favor?","water",["can i have some water please","could i have some water please"],[],"Can I have... se usa para pedir algo con cortesía."),
("I would like a coffee, please","Quisiera un café, por favor","coffee",["i would like a coffee please","i'd like a coffee please","i'd like a coffee, please"],[],"I would like es una forma educada de pedir algo."),
("Can I sit here?","¿Puedo sentarme aquí?","sit",["can i sit here","may i sit here"],[],"Sit significa «sentarse»."),
("Come in, please","Pasa, por favor","comein",["come in please"],[],"Come in significa «pasa» o «entre»."),
("Sit down, please","Siéntate, por favor","sitdown",["sit down please"],[],"Sit down significa «siéntate»."),
("Just a moment, please","Un momento, por favor","moment",["just a moment please","one moment please","one moment, please"],[],"Moment significa «momento»."),
("Wait here, please","Espera aquí, por favor","wait",["wait here please"],[],"Wait significa «esperar»."),
("Let's go","Vamos","go",["let us go","lets go"],[],"Let's es la contracción de let us."),
("What is your phone number?","¿Cuál es tu número de teléfono?","phone",["what is your phone number","what's your phone number"],[],"Phone number es número de teléfono."),
("What is your last name?","¿Cuál es tu apellido?","last",["what is your last name","what's your last name"],[],"Last name es apellido; first name es nombre."),
("Where do you live?","¿Dónde vives?","live",["where do you live"],[],"Live significa «vivir»."),
("I live in Costa Rica","Vivo en Costa Rica","live2",["i live in costa rica"],[],"Para decir dónde vives se usa live in."),
("Can you write it down, please?","¿Puedes escribirlo, por favor?","write",["can you write it down please","could you write it down please"],[],"Write it down significa «escríbelo»."),
("Be careful!","¡Ten cuidado!","care2",["be careful"],[],"Careful significa «cuidadoso»."),
("Hurry up!","¡Apúrate!","hurry",["hurry up"],[],"Hurry up significa «date prisa»."),
("Call the police!","¡Llama a la policía!","police",["call the police"],[],"Police es policía."),
("I feel sick","Me siento enfermo","sick",["i feel sick","i feel ill"],["me siento enferma","me siento mal"],"Sick significa «enfermo»."),
("I don't speak English very well","No hablo muy bien inglés","sp4",["i do not speak english very well","i dont speak english very well"],[],"Very well significa «muy bien»."),
]

ES_FR = ["¿Cómo se dice «{x}» en inglés?","Elige la traducción al inglés de «{x}».","Traduce al inglés: «{x}»","¿Cuál es la forma de decir «{x}» en inglés?","En inglés, «{x}» se dice…"]
EN_FR = ["¿Qué significa «{x}»?","Elige la traducción al español de «{x}».","«{x}» en español es…","Traduce al español: «{x}»","¿Qué quiere decir «{x}»?"]

def acc_es(a, alts=()):
    out = [a, a.lstrip("¿¡")] + list(alts)
    out += [x for x in [o.replace("¿","").replace("¡","") for o in out]]
    return list(dict.fromkeys(out))

def build(B):
    ex = []
    # ---- A1/B1 traducciones de saludos y cortesía ----
    def lexrows(items, fam_es, fam_en, d0, d1, dd):
        n = len(items)
        for i, (en, es, th, grp, acc, esalt, exp) in enumerate(items):
            rng = random.Random(en)
            others = [x for x in items if x[3] != grp]
            # ES -> EN
            wr = [x[0] for x in rng.sample(others, min(8, len(others)))]
            B.add(fam_es, ES_FR[i % 5].format(x=es), en, wr, accept_variants(en) + acc, exp, lerp(i, n, d0, d1))
    def lexrows_en(items, fam, d0, d1):
        n = len(items)
        for i, (en, es, th, grp, acc, esalt, exp) in enumerate(items):
            rng = random.Random("es" + en)
            others = [x for x in items if x[3] != grp]
            wr = [x[1] for x in rng.sample(others, min(8, len(others)))]
            B.add(fam, EN_FR[(i + 2) % 5].format(x=en), es, wr, acc_es(es, esalt), exp, lerp(i, n, d0, d1))
    basic = LEX
    basic_a = [x for x in basic if x[0] not in ("Nice to meet you, too","Bless you","Enjoy your meal")]
    lexrows(basic_a, "A_es_basico", None, 3, 38, 0)
    lexrows_en(LEX, "B_en_basico", 4, 40)
    # supervivencia
    sv = [(en, es, "surv", g, acc, alt, exp) for (en, es, g, acc, alt, exp) in SURV]
    sv_en = [(en, es, "surv", g, [], alt, exp) for (en, es, g, acc, alt, exp) in SURV]
    n = len(sv)
    for i, (en, es, th, g, acc, alt, exp) in enumerate(sv):
        rng = random.Random("sv" + en)
        others = [x for x in sv if x[3] != g]
        B.add("C_es_superv", ES_FR[(i + 1) % 5].format(x=es), en, [x[0] for x in rng.sample(others, 8)], list(dict.fromkeys(accept_variants(en) + acc)), exp, lerp(i, n, 22, 55))
    for i, (en, es, th, g, acc, alt, exp) in enumerate(sv):
        if i % 2 == 0 and i < 36:
            rng = random.Random("svx" + en)
            others = [x for x in sv if x[3] != g]
            B.add("D_en_superv", EN_FR[(i + 3) % 5].format(x=en), es, [x[1] for x in rng.sample(others, 8)], acc_es(es, alt), exp, lerp(i, n, 25, 58))

    # ---- diálogos ----
    REP = {"fine":"I'm fine, thank you.","name":"My name is Sam.","welcome":"You're welcome.","meet":"Nice to meet you, too.",
           "morning":"Good morning!","afternoon":"Good afternoon!","evening":"Good evening!","night":"Good night!",
           "bye":"Goodbye!","thanks":"Thank you!","age":"I am 12 years old.","origin":"I am from Peru.","sorry":"That's OK.","accept":"Yes, please."}
    DIAL = [
     # prompt, compat, correct replies, nota
     ("How are you?",{"fine"},["I'm fine, thank you.","I'm great, thanks.","Not bad, thank you."],""),
     ("How are you doing?",{"fine"},["I'm doing well, thanks.","I'm fine, thank you."],""),
     ("How is it going?",{"fine"},["Pretty good, thanks.","Not bad, thank you."],""),
     ("Are you OK?",{"fine"},["Yes, I'm fine, thanks.","Yes, I am fine, thank you."],""),
     ("How are you today?",{"fine"},["I'm very well, thank you.","I'm fine, thanks."],""),
     ("What is your name?",{"name"},["My name is Lucy.","I'm Lucy.","My name is Mark."],""),
     ("What's your name, please?",{"name"},["My name is Daniel.","I am Daniel."],""),
     ("May I have your name, please?",{"name"},["Yes, my name is Elena.","My name is Elena."],""),
     ("Thank you!",{"welcome","thanks","sorry"},["You're welcome."],""),
     ("Thank you very much!",{"welcome","thanks","sorry"},["You're welcome.","My pleasure."],""),
     ("Thanks for your help!",{"welcome","thanks","sorry"},["You're welcome.","No problem."],""),
     ("Thanks a lot!",{"welcome","thanks","sorry"},["You're welcome.","Anytime."],""),
     ("Nice to meet you.",{"meet","name"},["Nice to meet you, too."],""),
     ("Pleased to meet you.",{"meet","name"},["Pleased to meet you, too.","Nice to meet you, too."],""),
     ("Nice to meet you. I'm Ana.",{"meet","name"},["Nice to meet you, too, Ana.","Nice to meet you, Ana."],""),
     ("Good morning!",{"morning","fine"},["Good morning!","Good morning! How are you?"],""),
     ("Good morning, class!",{"morning","fine"},["Good morning, teacher!"],""),
     ("Good afternoon!",{"afternoon","fine"},["Good afternoon!","Good afternoon! How are you?"],""),
     ("Good afternoon, Mr. Lee.",{"afternoon","fine"},["Good afternoon, Ms. Smith.","Good afternoon, Mr. Lee."],""),
     ("Good evening!",{"evening","fine"},["Good evening!","Good evening! Welcome."],""),
     ("Good evening, ma'am.",{"evening","fine"},["Good evening, sir."],""),
     ("Good night!",{"night"},["Good night!","Good night! Sleep well."],""),
     ("Goodbye!",{"bye"},["Goodbye!","Bye!"],""),
     ("Bye!",{"bye"},["Bye!","Goodbye!","See you!"],""),
     ("See you tomorrow!",{"bye"},["See you!","See you tomorrow!","Bye!"],""),
     ("See you later!",{"bye"},["See you!","Bye!","See you later!"],""),
     ("See you on Monday!",{"bye"},["See you on Monday!","Bye, see you!"],""),
     ("Have a nice day!",{"bye","thanks"},["You too!","Thanks, you too!"],""),
     ("Have a good weekend!",{"bye","thanks"},["You too!","Thanks, you too!"],""),
     ("Take care!",{"bye","thanks"},["You too!","Thanks, you too!"],""),
     ("Happy birthday!",{"thanks"},["Thank you!","Thanks a lot!"],""),
     ("Good luck!",{"thanks"},["Thank you!","Thanks!"],""),
     ("Congratulations!",{"thanks"},["Thank you!","Thanks a lot!"],""),
     ("Merry Christmas!",{"thanks","bye"},["Merry Christmas to you, too!","You too!"],""),
     ("Happy New Year!",{"thanks","bye"},["Happy New Year to you, too!","You too!"],""),
     ("I'm sorry I'm late.",{"sorry"},["That's OK.","No problem.","Don't worry."],""),
     ("Sorry!",{"sorry"},["That's OK.","No problem."],""),
     ("Oh, sorry! I didn't see you.",{"sorry"},["It's OK.","Don't worry."],""),
     ("I'm sorry about that.",{"sorry"},["It's OK, don't worry.","That's all right."],""),
     ("How old are you?",{"age"},["I am 15 years old.","I'm 30 years old."],""),
     ("Where are you from?",{"origin"},["I am from Chile.","I'm from Spain."],""),
     ("Would you like some tea?",{"accept","thanks"},["Yes, please."],"Quieres aceptar la oferta."),
     ("Would you like some water?",{"accept","thanks"},["Yes, please."],"Quieres aceptar la oferta."),
    ]
    frames = ["Completa el diálogo. A: «{p}» B: «___»{n}","Elige la respuesta adecuada a «{p}»{n}","Alguien te dice: «{p}»{n}. ¿Qué respondes?","Tu amigo dice «{p}»{n}. ¿Cuál es la mejor respuesta?"]
    nD = len(DIAL)
    for i, (p, compat, corr, note) in enumerate(DIAL):
        nt = f" ({note})" if note else ""
        for j, c in enumerate(corr[:2]):
            rng = random.Random(p + c)
            wr = [REP[t] for t in REP if t not in compat]
            fr = frames[(i + j * 2) % 4]
            q = fr.format(p=p, n=nt)
            accs = accept_variants(c)
            B.add("E_dialogo", q, c, wr, accs, "Responde según el tipo de frase: saludo con saludo, gracias con «You are welcome», disculpa con «That is OK».", lerp(i, nD, 28, 66) + j * 2)

    # ---- hora del día ----
    times = {
     "Good morning":["6:00 a. m.","7:30 a. m.","9:00 a. m.","10:45 a. m.","11:15 a. m."],
     "Good afternoon":["1:00 p. m.","2:30 p. m.","3:45 p. m.","4:15 p. m."],
     "Good evening":["6:30 p. m.","7:00 p. m.","8:00 p. m.","8:45 p. m."],
    }
    who = ["tu maestra","un vecino","tus compañeros","la gerente del hotel","tus abuelos","el conductor del autobús","una cliente","tu entrenador"]
    exp_t = {"Good morning":"Good morning se usa por la mañana, hasta el mediodía.","Good afternoon":"Good afternoon se usa desde el mediodía hasta el atardecer.","Good evening":"Good evening se usa al llegar o encontrarse con alguien de noche."}
    tmpl = ["Son las {t} y te encuentras con {w}. ¿Qué saludo usas?","Llegas a las {t} y saludas a {w}. ¿Qué dices?","A las {t}, {w} te saluda. ¿Cómo le respondes con el saludo correcto?"]
    allg = ["Good morning","Good afternoon","Good evening","Good night"]
    k = 0; ds = []
    items = []
    for g, ts in times.items():
        for t in ts:
            items.append((g, t))
    random.Random(7).shuffle(items)
    for i, (g, t) in enumerate(items):
        w = who[i % len(who)]
        base = {"Good morning":20,"Good afternoon":26,"Good evening":34}[g]
        B.add("F_hora_dia", tmpl[i % 3].format(t=t, w=w), g, [x for x in allg if x != g], [g], exp_t[g], base + (i % 5))
    nights = ["Te vas a dormir a las {t}. ¿Qué le dices a tu familia?","Sales de la casa de tu amigo a las {t} y ya es de noche. Te despides con…","Son las {t} y tus hermanos se van a la cama. ¿Qué les dices?"]
    for i, t in enumerate(["9:30 p. m.","10:00 p. m.","10:45 p. m.","11:00 p. m.","11:30 p. m.","9:00 p. m."]):
        B.add("F_hora_dia", nights[i % 3].format(t=t), "Good night", ["Good morning","Good afternoon","Good evening"], ["Good night"], "Good night es una despedida para la noche o antes de dormir.", 36 + i)
    cuando = [("Good morning","Por la mañana","¿Cuándo se usa «Good morning»?"),("Good afternoon","Después del mediodía","¿En qué momento del día se dice «Good afternoon»?"),
              ("Good evening","Al llegar o saludar por la noche","¿Cuándo se dice «Good evening» a alguien?"),("Good night","Al despedirte antes de dormir","¿Cuándo se dice «Good night»?")]
    opts = ["Por la mañana","Después del mediodía","Al llegar o saludar por la noche","Al despedirte antes de dormir"]
    for i, (g, o, q) in enumerate(cuando):
        B.add("F_hora_dia", q, o, [x for x in opts if x != o], [], "Good morning, good afternoon y good evening son saludos; good night es una despedida.", 30 + i * 3)
    for i, (g, o, q) in enumerate(cuando):
        q2 = ["Si quieres saludar a las 10:00 de la mañana dices «Good morning». ¿Y para saludar a las 3:00 de la tarde?","Después de las 6:00 p. m. llegas a una cena. ¿Qué saludo corresponde?","Antes de acostarte, ¿qué expresión usas con tu mamá?","Estás en una tienda a las 11:00 a. m. ¿Qué saludo usas con la vendedora?"][i]
        ans = ["Good afternoon","Good evening","Good night","Good morning"][i]
        B.add("F_hora_dia", q2, ans, [x for x in allg if x != ans], [ans], "El saludo cambia según la hora: morning, afternoon, evening; y good night para despedirse.", 33 + i * 2)

    # ---- edades ----
    ages = [8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,25,28,30,35,40,45,50,60,70]
    for i, n in enumerate(ages):
        for who_, ans, wr_t, qt in [("yo", f"I am {n} years old", [f"I have {n} years", f"I am {n} years", f"I have {n} years old"], "Tienes {n} años. ¿Cómo respondes a «How old are you?»")]:
            B.add("G_edad", qt.format(n=n), ans, wr_t, accept_variants(ans) + [f"i am {n}", f"i'm {n}", f"i am {nw(n)} years old", f"i'm {nw(n)} years old"], "En inglés la edad se dice con to be: I am 20 years old, no con have.", lerp(i, len(ages), 36, 56))
    others3 = [("Tu hermana","She","9"),("Mi hermano","He","14"),("Tu abuela","She","70"),("Mi papá","He","45"),("Mi mamá","She","42"),("Tu primo","He","16"),("Mi amiga Sofía","She","13"),("Tu maestro","He","38"),("Mi abuelo","He","80"),("Tu vecina","She","30")]
    for i, (es, pr, n) in enumerate(others3):
        pos = {"Tu hermana":"Your sister","Mi hermano":"My brother","Tu abuela":"Your grandmother","Mi papá":"My father","Mi mamá":"My mother","Tu primo":"Your cousin","Mi amiga Sofía":"My friend Sofia","Tu maestro":"Your teacher","Mi abuelo":"My grandfather","Tu vecina":"Your neighbor"}[es]
        ans = f"{pr} is {n} years old"
        B.add("G_edad", f"{es} tiene {n} años. ¿Cómo lo dices en inglés?", ans, [f"{pr} has {n} years", f"{pr} is {n} years", f"{pr} has {n} years old"], accept_variants(ans) + [f"{pr.lower()} is {n}", f"{pr.lower()}'s {n}", f"{pr.lower()} is {nw(int(n))} years old", f"{pos.lower()} is {n} years old"], "Con he o she se usa is: He is 14 years old.", 42 + i * 1.5)

    # ---- origen / nacionalidad ----
    C = [("México","Mexico","Mexican","mexicano"),("España","Spain","Spanish","español"),("Colombia","Colombia","Colombian","colombiano"),("Costa Rica","Costa Rica","Costa Rican","costarricense"),
         ("Perú","Peru","Peruvian","peruano"),("Chile","Chile","Chilean","chileno"),("Brasil","Brazil","Brazilian","brasileño"),("Canadá","Canada","Canadian","canadiense"),
         ("Estados Unidos","the United States","American","estadounidense"),("Alemania","Germany","German","alemán"),("Francia","France","French","francés"),("Italia","Italy","Italian","italiano"),
         ("Japón","Japan","Japanese","japonés"),("China","China","Chinese","chino"),("Inglaterra","England","English","inglés"),("Panamá","Panama","Panamanian","panameño"),
         ("Ecuador","Ecuador","Ecuadorian","ecuatoriano"),("Cuba","Cuba","Cuban","cubano"),("Guatemala","Guatemala","Guatemalan","guatemalteco"),("Irlanda","Ireland","Irish","irlandés"),
         ("Australia","Australia","Australian","australiano"),("India","India","Indian","indio"),("Rusia","Russia","Russian","ruso"),("Portugal","Portugal","Portuguese","portugués")]
    for i, (es, en, nat, natE) in enumerate(C):
        subj = [("Soy de {es}. ¿Cómo lo dices en inglés?","I am from {en}","I am {x} {en}"),("Ella es de {es}. ¿Cómo se dice en inglés?","She is from {en}","She is {x} {en}"),("Él es de {es}. ¿Cómo se dice en inglés?","He is from {en}","He is {x} {en}"),("Nosotros somos de {es}. ¿Cómo se dice en inglés?","We are from {en}","We are {x} {en}")][i % 4]
        q, a, w = subj
        sj = a.split(" ")[0]; vb = a.split(" ")[1]
        ans = a.format(en=en); lowA = ans
        wr = [f"{sj} {vb} of {en}", f"{sj} {vb} from of {en}", (f"{sj} from {en}"), f"{sj} {vb} {en}"]
        accs = accept_variants(ans)
        B.add("H_origen", q.format(es=es), ans, wr, accs, "Para decir de dónde eres usa to be + from: I am from Peru.", lerp(i, len(C), 34, 60))
    for i, (es, en, nat, natE) in enumerate(C):
        if i % 2 == 1:
            pr = ["I","She","He","We"][i % 4]; vb = {"I":"am","She":"is","He":"is","We":"are"}[pr]
            es_pr = {"I":"Soy","She":"Ella es","He":"Él es","We":"Nosotros somos"}[pr]
            ans = f"{pr} {vb} {nat}"
            es_nat = natE + ("s" if pr == "We" else "")
            wr = [f"{pr} {vb} {en}", f"{pr} {vb} from {nat}", f"{pr} has {nat}"]
            B.add("H_origen", f"{es_pr} {es_nat}. ¿Cómo se dice en inglés?" if pr in ("I","We") else f"{es_pr} {natE}. ¿Cómo lo dices en inglés?", ans, wr, accept_variants(ans), "La nacionalidad es un adjetivo y en inglés lleva mayúscula: Mexican, Peruvian.", lerp(i, len(C), 40, 68))
    for i, (es, en, nat, natE) in enumerate(C):
        if en.lower() != es.lower() and en != "the United States" or es == "Estados Unidos":
            if es == "Estados Unidos": continue
            B.add("I_paises", ["¿Cómo se dice el país «{x}» en inglés?","Elige cómo se escribe «{x}» en inglés (país).","¿Cuál es el nombre en inglés de {x}?"][i % 3].format(x=es), en,
                  [c[1] for c in C if c[1] != en and c[1].lower() != es.lower()], [en], "Algunos países cambian de escritura en inglés: Spain, Germany, Japan, Peru.", 38 + (i % 12) * 2)
    for i, (es, en, nat, natE) in enumerate(C):
        if i % 2 == 0:
            wr = [en, f"{en}an", f"{nat}ese" if not nat.endswith("ese") else f"{nat}ish"]
            B.add("I_paises", f"¿Cómo se dice «{natE}» (nacionalidad) en inglés?", nat, [c[2] for c in C if c[2] != nat] , [nat], "Las nacionalidades en inglés llevan mayúscula inicial.", 44 + (i % 12) * 2)

    # ---- nombres ----
    names = ["Carlos","Sofía","Daniel","Valeria","Mateo","Camila","Andrés","Lucía","Diego","Paula","Tomás","Elena","Pablo","Marta"]
    for i, nm in enumerate(names):
        ans = f"My name is {nm}"
        wr = [f"I am name {nm}", f"Me call {nm}", f"I call me {nm}", f"Name is mine {nm}", f"My name are {nm}"]
        fr = ["Te llamas {nm}. ¿Cómo respondes a «What is your name?»","Quieres presentarte como {nm}. ¿Qué dices en inglés?","Alguien te pregunta tu nombre y te llamas {nm}. ¿Qué contestas?"][i % 3]
        B.add("J_nombre", fr.format(nm=nm), ans, wr, accept_variants(ans) + [f"i am {nm.lower()}", f"i'm {nm.lower()}"], "My name is... y I am... sirven para presentarte.", 14 + i * 1.2)
    rels = [("amigo","friend"),("hermano","brother"),("hermana","sister"),("papá","father"),("mamá","mother"),("maestro","teacher"),("primo","cousin"),("compañero de clase","classmate")]
    nn = ["Luis","Ana","Pedro","Marina","Jorge","Rosa","Iván","Nora"]
    for i, (es, en) in enumerate(rels):
        art = {"hermana":"sister","mamá":"mother"}
        ans = f"This is my {en} {nn[i]}"
        wr = [f"This are my {en} {nn[i]}", f"Is my {en} {nn[i]}", f"This my {en} is {nn[i]}", f"These is my {en} {nn[i]}"]
        pres = ["Presentas a tu {es} {n}. ¿Qué dices en inglés?","Quieres decir «Este es mi {es} {n}». ¿Cómo se dice?"][i % 2]
        B.add("K_present", pres.format(es=es if es != "hermana" else "hermana", n=nn[i]) if es not in ("hermana","mamá") else (pres.format(es=es, n=nn[i]).replace("Este es","Esta es")), ans, wr, accept_variants(ans), "This is... se usa para presentar a una persona.", 40 + i * 2)
    plur = [("amigos","friends","Ana y Luis"),("hermanos","brothers","Paco y Raúl"),("compañeros","classmates","Eva y Joel")]
    for i, (es, en, nm) in enumerate(plur):
        a_, b_ = nm.split(" y ")
        ans = f"These are my {en} {a_} and {b_}"
        wr = [f"This is my {en} {a_} and {b_}", f"These is my {en} {a_} and {b_}", f"These are my {en[:-1]} {a_} and {b_}"]
        B.add("K_present", f"Presentas a tus {es} {nm}. ¿Cómo lo dices en inglés?", ans, wr, accept_variants(ans), "Con varias personas se usa These are...", 52 + i * 3)

    # ---- completar ----
    CL = [
     ("Completa: How ___ you?","are",["is","am","be"],"Con you se usa are: How are you?"),
     ("Completa: My name ___ Carlos.","is",["am","are","be"],"Con name (singular) se usa is."),
     ("Completa: I ___ fine, thank you.","am",["is","are","have"],"Con I se usa am."),
     ("Completa: Nice to ___ you.","meet",["meets","meeting","met"],"Después de to va el verbo en forma base: to meet."),
     ("Completa: Good ___, Mr. Lee! (son las 8:00 a. m.)","morning",["afternoon","evening","night"],"Por la mañana se dice good morning."),
     ("Completa: See you ___! (mañana)","tomorrow",["yesterday","before","never"],"Tomorrow significa «mañana»."),
     ("Completa: Have a nice ___!","day",["days","dayly","daily"],"Se dice Have a nice day."),
     ("Completa: ___ me, where is the bank?","Excuse",["Excuses","Excusing","Excused"],"Excuse me se usa para llamar la atención."),
     ("Completa: Pleased to ___ you.","meet",["meets","meeting","met"],"Pleased to meet you es una forma educada de saludar."),
     ("Completa: I'm ___. I was late.","sorry",["sad","sorrow","thanks"],"I'm sorry es la forma de disculparte."),
     ("Completa: Do you ___ English?","speak",["speaks","speaking","says"],"Después de do you va el verbo en forma base."),
     ("Completa: I don't ___. Please repeat.","understand",["understands","understanding","understood"],"Después de don't va el verbo base."),
     ("Completa: Where ___ you from?","are",["is","am","be"],"Con you se usa are."),
     ("Completa: ___ old are you?","How",["What","Who","Where"],"How old...? pregunta la edad."),
     ("Completa: ___ is your name?","What",["Who","Where","When"],"What is your name? pregunta el nombre."),
     ("Completa: ___ are you from?","Where",["What","Who","When"],"Where pregunta por el lugar."),
     ("Completa: Thank you! — You're ___.","welcome",["welcomed","well","thanks"],"You're welcome es la respuesta a thank you."),
     ("Completa: A: Thank you. B: ___ welcome.","You're",["Your","You","Yours"],"You're es la contracción de you are; your es «tu»."),
     ("Completa: Good ___! (te vas a dormir)","night",["morning","afternoon","day"],"Good night es una despedida."),
     ("Completa: Welcome ___ our school!","to",["at","in","from"],"Welcome to... significa «bienvenido a»."),
     ("Completa: Happy ___! (feliz cumpleaños)","birthday",["birth day","birthdays","bornday"],"Birthday es una sola palabra."),
     ("Completa: Nice to see you ___.","again",["other","also","second"],"Again significa «otra vez»."),
     ("Completa: How ___ is it? (¿cuánto cuesta?)","much",["many","long","old"],"How much...? pregunta el precio."),
     ("Completa: Can you ___ me, please?","help",["helps","helping","to help"],"Después de can va el verbo en forma base."),
     ("Completa: Please ___ slowly.","speak",["speaks","speaking","to speak"],"El imperativo usa el verbo en forma base."),
     ("Completa: ___ you very much!","Thank",["Thanking","Thanked","Thankful"],"Thank you very much es una forma fuerte de agradecer."),
     ("Completa: Let me ___ my friend.","introduce",["introduces","introducing","to introduce"],"Introduce significa «presentar» a una persona."),
     ("Completa: I'm from Costa Rica. And ___?","you",["your","yours","yous"],"And you? significa «¿Y tú?»."),
     ("Completa: What's ___ name? (tu nombre)","your",["you","yours","yourself"],"Your es «tu»; you es «tú»."),
     ("Completa: I live ___ Lima.","in",["on","from","to"],"Para ciudades y países se usa in."),
     ("Completa: He is ___ Spain.","from",["of","by","for"],"is from + lugar indica el origen."),
     ("Completa: She ___ my teacher.","is",["am","are","be"],"Con she se usa is."),
     ("Completa: I ___ from Mexico.","am",["is","are","have"],"I am from... indica de dónde eres."),
     ("Completa: See you ___. (más tarde)","later",["latter","lately","lasting"],"Later significa «más tarde»."),
     ("Completa: Sorry, I ___ understand.","don't",["doesn't","isn't","aren't"],"Con I se usa don't."),
     ("Completa: What time ___ it?","is",["am","are","do"],"What time is it? pregunta la hora."),
     ("Completa: ___ you speak Spanish?","Do",["Does","Are","Is"],"Las preguntas con speak empiezan con Do you."),
     ("Completa: Can I ___ some water, please?","have",["has","having","to have"],"Can I have...? sirve para pedir algo."),
     ("Completa: My ___ is Ana. (mi nombre)","name",["names","called","call"],"Name es «nombre»."),
    ]
    for i, (q, a, wr, exp) in enumerate(CL):
        acc = [a] if a != "You're" else ["You're","youre"]
        B.add("L_completar", q, a, wr, acc, exp, lerp(i, len(CL), 7, 58))

    # ---- ordenar ----
    OR = [
     ("How / are / you","How are you",["How you are","Are how you","You how are"]),
     ("name / is / My / Ana","My name is Ana",["My is name Ana","Name my is Ana","Ana is name my"]),
     ("meet / to / Nice / you","Nice to meet you",["Nice meet to you","To nice meet you","You meet to nice"]),
     ("from / I / Peru / am","I am from Peru",["I from am Peru","Peru am I from","From I am Peru"]),
     ("later / you / See","See you later",["See later you","Later you see","You later see"]),
     ("old / you / How / are","How old are you",["How you old are","Old how are you","Are how old you"]),
     ("is / This / my / friend","This is my friend",["This my is friend","My this is friend","Friend this is my"]),
     ("speak / Do / English / you","Do you speak English",["Do speak you English","Do English you speak","Do you English speak"]),
     ("good / Have / day / a","Have a good day",["Have good a day","A have good day","Day good have a"]),
     ("are / from / Where / you","Where are you from",["Where you are from","Are where you from","From where you are"]),
     ("fine, / thank / I / am / you","I am fine, thank you",["I fine am, thank you","Fine I am, thank you","I am thank fine, you"]),
     ("morning / Good / teacher","Good morning, teacher",["Morning good teacher","Good teacher morning","Teacher good morning"]),
     ("is / She / my / sister","She is my sister",["She my is sister","Sister she is my","Is she sister my"]),
     ("meet / to / Pleased / you","Pleased to meet you",["Pleased meet to you","To pleased meet you","You meet pleased to"]),
     ("today / How / you / are","How are you today",["How you are today","Today are how you","Are you how today"]),
     ("is / What / your / number / phone","What is your phone number",["What your phone is number","Your what is phone number","What is phone your number"]),
     ("is / Where / the / bathroom","Where is the bathroom",["Where the bathroom is","The where bathroom is","Bathroom the is where"]),
     ("you / Thank / very / much","Thank you very much",["Thank very you much","You thank very much","Thank you much very"]),
    ]
    for i, (w, a, wr) in enumerate(OR):
        q = ["Ordena las palabras para formar una frase correcta: «{w}»","Forma la frase en inglés con estas palabras: «{w}»","¿Cómo se ordena correctamente «{w}»?"][i % 3].format(w=w)
        acc = [a, a.replace(",", "")]
        B.add("M_ordenar", q, a, wr, accept_variants(a) + [a.replace(",", "").lower()], "En inglés el orden normal es sujeto + verbo + resto; en preguntas el verbo auxiliar va primero.", lerp(i, len(OR), 40, 76))

    # ---- corregir ----
    CO = [
     ("My name are Ana","My name is Ana",["My name be Ana","My names are Ana"],"Con name (singular) se usa is, no are."),
     ("How old you are?","How old are you?",["How old you is?","How you old are?"],"En las preguntas el verbo to be va antes del sujeto."),
     ("Where you are from?","Where are you from?",["Where you from are?","Where is you from?"],"Después de where va are y luego you."),
     ("What is you name?","What is your name?",["What are you name?","What is yours name?"],"Your es el posesivo «tu»; you es «tú»."),
     ("Nice to meet to you","Nice to meet you",["Nice to meeting you","Nice meet to you"],"No lleva to antes de you: Nice to meet you."),
     ("Thanks you","Thank you",["Thanking you","Thank to you"],"Se dice Thank you o simplemente Thanks."),
     ("I have 15 years","I am 15 years old",["I have 15 years old","I am 15 years"],"La edad se dice con am/is/are + years old, no con have."),
     ("I am from of Chile","I am from Chile",["I am of Chile","I from Chile"],"Después de from va directamente el lugar."),
     ("Your welcome","You're welcome",["Your are welcome","You welcome are"],"You're es you are; your significa «tu»."),
     ("Me name is Tom","My name is Tom",["I name is Tom","Mine name is Tom"],"My es el posesivo; me es el pronombre objeto."),
     ("How are your?","How are you?",["How is you?","How are yous?"],"Aquí va you («tú»), no your («tu»)."),
     ("Excuse I, where is the bank?","Excuse me, where is the bank?",["Excuse my, where is the bank?","Excused me, where is the bank?"],"Se dice Excuse me, no Excuse I."),
     ("I no understand","I don't understand",["I not understand","I doesn't understand"],"La negación con I usa don't."),
     ("Have a nice days","Have a nice day",["Has a nice day","Have a nices day"],"Day va en singular en esta frase."),
     ("She name is Ana","Her name is Ana",["She's name is Ana","Hers name is Ana"],"Her es el posesivo de she."),
     ("He is from Brazilian","He is Brazilian",["He is from Brazilian country","He is Brazil"],"Brazilian ya indica nacionalidad; no necesita from."),
     ("I am Colombia","I am Colombian",["I am from Colombian","I have Colombian"],"La nacionalidad es adjetivo: Colombian."),
     ("Pleased to meet","Pleased to meet you",["Pleased to meets you","Pleased meeting you"],"Falta el objeto you."),
     ("How is you?","How are you?",["How be you?","How am you?"],"Con you se usa are."),
     ("Where is you from?","Where are you from?",["Where am you from?","Where do you from?"],"Con you se usa are."),
     ("What are your name?","What is your name?",["What be your name?","What am your name?"],"Name es singular, así que lleva is."),
     ("I'm fine, thank.","I'm fine, thank you.",["I'm fine, thanks you.","I'm fine thank to you."],"Thank necesita you: thank you."),
     ("Please, speaks slowly","Please, speak slowly",["Please, speaking slowly","Please, to speak slowly"],"El imperativo usa el verbo base."),
     ("Welcome at our school","Welcome to our school",["Welcome in our school","Welcome for our school"],"Se dice welcome to."),
     ("I am fine and you?","I am fine, and you?",["I am fine and your?","I am fine and yours?"],"And you? es «¿Y tú?»."),
     ("Good morning, I am Maria name","Good morning, my name is Maria",["Good morning, me name Maria","Good morning, I am name Maria"],"Para decir tu nombre usa my name is."),
     ("See you tomorow","See you tomorrow",["See you tomorow","See you tommorow"],"Tomorrow se escribe con dos r y una m."),
     ("I live in Lima, I from Peru","I live in Lima, I am from Peru",["I live in Lima, I are from Peru","I live in Lima, I have from Peru"],"Falta el verbo to be: I am from Peru."),
    ]
    for i, (w, a, wr, exp) in enumerate(CO):
        q = ["Corrige el error: «{w}»","¿Cuál es la forma correcta de «{w}»?","Hay un error en «{w}». Elige la versión correcta."][i % 3].format(w=w)
        B.add("N_corregir", q, a, wr + [w], accept_variants(a), exp, lerp(i, len(CO), 52, 90))

    # ---- situaciones ----
    SI = [
     ("Un amigo te regala un libro. Le dices:","Thank you",["You're welcome","Sorry","Goodbye"],"Al recibir algo se agradece con Thank you."),
     ("Pisas a alguien sin querer. Dices:","I'm sorry",["Thank you","Nice to meet you","Good morning"],"Para disculparte se usa I'm sorry."),
     ("Conoces a alguien nuevo en una fiesta. Dices:","Nice to meet you",["See you later","You're welcome","Good night"],"Nice to meet you se dice al conocer a alguien."),
     ("Quieres pasar entre dos personas que hablan. Dices:","Excuse me",["See you later","Happy birthday","You're welcome"],"Excuse me se usa para pedir permiso o paso."),
     ("Alguien te agradece por tu ayuda. Respondes:","You're welcome",["Excuse me","Good morning","Nice to meet you"],"You're welcome es la respuesta a thank you."),
     ("Terminas la clase y te vas. Te despides de tu maestra con:","Goodbye, teacher",["Good morning, teacher","Nice to meet you, teacher","Welcome, teacher"],"Goodbye se usa al despedirse."),
     ("Es el cumpleaños de tu amigo. Le dices:","Happy birthday",["Good luck","Welcome","Get well soon"],"Happy birthday se dice el día del cumpleaños."),
     ("Tu amigo tiene un examen mañana. Le deseas:","Good luck",["Happy birthday","Excuse me","Thank you"],"Good luck significa «buena suerte»."),
     ("Alguien estornuda a tu lado. Le dices:","Bless you",["Good luck","Excuse me","Welcome"],"Bless you se dice después de un estornudo."),
     ("Tu amigo está enfermo. Le dices:","Get well soon",["Happy birthday","Good luck","Welcome"],"Get well soon significa «que te mejores pronto»."),
     ("Llega un invitado a tu casa. Le dices:","Welcome",["Goodbye","Sorry","Good night"],"Welcome significa «bienvenido»."),
     ("No entendiste lo que dijo tu maestro. Dices:","Sorry, can you repeat that?",["Sorry, can you sit down?","Thank you, goodbye","Nice to meet you, teacher"],"Can you repeat that? pide que repitan."),
     ("Llegas tarde a clase. Dices:","I'm sorry I'm late",["Thank you, I'm late","Good night, everyone","You're welcome, teacher"],"I'm sorry I'm late significa «lo siento, llegué tarde»."),
     ("Contestas el teléfono a las 9:00 a. m. Dices:","Good morning",["Good night","Goodbye","You're welcome"],"A esa hora se usa good morning."),
     ("Quieres saber el nombre de alguien. Preguntas:","What is your name?",["Where are you from?","How old are you?","How are you?"],"What is your name? pregunta el nombre."),
     ("Quieres saber de dónde es alguien. Preguntas:","Where are you from?",["What is your name?","How old are you?","How are you?"],"Where are you from? pregunta el origen."),
     ("Quieres saber la edad de un compañero. Preguntas:","How old are you?",["What is your name?","Where are you from?","How are you?"],"How old are you? pregunta la edad."),
     ("Quieres saber cómo está tu abuela. Preguntas:","How are you, Grandma?",["What is your name, Grandma?","Where are you from, Grandma?","How old are you, Grandma?"],"How are you? pregunta cómo está alguien."),
     ("Te vas a dormir. Le dices a tu familia:","Good night",["Good morning","Good afternoon","Welcome"],"Good night se dice antes de dormir."),
     ("Quieres decir que no entiendes. Dices:","I don't understand",["I don't know","I don't like it","I don't have it"],"Don't understand significa «no entiendo»."),
     ("Pides ayuda a un desconocido en la calle. Dices:","Excuse me, can you help me?",["Excuse me, can you sit down?","Thanks, goodbye","Welcome, can you help?"],"Excuse me atrae la atención; can you help me? pide ayuda."),
     ("Tu mamá te ayudó con la tarea. Le dices:","Thank you, Mom",["You're welcome, Mom","Sorry, Mom","Good night, Mom"],"Thank you agradece una ayuda."),
     ("Tu amigo se va de viaje y vuelves a verlo en una semana. Te despides:","See you next week",["See you yesterday","Welcome back","Nice to meet you"],"See you next week significa «nos vemos la próxima semana»."),
     ("Un compañero pregunta cómo estás y te va bien. Respondes:","I'm fine, thank you",["I'm 12 years old","My name is Sam","I'm from Peru"],"I'm fine, thank you responde a How are you?"),
    ]
    for i, (q, a, wr, exp) in enumerate(SI):
        B.add("O_situacion", q, a, wr, accept_variants(a), exp, lerp(i, len(SI), 30, 66))

    # ---- función ----
    FN = {"sal":"Para saludar","desp":"Para despedirse","grac":"Para dar las gracias","resp":"Para responder a un agradecimiento","disc":"Para pedir disculpas",
          "perm":"Para pedir permiso o llamar la atención","suerte":"Para desear suerte o felicitar","cort":"Para pedir algo con cortesía","conoc":"Para conocer a alguien",
          "como":"Para preguntar cómo está alguien","noent":"Para avisar que no entiendes o pedir que repitan"}
    CONF = {"sal":{"como","conoc"},"desp":{"suerte"},"suerte":{"desp","sal"},"conoc":{"sal"},"como":{"sal"},"perm":{"disc"},"disc":{"perm"},"grac":set(),"resp":set(),"cort":{"perm"},"noent":{"perm","cort"}}
    P = [("Hello","sal"),("Hi","sal"),("Good morning","sal"),("Good afternoon","sal"),("Good evening","sal"),("Goodbye","desp"),("Bye","desp"),("See you later","desp"),("See you tomorrow","desp"),
         ("See you soon","desp"),("Good night","desp"),("Take care","desp"),("Thank you","grac"),("Thanks a lot","grac"),("Thank you very much","grac"),("You're welcome","resp"),("My pleasure","resp"),
         ("Sorry","disc"),("I'm sorry I'm late","disc"),("I'm very sorry","disc"),("Excuse me","perm"),("Good luck","suerte"),("Happy birthday","suerte"),("Congratulations","suerte"),("Merry Christmas","suerte"),
         ("Get well soon","suerte"),("Please","cort"),("Nice to meet you","conoc"),("Pleased to meet you","conoc"),("How are you?","como"),("How are you doing?","como"),("How is it going?","como"),
         ("I don't understand","noent"),("Can you repeat that, please?","noent"),("Please speak slowly","noent")]
    frs = ["¿Para qué sirve «{x}»?","¿Cuándo se usa «{x}»?","¿Qué función tiene «{x}» en una conversación?"]
    for i, (x, f) in enumerate(P):
        wr = [FN[k] for k in FN if k != f and k not in CONF[f] and f not in CONF[k]]
        B.add("P_funcion", frs[i % 3].format(x=x), FN[f], wr, [], "Cada expresión tiene una función: saludar, despedirse, agradecer, disculparse, etc.", lerp(i, len(P), 26, 60))
