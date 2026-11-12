# d-kalman (package D): results as measured

Tag d-kalman: collision3, task seed 1, 96 + 48 train episodes, fixed readout, --recip --persist-m 3 --persist-init identity,
add-node on, seeds 1-16, 1,500,000 candidates, --parallel 2 --threads 8 (batch 128), commit e979a8e, all seeds on epyc.
Total wall 22069 s (6.13 h). Controls runs/5a-A and runs/c-m2 (not rerun). Facts only; the interpretation is left to the research agent.

| seed | train | collision3 test | JAX on dump | T64 K8 | T128 K8 | train - test | family | S' reads | 1/( in S' | last best_acc gain at | rule 2 | minutes |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | 0.517 | 0.520 | 0.5198 | 0.584 | 0.553 | -0.003 | decayed linear attention | P2 | no | 200,052 | - | 61 |
| 2 | 0.676 | 0.684 | 0.6835 | 0.847 | 0.851 | -0.008 | unclassified | P1,P2 | no | 750,068 | pass | 59 |
| 3 | 0.631 | 0.639 | 0.6392 | 0.827 | 0.818 | -0.008 | unclassified | P2 | no | 650,100 | - | 85 |
| 4 | 0.627 | 0.631 | 0.6308 | 0.776 | 0.761 | -0.004 | unclassified | P1 | no | 1,200,116 | - | 35 |
| 5 | 0.626 | 0.641 | 0.6412 | 0.795 | 0.781 | -0.015 | unclassified | P2 | no | 1,000,052 | - | 21 |
| 6 | 0.622 | 0.629 | 0.6289 | 0.793 | 0.787 | -0.007 | unclassified | P1,P2 | no | 900,084 | - | 89 |
| 7 | 0.726 | 0.713 | 0.7131 | 0.849 | 0.851 | +0.013 | unclassified | P2 | yes | 1,300,084 | pass | 26 |
| 8 | 0.510 | 0.509 | 0.5095 | 0.574 | 0.543 | +0.001 | unclassified | neither | no | 550,004 | - | 17 |
| 9 | 0.863 | 0.855 | 0.8551 | 0.940 | 0.885 | +0.008 | unclassified | P1,P2 | no | 1,250,036 | pass | 40 |
| 10 | 0.644 | 0.644 | 0.6437 | 0.731 | 0.726 | +0.000 | unclassified | P1,P2 | no | 150,004 | - | 107 |
| 11 | 0.518 | 0.515 | 0.5147 | 0.565 | 0.558 | +0.003 | unclassified | P1 | no | 200,052 | - | 21 |
| 12 | 0.648 | 0.653 | 0.6531 | 0.827 | 0.819 | -0.005 | unclassified | P2 | no | 900,084 | - | 35 |
| 13 | 0.577 | 0.588 | 0.5876 | 0.627 | 0.619 | -0.011 | unclassified | P1 | no | 1,500,020 | - | 35 |
| 14 | 0.523 | 0.507 | 0.5075 | 0.553 | 0.538 | +0.016 | unclassified | P1,P2 | no | 800,116 | - | 31 |
| 15 | 0.656 | 0.663 | 0.6631 | 0.858 | 0.860 | -0.007 | unclassified | P1,P2 | no | 1,100,020 | pass | 34 |
| 16 | 0.635 | 0.636 | 0.6360 | 0.822 | 0.793 | -0.001 | unclassified | P2 | no | 750,068 | - | 24 |

"last best_acc gain at" is the candidate count of the last row in log.csv where best_acc rose (the logs hold train accuracy, see RUNBOOK).
Counts: S' reads P1 in 9 of 16 seeds, P2 in 12 of 16; S' contains a reciprocal in 1 of 16 (seed 7).

## Numbers asked for in RUNBOOK.md, package D

- Main count (test > 0.85 AND T128 K8 >= 0.838 AND train - test <= 0.03): 1 of 16, seed 9 (test 0.855, T128 K8 0.885, train - test +0.008).
- Seeds above 0.695 (best rule of C1): 2 (seeds 7 and 9), both also meet the other two conditions of rule 2.
- Rule 2 (test > 0.651 AND T128 K8 >= 0.838 AND train - test <= 0.03): 4 of 16 pass: 2, 7, 9, 15.
- Rule 1, Mann-Whitney (two-sided) of the 16 test accuracies:
  against c-m2: U = 149.0, p = 0.439; against 5a-A: U = 172.5, p = 0.097. Neither significant.
  Medians: d-kalman 0.6375, c-m2 0.6335, 5a-A 0.517.
- JAX against Rust on the dumped test data (verify_dump.txt, dump made with the epyc binary): largest difference 0.0005.

The ± in summary.md counts queries only; one task draw (task seed 1) was used, as in 5a-A and c-m2.

## Full formula of every seed with test above 0.72

seed 9 (test 0.855, train 0.863, T64 K8 0.940, T128 K8 0.885; structure [a=0.817 b=3.724 c=-0.024 g=-0.000, erase c/a=0.030, R²=0.4273, 1408 steps]; effective program 22 instructions):

    S'  = ((P2 + ((((norm(tanh(v)) + norm(tanh(v))) + (norm(tanh(v)) + norm(tanh(v)))) + (norm(tanh(v)) + norm(tanh(v)))))⊗(norm(σ(0)·σ(0)·(P1)ᵀ·k))) - (P1 - (P1·<norm(σ(0)·σ(0)·(P1)ᵀ·k), norm(σ(0)·σ(0)·(P1)ᵀ·k)>·k)⊗(norm(σ(0)·σ(0)·(P1)ᵀ·k))))
    P1' = (P1 - (P1·<norm(σ(0)·σ(0)·(P1)ᵀ·k), norm(σ(0)·σ(0)·(P1)ᵀ·k)>·k)⊗(norm(σ(0)·σ(0)·(P1)ᵀ·k)))
    P2' = σ(1.390)·(P2 + ((((norm(tanh(v)) + norm(tanh(v))) + (norm(tanh(v)) + norm(tanh(v)))) + (norm(tanh(v)) + norm(tanh(v)))))⊗(norm(σ(0)·σ(0)·(P1)ᵀ·k)))

Read off the formula, without interpretation: with u = norm(P1ᵀ k) (the factor σ(0)² cancels in norm, and <u, u> = 1 whenever P1ᵀk ≠ 0),
P1' = P1 − (P1 k) uᵀ with P1 starting at the identity, P2' = σ(1.390)·(P2 + 6·norm(tanh v) uᵀ), and S' = P2'/σ(1.390) − P1'.
S' does not read S. There is no reciprocal and no error term (v − S k) in the rule. Train accuracy stayed at 0.711 from 600,052 to
1,200,116 candidates and rose to 0.863 at 1,250,036 (log.csv).

Seed 7 (test 0.713) is the only rule with a reciprocal; it is below 0.72, its formula is in seed7/summary.md.

## Predictions against outcome

Research agent (README, "Package D"): main count 0 with P = 0.85: missed (1). At least one seed above 0.695 with P = 0.6: hit (2).
Executing agent (D_VORHERSAGE.md, committed in 1a4dd1b before any run):
1. time-d 2 to 8 min per seed: missed (1.8 and 3.3 min).
2. projection below 24 h: hit.
3. main count 0 (P = 0.85): missed (1).
4. at least one seed above 0.695 under rule 2's other conditions (P = 0.45): hit (seeds 7, 9).
5. at least one seed passes rule 2 (P = 0.55): hit (4).
6. rule 1 significant against c-m2 (P = 0.15) / against 5a-A (P = 0.25): neither (p = 0.44 / 0.097).
7. reciprocal in S' in at least 4 seeds (P = 0.50): missed (1).
8. S' reads P2 in at least 3 seeds (P = 0.40): hit (12).
9. at least one seed at 0.000 on T128 K8 (P = 0.40): missed (none).
10. JAX within 0.002 (P = 0.75): hit.
11. two-mode split repeats (P = 0.55): hit with one seed between: seeds 1, 8, 11, 14 at 0.507 to 0.520, seed 13 at 0.588, the rest 0.629 to 0.855.
