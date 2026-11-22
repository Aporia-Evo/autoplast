# n-plain (package N, testbed 2): results as measured

--task opt --opt-ops --persist-v 2, task seeds 901 to 916 (search seed = task seed, --task-seed-from-seed), 300,000 candidates, --parallel 2 --threads 8 (batch 128),
commit dce11aa, all seeds on epyc, started 2026-11-22T02:43:42Z, wall 5514 s (1.53 h). Summary line: `search: regularized evolution  tune-consts: 0  select: fitness  residual-insert: off`.
No seed failed or was rerun. Facts only; the interpretation (including the Adam-level count) is left to the research agent.
Objective: mean log10(f_T / f_0), lower is better. "suite 1" is the summary line `test opt train-distribution`.

## Overview

| tag | median suite 1 | best suite 1 (seed) | seeds with any diverged fraction > 0 (train or any suite) | seeds with suite 1 <= -3.023 | mean train - suite 1 | mean real evals | mean episode evals | mean minutes |
|---|---|---|---|---|---|---|---|---|
| n-plain | -2.1529 | -2.6468 (905) | 0/16 | 0/16 | -0.0198 | 205,528 | 26,307,640 | 11.5 |

Structural classes (verify/opt_structure.py on the train dump of each task seed, simplest member with R² >= 0.95, else unclassified):
unclassified 7 (901, 902, 903, 907, 908, 914, 916); SGD 8 (904, 906, 909, 910, 911, 912, 913, 915); momentum 1 (905)

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
| 901 | -2.2278 | -2.1529 | -0.0749 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 227,859 | 29,165,952 | 24 | 13.6 | unclassified | 0.929 / 0.929 / 0.751 / 0.751 |
| 902 | -2.3508 | -2.2879 | -0.0629 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 218,083 | 27,914,624 | 24 | 12.1 | unclassified | 0.912 / 0.912 / 0.740 / 0.740 |
| 903 | -2.1709 | -2.1529 | -0.0180 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 216,524 | 27,715,072 | 24 | 12.6 | unclassified | 0.942 / 0.942 / 0.767 / 0.767 |
| 904 | -2.1677 | -2.1521 | -0.0156 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 185,873 | 23,791,744 | 24 | 9.6 | SGD | 0.956 / 0.956 / 0.754 / 0.754 |
| 905 | -2.6318 | -2.6468 | +0.0150 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 222,355 | 28,461,440 | 24 | 11.0 | momentum | 0.700 / 0.963 / 0.598 / 0.795 |
| 906 | -2.2067 | -2.1529 | -0.0538 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 218,545 | 27,973,760 | 24 | 12.8 | SGD | 0.961 / 0.961 / 0.772 / 0.772 |
| 907 | -2.2065 | -2.1529 | -0.0536 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 222,124 | 28,431,872 | 24 | 13.2 | unclassified | 0.948 / 0.948 / 0.766 / 0.766 |
| 908 | -2.1574 | -2.1529 | -0.0045 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 219,594 | 28,108,032 | 24 | 13.0 | unclassified | 0.925 / 0.925 / 0.722 / 0.722 |
| 909 | -2.1858 | -2.1529 | -0.0329 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 221,327 | 28,329,856 | 24 | 13.0 | SGD | 0.954 / 0.954 / 0.770 / 0.770 |
| 910 | -2.1358 | -2.1529 | +0.0171 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 221,974 | 28,412,672 | 24 | 13.2 | SGD | 0.960 / 0.960 / 0.759 / 0.759 |
| 911 | -2.2176 | -2.1529 | -0.0647 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 224,291 | 28,709,248 | 24 | 13.5 | SGD | 0.960 / 0.960 / 0.767 / 0.767 |
| 912 | -2.1469 | -2.1529 | +0.0060 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 218,120 | 27,919,360 | 24 | 12.9 | SGD | 0.952 / 0.952 / 0.747 / 0.747 |
| 913 | -2.1052 | -2.1529 | +0.0477 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 193,429 | 24,758,912 | 24 | 11.3 | SGD | 0.960 / 0.960 / 0.753 / 0.753 |
| 914 | -0.0410 | -0.0303 | -0.0107 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 108,516 | 13,890,048 | 10 | 1.5 | unclassified | 0.143 / 0.143 / 0.047 / 0.047 |
| 915 | -2.1595 | -2.1529 | -0.0066 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 227,474 | 29,116,672 | 24 | 13.4 | SGD | 0.958 / 0.958 / 0.783 / 0.783 |
| 916 | -2.2697 | -2.2660 | -0.0037 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 142,367 | 18,222,976 | 24 | 6.6 | unclassified | 0.899 / 0.899 / 0.738 / 0.738 |

Objective on each of the seven suites:

| task seed | train-distribution | kappa1000 | d32 | d8 | sigma0.3 | T200 | scale10/0.1 |
|---|---|---|---|---|---|---|---|
| 901 | -2.1529 | -1.4477 | -1.8831 | -2.2144 | -1.0394 | -2.8413 | -0.6792 |
| 902 | -2.2879 | -1.3161 | -1.9172 | -2.4623 | -0.7081 | -2.6810 | -0.7505 |
| 903 | -2.1529 | -1.4477 | -1.8831 | -2.2144 | -1.0394 | -2.8413 | -0.6792 |
| 904 | -2.1521 | -1.4475 | -1.8789 | -2.2143 | -1.0376 | -2.8404 | -0.6768 |
| 905 | -2.6468 | -1.4834 | -2.3887 | -2.6997 | -1.0333 | -2.9239 | -0.9701 |
| 906 | -2.1529 | -1.4477 | -1.8831 | -2.2144 | -1.0394 | -2.8413 | -0.6792 |
| 907 | -2.1529 | -1.4477 | -1.8831 | -2.2144 | -1.0394 | -2.8413 | -0.6792 |
| 908 | -2.1529 | -1.4477 | -1.8831 | -2.2144 | -1.0394 | -2.8413 | -0.6792 |
| 909 | -2.1529 | -1.4477 | -1.8831 | -2.2144 | -1.0394 | -2.8413 | -0.6792 |
| 910 | -2.1529 | -1.4477 | -1.8831 | -2.2144 | -1.0394 | -2.8413 | -0.6792 |
| 911 | -2.1529 | -1.4477 | -1.8831 | -2.2144 | -1.0394 | -2.8413 | -0.6792 |
| 912 | -2.1529 | -1.4477 | -1.8831 | -2.2144 | -1.0394 | -2.8413 | -0.6792 |
| 913 | -2.1529 | -1.4477 | -1.8831 | -2.2144 | -1.0394 | -2.8413 | -0.6792 |
| 914 | -0.0303 | -0.0193 | 0.0161 | -0.0493 | -0.0258 | -0.0307 | -0.0303 |
| 915 | -2.1529 | -1.4477 | -1.8831 | -2.2144 | -1.0394 | -2.8413 | -0.6792 |
| 916 | -2.2660 | -1.2836 | -1.8869 | -2.4635 | -0.6453 | -2.6451 | -0.7036 |

## Best rule of the arm (lowest suite 1: task seed 905)

    w' = (w - tanh(tanh(σ(-0.201·-1.460)·tanh(tanh(tanh(tanh(tanh(tanh(tanh(tanh(tanh(tanh(tanh((tanh(tanh(tanh(g))) + tanh(u3))))))))))))))))
    u2' = tanh(tanh(tanh(tanh(tanh(tanh(tanh(tanh(tanh(tanh((tanh(tanh(tanh(g))) + tanh(u3))))))))))))
    u3' = σ(-0.201·-1.460)·tanh(tanh(tanh(tanh(tanh(tanh(tanh(tanh(tanh(tanh(tanh((tanh(tanh(tanh(g))) + tanh(u3)))))))))))))

runs/n-plain/seed905/best.json: momentum   SGD R²=0.700 (η=0.484, β=0, β₂=0)  momentum R²=0.963 (η=0.495, β=0.5, β₂=0)  RMSProp R²=0.598 (η=0.00317, β=0, β₂=0.999)  Adam R²=0.795 (η=0.00615, β=0.5, β₂=0.999)

Files: per seed summary.md, log.csv, best.json; aggregate.md as written by the runner (its columns are those of the memory task and stay empty
for testbed 2); opt_structure.txt (output of the structural test per seed); runner_log_epyc.txt.

## Predictions against outcome (runs/n-plain/N_VORHERSAGE.md, committed in be1b18b before any N run)

1. n-plain at least one of 16 at the Adam level (P = 0.10): no seed has suite 1 at or below -3.023 (best -2.6468, seed 905).
2. n-random at least one at the Adam level (P = 0.02): no (best -2.1207).
3. n-plain median suite 1 at or below SGD's -2.072 (P = 0.45): yes (-2.1529).
4. n-plain structural class SGD for 8 or more of 16 (P = 0.50): yes (8).
5. n-random median suite 1 worse (higher) than n-plain (P = 0.90): yes (-2.1148 vs -2.1529).
6. n-plain at least one seed with a diverged fraction above 0 (P = 0.70): no (0).
7. timing projection at or below 30 h for each arm (P = 0.70): yes (2.3 h and 0.6 h).
8. mean train - suite-1 gap of n-plain at or below 0.1 in absolute value (P = 0.75): yes (-0.0198).
