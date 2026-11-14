# Package H (h-base, h-share, h-lexicase): predictions of the executing agent (written 2026-11-14 15:01 UTC, before any build, timing or run)

Commit ad31161 (branch claude/inspiring-pascal-2sa9s7), source tree checked blob by blob (1826/1826). Changed against 6df6477:
src/evolve.rs, src/main.rs, src/task.rs, so the code is rebuilt. Machine: epyc for all three arms. The tree is uploaded without
.git, so the commit is passed as --extra="... --commit ad31161".

Design (RUNBOOK.md, package H): base task, seeds 1-32, 1,500,000 candidates, batch 128. h-base --val-log; h-share --select share --val-log;
h-lexicase --select lexicase --val-log. Effect: one-sided Fisher against h-base, p < 0.05 on the accuracy-level count or the structural count.
Research agent (README): h-share effect with P = 0.4, h-lexicase with P = 0.15; h-base 11 to 17 of 32 on the first count with P = 0.7.

Mine (subjective probabilities):
1. h-base: 11 to 17 of 32 at the delta beta=0.5 accuracy level, P = 0.70; 8 to 14 of 32 in the delta family by the structural test, P = 0.65.
2. h-share shows an effect by the rule above (either count): P = 0.30.
3. h-lexicase shows an effect by the rule above (either count): P = 0.12.
4. h-lexicase has more seeds ending at linear attention level (train < 0.84) than h-base: P = 0.50.
5. h-share: mean real evaluations per seed above 1.5 times h-base, P = 0.70; mean minutes per seed at least 3 times h-base, P = 0.55.
6. h-share has more delta rules with a within 0.02 of 1 than h-base: P = 0.30.
7. Arm mean of the last-row pop_mean_acc is lower in h-share than in h-base: P = 0.70.
8. Projection for all three arms from the timing (x10, x2 margin) at or below 30 h of wall time: P = 0.80.
9. verify.py within 0.02 of Rust on test ow0.3 for every seed of all three arms: P = 0.80.
