# v3: where it ran

All 16 seeds ran on workstation (Ryzen 7 5700G) on 10 Nov 2026, none on epyc or modal. No seed failed, none was rerun.
The owner decided to run package B locally only, because epyc was not reachable (the JupyterHub token was rejected).

Binary: commit 045ea3a (branch claude/inspiring-pascal-2sa9s7), cargo --release, source tree checked blob by blob against the commit.
Determinism check on workstation: md5 7e0c2197a77e256e63f643baf773bd7b, linear attention at 16,756 candidates (identical to the reference values in RUNBOOK.md).

How it was launched: git.exe cannot be executed in the agent sandbox on workstation, so local_runner.py (which calls git rev-parse / git status)
could not run unchanged. A driver outside the repository issued the same command line as local_runner.py, with the commit passed explicitly:

    autoplast search --seed N --budget 1500000 --threads 4 --batch 128 --log-every 50000 --out runs/v3/seedN --commit 045ea3a

jobs 2, threads 4. v3 and v3-noaddnode ran at the same time (4 processes x 4 threads on 16 logical threads), so the minutes below include
hyperthreading contention and are upper values for a machine running one tag. aggregate.md was written with aggregate.py from the same commit.
verify.txt: python verify/verify.py on all 16 best.json (JAX on CPU), not only the delta-family ones.

Tag name note: branch exp/v2-rediscovery-rate also has a runs/v3 (task v3 with long episodes, older code, 12/16). That is a different setting.
These two tags (base task, commit 045ea3a) were not renamed; a merge of the two branches has to resolve the name clash.

Total wall time: 108.0 min.

| seed | minutes |
|---|---|
| 1 | 6.5 |
| 2 | 4.3 |
| 3 | 21.4 |
| 4 | 25.0 |
| 5 | 7.2 |
| 6 | 19.0 |
| 7 | 6.5 |
| 8 | 7.4 |
| 9 | 23.2 |
| 10 | 4.2 |
| 11 | 6.4 |
| 12 | 13.1 |
| 13 | 8.8 |
| 14 | 6.8 |
| 15 | 3.6 |
| 16 | 27.0 |

## Package A timing (workstation only; time-* tags are not committed)

150,000 candidates, jobs 2, threads 4: time-base 0.33 and 0.58 min per seed, time-r8 (--regime rewrite8 --train-episodes 192, task seed = seed)
5.67 and 9.47 min per seed, ratio about 17. Peak RSS at most 42 MB. Runbook projection (x10, x2 margin) gave 7 to 12 min per base seed at 1.5M;
the real base seeds above took 3.6 to 31 min, so for rewrite8 at 1.5M 4 to 8 h per seed is the more realistic range.
Predictions for packages A and B were written before the runs (B_VORHERSAGE.md in this folder).
