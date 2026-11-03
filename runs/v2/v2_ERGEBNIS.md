# v2: result (16 seeds, 1.5M candidates, local)

Time: 2026-11-03 17:20 UTC. Commit 62cbf63 (branch exp/v2-rediscovery-rate). Command:
`python local_runner.py --seeds 1-16 --budget 1500000 --tag v2 --parallel 2 --threads 8`
(add-node on). Ryzen 5700G, total wall 7,600 s (2.1 h). All 16 seeds exit 0.
Prediction: v2_VORHERSAGE.md (written before the run). Aggregate: aggregate.md.
JAX check: `verify/verify.py runs/v2/seedN/best.json` for all 16 seeds (jax 0.10.2, CPU),
outputs in seedN/verify.txt, table in v2_verify_table.csv.

| seed | family | len | delta 0.5 at | decomposition a·S + b·vkᵀ + c·(Sk)kᵀ | R² | train | test ow0.3 | JAX ow0.3 | ow0.0 | ow0.6 | d32 T24 | d8 T6 | wall s |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | decayed LA | 6 | no | `+0.958·S +1.000·(v kᵀ) -0.000·((S k) kᵀ)` | 1.0000 | 0.814 | 0.787 | 0.778 | 0.884 | 0.636 | 0.874 | 0.633 | 510 |
| 2 | decayed LA | 6 | no | `+0.949·S +0.908·(v kᵀ) +0.000·((S k) kᵀ)` | 0.9997 | 0.817 | 0.789 | 0.775 | 0.865 | 0.648 | 0.878 | 0.637 | 504 |
| 3 | delta | 10 | 61,044 | `+1.098·S +0.748·(v kᵀ) -0.748·((S k) kᵀ)` | 0.9998 | 0.975 | 0.966 | 0.961 | 0.951 | 0.964 | 0.976 | 0.836 | 717 |
| 4 | decayed LA | 6 | no | `+0.950·S +0.908·(v kᵀ) +0.000·((S k) kᵀ)` | 0.9997 | 0.817 | 0.788 | 0.775 | 0.867 | 0.647 | 0.879 | 0.636 | 527 |
| 5 | decayed LA | 4 | no | `+0.958·S +1.000·(v kᵀ) +0.000·((S k) kᵀ)` | 1.0000 | 0.814 | 0.787 | 0.778 | 0.884 | 0.636 | 0.874 | 0.633 | 445 |
| 6 | delta | 12 | 1,207,284 | `+1.153·S +0.877·(v kᵀ) -0.877·((S k) kᵀ)` | 0.9993 | 0.969 | 0.965 | 0.957 | 0.949 | 0.959 | 0.886 | 0.845 | 934 |
| 7 | delta | 11 | 440,436 | `+1.098·S +0.748·(v kᵀ) -0.748·((S k) kᵀ)` | 0.9998 | 0.975 | 0.966 | 0.961 | 0.951 | 0.964 | 0.975 | 0.836 | 1114 |
| 8 | delta | 12 | 111,476 | `+1.055·S +1.782·(v kᵀ) -0.446·((S k) kᵀ)` | 0.9986 | 0.969 | 0.961 | 0.954 | 0.954 | 0.959 | 0.994 | 0.813 | 785 |
| 9 | decayed LA | 6 | no | `+0.949·S +0.908·(v kᵀ) +0.000·((S k) kᵀ)` | 0.9997 | 0.817 | 0.789 | 0.775 | 0.865 | 0.648 | 0.878 | 0.637 | 464 |
| 10 | decayed LA | 4 | no | `+0.958·S +0.958·(v kᵀ) +0.000·((S k) kᵀ)` | 1.0000 | 0.814 | 0.787 | 0.778 | 0.884 | 0.636 | 0.874 | 0.633 | 358 |
| 11 | decayed LA + weak value-side erase | 11 | no | `+0.952·S +0.904·(v kᵀ) -0.109·((S k) kᵀ)` | 0.9884 | 0.836 | 0.809 | 0.795 | 0.856 | 0.723 | 0.868 | 0.680 | 2279 |
| 12 | delta | 14 | 41,588 | `+1.089·S +0.901·(v kᵀ) -0.689·((S k) kᵀ)` | 0.9999 | 0.973 | 0.966 | 0.961 | 0.955 | 0.963 | 0.969 | 0.831 | 2107 |
| 13 | decayed LA | 4 | no | `+0.958·S +0.958·(v kᵀ) +0.000·((S k) kᵀ)` | 1.0000 | 0.814 | 0.787 | 0.778 | 0.884 | 0.636 | 0.874 | 0.633 | 248 |
| 14 | decayed LA | 14 | no | `+0.949·S +1.855·(v kᵀ) +0.000·((S k) kᵀ)` | 0.9990 | 0.821 | 0.787 | 0.776 | 0.867 | 0.648 | 0.878 | 0.634 | 1812 |
| 15 | decayed LA + weak value-side erase | 12 | no | `+0.954·S +0.953·(v kᵀ) -0.121·((S k) kᵀ)` | 0.9858 | 0.840 | 0.808 | 0.795 | 0.852 | 0.723 | 0.871 | 0.668 | 1625 |
| 16 | delta | 12 | 14,836 | `+1.108·S +0.725·(v kᵀ) -0.772·((S k) kᵀ)` | 0.9995 | 0.972 | 0.967 | 0.962 | 0.951 | 0.960 | 0.942 | 0.826 | 387 |

Rates:
- Linear attention milestone: 16/16 seeds, median 23,412 candidates.
- Delta rule beta=0.5 milestone: 6/16 seeds (37.5 %, Wilson 95 % interval 18.5 % to 61.4 %).
  Candidates when reached: 14,836 / 41,588 / 61,044 / 111,476 / 440,436 / 1,207,284;
  median 86,260 (aggregate.md prints the upper median, 111,476).
- The other 10 seeds end at decayed linear attention (a about 0.95, c about 0), test ow0.3
  0.787 to 0.809. Seeds 11 and 15 add a weak erase along the value direction,
  `-2(k·u)(S k) uᵀ` with u = tanh(v) (normalized in seed 15); it is linear in S.

Checks:
- JAX reproduction: max |JAX - Rust| over the four shared test suites is 0.018.
- Overfitting: train minus test ow0.3 is 0.004 to 0.009 for the six delta seeds and 0.027
  to 0.034 for the decayed-LA seeds (linear attention itself: 0.772 vs 0.750).
- Growth factor: all six delta seeds have a > 1 (1.055 to 1.153), as tuned Gated DeltaNet
  (a = 1.1). This is the short-episode artefact named in CLAUDE.md; queue item 3 targets it.
- Against tuned Gated DeltaNet (sweep: 0.968 / 0.957 / 0.964 / 0.957 / 0.841), the best
  delta seeds reach 0.961 to 0.967 on ow0.3. No seed is better on the main held-out suite.
  The higher d32 T24 values (seed 8: 0.994) are one seed with a > 1 and are not a claim.

Predictions vs outcome:
- Linear attention 16/16 (p 0.9): yes.
- Delta beta=0.5 by at least 1 seed (p 0.9): yes. By 3 to 9 of 16 (p 0.6): yes, 6.
- Median 400k to 1.2M candidates (p 0.6): no, 86k. Seeds that find delta mostly find it early.
- A seed with a state-dependent gate like v2-local seed 1 (p 0.5): no.
- Train minus test ow0.3 at most 0.03 for every seed (p 0.8): no, seeds 14 (0.034) and 15
  (0.032), both decayed LA.
- Total wall 1.5 to 3.1 h (p 0.6): yes, 2.1 h.
