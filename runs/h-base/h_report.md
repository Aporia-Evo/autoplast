# h-base (package H): results as measured

Base task (v2 setting), seeds 1-32, 1,500,000 candidates, --parallel 2 --threads 8 (batch 128), flags --val-log, commit ad31161,
all three arms on epyc one after the other. Summary line: `search: regularized evolution  tune-consts: 0  select: fitness`. Wall of this arm 4916 s (1.37 h).
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

Delta rules (structural family delta or gated delta) of this arm, growth factor and T128 K8: seed 3: a = 1.098, T128 K8 0.018, seed 6: a = 1.125, T128 K8 0.000, seed 7: a = 1.121, T128 K8 0.000, seed 8: a = 1.107, T128 K8 0.000, seed 9: a = 1.090, T128 K8 0.010, seed 12: a = 1.089, T128 K8 0.018, seed 16: a = 1.108, T128 K8 0.000, seed 21: a = 1.145, T128 K8 0.000, seed 27: a = 1.109, T128 K8 0.000, seed 29: a = 1.101, T128 K8 0.000, seed 31: a = 1.092, T128 K8 0.018, seed 32: a = 1.107, T128 K8 0.000.
Largest difference JAX (verify.txt, fresh embeddings) against Rust on test ow0.3: 0.014.

## Ranges of the final rules (all three arms)

- h-base: final train 0.812 to 0.977, test ow0.3 0.787 to 0.971, median T128 K8 0.378, seeds with T128 K8 >= 0.80: 0 of 32
- h-share: final train 0.931 to 0.971, test ow0.3 0.919 to 0.970, median T128 K8 0.019, seeds with T128 K8 >= 0.80: 10 of 31
- h-lexicase: final train 0.948 to 0.982, test ow0.3 0.935 to 0.975, median T128 K8 0.000, seeds with T128 K8 >= 0.80: 1 of 32

## Per seed

| seed | delta beta=0.5 level at | family | a | erase c/a | train | test ow0.3 | JAX ow0.3 | train - test | T64 K8 | T128 K8 | instr | real evals | val_acc | long_acc | pop_mean_acc | min |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | – | linear attention | 0.958 | 0.000 | 0.814 | 0.787 | 0.778 | +0.027 | 0.398 | 0.378 | 4 | 276,974 | 0.800 | 0.365 | 0.708 | 2.1 |
| 2 | – | linear attention | 0.951 | 0.001 | 0.817 | 0.789 | 0.775 | +0.028 | 0.451 | 0.449 | 6 | 365,486 | 0.800 | 0.416 | 0.660 | 2.9 |
| 3 | 61044 | gated delta rule | 1.098 | 0.683 | 0.975 | 0.966 | 0.961 | +0.009 | 0.081 | 0.018 | 10 | 516,088 | 0.972 | 0.010 | 0.733 | 3.9 |
| 4 | – | linear attention | 0.952 | 0.001 | 0.817 | 0.788 | 0.775 | +0.029 | 0.448 | 0.446 | 6 | 334,724 | 0.798 | 0.414 | 0.646 | 2.7 |
| 5 | – | linear attention | 0.951 | -0.000 | 0.812 | 0.789 | 0.776 | +0.023 | 0.436 | 0.449 | 6 | 355,969 | 0.806 | 0.397 | 0.672 | 2.6 |
| 6 | 18676 | gated delta rule | 1.125 | 0.672 | 0.971 | 0.970 | 0.963 | +0.001 | 0.034 | 0.000 | 9 | 506,183 | 0.970 | 0.000 | 0.667 | 3.7 |
| 7 | 440436 | gated delta rule | 1.121 | 0.675 | 0.977 | 0.971 | 0.967 | +0.006 | 0.049 | 0.000 | 15 | 779,404 | 0.972 | 0.000 | 0.683 | 6.9 |
| 8 | 531572 | gated delta rule | 1.107 | 0.703 | 0.973 | 0.968 | 0.963 | +0.005 | 0.062 | 0.000 | 11 | 533,664 | 0.972 | 0.000 | 0.691 | 4.4 |
| 9 | 1349108 | gated delta rule | 1.090 | 0.630 | 0.971 | 0.967 | 0.961 | +0.004 | 0.063 | 0.010 | 14 | 393,982 | 0.970 | 0.000 | 0.673 | 3.3 |
| 10 | – | linear attention | 0.958 | -0.000 | 0.814 | 0.787 | 0.778 | +0.027 | 0.398 | 0.378 | 4 | 245,964 | 0.800 | 0.365 | 0.721 | 2.0 |
| 11 | – | unclassified | 0.954 | 0.124 | 0.836 | 0.809 | 0.795 | +0.027 | 0.550 | 0.515 | 11 | 593,604 | 0.825 | 0.539 | 0.619 | 14.3 |
| 12 | 41588 | gated delta rule | 1.089 | 0.633 | 0.973 | 0.966 | 0.961 | +0.007 | 0.089 | 0.018 | 14 | 736,988 | 0.975 | 0.008 | 0.724 | 13.3 |
| 13 | – | linear attention | 0.958 | 0.000 | 0.814 | 0.787 | 0.778 | +0.027 | 0.398 | 0.378 | 4 | 220,508 | 0.800 | 0.365 | 0.684 | 1.8 |
| 14 | – | linear attention | 0.952 | 0.001 | 0.821 | 0.787 | 0.776 | +0.034 | 0.450 | 0.439 | 14 | 614,240 | 0.795 | 0.420 | 0.681 | 12.7 |
| 15 | – | unclassified | 0.955 | 0.137 | 0.840 | 0.808 | 0.795 | +0.032 | 0.548 | 0.515 | 12 | 456,625 | 0.823 | 0.533 | 0.649 | 11.7 |
| 16 | 14836 | gated delta rule | 1.108 | 0.696 | 0.972 | 0.967 | 0.962 | +0.005 | 0.044 | 0.000 | 12 | 643,482 | 0.972 | 0.000 | 0.707 | 4.2 |
| 17 | – | linear attention | 0.951 | 0.001 | 0.817 | 0.789 | 0.775 | +0.028 | 0.451 | 0.449 | 6 | 347,598 | 0.800 | 0.416 | 0.686 | 2.7 |
| 18 | – | linear attention | 0.951 | -0.000 | 0.812 | 0.789 | 0.776 | +0.023 | 0.436 | 0.449 | 6 | 351,032 | 0.806 | 0.397 | 0.659 | 2.6 |
| 19 | – | linear attention | 0.958 | 0.000 | 0.814 | 0.787 | 0.778 | +0.027 | 0.398 | 0.378 | 5 | 267,317 | 0.800 | 0.365 | 0.715 | 2.5 |
| 20 | – | decayed linear attention | 0.949 | -0.000 | 0.812 | 0.788 | 0.776 | +0.024 | 0.444 | 0.459 | 8 | 418,489 | 0.809 | 0.404 | 0.653 | 3.2 |
| 21 | 198516 | gated delta rule | 1.145 | 0.729 | 0.970 | 0.966 | 0.957 | +0.004 | 0.030 | 0.000 | 11 | 561,190 | 0.970 | 0.000 | 0.675 | 4.7 |
| 22 | – | linear attention | 0.958 | 0.000 | 0.814 | 0.787 | 0.778 | +0.027 | 0.398 | 0.378 | 4 | 238,412 | 0.800 | 0.365 | 0.698 | 2.0 |
| 23 | – | linear attention | 0.958 | 0.000 | 0.814 | 0.787 | 0.778 | +0.027 | 0.398 | 0.378 | 4 | 289,482 | 0.800 | 0.365 | 0.716 | 2.3 |
| 24 | – | linear attention | 0.951 | 0.001 | 0.818 | 0.789 | 0.776 | +0.029 | 0.449 | 0.448 | 9 | 488,093 | 0.800 | 0.416 | 0.583 | 3.7 |
| 25 | – | linear attention | 0.958 | 0.000 | 0.814 | 0.787 | 0.778 | +0.027 | 0.398 | 0.378 | 4 | 223,276 | 0.800 | 0.365 | 0.695 | 1.8 |
| 26 | – | unclassified | 0.954 | 0.080 | 0.836 | 0.808 | 0.794 | +0.028 | 0.530 | 0.517 | 15 | 507,536 | 0.813 | 0.496 | 0.650 | 3.9 |
| 27 | 114036 | gated delta rule | 1.109 | 0.693 | 0.975 | 0.968 | 0.962 | +0.007 | 0.050 | 0.000 | 14 | 708,845 | 0.972 | 0.000 | 0.702 | 5.7 |
| 28 | – | unclassified | 0.952 | 0.064 | 0.834 | 0.809 | 0.797 | +0.025 | 0.521 | 0.516 | 9 | 275,266 | 0.820 | 0.488 | 0.697 | 3.9 |
| 29 | 166644 | gated delta rule | 1.101 | 0.726 | 0.971 | 0.968 | 0.962 | +0.003 | 0.081 | 0.000 | 8 | 471,899 | 0.969 | 0.000 | 0.765 | 3.4 |
| 30 | – | decayed linear attention | 0.945 | 0.001 | 0.818 | 0.789 | 0.777 | +0.029 | 0.467 | 0.459 | 11 | 631,043 | 0.802 | 0.426 | 0.581 | 4.7 |
| 31 | 207348 | gated delta rule | 1.092 | 0.622 | 0.972 | 0.966 | 0.961 | +0.006 | 0.076 | 0.018 | 14 | 719,015 | 0.971 | 0.004 | 0.729 | 13.7 |
| 32 | 66292 | gated delta rule | 1.107 | 0.722 | 0.970 | 0.966 | 0.958 | +0.004 | 0.058 | 0.000 | 10 | 553,684 | 0.972 | 0.000 | 0.721 | 4.7 |
