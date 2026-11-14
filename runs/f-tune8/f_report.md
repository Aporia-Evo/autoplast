# f-tune8 (package F): results as measured

Base task (v2 setting: no --task, no --regime, default 19-op alphabet, one state, add-node on), seeds 1-16, 1,500,000 candidates,
--parallel 2 --threads 8 (batch 128), flags --tune-consts 8 --val-log, commit 6df6477, all seeds on epyc. Wall 3401 s (0.94 h).
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

f-tune8: primary 7/16, structural 5/16. Below both thresholds: no detectable effect at this sample size.
The Fisher p-values are extra context, not the pre-registered rule.

## Per seed

| seed | delta beta=0.5 level at | family | a | erase c/a | train | test ow0.3 | JAX ow0.3 | train - test | T64 K8 | T128 K8 | instr | real evals | val_acc | long_acc | min |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | – | linear attention | 0.958 | -0.000 | 0.814 | 0.787 | 0.778 | +0.027 | 0.398 | 0.378 | 5 | 577,913 | 0.800 | 0.365 | 4.4 |
| 2 | 782052 | gated delta rule | 1.093 | 0.644 | 0.970 | 0.964 | 0.957 | +0.006 | 0.074 | 0.018 | 14 | 733,474 | 0.967 | 0.006 | 14.0 |
| 3 | – | linear attention | 0.958 | 0.000 | 0.814 | 0.787 | 0.778 | +0.027 | 0.398 | 0.378 | 4 | 416,778 | 0.800 | 0.365 | 3.6 |
| 4 | 520284 | delta rule | 1.000 | 0.504 | 0.940 | 0.922 | 0.921 | +0.018 | 0.830 | 0.828 | 13 | 885,902 | 0.934 | 0.826 | 19.5 |
| 5 | 292436 | gated delta rule | 1.098 | 0.683 | 0.975 | 0.966 | 0.961 | +0.009 | 0.081 | 0.000 | 11 | 983,227 | 0.972 | 0.000 | 7.8 |
| 6 | 221140 | gated delta rule | 1.118 | 0.746 | 0.972 | 0.966 | 0.957 | +0.006 | 0.031 | 0.000 | 13 | 907,633 | 0.969 | 0.000 | 8.2 |
| 7 | – | linear attention | 0.958 | -0.000 | 0.814 | 0.787 | 0.778 | +0.027 | 0.398 | 0.378 | 6 | 556,365 | 0.800 | 0.365 | 5.1 |
| 8 | – | linear attention | 0.958 | -0.000 | 0.814 | 0.787 | 0.778 | +0.027 | 0.398 | 0.378 | 5 | 431,482 | 0.800 | 0.365 | 3.7 |
| 9 | – | linear attention | 0.958 | -0.000 | 0.814 | 0.787 | 0.778 | +0.027 | 0.398 | 0.378 | 6 | 587,959 | 0.800 | 0.365 | 4.6 |
| 10 | – | linear attention | 0.958 | -0.000 | 0.814 | 0.787 | 0.778 | +0.027 | 0.398 | 0.378 | 5 | 476,235 | 0.800 | 0.365 | 4.1 |
| 11 | 116636 | unclassified | 1.140 | 0.737 | 0.971 | 0.967 | 0.959 | +0.004 | 0.028 | 0.000 | 12 | 922,866 | 0.970 | 0.000 | 7.8 |
| 12 | 1269540 | gated delta rule | 1.117 | 0.713 | 0.972 | 0.970 | 0.967 | +0.002 | 0.105 | 0.000 | 15 | 559,882 | 0.975 | 0.000 | 4.7 |
| 13 | – | linear attention | 0.958 | -0.000 | 0.814 | 0.787 | 0.778 | +0.027 | 0.398 | 0.378 | 4 | 334,011 | 0.800 | 0.365 | 2.9 |
| 14 | – | linear attention | 0.958 | 0.001 | 0.820 | 0.789 | 0.777 | +0.031 | 0.402 | 0.375 | 10 | 685,025 | 0.800 | 0.353 | 5.2 |
| 15 | 208356 | unclassified | 1.000 | 0.429 | 0.954 | 0.937 | 0.927 | +0.017 | 0.000 | 0.000 | 11 | 992,486 | 0.948 | 0.000 | 11.4 |
| 16 | – | linear attention | 0.958 | -0.000 | 0.814 | 0.787 | 0.778 | +0.027 | 0.398 | 0.378 | 4 | 384,476 | 0.800 | 0.365 | 3.3 |

"delta beta=0.5 level at" is the Milestones line (first candidate count where best train accuracy reached 0.932).
val_acc and long_acc are the last row of log.csv (--val-log). Largest difference JAX (verify.txt, fresh embeddings) against Rust on
test ow0.3: 0.012.
Growth factor a of the final rules at the delta level or in the delta family: 1.093, 1.000, 1.098, 1.118, 1.140, 1.117, 1.000; a = 1.000 in seeds 4, 15.
