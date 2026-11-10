# v3: result (16 seeds, 1.5M candidates, task v3, local)

Time: 2026-11-04 00:54 UTC. Code: ff3b76c plus uncommitted v3 task option (archive autoplast_uncommitted.tar.gz;
git.exe blocked by the sandbox). Command:
`python local_runner.py --seeds 1-16 --budget 1500000 --tag v3 --task v3 --parallel 2 --threads 8`
Total wall 12,711 s (3.5 h), all 16 seeds exit 0. Prediction: v3_VORHERSAGE.md.
JAX check (verify.py with long suites and divergence flag): seedN/verify.txt, v3_verify_table.csv.
"train − mix" = train acc minus (0.70·T12 ow0.3 + 0.30·T64 K8), the train set's query shares.

| seed | family | len | delta 0.5 at | decomposition | R² | train | T12 ow0.3 | JAX | T64 K8 | JAX | T128 K8 | JAX | d32 T24 | d8 T6 | train − mix | wall s |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | decayed LA | 5 | no | `+0.907·S +1.000·(v kᵀ) -0.000·((S k) kᵀ)` | 1.0000 | 0.725 | 0.769 | 0.763 | 0.571 | 0.585 | 0.555 | 0.567 | 0.734 | 0.646 | 0.015 | 590 |
| 2 | delta, erase scaled by ‖(S − 0.58·k vᵀ)k‖ | 13 | 18,420 | `+1.000·S +0.935·(v kᵀ) -0.731·((S k) kᵀ)` | 0.9984 | 0.918 | 0.935 | 0.925 | 0.852 | 0.857 | 0.850 | 0.845 | 0.990 | 0.794 | 0.008 | 1696 |
| 3 | delta, write gated by σ(‖tanh v‖²·‖tanh(k⊙tanh v + S tanh² k)‖) | 15 | 258,164 | `+1.000·S +0.644·(v kᵀ) -0.625·((S k) kᵀ)` | 0.9997 | 0.914 | 0.921 | 0.915 | 0.849 | 0.854 | 0.840 | 0.848 | 0.983 | 0.783 | 0.015 | 1535 |
| 4 | decayed LA | 4 | no | `+0.907·S +0.907·(v kᵀ) +0.000·((S k) kᵀ)` | 1.0000 | 0.725 | 0.769 | 0.763 | 0.571 | 0.585 | 0.555 | 0.567 | 0.734 | 0.646 | 0.015 | 508 |
| 5 | delta, erase scaled by ‖tanh(S k)‖ | 10 | 885,748 | `+1.000·S +0.677·(v kᵀ) -0.823·((S k) kᵀ)` | 0.9990 | 0.918 | 0.937 | 0.929 | 0.845 | 0.858 | 0.835 | 0.834 | 0.990 | 0.791 | 0.009 | 700 |
| 6 | delta | 10 | 198,644 | `+1.000·S +1.949·(v kᵀ) -0.556·((S k) kᵀ)` | 0.9999 | 0.908 | 0.923 | 0.917 | 0.851 | 0.859 | 0.847 | 0.847 | 0.985 | 0.792 | 0.007 | 898 |
| 7 | delta | 15 | 20,852 | `+1.000·S +1.116·(v kᵀ) -0.550·((S k) kᵀ)` | 0.9996 | 0.911 | 0.924 | 0.917 | 0.851 | 0.854 | 0.850 | 0.847 | 0.984 | 0.789 | 0.009 | 1890 |
| 8 | decayed LA | 4 | no | `+0.907·S +1.000·(v kᵀ) -0.000·((S k) kᵀ)` | 1.0000 | 0.725 | 0.769 | 0.763 | 0.571 | 0.585 | 0.555 | 0.567 | 0.734 | 0.646 | 0.015 | 539 |
| 9 | delta | 16 | 37,620 | `+1.000·S +0.485·(v kᵀ) -0.574·((S k) kᵀ)` | 1.0000 | 0.911 | 0.922 | 0.914 | 0.851 | 0.859 | 0.854 | 0.853 | 0.985 | 0.787 | 0.010 | 2545 |
| 10 | delta | 13 | 102,260 | `+1.000·S +1.060·(v kᵀ) -0.596·((S k) kᵀ)` | 0.9998 | 0.908 | 0.920 | 0.914 | 0.853 | 0.861 | 0.854 | 0.855 | 0.984 | 0.788 | 0.008 | 4001 |
| 11 | delta | 8 | 258,548 | `+1.000·S +0.577·(v kᵀ) -0.607·((S k) kᵀ)` | 0.9999 | 0.907 | 0.919 | 0.914 | 0.854 | 0.863 | 0.853 | 0.857 | 0.983 | 0.787 | 0.008 | 2688 |
| 12 | delta, erase −0.58·‖tanh(S k)‖·tanh(S k) kᵀ | 10 | 133,876 | `+1.000·S +0.999·(v kᵀ) -0.616·((S k) kᵀ)` | 0.9995 | 0.916 | 0.937 | 0.932 | 0.850 | 0.864 | 0.843 | 0.845 | 0.990 | 0.799 | 0.005 | 1594 |
| 13 | delta | 17 | 138,612 | `+1.000·S +1.000·(v kᵀ) -0.569·((S k) kᵀ)` | 0.9993 | 0.908 | 0.918 | 0.909 | 0.844 | 0.847 | 0.826 | 0.837 | 0.974 | 0.768 | 0.012 | 2001 |
| 14 | decayed LA | 9 | no | `+0.909·S +2.855·(v kᵀ) +0.000·((S k) kᵀ)` | 0.9989 | 0.721 | 0.776 | 0.761 | 0.561 | 0.583 | 0.550 | 0.565 | 0.856 | 0.639 | 0.009 | 1000 |
| 15 | delta | 9 | 948,596 | `+1.000·S +0.419·(v kᵀ) -0.581·((S k) kᵀ)` | 1.0000 | 0.905 | 0.920 | 0.916 | 0.854 | 0.862 | 0.851 | 0.853 | 0.984 | 0.796 | 0.005 | 1836 |
| 16 | delta (a = 1.015) | 12 | 1,362,804 | `+1.015·S +2.060·(v kᵀ) -0.678·((S k) kᵀ)` | 0.9995 | 0.908 | 0.927 | 0.920 | 0.841 | 0.849 | 0.812 | 0.814 | 0.990 | 0.800 | 0.007 | 926 |

Tuned baselines on v3 (runs/v3-baselines/sweep_v3.md): DeltaNet (a = 1, e = 0.55) T12 0.923,
T64 0.852, T128 0.850, d32 0.985; Gated DeltaNet (a = 1.01) 0.930, 0.833, 0.809, 0.991.

Rates:
- Linear attention: 16/16, median 25,076 candidates.
- Delta beta=0.5 milestone: 12/16 (Wilson 95 % 50.5% to 89.8%); v2 had 6/16.
  Candidates when reached: 18,420, 20,852, 37,620, 102,260, 133,876, 138,612, 198,644, 258,164, 258,548, 885,748, 948,596, 1,362,804; median 168,628.
- The other 4 seeds end at decayed linear attention (a = 0.907), T128 K8 0.550 to 0.555.

Checks:
- Growth factor: 11 of 12 delta seeds have a = 1.000 in the decomposition, seed 16 has 1.015.
  The v3 task removed the amplification artefact of v2.
- JAX reproduction: max |JAX − Rust| 0.022 over all six shared suites; no suite diverged.
- Overfitting: train − mix 0.005 to 0.015 for all seeds.
- Against tuned baselines on v3: best delta seeds reach T12 0.937 (seeds 5 and 12; JAX
  0.929 and 0.932) against 0.923 (DeltaNet) and 0.930 (Gated DeltaNet), and T128 0.854
  (seeds 9, 10) against 0.850 (DeltaNet). Differences of +0.004 to +0.007 are within about
  two standard errors of a 512-episode suite (about 0.004). No claim of "better".
- Four delta seeds use a nonlinear, state-dependent erase or write gate (2, 3, 5, 12). Seeds 5
  and 12 scale the erase by ‖tanh(S k)‖; seed 3 gates the write by a sigmoid of a state term.
  They score at the same level as plain delta seeds; whether the nonlinearity matters needs
  a tuned family that includes it (e.g. DeltaNet with tanh(v) and a tuned erase scale).

Predictions vs outcome:
- Delta by 4 to 12 of 16 (p 0.6): yes, 12. By at least 1 (p 0.95): yes.
- Median a of delta seeds in [0.98, 1.03] (p 0.65): yes, 1.000. No a > 1.06 (p 0.7): yes, max 1.015.
- Every delta seed T128 K8 at least 0.75 (p 0.6): yes, min 0.812.
- A seed beats tuned DeltaNet on T128 by more than 0.02 (p 0.25): no, at most +0.004.
- No seed beats tuned GDN on T12 by more than 0.01 (p 0.75): yes, at most +0.007.
- Train − mix at most 0.03 for all seeds (p 0.7): yes, at most 0.015.
- Wall 4 to 9 h (p 0.65): no, 3.5 h.
