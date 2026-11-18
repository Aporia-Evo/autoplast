"""j-lexicase seed 6 without the Normalize epsilon (README, "Package J, arm j-lexicase").

Reference probe only (CLAUDE.md rule 6): hand-written rewrites of an evolved rule, never part of
a population, mutation or fitness. The evolved program writes S' = 1.011 (S + v uᵀ)(I - ûûᵀ), which
is S' = 1.011 S (I - ûûᵀ) in exact arithmetic; its only write is the leak left by the 1e-6 in
Normalize, about 1e-6 (1 + |u|) v ûᵀ. The two rewrites below make that write explicit, at scale 1:
  clean-a: S' = 1.011 [S (I - ûûᵀ) + v ûᵀ]                 (delta rule, beta 1, on the key û)
  clean-b: S' = 1.011 [S (I - ûûᵀ) + (1 + |u|) v ûᵀ]       (the leak's own weighting)
with u = k + P tanh(k), P' = 0.9935 P - 0.366 u uᵀ, P0 = I, as in the evolved program.
Writes JSON programs for `autoplast eval` and `verify.py --task-json`.
"""
import json
import sys

C = dict(beta_src=0.19855946, mul=2.1480, growth=1.0114)


def I(op, out, a=0, b=0, c=0.0):
    return {"op": op, "out": out, "a": a, "b": b, "c": c}


def program(variant):
    p = [
        I("Tanh", 2, 0),           # V2 = tanh(k)
        I("MatVec", 4, 1, 2),      # V4 = P tanh(k)
        I("VecAdd", 4, 0, 4),      # V4 = u = k + P tanh(k)
        I("Normalize", 3, 4),      # V3 = û
        I("Outer", 2, 3, 3),       # M2 = ûûᵀ
        I("MatMul", 3, 0, 2),      # M3 = S ûûᵀ
        I("MatSub", 0, 0, 3),      # S = S (I - ûûᵀ)
        I("Outer", 3, 1, 3),       # M3 = v ûᵀ
        I("MatAdd", 0, 0, 3),
    ]
    if variant == "b":
        p += [I("Outer", 3, 1, 4), I("MatAdd", 0, 0, 3)]   # + v uᵀ = |u| v ûᵀ
    p += [
        I("Const", 3, c=C["growth"]),
        I("MatScale", 0, 3, 0),    # S = 1.011 S
        # P update, constants as evolved: s1 = σ(Recip(0.1986)), s2 = (σ(0.1986·2.148) |u|)²
        I("Const", 2, c=C["beta_src"]),
        I("Recip", 3, 2),
        I("Sigmoid", 1, 3),
        I("Const", 0, c=C["mul"]),
        I("SMul", 0, 2, 0),
        I("Sigmoid", 2, 0),
        I("VecScale", 5, 2, 4),
        I("Norm", 0, 5),
        I("SMul", 2, 0, 0),
        I("MatScale", 3, 1, 1),    # M3 = s1 P
        I("MatScale", 2, 2, 2),    # M2 = s2 ûûᵀ
        I("MatSub", 1, 3, 2),      # P' = s1 P - s2 ûûᵀ
    ]
    return {"persist_m": 3, "persist_v": 0, "persist_identity": 1, "instrs": p}


if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else "."
    for v in "ab":
        json.dump(program(v), open(f"{out}/j6_clean_{v}.json", "w"), indent=1)
        print(f"{out}/j6_clean_{v}.json")
