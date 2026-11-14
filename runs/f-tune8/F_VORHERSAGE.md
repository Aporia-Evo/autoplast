# Package F (f-tune8, f-tune3, f-random): predictions of the executing agent (written 2026-11-14 10:08 UTC, before any build, timing or run)

Commit 6df6477 (branch claude/inspiring-pascal-2sa9s7), source tree checked blob by blob (1522/1522). Changes under src/ since
e979a8e: src/evolve.rs, src/main.rs, so the code is rebuilt. Machine: epyc (RUNBOOK allows any one machine). The tree is uploaded
without .git, so the commit is passed as --extra="... --commit 6df6477".

Design (RUNBOOK.md, package F): base task (v2 setting), default 19-op alphabet, one state, add-node on, seeds 1-16,
1,500,000 candidates, batch 128. Arms f-tune8 (--tune-consts 8 --val-log), f-tune3 (--tune-consts 3 --val-log),
f-random (--algo random --val-log). Baseline runs/v2 + runs/v2-noaddnode pooled: 14/32 at the accuracy level of delta beta=0.5,
11/32 in the delta family by the structural test. Detection threshold fixed in README: 12/16 (primary) or 11/16 (structural).

Research agent (README): f-tune8 at 5 to 9 of 16 on the primary count with P = 0.6, 12 or more with P = 0.1; f-random 0 of 16 with P = 0.9.

Mine (subjective probabilities):
1. f-tune8 primary count: 4 or fewer P = 0.25; 5 to 9 P = 0.55; 10 or 11 P = 0.10; 12 or more P = 0.10.
2. f-tune3 primary count 5 to 9 of 16: P = 0.55; 12 or more: P = 0.08.
3. f-random primary count 0 of 16: P = 0.90. All 16 f-random seeds end below train 0.84: P = 0.85.
4. Neither tuning arm reaches the detection threshold on either count: P = 0.80.
5. Among seeds that reach the delta beta=0.5 level, the median candidate count in f-tune8 is below the pooled baseline median: P = 0.55.
6. Mean train - test ow0.3 of f-tune8 exceeds the pooled baseline mean by more than 0.01: P = 0.25.
7. Every final rule at the delta level in the two tuning arms has a growth factor a > 1: P = 0.75.
8. Timing time-f (150k, --tune-consts 8) on epyc: 0.5 to 3 min per seed: P = 0.60. All three arms together below 15 h of wall time: P = 0.70.
9. verify.py (fresh embeddings, no dump on the base task) within 0.02 of Rust on test ow0.3 for every seed of all three arms: P = 0.80.
