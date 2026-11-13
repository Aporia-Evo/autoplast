# Package E: d-kalman seeds 17 to 32, and the 32 seeds together

Seeds 17-32 of tag d-kalman, same setting as package D: collision3, task seed 1, 96 + 48 train episodes, fixed readout,
--recip --persist-m 3 --persist-init identity, add-node on, 1,500,000 candidates, --parallel 2 --threads 8 (batch 128).
Same machine (epyc) and the same binary as seeds 1-16 (built from e979a8e on 12 Nov 2026; src/ unchanged up to af0a992).
All 32 summaries carry commit e979a8e. Wall time of seeds 17-32: 19314 s (5.37 h). Seeds 1-16 and d-kalman_report.md
were not touched. Facts only; the interpretation is left to the research agent.

## Seeds 17 to 32

| seed | train | collision3 test | JAX on dump | T64 K8 | T128 K8 | train - test | family | S' reads | 1/( in S' | last best_acc gain at | rule 2 | minutes |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 17 | 0.623 | 0.634 | 0.6337 | 0.817 | 0.818 | -0.011 | unclassified | P1,P2 | no | 1,450,100 | - | 34 |
| 18 | 0.536 | 0.528 | 0.5278 | 0.586 | 0.566 | +0.008 | unclassified | P2 | no | 1,000,052 | - | 17 |
| 19 | 0.515 | 0.518 | 0.5181 | 0.573 | 0.558 | -0.003 | decayed linear attention | neither | no | 350,068 | - | 20 |
| 20 | 0.520 | 0.513 | 0.5130 | 0.575 | 0.549 | +0.007 | unclassified | P1,P2 | no | 1,450,100 | - | 55 |
| 21 | 0.515 | 0.520 | 0.5201 | 0.582 | 0.561 | -0.005 | unclassified | P2 | yes | 1,200,116 | - | 26 |
| 22 | 0.519 | 0.000 | 0.5153 (diverged) | 0.577 | 0.561 | +0.519 | unclassified | P1,P2 | no | 500,084 | - | 29 |
| 23 | 0.509 | 0.516 | 0.5162 | 0.583 | 0.550 | -0.007 | decayed linear attention | neither | no | 100,084 | - | 15 |
| 24 | 0.654 | 0.657 | 0.6568 | 0.860 | 0.866 | -0.003 | unclassified | P2 | no | 1,250,036 | pass | 30 |
| 25 | 0.667 | 0.672 | 0.6715 | 0.859 | 0.861 | -0.005 | unclassified | P2 | no | 1,350,004 | pass | 91 |
| 26 | 0.511 | 0.516 | 0.5156 | 0.583 | 0.553 | -0.005 | decayed linear attention | neither | no | 100,084 | - | 15 |
| 27 | 0.681 | 0.687 | 0.6868 | 0.816 | 0.808 | -0.006 | unclassified | P1,P2 | no | 650,100 | - | 55 |
| 28 | 0.572 | 0.578 | 0.5782 | 0.700 | 0.665 | -0.006 | unclassified | P1,P2 | no | 800,116 | - | 27 |
| 29 | 0.512 | 0.513 | 0.5135 | 0.578 | 0.562 | -0.001 | unclassified | P1,P2 | no | 250,100 | - | 41 |
| 30 | 0.642 | 0.642 | 0.6422 | 0.808 | 0.800 | +0.000 | unclassified | P2 | no | 850,036 | - | 61 |
| 31 | 0.633 | 0.634 | 0.6336 | 0.792 | 0.784 | -0.001 | unclassified | P2 | no | 450,036 | - | 72 |
| 32 | 0.600 | 0.603 | 0.6028 | 0.758 | 0.760 | -0.003 | unclassified | P2 | no | 600,052 | - | 44 |

Seed 22: Rust scores the collision3 test 0.000 because the overflow guard (|S| > 1e4 or not finite in any episode) zeroes the whole
suite; verify.py flags the same seed as diverged and gives 0.5153 without the guard. Its train accuracy is 0.519, so it fails rule 2
in either reading.

## Counts, three times

### Seeds 17 to 32 (new)

- Main count (test > 0.85 AND T128 K8 >= 0.838 AND train - test <= 0.03): 0 of 16 (none).
- Seeds above 0.695 under rule 2's other two conditions: 0 of 16 (none); above 0.695 at all: 0.
- Rule 2 (test > 0.651 AND T128 K8 >= 0.838 AND train - test <= 0.03): 2 of 16 (24, 25).
- Median test 0.5530; seeds below 0.53 (decayed linear attention level, or 0 from the overflow guard): 8 (18, 19, 20, 21, 22, 23, 26, 29).
- Rule 1, Mann-Whitney (two-sided) of the test accuracies: against c-m2 (16 seeds) U = 118.0, p = 0.720;
  against 5a-A (16 seeds) U = 145.5, p = 0.521.
- S' reads P1 in 6, P2 in 13; reciprocal in S' in 1.
- JAX against Rust on the dumped test data: largest difference 0.5153; without seeds flagged as diverged 0.0005.

### Seeds 1 to 16 (as reported in d-kalman_report.md)

- Main count (test > 0.85 AND T128 K8 >= 0.838 AND train - test <= 0.03): 1 of 16 (9).
- Seeds above 0.695 under rule 2's other two conditions: 2 of 16 (7, 9); above 0.695 at all: 2.
- Rule 2 (test > 0.651 AND T128 K8 >= 0.838 AND train - test <= 0.03): 4 of 16 (2, 7, 9, 15).
- Median test 0.6375; seeds below 0.53 (decayed linear attention level, or 0 from the overflow guard): 4 (1, 8, 11, 14).
- Rule 1, Mann-Whitney (two-sided) of the test accuracies: against c-m2 (16 seeds) U = 149.0, p = 0.439;
  against 5a-A (16 seeds) U = 172.5, p = 0.097.
- S' reads P1 in 9, P2 in 12; reciprocal in S' in 1.
- JAX against Rust on the dumped test data: largest difference 0.0005; without seeds flagged as diverged 0.0005.

### All 32 seeds (the base rate for later comparisons)

- Main count (test > 0.85 AND T128 K8 >= 0.838 AND train - test <= 0.03): 1 of 32 (9).
- Seeds above 0.695 under rule 2's other two conditions: 2 of 32 (7, 9); above 0.695 at all: 2.
- Rule 2 (test > 0.651 AND T128 K8 >= 0.838 AND train - test <= 0.03): 6 of 32 (2, 7, 9, 15, 24, 25).
- Median test 0.6300; seeds below 0.53 (decayed linear attention level, or 0 from the overflow guard): 12 (1, 8, 11, 14, 18, 19, 20, 21, 22, 23, 26, 29).
- Rule 1, Mann-Whitney (two-sided) of the test accuracies: against c-m2 (16 seeds) U = 267.0, p = 0.818;
  against 5a-A (16 seeds) U = 318.0, p = 0.178.
- S' reads P1 in 15, P2 in 25; reciprocal in S' in 2.
- JAX against Rust on the dumped test data: largest difference 0.5153; without seeds flagged as diverged 0.0005.

## Formulas of new seeds with test above 0.72

None of seeds 17-32 is above 0.72 (highest: seed 27, test 0.687, T128 K8 0.808). The seed-9 shape check therefore has no case.
For reference, the two new seeds that pass rule 2 (24: 0.657, 25: 0.672) are in seed24/summary.md and seed25/summary.md.

## Predictions against outcome (seeds 17 to 32)

Research agent (README, "Package E"): main count 0 with P = 0.45: hit (0). At least one seed above 0.695 with P = 0.85: missed (0).
Executing agent (E_VORHERSAGE.md, committed in 107f920 before the run):
1. main count 0 (P = 0.45), 1 (P = 0.33), 2 or more (P = 0.22): 0.
2. at least one seed above 0.695 under rule 2's other conditions (P = 0.75): missed.
3. rule 2 passed by 2 to 7 new seeds (P = 0.65): hit (2).
4. seed-9 shape for new seeds above 0.72 (conditional): no case.
5. at least 3 new seeds at decayed linear attention level (P = 0.70): hit (7 seeds at 0.513 to 0.528, plus seed 22 at 0 from the guard).
6. wall time 5 to 8 h (P = 0.70): hit (5.37 h).
7. JAX within 0.002 for every new seed (P = 0.80): missed, because of seed 22 (guard); 0.0005 for the other 15.
8. rule 1 over all 32 significant against 5a-A (P = 0.45) / against c-m2 (P = 0.10): neither (p = 0.178 / 0.818).
