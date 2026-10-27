from lib import *
from run import run, run_many
B = Bank()
WORDS = ['sol', 'luna', 'casa', 'perro', 'gato', 'mesa', 'libro', 'verde', 'agua', 'cielo', 'mundo', 'codigo', 'python', 'datos', 'nube']

class Spec:
    def __init__(s, cat, lang, code, muts, d, expl, pre='¿Qué imprime este código?', show=None):
        s.cat, s.lang, s.code, s.muts, s.d, s.expl, s.pre, s.show = cat, lang, code, muts, d, expl, pre, show
SPECS = []
def spec(*a, **k): SPECS.append(Spec(*a, **k))

LANGNAME = {'py': 'Python', 'js': 'JavaScript', 'cpp': 'C++'}
def build(cat_filter=None):
    items = []
    for sp in SPECS:
        items.append((sp.lang, sp.code))
        for m in sp.muts: items.append((sp.lang, m))
    run_many(items)
    for sp in SPECS:
        ans = run(sp.lang, sp.code)
        if not ans: continue
        wr = []
        for m in sp.muts:
            o = run(sp.lang, m)
            if o and o != ans and o not in wr: wr.append(o)
        if len(wr) < 3:
            try:
                n = int(ans)
                for x in pick_near(n):
                    if str(x) not in wr and str(x) != ans: wr.append(str(x))
            except ValueError:
                pass
        if len(wr) < 3: continue
        code = sp.show if sp.show else sp.code
        q = f'{sp.pre}\n{code}'
        B.add(sp.cat, q, ans, wr, sp.d, sp.expl, [ans])

def cpp_wrap(code): return code
