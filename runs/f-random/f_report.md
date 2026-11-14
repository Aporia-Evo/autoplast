# f-random (package F): results as measured

Base task (v2 setting: no --task, no --regime, default 19-op alphabet, one state, add-node on), seeds 1-16, 1,500,000 candidates,
--parallel 2 --threads 8 (batch 128), flags --algo random --val-log, commit 6df6477, all seeds on epyc. Wall 1421 s (0.39 h).
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

f-random: primary 0/16, structural 0/16. Below both thresholds: no detectable effect at this sample size.
The Fisher p-values are extra context, not the pre-registered rule.

## Per seed

| seed | delta beta=0.5 level at | family | a | erase c/a | train | test ow0.3 | JAX ow0.3 | train - test | T64 K8 | T128 K8 | instr | real evals | val_acc | long_acc | min |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | – | linear attention | 1.000 | 0.000 | 0.772 | 0.750 | 0.741 | +0.022 | 0.104 | 0.062 | 2 | 870,418 | 0.757 | 0.051 | 2.9 |
| 2 | – | linear attention | 1.000 | 0.000 | 0.772 | 0.750 | 0.741 | +0.022 | 0.104 | 0.062 | 2 | 871,105 | 0.757 | 0.051 | 3.0 |
| 3 | – | linear attention | 1.000 | 0.000 | 0.772 | 0.750 | 0.741 | +0.022 | 0.104 | 0.062 | 2 | 871,482 | 0.757 | 0.051 | 3.0 |
| 4 | – | linear attention | 1.000 | 0.000 | 0.772 | 0.750 | 0.741 | +0.022 | 0.104 | 0.062 | 2 | 871,608 | 0.757 | 0.051 | 3.0 |
| 5 | – | linear attention | 1.000 | 0.000 | 0.772 | 0.750 | 0.741 | +0.022 | 0.104 | 0.062 | 2 | 871,561 | 0.757 | 0.051 | 3.0 |
| 6 | – | linear attention | 1.000 | 0.000 | 0.772 | 0.750 | 0.741 | +0.022 | 0.104 | 0.062 | 2 | 871,918 | 0.757 | 0.051 | 3.0 |
| 7 | – | linear attention | 1.000 | 0.000 | 0.772 | 0.750 | 0.741 | +0.022 | 0.104 | 0.062 | 2 | 871,955 | 0.757 | 0.051 | 3.0 |
| 8 | – | linear attention | 1.000 | 0.000 | 0.772 | 0.750 | 0.741 | +0.022 | 0.104 | 0.062 | 2 | 872,077 | 0.757 | 0.051 | 3.0 |
| 9 | – | linear attention | 1.000 | 0.000 | 0.772 | 0.750 | 0.741 | +0.022 | 0.104 | 0.062 | 2 | 872,478 | 0.757 | 0.051 | 2.9 |
| 10 | – | linear attention | 1.000 | 0.000 | 0.772 | 0.750 | 0.741 | +0.022 | 0.104 | 0.062 | 2 | 872,662 | 0.757 | 0.051 | 2.9 |
| 11 | – | linear attention | 1.000 | 0.000 | 0.772 | 0.750 | 0.741 | +0.022 | 0.104 | 0.062 | 2 | 872,773 | 0.757 | 0.051 | 3.0 |
| 12 | – | linear attention | 1.000 | 0.000 | 0.772 | 0.750 | 0.741 | +0.022 | 0.104 | 0.062 | 2 | 872,283 | 0.757 | 0.051 | 3.0 |
| 13 | – | linear attention | 1.000 | 0.000 | 0.772 | 0.750 | 0.741 | +0.022 | 0.104 | 0.062 | 2 | 871,634 | 0.757 | 0.051 | 2.9 |
| 14 | – | linear attention | 1.000 | 0.000 | 0.772 | 0.750 | 0.741 | +0.022 | 0.104 | 0.062 | 2 | 872,276 | 0.757 | 0.051 | 2.9 |
| 15 | – | linear attention | 1.000 | 0.000 | 0.772 | 0.750 | 0.741 | +0.022 | 0.104 | 0.062 | 2 | 872,437 | 0.757 | 0.051 | 2.9 |
| 16 | – | linear attention | 1.000 | 0.000 | 0.772 | 0.750 | 0.741 | +0.022 | 0.104 | 0.062 | 2 | 871,136 | 0.757 | 0.051 | 2.9 |

"delta beta=0.5 level at" is the Milestones line (first candidate count where best train accuracy reached 0.932).
val_acc and long_acc are the last row of log.csv (--val-log). Largest difference JAX (verify.txt, fresh embeddings) against Rust on
test ow0.3: 0.009.
Growth factor a of the final rules at the delta level or in the delta family: none.

Every f-random seed ends at plain linear attention, S' = S + v kᵀ in 2 instructions (train 0.772); no seed goes beyond it.
