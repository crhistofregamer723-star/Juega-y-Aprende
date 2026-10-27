# -*- coding: utf-8 -*-
import json, hashlib, os, random, subprocess, re

HERE = os.path.dirname(os.path.abspath(__file__))
CP = os.path.join(HERE, '.cache.json')
try:
    CACHE = json.load(open(CP))
except Exception:
    CACHE = {}

def save_cache():
    json.dump(CACHE, open(CP, 'w'))

def _h(*a):
    return hashlib.md5('\x00'.join(a).encode()).hexdigest()

def _sub(cmd, code):
    try:
        r = subprocess.run(cmd, input=code, capture_output=True, text=True, timeout=10)
        return r
    except Exception:
        return None

def run_py(code):
    k = _h('py', code)
    if k in CACHE: return CACHE[k]
    r = _sub(['python3', '-I', '-'], code)
    o = r.stdout.rstrip() if r and r.returncode == 0 else None
    CACHE[k] = o; return o

def run_js(code):
    k = _h('js', code)
    if k in CACHE: return CACHE[k]
    r = _sub(['node', '-'], code)
    o = r.stdout.rstrip() if r and r.returncode == 0 else None
    CACHE[k] = o; return o

def err_py(code):
    r = _sub(['python3', '-I', '-'], code)
    if r is None or r.returncode == 0: return None
    last = r.stderr.strip().splitlines()[-1]
    return last.split(':')[0]

def err_js(code):
    r = _sub(['node', '-'], code)
    if r is None or r.returncode == 0: return None
    for ln in r.stderr.splitlines():
        m = re.match(r'^(\w*Error)\b', ln.strip())
        if m: return m.group(1)
    return None

HDR = ('#include <iostream>\n#include <vector>\n#include <string>\n#include <algorithm>\n#include <cmath>\n'
       '#include <map>\n#include <set>\n#include <sstream>\n#include <numeric>\n#include <functional>\n'
       '#include <climits>\n#include <cstring>\n#include <cstdlib>\n#include <iomanip>\n#include <stack>\n'
       '#include <queue>\n#include <array>\n#include <memory>\n#include <utility>\nusing namespace std;\n')

def _split_cpp(code):
    if '\n@@\n' in code:
        pre, body = code.split('\n@@\n', 1)
    else:
        pre, body = '', code
    return pre, body

def _compile_run(src):
    import tempfile
    d = tempfile.mkdtemp(dir=os.environ.get('TMPDIR', '/tmp'))
    f = os.path.join(d, 'a.cpp'); exe = os.path.join(d, 'a.out')
    open(f, 'w').write(src)
    try:
        c = subprocess.run(['g++', '-std=c++17', '-w', '-O0', f, '-o', exe], capture_output=True, text=True, timeout=60)
        if c.returncode != 0: return None
        r = subprocess.run([exe], capture_output=True, text=True, timeout=10)
        if r.returncode != 0: return None
        return r.stdout
    except Exception:
        return None
    finally:
        subprocess.run(['rm', '-rf', d])

def run_cpp_many(codes):
    res = [None] * len(codes)
    todo = []
    for i, c in enumerate(codes):
        k = _h('cpp', c)
        if k in CACHE: res[i] = CACHE[k]
        else: todo.append(i)
    if todo:
        def build(idxs):
            s = HDR; m = 'int main(){\n'
            for j, i in enumerate(idxs):
                pre, body = _split_cpp(codes[i])
                s += 'namespace v%d {\n%s\nvoid run(){\n%s\n}\n}\n' % (j, pre, body)
                m += 'v%d::run(); cout << "\\x01";\n' % j
            return s + m + '}\n'
        out = _compile_run(build(todo))
        if out is not None:
            parts = out.split('\x01')
            for j, i in enumerate(todo):
                res[i] = parts[j].rstrip()
        else:
            for i in todo:
                o = _compile_run(build([i]))
                res[i] = o.split('\x01')[0].rstrip() if o is not None else None
        for i in todo:
            CACHE[_h('cpp', codes[i])] = res[i]
    return res

def run_many(lang, codes):
    if lang == 'py': return [run_py(c) for c in codes]
    if lang == 'js': return [run_js(c) for c in codes]
    if lang == 'cpp': return run_cpp_many(codes)
    raise ValueError(lang)

LANGN = {'py': 'Python', 'js': 'JavaScript', 'cpp': 'C++', 'pseudo': 'pseudocódigo'}

# ---------------------------------------------------------------- banco
GSEEN = set()

class Bank:
    def __init__(self, cat):
        self.cat = cat
        self.items = []
        self.seen = set()
        self.fams = {}

    def add(self, fam, d, q, a, ws, acc=None, e=''):
        q = q.strip('\n')
        assert isinstance(a, str) and a, (fam, q)
        ws = list(dict.fromkeys(ws))
        assert len(ws) == 3, (fam, q, a, ws)
        assert len(set(norm(x) for x in [a] + ws)) == 4, (fam, q, a, ws)
        assert len(q) <= 500, (fam, len(q), q)
        for x in [a] + ws:
            assert len(x) <= 60, (fam, x)
        if norm(q) in GSEEN: return False
        GSEEN.add(norm(q))
        if acc is None:
            acc = [a] if len(a) <= 40 else []
        if acc and norm(a) not in [norm(x) for x in acc]:
            acc = [a] + list(acc)
        acc = list(dict.fromkeys(acc))
        assert len(e) >= 12, (fam, q)
        self.items.append((int(round(d)), fam, [q, a, ws, acc, e]))
        self.fams[fam] = self.fams.get(fam, 0) + 1
        return True

def norm(s):
    import unicodedata
    s = unicodedata.normalize('NFD', str(s).lower())
    s = ''.join(c for c in s if not unicodedata.combining(c))
    s = re.sub(r'\s+', ' ', s)
    s = re.sub(r'[.¿?¡!]+$', '', s).strip()
    return s

def spread(i, n, lo, hi):
    if n <= 1: return lo
    return lo + (hi - lo) * i / (n - 1)

PROMPTS = [
    '¿Qué imprime este código en {L}?',
    '¿Cuál es la salida de este programa en {L}?',
    'Al ejecutar este fragmento de {L}, ¿qué se muestra?',
    '¿Qué aparece en la consola al correr este código de {L}?',
    'Observa este código de {L}. ¿Qué salida produce?',
    'Dado este código en {L}, ¿qué texto se imprime?',
    'Sigue la ejecución de este código en {L}: ¿qué muestra?',
    '¿Qué resultado se ve en pantalla con este código en {L}?',
]

def perturb(s):
    c = []
    if s in ('True', 'False'): return ['False' if s == 'True' else 'True', 'None', 'Error']
    if s in ('true', 'false'): return ['false' if s == 'true' else 'true', 'undefined', 'null']
    toks = re.split(r'(\s+|,\s*)', s)
    nums = [(i, t) for i, t in enumerate(toks) if re.fullmatch(r'-?\d+(\.\d+)?', t)]
    if nums and len(nums) == len([t for t in toks if t.strip() and not re.fullmatch(r'\s+|,\s*', t)]):
        isf = any('.' in t for _, t in nums)
        def conv(v): return ('%g' % v) if isf else str(int(v))
        for i, t in nums:
            v = float(t)
            for dlt in (1, -1, 2, -2, 10):
                tt = toks[:]; tt[i] = conv(v + dlt); c.append(''.join(tt))
        if len(nums) > 1:
            tt = toks[:]
            idx = [i for i, _ in nums]
            vals = [toks[i] for i in idx][::-1]
            for i, v in zip(idx, vals): tt[i] = v
            c.append(''.join(tt))
            c.append(''.join(toks[:nums[-1][0] - 1]).rstrip(', ') if nums[-1][0] > 0 else s)
            tt = toks[:]; a, b = idx[0], idx[1]; tt[a], tt[b] = tt[b], tt[a]; c.append(''.join(tt))
    else:
        if len(s) > 1:
            c += [s[::-1], s[1:], s[:-1], s.upper(), s.lower(), s.capitalize(), s + s[-1]]
        if ' ' in s:
            c.append(' '.join(s.split(' ')[::-1]))
        c.append(s + ' ' + s[:3])
        c += [s * 2, s + 's', 'Error', 'None', 'a' + s]
    out = []
    for x in c:
        if x != s and x.strip() and x not in out and len(x) <= 60: out.append(x)
    return out

def apply_mut(code, m):
    if isinstance(m, tuple):
        assert m[0] in code, (m, code)
        return code.replace(m[0], m[1], 1)
    return m

def show_code(code):
    return code.replace('\n@@\n', '\n')

def OUT(B, fam, d, lang, code, muts=(), prompt=None, post=None, acc=(), expl='', wr=(), show=None,
        label=None, runlang=None, multi=False):
    rl = runlang or lang
    variants = [code] + [apply_mut(code, m) for m in muts]
    outs = run_many(rl, variants)
    if post: outs = [post(o) if o is not None else None for o in outs]
    correct = outs[0]
    assert correct not in (None, ''), (fam, code, outs)
    assert multi or '\n' not in correct, (fam, code, correct)
    pool = []
    for o in outs[1:]:
        if o is not None and o != correct and o not in pool: pool.append(o)
    rng = random.Random(int(_h(code), 16))
    rng.shuffle(pool)
    ws = []
    def okw(w):
        return len(w) <= 60 and norm(w) != norm(correct) and norm(w) not in [norm(x) for x in ws] and w.strip()
    for w in pool:
        if len(ws) < 3 and okw(w): ws.append(w)
    if len(ws) < 3:
        extra = list(wr); rng.shuffle(extra)
        for w in extra:
            if len(ws) < 3 and okw(w): ws.append(w)
    if len(ws) < 3:
        ex = perturb(correct); rng.shuffle(ex)
        for w in ex:
            if len(ws) < 3 and okw(w): ws.append(w)
    assert len(ws) >= 3, (fam, code, correct)
    L = label or LANGN[lang]
    p = (prompt or rng.choice(PROMPTS)).replace('{L}', L)
    q = p + '\n' + show_code(show if show is not None else code)
    accs = [correct] if len(correct) <= 40 else []
    if '\n' in correct: accs.append(correct.replace('\n', ' '))
    accs += list(acc)
    if correct.startswith('"') and correct.endswith('"') and len(correct) > 2:
        accs.append(correct[1:-1])
    if callable(expl): expl = expl(correct)
    return B.add(fam, d, q, correct, ws[:3], accs, expl)

def FILL(B, fam, d, lang, tmpl, goal, correct, wrongs, acc=None, expl='', check=True, prompt=None):
    """tmpl con ___ ; goal = texto de lo que debe lograr ; se verifica ejecutando."""
    if check and lang in ('py', 'js', 'cpp'):
        cs = [tmpl.replace('___', correct)] + [tmpl.replace('___', w) for w in wrongs]
        outs = run_many(lang, cs)
        assert outs[0] not in (None, ''), (fam, tmpl, correct, outs)
        for w, o in zip(wrongs, outs[1:]):
            assert o != outs[0], ('FILL ambigua', fam, tmpl, w, o)
    p = prompt or 'Completa el código para que %s:' % goal
    q = p + '\n' + show_code(tmpl)
    return B.add(fam, d, q, correct, wrongs, acc, expl)

def ERR(B, fam, d, lang, code, pool_names, expl='', prompt=None, extra=None):
    """Pregunta ¿qué error produce? Verifica ejecutando."""
    name = (err_py if lang == 'py' else err_js)(code)
    assert name, (fam, code)
    ws = [n for n in pool_names if n != name]
    rng = random.Random(int(_h(code), 16))
    rng.shuffle(ws)
    p = prompt or '¿Qué error produce este código en %s al ejecutarse?' % LANGN[lang]
    return B.add(fam, d, p + '\n' + code, name, ws[:3], [name], expl)

def pickw(rng, correct, pool, k=3):
    p = [x for x in pool if norm(x) != norm(correct)]
    p = list(dict.fromkeys(p))
    rng.shuffle(p)
    return p[:k]

def H(B, fam, rows):
    for r in rows:
        d, q, a, ws = r[0], r[1], r[2], r[3]
        acc = r[4] if len(r) > 4 else None
        e = r[5] if len(r) > 5 else ''
        B.add(fam, d, q, a, ws, acc, e)
