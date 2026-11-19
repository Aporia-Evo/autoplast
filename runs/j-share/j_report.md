# j-share (package J): results as measured

collision3, task seed 1, 96 + 48 train episodes, fixed readout, --recip --persist-m 3 --persist-init identity, add-node on,
--select share --val-log --level-acc 0.651 --level-long 0.838, seeds 1-32, 1,500,000 candidates, --parallel 2 --threads 8 (batch 128),
commit 50c2d10, all seeds on epyc. Wall 48366 s (13.44 h). Baseline: the committed 32 seeds of runs/d-kalman (not rerun).
Facts only; the interpretation is left to the research agent.

## Counts against d-kalman

| tag | rule 2 | stuck below 0.53 | test > 0.85 with rule 2's other conditions | above 0.695 under those conditions | above 0.90 | median test | mean train - test | mean real evals | mean minutes | mean last pop_mean_acc |
|---|---|---|---|---|---|---|---|---|---|---|
| j-share | 11/32 | 0/32 | 0/32 (none) | 0/32 (none) | 0/32 | 0.6525 | -0.0123 | 962,443 | 49.4 | 0.349 |
| d-kalman (32 seeds, baseline) | 6/32 | 12/32 | 1/32 (9) | 2/32 (7, 9) | 0/32 | 0.6300 | +0.0141 | 784,926 | 42.2 | 0.418 |
| j-lexicase (first arm of J, for reference) | 12/32 | 0/32 | 1/32 (6) | 5/32 (2, 6, 9, 12, 17) | 0/32 | 0.6815 | +0.0002 | 806,780 | 59.5 | 0.446 |

Fixed before the run (README, "Package J", thresholds of E): an effect is shown by rule 2 in 13/32 or more, by at most 5/32 stuck below
0.53, or by test > 0.85 under rule 2's other conditions in 7/32 or more. Outcome: rule 2 11/32 (not met), stuck 0/32 (met),
test > 0.85 0/32 (not met). Six looks in total over the two arms (README).
Rule 1, Mann-Whitney (two-sided) of the 32 test accuracies against the 32 of d-kalman: U = 741.0, p = 0.0021.
For reference, against j-lexicase: U = 259.5, p = 0.00071 (j-share lower).
Test range 0.617 to 0.694. Validation level reached in 16/32 seeds.
Structural families of the final rules: unclassified 26, delta rule 5, delta + Kronecker mix 1.
S' reads P1 in 20, P2 in 22; reciprocal in S' in 6.
JAX against Rust on the dumped test data: largest difference 0.0005; no seed flagged as diverged.

## Per seed

| seed | train | collision3 test | JAX on dump | T64 K8 | T128 K8 | train - test | family | S' reads | 1/( in S' | validation level at (candidates) | real evals at that row | instr | real evals | min | last pop_mean_acc | rule 2 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | 0.642 | 0.658 | 0.6583 | 0.861 | 0.881 | -0.016 | unclassified | P1,P2 | no | 1,250,036 | 776,333 | 13 | 937,470 | 47 | 0.369 | pass |
| 2 | 0.651 | 0.663 | 0.6632 | 0.833 | 0.816 | -0.012 | unclassified | P1,P2 | no | 800,116 | 525,702 | 14 | 971,921 | 47 | 0.403 | - |
| 3 | 0.618 | 0.634 | 0.6336 | 0.838 | 0.845 | -0.016 | unclassified | P2 | yes | not reached | – | 15 | 973,241 | 49 | 0.331 | - |
| 4 | 0.617 | 0.640 | 0.6402 | 0.840 | 0.828 | -0.023 | delta rule | neither | no | not reached | – | 10 | 963,988 | 46 | 0.290 | - |
| 5 | 0.672 | 0.690 | 0.6900 | 0.859 | 0.861 | -0.018 | unclassified | P1,P2 | yes | 100,084 | 52,261 | 20 | 979,873 | 76 | 0.319 | pass |
| 6 | 0.673 | 0.682 | 0.6823 | 0.864 | 0.884 | -0.009 | unclassified | P1,P2 | no | 900,084 | 553,582 | 15 | 953,469 | 50 | 0.390 | pass |
| 7 | 0.638 | 0.628 | 0.6283 | 0.810 | 0.789 | +0.010 | unclassified | P1,P2 | no | not reached | – | 19 | 960,341 | 40 | 0.349 | - |
| 8 | 0.631 | 0.640 | 0.6400 | 0.832 | 0.860 | -0.009 | unclassified | P1,P2 | no | 700,020 | 461,337 | 16 | 983,172 | 53 | 0.335 | - |
| 9 | 0.698 | 0.694 | 0.6940 | 0.861 | 0.868 | +0.004 | unclassified | P2 | yes | 300,020 | 196,884 | 17 | 1,010,986 | 46 | 0.334 | pass |
| 10 | 0.617 | 0.640 | 0.6402 | 0.840 | 0.828 | -0.023 | delta rule | neither | no | not reached | – | 8 | 981,836 | 76 | 0.326 | - |
| 11 | 0.668 | 0.672 | 0.6718 | 0.829 | 0.835 | -0.004 | unclassified | P1,P2 | no | 150,004 | 94,308 | 18 | 999,129 | 44 | 0.333 | - |
| 12 | 0.644 | 0.663 | 0.6629 | 0.873 | 0.891 | -0.019 | unclassified | P1 | no | 150,004 | 82,478 | 17 | 930,251 | 44 | 0.346 | pass |
| 13 | 0.603 | 0.622 | 0.6222 | 0.854 | 0.863 | -0.019 | delta rule | neither | yes | not reached | – | 15 | 958,767 | 52 | 0.340 | - |
| 14 | 0.627 | 0.640 | 0.6405 | 0.823 | 0.807 | -0.013 | delta + Kronecker mix | neither | no | 350,068 | 219,103 | 11 | 953,752 | 45 | 0.411 | - |
| 15 | 0.624 | 0.631 | 0.6314 | 0.778 | 0.764 | -0.007 | unclassified | P1,P2 | no | not reached | – | 15 | 998,158 | 37 | 0.339 | - |
| 16 | 0.621 | 0.636 | 0.6359 | 0.838 | 0.819 | -0.015 | unclassified | P1,P2 | no | not reached | – | 12 | 968,482 | 49 | 0.316 | - |
| 17 | 0.659 | 0.677 | 0.6769 | 0.870 | 0.881 | -0.018 | unclassified | P2 | no | 150,004 | 96,187 | 16 | 963,929 | 74 | 0.342 | pass |
| 18 | 0.615 | 0.641 | 0.6409 | 0.827 | 0.809 | -0.026 | delta rule | neither | no | not reached | – | 9 | 951,125 | 53 | 0.290 | - |
| 19 | 0.658 | 0.656 | 0.6560 | 0.687 | 0.681 | +0.002 | unclassified | P1 | yes | not reached | – | 19 | 963,498 | 39 | 0.337 | - |
| 20 | 0.642 | 0.657 | 0.6569 | 0.797 | 0.771 | -0.015 | unclassified | P1,P2 | no | not reached | – | 15 | 984,267 | 44 | 0.382 | - |
| 21 | 0.643 | 0.649 | 0.6489 | 0.739 | 0.732 | -0.006 | unclassified | P1,P2 | no | not reached | – | 13 | 940,418 | 47 | 0.294 | - |
| 22 | 0.657 | 0.668 | 0.6677 | 0.865 | 0.874 | -0.011 | unclassified | P2 | yes | 200,052 | 120,372 | 19 | 957,432 | 41 | 0.362 | pass |
| 23 | 0.641 | 0.630 | 0.6299 | 0.788 | 0.782 | +0.011 | unclassified | P1,P2 | no | not reached | – | 18 | 1,010,465 | 78 | 0.327 | - |
| 24 | 0.653 | 0.667 | 0.6672 | 0.864 | 0.863 | -0.014 | unclassified | P2 | no | 400,116 | 232,364 | 15 | 915,446 | 50 | 0.417 | pass |
| 25 | 0.614 | 0.617 | 0.6168 | 0.770 | 0.767 | -0.003 | unclassified | P1,P2 | no | not reached | – | 18 | 927,487 | 40 | 0.328 | - |
| 26 | 0.653 | 0.668 | 0.6678 | 0.846 | 0.849 | -0.015 | unclassified | P1 | no | 150,004 | 90,882 | 15 | 953,193 | 44 | 0.406 | pass |
| 27 | 0.671 | 0.684 | 0.6840 | 0.804 | 0.796 | -0.013 | unclassified | P1,P2 | no | not reached | – | 16 | 1,025,448 | 50 | 0.354 | - |
| 28 | 0.617 | 0.640 | 0.6402 | 0.840 | 0.828 | -0.023 | delta rule | P2 | no | not reached | – | 14 | 965,099 | 41 | 0.300 | - |
| 29 | 0.604 | 0.636 | 0.6360 | 0.763 | 0.667 | -0.032 | unclassified | P2 | no | not reached | – | 14 | 935,728 | 43 | 0.341 | - |
| 30 | 0.655 | 0.672 | 0.6723 | 0.858 | 0.859 | -0.017 | unclassified | P1,P2 | no | 900,084 | 575,170 | 16 | 974,282 | 55 | 0.354 | pass |
| 31 | 0.633 | 0.640 | 0.6405 | 0.866 | 0.879 | -0.007 | unclassified | P1 | no | 200,052 | 117,704 | 16 | 886,468 | 43 | 0.441 | - |
| 32 | 0.640 | 0.656 | 0.6557 | 0.844 | 0.850 | -0.016 | unclassified | P1 | no | 100,084 | 52,598 | 14 | 919,043 | 40 | 0.376 | pass |

"validation level at" is the candidate count in the `validation level` line of summary.md; "real evals at that row" is column 2 of that log row.

## Full formula of every seed with test above 0.72

None (highest test 0.694). The shape check therefore has no case.

## Predictions against outcome (J_VORHERSAGE.md, committed in 92b6846 before any J run)

Research agent for j-share (j-lexicase numbers minus 0.05): at most 5 stuck (P = 0.50): met (0). Rule 2 in 13 or more (P = 0.35): no (11).
At least one above 0.85 (P = 0.45): no. 7 or more above 0.85 (P = 0.03): no. A seed above 0.90 (P = 0.02): no.
Executing agent:
8. at most 5 stuck (P = 0.45): met; rule 2 in 13 or more (P = 0.25): no; at least one above 0.85 under the conditions (P = 0.30): no.
9. projection at or below 40 h (P = 0.60): hit (22 h projected; actual 13.4 h).
10. no seed aborts (P = 0.90): hit.
11. JAX within 0.002 for every seed (P = 0.80): hit (0.0005).
