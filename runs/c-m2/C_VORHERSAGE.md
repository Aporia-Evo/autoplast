# Package C, arm C1 (c-m2): predictions (written 2026-11-10 17:54 UTC, before any timing or search run)

Commit 21e513a (branch claude/inspiring-pascal-2sa9s7), source tree checked blob by blob (1213/1213), cargo --release, baselines self-check OK.
Machine: workstation only (owner's decision). git cannot be executed in the agent sandbox, so the commit is passed as
--extra="--persist-m 2 --commit 21e513a" (main.rs takes the first --commit; local_runner.py appends --commit unknown after it).

Design (RUNBOOK.md, package C): 5a-A with --persist-m 2 and nothing else changed. collision3, task seed 1, 96 train episodes,
19 ops, fixed readout, seeds 1-16, 1,500,000 candidates, --parallel 2 --threads 8 (batch 128).
Control: committed runs/5a-A (test median 0.517, max 0.660; 7 seeds at 0.634 to 0.660, 9 seeds at 0.506 to 0.517; no seed passes rule 2;
total wall 10,065 s on epyc, median 900 s per seed).
Bars on the collision3 test: tuned DeltaNet 0.640, tuned GDN 0.644, hand-written two-state probe 0.679 (T128 K8 0.857), Kalman delta 0.935, ridge 1.000.
Decision rules (as in 5a, unchanged): rule 1 Mann-Whitney of the 16 test accuracies against 5a-A; rule 2 test > 0.651 AND T128 K8 >= 0.838 AND train - test <= 0.03.

Predictions (subjective probabilities):
1. Timing tag time-c (150k): 0.3 to 2 min per seed. P = 0.70.
2. Projection for 16 seeds at 1.5M (x10, x2 margin) below 24 h wall. P = 0.90.
3. C1 total wall time 1.5 to 6 h. P = 0.70.
4. Final rule uses the second state (a P1' line in summary.md) in 2 to 8 of 16 seeds. P = 0.50. In 0 seeds: P = 0.20.
5. Rule 1 significant (Mann-Whitney p < 0.05, either direction). P = 0.25.
6. At least one seed passes rule 2. P = 0.25.
7. At least one seed beats the probe (test > 0.679) with T128 K8 >= 0.838 and train - test <= 0.03. P = 0.12.
8. Median test of C1 within 0.03 of the 5a-A median 0.517. P = 0.55.
9. The two-mode split of 5a-A (a delta-like group near 0.64 and a decayed linear attention group near 0.51) repeats. P = 0.65.
10. JAX on the dumped test data reproduces Rust within 0.002 for every seed. P = 0.80.
