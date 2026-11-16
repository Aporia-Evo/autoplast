# Package J (j-lexicase, j-share): predictions of the executing agent (written 2026-11-16 09:52 UTC, while package I is running and before any
I or J result is known to the executing agent; before any J timing or run)

Commit 50c2d10 (branch claude/inspiring-pascal-2sa9s7), same build on epyc as package I (self-check of F matched; no change under src/
since 2f49b69). The tree has no .git, so the commit is passed as --extra="... --commit 50c2d10".

Design (RUNBOOK.md, package J): collision3, --recip --persist-m 3 --persist-init identity, seeds 1-32, 1,500,000 candidates, batch 128;
j-lexicase adds --select lexicase, j-share --select share, both with --val-log --level-acc 0.651 --level-long 0.838. Baseline: the 32
seeds of runs/d-kalman (rule 2 6/32, stuck below 0.53 12/32, test > 0.85 under rule 2's other conditions 1/32, median test 0.630).
Effect per arm (README, thresholds of E): rule 2 in 13/32 or more, at most 5/32 stuck, or 7/32 or more above 0.85.
Research agent for j-lexicase: at most 5 stuck P = 0.55; rule 2 13+ P = 0.40; at least one above 0.85 P = 0.50; 7+ above 0.85 P = 0.08;
a seed above 0.90 P = 0.07; for j-share each 0.05 less.

Mine (subjective probabilities):
j-lexicase
1. At most 5 of 32 stuck below 0.53: P = 0.50.
2. Rule 2 in 13 of 32 or more: P = 0.30.
3. At least one seed with test > 0.85 under rule 2's other conditions: P = 0.35. Seven or more: P = 0.04.
4. At least one seed above 0.90: P = 0.04.
5. Median test at least 0.02 above the d-kalman median (0.630): P = 0.55. Mann-Whitney against d-kalman p < 0.05: P = 0.40.
6. Any seed above 0.72 has the shape of seed 9 or a gain of the form P k / (c + kᵀP k): P = 0.25 (conditional on such a seed).
7. Projection for 32 seeds from time-j-lex (x10, x2 margin) at or below 40 h: P = 0.85.
j-share
8. At most 5 of 32 stuck: P = 0.45. Rule 2 in 13 or more: P = 0.25. At least one seed above 0.85 under the conditions: P = 0.30.
9. Projection for 32 seeds from time-j-share at or below 40 h: P = 0.60.
Both arms
10. No seed aborts: P = 0.90 each.
11. JAX on the dumped test data within 0.002 of Rust for every seed not flagged as diverged: P = 0.80 each.
