# h-share (package H): results as measured

Base task (v2 setting), seeds 1-32, 1,500,000 candidates, --parallel 2 --threads 8 (batch 128), flags --select share --val-log, commit ad31161,
all three arms on epyc one after the other. Summary line: `search: regularized evolution  tune-consts: 0  select: share (radius 0.05)`. Wall of this arm 11913 s (3.31 h).
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

Delta rules (structural family delta or gated delta) of this arm, growth factor and T128 K8: seed 1: a = 1.122, T128 K8 0.000, seed 2: a = 1.000, T128 K8 0.839, seed 3: a = 1.092, T128 K8 0.021, seed 6: a = 1.209, T128 K8 0.000, seed 8: a = 1.000, T128 K8 0.733, seed 9: a = 1.170, T128 K8 0.000, seed 10: a = 1.123, T128 K8 0.000, seed 11: a = 1.000, T128 K8 0.725, seed 12: a = 1.209, T128 K8 0.000, seed 14: a = 1.110, T128 K8 0.000, seed 17: a = 1.065, T128 K8 0.074, seed 18: a = 1.000, T128 K8 0.821, seed 20: a = 1.172, T128 K8 0.000, seed 24: a = 1.094, T128 K8 0.021, seed 25: a = 1.101, T128 K8 0.018, seed 26: a = 1.100, T128 K8 0.019, seed 27: a = 1.167, T128 K8 0.000, seed 28: a = 1.174, T128 K8 0.000, seed 31: a = 1.115, T128 K8 0.000.
Largest difference JAX (verify.txt, fresh embeddings) against Rust on test ow0.3: 0.011.

## Failed seed

Seed 16 aborted after 681 s (exit -6): `thread 'main' panicked at src/evolve.rs:189:25: no entry found for key` (seed16/stderr.txt).
Its last log row is at 1,450,100 candidates (train 0.971, val 0.971, long 0.000). Read off the code, without a change to it: with a
behaviour cache (`--select share` or `lexicase`) the score cache is cleared once it holds more than 1,000,000 entries (lines 170 to 175),
after a batch has been evaluated and before the children look up their scores; only the freshly evaluated programs are inserted again,
so a child that was a cache hit in that batch is missing at line 189. Without a behaviour cache the threshold is 3,000,000.
The seed has no summary.md, so a later call of the runner would start it again. Not rerun: search code is not changed by the executing agent.

## Ranges of the final rules (all three arms)

- h-base: final train 0.812 to 0.977, test ow0.3 0.787 to 0.971, median T128 K8 0.378, seeds with T128 K8 >= 0.80: 0 of 32
- h-share: final train 0.931 to 0.971, test ow0.3 0.919 to 0.970, median T128 K8 0.019, seeds with T128 K8 >= 0.80: 10 of 31
- h-lexicase: final train 0.948 to 0.982, test ow0.3 0.935 to 0.975, median T128 K8 0.000, seeds with T128 K8 >= 0.80: 1 of 32

## Per seed

| seed | delta beta=0.5 level at | family | a | erase c/a | train | test ow0.3 | JAX ow0.3 | train - test | T64 K8 | T128 K8 | instr | real evals | val_acc | long_acc | pop_mean_acc | min |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | 61684 | gated delta rule | 1.122 | 0.672 | 0.970 | 0.970 | 0.964 | +0.000 | 0.036 | 0.000 | 15 | 952,921 | 0.971 | 0.000 | 0.536 | 10.6 |
| 2 | 90100 | delta rule | 1.000 | 0.474 | 0.941 | 0.934 | 0.926 | +0.007 | 0.849 | 0.839 | 15 | 966,385 | 0.943 | 0.820 | 0.512 | 9.2 |
| 3 | 119412 | gated delta rule | 1.092 | 0.679 | 0.969 | 0.968 | 0.962 | +0.001 | 0.099 | 0.021 | 14 | 977,775 | 0.974 | 0.010 | 0.553 | 11.3 |
| 4 | 87668 | unclassified | 1.000 | 0.446 | 0.943 | 0.934 | 0.927 | +0.009 | 0.832 | 0.822 | 13 | 947,374 | 0.943 | 0.809 | 0.557 | 12.7 |
| 5 | 41076 | unclassified | 1.000 | 0.497 | 0.945 | 0.936 | 0.930 | +0.009 | 0.847 | 0.841 | 15 | 917,400 | 0.946 | 0.822 | 0.559 | 9.8 |
| 6 | 61812 | gated delta rule | 1.209 | 0.827 | 0.954 | 0.950 | 0.941 | +0.004 | 0.000 | 0.000 | 15 | 920,264 | 0.956 | 0.000 | 0.557 | 19.6 |
| 7 | 29044 | linear, not error-correcting | 1.000 | 0.549 | 0.931 | 0.921 | 0.916 | +0.010 | 0.843 | 0.838 | 12 | 952,047 | 0.934 | 0.824 | 0.539 | 19.6 |
| 8 | 33012 | delta rule | 1.000 | 0.409 | 0.936 | 0.920 | 0.911 | +0.016 | 0.772 | 0.733 | 17 | 948,377 | 0.929 | 0.768 | 0.557 | 12.3 |
| 9 | 31988 | gated delta rule | 1.170 | 0.855 | 0.960 | 0.956 | 0.951 | +0.004 | 0.022 | 0.000 | 12 | 951,237 | 0.966 | 0.000 | 0.530 | 14.8 |
| 10 | 360308 | gated delta rule | 1.123 | 0.721 | 0.971 | 0.969 | 0.963 | +0.002 | 0.042 | 0.000 | 18 | 892,872 | 0.972 | 0.000 | 0.542 | 12.7 |
| 11 | 99188 | delta rule | 1.000 | 0.472 | 0.935 | 0.919 | 0.912 | +0.016 | 0.775 | 0.725 | 14 | 960,245 | 0.934 | 0.777 | 0.573 | 11.3 |
| 12 | 69748 | gated delta rule | 1.209 | 0.827 | 0.954 | 0.950 | 0.941 | +0.004 | 0.000 | 0.000 | 13 | 942,979 | 0.957 | 0.000 | 0.571 | 10.2 |
| 13 | 110068 | linear, not error-correcting | 1.139 | 0.777 | 0.957 | 0.958 | 0.947 | -0.001 | 0.024 | 0.000 | 9 | 910,042 | 0.954 | 0.000 | 0.591 | 10.1 |
| 14 | 241780 | gated delta rule | 1.110 | 0.703 | 0.967 | 0.970 | 0.964 | -0.003 | 0.055 | 0.000 | 15 | 972,475 | 0.973 | 0.000 | 0.546 | 10.8 |
| 15 | 29940 | delta + Kronecker mix | 1.125 | 0.728 | 0.964 | 0.968 | 0.963 | -0.004 | 0.073 | 0.000 | 13 | 952,693 | 0.974 | 0.000 | 0.565 | 11.5 |
| 16 | failed: panic at src/evolve.rs:189 after 681 s, no summary | | | | | | | | | | | | | | | 11.4 |
| 17 | 98932 | gated delta rule | 1.065 | 0.867 | 0.940 | 0.939 | 0.931 | +0.001 | 0.471 | 0.074 | 13 | 915,449 | 0.950 | 0.055 | 0.543 | 13.2 |
| 18 | 83444 | delta rule | 1.000 | 0.500 | 0.938 | 0.925 | 0.918 | +0.013 | 0.837 | 0.821 | 18 | 974,926 | 0.934 | 0.807 | 0.468 | 12.0 |
| 19 | 64884 | unclassified | 1.000 | 0.446 | 0.943 | 0.934 | 0.927 | +0.009 | 0.832 | 0.822 | 18 | 958,430 | 0.943 | 0.809 | 0.576 | 12.1 |
| 20 | 76660 | gated delta rule | 1.172 | 0.853 | 0.961 | 0.956 | 0.951 | +0.005 | 0.022 | 0.000 | 10 | 926,895 | 0.967 | 0.000 | 0.583 | 11.3 |
| 21 | 153076 | unclassified | 1.090 | 0.846 | 0.946 | 0.944 | 0.939 | +0.002 | 0.057 | 0.019 | 13 | 933,605 | 0.951 | 0.004 | 0.545 | 13.4 |
| 22 | 123124 | unclassified | 1.000 | 0.446 | 0.943 | 0.934 | 0.927 | +0.009 | 0.832 | 0.822 | 10 | 938,256 | 0.943 | 0.809 | 0.548 | 12.0 |
| 23 | 121332 | unclassified | 1.215 | 0.825 | 0.948 | 0.937 | 0.928 | +0.011 | 0.000 | 0.000 | 14 | 919,380 | 0.944 | 0.000 | 0.506 | 14.9 |
| 24 | 78324 | gated delta rule | 1.094 | 0.657 | 0.969 | 0.967 | 0.962 | +0.002 | 0.083 | 0.021 | 15 | 947,556 | 0.976 | 0.002 | 0.544 | 11.4 |
| 25 | 150004 | gated delta rule | 1.101 | 0.646 | 0.970 | 0.967 | 0.963 | +0.003 | 0.062 | 0.018 | 14 | 928,808 | 0.972 | 0.000 | 0.510 | 15.0 |
| 26 | 430708 | gated delta rule | 1.100 | 0.637 | 0.970 | 0.967 | 0.962 | +0.003 | 0.058 | 0.019 | 17 | 951,708 | 0.973 | 0.000 | 0.518 | 10.3 |
| 27 | 154868 | gated delta rule | 1.167 | 0.814 | 0.963 | 0.961 | 0.956 | +0.002 | 0.022 | 0.000 | 14 | 938,296 | 0.969 | 0.000 | 0.501 | 10.8 |
| 28 | 163444 | gated delta rule | 1.174 | 0.852 | 0.960 | 0.956 | 0.951 | +0.004 | 0.021 | 0.000 | 12 | 900,191 | 0.967 | 0.000 | 0.596 | 9.6 |
| 29 | 44532 | unclassified | 1.000 | 0.446 | 0.943 | 0.934 | 0.927 | +0.009 | 0.832 | 0.822 | 14 | 936,223 | 0.943 | 0.809 | 0.515 | 14.3 |
| 30 | 105716 | unclassified | 1.000 | 0.375 | 0.940 | 0.936 | 0.925 | +0.004 | 0.829 | 0.820 | 12 | 902,884 | 0.940 | 0.815 | 0.593 | 10.1 |
| 31 | 52084 | gated delta rule | 1.115 | 0.749 | 0.964 | 0.968 | 0.962 | -0.004 | 0.052 | 0.000 | 18 | 967,643 | 0.970 | 0.000 | 0.546 | 9.2 |
| 32 | 197236 | unclassified | 1.000 | 0.419 | 0.942 | 0.939 | 0.929 | +0.003 | 0.847 | 0.840 | 14 | 941,936 | 0.941 | 0.818 | 0.510 | 12.6 |
