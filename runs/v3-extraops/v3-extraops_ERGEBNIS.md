# v3-extraops: result (16 seeds, 1.5M candidates, task v3, --extra-ops)

Time: 2026-11-04 15:25 UTC. Seed 2 ran locally (4 Nov 2026, Ryzen 5700G, 2,695 s) before the abort; seeds 1
and 3-16 ran on the JupyterHub (jh.ide3.de, cargo 1.99.1) after the resume, 24,120 s wall in
total, all exit 0. Equality hub vs local was checked before the resume (identical log rows).
The aggregate printed on the hub says "local" because that is the runner's fixed label.
Aborted local partial seeds 1, 3, 4, 5 are kept unchanged in aborted_local/.
Prediction and decision rule: runs/v3-nomatvec/3a_VORHERSAGE.md (with addenda 1 and 2).
JAX check for all 16 seeds: seedN/verify.txt, v3-extraops_verify_table.csv.

| seed | delta 0.5 at | extra ops in best rule | len | decomposition | R² | train | T12 ow0.3 | JAX | T64 K8 | T128 K8 | JAX | d32 T24 | train − mix | wall s |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | 1,253,492 | none | 15 | `+1.000·S +0.949·(v kᵀ) -0.598·((S k) kᵀ)` | 0.9999 | 0.909 | 0.919 | 0.914 | 0.853 | 0.852 | 0.854 | 0.983 | 0.010 | 4314 |
| 2 | 998,644 | VecMax | 15 | `+1.000·S +0.502·(v kᵀ) -0.600·((S k) kᵀ)` | 0.9994 | 0.912 | 0.914 | 0.910 | 0.850 | 0.845 | 0.852 | 0.974 | 0.017 | 2695 |
| 3 | no | MatTanh | 14 | `-0.940·S +0.941·(v kᵀ) +0.011·((S k) kᵀ)` | 0.3107 | 0.789 | 0.835 | 0.823 | 0.680 | 0.666 | 0.680 | 0.913 | 0.001 | 5117 |
| 4 | no | MatTanh | 4 | `+0.923·S +2.000·(v kᵀ) +0.000·((S k) kᵀ)` | 0.9971 | 0.720 | 0.797 | 0.786 | 0.532 | 0.537 | 0.539 | 0.882 | 0.003 | 793 |
| 5 | 1,301,236 | none | 13 | `+0.999·S +0.999·(v kᵀ) -0.597·((S k) kᵀ)` | 0.9991 | 0.903 | 0.916 | 0.912 | 0.849 | 0.847 | 0.854 | 0.975 | 0.007 | 4849 |
| 6 | no | MatTanh | 21 | `+0.995·S +0.839·(v kᵀ) -1.244·((S k) kᵀ)` | 0.9607 | 0.893 | 0.909 | 0.898 | 0.787 | 0.737 | 0.762 | 0.950 | 0.021 | 11266 |
| 7 | no | MatTanh | 7 | `+0.923·S +2.101·(v kᵀ) +0.000·((S k) kᵀ)` | 0.9971 | 0.724 | 0.796 | 0.784 | 0.542 | 0.538 | 0.551 | 0.881 | 0.004 | 1300 |
| 8 | 772,468 | VecMax | 15 | `+1.000·S +0.910·(v kᵀ) -0.768·((S k) kᵀ)` | 0.9977 | 0.918 | 0.935 | 0.928 | 0.843 | 0.841 | 0.852 | 0.987 | 0.011 | 3258 |
| 9 | no | MatTanh | 7 | `+0.850·S +0.874·(v kᵀ) +0.000·((S k) kᵀ)` | 0.9966 | 0.727 | 0.772 | 0.764 | 0.578 | 0.551 | 0.573 | 0.767 | 0.013 | 1450 |
| 10 | 30,708 | VecMax | 13 | `+1.000·S +0.645·(v kᵀ) -0.594·((S k) kᵀ)` | 0.9995 | 0.908 | 0.919 | 0.914 | 0.852 | 0.846 | 0.848 | 0.981 | 0.009 | 1338 |
| 11 | 698,356 | none | 7 | `+1.000·S +0.711·(v kᵀ) -0.562·((S k) kᵀ)` | 1.0000 | 0.907 | 0.922 | 0.916 | 0.853 | 0.851 | 0.847 | 0.985 | 0.006 | 1341 |
| 12 | no | VecRelu,VecMax,VecSigmoid,MatTanh,VecSum,SAbs | 19 | `+0.975·S +2.000·(v kᵀ) -0.004·((S k) kᵀ)` | 0.9994 | 0.763 | 0.805 | 0.798 | 0.582 | 0.554 | 0.566 | 0.852 | 0.025 | 1445 |
| 13 | no | MatHadamard,MatTanh | 11 | `+0.724·S +0.844·(v kᵀ) -0.008·((S k) kᵀ)` | 0.9640 | 0.730 | 0.786 | 0.772 | 0.566 | 0.552 | 0.562 | 0.878 | 0.010 | 6395 |
| 14 | 1,022,324 | VecMax | 16 | `+0.999·S +0.676·(v kᵀ) -0.590·((S k) kᵀ)` | 0.9985 | 0.904 | 0.911 | 0.905 | 0.849 | 0.850 | 0.853 | 0.976 | 0.012 | 1455 |
| 15 | 325,492 | none | 11 | `+1.000·S +0.570·(v kᵀ) -0.601·((S k) kᵀ)` | 0.9997 | 0.913 | 0.922 | 0.915 | 0.854 | 0.855 | 0.849 | 0.985 | 0.011 | 925 |
| 16 | 1,285,876 | MatTanh | 13 | `+1.000·S +3.001·(v kᵀ) -0.197·((S k) kᵀ)` | 0.9993 | 0.913 | 0.930 | 0.924 | 0.846 | 0.845 | 0.840 | 0.989 | 0.008 | 1928 |

Rates and decision rule:
- Delta beta=0.5: 9/16 (Wilson 95 % 33.2% to 76.9%) against 12/16 on v3 with the
  default alphabet. Fisher exact two-sided p = 0.458. By the rule fixed in advance (significant
  only at 5/16 or fewer): no significant drop.
- Candidates when reached: 30,708, 325,492, 698,356, 772,468, 998,644, 1,022,324, 1,253,492, 1,285,876, 1,301,236; median 998,644
  (v3 default alphabet: 168,628). Descriptive: the search reaches delta about six times later.
- The 7 seeds without delta all have MatTanh (elementwise tanh of the matrix, a saturating
  memory) in their best rule; 5 of them sit at linear-attention level on long episodes
  (T128 0.537 to 0.554), seed 3 at 0.666 and seed 6 at 0.737 (T12 0.909, no delta).
- 4 of the 9 delta seeds use VecMax, one MatTanh; the extra ops are used, not ignored.

Checks:
- JAX reproduction: max |JAX − Rust| 0.030 (T64 K8), 0.025 (T128 K8), at most 0.014 elsewhere;
  no suite diverged.
- Growth factor: all 9 delta seeds have a = 0.999 to 1.000.
- Overfitting: train − mix at most 0.025.
- Against tuned DeltaNet on v3 (T12 0.923, T64 0.852, T128 0.850): delta seeds T12 0.911 to
  0.935, T64 0.843 to 0.854, T128 0.841 to 0.855. No seed is better beyond noise.

Reading: diluting the alphabet with ten generic ops does not stop the search from finding the
delta family (9/16, not significantly fewer than 12/16), but it slows it down about sixfold and
opens a competing basin, a saturating tanh memory, that captures most failed seeds. With 16
seeds per arm the test can only detect large drops; a drop from 12 to 9 is not excluded.
The no-MatVec arm was not run (held by the user), so the "short path" question is open.

Predictions vs outcome (extra-ops arm):
- Delta by at least 1 seed (p 0.9): yes, 9.
- Rate not significantly below v3 (p 0.65): yes, p = 0.458.
- At least one best rule uses an extra op (p 0.8): yes, 12 of 16.
- Every delta seed T128 at least 0.75 (p 0.6): yes, min 0.841.
- No seed beats tuned DeltaNet on T128 by more than 0.02 (p 0.8): yes, max +0.005.
- Pilot wall time 2 to 6 min per seed (p 0.6): no (see pilot result).
No-MatVec predictions: untested.
