# Package G (g-tune8): predictions of the executing agent (written 2026-11-14 15:08 UTC, while package H is running and before any H result
is known to the executing agent; before any G timing or run)

Commit ad31161 (branch claude/inspiring-pascal-2sa9s7), same build on epyc as package H (self-check matched). The tree has no .git,
so the commit is passed as --extra="... --commit ad31161".

Design (RUNBOOK.md, package G): collision3, --recip --persist-m 3 --persist-init identity, seeds 1-32, 1,500,000 candidates, batch 128,
--tune-consts 8 --val-log --level-acc 0.651 --level-long 0.838. Baseline: the 32 seeds of runs/d-kalman (rule 2 in 6/32, below 0.53 in 12/32,
test > 0.85 under rule 2's other conditions in 1/32). Effect (README): rule 2 in 13/32 or more, or at most 5/32 below 0.53,
or test > 0.85 in 7/32 or more. Research agent: rule 2 in 5 to 10 of 32 with P = 0.6, 13 or more with P = 0.12; at least one seed above 0.85 with P = 0.45.

Mine (subjective probabilities):
1. Rule 2 in 5 to 10 of 32: P = 0.55. 13 or more: P = 0.12.
2. At least one seed with test > 0.85 under rule 2's other two conditions: P = 0.40. Seven or more: P = 0.04.
3. At most 5 of 32 seeds below 0.53: P = 0.15.
4. The arm shows an effect by any of the three criteria: P = 0.22.
5. At least one seed whose formula has the shape of seed 9 (address such as norm(P1ᵀ k) from a persistent register, write along it): P = 0.30.
6. Mean train - test over the 32 seeds exceeds the d-kalman mean by more than 0.01: P = 0.20.
7. Projection for 32 seeds from time-g (x10, x2 margin) at or below 30 h: P = 0.60.
8. JAX on the dumped test data within 0.002 of Rust for every seed not flagged as diverged: P = 0.80.
