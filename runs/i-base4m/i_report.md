# Package I: i-base4m and the rerun of h-share seed 16

i-base4m: base task, plain search (--val-log), seeds 1-32, 4,000,000 candidates, --parallel 2 --threads 8 (batch 128), commit 50c2d10
(with the cache fix), epyc, wall 17485 s (4.86 h). h-share seed 16 rerun: --select share --val-log, 1,500,000 candidates, same build.
Facts only; the interpretation is left to the research agent.

## Counts of package H, with i-base4m

| tag | budget | accuracy level delta beta=0.5 | median candidates to it | structural delta / gated delta | unclassified, erase > 0.3 | train < 0.84 | median test ow0.3 | mean train - test | mean real evals | mean minutes | median instructions | delta rules abs(a-1) <= 0.02 | T128 K8 >= 0.80 | mean last pop_mean_acc |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| i-base4m | 4M | 24/32 | 1,461,812 | 22/32 | 2 | 7/32 | 0.966 | +0.0122 | 1,356,502 | 17.7 | 11 | 1 | 2 | 0.703 |
| h-base | 1.5M | 12/32 | 140,340 | 12/32 | 0 | 19/32 | 0.798 | +0.0190 | 457,064 | 4.9 | 9 | 0 | 0 | 0.683 |
| h-share (32 seeds with the rerun of seed 16) | 1.5M | 32/32 | 88,884 | 20/32 | 9 | 0/32 | 0.950 | +0.0048 | 942,486 | 12.2 | 14 | 4 | 10 | 0.544 |
| h-lexicase | 1.5M | 32/32 | 74,548 | 10/32 | 18 | 0/32 | 0.969 | +0.0075 | 747,112 | 9.2 | 15 | 0 | 1 | 0.702 |

i-base4m at the accuracy level of delta beta=0.5 (Milestones line): by 1,500,000 candidates 12/32 (seeds 3, 6, 7, 8, 9, 12, 16, 21, 27, 29, 31, 32),
by 4,000,000 candidates 24/32 (seeds 3, 5, 6, 7, 8, 9, 11, 12, 14, 16, 18, 19, 20, 21, 22, 24, 25, 26, 27, 28, 29, 30, 31, 32). The seeds reached by 1.5M are exactly those of h-base.
Count fixed before the run (README, "Package I"): 24/32 at 4M. The README names two cases, below 24/32 and 28/32 or more;
24/32 is in neither.
One-sided Fisher tests (extra context, as in H):
- h-share against i-base4m, accuracy level: 32/32 vs 24/32, p = 0.0024; structural: 20/32 vs 22/32, p = 0.785
- h-lexicase against i-base4m, accuracy level: 32/32 vs 24/32, p = 0.0024; structural: 10/32 vs 22/32, p = 1.000
Largest difference JAX (verify.txt, fresh embeddings) against Rust on test ow0.3 for i-base4m: 0.014.
Minutes per seed: mean 17.7, min 5.0, max 51.0.

## h-share seed 16, rerun with the fixed code

| seed | level at | family | a | erase c/a | train | test ow0.3 | JAX ow0.3 | train - test | T64 K8 | T128 K8 | instr | real evals | val_acc | long_acc | pop_mean_acc | min |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 16 | 39284 | gated delta rule | 1.118 | 0.729 | 0.971 | 0.968 | 0.962 | +0.003 | 0.050 | 0.000 | 17 | 1,012,274 | 0.971 | 0.000 | 0.531 | 11.6 |

- The first 30 log rows of the rerun equal all 30 rows of the aborted run in every column except real_evals and seconds
  (the aborted log is kept in runs/h-share/seed16_aborted/ with its stderr.txt). The rerun has 31 rows.
- The 31 rows of this rerun also equal those of runs/h-share/seed16_local_rerun/ (review machine) in the same columns.
- h-share with 32 seeds: accuracy level 32/32, structural 20/32; one-sided Fisher against h-base:
  p = 1.2e-08 and p = 0.040.
- runs/h-share/aggregate.md was not rewritten: after the seed finished, aggregate.py stopped with
  `ValueError: invalid literal for int() with base 10: '16_local_rerun'` (it reads every seed* folder name as a number; the folders
  seed16_local_rerun and seed16_aborted break it). The committed aggregate.md of h-share still lists 31 seeds. Not changed by the executing agent.

## Per seed, i-base4m

| seed | level at | family | a | erase c/a | train | test ow0.3 | JAX ow0.3 | train - test | T64 K8 | T128 K8 | instr | real evals | val_acc | long_acc | pop_mean_acc | min |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | – | linear attention | 0.958 | 0.000 | 0.814 | 0.787 | 0.778 | +0.027 | 0.398 | 0.378 | 4 | 641,437 | 0.800 | 0.365 | 0.710 | 5.2 |
| 2 | – | linear attention | 0.951 | 0.001 | 0.817 | 0.789 | 0.775 | +0.028 | 0.451 | 0.449 | 6 | 946,164 | 0.800 | 0.416 | 0.654 | 7.5 |
| 3 | 61044 | gated delta rule | 1.098 | 0.683 | 0.975 | 0.966 | 0.961 | +0.009 | 0.081 | 0.018 | 10 | 1,391,197 | 0.972 | 0.010 | 0.747 | 10.8 |
| 4 | – | linear attention | 0.952 | 0.001 | 0.818 | 0.788 | 0.774 | +0.030 | 0.448 | 0.446 | 8 | 975,879 | 0.797 | 0.412 | 0.623 | 7.8 |
| 5 | 2176884 | unclassified | 1.185 | 0.636 | 0.978 | 0.972 | 0.965 | +0.006 | 0.000 | 0.000 | 14 | 1,438,293 | 0.977 | 0.000 | 0.703 | 10.1 |
| 6 | 18676 | gated delta rule | 1.104 | 0.669 | 0.973 | 0.968 | 0.962 | +0.005 | 0.057 | 0.000 | 10 | 1,314,762 | 0.972 | 0.000 | 0.674 | 9.6 |
| 7 | 440436 | gated delta rule | 1.119 | 0.676 | 0.977 | 0.971 | 0.966 | +0.006 | 0.052 | 0.000 | 15 | 2,157,102 | 0.973 | 0.000 | 0.686 | 18.4 |
| 8 | 531572 | gated delta rule | 1.107 | 0.703 | 0.973 | 0.968 | 0.963 | +0.005 | 0.062 | 0.000 | 11 | 1,489,776 | 0.972 | 0.000 | 0.679 | 11.9 |
| 9 | 1349108 | gated delta rule | 1.095 | 0.653 | 0.971 | 0.967 | 0.960 | +0.004 | 0.053 | 0.000 | 10 | 1,535,116 | 0.971 | 0.000 | 0.732 | 12.3 |
| 10 | – | linear attention | 0.958 | 0.000 | 0.814 | 0.787 | 0.778 | +0.027 | 0.398 | 0.378 | 4 | 611,489 | 0.800 | 0.365 | 0.707 | 5.2 |
| 11 | 2840948 | gated delta rule | 1.099 | 0.726 | 0.971 | 0.968 | 0.962 | +0.003 | 0.087 | 0.000 | 10 | 1,658,326 | 0.969 | 0.000 | 0.769 | 44.9 |
| 12 | 41588 | gated delta rule | 1.101 | 0.654 | 0.975 | 0.969 | 0.962 | +0.006 | 0.062 | 0.000 | 16 | 2,097,807 | 0.972 | 0.000 | 0.685 | 40.4 |
| 13 | – | linear attention | 0.958 | 0.000 | 0.814 | 0.787 | 0.778 | +0.027 | 0.398 | 0.378 | 4 | 585,322 | 0.800 | 0.365 | 0.689 | 5.0 |
| 14 | 2638836 | unclassified | 1.000 | 0.532 | 0.949 | 0.937 | 0.931 | +0.012 | 0.829 | 0.830 | 15 | 1,886,554 | 0.938 | 0.812 | 0.692 | 33.6 |
| 15 | – | unclassified | 0.956 | 0.137 | 0.841 | 0.810 | 0.797 | +0.031 | 0.544 | 0.511 | 14 | 1,719,320 | 0.823 | 0.527 | 0.672 | 51.0 |
| 16 | 14836 | gated delta rule | 1.108 | 0.696 | 0.972 | 0.967 | 0.962 | +0.005 | 0.044 | 0.000 | 11 | 1,634,873 | 0.972 | 0.000 | 0.745 | 11.1 |
| 17 | – | linear attention | 0.951 | 0.001 | 0.817 | 0.789 | 0.775 | +0.028 | 0.451 | 0.449 | 6 | 931,737 | 0.800 | 0.416 | 0.668 | 7.4 |
| 18 | 3788532 | delta rule | 1.000 | 0.493 | 0.938 | 0.921 | 0.917 | +0.017 | 0.814 | 0.806 | 13 | 987,625 | 0.932 | 0.797 | 0.682 | 8.5 |
| 19 | 2114548 | gated delta rule | 1.065 | 0.674 | 0.969 | 0.959 | 0.949 | +0.010 | 0.000 | 0.000 | 14 | 1,349,419 | 0.966 | 0.000 | 0.740 | 33.8 |
| 20 | 2947060 | gated delta rule | 1.104 | 0.665 | 0.976 | 0.970 | 0.968 | +0.006 | 0.119 | 0.000 | 11 | 1,062,059 | 0.972 | 0.000 | 0.767 | 8.3 |
| 21 | 198516 | gated delta rule | 1.145 | 0.729 | 0.970 | 0.966 | 0.957 | +0.004 | 0.030 | 0.000 | 10 | 1,493,236 | 0.970 | 0.000 | 0.708 | 12.8 |
| 22 | 2342644 | gated delta rule | 1.107 | 0.708 | 0.972 | 0.968 | 0.963 | +0.004 | 0.062 | 0.000 | 10 | 906,105 | 0.973 | 0.000 | 0.743 | 7.5 |
| 23 | – | linear attention | 0.958 | 0.000 | 0.814 | 0.787 | 0.778 | +0.027 | 0.398 | 0.378 | 4 | 657,838 | 0.800 | 0.365 | 0.696 | 5.5 |
| 24 | 2322036 | gated delta rule | 1.117 | 0.730 | 0.971 | 0.968 | 0.962 | +0.003 | 0.051 | 0.000 | 9 | 1,384,480 | 0.971 | 0.000 | 0.764 | 20.3 |
| 25 | 3171060 | gated delta rule | 1.110 | 0.708 | 0.975 | 0.967 | 0.960 | +0.008 | 0.056 | 0.000 | 14 | 883,897 | 0.971 | 0.000 | 0.725 | 7.1 |
| 26 | 1574516 | gated delta rule | 1.097 | 0.658 | 0.975 | 0.968 | 0.960 | +0.007 | 0.074 | 0.016 | 13 | 1,628,573 | 0.973 | 0.000 | 0.689 | 37.3 |
| 27 | 114036 | gated delta rule | 1.109 | 0.690 | 0.975 | 0.968 | 0.962 | +0.007 | 0.057 | 0.000 | 11 | 1,916,412 | 0.972 | 0.000 | 0.710 | 15.9 |
| 28 | 1578996 | gated delta rule | 1.106 | 0.680 | 0.975 | 0.967 | 0.961 | +0.008 | 0.053 | 0.000 | 15 | 1,593,157 | 0.971 | 0.000 | 0.678 | 40.4 |
| 29 | 166644 | gated delta rule | 1.098 | 0.683 | 0.975 | 0.966 | 0.961 | +0.009 | 0.079 | 0.018 | 10 | 1,295,776 | 0.972 | 0.010 | 0.734 | 9.9 |
| 30 | 2682612 | gated delta rule | 1.147 | 0.828 | 0.969 | 0.960 | 0.953 | +0.009 | 0.017 | 0.000 | 14 | 1,887,383 | 0.969 | 0.000 | 0.645 | 15.7 |
| 31 | 207348 | gated delta rule | 1.092 | 0.637 | 0.973 | 0.966 | 0.962 | +0.007 | 0.083 | 0.017 | 11 | 1,829,398 | 0.974 | 0.008 | 0.700 | 35.8 |
| 32 | 66292 | gated delta rule | 1.106 | 0.693 | 0.972 | 0.965 | 0.957 | +0.007 | 0.032 | 0.000 | 12 | 1,517,542 | 0.969 | 0.000 | 0.675 | 13.6 |

## Predictions against outcome (I_VORHERSAGE.md, committed in e7c41e0 before the run)

Research agent: 13 to 20 of 32 (P = 0.65): missed (24). 28 or more (P = 0.05): no.
1. 12 or fewer P = 0.10; 13 to 20 P = 0.65; 21 to 23 P = 0.12; 24 or more P = 0.13 (28 or more P = 0.03): 24, the bin given P = 0.13.
2. the same 12 seeds as h-base by 1.5M (P = 0.90): hit.
3. rerun of seed 16 reproduces the aborted rows (P = 0.90): hit.
4. seed 16 at the accuracy level (P = 0.90): hit; in the delta family (P = 0.60): hit (gated delta rule).
5. mean minutes 10 to 25 (P = 0.60): hit (17.7); total wall at or below 10 h (P = 0.75): hit (4.9 h).
6. mean train - test within 0.005 of h-base (P = 0.60): missed (+0.0122 against +0.0190).
