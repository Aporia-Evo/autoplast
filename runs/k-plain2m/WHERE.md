# k-plain2m: where it ran

All 32 seeds ran on epyc (16 cores, 1 thread per core), started 2026-11-20T15:25:21Z, 62119 s, under nice -n 10, with a keepalive kernel that
prints a line every 60 s. None on workstation or modal. No seed failed, none was rerun.

RUNBOOK.md puts this arm on the workstation after package L. The workstation timing (tag time-k-plain2m, not committed; 122 s and 260 s per
seed at 150,000) gave 32.4 h with the runbook margin (23.8 h from the mean), above 30 h, so the executing agent asked; the owner decided to run it
on epyc after k-ri-lex. epyc timing (same tag, not committed): 109 s and 194 s; projection 194 s x 14 x 16 pairs = 12.1 h, x2 = 24.1 h.

Binary: commit 6c2f60a, the same build in ~/autoplast-k as k-ri-lex (self-checks in runs/k-ri-lex/WHERE.md). src/ changed later on the branch
(research agent's growth-loop work); this arm was not rebuilt. Command (RUNBOOK.md, package K), commit passed through --extra:

    python local_runner.py --seeds 1-32 --budget 2100000 --tag k-plain2m --parallel 2 --threads 8 --regime collision3 --recip --extra="--persist-m 3 --persist-init identity --val-log --level-acc 0.651 --level-long 0.838 --commit 6c2f60a"

Dump made with the epyc binary; verify.py --task-json, the epsilon check and eps_scale.py ran on workstation (JAX on CPU) -> verify_dump.txt,
verify_eps_x64.txt, eps_scale.txt; the dump was deleted on both machines. Runner log: runner_log_epyc.txt.

Total wall 62119 s.

| seed | minutes |
|---|---|
| 1 | 85.9 |
| 2 | 79.2 |
| 3 | 137.5 |
| 4 | 50.2 |
| 5 | 31.2 |
| 6 | 170.8 |
| 7 | 39.3 |
| 8 | 22.6 |
| 9 | 56.7 |
| 10 | 151.3 |
| 11 | 31.1 |
| 12 | 49.5 |
| 13 | 56.8 |
| 14 | 46.8 |
| 15 | 46.8 |
| 16 | 35.7 |
| 17 | 49.0 |
| 18 | 27.0 |
| 19 | 27.4 |
| 20 | 80.8 |
| 21 | 37.3 |
| 22 | 41.8 |
| 23 | 40.0 |
| 24 | 46.7 |
| 25 | 142.1 |
| 26 | 21.2 |
| 27 | 79.7 |
| 28 | 37.6 |
| 29 | 58.4 |
| 30 | 93.4 |
| 31 | 104.0 |
| 32 | 67.8 |
