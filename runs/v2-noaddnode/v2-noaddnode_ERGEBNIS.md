# v2-noaddnode: result (16 seeds, 1.5M candidates, add-node off, local)

Time: 2026-11-03 20:40 UTC. Same binary and code as runs/v2 (commit ff3b76c plus uncommitted README fix;
git.exe was blocked by the sandbox at run time ("Zugriff verweigert"), so the prediction file,
written before the run, could only be committed afterwards). Command:
`python local_runner.py --seeds 1-16 --budget 1500000 --tag v2-noaddnode --parallel 2 --threads 8 --no-split-edge`
Total wall 3,263 s (0.9 h), all 16 seeds exit 0. Prediction: v2-noaddnode_VORHERSAGE.md.
JAX check for all 16 seeds: seedN/verify.txt, table v2-noaddnode_verify_table.csv.

| seed | family | len | delta 0.5 at | decomposition | R² | train | test ow0.3 | JAX ow0.3 | ow0.0 | ow0.6 | d32 T24 | JAX d32 T24 | d8 T6 | wall s |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | decayed LA | 7 | no | `+0.949·S +0.908·(v kᵀ) +0.000·((S k) kᵀ)` | 0.9997 | 0.817 | 0.789 | 0.775 | 0.865 | 0.648 | 0.878 | 0.886 | 0.637 | 386 |
| 2 | delta | 14 | 627,572 | `+1.096·S +0.330·(v kᵀ) -0.715·((S k) kᵀ)` | 1.0000 | 0.975 | 0.968 | 0.961 | 0.953 | 0.963 | 0.953 | 0.957 | 0.834 | 922 |
| 3 | decayed LA | 4 | no | `+0.958·S +1.000·(v kᵀ) -0.000·((S k) kᵀ)` | 1.0000 | 0.814 | 0.787 | 0.778 | 0.884 | 0.636 | 0.874 | 0.878 | 0.633 | 163 |
| 4 | delta, write gated by σ(‖S k‖²) | 9 | 78,324 | `+1.111·S +0.796·(v kᵀ) -0.821·((S k) kᵀ)` | 0.9995 | 0.977 | 0.971 | 0.966 | 0.962 | 0.964 | 0.991 | 0.992 | 0.826 | 346 |
| 5 | delta | 11 | 337,524 | `+1.122·S +0.843·(v kᵀ) -0.800·((S k) kᵀ)` | 0.9993 | 0.970 | 0.967 | 0.959 | 0.951 | 0.963 | 0.959 | 0.960 | 0.830 | 447 |
| 6 | delta | 12 | 109,940 | `+1.101·S +0.302·(v kᵀ) -0.799·((S k) kᵀ)` | 1.0000 | 0.971 | 0.968 | 0.962 | 0.948 | 0.963 | 0.975 | 0.979 | 0.838 | 1604 |
| 7 | delta | 8 | 500,340 | `+1.141·S +0.901·(v kᵀ) -0.949·((S k) kᵀ)` | 0.9999 | 0.966 | 0.962 | 0.954 | 0.939 | 0.957 | 0.932 | 0.937 | 0.842 | 276 |
| 8 | decayed LA | 6 | no | `+0.949·S +0.908·(v kᵀ) +0.000·((S k) kᵀ)` | 0.9997 | 0.817 | 0.789 | 0.775 | 0.865 | 0.648 | 0.878 | 0.886 | 0.637 | 246 |
| 9 | decayed LA | 4 | no | `+0.958·S +0.958·(v kᵀ) -0.000·((S k) kᵀ)` | 1.0000 | 0.814 | 0.787 | 0.778 | 0.884 | 0.636 | 0.874 | 0.878 | 0.633 | 177 |
| 10 | decayed LA | 4 | no | `+0.958·S +0.958·(v kᵀ) -0.000·((S k) kᵀ)` | 1.0000 | 0.814 | 0.787 | 0.778 | 0.884 | 0.636 | 0.874 | 0.878 | 0.633 | 162 |
| 11 | delta, S scaled by ‖v − tanh(S k)‖ (diverges) | 12 | 1,461,620 | `+1.477·S +0.994·(v kᵀ) -0.958·((S k) kᵀ)` | 0.9764 | 0.954 | 0.953 | 0.945 | 0.924 | 0.929 | 0.000 | 0.748 | 0.802 | 262 |
| 12 | decayed LA | 6 | no | `+0.958·S +1.000·(v kᵀ) +0.000·((S k) kᵀ)` | 1.0000 | 0.814 | 0.787 | 0.778 | 0.884 | 0.636 | 0.874 | 0.878 | 0.633 | 232 |
| 13 | delta | 13 | 494,068 | `+1.100·S +0.674·(v kᵀ) -0.710·((S k) kᵀ)` | 0.9999 | 0.973 | 0.968 | 0.962 | 0.956 | 0.960 | 0.962 | 0.959 | 0.836 | 485 |
| 14 | decayed LA | 7 | no | `+0.949·S +1.949·(v kᵀ) +0.000·((S k) kᵀ)` | 0.9998 | 0.812 | 0.789 | 0.776 | 0.871 | 0.646 | 0.878 | 0.889 | 0.642 | 301 |
| 15 | delta | 10 | 980,852 | `+1.098·S +0.748·(v kᵀ) -0.748·((S k) kᵀ)` | 0.9998 | 0.975 | 0.966 | 0.961 | 0.951 | 0.964 | 0.975 | 0.978 | 0.836 | 264 |
| 16 | decayed LA | 7 | no | `+0.950·S +0.903·(v kᵀ) +0.000·((S k) kᵀ)` | 0.9997 | 0.817 | 0.788 | 0.775 | 0.866 | 0.647 | 0.878 | 0.887 | 0.634 | 223 |

Rates and decision rule:
- Linear attention: 16/16 seeds, median 18,932 candidates.
- Delta beta=0.5: 8/16 seeds (Wilson 95 % 28.0% to 72.0%), against 6/16 with add-node.
  Two-sided Fisher exact p = 0.72. By the rule fixed before the run: no detectable effect
  of the add-node mutation at this sample size. The point estimate is not lower without it.
- Candidates when reached: 78,324, 109,940, 337,524, 494,068, 500,340, 627,572, 980,852, 1,461,620; median 497,204
  (v2 with add-node: 86,260). Descriptive only: without add-node the delta seeds needed
  more candidates, but runs were faster (smaller programs, 0.9 h vs 2.1 h).

Checks:
- JAX reproduction: max |JAX - Rust| 0.017 on the d16 suites. d32 T24 agrees except seed 11.
- Seed 11 is degenerate: S is multiplied by ‖v − tanh(S k)‖ each step (a = 1.477 in the
  decomposition). It scores 0.953 on d16 T12 but 0.000 accuracy and 0.000 margin on d32 T24
  in Rust. Cause (post hoc, from src/task.rs): `evaluate` scores a rule 0 as soon as any entry
  of S exceeds 1e4 or is not finite, and S grows past that on 24-write episodes. verify.py has
  no such guard, which explains its 0.748. Excluding seed 11
  as a valid rule gives 7/16, which does not change the conclusion.
- Growth factor: every delta seed has a > 1 (1.096 to 1.141, seed 11 1.477).
- Overfitting: train minus test ow0.3 is 0.001 to 0.009 for delta seeds, 0.023 to 0.029 for
  decayed LA.
- Against tuned Gated DeltaNet (ow0.3 0.968): best delta seeds 0.962 to 0.971. Seed 4 has
  0.971 in Rust and 0.966 in JAX, within noise of 0.968. No claim.
- Seed 4 has a state-dependent write gate: `S' = 1.111·S + σ(‖S k‖²)·(v − S k)⊗k`. This is
  the same occupancy signal as v2-local seed 1, now on a delta write. Input for queue items
  4 (gate analysis on realistic states) and 6 (literature check).

Predictions vs outcome:
- Linear attention 16/16 (p 0.9): yes.
- Delta in fewer than 6 seeds (p 0.5): no, 8. Delta in 0 seeds (p 0.15): no.
- Result in the non-significant band 1 to 12 (p 0.8): yes.
- Delta seeds with a > 1 (p 0.9): yes.
- Total wall 1.2 to 3 h (p 0.6): no, 0.9 h.
