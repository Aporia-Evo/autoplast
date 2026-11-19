# l-downsample (package L): results as measured

Base task (v2 setting, no --task, no --regime), seeds 1-32, 1,500,000 candidates, --parallel 2 --threads 8 (batch 128), flags --select downsample --val-log,
commit 6c2f60a (passed as --extra="... --commit 6c2f60a", no git in the sandbox), workstation (Ryzen 7 5700G, Windows), 19 Nov 2026.
Summary line: `search: regularized evolution  tune-consts: 0  select: downsample (rate 0.1)  residual-insert: off`. Wall of this arm 6815 s (1.89 h).
Self-check of package F on the workstation before the run: last row `120052,22831,29.7,0.82164,0.8142,4,0.7183` (as expected).
Baselines h-base, h-share, h-lexicase: the committed runs (epyc, commit ad31161; h-share seed 16 is the epyc rerun at 50c2d10 from package I, its JAX value from verify_seed16.txt).
All four arms parsed with the same script from summary.md, log.csv, wall_seconds.txt and verify.txt; h-base and h-lexicase reproduce the numbers of their h_report.md.
Note: l-downsample ran on the workstation, the baselines on epyc; minutes are therefore not directly comparable.
Facts only; the interpretation is left to the research agent.

## Comparison

| tag | seeds with summary | accuracy level delta beta=0.5 | median candidates to it | median real evals to it | structural: delta / gated delta | unclassified, erase c/a > 0.3 | train < 0.84 (linear attention level) | median test ow0.3 | best test ow0.3 | mean train - test | mean real evals | mean minutes | mean last pop_mean_acc | delta rules with abs(a - 1) <= 0.02 | T128 K8 >= 0.80 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| l-downsample | 32/32 | 19/32 | 345,844 | 74,848 | 13/32 | 7 (1, 4, 8, 9, 24, 26, 31) | 13/32 | 0.9525 | 0.975 | +0.0155 | 489,513 | 7.0 | 0.702 | 1 of 13 | 2/32 |
| h-base | 32/32 | 12/32 | 140,340 | 39,672 | 12/32 | 0 (none) | 19/32 | 0.7985 | 0.971 | +0.0190 | 457,064 | 4.9 | 0.683 | 0 of 12 | 0/32 |
| h-share | 32/32 | 32/32 | 88,884 | 57,534 | 20/32 | 9 (4, 5, 19, 21, 22, 23, 29, 30, 32) | 0/32 | 0.9500 | 0.970 | +0.0048 | 942,486 | 12.2 | 0.544 | 4 of 20 | 10/32 |
| h-lexicase | 32/32 | 32/32 | 74,548 | 40,612 | 10/32 | 18 (1, 4, 5, 6, 8, 9, 12, 16, 19, 20, 23, 24, 25, 26, 27, 28, 30, 31) | 0/32 | 0.9690 | 0.975 | +0.0075 | 747,112 | 9.2 | 0.702 | 0 of 10 | 1/32 |

One-sided Fisher tests (fixed in README before the run; all four stated, none picked):
- l-downsample vs h-base, accuracy level (alternative: more): 19/32 vs 12/32, p = 0.066
- l-downsample vs h-lexicase, accuracy level (alternative: fewer): 19/32 vs 32/32, p = 2.6e-05
- l-downsample vs h-base, structural (alternative: more): 13/32 vs 12/32, p = 0.500
- l-downsample vs h-lexicase, structural (alternative: fewer): 13/32 vs 10/32, p = 0.851

Thresholds fixed in README: effect of down-sampling if 20/32 or more reach the accuracy level; lexicase does more than down-sampling if l-downsample
reaches 27/32 or fewer. Measured: 19/32.

"accuracy level" is the Milestones line `delta rule (beta=0.5)`: the first candidate count at which the best train accuracy reached 0.932 during the run;
the final rule can be another one. "real evals at level" is the real_evals column of the first log row at or after that candidate count.
"structural" is the family of the final rule (structure line). "train < 0.84" is the final train accuracy.
The 13 seeds without the accuracy level are the same 13 seeds that end below train 0.84: 3, 6, 7, 11, 14, 17, 18, 20, 21, 22, 27, 28, 29.
Seed 14 ends as structural family "delta rule" (a = 0.958) with train 0.825, below the accuracy level.
Seeds with train - test above 0.03: 3 (+0.031), 29 (+0.031).

Delta rules (structural family delta or gated delta) of this arm, growth factor and T128 K8: seed 2: gated delta rule, a = 1.107, T128 K8 0.000, seed 5: gated delta rule, a = 1.109, T128 K8 0.000, seed 10: gated delta rule, a = 1.105, T128 K8 0.000, seed 12: gated delta rule, a = 1.092, T128 K8 0.036, seed 13: gated delta rule, a = 1.087, T128 K8 0.019, seed 14: delta rule, a = 0.958, T128 K8 0.780, seed 15: gated delta rule, a = 1.109, T128 K8 0.000, seed 16: gated delta rule, a = 1.098, T128 K8 0.018, seed 19: gated delta rule, a = 1.086, T128 K8 0.008, seed 23: gated delta rule, a = 1.116, T128 K8 0.000, seed 25: gated delta rule, a = 1.106, T128 K8 0.000, seed 30: gated delta rule, a = 1.102, T128 K8 0.000, seed 32: delta rule, a = 1.000, T128 K8 0.800.
Seeds with T128 K8 >= 0.80: seed 4 (unclassified, a = 1.000, T128 K8 0.843), seed 32 (delta rule, a = 1.000, T128 K8 0.800).
Minutes per seed on the workstation: 2.7 to 24.2.

## Ranges of the final rules

- l-downsample: final train 0.814 to 0.982, test ow0.3 0.787 to 0.975, median T128 K8 0.071, seeds with T128 K8 >= 0.80: 2 of 32, largest JAX - Rust difference on test ow0.3 0.014
- h-base: final train 0.812 to 0.977, test ow0.3 0.787 to 0.971, median T128 K8 0.378, seeds with T128 K8 >= 0.80: 0 of 32, largest JAX - Rust difference on test ow0.3 0.014
- h-share: final train 0.931 to 0.971, test ow0.3 0.919 to 0.970, median T128 K8 0.019, seeds with T128 K8 >= 0.80: 10 of 32, largest JAX - Rust difference on test ow0.3 0.011
- h-lexicase: final train 0.948 to 0.982, test ow0.3 0.935 to 0.975, median T128 K8 0.000, seeds with T128 K8 >= 0.80: 1 of 32, largest JAX - Rust difference on test ow0.3 0.011

## Per seed (l-downsample)

| seed | delta beta=0.5 level at | real evals at level | linear attention level at | family | a | erase c/a | train | test ow0.3 | JAX ow0.3 | train - test | T64 K8 | T128 K8 | instr | real evals | val_acc | long_acc | pop_mean_acc | min |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | 482676 | 98,108 | 8052 | unclassified | 1.074 | 0.563 | 0.978 | 0.967 | 0.962 | +0.011 | 0.000 | 0.000 | 17 | 595,862 | 0.970 | 0.000 | 0.721 | 8.4 |
| 2 | 93172 | 28,039 | 22260 | gated delta rule | 1.107 | 0.689 | 0.973 | 0.967 | 0.962 | +0.006 | 0.060 | 0.000 | 11 | 541,323 | 0.972 | 0.000 | 0.740 | 6.4 |
| 3 | – | – | 9716 | linear attention | 0.958 | 0.000 | 0.819 | 0.788 | 0.778 | +0.031 | 0.398 | 0.377 | 7 | 381,316 | 0.802 | 0.361 | 0.727 | 11.3 |
| 4 | 359028 | 70,746 | 6644 | unclassified | 1.000 | 0.461 | 0.955 | 0.941 | 0.927 | +0.014 | 0.843 | 0.843 | 16 | 664,501 | 0.949 | 0.822 | 0.733 | 7.2 |
| 5 | 1016948 | 322,203 | 23284 | gated delta rule | 1.109 | 0.700 | 0.975 | 0.969 | 0.962 | +0.006 | 0.054 | 0.000 | 13 | 505,417 | 0.972 | 0.000 | 0.703 | 5.0 |
| 6 | – | – | 19956 | linear attention | 0.958 | 0.000 | 0.814 | 0.787 | 0.778 | +0.027 | 0.398 | 0.378 | 4 | 239,607 | 0.800 | 0.365 | 0.684 | 2.7 |
| 7 | – | – | 7412 | linear attention | 0.958 | -0.000 | 0.814 | 0.787 | 0.778 | +0.027 | 0.398 | 0.378 | 6 | 358,016 | 0.800 | 0.365 | 0.663 | 4.3 |
| 8 | 123252 | 58,149 | 118260 | unclassified | 1.167 | 0.644 | 0.982 | 0.975 | 0.968 | +0.007 | 0.000 | 0.000 | 16 | 712,182 | 0.975 | 0.000 | 0.748 | 6.8 |
| 9 | 854900 | 296,439 | 18164 | unclassified | 1.026 | 0.552 | 0.949 | 0.938 | 0.928 | +0.011 | 0.581 | 0.107 | 15 | 588,947 | 0.944 | 0.121 | 0.717 | 24.2 |
| 10 | 345844 | 74,848 | 39540 | gated delta rule | 1.105 | 0.689 | 0.975 | 0.968 | 0.962 | +0.007 | 0.062 | 0.000 | 15 | 681,351 | 0.973 | 0.000 | 0.730 | 19.1 |
| 11 | – | – | 25204 | linear attention | 0.958 | 0.000 | 0.814 | 0.787 | 0.778 | +0.027 | 0.398 | 0.378 | 4 | 219,590 | 0.800 | 0.365 | 0.689 | 3.0 |
| 12 | 517492 | 187,169 | 5108 | gated delta rule | 1.092 | 0.672 | 0.976 | 0.969 | 0.965 | +0.007 | 0.239 | 0.036 | 14 | 634,608 | 0.974 | 0.018 | 0.707 | 8.9 |
| 13 | 303604 | 126,392 | 136820 | gated delta rule | 1.087 | 0.579 | 0.970 | 0.965 | 0.959 | +0.005 | 0.077 | 0.019 | 10 | 664,001 | 0.967 | 0.012 | 0.722 | 9.5 |
| 14 | – | – | 88052 | delta rule | 0.958 | 1.000 | 0.825 | 0.808 | 0.805 | +0.017 | 0.775 | 0.780 | 7 | 337,342 | 0.821 | 0.762 | 0.695 | 4.1 |
| 15 | 148852 | 37,359 | 11380 | gated delta rule | 1.109 | 0.682 | 0.973 | 0.968 | 0.962 | +0.005 | 0.053 | 0.000 | 11 | 554,587 | 0.972 | 0.000 | 0.736 | 6.9 |
| 16 | 94452 | 20,821 | 4340 | gated delta rule | 1.098 | 0.683 | 0.975 | 0.966 | 0.961 | +0.009 | 0.081 | 0.018 | 11 | 606,363 | 0.972 | 0.010 | 0.661 | 7.3 |
| 17 | – | – | 57972 | linear attention | 0.958 | 0.000 | 0.814 | 0.787 | 0.778 | +0.027 | 0.398 | 0.378 | 4 | 234,806 | 0.800 | 0.365 | 0.680 | 3.0 |
| 18 | – | – | 17652 | linear attention | 0.958 | -0.000 | 0.814 | 0.787 | 0.778 | +0.027 | 0.398 | 0.378 | 6 | 314,617 | 0.800 | 0.365 | 0.669 | 3.4 |
| 19 | 1138932 | 271,050 | 9716 | gated delta rule | 1.086 | 0.605 | 0.973 | 0.964 | 0.958 | +0.009 | 0.075 | 0.008 | 14 | 435,600 | 0.969 | 0.006 | 0.709 | 4.6 |
| 20 | – | – | 12276 | linear attention | 0.958 | -0.000 | 0.814 | 0.787 | 0.778 | +0.027 | 0.398 | 0.378 | 4 | 231,544 | 0.800 | 0.365 | 0.704 | 2.9 |
| 21 | – | – | 57716 | linear attention | 0.952 | 0.001 | 0.818 | 0.788 | 0.775 | +0.030 | 0.448 | 0.443 | 9 | 483,814 | 0.797 | 0.410 | 0.688 | 4.8 |
| 22 | – | – | 41972 | linear attention | 0.958 | -0.000 | 0.814 | 0.787 | 0.778 | +0.027 | 0.398 | 0.378 | 4 | 228,547 | 0.800 | 0.365 | 0.699 | 2.8 |
| 23 | 17652 | 16,564 | 15988 | gated delta rule | 1.116 | 0.716 | 0.971 | 0.967 | 0.958 | +0.004 | 0.041 | 0.000 | 12 | 657,401 | 0.972 | 0.000 | 0.730 | 9.5 |
| 24 | 403700 | 132,856 | 7668 | unclassified | 1.200 | 0.661 | 0.981 | 0.974 | 0.971 | +0.007 | 0.000 | 0.000 | 15 | 595,561 | 0.977 | 0.000 | 0.718 | 6.9 |
| 25 | 161908 | 62,894 | 12404 | gated delta rule | 1.106 | 0.706 | 0.973 | 0.968 | 0.963 | +0.005 | 0.063 | 0.000 | 12 | 643,231 | 0.973 | 0.000 | 0.695 | 9.5 |
| 26 | 47604 | 13,577 | 7028 | unclassified | 1.161 | 0.598 | 0.979 | 0.973 | 0.968 | +0.006 | 0.000 | 0.000 | 16 | 736,892 | 0.975 | 0.000 | 0.710 | 7.6 |
| 27 | – | – | 9588 | linear attention | 0.958 | 0.000 | 0.814 | 0.787 | 0.778 | +0.027 | 0.398 | 0.378 | 4 | 230,497 | 0.800 | 0.365 | 0.704 | 2.7 |
| 28 | – | – | 7796 | linear attention | 0.958 | -0.000 | 0.814 | 0.787 | 0.778 | +0.027 | 0.398 | 0.378 | 4 | 273,714 | 0.800 | 0.365 | 0.678 | 3.4 |
| 29 | – | – | 50548 | linear attention | 0.952 | 0.001 | 0.818 | 0.787 | 0.775 | +0.031 | 0.449 | 0.446 | 12 | 613,586 | 0.797 | 0.410 | 0.575 | 9.5 |
| 30 | 48628 | 16,343 | 26100 | gated delta rule | 1.102 | 0.662 | 0.975 | 0.970 | 0.968 | +0.005 | 0.063 | 0.000 | 12 | 726,396 | 0.972 | 0.000 | 0.721 | 7.1 |
| 31 | 724596 | 170,784 | 6388 | unclassified | 1.111 | 0.569 | 0.977 | 0.971 | 0.966 | +0.006 | 0.180 | 0.000 | 11 | 475,876 | 0.973 | 0.000 | 0.763 | 5.4 |
| 32 | 1410164 | 473,540 | 222580 | delta rule | 1.000 | 0.539 | 0.928 | 0.914 | 0.905 | +0.014 | 0.819 | 0.800 | 13 | 497,311 | 0.926 | 0.799 | 0.641 | 6.3 |
