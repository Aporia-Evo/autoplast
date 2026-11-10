# v3-baselines: result

Time: 2026-11-03 21:10 UTC. Code: ff3b76c plus uncommitted v3 task option. Raw outputs: baselines_v2.md,
baselines_v3.md, sweep_v2.md, sweep_v3.md, found_rules_long_suites.csv. Sweeps took 144 s (v3)
and 42 s (v2).

Tuned baselines (sweep, tuned on the respective train set):

| train task | family | a | e | train | T12 ow0.3 | T12 ow0.0 | T12 ow0.6 | d32 T24 | d8 T6 | T64 K8 | T128 K8 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| v2 | DeltaNet | 1 | 0.50 | 0.932 | 0.924 | 0.900 | 0.941 | 0.987 | 0.793 | 0.840 | 0.828 |
| v2 | Gated DeltaNet | 1.1 | 0.65 | 0.970 | 0.968 | 0.957 | 0.964 | 0.957 | 0.841 | 0.064 | 0.020 |
| v3 | DeltaNet | 1 | 0.55 | 0.904 | 0.923 | 0.892 | 0.946 | 0.985 | 0.794 | 0.852 | 0.850 |
| v3 | Gated DeltaNet | 1.01 | 0.55 | 0.905 | 0.930 | 0.905 | 0.949 | 0.991 | 0.802 | 0.833 | 0.809 |

The untied family gives the same accuracies as Gated DeltaNet on both tasks (the write gain
only rescales S, see v2 reading).

Found rules from runs/v2 and runs/v2-noaddnode on the new long suites:
- 14 delta rules (all a > 1): T64 K8 0.000 to 0.448, T128 K8 0.000 to 0.081.
- 18 decayed-linear-attention rules: T64 K8 0.398 to 0.550, T128 K8 0.378 to 0.515.

Reading: the v2 delta rules and tuned v2 Gated DeltaNet only work on short episodes; their
amplification a > 1 destroys recall at T = 64 and 128. On v3 the tuned optimum moves from
a = 1.1 to a = 1.01, and plain DeltaNet (a = 1) is best on T128 (0.850).

Predictions vs outcome:
- v3 optimum at a <= 1.0 (p 0.65): no, a = 1.01 (one grid step above). The criterion fixed
  in README is missed narrowly; a = 1.01 still costs 0.04 on T128 against a = 1.
- v2 optimum stays a > 1 with refined grid (p 0.8): yes, 1.1.
- Delta beta=0.5 above 0.8 on T128 (p 0.6): yes, 0.828.
- At least 12 of 14 found delta rules below 0.5 on T128 (p 0.75): yes, 14 of 14.
- Linear attention below 0.3 on T64 K8 (p 0.7): yes, 0.104.
- Tuned GDN on v3 at least 0.95 on T12 ow0.3 (p 0.6): no, 0.930.
