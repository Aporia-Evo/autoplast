# Package K (k-ri-lex on epyc, k-plain2m on the workstation): predictions of the executing agent (written 2026-11-19 12:47 UTC, before any build,
self-check, timing or run of K)

Commit 6c2f60a (branch claude/inspiring-pascal-2sa9s7; contains the note "Corrected 19 Nov"), source tree checked blob by blob
(3238/3238). Changed against my last build 50c2d10: src/evolve.rs, src/main.rs, src/program.rs, aggregate.py, verify/verify.py,
verify/eps_scale.py (and two probe scripts). Rebuilt on both machines; self-checks of F and of d-kalman seed 9 to 50,000 on both.
No k-ri-lex run or timing was started by the executing agent with an earlier build, so there is no k-ri-lex-faulty folder.
Neither tree has .git, so the commit is passed as --extra="... --commit 6c2f60a".

Design: RUNBOOK.md, package K. k-ri-lex = setting of D and E + --select lexicase --residual-insert --val-log --level-acc 0.651 --level-long 0.838,
1.5M, seeds 1-32, baseline j-lexicase. k-plain2m = setting of D and E + --val-log ..., 2.1M, seeds 1-32, wall-time control for J
(runs on the workstation after package L). Thresholds and predictions of the research agent are in README, "Package K".

Mine (subjective probabilities):
k-ri-lex
1. Main count (test > 0.90, T128 K8 >= 0.838, train - test <= 0.03, passes the epsilon check) 2 or more of 32: P = 0.08.
2. At least one seed above 0.90 under those conditions: P = 0.15.
3. Secondary: 3 or more above 0.85 under the conditions: P = 0.12.
4. Median test below that of j-lexicase (0.682): P = 0.45.
5. At most 5 of 32 stuck below 0.53: P = 0.85.
6. Rule 2 in 12 of 32 or more (the level of j-lexicase): P = 0.45.
7. Blocks inserted / attempts between 0.75 and 0.95 in the median seed: P = 0.60.
8. The epsilon check moves at least one seed by more than 0.02: P = 0.25.
9. No seed aborts: P = 0.85. JAX on the dump within 0.002 of Rust for every seed not flagged as diverged: P = 0.80.
10. Projection from time-k-ri-lex (x10, x2 margin) at or below 30 h: P = 0.75.
k-plain2m
11. 5 or more of 32 below 0.53 on test: P = 0.75. Any seed above 0.90 under the conditions: P = 0.03.
12. Projection from time-k-plain2m on the workstation at or below 30 h: P = 0.50.
13. The seeds below 0.53 in train accuracy at the last row at or below 1,500,100 are exactly the 11 of d-kalman: P = 0.30
    (other platform, rule 7, and d-kalman was run with an older binary).
