# Package D (d-kalman): predictions of the executing agent (written 2026-11-12 09:29 UTC, before any timing or search run)

Commit e979a8e (branch claude/inspiring-pascal-2sa9s7), source tree checked blob by blob against the commit (1318/1318).
Machine: epyc (owner's decision for package D): 16 cores, 1 thread per core, 62 GB RAM, load 0.00 at the check.
git can run there, but the repository is uploaded as the commit tarball without .git, so the commit is passed as
--extra="--persist-m 3 --persist-init identity --commit e979a8e" (main.rs reads the first --commit).

Design (RUNBOOK.md, package D): collision3, task seed 1, 96 + 48 train episodes, fixed readout, seeds 1-16, 1,500,000 candidates,
batch 128, --recip --persist-m 3 --persist-init identity. Controls runs/5a-A and runs/c-m2, not rerun.
Bars: tuned DeltaNet 0.640, c-m2 seed 2 0.695, hand-written Kalman delta 0.933 (T128 K8 0.950), ridge 1.000.
Main count, fixed before the run by the research agent: seeds with test > 0.85 AND T128 K8 >= 0.838 AND train - test <= 0.03.

The research agent's predictions are in README ("Package D"): main count 0 with P = 0.85; at least one seed above 0.695 with P = 0.6.
Mine, independent of the outcome (subjective probabilities):

1. time-d (150k) on epyc: 2 to 8 min per seed. P = 0.60.
2. Projection for 16 seeds at 1.5M (x10, x2 margin) below 24 h wall. P = 0.75.
3. Main count 0. P = 0.85.
4. At least one seed above 0.695 under rule 2's other two conditions. P = 0.45.
5. At least one seed passes rule 2. P = 0.55.
6. Rule 1 significant (p < 0.05) against c-m2: P = 0.15. Against 5a-A: P = 0.25.
7. The S' formula contains a reciprocal (1/() in at least 4 of 16 seeds. P = 0.50.
8. S' reads P2 in at least 3 of 16 seeds. P = 0.40.
9. At least one seed scores 0.000 on T128 K8 (overflow guard, from the identity start or the reciprocal). P = 0.40.
10. JAX on the dumped test data reproduces Rust within 0.002 for every seed. P = 0.75.
11. The two-mode split of 5a-A and c-m2 (a group near 0.51 and a group at 0.63 or above) repeats. P = 0.55.
