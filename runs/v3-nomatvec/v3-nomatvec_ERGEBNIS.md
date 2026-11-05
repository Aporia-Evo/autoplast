# v3-nomatvec: result (16 seeds, 1.5M candidates, task v3, --no-op MatVec)

Time: 2026-11-04 19:10 UTC. Ran on the JupyterHub (jh.ide3.de, same binary as the extra-ops arm; equality hub vs
local checked before the extra-ops resume). Command as in runs/v3-nomatvec/3a_VORHERSAGE.md;
total wall 12,362 s, all 16 seeds exit 0. The hub aggregate (aggregate_hub.md) says "local"
because that is the runner's fixed label. JAX check: seedN/verify.txt, v3-nomatvec_verify_table.csv.

| seed | delta 0.5 at | MatMul in rule | len | decomposition | R² | train | T12 ow0.3 | JAX | T64 K8 | T128 K8 | JAX | d32 T24 | train − mix | wall s |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | 1,076,980 | yes | 10 | `+1.004·S +0.404·(v kᵀ) -0.598·((S k) kᵀ)` | 1.0000 | 0.908 | 0.923 | 0.917 | 0.854 | 0.851 | 0.845 | 0.986 | 0.006 | 998 |
| 2 | 49,140 | yes | 17 | `+1.000·S +0.903·(v kᵀ) -0.587·((S k) kᵀ)` | 0.9993 | 0.910 | 0.918 | 0.911 | 0.847 | 0.842 | 0.850 | 0.977 | 0.013 | 5323 |
| 3 | 60,788 | yes | 11 | `+1.000·S +0.639·(v kᵀ) -0.606·((S k) kᵀ)` | 0.9999 | 0.909 | 0.917 | 0.914 | 0.853 | 0.856 | 0.855 | 0.983 | 0.011 | 3726 |
| 4 | no | no | 4 | `+0.907·S +1.000·(v kᵀ) +0.000·((S k) kᵀ)` | 1.0000 | 0.725 | 0.769 | 0.763 | 0.571 | 0.555 | 0.567 | 0.734 | 0.015 | 344 |
| 5 | no | no | 5 | `+0.907·S +0.907·(v kᵀ) +0.000·((S k) kᵀ)` | 1.0000 | 0.725 | 0.769 | 0.763 | 0.571 | 0.555 | 0.567 | 0.734 | 0.015 | 847 |
| 6 | no | yes | 11 | `+0.908·S +1.000·(v kᵀ) -0.000·((S k) kᵀ)` | 0.9997 | 0.728 | 0.771 | 0.763 | 0.571 | 0.552 | 0.567 | 0.737 | 0.017 | 2394 |
| 7 | 1,356,532 | yes | 21 | `+1.007·S +1.546·(v kᵀ) -0.637·((S k) kᵀ)` | 0.9985 | 0.916 | 0.919 | 0.913 | 0.847 | 0.843 | 0.849 | 0.982 | 0.019 | 2864 |
| 8 | no | no | 4 | `+0.907·S +0.907·(v kᵀ) -0.000·((S k) kᵀ)` | 1.0000 | 0.725 | 0.769 | 0.763 | 0.571 | 0.555 | 0.567 | 0.734 | 0.015 | 437 |
| 9 | no | no | 4 | `+0.907·S +1.000·(v kᵀ) -0.000·((S k) kᵀ)` | 1.0000 | 0.725 | 0.769 | 0.763 | 0.571 | 0.555 | 0.567 | 0.734 | 0.015 | 353 |
| 10 | no | yes | 13 | `+0.949·S +0.949·(v kᵀ) -0.101·((S k) kᵀ)` | 0.9887 | 0.755 | 0.808 | 0.795 | 0.568 | 0.540 | 0.549 | 0.893 | 0.019 | 2191 |
| 11 | no | no | 4 | `+0.907·S +0.907·(v kᵀ) -0.000·((S k) kᵀ)` | 1.0000 | 0.725 | 0.769 | 0.763 | 0.571 | 0.555 | 0.567 | 0.734 | 0.015 | 550 |
| 12 | no | no | 6 | `+0.907·S +1.000·(v kᵀ) +0.000·((S k) kᵀ)` | 1.0000 | 0.725 | 0.769 | 0.763 | 0.571 | 0.555 | 0.567 | 0.734 | 0.015 | 456 |
| 13 | no | no | 4 | `+0.907·S +1.000·(v kᵀ) -0.000·((S k) kᵀ)` | 1.0000 | 0.725 | 0.769 | 0.763 | 0.571 | 0.555 | 0.567 | 0.734 | 0.015 | 349 |
| 14 | no | no | 7 | `+0.907·S +1.000·(v kᵀ) -0.000·((S k) kᵀ)` | 1.0000 | 0.725 | 0.769 | 0.763 | 0.571 | 0.555 | 0.567 | 0.734 | 0.015 | 498 |
| 15 | no | no | 5 | `+0.907·S +1.000·(v kᵀ) -0.000·((S k) kᵀ)` | 1.0000 | 0.725 | 0.769 | 0.763 | 0.571 | 0.555 | 0.567 | 0.734 | 0.015 | 382 |
| 16 | 384,372 | yes | 10 | `+1.000·S +0.948·(v kᵀ) -0.607·((S k) kᵀ)` | 0.9998 | 0.908 | 0.917 | 0.912 | 0.856 | 0.857 | 0.857 | 0.983 | 0.009 | 1664 |

Rates and decision rule:
- Delta beta=0.5: 5/16 (Wilson 95 % 14.2% to 55.6%) against 12/16 with the default
  alphabet. Fisher exact two-sided p = 0.032. By the rule fixed in advance (significant at
  5/16 or fewer): significant drop. The result sits exactly at the threshold.
- Candidates when reached: 49,140, 60,788, 384,372, 1,076,980, 1,356,532; median 384,372 (v3: 168,628).
- All 5 delta rules build S·k through MatMul with an outer product of k, e.g. seed 1
  `S' = (S + v kᵀ) − 0.596·(S + v kᵀ)(k kᵀ)` and seed 16 `S' = S − 0.674·S(tanh k tanh kᵀ) + …`.
- The 11 other seeds stay at decayed linear attention, almost all exactly `0.907·S + v kᵀ`
  (a = σ(2.278)); T128 K8 0.540 to 0.555. Most of them ended early
  (344 to 850 s), i.e. the population settled in this basin without growing MatMul paths.

Checks:
- JAX reproduction: max |JAX − Rust| 0.015 over all six shared suites; no suite diverged.
- Growth factor: delta seeds a = 1.000 to 1.007.
- Overfitting: train − mix at most 0.019.
- Against tuned DeltaNet on v3 (T12 0.923, T64 0.852, T128 0.850): delta seeds T12 0.917 to
  0.923, T64 0.847 to 0.856, T128 0.842 to 0.857. No seed better beyond noise.

Predictions vs outcome (no-MatVec arm):
- Delta by at least 1 seed (p 0.9): yes, 5.
- Rate not significantly below v3 (p 0.6): no, p = 0.032.
- Median candidates higher than v3's 168,628 (p 0.7): yes, 384,372.
- Found delta rules use MatMul with an outer product of k (p 0.85): yes, 5 of 5.
- Every delta seed T128 at least 0.75 (p 0.6): yes, min 0.842.
- No seed beats tuned DeltaNet on T128 by more than 0.02 (p 0.8): yes, max +0.007.

## 3a overall (both arms)

| alphabet | delta seeds | Fisher p vs default | median candidates to delta | failed seeds end in |
|---|---|---|---|---|
| default (runs/v3) | 12/16 | | 168,628 | decayed linear attention |
| + 10 generic extra ops | 9/16 | 0.458 | 998,644 | saturating tanh memory (MatTanh) |
| without MatVec | 5/16 | 0.032 | 384,372 | decayed linear attention |

Reading: the rediscovery rate depends on the alphabet. Removing the one op that gives S·k in a
single step (delta then needs five instructions instead of four) cuts the rate from 12/16 to
5/16; diluting the alphabet slows the search about sixfold without a significant drop in rate.
The delta family is still reachable from scratch in every variant, and wherever it is found it
lands at the same accuracy as tuned DeltaNet. For the rediscovery claim this means: the search
finds the rule because the task demands it, but how often it finds it within the budget is
largely set by how short the rule is in the given alphabet. This must be stated alongside any
rate. With 16 seeds per arm and p = 0.032 exactly at the pre-set threshold, the no-MatVec drop
is a single borderline test, not a robust effect size.
