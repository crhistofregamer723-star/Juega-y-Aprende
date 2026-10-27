# -*- coding: utf-8 -*-
import random, re, unicodedata

def norm(s):
    s = unicodedata.normalize("NFD", str(s).lower())
    s = "".join(c for c in s if not unicodedata.combining(c))
    s = re.sub(r"\s+", " ", s)
    s = re.sub(r"[.¿?¡!]+$", "", s)
    return s.strip()

class Bank:
    def __init__(self, cat):
        self.cat = cat
        self.rows = []   # dict(fam,q,a,wr,acc,exp,d)
        self.seen = set()
    def add(self, fam, q, a, wr, acc=None, exp="", d=1.0):
        wr = [w for w in dict.fromkeys(wr) if norm(w) != norm(a)]
        if len(wr) < 3:
            raise ValueError(f"[{self.cat}] pocas incorrectas: {q} | {a} | {wr}")
        if len(wr) > 3:
            r = random.Random(q + a)
            wr = r.sample(wr, 3)
        if len({norm(a)} | {norm(w) for w in wr}) != 4:
            raise ValueError(f"[{self.cat}] repetidas: {q} | {a} | {wr}")
        if acc is None:
            acc = [a]
        elif acc:
            acc = list(dict.fromkeys([a] + list(acc)))
        if len(q) > 250: raise ValueError("largo q " + q)
        for o in [a] + wr:
            if len(o) > 60: raise ValueError("largo opcion " + o)
        k = norm(q)
        if k in self.seen:
            return False
        self.seen.add(k)
        self.rows.append(dict(fam=fam, q=q, a=a, wr=wr, acc=acc, exp=exp, d=float(d)))
        return True

CONTR = [("i am","i'm"),("you are","you're"),("he is","he's"),("she is","she's"),("it is","it's"),
 ("we are","we're"),("they are","they're"),("that is","that's"),("what is","what's"),("where is","where's"),
 ("who is","who's"),("how is","how's"),("there is","there's"),("here is","here's"),("is not","isn't"),("are not","aren't"),
 ("was not","wasn't"),("were not","weren't"),("do not","don't"),("does not","doesn't"),("did not","didn't"),
 ("cannot","can't"),("i will","i'll"),("what is","what's"),("let us","let's"),("have not","haven't"),("has not","hasn't")]

def accept_variants(s):
    """variantes: original, contraído, expandido y sin apóstrofo."""
    low = s.lower()
    out = {low}
    exp = low
    for full, con in CONTR:
        exp = re.sub(r"\b" + re.escape(con) + r"\b", full, exp)
    out.add(exp)
    con_s = low
    for full, con in CONTR:
        con_s = re.sub(r"\b" + re.escape(full) + r"\b", con, con_s)
    out.add(con_s)
    for v in list(out):
        if "'" in v:
            out.add(v.replace("'", ""))
    return list(dict.fromkeys([s] + sorted(out)))

# ---------- números ----------
ONES = ["zero","one","two","three","four","five","six","seven","eight","nine","ten","eleven","twelve",
        "thirteen","fourteen","fifteen","sixteen","seventeen","eighteen","nineteen"]
TENS = ["","","twenty","thirty","forty","fifty","sixty","seventy","eighty","ninety"]
def nw(n, and_=False):
    if n < 20: return ONES[n]
    if n < 100: return TENS[n//10] + ("-" + ONES[n%10] if n % 10 else "")
    if n < 1000:
        r = n % 100
        return ONES[n//100] + " hundred" + ((" and " if and_ else " ") + nw(r, and_) if r else "")
    for unit, name in [(10**9,"billion"),(10**6,"million"),(1000,"thousand")]:
        if n >= unit:
            r = n % unit
            return nw(n//unit, and_) + " " + name + (((" and " if (and_ and r < 100) else " ") + nw(r, and_)) if r else "")
def nw_variants(n):
    v = {nw(n), nw(n, True)}
    v |= {x.replace("-", " ") for x in v}
    return [nw(n)] + sorted(v - {nw(n)})

ORD_IRR = {"one":"first","two":"second","three":"third","five":"fifth","eight":"eighth","nine":"ninth","twelve":"twelfth"}
def ordw(n):
    w = nw(n)
    # separar última palabra
    m = re.match(r"^(.*?)([a-z]+)$", w)
    pre, last = m.group(1), m.group(2)
    if last in ORD_IRR: last = ORD_IRR[last]
    elif last.endswith("y"): last = last[:-1] + "ieth"
    else: last = last + "th"
    return pre + last
def ordnum(n):
    if 10 <= n % 100 <= 13: return f"{n}th"
    return f"{n}" + {1:"st",2:"nd",3:"rd"}.get(n % 10, "th")

# ---------- morfología verbal ----------
DOUBLE = {"run","sit","swim","stop","get","put","cut","shop","plan","chat","begin","jog","hit","win","drop","clap","skip"}
def s3(v):
    if v == "have": return "has"
    if v.endswith(("s","sh","ch","x","z","o")): return v + "es"
    if v.endswith("y") and v[-2] not in "aeiou": return v[:-1] + "ies"
    return v + "s"
def ing(v):
    if v.endswith("ie"): return v[:-2] + "ying"
    if v.endswith("e") and not v.endswith("ee"): return v[:-1] + "ing"
    if v in DOUBLE: return v + v[-1] + "ing"
    return v + "ing"

def pick(rng, seq, k=1):
    return rng.sample(list(seq), k)

def lerp(i, n, lo, hi):
    return lo + (hi - lo) * (i / max(1, n - 1))

def cap(s):
    return s[0].upper() + s[1:]
