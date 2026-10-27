# Traductor de un pseudocódigo en español a Python (para calcular salidas reales).
import re
PRE = ("def _w(x):\n"
       "    if isinstance(x,bool): x='Verdadero' if x else 'Falso'\n"
       "    elif isinstance(x,float) and x==int(x): x=int(x)\n"
       "    print(x)\n")

def _ex(e):
    e = e.replace('<>', '!=')
    e = re.sub(r'(?<![<>!=])=(?!=)', '==', e)
    e = re.sub(r'\bY\b', ' and ', e)
    e = re.sub(r'\bO\b', ' or ', e)
    e = re.sub(r'\bNO\b', ' not ', e)
    e = re.sub(r'\bMOD\b', '%', e)
    e = re.sub(r'\bDIV\b', '//', e)
    e = e.replace('^', '**')
    e = e.replace('Verdadero', 'True').replace('Falso', 'False')
    return e.strip()

def tr(src):
    strs = []
    def sv(m):
        strs.append(m.group(0)); return '\x00%d\x00' % (len(strs) - 1)
    s = re.sub(r'"[^"]*"', sv, src)
    s = re.sub(r'\bHacer\b', 'Hacer\n', s)
    s = re.sub(r'\bEntonces\b', 'Entonces\n', s)
    s = re.sub(r'\bRepetir\b', 'Repetir\n', s)
    s = re.sub(r'\bSino\b', '\nSino\n', s)
    s = re.sub(r'\b(FinPara|FinMientras|FinSi)\b', r'\n\1\n', s)
    s = re.sub(r'\bHasta Que\b', '\nHasta Que', s)
    s = s.replace(';', '\n')
    lines = [l.strip() for l in s.split('\n') if l.strip()]
    out = []; ind = 0
    for l in lines:
        pad = '    ' * ind
        if l in ('Inicio', 'Fin'):
            continue
        m = re.match(r'Para (\w+) <- (.+?) Hasta (.+?)(?: Paso (.+?))? Hacer$', l)
        if m:
            v, a, b, st = m.groups(); st = st or '1'
            end = '(%s)-1' % _ex(b) if st.strip().startswith('-') else '(%s)+1' % _ex(b)
            out.append('%sfor %s in range(%s, %s, %s):' % (pad, v, _ex(a), end, _ex(st))); ind += 1; continue
        m = re.match(r'Mientras (.+) Hacer$', l)
        if m: out.append('%swhile %s:' % (pad, _ex(m.group(1)))); ind += 1; continue
        m = re.match(r'Si (.+) Entonces$', l)
        if m: out.append('%sif %s:' % (pad, _ex(m.group(1)))); ind += 1; continue
        if l == 'Sino': out.append('    ' * (ind - 1) + 'else:'); continue
        if l == 'Repetir': out.append(pad + 'while True:'); ind += 1; continue
        m = re.match(r'Hasta Que (.+)$', l)
        if m: out.append('%sif %s: break' % (pad, _ex(m.group(1)))); ind -= 1; continue
        if l in ('FinPara', 'FinMientras', 'FinSi'): ind -= 1; continue
        m = re.match(r'Escribir (.+)$', l)
        if m: out.append('%s_w(%s)' % (pad, _ex(m.group(1)))); continue
        m = re.match(r'(\w+) <- (.+)$', l)
        if m: out.append('%s%s = %s' % (pad, m.group(1), _ex(m.group(2)))); continue
        raise ValueError('pseudo no reconocido: ' + l)
    res = '\n'.join(out)
    return PRE + re.sub('\x00(\\d+)\x00', lambda m: strs[int(m.group(1))], res)
