# h-share seed 16, rerun by the research agent with the cache fix (15 Nov 2026)

The run of package H aborted at about 1,450,000 candidates (cache fault, README "Package H:
result and reading"). This is the same command with the fixed code (commit 2f49b69), run on the
review machine (Linux, 4 threads, batch 128), not on epyc:

    autoplast search --seed 16 --budget 1500000 --threads 4 --batch 128 --log-every 50000 --select share --val-log

All 30 log rows of the aborted epyc run are identical to this run in every column except
`real_evals` and `seconds`. Result: gated delta rule (a = 1.118, erase 0.729, R² = 1.0000), accuracy
level of delta β = 0.5 reached at 39,284 candidates, train 0.971, test ow0.3 0.968, T128 K8 0.000.

The rerun on epyc in package I is the one that goes into `runs/h-share/seed16/`; this folder is the
research agent's check and is not counted by `aggregate.py`.
