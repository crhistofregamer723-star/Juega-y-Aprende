# -*- coding: utf-8 -*-
import json, sys, os, importlib
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import lib
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EXIST = json.load(open(os.path.join(ROOT, 'existentes.json')))
EXD = {
 'cpp':   [3,2,4,3,2,5,4,7,3,12,8,10],
 'py':    [2,3,4,6,8,9,10,12,13,7,9,14],
 'html':  [2,3,2,3,3,6,5,5,4,4,6,8],
 'js':    [3,5,6,9,8,3,7,10,10,16,14,8],
 'pseudo':[2,2,3,3,4,4,6,5,10,7,8,9],
 'func':  [3,4,5,4,5,5,14,6,8,12,16,24],
 'bucles':[2,6,7,12,10,14,15,9,11,12,20,18],
 'arr':   [2,3,8,9,12,10,9,14,10,16,13,11],
}
CATS = ['cpp','py','html','js','pseudo','func','bucles','arr']
def main(which):
    out = {}
    for cat in which:
        B = lib.Bank(cat)
        for i, q in enumerate(EXIST[cat]['qs']):
            q = list(q)[:5]
            B.items.append((EXD[cat][i], 'base', q)); B.fams['base'] = B.fams.get('base', 0) + 1
            lib.GSEEN.add(lib.norm(q[0]))
        mod = importlib.import_module('c_' + cat)
        mod.build(B)
        items = sorted(B.items, key=lambda t: t[0])  # estable
        out[cat] = [it[2] + [it[0]] for it in items]
        n = len(items)
        top = max(B.fams.values())
        print(cat, n, 'familias', len(B.fams), 'max', top, '(%.1f%%)' % (100 * top / n))
        lib.save_cache()
    return out
if __name__ == '__main__':
    which = sys.argv[1:] or CATS
    dst = os.path.join(ROOT, 'prog.json')
    full = {}
    if len(which) < len(CATS) and os.path.exists(dst):
        full = json.load(open(dst))
    full.update(main(which))
    json.dump({c: full[c] for c in CATS if c in full}, open(dst, 'w'), ensure_ascii=False, indent=0)
