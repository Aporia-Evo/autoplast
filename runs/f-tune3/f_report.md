# f-tune3 (package F): results as measured

Base task (v2 setting: no --task, no --regime, default 19-op alphabet, one state, add-node on), seeds 1-16, 1,500,000 candidates,
--parallel 2 --threads 8 (batch 128), flags --tune-consts 3 --val-log, commit 6df6477, all seeds on epyc. Wall 3333 s (0.93 h).
Baseline: committed runs/v2 and runs/v2-noaddnode (not rerun). Their summaries predate the structure line and the T64/T128 suites;
their family, a and erase c/a are taken from the committed runs/structural-rescore.md. Facts only; interpretation is left to the research agent.

## Comparison (fixed before the run: an arm shows at 12/16 on the primary count or 11/16 on the structural count)

| tag | primary: delta beta=0.5 level | median candidates to it | structural: delta / gated delta | unclassified, erase c/a > 0.3 | train < 0.84 | mean train - test | one-sided Fisher vs pooled (primary / structural) |
|---|---|---|---|---|---|---|---|
| f-tune8 | 7/16 | 292,436 | 5/16 | 11, 15 | 9/16 | +0.0193 | 0.62 / 0.70 |
| f-tune3 | 8/16 | 135,099 | 6/16 | 12 | 8/16 | +0.0174 | 0.46 / 0.54 |
| f-random | 0/16 | – | 0/16 | none | 16/16 | +0.0220 | 1.00 / 1.00 |
| v2 | 6/16 | 86,260 | 5/16 | 8 | 9/16 | +0.0205 | – |
| v2-noaddnode | 8/16 | 497,204 | 6/16 | 4, 11 | 8/16 | +0.0159 | – |
| v2 + v2-noaddnode pooled | 14/32 | 388,980 | 11/32 | – | 17/32 | +0.0182 | – |

f-tune3: primary 8/16, structural 6/16. Below both thresholds: no detectable effect at this sample size.
The Fisher p-values are extra context, not the pre-registered rule.

## Per seed

| seed | delta beta=0.5 level at | family | a | erase c/a | train | test ow0.3 | JAX ow0.3 | train - test | T64 K8 | T128 K8 | instr | real evals | val_acc | long_acc | min |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | – | linear attention | 0.958 | -0.000 | 0.814 | 0.787 | 0.778 | +0.027 | 0.398 | 0.378 | 4 | 320,066 | 0.800 | 0.365 | 2.7 |
| 2 | 30739 | gated delta rule | 1.106 | 0.707 | 0.973 | 0.968 | 0.964 | +0.005 | 0.063 | 0.000 | 11 | 768,056 | 0.973 | 0.000 | 6.1 |
| 3 | 212911 | gated delta rule | 1.107 | 0.722 | 0.970 | 0.966 | 0.958 | +0.004 | 0.058 | 0.000 | 10 | 628,010 | 0.972 | 0.000 | 4.8 |
| 4 | – | linear attention | 0.958 | -0.000 | 0.814 | 0.787 | 0.778 | +0.027 | 0.398 | 0.378 | 6 | 419,372 | 0.800 | 0.365 | 3.1 |
| 5 | – | decayed linear attention | 0.945 | -0.001 | 0.814 | 0.790 | 0.776 | +0.024 | 0.465 | 0.447 | 10 | 618,197 | 0.806 | 0.430 | 5.1 |
| 6 | – | linear attention | 0.952 | 0.001 | 0.818 | 0.789 | 0.775 | +0.029 | 0.447 | 0.444 | 9 | 503,473 | 0.798 | 0.412 | 3.6 |
| 7 | 99755 | gated delta rule | 1.113 | 0.649 | 0.977 | 0.970 | 0.966 | +0.007 | 0.021 | 0.000 | 13 | 848,517 | 0.976 | 0.000 | 5.9 |
| 8 | – | decayed linear attention | 0.941 | 0.001 | 0.818 | 0.790 | 0.773 | +0.028 | 0.481 | 0.478 | 10 | 665,091 | 0.803 | 0.445 | 4.8 |
| 9 | 1196749 | delta rule | 1.000 | 0.549 | 0.938 | 0.922 | 0.916 | +0.016 | 0.847 | 0.846 | 16 | 688,962 | 0.932 | 0.828 | 19.5 |
| 10 | – | linear attention | 0.958 | -0.000 | 0.814 | 0.787 | 0.778 | +0.027 | 0.398 | 0.378 | 5 | 353,406 | 0.800 | 0.365 | 2.9 |
| 11 | 369422 | gated delta rule | 1.090 | 0.641 | 0.972 | 0.961 | 0.955 | +0.011 | 0.075 | 0.021 | 16 | 852,492 | 0.968 | 0.006 | 22.4 |
| 12 | 170444 | unclassified | 1.117 | 0.747 | 0.972 | 0.962 | 0.953 | +0.010 | 0.000 | 0.000 | 12 | 707,567 | 0.965 | 0.000 | 5.0 |
| 13 | 28498 | gated delta rule | 1.119 | 0.731 | 0.971 | 0.969 | 0.963 | +0.002 | 0.049 | 0.000 | 11 | 741,716 | 0.971 | 0.000 | 12.0 |
| 14 | – | linear attention | 0.958 | -0.000 | 0.814 | 0.787 | 0.778 | +0.027 | 0.398 | 0.378 | 4 | 306,903 | 0.800 | 0.365 | 2.6 |
| 15 | 61298 | linear, not error-correcting | 1.095 | 0.729 | 0.970 | 0.964 | 0.952 | +0.006 | 0.060 | 0.000 | 13 | 797,088 | 0.967 | 0.000 | 6.5 |
| 16 | – | linear attention | 0.951 | 0.001 | 0.817 | 0.789 | 0.775 | +0.028 | 0.451 | 0.449 | 6 | 348,566 | 0.800 | 0.416 | 2.7 |

"delta beta=0.5 level at" is the Milestones line (first candidate count where best train accuracy reached 0.932).
val_acc and long_acc are the last row of log.csv (--val-log). Largest difference JAX (verify.txt, fresh embeddings) against Rust on
test ow0.3: 0.017.
Growth factor a of the final rules at the delta level or in the delta family: 1.106, 1.107, 1.113, 1.000, 1.090, 1.117, 1.119, 1.095; a = 1.000 in seeds 9.
