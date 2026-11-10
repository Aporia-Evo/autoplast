# v3-noaddnode: where it ran

All 16 seeds ran on workstation (Ryzen 7 5700G) on 10 Nov 2026, none on epyc or modal. No seed failed, none was rerun.
The owner decided to run package B locally only, because epyc was not reachable (the JupyterHub token was rejected).

Binary: commit 045ea3a (branch claude/inspiring-pascal-2sa9s7), cargo --release, source tree checked blob by blob against the commit.
Determinism check on workstation: md5 7e0c2197a77e256e63f643baf773bd7b, linear attention at 16,756 candidates (identical to the reference values in RUNBOOK.md).

How it was launched: git.exe cannot be executed in the agent sandbox on workstation, so local_runner.py (which calls git rev-parse / git status)
could not run unchanged. A driver outside the repository issued the same command line as local_runner.py, with the commit passed explicitly:

    autoplast search --seed N --budget 1500000 --threads 4 --batch 128 --log-every 50000 --out runs/v3-noaddnode/seedN --commit 045ea3a --no-split-edge

jobs 2, threads 4. v3 and v3-noaddnode ran at the same time (4 processes x 4 threads on 16 logical threads), so the minutes below include
hyperthreading contention and are upper values for a machine running one tag. aggregate.md was written with aggregate.py from the same commit.
verify.txt: python verify/verify.py on all 16 best.json (JAX on CPU), not only the delta-family ones.

Tag name note: branch exp/v2-rediscovery-rate also has a runs/v3 (task v3 with long episodes, older code, 12/16). That is a different setting.
These two tags (base task, commit 045ea3a) were not renamed; a merge of the two branches has to resolve the name clash.

Total wall time: 79.9 min.

| seed | minutes |
|---|---|
| 1 | 5.7 |
| 2 | 6.7 |
| 3 | 11.9 |
| 4 | 6.1 |
| 5 | 4.8 |
| 6 | 6.0 |
| 7 | 4.5 |
| 8 | 4.4 |
| 9 | 8.8 |
| 10 | 31.4 |
| 11 | 19.2 |
| 12 | 10.3 |
| 13 | 6.4 |
| 14 | 16.5 |
| 15 | 4.4 |
| 16 | 11.1 |
