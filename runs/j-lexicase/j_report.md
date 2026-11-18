# j-lexicase (package J): results as measured

collision3, task seed 1, 96 + 48 train episodes, fixed readout, --recip --persist-m 3 --persist-init identity, add-node on,
--select lexicase --val-log --level-acc 0.651 --level-long 0.838, seeds 1-32, 1,500,000 candidates, --parallel 2 --threads 8 (batch 128),
commit 50c2d10, all seeds on epyc. Wall 57897 s (16.08 h). Baseline: the committed 32 seeds of runs/d-kalman (not rerun).
Facts only; the interpretation is left to the research agent.

## Counts against d-kalman

| tag | rule 2 | stuck below 0.53 | test > 0.85 with rule 2's other conditions | above 0.695 under those conditions | above 0.90 | median test | mean train - test | mean real evals | mean minutes | mean last pop_mean_acc |
|---|---|---|---|---|---|---|---|---|---|---|
| j-lexicase | 12/32 | 0/32 | 1/32 (6) | 5/32 (2, 6, 9, 12, 17) | 0/32 | 0.6815 | +0.0002 | 806,780 | 59.5 | 0.446 |
| d-kalman (32 seeds, baseline) | 6/32 | 12/32 | 1/32 (9) | 2/32 (7, 9) | 0/32 | 0.6300 | +0.0141 | 784,926 | 42.2 | 0.418 |

Fixed before the run (README, "Package J", thresholds of E): an effect is shown by rule 2 in 13/32 or more, by at most 5/32 stuck below
0.53, or by test > 0.85 under rule 2's other conditions in 7/32 or more. Outcome: rule 2 12/32 (not met), stuck 0/32 (met),
test > 0.85 1/32 (not met). Six looks in total over the two arms (README).
Rule 1, Mann-Whitney (two-sided) of the 32 test accuracies against the 32 of d-kalman: U = 848.0, p = 6.6e-06.
Validation level reached in 20/32 seeds. JAX against Rust on the dumped test data: largest difference 0.0006;
no seed flagged as diverged.

## Additional check by the executing agent: seed 6 (not in RUNBOOK.md)

Read off the formula of seed 6 (below), with r = k + P1·tanh(k) and u = norm(r) = r/|r|:
S' = -1.011·((S + v rᵀ) u uᵀ - (S + v rᵀ)) = 1.011·(S + v rᵀ)(I - u uᵀ). Because r = |r|·u, the write term v rᵀ(I - u uᵀ) is zero in exact
arithmetic, so S' = 1.011·S(I - u uᵀ), and S, which starts at zero, stays zero.
Measured with the unchanged interpreter of verify.py (build_step) on 20 dumped test episodes per write length, float32: largest entry of S at the
end of an episode median 1.0e-6 (max 1.7e-6); median norm of the readout S q 1.7e-6. verify.py counts a query only if the norm of the readout
is above 1e-6. For comparison, the same measurement gives 3.3 (S) and 4.9 (S q) for j-lexicase seed 2, and 2.1 and 1.5 for d-kalman seed 9.
So the accuracy of seed 6 (Rust 0.893, JAX 0.8934) is carried by values of about 1e-6 in S, of the size of float32 rounding residues;
argmax decoding ignores their scale (CLAUDE.md rule 3). A float64 run was tried with JAX_ENABLE_X64=1; verify.py stops with a type error in
that mode and was not changed. Without seed 6 the counts read: test > 0.85 0/31, above 0.695 4/31, rule 2 11/31.

## Per seed

| seed | train | collision3 test | JAX on dump | T64 K8 | T128 K8 | train - test | family | S' reads | 1/( in S' | validation level at (candidates) | real evals at that row | instr | real evals | min | last pop_mean_acc | rule 2 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | 0.684 | 0.684 | 0.6838 | 0.795 | 0.773 | +0.000 | unclassified | neither | no | 250,100 | 109,458 | 22 | 877,711 | 40 | 0.459 | - |
| 2 | 0.732 | 0.721 | 0.7209 | 0.869 | 0.881 | +0.011 | unclassified | P2 | no | 900,084 | 497,717 | 20 | 905,995 | 40 | 0.494 | pass |
| 3 | 0.654 | 0.659 | 0.6589 | 0.841 | 0.847 | -0.005 | unclassified | P2 | no | not reached | – | 10 | 723,988 | 21 | 0.458 | pass |
| 4 | 0.689 | 0.680 | 0.6797 | 0.842 | 0.851 | +0.009 | unclassified | neither | no | 500,084 | 266,449 | 20 | 889,341 | 101 | 0.424 | pass |
| 5 | 0.671 | 0.672 | 0.6715 | 0.820 | 0.813 | -0.001 | unclassified | P1,P2 | no | 700,020 | 333,893 | 16 | 771,730 | 47 | 0.454 | - |
| 6 | 0.909 | 0.893 | 0.8934 | 0.997 | 0.995 | +0.016 | unclassified | P1 | no | 300,020 | 158,369 | 24 | 1,106,960 | 80 | 0.544 | pass |
| 7 | 0.710 | 0.712 | 0.7114 | 0.745 | 0.713 | -0.002 | unclassified | P1 | no | 850,036 | 496,611 | 23 | 980,806 | 35 | 0.445 | - |
| 8 | 0.696 | 0.686 | 0.6855 | 0.805 | 0.815 | +0.010 | unclassified | P1,P2 | no | 600,052 | 312,019 | 15 | 769,600 | 57 | 0.482 | - |
| 9 | 0.729 | 0.720 | 0.7197 | 0.883 | 0.899 | +0.009 | unclassified | P2 | no | 100,084 | 39,055 | 20 | 958,140 | 81 | 0.470 | pass |
| 10 | 0.572 | 0.564 | 0.5644 | 0.547 | 0.510 | +0.008 | unclassified | P1,P2 | no | not reached | – | 13 | 737,686 | 57 | 0.351 | - |
| 11 | 0.636 | 0.642 | 0.6423 | 0.809 | 0.806 | -0.006 | unclassified | P2 | no | not reached | – | 13 | 643,819 | 39 | 0.422 | - |
| 12 | 0.697 | 0.704 | 0.7040 | 0.851 | 0.868 | -0.007 | unclassified | P2 | no | 950,004 | 399,973 | 20 | 747,347 | 25 | 0.452 | pass |
| 13 | 0.624 | 0.625 | 0.6248 | 0.803 | 0.791 | -0.001 | unclassified | P1,P2 | no | not reached | – | 14 | 792,477 | 44 | 0.404 | - |
| 14 | 0.626 | 0.643 | 0.6432 | 0.798 | 0.784 | -0.017 | unclassified | P1 | no | not reached | – | 12 | 625,440 | 57 | 0.419 | - |
| 15 | 0.681 | 0.690 | 0.6895 | 0.819 | 0.810 | -0.009 | unclassified | P1 | no | 350,068 | 157,617 | 18 | 837,117 | 69 | 0.420 | - |
| 16 | 0.683 | 0.681 | 0.6806 | 0.804 | 0.785 | +0.002 | unclassified | P1,P2 | no | not reached | – | 21 | 989,361 | 91 | 0.438 | - |
| 17 | 0.731 | 0.720 | 0.7204 | 0.864 | 0.873 | +0.011 | unclassified | P1,P2 | no | 450,036 | 197,425 | 18 | 838,382 | 58 | 0.505 | pass |
| 18 | 0.681 | 0.684 | 0.6845 | 0.792 | 0.796 | -0.003 | unclassified | P1 | no | not reached | – | 16 | 748,751 | 109 | 0.484 | - |
| 19 | 0.699 | 0.683 | 0.6828 | 0.721 | 0.694 | +0.016 | unclassified | P1,P2 | no | not reached | – | 20 | 878,838 | 51 | 0.408 | - |
| 20 | 0.622 | 0.629 | 0.6288 | 0.771 | 0.755 | -0.007 | unclassified | P2 | no | not reached | – | 12 | 772,833 | 40 | 0.455 | - |
| 21 | 0.690 | 0.700 | 0.6997 | 0.807 | 0.806 | -0.010 | unclassified | P1 | no | 350,068 | 163,802 | 20 | 860,919 | 150 | 0.450 | - |
| 22 | 0.653 | 0.666 | 0.6657 | 0.860 | 0.860 | -0.013 | unclassified | P1,P2 | no | 1,500,020 | 807,993 | 15 | 807,993 | 34 | 0.428 | pass |
| 23 | 0.700 | 0.687 | 0.6869 | 0.800 | 0.801 | +0.013 | unclassified | P2 | no | 300,020 | 132,636 | 17 | 816,485 | 88 | 0.495 | - |
| 24 | 0.667 | 0.677 | 0.6771 | 0.861 | 0.853 | -0.010 | unclassified | P2 | yes | 400,116 | 144,348 | 17 | 742,536 | 66 | 0.427 | pass |
| 25 | 0.681 | 0.658 | 0.6579 | 0.796 | 0.787 | +0.023 | unclassified | P2 | no | not reached | – | 20 | 881,324 | 59 | 0.459 | - |
| 26 | 0.600 | 0.609 | 0.6094 | 0.824 | 0.839 | -0.009 | unclassified | neither | no | not reached | – | 13 | 637,097 | 28 | 0.398 | - |
| 27 | 0.689 | 0.690 | 0.6897 | 0.817 | 0.812 | -0.001 | unclassified | P2 | no | 300,020 | 139,238 | 19 | 884,536 | 71 | 0.433 | - |
| 28 | 0.667 | 0.675 | 0.6752 | 0.862 | 0.878 | -0.008 | unclassified | P1 | no | 550,004 | 229,952 | 15 | 687,079 | 60 | 0.428 | pass |
| 29 | 0.649 | 0.648 | 0.6479 | 0.785 | 0.783 | +0.001 | unclassified | neither | no | not reached | – | 15 | 653,520 | 43 | 0.463 | - |
| 30 | 0.674 | 0.682 | 0.6823 | 0.863 | 0.884 | -0.008 | unclassified | P1,P2 | no | 550,004 | 237,071 | 17 | 712,791 | 69 | 0.418 | pass |
| 31 | 0.684 | 0.670 | 0.6698 | 0.772 | 0.792 | +0.014 | unclassified | P1,P2 | no | 100,084 | 36,270 | 15 | 818,102 | 46 | 0.448 | - |
| 32 | 0.668 | 0.686 | 0.6863 | 0.859 | 0.875 | -0.018 | unclassified | P1 | no | 750,068 | 311,933 | 15 | 718,260 | 45 | 0.431 | pass |

"validation level at" is the candidate count in the `validation level` line of summary.md; "real evals at that row" is column 2 of that log row.

## Full formula of every seed with test above 0.72

seed 2 (test 0.721, train 0.732, T64 K8 0.869, T128 K8 0.881; structure [a=1.070 b=0.906 c=-0.963 g=-0.000, erase c/a=0.900, R²=0.7945, 1408 steps]; 20 instructions):

    S'  = (σ(2.247)·((v + P2·k))⊗((k - 0)) - P2)
    P1' = ((σ(2.247)·((v + P2·k))⊗((k - 0)) - P2) + ((1.163 + 2.247)·(v)⊗(1.163·((k - 0) + k)) + (P2 + P1)))
    P2' = (σ(1.163)·((1.163 + 2.247)·(v)⊗(1.163·((k - 0) + k)) + (P2 + P1)) - ((σ(2.247)·((v + P2·k))⊗((k - 0)) - P2) + ((1.163 + 2.247)·(v)⊗(1.163·((k - 0) + k)) + (P2 + P1))))

seed 6 (test 0.893, train 0.909, T64 K8 0.997, T128 K8 0.995; structure [a=0.000 b=0.000 c=0.000 g=0.000, erase c/a=0.000, R²=0.1052, 1408 steps]; 24 instructions):

    S'  = -1.011·((((v)⊗((k + P1·tanh(k))) + S))((norm(norm((k + P1·tanh(k)))))⊗(norm((k + P1·tanh(k))))) - ((v)⊗((k + P1·tanh(k))) + S))
    P1' = (σ(1/(0.199))·P1 - |σ(0.199·2.148)·(k + P1·tanh(k))|·|σ(0.199·2.148)·(k + P1·tanh(k))|·(norm(norm((k + P1·tanh(k)))))⊗(norm((k + P1·tanh(k)))))
    P2' = |σ(0.199·2.148)·(k + P1·tanh(k))|·|σ(0.199·2.148)·(k + P1·tanh(k))|·(norm(norm((k + P1·tanh(k)))))⊗(norm((k + P1·tanh(k))))

Read off the formulas only.
- Seed 2: S' = σ(2.247)·(v + P2 k) kᵀ - P2; the memory is carried in P2 and P1, and the address of every write is k (or 2.33·k). No address
  is computed from a persistent register, there is no reciprocal and no gain of the form P k / (c + kᵀP k).
- Seed 6: the address is r = k + P1·tanh(k), computed from the persistent register P1, and the writes go along r and u = norm(r)
  (P1' = σ(1/0.199)·P1 - |σ(0.427)·r|²·u uᵀ, P2' = |σ(0.427)·r|²·u uᵀ). So it has an address taken from a persistent register, as in seed 9,
  and no gain of the form P k / (c + kᵀP k). Its write into S cancels exactly, see the additional check above.

## Predictions against outcome (J_VORHERSAGE.md, committed in 92b6846 before any J run)

Research agent: at most 5 stuck (P = 0.55): met (0). Rule 2 in 13 or more (P = 0.40): no (12). At least one above 0.85 (P = 0.50): yes,
seed 6 (see the additional check). 7 or more above 0.85 (P = 0.08): no. A seed above 0.90 (P = 0.07): no.
Executing agent:
1. at most 5 stuck (P = 0.50): met.
2. rule 2 in 13 or more (P = 0.30): no.
3. at least one seed above 0.85 under the conditions (P = 0.35): yes (seed 6); seven or more (P = 0.04): no.
4. a seed above 0.90 (P = 0.04): no.
5. median at least 0.02 above 0.630 (P = 0.55): yes (0.681); Mann-Whitney p < 0.05 (P = 0.40): yes.
6. seed-9 shape or Kalman gain in a seed above 0.72 (P = 0.25): seed 6 has an address from a persistent register; no Kalman gain.
7. projection at or below 40 h (P = 0.85): hit (13 h projected; actual 16.1 h).
10. no seed aborts (P = 0.90): hit.
11. JAX within 0.002 for every seed (P = 0.80): hit (0.0006).
