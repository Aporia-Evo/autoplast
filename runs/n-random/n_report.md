# n-random (package N, testbed 2): results as measured

--task opt --opt-ops --persist-v 2 --algo random, task seeds 901 to 916 (search seed = task seed, --task-seed-from-seed), 300,000 candidates, --parallel 2 --threads 8 (batch 128),
commit dce11aa, all seeds on epyc, started 2026-11-22T04:15:36Z, wall 1027 s (0.29 h). Summary line: `search: random programs, no selection  tune-consts: 0  select: fitness  residual-insert: off`.
No seed failed or was rerun. Facts only; the interpretation (including the Adam-level count) is left to the research agent.
Objective: mean log10(f_T / f_0), lower is better. "suite 1" is the summary line `test opt train-distribution`.

## Overview

| tag | median suite 1 | best suite 1 (seed) | seeds with any diverged fraction > 0 (train or any suite) | seeds with suite 1 <= -3.023 | mean train - suite 1 | mean real evals | mean episode evals | mean minutes |
|---|---|---|---|---|---|---|---|---|
| n-random | -2.1148 | -2.1207 (901) | 0/16 | 0/16 | -0.0167 | 164,769 | 21,090,448 | 2.1 |

Structural classes (verify/opt_structure.py on the train dump of each task seed, simplest member with R² >= 0.95, else unclassified):
SGD 14 (901, 902, 903, 904, 905, 906, 907, 909, 910, 911, 913, 914, 915, 916); unclassified 2 (908, 912)

Ladder for reference (README, "Testbed 2: implementation"):

| rule (README ladder, task seed 1) | train | suite 1 |
|---|---|---|
| SGD | -2.013 | -2.072 |
| momentum | -2.614 | -2.638 |
| RMSProp | -2.717 | -2.679 |
| Adam | -3.130 | -3.073 |

The suite-1 objective repeats to four decimals across task seeds (for example -2.1529 in several seeds); the held-out suites appear not to
depend on the task seed, while the train task does.

## Per seed

| task seed | train | suite 1 | train - suite 1 | div. train | div. train-distribution | div. kappa1000 | div. d32 | div. d8 | div. sigma0.3 | div. T200 | div. scale10/0.1 | real evals | episode evals (x128) | instr | min | structural class | R² SGD / momentum / RMSProp / Adam |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 901 | -2.1768 | -2.1207 | -0.0561 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 164,824 | 21,097,472 | 3 | 2.1 | SGD | 0.992 / 0.992 / 0.620 / 0.620 |
| 902 | -2.1889 | -2.1148 | -0.0741 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 165,273 | 21,154,944 | 2 | 2.1 | SGD | 0.998 / 0.998 / 0.651 / 0.651 |
| 903 | -2.1413 | -2.1207 | -0.0206 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 164,712 | 21,083,136 | 3 | 2.1 | SGD | 0.986 / 0.986 / 0.674 / 0.674 |
| 904 | -2.1194 | -2.1148 | -0.0046 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 165,030 | 21,123,840 | 2 | 2.1 | SGD | 0.994 / 0.994 / 0.571 / 0.571 |
| 905 | -2.1305 | -2.1148 | -0.0157 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 164,385 | 21,041,280 | 2 | 2.1 | SGD | 0.994 / 0.994 / 0.624 / 0.624 |
| 906 | -2.1699 | -2.1148 | -0.0551 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 164,517 | 21,058,176 | 2 | 2.1 | SGD | 0.996 / 0.996 / 0.624 / 0.624 |
| 907 | -2.1621 | -2.1148 | -0.0473 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 164,943 | 21,112,704 | 2 | 2.1 | SGD | 0.996 / 0.996 / 0.649 / 0.649 |
| 908 | -2.1013 | -2.1148 | +0.0135 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 164,630 | 21,072,640 | 2 | 2.1 | unclassified | 0.945 / 0.945 / 0.450 / 0.450 |
| 909 | -2.1611 | -2.1207 | -0.0404 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 164,509 | 21,057,152 | 4 | 2.1 | SGD | 0.996 / 0.996 / 0.690 / 0.690 |
| 910 | -2.0675 | -2.1148 | +0.0473 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 164,948 | 21,113,344 | 2 | 2.1 | SGD | 0.989 / 0.989 / 0.548 / 0.548 |
| 911 | -2.1820 | -2.1148 | -0.0672 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 165,049 | 21,126,272 | 2 | 2.1 | SGD | 0.985 / 0.985 / 0.522 / 0.522 |
| 912 | -2.1143 | -2.1207 | +0.0064 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 164,828 | 21,097,984 | 3 | 2.1 | unclassified | 0.936 / 0.936 / 0.566 / 0.566 |
| 913 | -2.0556 | -2.1148 | +0.0592 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 164,442 | 21,048,576 | 2 | 2.1 | SGD | 0.996 / 0.996 / 0.613 / 0.613 |
| 914 | -2.0839 | -2.1148 | +0.0309 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 164,444 | 21,048,832 | 2 | 2.1 | SGD | 0.998 / 0.998 / 0.620 / 0.620 |
| 915 | -2.1237 | -2.1148 | -0.0089 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 164,805 | 21,095,040 | 2 | 2.1 | SGD | 0.996 / 0.996 / 0.636 / 0.636 |
| 916 | -2.1552 | -2.1207 | -0.0345 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 164,967 | 21,115,776 | 3 | 2.1 | SGD | 0.981 / 0.981 / 0.656 / 0.656 |

Objective on each of the seven suites:

| task seed | train-distribution | kappa1000 | d32 | d8 | sigma0.3 | T200 | scale10/0.1 |
|---|---|---|---|---|---|---|---|
| 901 | -2.1207 | -1.4397 | -1.6095 | -2.2075 | -0.9809 | -2.8056 | -0.2027 |
| 902 | -2.1148 | -1.4388 | -1.5313 | -2.2068 | -0.9748 | -2.7978 | -0.0893 |
| 903 | -2.1207 | -1.4397 | -1.6095 | -2.2075 | -0.9809 | -2.8056 | -0.2027 |
| 904 | -2.1148 | -1.4388 | -1.5313 | -2.2068 | -0.9748 | -2.7978 | -0.0893 |
| 905 | -2.1148 | -1.4388 | -1.5313 | -2.2068 | -0.9748 | -2.7978 | -0.0893 |
| 906 | -2.1148 | -1.4388 | -1.5313 | -2.2068 | -0.9748 | -2.7978 | -0.0893 |
| 907 | -2.1148 | -1.4388 | -1.5313 | -2.2068 | -0.9748 | -2.7978 | -0.0893 |
| 908 | -2.1148 | -1.4388 | -1.5313 | -2.2068 | -0.9748 | -2.7978 | -0.0893 |
| 909 | -2.1207 | -1.4397 | -1.6095 | -2.2075 | -0.9809 | -2.8056 | -0.2027 |
| 910 | -2.1148 | -1.4388 | -1.5313 | -2.2068 | -0.9748 | -2.7978 | -0.0893 |
| 911 | -2.1148 | -1.4388 | -1.5313 | -2.2068 | -0.9748 | -2.7978 | -0.0893 |
| 912 | -2.1207 | -1.4397 | -1.6095 | -2.2075 | -0.9809 | -2.8056 | -0.2027 |
| 913 | -2.1148 | -1.4388 | -1.5313 | -2.2068 | -0.9748 | -2.7978 | -0.0893 |
| 914 | -2.1148 | -1.4388 | -1.5313 | -2.2068 | -0.9748 | -2.7978 | -0.0893 |
| 915 | -2.1148 | -1.4388 | -1.5313 | -2.2068 | -0.9748 | -2.7978 | -0.0893 |
| 916 | -2.1207 | -1.4397 | -1.6095 | -2.2075 | -0.9809 | -2.8056 | -0.2027 |

## Best rule of the arm (lowest suite 1: task seed 901)

    w' = (w - tanh(tanh(g)))
    u3' = tanh(g)

runs/n-random/seed901/best.json: SGD   SGD R²=0.992 (η=0.93, β=0, β₂=0)  momentum R²=0.992 (η=0.93, β=0, β₂=0)  RMSProp R²=0.620 (η=0.0071, β=0, β₂=0.999)  Adam R²=0.620 (η=0.0071, β=0, β₂=0.999)

Files: per seed summary.md, log.csv, best.json; aggregate.md as written by the runner (its columns are those of the memory task and stay empty
for testbed 2); opt_structure.txt (output of the structural test per seed); runner_log_epyc.txt.

## Predictions (same file as n-plain) against outcome (runs/n-plain/N_VORHERSAGE.md, committed in be1b18b before any N run)

1. n-plain at least one of 16 at the Adam level (P = 0.10): no seed has suite 1 at or below -3.023 (best -2.6468, seed 905).
2. n-random at least one at the Adam level (P = 0.02): no (best -2.1207).
3. n-plain median suite 1 at or below SGD's -2.072 (P = 0.45): yes (-2.1529).
4. n-plain structural class SGD for 8 or more of 16 (P = 0.50): yes (8).
5. n-random median suite 1 worse (higher) than n-plain (P = 0.90): yes (-2.1148 vs -2.1529).
6. n-plain at least one seed with a diverged fraction above 0 (P = 0.70): no (0).
7. timing projection at or below 30 h for each arm (P = 0.70): yes (2.3 h and 0.6 h).
8. mean train - suite-1 gap of n-plain at or below 0.1 in absolute value (P = 0.75): yes (-0.0198).
