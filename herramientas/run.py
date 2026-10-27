import subprocess, hashlib, os, tempfile
from concurrent.futures import ThreadPoolExecutor
CACHE = {}
def _norm(o): return ' '.join(o.split())
def run(lang, code):
    key = (lang, code)
    if key in CACHE: return CACHE[key]
    try:
        if lang == 'py':
            p = subprocess.run(['python3', '-I', '-c', code], capture_output=True, text=True, timeout=10)
        elif lang == 'js':
            p = subprocess.run(['node', '-e', code], capture_output=True, text=True, timeout=10)
        else:
            d = tempfile.mkdtemp(prefix='cpp_', dir='/tmp/claude-0')
            open(d + '/a.cpp', 'w').write('#include <iostream>\n#include <string>\n#include <vector>\nusing namespace std;\nint main(){\n' + code + '\nreturn 0;}\n')
            c = subprocess.run(['g++', '-std=c++17', '-w', '-o', d + '/a', d + '/a.cpp'], capture_output=True, text=True, timeout=60)
            if c.returncode: CACHE[key] = None; return None
            p = subprocess.run([d + '/a'], capture_output=True, text=True, timeout=10)
        out = _norm(p.stdout) if p.returncode == 0 else None
    except Exception:
        out = None
    CACHE[key] = out
    return out
def run_many(items):
    with ThreadPoolExecutor(8) as ex:
        return list(ex.map(lambda it: run(*it), items))
