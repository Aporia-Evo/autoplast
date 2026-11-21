"""Long-horizon probe in JAX (21 Nov 2026): max |state| over all persistent registers and
accuracy on collision-type episodes (8 clusters, cos 0.85, at most 8 keys, overwrite 0.3) of
length T. Reference check only.

    python verify/long_probe_jax.py 1024 rule.json [more.json ...]
"""
import json, sys
sys.path.insert(0, "verify")
import numpy as np, jax, jax.numpy as jnp
import verify as V
T = int(sys.argv[1]); paths = [a for a in sys.argv[2:] if a.endswith(".json")]
for p in paths:
    prog = json.load(open(p))
    step = V.build_step(prog["instrs"], pm=prog["persist_m"], pv=0, ident=prog["persist_identity"] == 1)
    out = []
    for seed in range(4):
        rng = np.random.default_rng(1000 + seed)
        keys, vals, W, Q, Qm = V.make_task(rng, 16, 512, 512, T, 0.3, 32, max_keys=8, clusters=8, cluster_cos=0.85)
        def episode(w):
            def body(c, kv):
                st, mx = c
                st = step(st, keys[kv[0]], vals[kv[1]])
                S, em, _ = st
                m = jnp.max(jnp.array([jnp.max(jnp.abs(S))] + [jnp.max(jnp.abs(x)) for x in em]))
                m = jnp.where(jnp.isfinite(m), m, jnp.inf)
                return (st, jnp.maximum(mx, m)), None
            (st, mx), _ = jax.lax.scan(body, (step.init(16), V.FT(0.0)), w)
            return mx
        mx = jax.jit(jax.vmap(episode))(W)
        out.append(float(jnp.max(mx)))
    acc = V.accuracy(step, V.make_task(np.random.default_rng(7), 16, 512, 512, T, 0.3, 64, max_keys=8, clusters=8, cluster_cos=0.85))[0]
    print(f"{p.split('/')[-1]}: T={T} max|state| per draw {['%.1f' % x for x in out]}  acc {acc:.3f}")
