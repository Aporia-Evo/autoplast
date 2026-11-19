# Package L (l-downsample, base task, workstation): predictions of the executing agent (written 2026-11-19 12:47 UTC, before any build,
self-check or run of L)

Commit 6c2f60a (branch claude/inspiring-pascal-2sa9s7; contains the note "Corrected 19 Nov"), source tree checked blob by blob
(3238/3238). Changed against my last build 50c2d10: src/evolve.rs, src/main.rs, src/program.rs, aggregate.py, verify/verify.py,
verify/eps_scale.py (and two probe scripts). Rebuilt on both machines; self-checks of F and of d-kalman seed 9 to 50,000 on both.
No k-ri-lex run or timing was started by the executing agent with an earlier build, so there is no k-ri-lex-faulty folder.
Neither tree has .git, so the commit is passed as --extra="... --commit 6c2f60a".

Design: RUNBOOK.md, package L. Base task, seeds 1-32, 1.5M, --select downsample --val-log, baseline h-base, h-share, h-lexicase (epyc).
Fixed in README: down-sampling gives an effect at 20/32 or more on the accuracy level of delta beta = 0.5 (h-base 12/32); lexicase does
more than down-sampling if l-downsample reaches 27/32 or fewer (h-lexicase 32/32). Research agent: 20 or more P = 0.6, 27 or fewer P = 0.5.

Mine (subjective probabilities):
1. Accuracy level in 20 of 32 or more: P = 0.55.
2. Accuracy level in 27 of 32 or fewer: P = 0.55.
3. Structural count (delta / gated delta) at least 12 of 32 (h-base): P = 0.60.
4. At most 3 of 32 end at linear attention level (train < 0.84): P = 0.45.
5. Mean minutes per seed on the workstation between 5 and 15: P = 0.60; total wall 2 to 5 h: P = 0.65.
6. verify.py within 0.02 of Rust on test ow0.3 for every seed: P = 0.80.
7. Self-check of F gives the Linux row 120052,22831,...,0.82164,0.8142,4 on the workstation too: P = 0.70.
