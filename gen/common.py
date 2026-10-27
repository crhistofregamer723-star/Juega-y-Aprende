import ast, json, os, random, re, subprocess, sys, tempfile
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from pseudo_tr import tr as pseudo_tr
CATS = ['cpp', 'py', 'html', 'js', 'pseudo', 'func', 'bucles', 'arr']
ROWS = {c: [] for c in CATS}
ITEMS = []
SEEN_Q = set(); SEEN_CODE = set()
PROMPTS = ['¿Qué imprime este código?', '¿Cuál es la salida del siguiente código?',
           '¿Qué se muestra en pantalla al ejecutar este código?',
           'Observa el código. ¿Qué resultado produce?', 'Al ejecutar este programa, ¿qué aparece en la salida?']
ERRS_PY = ['ZeroDivisionError', 'IndexError', 'KeyError', 'TypeError', 'NameError', 'ValueError', 'AttributeError']
ERRS_JS = ['TypeError', 'ReferenceError', 'RangeError', 'SyntaxError', 'Error']

def clamp(d): return max(0, min(100, int(round(d))))

def _acc(a, extra=()):
    s = [a]
    if ' ' in a and len(a) < 40: s.append(a.replace(' ', ''))
    if a.startswith('<') and a.endswith('>') and len(a) > 2: s.append(a[1:-1])
    for e in extra:
        if e not in s: s.append(e)
    return s[:5]

def row(cat, q, a, w, d, e='', acc=()):
    q = q.strip()
    if q in SEEN_Q: return False
    key = lambda x: re.sub(r'\s+', '', str(x)).lower()
    opts = [a] + list(w)
    assert len(w) == 3 and len({key(o) for o in opts}) == 4, ('opciones no válidas', q, opts)
    SEEN_Q.add(q)
    ROWS[cat].append([q, a, list(w), _acc(a, acc), e, clamp(d)])
    return True

def C(cat, block):
    """Bloque conceptual: d§pregunta§correcta§m1§m2§m3§explicación   (\\n = salto de línea)"""
    for line in block.strip().splitlines():
        line = line.strip()
        if not line or line.startswith('#'): continue
        p = [x.strip().replace('\\n', '\n') for x in line.split('§')]
        if len(p) == 6: p.append('')
        assert len(p) == 7, ('línea mal formada', line)
        d, q, a, w1, w2, w3, e = p
        row(cat, q, a, [w1, w2, w3], int(d), e)

def code(cat, lang, src, d, alts=(), why='', prompt=None, wait=0, mode='out', top='', acc=()):
    key = (lang, top, src)
    if key in SEEN_CODE: return False
    SEEN_CODE.add(key)
    if prompt is None:
        prompt = '¿Qué excepción lanza este código?' if mode == 'err' else PROMPTS[len(ITEMS) % len(PROMPTS)]
    ITEMS.append(dict(cat=cat, lang=lang, src=src.strip('\n'), top=top.strip('\n'), d=d, alts=list(alts), why=why,
                      prompt=prompt, wait=wait, mode=mode, acc=list(acc)))
    return True

def fam(n, fn):
    got = 0; tries = 0
    while got < n and tries < n * 40:
        tries += 1
        if fn(): got += 1
    if got < n: print('  aviso: familia', fn.__name__, 'solo', got, 'de', n)

# ---------- ejecución real ----------
def _run_py(srcs):
    with tempfile.TemporaryDirectory() as t:
        fi, fo = t + '/i.json', t + '/o.json'
        json.dump(srcs, open(fi, 'w'))
        subprocess.run([sys.executable, '-I', HERE + '/run_py.py', fi, fo], check=True, timeout=600)
        return json.load(open(fo))

def _run_js(items):
    with tempfile.TemporaryDirectory() as t:
        fi = t + '/i.json'
        json.dump(items, open(fi, 'w'))
        r = subprocess.run(['node', HERE + '/run_js.js', fi], capture_output=True, text=True, timeout=900)
        if r.returncode: raise RuntimeError(r.stderr)
        return json.loads(r.stdout)

CPP_HEAD = '#include <iostream>\n#include <string>\n#include <vector>\n#include <algorithm>\n#include <cmath>\nusing namespace std;\n'
def _run_cpp(items):
    tops = ''.join('namespace n%d {\n%s\n}\n' % (i, it['top']) for i, it in enumerate(items))
    body = ''.join('static void s%d(){\nusing namespace n%d;\n%s\n}\n' % (i, i, it['src']) for i, it in enumerate(items))
    main = 'int main(){\n' + ''.join('cout<<"@@%d\\n"; s%d(); cout<<"\\n";\n' % (i, i) for i in range(len(items))) + '}\n'
    with tempfile.TemporaryDirectory() as t:
        open(t + '/a.cpp', 'w').write(CPP_HEAD + tops + body + main)
        r = subprocess.run(['g++', '-std=c++17', '-w', '-O0', t + '/a.cpp', '-o', t + '/a'], capture_output=True, text=True)
        if r.returncode:
            print(r.stderr[:3000]); raise RuntimeError('fallo al compilar C++')
        r = subprocess.run([t + '/a'], capture_output=True, text=True, timeout=60)
    parts = re.split(r'@@(\d+)\n', r.stdout)
    res = [None] * len(items)
    for i in range(1, len(parts), 2): res[int(parts[i])] = {'out': parts[i + 1], 'err': None}
    return res

def execute():
    res = [None] * len(ITEMS)
    for lang in ('py', 'pseudo', 'js', 'cpp'):
        idx = [i for i, it in enumerate(ITEMS) if it['lang'] == lang]
        if not idx: continue
        if lang == 'py': out = _run_py([ITEMS[i]['src'] for i in idx])
        elif lang == 'pseudo': out = _run_py([pseudo_tr(ITEMS[i]['src']) for i in idx])
        elif lang == 'js': out = _run_js([{'src': ITEMS[i]['src'], 'wait': ITEMS[i]['wait']} for i in idx])
        else: out = _run_cpp([ITEMS[i] for i in idx])
        for i, o in zip(idx, out): res[i] = o
    return res

# ---------- distractores ----------
def _num_fmt(x, dec):
    return ('%.' + str(dec) + 'f') % x if dec else str(int(round(x)))

def mutate(s, rng):
    c = []
    def add(x):
        x = str(x)
        if x != s and x not in c: c.append(x)
    t = s.strip()
    low = t.lower()
    if low in ('true', 'false'):
        add(('True' if t[0] == 'T' else 'true') if low == 'false' else ('False' if t[0] == 'T' else 'false'))
        if t[0] == 'T': add('None'); add('Error')
        else: add('undefined'); add('null')
    try: v = ast.literal_eval(t)
    except Exception: v = None
    if isinstance(v, bool): pass
    elif isinstance(v, int):
        for x in (v + 1, v - 1, v + 2, v - 2, v * 2 if v else 1, -v if v else 10, v + 10, v - 10, v // 2 if abs(v) > 3 else v + 3): add(x)
    elif isinstance(v, float):
        dec = len(t.split('.')[1]) if '.' in t else 1
        for x in (v + 1, v - 1, v + .5, v - .5, v * 2, int(v)):
            add(_num_fmt(x, dec) if x != int(v) or x is not int else x)
        add(str(int(v)))
    elif isinstance(v, (list, tuple)) and len(v) > 1:
        L = list(v); mk = (lambda z: repr(type(v)(z)))
        add(mk(L[::-1])); add(mk(L[:-1])); add(mk(L[1:])); add(mk(sorted(L, key=str)))
        for i in range(len(L)):
            if isinstance(L[i], int) and not isinstance(L[i], bool):
                for dlt in (1, -1):
                    M = L[:]; M[i] += dlt; add(mk(M))
        add(mk(L + [L[-1]]))
        if len(L) > 2: M = L[:]; M[0], M[1] = M[1], M[0]; add(mk(M))
    elif v is None or not isinstance(v, (int, float, list, tuple)):
        sep = ' ' if ' ' in t else (',' if ',' in t else None)
        if sep:
            tk = t.split(sep)
            add(sep.join(tk[::-1])); add(sep.join(tk[:-1])); add(sep.join(tk[1:])); add(sep.join(tk + [tk[-1]]))
            for i, x in enumerate(tk):
                if re.fullmatch(r'-?\d+', x):
                    for dlt in (1, -1):
                        M = tk[:]; M[i] = str(int(x) + dlt); add(sep.join(M))
            if len(tk) > 2: M = tk[:]; M[0], M[1] = M[1], M[0]; add(sep.join(M))
        for x in (t[::-1], t.upper(), t.lower(), t.capitalize(), t[1:], t[:-1], t + t[-1:], t.swapcase()):
            if x: add(x)
        for m in list(re.finditer(r'-?\d+', t))[:4]:
            for dlt in (1, -1): add(t[:m.start()] + str(int(m.group()) + dlt) + t[m.end():])
    rng.shuffle(c)
    return c

def wrongs(ans, alts, rng, avoid=()):
    key = lambda x: re.sub(r'\s+', '', str(x)).lower()
    used = {key(ans)} | {key(a) for a in avoid}
    out = []
    pool = list(alts); rng.shuffle(pool)
    for a in pool:
        a = str(a)
        if key(a) not in used and len(out) < 3: out.append(a); used.add(key(a))
    if len(out) < 3:
        for a in mutate(ans, rng):
            if key(a) not in used and len(out) < 3: out.append(a); used.add(key(a))
    assert len(out) == 3, ('pocos distractores', ans, out)
    return out

def finalize(res):
    rng = random.Random(777)
    bad = []
    for it, r in zip(ITEMS, res):
        if r is None: bad.append((it, 'sin resultado')); continue
        shown = (it['top'] + '\n' if it['top'] else '') + it['src']
        q = it['prompt'] + '\n' + shown
        if it['mode'] == 'err':
            if not r['err']: bad.append((it, 'no lanzó error')); continue
            ans = r['err']
            base = ERRS_JS if it['lang'] == 'js' else ERRS_PY
            alts = it['alts'] or [e for e in base if e != ans]
            w = wrongs(ans, alts, rng)
            e = 'Se lanza %s. %s' % (ans, it['why'])
            row(it['cat'], q, ans, w, it['d'], e.strip(), it['acc'])
            continue
        if r['err']: bad.append((it, 'error ' + str(r['err']))); continue
        out = r['out'].strip()
        ans = ' '.join(out.split()) if '\n' in out else out
        if not ans: bad.append((it, 'salida vacía')); continue
        w = wrongs(ans, it['alts'], rng)
        e = ('La salida es «%s». %s' % (ans, it['why'])).strip()
        row(it['cat'], q, ans, w, it['d'], e, it['acc'])
    if bad:
        for it, why in bad[:40]: print('ERROR', why, '|', it['lang'], '|', it['src'][:150].replace('\n', ' / '))
        print(len(bad), 'ítems con problemas'); sys.exit(1)
