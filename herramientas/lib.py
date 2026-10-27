import random, json, os, re
R = random.Random(2026)
HERE = os.path.dirname(os.path.abspath(__file__))

class Bank:
    def __init__(self):
        self.cats = {}
        self.seen = set()
    def add(self, cat, q, ans, wrong, d, expl='', acc=None):
        ans = str(ans)
        wrong = [str(w) for w in wrong]
        uniq = []
        for w in wrong:
            if w != ans and w not in uniq:
                uniq.append(w)
        if len(uniq) < 3 or q in self.seen:
            return False
        self.seen.add(q)
        acc = [ans] + [a for a in (acc or []) if a != ans]
        self.cats.setdefault(cat, []).append([q, ans, uniq[:3], acc, expl, int(max(0, min(100, d)))])
        return True
    def finish(self, path):
        for c in self.cats:
            self.cats[c].sort(key=lambda r: r[5])
        json.dump(self.cats, open(path, 'w', encoding='utf-8'), ensure_ascii=False, separators=(',', ':'))
        for c, rows in self.cats.items():
            print(c, len(rows), 'd', rows[0][5], '-', rows[-1][5])
        print('total', sum(len(v) for v in self.cats.values()))

def near_int(a, extra=()):
    """3 distractores enteros plausibles."""
    c = [a + 1, a - 1, a + 2, a - 2, a + 10, a - 10, -a, a * 2, a + 5, a - 5, a + 3, a - 3]
    c = list(extra) + c
    out = []
    for x in c:
        if x != a and x not in out:
            out.append(x)
    return out[:3] if len(out) >= 3 else out

def pick_near(a, extra=()):
    base = list(extra)
    pool = [a + 1, a - 1, a + 2, a - 2, a + 10, a - 10, a * 2, a + 5, a - 5, a + 3, a - 3]
    if a != 0: pool.insert(2, -a)
    out = []
    for x in base + pool:
        if x != a and x not in out: out.append(x)
    head = out[:len(base)]
    rest = out[len(base):]
    R.shuffle(rest)
    return (head + rest)[:3]

def fr(x):
    from fractions import Fraction
    x = Fraction(x)
    return str(x.numerator) if x.denominator == 1 else f'{x.numerator}/{x.denominator}'

def near_fr(a, extra=(), prob=False):
    from fractions import Fraction
    a = Fraction(a)
    cands = list(extra) + ([Fraction(1, 2), Fraction(1, 3), Fraction(2, 3), Fraction(1, 4), Fraction(3, 4), 1 - a, a / 2, a * 2, Fraction(1, 6), Fraction(5, 6)] if prob else []) + [a + Fraction(1, 2), a - Fraction(1, 2), a + 1, a - 1, -a, a * 2, a / 2 if a != 0 else 1, a + Fraction(1, 3), a + 2]
    out = []
    for x in cands:
        x = Fraction(x)
        if prob and not (0 <= x <= 1): continue
        if x != a and fr(x) not in [fr(o) for o in out]: out.append(x)
    return [fr(x) for x in out[:3]]

SUP = {'2': '²', '3': '³', '4': '⁴', '5': '⁵', '6': '⁶', '7': '⁷'}
def pw(n):
    return SUP.get(str(n), '^' + str(n))

def poly(coefs, var='x'):
    """coefs de mayor a menor grado -> '3x² − 2x + 5'"""
    n = len(coefs) - 1
    s = ''
    for i, c in enumerate(coefs):
        k = n - i
        if c == 0: continue
        sign = '−' if c < 0 else '+'
        a = abs(c)
        if k == 0: term = str(a)
        else:
            coef = '' if a == 1 else str(a)
            term = coef + var + (pw(k) if k > 1 else '')
        if not s: s = ('−' if c < 0 else '') + term
        else: s += f' {sign} {term}'
    return s or '0'

def plain(s):
    """Variantes aceptadas para respuestas escritas."""
    v = {s, s.replace(' ', ''), s.replace('−', '-'), s.replace('−', '-').replace(' ', '')}
    for k, e in SUP.items():
        v |= {x.replace(e, '^' + k) for x in list(v)}
    return sorted(v)

def cf(c):  # coeficiente: 1 se omite
    return '' if c == 1 else ('−' if c == -1 else str(c))
