import importlib, os
import gen_prog_code as G
from gen_prog_concept import CONC
from lib import HERE
LIMIT = 85
orig_add = G.B.add
def limited(cat, *a, **k):
    if len(G.B.cats.get(cat, [])) >= LIMIT: return False
    return orig_add(cat, *a, **k)
G.B.add = limited
for rnd in range(5):
    import gen_prog_specs, gen_prog_specs2, gen_prog_specs3
    G.SPECS.clear()
    importlib.reload(gen_prog_specs); importlib.reload(gen_prog_specs2); importlib.reload(gen_prog_specs3)
    # (los specs se registran en gen_prog_code.SPECS al importar)
    G.build()
    print('ronda', rnd, {c: len(v) for c, v in G.B.cats.items()})
for cat, rows in CONC.items():
    for q, a, w, d, e in rows: orig_add(cat, q, a, w, d, e, [a])
G.B.finish(os.path.join(HERE, 'out_prog.json'))
