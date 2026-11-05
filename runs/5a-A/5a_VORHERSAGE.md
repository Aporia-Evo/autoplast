# 5a on collision3: prediction and decision rule (written before the runs)

Time: 2026-11-05 06:37 UTC. Code d4f64b8 (README "Evolved readout", "Stage-2 regimes"). Runs on the JupyterHub,
one after the other, 16 seeds x 1.5M each, two seeds in parallel with 8 threads:
- A: `local_runner.py --seeds 1-16 --budget 1500000 --tag 5a-A --regime collision3 --parallel 2 --threads 8`
- B: `... --tag 5a-B --regime collision3 --evolve-readout --extra-ops ...`
- C: `... --tag 5a-C --regime collision3 --evolve-readout ...`
Reference on the collision3 test (512 + 256 episodes, 6,503 queries): tuned DeltaNet = tuned
Gated DeltaNet 0.631 (T128 K8 0.858), LS reference 1.000. Standard error of an accuracy near
0.63 on 6,503 queries is about 0.006.

Decision rules, fixed now:
1. Arm comparison: per-seed collision3 test accuracy of the best rule; B vs A and C vs A by a
   two-sided Mann-Whitney U test (16 vs 16), significant at p < 0.05.
2. A seed counts as "beats tuned DeltaNet" only if its best rule is above 0.631 + 0.02 = 0.651
   on the collision3 test AND not more than 0.02 below 0.858 on T128 K8 AND train minus test is
   at most 0.03. Any such seed then needs JAX verification and a check against the known
   neighbours (multi-step delta / DeltaProduct, RLS / Mesa layer, the readout family it uses)
   before anything is called better or new.

Predictions (subjective probabilities):
- A: at least one seed reaches the delta milestone (p 0.7); median test accuracy of the 16
  best rules between 0.55 and 0.64 (p 0.6); no A seed beats tuned DeltaNet (p 0.8).
- B: at least one seed beats tuned DeltaNet by rule 2 (p 0.35). C: same (p 0.3).
- B significantly above A by rule 1 (p 0.3); C significantly above A (p 0.25).
- At least one best rule over all arms has a non-empty effective read program (p 0.75).
- Wall time on the hub: A 5 to 9 h, B 9 to 16 h, C 3 to 5 h (p 0.6).
