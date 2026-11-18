"""Does a rule's memory live on the epsilon of Normalize? (README, "Package J, arm j-lexicase")

    python verify/eps_scale.py --task-json task.json runs/<tag>/seed6/best.json ...

Runs each program in float64 with Normalize epsilon 1e-6 (as in Rust) and 1e-3 and prints the
median over episodes of max|S| at the end of the episode. A ratio near 1000 means S is made of the
epsilon itself: the rule writes nothing in exact arithmetic and scores only because argmax
decoding ignores the scale of S (CLAUDE.md rule 3). A ratio near 1 means the epsilon is at most a
numerical floor. Use it on seeds whose accuracy moves under `verify.py --x64 --norm-eps 1e-9`.
"""
import json
import sys

sys.argv = [sys.argv[0], "--x64"] + sys.argv[1:]  # float64 must be set before verify is imported
sys.path.insert(0, __file__.rsplit("/", 1)[0])
import jax  # noqa: E402
import jax.numpy as jnp  # noqa: E402
import numpy as np  # noqa: E402

import verify as V  # noqa: E402

i = sys.argv.index("--task-json")
tasks = V.load_task_json(sys.argv[i + 1])
paths = sys.argv[2:i] + sys.argv[i + 2 :]
for path in paths:
    prog = json.load(open(path))
    row = []
    for eps in (1e-6, 1e-3):
        V.NORM_EPS = eps
        step = V.build_step(prog["instrs"], pm=prog.get("persist_m", 1), pv=prog.get("persist_v", 0), ident=bool(prog.get("persist_identity", 0)))
        init = getattr(step, "init", lambda d: jnp.zeros((d, d)))
        mem = (lambda st: st[0]) if hasattr(step, "init") else (lambda st: st)
        mags = []
        for t in tasks:
            keys, vals, W = t[0], t[1], t[2]
            d = keys.shape[1]

            def ep(w):
                def body(st, kv):
                    return step(st, keys[kv[0]], vals[kv[1]]), None

                st, _ = jax.lax.scan(body, init(d), w)
                return jnp.max(jnp.abs(mem(st)))

            mags.append(np.asarray(jax.jit(jax.vmap(ep))(W)))
        row.append(float(np.median(np.concatenate(mags))))
    print(f"{path}: median max|S|  eps 1e-6: {row[0]:.3g}  eps 1e-3: {row[1]:.3g}  ratio {row[1] / row[0]:.3g}")
