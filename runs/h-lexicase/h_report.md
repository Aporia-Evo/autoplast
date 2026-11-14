# h-lexicase (package H): results as measured

Base task (v2 setting), seeds 1-32, 1,500,000 candidates, --parallel 2 --threads 8 (batch 128), flags --select lexicase --val-log, commit ad31161,
all three arms on epyc one after the other. Summary line: `search: regularized evolution  tune-consts: 0  select: lexicase`. Wall of this arm 8919 s (2.48 h).
Facts only; the interpretation is left to the research agent.

## Comparison with h-base

| tag | seeds with summary | accuracy level delta beta=0.5 | median candidates to it | structural: delta / gated delta | unclassified, erase c/a > 0.3 | train < 0.84 | mean train - test | mean real evals | mean minutes | mean last pop_mean_acc | delta rules with abs(a - 1) <= 0.02 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| h-base | 32/32 | 12/32 | 140,340 | 12/32 | 0 (none) | 19/32 | +0.0190 | 457,064 | 4.9 | 0.683 | 0 of 12 |
| h-share | 31/32 | 31/31 | 90,100 | 19/31 | 9 (4, 5, 19, 21, 22, 23, 29, 30, 32) | 0/31 | +0.0048 | 940,235 | 12.2 | 0.545 | 4 of 19 |
| h-lexicase | 32/32 | 32/32 | 74,548 | 10/32 | 18 (1, 4, 5, 6, 8, 9, 12, 16, 19, 20, 23, 24, 25, 26, 27, 28, 30, 31) | 0/32 | +0.0075 | 747,112 | 9.2 | 0.702 | 0 of 10 |

One-sided Fisher tests against h-base (fixed before the run; four tests, no one is picked):
- h-share, accuracy level: 31/31 vs 12/32, p = 1.7e-08
- h-share, structural: 19/31 vs 12/32, p = 0.051
- h-lexicase, accuracy level: 32/32 vs 12/32, p = 1.2e-08
- h-lexicase, structural: 10/32 vs 12/32, p = 0.785
With the failed h-share seed 16 counted as a seed without success (n = 32): accuracy level p = 1.8e-07, structural p = 0.066.

"accuracy level" is the Milestones line `delta rule (beta=0.5)`: the first candidate count at which the best train accuracy reached
0.932 during the run; the final rule can be another one. "structural" is the family of the final rule (structure line).

Delta rules (structural family delta or gated delta) of this arm, growth factor and T128 K8: seed 2: a = 1.099, T128 K8 0.000, seed 7: a = 1.120, T128 K8 0.000, seed 10: a = 1.104, T128 K8 0.000, seed 11: a = 1.109, T128 K8 0.000, seed 13: a = 1.101, T128 K8 0.000, seed 15: a = 1.156, T128 K8 0.000, seed 17: a = 1.110, T128 K8 0.000, seed 21: a = 1.113, T128 K8 0.000, seed 22: a = 1.101, T128 K8 0.021, seed 32: a = 1.111, T128 K8 0.000.
Largest difference JAX (verify.txt, fresh embeddings) against Rust on test ow0.3: 0.011.

## Ranges of the final rules (all three arms)

- h-base: final train 0.812 to 0.977, test ow0.3 0.787 to 0.971, median T128 K8 0.378, seeds with T128 K8 >= 0.80: 0 of 32
- h-share: final train 0.931 to 0.971, test ow0.3 0.919 to 0.970, median T128 K8 0.019, seeds with T128 K8 >= 0.80: 10 of 31
- h-lexicase: final train 0.948 to 0.982, test ow0.3 0.935 to 0.975, median T128 K8 0.000, seeds with T128 K8 >= 0.80: 1 of 32

## Per seed

| seed | delta beta=0.5 level at | family | a | erase c/a | train | test ow0.3 | JAX ow0.3 | train - test | T64 K8 | T128 K8 | instr | real evals | val_acc | long_acc | pop_mean_acc | min |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | 497140 | unclassified | 1.169 | 0.625 | 0.982 | 0.975 | 0.968 | +0.007 | 0.000 | 0.000 | 17 | 727,559 | 0.976 | 0.000 | 0.708 | 5.7 |
| 2 | 364916 | gated delta rule | 1.099 | 0.684 | 0.973 | 0.967 | 0.960 | +0.006 | 0.071 | 0.000 | 15 | 658,917 | 0.973 | 0.000 | 0.695 | 16.8 |
| 3 | 133876 | delta + Kronecker mix | 1.100 | 0.623 | 0.978 | 0.969 | 0.964 | +0.009 | 0.108 | 0.021 | 14 | 772,459 | 0.975 | 0.006 | 0.707 | 6.7 |
| 4 | 372596 | unclassified | 1.194 | 0.578 | 0.981 | 0.971 | 0.966 | +0.010 | 0.000 | 0.000 | 14 | 739,223 | 0.975 | 0.000 | 0.728 | 5.4 |
| 5 | 312948 | unclassified | 1.111 | 0.569 | 0.977 | 0.971 | 0.965 | +0.006 | 0.178 | 0.000 | 10 | 604,407 | 0.973 | 0.000 | 0.752 | 5.2 |
| 6 | 165236 | unclassified | 1.167 | 0.645 | 0.977 | 0.974 | 0.970 | +0.003 | 0.036 | 0.000 | 13 | 765,238 | 0.973 | 0.000 | 0.686 | 6.8 |
| 7 | 81268 | gated delta rule | 1.120 | 0.722 | 0.973 | 0.969 | 0.962 | +0.004 | 0.046 | 0.000 | 15 | 821,933 | 0.972 | 0.000 | 0.680 | 17.0 |
| 8 | 116596 | unclassified | 1.119 | 0.578 | 0.979 | 0.971 | 0.965 | +0.008 | 0.035 | 0.000 | 16 | 784,221 | 0.971 | 0.000 | 0.690 | 6.8 |
| 9 | 30196 | unclassified | 1.155 | 0.642 | 0.978 | 0.973 | 0.969 | +0.005 | 0.025 | 0.000 | 15 | 773,962 | 0.976 | 0.000 | 0.705 | 6.9 |
| 10 | 35444 | gated delta rule | 1.104 | 0.688 | 0.975 | 0.968 | 0.959 | +0.007 | 0.068 | 0.000 | 12 | 686,525 | 0.973 | 0.000 | 0.698 | 6.7 |
| 11 | 20724 | gated delta rule | 1.109 | 0.643 | 0.979 | 0.971 | 0.966 | +0.008 | 0.053 | 0.000 | 15 | 732,998 | 0.975 | 0.000 | 0.751 | 5.5 |
| 12 | 52852 | unclassified | 1.000 | 0.524 | 0.958 | 0.946 | 0.937 | +0.012 | 0.839 | 0.836 | 16 | 855,233 | 0.952 | 0.826 | 0.723 | 23.4 |
| 13 | 872820 | gated delta rule | 1.101 | 0.686 | 0.972 | 0.968 | 0.960 | +0.004 | 0.068 | 0.000 | 13 | 557,188 | 0.972 | 0.000 | 0.672 | 14.4 |
| 14 | 94708 | delta + Kronecker mix | 1.114 | 0.668 | 0.978 | 0.967 | 0.962 | +0.011 | 0.035 | 0.000 | 13 | 686,778 | 0.975 | 0.000 | 0.686 | 5.4 |
| 15 | 28532 | gated delta rule | 1.156 | 0.785 | 0.971 | 0.965 | 0.957 | +0.006 | 0.025 | 0.000 | 13 | 703,725 | 0.969 | 0.000 | 0.683 | 6.7 |
| 16 | 76532 | unclassified | 1.211 | 0.685 | 0.982 | 0.974 | 0.968 | +0.008 | 0.000 | 0.000 | 18 | 923,864 | 0.976 | 0.000 | 0.659 | 6.5 |
| 17 | 72564 | gated delta rule | 1.110 | 0.689 | 0.978 | 0.970 | 0.966 | +0.008 | 0.054 | 0.000 | 14 | 795,417 | 0.973 | 0.000 | 0.706 | 5.8 |
| 18 | 311028 | delta + Kronecker mix | 1.074 | 0.530 | 0.975 | 0.958 | 0.956 | +0.017 | 0.260 | 0.014 | 16 | 811,700 | 0.968 | 0.021 | 0.647 | 14.8 |
| 19 | 342260 | unclassified | 1.067 | 0.593 | 0.977 | 0.967 | 0.964 | +0.010 | 0.180 | 0.015 | 18 | 838,748 | 0.971 | 0.025 | 0.690 | 8.6 |
| 20 | 13044 | unclassified | 1.111 | 0.569 | 0.977 | 0.971 | 0.966 | +0.006 | 0.180 | 0.000 | 12 | 705,032 | 0.973 | 0.000 | 0.682 | 5.8 |
| 21 | 267124 | gated delta rule | 1.113 | 0.674 | 0.977 | 0.970 | 0.967 | +0.007 | 0.221 | 0.000 | 15 | 717,214 | 0.973 | 0.000 | 0.751 | 6.9 |
| 22 | 58484 | gated delta rule | 1.101 | 0.726 | 0.971 | 0.968 | 0.962 | +0.003 | 0.081 | 0.021 | 14 | 843,609 | 0.969 | 0.012 | 0.683 | 27.1 |
| 23 | 98548 | unclassified | 1.113 | 0.725 | 0.972 | 0.966 | 0.956 | +0.006 | 0.033 | 0.000 | 15 | 806,444 | 0.968 | 0.000 | 0.668 | 7.7 |
| 24 | 42484 | unclassified | 1.170 | 0.642 | 0.977 | 0.974 | 0.970 | +0.003 | 0.030 | 0.000 | 11 | 556,162 | 0.973 | 0.000 | 0.765 | 3.8 |
| 25 | 27636 | unclassified | 1.057 | 0.431 | 0.948 | 0.935 | 0.924 | +0.013 | 0.000 | 0.000 | 18 | 805,286 | 0.937 | 0.000 | 0.652 | 13.6 |
| 26 | 24308 | unclassified | 1.220 | 0.659 | 0.978 | 0.970 | 0.966 | +0.008 | 0.000 | 0.000 | 13 | 699,179 | 0.974 | 0.000 | 0.717 | 5.2 |
| 27 | 68980 | unclassified | 1.127 | 0.615 | 0.981 | 0.971 | 0.964 | +0.010 | 0.000 | 0.000 | 19 | 875,058 | 0.973 | 0.000 | 0.648 | 17.2 |
| 28 | 52468 | unclassified | 1.200 | 0.656 | 0.979 | 0.975 | 0.970 | +0.004 | 0.000 | 0.000 | 16 | 771,173 | 0.974 | 0.000 | 0.744 | 7.6 |
| 29 | 119284 | delta + Kronecker mix | 1.136 | 0.663 | 0.977 | 0.969 | 0.964 | +0.008 | 0.059 | 0.000 | 13 | 678,954 | 0.975 | 0.000 | 0.713 | 5.0 |
| 30 | 27380 | unclassified | 1.087 | 0.660 | 0.971 | 0.967 | 0.964 | +0.004 | 0.122 | 0.015 | 11 | 606,091 | 0.969 | 0.018 | 0.717 | 5.1 |
| 31 | 58612 | unclassified | 1.131 | 0.614 | 0.979 | 0.969 | 0.963 | +0.010 | 0.189 | 0.000 | 16 | 792,133 | 0.973 | 0.000 | 0.735 | 6.4 |
| 32 | 66676 | gated delta rule | 1.111 | 0.687 | 0.975 | 0.967 | 0.961 | +0.008 | 0.050 | 0.000 | 15 | 811,170 | 0.973 | 0.000 | 0.728 | 7.0 |
