import sys, json, io, contextlib, signal
items = json.load(open(sys.argv[1])); res = []
def h(s, f): raise TimeoutError('timeout')
signal.signal(signal.SIGALRM, h)
for src in items:
    buf = io.StringIO()
    try:
        signal.alarm(2)
        with contextlib.redirect_stdout(buf):
            exec(compile(src, '<q>', 'exec'), {'__name__': '__main__'})
        signal.alarm(0); res.append({'out': buf.getvalue(), 'err': None})
    except BaseException as e:
        signal.alarm(0); res.append({'out': buf.getvalue(), 'err': type(e).__name__})
json.dump(res, open(sys.argv[2], 'w'))
