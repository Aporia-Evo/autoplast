# Package I (i-base4m, rerun of h-share seed 16): predictions of the executing agent (written 2026-11-16 09:38 UTC, before any build or run)

Commit 50c2d10 (branch claude/inspiring-pascal-2sa9s7), source tree checked blob by blob (2618/2618). Changed under src/ against my
last build ad31161: src/evolve.rs (the cache fix); no change under src/ between 2f49b69 and 50c2d10. Rebuilt on epyc, self-check of F
repeated. The tree has no .git, so the commit is passed as --extra="... --commit 50c2d10".

Design (RUNBOOK.md, package I): base task, plain search, seeds 1-32, 4,000,000 candidates, --val-log, same machine as H (epyc).
Count fixed in README: seeds at the accuracy level of delta beta=0.5 at 4M. Below 24/32: the selection arms beat the plain search at
equal wall time; at 28/32 or more the gain of the arms is a saving of candidates. Research agent: 13 to 20 of 32 with P = 0.65; 28 or more with P = 0.05.
Rerun of h-share seed 16 (1.5M, --select share --val-log) with the fixed code; the aborted run's log.csv and stderr.txt go to
runs/h-share/seed16_aborted/ first.

Mine (subjective probabilities):
1. i-base4m at 4M: 12 or fewer of 32 P = 0.10; 13 to 20 P = 0.65; 21 to 23 P = 0.12; 24 or more P = 0.13 (28 or more P = 0.03).
2. i-base4m at 1.5M (Milestones line at or below 1,500,000) gives exactly the 12 seeds of h-base, the same seed numbers, because the
   trajectory does not depend on the budget and the cache fix does not change scores: P = 0.90.
3. The rerun of h-share seed 16 reproduces every row of the aborted log in all columns except real_evals and seconds: P = 0.90.
4. h-share seed 16 ends at the accuracy level (the aborted run was at train 0.971 at 1,450,100): P = 0.90; in the delta family by the
   structural test: P = 0.60.
5. Mean minutes per i-base4m seed between 10 and 25: P = 0.60. Total wall of i-base4m at or below 10 h: P = 0.75.
6. Mean train - test of i-base4m within 0.005 of h-base (+0.019): P = 0.60.
