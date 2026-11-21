# Package M (m-plain, m-lexicase): predictions of the executing agent (written 2026-11-21 21:32 UTC, before the build, the self-checks and any run of M)

Build: commit dce11aa (branch claude/inspiring-pascal-2sa9s7, head at the time of writing; tree checked blob by blob, 4327/4327).
src/ differs from 6c2f60a only by the testbed-2 code (src/opt.rs, main.rs, program.rs, task.rs; RUNBOOK: memory search unchanged).
Machine: epyc, a fresh directory with this tree, cargo --release. Self-checks before any run: package F (seed 2, 120,000) and
d-kalman seed 9 to 50,000 (expected row 50036,19778,...,0.50570,0.5094,12,0.3803). The tree has no .git, so the commit is passed as
--extra="... --commit dce11aa". Keepalive kernel that prints a line every 60 s.

Design: RUNBOOK.md, package M. collision3 with --recip --persist-m 3 --persist-init identity, task seeds 801 to 808 (search seed = task seed,
--task-seed-from-seed), 1,500,000 candidates, --parallel 2 --threads 8, --val-log --level-acc 0.651 --level-long 0.838; m-lexicase adds
--select lexicase. The two arms run one after the other on epyc in one script. Then per arm: dump of each task seed's test split, JAX check,
epsilon check (verify.py --x64 --norm-eps 1e-9, eps_scale.py for seeds moving by more than 0.02), long-episode probe in nine draws
(own task seed and 1 to 8, evalmany --split long, largest of the nine).
Research agent: m-plain 0/8 above 0.90 (with the other conditions) P = 0.85; m-lexicase 0/8 P = 0.8. The frozen memetic search counted 5 of these 8.

Mine (subjective probabilities):
1. m-plain: 0/8 above 0.90 under the conditions: P = 0.88.
2. m-lexicase: 0/8 above 0.90 under the conditions: P = 0.85.
3. Any seed of either arm with test >= 0.99: P = 0.03.
4. m-plain: 2 or more of 8 below 0.53 on test: P = 0.60.
5. m-lexicase: 0 of 8 below 0.53: P = 0.75.
6. Median test of m-lexicase above that of m-plain: P = 0.75.
7. Total wall of both arms between 6 and 14 h (K: about 60 minutes per seed): P = 0.70.
8. JAX on the dump within 0.002 of Rust for every seed not flagged as diverged: P = 0.80.
9. The epsilon check moves at least one seed (both arms together) by more than 0.02: P = 0.30.
10. The best-test seed of each arm stays below 100 in all nine long-probe draws: P = 0.50.
11. Both self-checks reproduce the Linux rows on epyc: P = 0.95.
