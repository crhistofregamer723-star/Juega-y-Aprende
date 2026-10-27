# -*- coding: utf-8 -*-
import random, json
from lib import *

def build(cat, families, handwritten, existing, exist_d, seed, area_seen):
    """families: [(nombre, func, n, dlo, dhi)]. Devuelve filas ordenadas por dificultad."""
    assert len(existing) == len(exist_d), (cat, len(existing), len(exist_d))
    rows = []
    famcount = {}
    seen = area_seen
    # existentes
    for q, d in zip(existing, exist_d):
        key = norm(q[0]); seen.add(key)
        rows.append((d, 0, list(q[:5]) + [d], "existente"))
    # escritas a mano
    for h in handwritten:
        q, a, w, acc, e, d = h
        row = mk(q, a, w, e, acc=acc)
        key = norm(q)
        assert key not in seen, "duplicada: " + q
        seen.add(key)
        rows.append((d, 1, row + [d], "manual"))
    rng = random.Random(seed)
    for fi, (name, f, n, dlo, dhi) in enumerate(families):
        got = 0
        i = 0
        tries = 0
        while got < n and tries < n * 60:
            tries += 1
            t = got / max(1, n - 1)
            row = f(rng, t)
            key = norm(row[0])
            if key in seen: continue
            seen.add(key)
            d = int(round(dlo + (dhi - dlo) * t + rng.uniform(-1.2, 1.2)))
            d = max(1, min(100, d))
            rows.append((d, 2 + fi, row + [d], name))
            got += 1
        famcount[name] = got
        if got < n: print("AVISO familia corta", cat, name, got, "/", n)
    # orden estable por dificultad; dentro de un mismo d, existentes primero
    rows.sort(key=lambda x: (x[0], x[1]))
    # verificación de monotonía
    ds = [r[2][5] for r in rows]
    assert ds == sorted(ds)
    return [r[2] for r in rows], famcount, [r[3] for r in rows]
