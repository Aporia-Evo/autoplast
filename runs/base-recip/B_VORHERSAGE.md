# Package B (CLAUDE.md item 4): predictions (written 2026-11-10 13:28 UTC, before the run)

Commit 045ea3a, branch claude/inspiring-pascal-2sa9s7. Owner's instruction 10 Nov 2026: run all of it locally on workstation (epyc token rejected).
Tags v3 and v3-noaddnode (--no-split-edge), seeds 1-16, 1,500,000 candidates, jobs 2, threads 4, batch 128, base task, defaults otherwise
(reciprocal op on, persistent registers 1 matrix 0 vector). Both tags run at the same time on the 16 logical threads, so minutes per seed are inflated by hyperthreading.
Run via run_seeds.py (identical command line to local_runner.py, --commit 045ea3a), because git.exe is blocked in the sandbox.
Afterwards: aggregate.py per tag, verify/verify.py on every best.json, WHERE.md per tag.

Context (other branch, older code without Recip and without the structural test): v2 6/16 and v2-noaddnode 8/16 reached the delta accuracy level, Fisher p = 0.72.

Predictions (subjective probabilities):
1. v3: final rule in the delta or gated delta family in 4 to 9 of 16 seeds. P = 0.60.
2. v3-noaddnode: same family in 4 to 10 of 16 seeds. P = 0.60.
3. Two-sided Fisher test v3 vs v3-noaddnode on that count: p > 0.05. P = 0.85.
4. Linear attention seen as best rule in at least 14 of 16 seeds per tag. P = 0.75.
5. Median first appearance of the delta family, over seeds that reach it, below 600,000 candidates in v3. P = 0.55.
6. Most delta-family final rules carry a growth factor above 1 (short episodes reward it). P = 0.65.
7. verify.py reproduces the Rust test accuracy within 0.02 for every delta-family final rule. P = 0.75.
8. Total wall time 1.5 to 5 h. P = 0.70.
