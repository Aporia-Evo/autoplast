# g-tune8 (package G): results as measured

collision3, task seed 1, 96 + 48 train episodes, fixed readout, --recip --persist-m 3 --persist-init identity, add-node on,
--tune-consts 8 --val-log --level-acc 0.651 --level-long 0.838, seeds 1-32, 1,500,000 candidates, --parallel 2 --threads 8 (batch 128),
commit ad31161, all seeds on epyc. Wall 43041 s (11.96 h). Baseline: the committed 32 seeds of runs/d-kalman (not rerun).
Facts only; the interpretation is left to the research agent.

## Counts against d-kalman

| tag | main count (test > 0.85, T128 K8 >= 0.838, train - test <= 0.03) | above 0.695 under rule 2's other conditions | rule 2 | below 0.53 | median test | mean train - test | mean real evals | mean minutes | S' reads P1 / P2 / reciprocal |
|---|---|---|---|---|---|---|---|---|---|
| g-tune8 | 0/32 (none) | 3/32 (3, 9, 25) | 6/32 (3, 9, 10, 15, 25, 30) | 11/32 | 0.6395 | -0.0024 | 991,670 | 44.3 | 12 / 13 / 5 |
| d-kalman (32 seeds, baseline) | 1/32 (9) | 2/32 (7, 9) | 6/32 (2, 7, 9, 15, 24, 25) | 12/32 | 0.6300 | +0.0141 | 784,926 | 42.2 | 15 / 25 / 2 |

Fixed before the run (README, "Package G"): the arm shows an effect with rule 2 in 13/32 or more, at most 5/32 below 0.53, or test > 0.85
in 7/32 or more. Outcome: rule 2 6/32, below 0.53 11/32, test > 0.85 0/32. None of the three is met.
Rule 1, Mann-Whitney (two-sided) of the 32 test accuracies against the 32 of d-kalman: U = 564.0, p = 0.489.
Validation level (val > 0.651, T128 K8 on validation >= 0.838, train - val <= 0.03, checked every 50,000 candidates) reached in
7/32 seeds (3, 4, 9, 10, 15, 25, 30); d-kalman summaries predate this line.
JAX against Rust on the dumped test data (verify_dump.txt): largest difference 0.0005; no seed flagged as diverged.

## Per seed

| seed | train | collision3 test | JAX on dump | T64 K8 | T128 K8 | train - test | family | S' reads | 1/( in S' | instr | last best_acc gain at | validation level reached at | rule 2 | real evals | min |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | 0.624 | 0.641 | 0.6408 | 0.824 | 0.803 | -0.017 | delta rule | neither | no | 13 | 950,188 | not reached | - | 852,910 | 47 |
| 2 | 0.608 | 0.618 | 0.6182 | 0.739 | 0.695 | -0.010 | unclassified | P1 | no | 12 | 650,292 | not reached | - | 992,287 | 55 |
| 3 | 0.728 | 0.724 | 0.7238 | 0.873 | 0.880 | +0.004 | unclassified | P1,P2 | no | 19 | 250,252 | 200020 candidates | pass | 1,183,806 | 81 |
| 4 | 0.691 | 0.697 | 0.6972 | 0.805 | 0.791 | -0.006 | unclassified | P1,P2 | yes | 18 | 1,100,020 | 1000100 candidates | - | 1,094,062 | 50 |
| 5 | 0.517 | 0.503 | 0.5032 | 0.551 | 0.544 | +0.014 | unclassified | neither | no | 13 | 1,050,052 | not reached | - | 796,488 | 32 |
| 6 | 0.641 | 0.645 | 0.6451 | 0.775 | 0.714 | -0.004 | unclassified | P2 | no | 17 | 1,200,124 | not reached | - | 1,056,448 | 73 |
| 7 | 0.624 | 0.628 | 0.6285 | 0.784 | 0.770 | -0.004 | unclassified | P1 | no | 10 | 1,200,148 | not reached | - | 942,980 | 42 |
| 8 | 0.628 | 0.639 | 0.6391 | 0.808 | 0.764 | -0.011 | unclassified | neither | yes | 16 | 400,236 | not reached | - | 1,031,817 | 86 |
| 9 | 0.729 | 0.713 | 0.7134 | 0.832 | 0.845 | +0.016 | unclassified | P1 | no | 22 | 1,350,108 | 1000172 candidates | pass | 1,126,434 | 41 |
| 10 | 0.667 | 0.674 | 0.6745 | 0.866 | 0.891 | -0.007 | unclassified | P1,P2 | no | 14 | 900,084 | 450244 candidates | pass | 1,129,701 | 47 |
| 11 | 0.510 | 0.509 | 0.5093 | 0.573 | 0.542 | +0.001 | unclassified | neither | no | 7 | 400,276 | not reached | - | 857,483 | 24 |
| 12 | 0.637 | 0.634 | 0.6342 | 0.821 | 0.798 | +0.003 | unclassified | P2 | no | 17 | 1,500,196 | not reached | - | 1,101,172 | 31 |
| 13 | 0.514 | 0.517 | 0.5175 | 0.579 | 0.551 | -0.003 | unclassified | P1 | yes | 15 | 1,050,196 | not reached | - | 968,988 | 38 |
| 14 | 0.686 | 0.692 | 0.6924 | 0.820 | 0.807 | -0.006 | unclassified | P2 | yes | 17 | 1,500,204 | not reached | - | 1,165,076 | 78 |
| 15 | 0.675 | 0.684 | 0.6835 | 0.865 | 0.874 | -0.009 | unclassified | neither | no | 17 | 1,400,340 | 1050140 candidates | pass | 1,113,521 | 58 |
| 16 | 0.514 | 0.514 | 0.5138 | 0.572 | 0.545 | +0.000 | unclassified | P2 | no | 11 | 700,148 | not reached | - | 1,024,689 | 36 |
| 17 | 0.631 | 0.645 | 0.6452 | 0.780 | 0.757 | -0.014 | delta + Kronecker mix | neither | no | 17 | 850,156 | not reached | - | 1,041,317 | 36 |
| 18 | 0.511 | 0.512 | 0.5118 | 0.575 | 0.544 | -0.001 | unclassified | neither | no | 14 | 1,450,036 | not reached | - | 816,348 | 26 |
| 19 | 0.514 | 0.514 | 0.5139 | 0.572 | 0.547 | +0.000 | unclassified | neither | no | 12 | 100,180 | not reached | - | 935,767 | 31 |
| 20 | 0.657 | 0.668 | 0.6682 | 0.818 | 0.809 | -0.011 | unclassified | P2 | no | 18 | 1,000,140 | not reached | - | 1,064,068 | 45 |
| 21 | 0.521 | 0.511 | 0.5108 | 0.578 | 0.548 | +0.010 | unclassified | neither | no | 13 | 50,140 | not reached | - | 1,005,579 | 34 |
| 22 | 0.633 | 0.640 | 0.6396 | 0.819 | 0.802 | -0.007 | unclassified | P1,P2 | no | 16 | 850,340 | not reached | - | 1,176,305 | 63 |
| 23 | 0.521 | 0.507 | 0.5068 | 0.579 | 0.538 | +0.014 | unclassified | P2 | no | 20 | 750,196 | not reached | - | 1,194,013 | 51 |
| 24 | 0.509 | 0.516 | 0.5162 | 0.583 | 0.550 | -0.007 | decayed linear attention | neither | no | 6 | 100,100 | not reached | - | 568,024 | 17 |
| 25 | 0.730 | 0.721 | 0.7211 | 0.865 | 0.882 | +0.009 | unclassified | P1 | no | 20 | 600,100 | 150124 candidates | pass | 1,161,031 | 42 |
| 26 | 0.653 | 0.650 | 0.6495 | 0.788 | 0.765 | +0.003 | unclassified | P1 | no | 14 | 1,000,132 | not reached | - | 957,486 | 42 |
| 27 | 0.510 | 0.509 | 0.5093 | 0.573 | 0.542 | +0.001 | unclassified | neither | no | 6 | 50,132 | not reached | - | 689,184 | 20 |
| 28 | 0.631 | 0.636 | 0.6360 | 0.847 | 0.845 | -0.005 | unclassified | P1 | no | 16 | 1,500,212 | not reached | - | 918,325 | 45 |
| 29 | 0.636 | 0.649 | 0.6491 | 0.771 | 0.764 | -0.013 | unclassified | neither | no | 12 | 1,450,068 | not reached | - | 735,932 | 27 |
| 30 | 0.686 | 0.694 | 0.6935 | 0.839 | 0.853 | -0.008 | unclassified | P2 | yes | 13 | 950,028 | 350180 candidates | pass | 934,166 | 54 |
| 31 | 0.515 | 0.517 | 0.5165 | 0.582 | 0.554 | -0.002 | unclassified | P2 | no | 13 | 900,004 | not reached | - | 1,021,375 | 31 |
| 32 | 0.649 | 0.655 | 0.6546 | 0.828 | 0.822 | -0.006 | unclassified | P1,P2 | no | 14 | 100,044 | not reached | - | 1,076,658 | 33 |

"validation level reached at" is the candidate count in the `validation level` line of summary.md. "last best_acc gain at" is the last
row of log.csv where best_acc rose.

## Full formula of every seed with test above 0.72

seed 3 (test 0.724, train 0.728, T64 K8 0.873, T128 K8 0.880; structure [a=1.071 b=7.613 c=-0.909 g=-0.001, erase c/a=0.849, R²=0.8220, 1408 steps]; 19 instructions):

    S'  = ((((P1 + P2) + S) + (-0.906·((P1 + P2) + S))((k)⊗(tanh(k)))) + ((((tanh(v) + tanh(v)) + (tanh(v) + tanh(v))) + ((tanh(v) + tanh(v)) + (tanh(v) + tanh(v)))))⊗(k))
    P1' = (((((tanh(v) + tanh(v)) + (tanh(v) + tanh(v))) + ((tanh(v) + tanh(v)) + (tanh(v) + tanh(v)))))⊗(k) + σ(σ(|tanh(v)|))·P1)
    P2' = σ(σ(|tanh(v)|))·P1

seed 25 (test 0.721, train 0.730, T64 K8 0.865, T128 K8 0.882; structure [a=1.073 b=8.012 c=-0.961 g=-0.000, erase c/a=0.896, R²=0.8188, 1408 steps]; 20 instructions):

    S'  = ((S + P1) - (((S + P1)·tanh(tanh(k)) - (((v + v) + (v + v)) - ((tanh(tanh(k)) ⊙ (v + v)) - ((v + v) + (v + v))))))⊗(norm(tanh(k))))
    P1' = σ(1.148)·(P1 + ((((v + v) + (v + v)) + ((((v + v) + (v + v)) - ((tanh(tanh(k)) ⊙ (v + v)) - ((v + v) + (v + v)))) + (((v + v) + (v + v)) - ((tanh(tanh(k)) ⊙ (v + v)) - ((v + v) + (v + v)))))))⊗(norm(tanh(k))))
    P2' = (((S + P1)·tanh(tanh(k)) - (((v + v) + (v + v)) - ((tanh(tanh(k)) ⊙ (v + v)) - ((v + v) + (v + v))))))⊗(norm(tanh(k)))

Shape of seed 9 (README, "What seed 9 is": an address such as norm(P1ᵀ k) taken from a persistent register and a write along that address):
read off the formulas only. In seed 3 the writes use k as address (v-term ⊗ k into P1 and S, erase along k ⊗ tanh(k)); P1 is a
decayed sum of 8·tanh(v) kᵀ and P2 a scaled copy of P1; no address is computed from a persistent register. In seed 25 the writes use
norm(tanh(k)) as address (error term ⊗ norm(tanh k) into S + P1, value term ⊗ norm(tanh k) into P1 with decay σ(1.148)); no address
is computed from a persistent register. Neither formula has the shape of seed 9.

## Predictions against outcome

Research agent (README, "Package G"): rule 2 in 5 to 10 of 32 (P = 0.6): hit (6). 13 or more (P = 0.12): no. At least one seed above 0.85 (P = 0.45): no.
Executing agent (G_VORHERSAGE.md, committed in f72bd0f before any G run):
1. rule 2 in 5 to 10 of 32 (P = 0.55): hit (6); 13 or more (P = 0.12): no.
2. at least one seed above 0.85 under rule 2's other conditions (P = 0.40): no; seven or more (P = 0.04): no.
3. at most 5 of 32 below 0.53 (P = 0.15): no (11).
4. effect by any of the three criteria (P = 0.22): no.
5. at least one seed with the shape of seed 9 (P = 0.30): no.
6. mean train - test above the d-kalman mean by more than 0.01 (P = 0.20): no (-0.0024 against +0.0141).
7. projection from time-g at or below 30 h (P = 0.60): hit (18.8 h; actual 12.0 h).
8. JAX within 0.002 for every seed not flagged as diverged (P = 0.80): hit (0.0005).
