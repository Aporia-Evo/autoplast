# c-m2 (package C, arm C1): results as measured

Tag c-m2: collision3, task seed 1, 96 + 48 train episodes, 19 ops, fixed readout, --persist-m 2, add-node on, seeds 1-16,
1,500,000 candidates, --parallel 2 --threads 8 (batch 128), commit 21e513a, workstation. Total wall 16431 s (4.56 h).
Control: committed runs/5a-A (not rerun). Facts only; the interpretation is left to the research agent.

| seed | train | collision3 test | JAX on dump | T128 K8 | train - test | family (structural) | P1' line | S' reads P1 | rule 2 | minutes |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | 0.651 | 0.661 | 0.6614 | 0.799 | -0.010 | unclassified | no | no | - | 27.0 |
| 2 | 0.683 | 0.695 | 0.6949 | 0.861 | -0.012 | unclassified | yes | yes | pass | 73.4 |
| 3 | 0.512 | 0.515 | 0.5150 | 0.545 | -0.003 | unclassified | yes | no | - | 18.4 |
| 4 | 0.512 | 0.517 | 0.5175 | 0.553 | -0.005 | decayed linear attention | no | no | - | 24.2 |
| 5 | 0.626 | 0.638 | 0.6380 | 0.787 | -0.012 | unclassified | yes | no | - | 26.8 |
| 6 | 0.641 | 0.655 | 0.6546 | 0.848 | -0.014 | unclassified | yes | yes | pass | 83.4 |
| 7 | 0.512 | 0.515 | 0.5150 | 0.545 | -0.003 | unclassified | yes | no | - | 15.7 |
| 8 | 0.510 | 0.514 | 0.5139 | 0.547 | -0.004 | decayed linear attention | yes | no | - | 20.2 |
| 9 | 0.667 | 0.679 | 0.6786 | 0.885 | -0.012 | unclassified | yes | yes | pass | 62.3 |
| 10 | 0.514 | 0.513 | 0.5135 | 0.551 | +0.001 | unclassified | yes | yes | - | 29.8 |
| 11 | 0.619 | 0.637 | 0.6366 | 0.840 | -0.018 | delta rule | yes | yes | - | 12.4 |
| 12 | 0.627 | 0.640 | 0.6399 | 0.844 | -0.013 | delta rule | yes | yes | - | 28.1 |
| 13 | 0.623 | 0.638 | 0.6376 | 0.769 | -0.015 | unclassified | yes | no | - | 32.4 |
| 14 | 0.515 | 0.515 | 0.5153 | 0.550 | +0.000 | unclassified | yes | yes | - | 48.4 |
| 15 | 0.512 | 0.515 | 0.5150 | 0.545 | -0.003 | unclassified | no | no | - | 15.3 |
| 16 | 0.621 | 0.630 | 0.6300 | 0.749 | -0.009 | unclassified | yes | yes | - | 27.0 |

"P1' line" is the criterion named in RUNBOOK.md. "S' reads P1" says whether the printed S' formula contains P1; a P1' line with
"no" there means the second state is written but never reaches S.

## Decision rules (as in 5a, unchanged)

- Rule 1, Mann-Whitney (two-sided) of the 16 collision3 test accuracies against runs/5a-A: U = 154.5, p = 0.326.
  Median 0.6335 (c-m2) vs 0.517 (5a-A). Not significant.
- Rule 2 (test > 0.651 AND T128 K8 >= 0.838 AND train - test <= 0.03): 3 of 16 seeds pass: 2, 6, 9. (5a-A: 0 of 16.)
- Above the hand-written probe (test > 0.679) with the other two conditions of rule 2: 1 seed (2).
  Seed 9 scores 0.679, equal to the probe, not above it.
- JAX against Rust on the dumped test data (verify_dump.txt): largest difference 0.0005.

The ± in summary.md counts queries only (about 0.006 here); the spread over draws of the embeddings is larger (README, package B check).
Only one task draw (task seed 1) was used, as in 5a-A.

## Formulas of the seeds that pass rule 2

seed 2 (test 0.695, T128 K8 0.861, structure [a=1.009 b=0.149 c=-0.963 g=0.000, erase c/a=0.955, R²=0.4450, 1408 steps]):

    S' = ((1.114·1.114·1.114·(-0.889·(0 - (P1 + (v)⊗(k))) - ((P1 + (v)⊗(k))·k)⊗(k)) + 1.114·1.114·1.114·(-0.889·(0 - (P1 + (v)⊗(k))) - ((P1 + (v)⊗(k))·k)⊗(k))) + (-0.889·(0 - (P1 + (v)⊗(k))) - 0.391·1.114·((P1 + (v)⊗(k))·k)⊗(k)))
    P1' = 1.114·(-0.889·(0 - (P1 + (v)⊗(k))) - 0.391·1.114·((P1 + (v)⊗(k))·k)⊗(k))

seed 6 (test 0.655, T128 K8 0.848, structure [a=1.002 b=3.273 c=-0.364 g=0.004, erase c/a=0.363, R²=0.7772, 1408 steps]):

    S' = (((tanh(v))⊗(k) - P1) - ((((tanh(v))⊗(k) + (P1 + (tanh(v))⊗(k))))((tanh(tanh(tanh(k))))⊗((0 - tanh(tanh(tanh(tanh(k))))))) - ((tanh(v))⊗(k) - P1)))
    P1' = ((((tanh(v))⊗(k) + (P1 + (tanh(v))⊗(k))))((tanh(tanh(tanh(k))))⊗((0 - tanh(tanh(tanh(tanh(k))))))) - ((tanh(v))⊗(k) - P1))

seed 9 (test 0.679, T128 K8 0.885, structure [a=1.040 b=0.354 c=-0.815 g=0.001, erase c/a=0.783, R²=0.5593, 1408 steps]):

    S' = ((0.888·(v)⊗(k) + (0.888·0.888·(v)⊗(k) + (S + (P1)ᵀ))) - ((0.888·(v)⊗(k) + (0.888·0.888·(v)⊗(k) + (S + (P1)ᵀ))))(((0.888·(v)⊗(k))ᵀ)(0.888·(v)⊗(k))))
    P1' = (0.888·(v)⊗(k))ᵀ

## Predictions (C_VORHERSAGE.md, committed in 1b82762 before any run) against outcome

1. time-c 0.3 to 2 min per seed: missed (1.9 and 3.3 min).
2. projection below 24 h: hit.
3. C1 wall 1.5 to 6 h: hit (4.56 h).
4. P1' line in 2 to 8 seeds: missed (13 of 16; S' reads P1 in 8 of 16).
5. Rule 1 significant (P = 0.25): not significant.
6. At least one seed passes rule 2 (P = 0.25): yes, 3 seeds.
7. At least one seed above the probe under rule 2 (P = 0.12): yes, seed 2.
8. Median within 0.03 of 0.517: missed (0.6335).
9. Two-mode split repeats: hit (7 seeds at 0.513 to 0.517, 9 seeds at 0.630 to 0.695).
10. JAX within 0.002: hit.
