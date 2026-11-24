import itertools, json, re, subprocess, sys, pathlib
sys.path.insert(0, "verify")
from probe_olam import program as olam
from probe_rls import kalman, program as rls
EXE = "./target/release/autoplast"
def floored(dp, eps, q):
    p = olam(dp, eps)
    if q == 0:
        return p
    p = json.loads(json.dumps(p)); p["persist_m"] = 3
    ins = []
    for i in p["instrs"]:
        i = dict(i)
        if i["op"] == "Outer" and i["out"] == 2: i["out"] = 3
        if i["op"] in ("MatAdd", "MatSub") and i["b"] == 2: i["b"] = 3
        ins.append(i)
    ins += [{"op": "Const", "out": 3, "a": 0, "b": 0, "c": q}, {"op": "MatScale", "out": 3, "a": 3, "b": 2, "c": 0.0},
            {"op": "MatAdd", "out": 1, "a": 1, "b": 3, "c": 0.0}]
    p["instrs"] = ins
    return p
def ev(prog, regime):
    f = pathlib.Path(sys.argv[2]) / "p.json"; f.write_text(json.dumps(prog))
    o = subprocess.run([EXE, "eval", "--prog", str(f), "--regime", regime], capture_output=True, text=True).stdout
    g = lambda pat: float(re.search(pat, o, re.M).group(1))
    return g(r"^train acc ([0-9.]+)"), g(r"test regime \S+: acc ([0-9.]+)"), g(r"T128 K8 ow0.3: acc ([0-9.]+)")
regime = sys.argv[1]
cands = [("untied+qI", (dp, e, q), floored(dp, e, q)) for dp, e, q in itertools.product([0.01, 0.03, 0.1, 0.3, 1.0], [0.0, 0.01, 0.1], [0, 1e-3, 3e-3, 0.01, 0.03])]
cands += [("kalman", (d, q), kalman(d, q)) for d, q in itertools.product([0.01, 0.03, 0.1, 0.3, 1.0], [0.001, 0.003, 0.01, 0.03, 0.1])]
cands += [("rls", (d, r), rls(d, r)) for d, r in itertools.product([0.01, 0.03, 0.1, 0.3, 1.0], [1.0, 1.02, 1.05])]
rows = []
for fam, par, p in cands:
    tr, te, t128 = ev(p, regime)
    rows.append((fam, par, tr, te, t128))
ok = [r for r in rows if r[4] >= 0.838]
best = max(ok, key=lambda r: r[2]) if ok else None
print(regime, "best by train among T128>=0.838:", best)
for fam in ("untied+qI", "kalman", "rls"):
    fr = [r for r in ok if r[0] == fam]
    print("  ", fam, max(fr, key=lambda r: r[2]) if fr else "none")
