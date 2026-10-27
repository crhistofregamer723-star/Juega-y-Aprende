import random, re, json
from vocab_ing import VOCAB_TXT

R = random.Random(20261019)
CATS = ['ing1', 'ing2', 'ing3', 'ing4', 'ing5', 'ing6']
ROWS = {c: [] for c in CATS}
SEEN = set()
SKIPPED = {c: 0 for c in CATS}

def norm(s):
    return re.sub(r'\s+', ' ', s.strip().lower())

def acc_variants(ans):
    out = [ans]
    low = ans.lower()
    out.append(low)
    nop = re.sub(r'[.?!¿¡]', '', ans).strip()
    out.append(nop)
    out.append(nop.lower())
    # contracciones <-> formas completas (aceptar ambas)
    pairs = [("I am", "I'm"), ("you are", "you're"), ("he is", "he's"), ("she is", "she's"),
             ("it is", "it's"), ("we are", "we're"), ("they are", "they're"),
             ("is not", "isn't"), ("are not", "aren't"), ("do not", "don't"), ("does not", "doesn't"),
             ("was not", "wasn't"), ("were not", "weren't"), ("cannot", "can't")]
    for a, b in pairs:
        for v in list(out):
            for x, y in ((a, b), (b, a)):
                if re.search(r'\b' + re.escape(x) + r'\b', v, flags=re.I):
                    out.append(re.sub(r'\b' + re.escape(x) + r'\b', y, v, flags=re.I))
    seen, res = set(), []
    for v in out:
        k = v.strip()
        if k and k not in seen and len(k) <= 60:
            seen.add(k); res.append(k)
    return res[:8]

def add(cat, q, ans, cands, d, expl, acc=None, shuffle=True):
    """Añade una fila. cands = posibles incorrectas (se eligen 3 únicas)."""
    if q in SEEN:
        return False
    seen = {norm(ans)}
    pool = []
    for c in cands:
        k = norm(c)
        if k and k not in seen:
            seen.add(k); pool.append(c)
    if len(pool) < 3:
        SKIPPED[cat] += 1
        return False
    wr = R.sample(pool, 3) if shuffle and len(pool) > 3 else pool[:3]
    accepted = acc if acc is not None else acc_variants(ans)
    if ans not in accepted:
        accepted = [ans] + accepted
    SEEN.add(q)
    ROWS[cat].append([q, ans, wr, accepted, expl, d + R.random() * 2])
    return True

# ---------- vocabulario ----------
VOC = []  # dicts: en, es, lvl, pos, key, phrase
def _load():
    key = lvl = pos = phrase = None
    for line in VOCAB_TXT.splitlines():
        line = line.strip()
        if not line:
            continue
        if line.startswith('@'):
            head, phrase = [x.strip() for x in line[1:].split('|')]
            key, lvl, pos = head.split()
            lvl = int(lvl)
            continue
        en, es = [x.strip() for x in line.split('=')]
        VOC.append(dict(en=en, es=es, lvl=lvl, pos=pos, key=key, phrase=phrase))
_load()
EN_COUNT = {}
for v in VOC:
    EN_COUNT[v['en']] = EN_COUNT.get(v['en'], 0) + 1

LVL_D = {1: 6, 2: 28, 3: 52, 4: 76}

# ---------- gramática ----------
IRR_PL = {'man': 'men', 'woman': 'women', 'child': 'children', 'tooth': 'teeth', 'foot': 'feet',
          'mouse': 'mice', 'person': 'people', 'goose': 'geese', 'sheep': 'sheep', 'fish': 'fish',
          'deer': 'deer', 'leaf': 'leaves', 'knife': 'knives', 'wife': 'wives', 'life': 'lives',
          'wolf': 'wolves', 'shelf': 'shelves', 'loaf': 'loaves', 'thief': 'thieves', 'half': 'halves',
          'scarf': 'scarves', 'potato': 'potatoes', 'tomato': 'tomatoes', 'hero': 'heroes',
          'mother-in-law': 'mothers-in-law', 'ox': 'oxen', 'louse': 'lice', 'woman ': 'women'}
IRR_WRONG = {
    'man': ['mans', 'manes', 'mens'], 'woman': ['womans', 'womens', 'womanes'],
    'child': ['childs', 'childrens', 'childes'], 'tooth': ['tooths', 'teeths', 'toothes'],
    'foot': ['foots', 'feets', 'footes'], 'mouse': ['mouses', 'mices', 'mousees'],
    'person': ['persones', 'peoples', 'personns'], 'goose': ['gooses', 'geeses', 'goosees'],
    'sheep': ['sheeps', 'sheepes', 'sheeps'], 'fish': ['fishes', 'fishs', 'fishies'],
    'deer': ['deers', 'deeres', 'deeries'], 'leaf': ['leafs', 'leafes', 'leavs'],
    'knife': ['knifes', 'knifs', 'knifees'], 'wife': ['wifes', 'wifs', 'wivess'],
    'wolf': ['wolfs', 'wolfes', 'wolvs'], 'shelf': ['shelfs', 'shelfes', 'shelvs'],
    'scarf': ['scarfes', 'scarvs', 'scarfies'], 'potato': ['potatos', 'potatoies', 'potatoss'],
    'tomato': ['tomatos', 'tomatoies', 'tomatoss'], 'mother-in-law': ['mother-in-laws', 'mothers-in-laws', 'mother-in-lawes'],
}
AMBIG_PL = {'volcano', 'tornado', 'hurricane', 'scarf', 'fish', 'avocado', 'hedgehog', 'dolphin'}
AMBIG_PL = {'volcano', 'scarf', 'fish', 'sheep', 'deer'} - {'sheep', 'deer', 'fish'}  # scarves/scarfs: ambiguo
AMBIG_PL = {'volcano', 'scarf'}

def plural(n):
    if n in IRR_PL:
        return IRR_PL[n]
    if re.search(r'(s|x|z|ch|sh)$', n):
        return n + 'es'
    if re.search(r'[^aeiou]y$', n):
        return n[:-1] + 'ies'
    return n + 's'

def plural_wrongs(n):
    if n in IRR_WRONG:
        return IRR_WRONG[n]
    out = []
    ans = plural(n)
    if re.search(r'[^aeiou]y$', n):
        out += [n + 's', n[:-1] + 'es', n + 'es']
    elif re.search(r'(s|x|z|ch|sh)$', n):
        out += [n + 's', n, n + 'ies']
    elif n.endswith('o'):
        out += [n + 'es', n + 'ies', n]
    elif n.endswith('f') or n.endswith('fe'):
        out += [n + 'es', n[:-1] + 'ves', n + 'ies']
    else:
        out += [n + 'es', n + 'ies', n, n + 'ses']
    return [o for o in out if o != ans]

def pl_kind(n):
    """Dificultad del plural de n."""
    if n in IRR_PL:
        return 'irr'
    if re.search(r'(s|x|z|ch|sh)$', n):
        return 'es'
    if re.search(r'[^aeiou]y$', n):
        return 'ies'
    return 's'

def art(w):
    lw = w.lower()
    if lw.startswith(('hour', 'honest', 'honor', 'heir', 'x-ray')):
        return 'an'
    if lw.startswith(('uni', 'use', 'usu', 'eu', 'one', 'ubiq')):
        return 'a'
    return 'an' if lw[0] in 'aeiou' else 'a'

def s3(v):
    irr = {'have': 'has', 'go': 'goes', 'do': 'does', 'be': 'is'}
    if v in irr:
        return irr[v]
    if re.search(r'(s|x|z|ch|sh)$', v):
        return v + 'es'
    if re.search(r'[^aeiou]y$', v):
        return v[:-1] + 'ies'
    return v + 's'

def ing_form(v):
    dbl = {'run', 'swim', 'sit', 'stop', 'get', 'put', 'cut', 'plan'}
    if v in dbl:
        return v + v[-1] + 'ing'
    if v.endswith('ie'):
        return v[:-2] + 'ying'
    if v.endswith('e') and not v.endswith('ee'):
        return v[:-1] + 'ing'
    return v + 'ing'

# ---------- números ----------
ONES = ['zero', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine', 'ten', 'eleven',
        'twelve', 'thirteen', 'fourteen', 'fifteen', 'sixteen', 'seventeen', 'eighteen', 'nineteen']
TENS = ['', '', 'twenty', 'thirty', 'forty', 'fifty', 'sixty', 'seventy', 'eighty', 'ninety']

def words(n):
    if n < 20:
        return ONES[n]
    if n < 100:
        t, o = divmod(n, 10)
        return TENS[t] + ('-' + ONES[o] if o else '')
    if n < 1000:
        h, r = divmod(n, 100)
        return ONES[h] + ' hundred' + (' ' + words(r) if r else '')
    for unit, name in ((10**9, 'billion'), (10**6, 'million'), (1000, 'thousand')):
        if n >= unit:
            q, r = divmod(n, unit)
            return words(q) + ' ' + name + (' ' + words(r) if r else '')

def words_and(n):
    w = words(n)
    return re.sub(r'hundred (?!and)(?=\w)', 'hundred and ', w)

def ordinal_word(n):
    w = words(n)
    parts = re.split(r'([ -])', w)
    last = parts[-1]
    irr = {'one': 'first', 'two': 'second', 'three': 'third', 'five': 'fifth', 'eight': 'eighth',
           'nine': 'ninth', 'twelve': 'twelfth'}
    if last in irr:
        last = irr[last]
    elif last.endswith('y'):
        last = last[:-1] + 'ieth'
    else:
        last += 'th'
    parts[-1] = last
    return ''.join(parts)

def ordinal_digit(n):
    if 10 <= n % 100 <= 20:
        suf = 'th'
    else:
        suf = {1: 'st', 2: 'nd', 3: 'rd'}.get(n % 10, 'th')
    return str(n) + suf

def fmt(n):
    return f'{n:,}'

# ---------- español ----------
def es_pl(w):
    special = {'joven': 'jóvenes', 'fácil': 'fáciles', 'difícil': 'difíciles'}
    if w in special:
        return special[w]
    if w.endswith('z'):
        return w[:-1] + 'ces'
    if w[-1] in 'aeiouéáíóú':
        return w + 's'
    return w + 'es'

def finish(cat_caps):
    """Ordena por dificultad, recorta y valida. Devuelve dict listo para JSON."""
    out = {}
    for c in CATS:
        rows = ROWS[c]
        cap = cat_caps.get(c)
        if cap and len(rows) > cap:
            R.shuffle(rows)
            rows = rows[:cap]
        rows.sort(key=lambda r: r[5])
        out[c] = [[r[0], r[1], r[2], r[3], r[4], max(0, min(100, int(round(r[5]))))] for r in rows]
    return out
