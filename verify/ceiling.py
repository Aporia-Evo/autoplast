"""Offline least-squares reference for a dumped task (not a rule, not an upper bound).

For every episode it fits the best linear memory for the final state directly,
    S* = argmin_S  sum_i |S k_i - v_i|^2 + lam |S|^2     over the latest (key, value) pairs,
and decodes queries exactly like the Rust evaluator (o = S q, best-matching value embedding;
noisy query vectors are used when the dump contains them). It shows how much headroom an
online rule with the fixed linear readout could have on a regime.

usage: python verify/ceiling.py task.json [lam]
"""

import json
import sys

import numpy as np


def main(path, lam=1e-3):
    t = json.load(open(path))
    d = t["d"]
    K = np.array(t["keys"], dtype=np.float64).reshape(-1, d)
    V = np.array(t["vals"], dtype=np.float64).reshape(-1, d)
    correct = total = 0
    for e in t["episodes"]:
        latest = {}
        for k, v in e["w"]:
            latest[k] = v
        ks = list(latest)
        Kq = K[ks]                       # n x d
        Vq = V[[latest[k] for k in ks]]  # n x d
        S = Vq.T @ Kq @ np.linalg.inv(Kq.T @ Kq + lam * np.eye(d))
        qv = np.array(e["qv"], dtype=np.float64).reshape(-1, d) if e["qv"] else None
        for i, (k, target) in enumerate(e["q"]):
            q = qv[i] if qv is not None else K[k]
            o = S @ q
            total += 1
            if np.linalg.norm(o) < 1e-6:
                continue
            correct += int(np.argmax(V @ o) == target)
    print(f"{path}: offline least-squares reference acc {correct / total:.3f} (lam {lam}, {total} queries)")


if __name__ == "__main__":
    main(sys.argv[1], float(sys.argv[2]) if len(sys.argv) > 2 else 1e-3)
