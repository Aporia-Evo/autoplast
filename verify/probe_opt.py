"""Testbed 2 references (README, "Testbed 2: optimizer update rules"): the ladder SGD, momentum,
RMSProp, Adam written by hand as programs of the space, tuned by grid on the train task, and the
ceiling. References only (CLAUDE.md rule 6): never a candidate, seed or mutation.

Register convention: V0 = w on entry, new w in V0 on exit, V1 = g; V2 (first moment) and V3
(second moment) persistent, zero at the start of an episode. Adam without bias correction (the
program gets no step counter). The 1e-6 inside VecRecip stands in for Adam's epsilon.

    python verify/probe_opt.py [--task-seed N] [--out runs/sweeps/probe_opt.md]
"""
import itertools
import json
import pathlib
import subprocess
import sys
import tempfile

ROOT = pathlib.Path(__file__).parent.parent
EXE = str(ROOT / "target/release/autoplast")
FLAGS = ["--task", "opt", "--opt-ops", "--persist-v", "2"]


def ins(op, out, a=0, b=0, c=0.0):
    return {"op": op, "out": out, "a": a, "b": b, "c": c}


def prog(instrs):
    return {"persist_m": 1, "persist_v": 2, "persist_identity": 0, "instrs": instrs}


def sgd(eta):
    return prog([ins("Const", 0, c=eta), ins("VecScale", 4, 0, 1), ins("VecSub", 0, 0, 4)])


def momentum(eta, beta):
    return prog([ins("Const", 0, c=beta), ins("VecScale", 2, 0, 2), ins("VecAdd", 2, 2, 1),
                 ins("Const", 1, c=eta), ins("VecScale", 4, 1, 2), ins("VecSub", 0, 0, 4)])


def second_moment(beta2):
    # V3 = beta2·V3 + (1 − beta2)·g⊙g ; V5 = 1/sqrt(V3)
    return [ins("Hadamard", 4, 1, 1), ins("Const", 2, c=1 - beta2), ins("VecScale", 4, 2, 4),
            ins("Const", 3, c=beta2), ins("VecScale", 3, 3, 3), ins("VecAdd", 3, 3, 4),
            ins("VecSqrt", 5, 3), ins("VecRecip", 5, 5)]


def rmsprop(eta, beta2):
    return prog(second_moment(beta2) + [ins("Hadamard", 5, 1, 5), ins("Const", 0, c=eta),
                                         ins("VecScale", 5, 0, 5), ins("VecSub", 0, 0, 5)])


def adam(eta, beta1, beta2):
    first = [ins("Const", 0, c=beta1), ins("VecScale", 2, 0, 2), ins("Const", 1, c=1 - beta1),
             ins("VecScale", 4, 1, 1), ins("VecAdd", 2, 2, 4)]
    return prog(first + second_moment(beta2) + [ins("Hadamard", 5, 2, 5), ins("Const", 0, c=eta),
                                                ins("VecScale", 5, 0, 5), ins("VecSub", 0, 0, 5)])


ETAS = [0.003, 0.005, 0.01, 0.02, 0.03, 0.05, 0.1, 0.2, 0.3, 0.5, 0.7, 1.0, 1.5, 2.0, 3.0]
FAMILIES = [
    ("SGD", sgd, [(e,) for e in ETAS]),
    ("momentum", momentum, list(itertools.product(ETAS, [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 0.95]))),
    ("RMSProp", rmsprop, list(itertools.product(ETAS, [0.5, 0.7, 0.9, 0.95, 0.99, 0.999]))),
    ("Adam", adam, list(itertools.product(ETAS, [0.0, 0.2, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 0.95], [0.5, 0.7, 0.9, 0.95, 0.99, 0.999]))),
]


def evalmany(progs, extra):
    with tempfile.TemporaryDirectory() as tmp:
        f = pathlib.Path(tmp) / "p.jsonl"
        f.write_text("\n".join(json.dumps(p) for p in progs) + "\n")
        out = subprocess.run([EXE, "evalmany", "--in", str(f), "--threads", "4"] + FLAGS + extra,
                             capture_output=True, text=True, check=True).stdout
    return [tuple(float(x) for x in l.split()) for l in out.splitlines() if l.strip()]


SUITES = ["train distribution", "kappa 1000", "d 32", "d 8", "sigma 0.3", "T 200", "scale 10 / 0.1"]

if __name__ == "__main__":
    ts = sys.argv[sys.argv.index("--task-seed") + 1] if "--task-seed" in sys.argv else "1"
    out_path = sys.argv[sys.argv.index("--out") + 1] if "--out" in sys.argv else None
    lines = [f"# Testbed 2 references, tuned on the train task of task seed {ts}\n",
             "Objective: mean log10(f(w_T)/f(w_0)) over episodes, lower is better; div = fraction of diverged episodes.\n"]
    best = {}
    for name, fam, grid in FAMILIES:
        progs = [fam(*p) for p in grid]
        res = evalmany(progs, ["--task-seed", ts])
        ok = [(r[0], p, q) for r, p, q in zip(res, grid, progs) if r[1] == 0.0]
        obj, params, q = min(ok, key=lambda x: x[0])
        best[name] = (params, q, obj)
    header = "| rule | parameters | train | " + " | ".join(SUITES) + " |"
    lines += [header, "|" + "---|" * (3 + len(SUITES))]
    for name, (params, q, obj) in best.items():
        cells = []
        for i in range(1, 8):
            o, dv, _ = evalmany([q], ["--split", "test", "--suite", str(i)])[0]
            cells.append(f"{o:.3f}" + (f" (div {dv:.2f})" if dv > 0 else ""))
        lines.append(f"| {name} | {', '.join(f'{x:g}' for x in params)} | {obj:.3f} | " + " | ".join(cells) + " |")
    ceil = subprocess.run([EXE, "ceiling"] + FLAGS + ["--task-seed", ts], capture_output=True, text=True).stdout
    lines += ["", "Grid edges: a best value on the edge of its grid is marked in the table below if any.",
              "", "Ceiling (not expressible in the space). `optimum`: w* on the quadratics, the least-squares",
              "solution on regression. `newton`: Newton steps with the exact Hessian on the same stochastic",
              "gradients; noise-limited, so not a ceiling, shown for reference.", "", "```", ceil.strip(), "```"]
    for name, fam, grid in FAMILIES:
        params = best[name][0]
        for j, x in enumerate(params):
            vals = sorted({p[j] for p in grid})
            if x in (vals[0], vals[-1]) and len(vals) > 1:
                lines.append(f"- {name}: parameter {j + 1} = {x:g} is on the edge of its grid")
    text = "\n".join(lines)
    print(text)
    if out_path:
        pathlib.Path(out_path).write_text(text + "\n")
        for name, (params, q, obj) in best.items():
            (pathlib.Path(out_path).parent / f"opt_ref_{name}.json").write_text(json.dumps(q))
