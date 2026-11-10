# c-m2: where it ran

All 16 seeds ran on workstation (Ryzen 7 5700G), 10 Nov 2026, 17:59 to 22:33 UTC. None on epyc or modal. No seed failed, none was rerun.

Binary: commit 21e513a, cargo --release, source tree checked blob by blob against the commit (1213/1213). Baselines self-check OK.
Command (RUNBOOK.md, package C, step 2), with the commit passed through --extra because git cannot be executed in the agent sandbox:

    python local_runner.py --seeds 1-16 --budget 1500000 --tag c-m2 --parallel 2 --threads 8 --regime collision3 --extra="--persist-m 2 --commit 21e513a"

local_runner.py appends --commit unknown after the extra flags; main.rs reads the first --commit, so summaries say 21e513a.
The sandbox Python runs in safe-path mode and does not put the script folder on sys.path, so PYTHONPATH was set to the repository
root for `import aggregate`. No file was changed.

Timing (tag time-c, not committed): 150,000 candidates, seed 1 115 s, seed 2 195 s.
Step 4: autoplast dump --regime collision3 --split test (264 KB), verify.py --task-json on all 16 best.json -> verify_dump.txt;
the dump was deleted afterwards as the runbook asks.

Total wall 16431 s.

| seed | minutes |
|---|---|
| 1 | 27.0 |
| 2 | 73.4 |
| 3 | 18.4 |
| 4 | 24.2 |
| 5 | 26.8 |
| 6 | 83.4 |
| 7 | 15.7 |
| 8 | 20.2 |
| 9 | 62.3 |
| 10 | 29.8 |
| 11 | 12.4 |
| 12 | 28.1 |
| 13 | 32.4 |
| 14 | 48.4 |
| 15 | 15.3 |
| 16 | 27.0 |
