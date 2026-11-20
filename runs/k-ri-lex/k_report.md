# k-ri-lex (package K, arm 1): results as measured

collision3, task seed 1, 96 + 48 train episodes, fixed readout, --recip --persist-m 3 --persist-init identity, add-node on,
--select lexicase --residual-insert --val-log --level-acc 0.651 --level-long 0.838, seeds 1-32, 1,500,000 candidates, --parallel 2 --threads 8 (batch 128),
commit 6c2f60a (contains "Corrected 19 Nov"), all seeds on epyc. Summary line: `search: regularized evolution  tune-consts: 0  select: lexicase  residual-insert: on`.
Wall of the complete run 63244 s (17.57 h), started 2026-11-19T20:33:59Z. Two earlier starts of the same command were killed with the hub server
after about 10 minutes (see WHERE.md; kept in aborted1/ and aborted2/); no seed of the complete run failed or was rerun.
Baselines: the committed 32 seeds of runs/j-lexicase and runs/d-kalman (not rerun). Facts only; the interpretation is left to the research agent.

## Counts against j-lexicase and d-kalman

"under the conditions" = T128 K8 >= 0.838 and train - test <= 0.03 (rule 2's other conditions). "stuck" = collision3 test below 0.53.

| tag | rule 2 | stuck below 0.53 | test > 0.85 under the conditions | above 0.695 under the conditions | above 0.90 under the conditions | median test | mean train - test | mean real evals | mean minutes | mean last pop_mean_acc | validation level reached |
|---|---|---|---|---|---|---|---|---|---|---|---|
| k-ri-lex | 11/32 (1, 3, 5, 7, 8, 10, 11, 15, 16, 18, 21) | 0/32 | 0/32 | 7/32 (1, 3, 7, 15, 16, 18, 21) | 0/32 | 0.6765 | +0.0064 | 939,286 | 63.7 | 0.457 | 21/32 |
| j-lexicase (baseline) | 12/32 (2, 3, 4, 6, 9, 12, 17, 22, 24, 28, 30, 32) | 0/32 | 1/32 (6) | 5/32 (2, 6, 9, 12, 17) | 0/32 | 0.6815 | +0.0002 | 806,780 | 59.5 | 0.446 | 20/32 |
| d-kalman (baseline) | 6/32 (2, 7, 9, 15, 24, 25) | 12/32 (1, 8, 11, 14, 18, 19, 20, 21, 22, 23, 26, 29) | 1/32 (9) | 2/32 (7, 9) | 0/32 | 0.6300 | +0.0141 | 784,926 | 42.2 | 0.418 | 0/32 |

The j-lexicase row counts seed 6 as Rust scores it; README records it as a scale artefact (it drops to 0.0000 under the epsilon check, see below).
d-kalman ran without --val-log, so it has no validation level.

Rule 1, Mann-Whitney (two-sided) of the 32 test accuracies against j-lexicase: U = 536.5, p = 0.747.
Against d-kalman: U = 882.0, p = 7.0e-07.
Main count fixed in README (test > 0.90 under the conditions, passing the epsilon check, in 2 or more seeds): 0/32. Seeds above 0.90: 0. Seeds above 0.85: 0.
Best test: seed 16 at 0.726.

## JAX and epsilon check

Dump made with the epyc binary (`autoplast dump --regime collision3 --split test`), checked on the workstation, then deleted on both machines.
- `verify.py --task-json` (float32, Normalize epsilon 1e-6 as in Rust): largest difference to Rust 0.0005; no seed flagged as diverged. -> verify_dump.txt
- `verify.py --x64 --norm-eps 1e-9 --task-json`: the correct count is identical to the float32 run for all 32 seeds (largest change 0.0000), so no
  seed moves by more than 0.02 and `verify/eps_scale.py` was not needed. -> verify_eps_x64.txt
- Extra check by the executing agent (not in RUNBOOK): the same epsilon command on runs/j-lexicase/seed6/best.json with this dump gives
  0.0000 (0/6503) against 0.8934 in float32, so the check does detect the known case.

## Residual insertion

Per seed below: attempts, blocks inserted, and the number of times dead instructions were removed first (the summary line `residual insert: ...`).
Inserted / attempts: median 0.73, range 0.31 to 0.84. Attempts per seed 355,846 to 357,932.

## Per seed

| seed | train | collision3 test | JAX on dump | T64 K8 | T128 K8 | train - test | family | S' reads | 1/( in S' | validation level at (candidates) | real evals at that row | instr | real evals | min | last pop_mean_acc | residual insert: attempts | blocks inserted | dead code removed first | rule 2 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | 0.735 | 0.721 | 0.7209 | 0.869 | 0.878 | +0.014 | unclassified | P1 | no | 150,004 | 75,295 | 23 | 1,067,790 | 49 | 0.423 | 356,412 | 114,683 | 122,596 | pass |
| 2 | 0.676 | 0.668 | 0.6677 | 0.825 | 0.812 | +0.008 | unclassified | P1,P2 | no | 50,036 | 30,468 | 16 | 956,204 | 46 | 0.470 | 357,156 | 262,109 | 279,807 | - |
| 3 | 0.734 | 0.719 | 0.7189 | 0.871 | 0.881 | +0.015 | unclassified | P2 | no | 200,052 | 99,889 | 20 | 958,723 | 83 | 0.486 | 357,779 | 226,257 | 248,356 | pass |
| 4 | 0.602 | 0.600 | 0.6005 | 0.589 | 0.499 | +0.002 | unclassified | P1,P2 | no | not reached | – | 22 | 888,722 | 103 | 0.393 | 356,252 | 268,065 | 296,085 | - |
| 5 | 0.660 | 0.667 | 0.6666 | 0.843 | 0.852 | -0.007 | unclassified | P1,P2 | no | 200,052 | 106,853 | 20 | 879,940 | 31 | 0.445 | 357,932 | 284,939 | 292,612 | pass |
| 6 | 0.664 | 0.668 | 0.6682 | 0.829 | 0.827 | -0.004 | unclassified | P1,P2 | no | 150,004 | 72,094 | 20 | 916,666 | 99 | 0.476 | 356,823 | 231,571 | 259,143 | - |
| 7 | 0.740 | 0.723 | 0.7227 | 0.880 | 0.898 | +0.017 | unclassified | P1 | no | 850,036 | 476,229 | 22 | 934,591 | 84 | 0.476 | 357,101 | 226,461 | 243,489 | pass |
| 8 | 0.676 | 0.685 | 0.6848 | 0.864 | 0.861 | -0.009 | unclassified | P1 | no | 350,068 | 171,814 | 21 | 896,965 | 78 | 0.464 | 357,288 | 263,230 | 287,510 | pass |
| 9 | 0.681 | 0.678 | 0.6785 | 0.742 | 0.737 | +0.003 | unclassified | P2 | no | not reached | – | 22 | 910,112 | 34 | 0.489 | 356,810 | 255,103 | 263,709 | - |
| 10 | 0.681 | 0.677 | 0.6772 | 0.863 | 0.869 | +0.004 | unclassified | P1 | no | 200,052 | 111,264 | 19 | 944,872 | 40 | 0.457 | 356,123 | 284,531 | 295,867 | pass |
| 11 | 0.704 | 0.695 | 0.6951 | 0.885 | 0.897 | +0.009 | unclassified | P2 | no | 600,052 | 339,826 | 23 | 909,216 | 41 | 0.461 | 357,352 | 273,565 | 293,143 | pass |
| 12 | 0.723 | 0.720 | 0.7200 | 0.839 | 0.834 | +0.003 | unclassified | P1,P2 | no | 150,004 | 80,002 | 23 | 1,088,422 | 97 | 0.424 | 357,396 | 111,755 | 118,577 | - |
| 13 | 0.661 | 0.663 | 0.6632 | 0.799 | 0.000 | -0.002 | unclassified | P1 | no | 1,000,052 | 599,724 | 22 | 872,588 | 55 | 0.427 | 356,592 | 292,274 | 307,678 | - |
| 14 | 0.676 | 0.673 | 0.6732 | 0.823 | 0.821 | +0.003 | unclassified | P1,P2 | no | 150,004 | 84,654 | 21 | 968,447 | 43 | 0.452 | 357,223 | 254,949 | 266,004 | - |
| 15 | 0.736 | 0.721 | 0.7214 | 0.857 | 0.880 | +0.015 | unclassified | P1,P2 | no | 300,020 | 174,243 | 23 | 958,200 | 52 | 0.519 | 357,815 | 246,047 | 266,008 | pass |
| 16 | 0.738 | 0.726 | 0.7260 | 0.880 | 0.893 | +0.012 | unclassified | P2 | no | 200,052 | 113,443 | 21 | 989,699 | 44 | 0.543 | 355,846 | 234,476 | 250,608 | pass |
| 17 | 0.675 | 0.666 | 0.6663 | 0.803 | 0.797 | +0.009 | unclassified | P1 | no | 50,036 | 26,023 | 23 | 951,272 | 40 | 0.448 | 357,211 | 279,110 | 290,838 | - |
| 18 | 0.737 | 0.725 | 0.7246 | 0.879 | 0.890 | +0.012 | unclassified | P2 | no | 150,004 | 74,839 | 24 | 1,001,164 | 84 | 0.477 | 357,109 | 195,671 | 211,298 | pass |
| 19 | 0.686 | 0.676 | 0.6761 | 0.610 | 0.427 | +0.010 | unclassified | P2 | no | not reached | – | 23 | 896,788 | 56 | 0.434 | 357,497 | 276,733 | 290,736 | - |
| 20 | 0.686 | 0.674 | 0.6743 | 0.833 | 0.817 | +0.012 | unclassified | P1,P2 | no | not reached | – | 21 | 993,458 | 42 | 0.448 | 357,359 | 207,696 | 225,898 | - |
| 21 | 0.738 | 0.723 | 0.7226 | 0.883 | 0.898 | +0.015 | unclassified | P1,P2 | no | 850,036 | 487,269 | 22 | 919,657 | 44 | 0.495 | 356,949 | 251,810 | 275,714 | pass |
| 22 | 0.676 | 0.674 | 0.6745 | 0.807 | 0.824 | +0.002 | unclassified | P1,P2 | no | not reached | – | 24 | 960,275 | 78 | 0.434 | 357,142 | 241,117 | 259,683 | - |
| 23 | 0.674 | 0.674 | 0.6738 | 0.835 | 0.825 | +0.000 | unclassified | P1,P2 | no | 300,020 | 172,531 | 22 | 949,497 | 43 | 0.467 | 356,686 | 271,587 | 288,668 | - |
| 24 | 0.672 | 0.666 | 0.6663 | 0.803 | 0.805 | +0.006 | unclassified | P2 | no | not reached | – | 17 | 841,086 | 41 | 0.484 | 356,023 | 297,824 | 313,935 | - |
| 25 | 0.695 | 0.686 | 0.6861 | 0.832 | 0.832 | +0.009 | unclassified | P2 | no | 250,100 | 137,538 | 24 | 956,952 | 137 | 0.446 | 356,927 | 259,156 | 274,904 | - |
| 26 | 0.682 | 0.690 | 0.6901 | 0.810 | 0.786 | -0.008 | unclassified | neither | no | 700,020 | 425,697 | 22 | 951,774 | 85 | 0.427 | 356,164 | 255,676 | 274,967 | - |
| 27 | 0.645 | 0.636 | 0.6365 | 0.743 | 0.725 | +0.009 | unclassified | neither | no | not reached | – | 23 | 875,383 | 100 | 0.445 | 357,742 | 299,990 | 315,525 | - |
| 28 | 0.676 | 0.664 | 0.6640 | 0.792 | 0.785 | +0.012 | unclassified | P1,P2 | no | not reached | – | 23 | 950,834 | 48 | 0.443 | 357,551 | 264,299 | 287,078 | - |
| 29 | 0.710 | 0.682 | 0.6820 | 0.793 | 0.779 | +0.028 | unclassified | neither | no | not reached | – | 23 | 962,484 | 81 | 0.429 | 356,652 | 219,709 | 241,043 | - |
| 30 | 0.686 | 0.681 | 0.6812 | 0.797 | 0.814 | +0.005 | unclassified | P1 | no | 250,100 | 132,130 | 23 | 890,579 | 44 | 0.481 | 357,187 | 270,864 | 295,082 | - |
| 31 | 0.671 | 0.664 | 0.6643 | 0.794 | 0.784 | +0.007 | unclassified | P1,P2 | no | not reached | – | 23 | 916,886 | 38 | 0.428 | 356,367 | 277,928 | 304,166 | - |
| 32 | 0.619 | 0.626 | 0.6265 | 0.774 | 0.777 | -0.007 | unclassified | P2 | no | not reached | – | 24 | 897,912 | 99 | 0.421 | 357,160 | 292,066 | 302,356 | - |

"validation level at" is the candidate count in the `validation level` line of summary.md; "real evals at that row" is column 2 of that log row.
"S' reads" and "1/( in S'" are read off the printed S' line (for seed 7 that line is abbreviated, see below).

## Full formula of every seed with test above 0.72

seed 1 (test 0.721, train 0.735, T64 K8 0.869, T128 K8 0.878; structure [a=1.073 b=20.009 c=-0.939 g=-0.000, erase c/a=0.875, R²=0.8313, 1408 steps]; 23 instructions):

    S' = ((-0.147·((S - P1) + (S - P1))·k)⊗((k - 0)) + ((((S - P1) + (v)⊗(((((k - 0) + ((k + k) + (k + k))) + ((k - 0) + ((k + k) + (k + k)))) + ((((k - 0) + ((k + k) + (k + k))) + ((k - 0) + ((k + k) + (k + k)))) + v)))) + (-0.147·((S - P1) + (S - P1))·k)⊗((k - 0))) + (-0.147·((S - P1) + (S - P1))·k)⊗((k - 0))))
    P1' = -0.767·(((S - P1) + (v)⊗(((((k - 0) + ((k + k) + (k + k))) + ((k - 0) + ((k + k) + (k + k)))) + ((((k - 0) + ((k + k) + (k + k))) + ((k - 0) + ((k + k) + (k + k)))) + v)))) + ((v)⊗(((((k - 0) + ((k + k) + (k + k))) + ((k - 0) + ((k + k) + (k + k)))) + ((((k - 0) + ((k + k) + (k + k))) + ((k - 0) + ((k + k) + (k + k)))) + v))) - (0 + S)))
    P2' = ((v)⊗(((((k - 0) + ((k + k) + (k + k))) + ((k - 0) + ((k + k) + (k + k)))) + ((((k - 0) + ((k + k) + (k + k))) + ((k - 0) + ((k + k) + (k + k)))) + v))) - (0 + S))

seed 7 (test 0.723, train 0.740, T64 K8 0.880, T128 K8 0.898; structure [a=1.075 b=2.978 c=-0.945 g=0.003, erase c/a=0.879, R²=0.7825, 1408 steps]; 22 instructions):

    S' = (… + ((…)((tanh(k))⊗(tanh(k))) + 0.050·((((((v + v))⊗(k) + ((v + v))⊗(k)) + (((v + v))⊗(k) + ((v + v))⊗(k))) + 0.744·P1) + -0.005·S)))
    P1' = ((((((v + v))⊗(k) + ((v + v))⊗(k)) + (((v + v))⊗(k) + ((v + v))⊗(k))) + 0.744·P1) + -0.005·S)
    P2' = ((…)((tanh(k))⊗(tanh(k))) + 0.050·((((((v + v))⊗(k) + ((v + v))⊗(k)) + (((v + v))⊗(k) + ((v + v))⊗(k))) + 0.744·P1) + -0.005·S))

seed 15 (test 0.721, train 0.736, T64 K8 0.857, T128 K8 0.880; structure [a=1.073 b=1.001 c=-0.907 g=-0.000, erase c/a=0.846, R²=0.7936, 1408 steps]; 23 instructions):

    S' = ((-0.426·(-0.426·(P1 - P2) + (S + P2))·k)⊗(k) + ((((S + P2) + (-0.426·(-0.426·(P1 - P2) + (S + P2))·k)⊗(k)) + -0.426·(P1 - P2)) + (v)⊗(k)))
    P1' = (0.216 + <k, v>)·(-0.426·(P1 - P2) + -0.015·(((-0.426·(P1 - P2) + (v)⊗(k)) + -0.426·(P1 - P2)) - ((-0.426·(-0.426·(P1 - P2) + (S + P2))·k)⊗(k) + ((((S + P2) + (-0.426·(-0.426·(P1 - P2) + (S + P2))·k)⊗(k)) + -0.426·(P1 - P2)) + (v)⊗(k)))))
    P2' = ((-0.426·(P1 - P2) + (v)⊗(k)) + -0.426·(P1 - P2))

seed 16 (test 0.726, train 0.738, T64 K8 0.880, T128 K8 0.893; structure [a=1.078 b=4.006 c=-0.960 g=-0.000, erase c/a=0.891, R²=0.7980, 1408 steps]; 21 instructions):

    S' = (((S + (P2)ᵀ) + (-0.008·((S + (P2)ᵀ))ᵀ)(-0.008·((S + (P2)ᵀ))ᵀ)) + (((v + v) + -0.224·(S + (P2)ᵀ)·(k + k)))⊗((k + k)))
    P1' = (((v + v) + -0.224·(S + (P2)ᵀ)·(k + k)))⊗((k + k))
    P2' = (0.780·(P2 + -0.008·((S + (P2)ᵀ))ᵀ) + (((k + k))⊗((v + v)) + ((k + k))⊗((v + v))))

seed 18 (test 0.725, train 0.737, T64 K8 0.879, T128 K8 0.890; structure [a=1.078 b=4.006 c=-0.941 g=-0.000, erase c/a=0.873, R²=0.8010, 1408 steps]; 24 instructions):

    S' = ((-0.220·(S + P2))((((0 + k) + (0 + k)))⊗(((0 + k) + (0 + k)))) + ((S + P2) + (((v + v) + (v + v)))⊗((0 + k))))
    P1' = (((v + 0.115·(((v + v) + (v + v)) + v)) + (v + v)))⊗(((0 + k) + (0 + k)))
    P2' = (((P2 + -0.220·P2) + -0.006·((S + P2) + (((v + v) + (v + v)))⊗((0 + k)))) + (((v + 0.115·(((v + v) + (v + v)) + v)) + (v + v)))⊗(((0 + k) + (0 + k))))

seed 21 (test 0.723, train 0.738, T64 K8 0.883, T128 K8 0.898; structure [a=1.075 b=3.850 c=-0.964 g=-0.001, erase c/a=0.897, R²=0.7869, 1408 steps]; 22 instructions):

    S' = (((S + (((P2 + P2) + -0.016·(P1)(S)) - P1)) + (((v + v))⊗(k) + 0.184·(((P2 + P2) + -0.016·(P1)(S)) - P1))) + -0.917·(((S + (((P2 + P2) + -0.016·(P1)(S)) - P1))·k - (v + v)))⊗(k))
    P1' = 0.003·(((S + (((P2 + P2) + -0.016·(P1)(S)) - P1)) + (((v + v))⊗(k) + 0.184·(((P2 + P2) + -0.016·(P1)(S)) - P1))) + -0.917·(((S + (((P2 + P2) + -0.016·(P1)(S)) - P1))·k - (v + v)))⊗(k))
    P2' = ((((v + v))⊗(k) + 0.184·(((P2 + P2) + -0.016·(P1)(S)) - P1)) + (((v + v))⊗(k) + 0.184·(((P2 + P2) + -0.016·(P1)(S)) - P1)))

Read off the formulas only (collected forms checked numerically against the verify.py interpreter on random states: largest relative
difference 1.1%, from the rounding of the printed constants). No best rule of the arm contains a Recip instruction (checked in best.json).
- Seed 1: S' reads P1 (S − P1), not P2. Collected: with w = 20k + v, S' = (S − P1) + v wᵀ − 0.882·((S − P1)k)kᵀ, P1' = 0.767·P1 − 1.534·v wᵀ, P2' = v wᵀ − S. So the persistent register P1 is updated by subtracting an outer product (v wᵀ); P2 is overwritten every step. No reciprocal, no gain of the form P k / (c + kᵀP k).
- Seed 7: The printed formula is abbreviated with "…"; read off the effective program instead. S' reads P1 (through P1'), not the old P2. With t = tanh(k): P1' = 0.744·P1 + 8·v kᵀ − 0.005·S; Y = S + P1' + 16·v kᵀ; P2' = −(Y t)tᵀ + 0.05·P1'; S' = Y(I − t tᵀ) + 0.05·P1'. So P2 is updated by subtracting an outer product ((Y t)tᵀ), and P2 does not read its old value. No reciprocal, no gain of the form P k / (c + kᵀP k).
- Seed 15: S' reads P1 and P2. Collected: M = S + P2 − 0.426·(P1 − P2); S' = M + v kᵀ − 0.852·(M k)kᵀ; P2' = −0.852·(P1 − P2) + v kᵀ; P1' = (0.216 + kᵀv)·(−0.426·(P1 − P2) − 0.015·(P2' − S')), which contains −0.0128·(0.216 + kᵀv)·(M k)kᵀ. So P1 is updated with a subtracted outer product ((M k)kᵀ), scaled by the scalar 0.216 + kᵀv. No reciprocal, no gain of the form P k / (c + kᵀP k).
- Seed 16: S' reads P2 (as P2ᵀ), not P1. Collected: T = S + P2ᵀ; S' = T + 6.4e-5·(Tᵀ)² + 4·v kᵀ − 0.896·(T k)kᵀ; P1' = 4·v kᵀ − 0.896·(T k)kᵀ (overwritten every step, not read); P2' = 0.780·(P2 − 0.008·Tᵀ) + 8·k vᵀ. So P1 is set to a write that subtracts an outer product ((T k)kᵀ); P2 only adds one. No reciprocal, no gain of the form P k / (c + kᵀP k).
- Seed 18: S' reads P2, not P1. Collected: S' = (S + P2)(I − 0.88·k kᵀ) + 4·v kᵀ; P1' = 7.15·v kᵀ (overwritten every step, not read); P2' = 0.78·P2 − 0.006·S' + 7.15·v kᵀ, so P2' contains +0.0053·((S + P2)k)kᵀ and a net +7.126·v kᵀ. No persistent register has a subtracted outer product except through the small −0.006·S' term. No reciprocal, no gain of the form P k / (c + kᵀP k).
- Seed 21: S' reads P1 and P2. Collected: Q = 2·P2 − 0.016·P1 S − P1; S' = S + 1.184·Q + 3.834·v kᵀ − 0.917·((S + Q)k)kᵀ; P1' = 0.003·S'; P2' = 4·v kᵀ + 0.368·Q. So P1 receives a small multiple of S', which contains the subtracted outer product ((S + Q)k)kᵀ; P2 only adds one. No reciprocal, no gain of the form P k / (c + kᵀP k).

## Predictions against outcome (K_VORHERSAGE.md, committed in 1f4716c before any K run)

Research agent (README): main count 2 or more above 0.90 (P = 0.12): no (0). At least one above 0.90 (P = 0.22): no. 3 or more above 0.85
(P = 0.20): no (0). Median below j-lexicase (P = 0.35): yes (0.6765 vs 0.6815; Mann-Whitney p = 0.75). At most 5 stuck (P = 0.85): yes (0).
Executing agent:
1. main count 2 or more (P = 0.08): no.
2. at least one above 0.90 (P = 0.15): no.
3. 3 or more above 0.85 (P = 0.12): no.
4. median below j-lexicase (P = 0.45): yes.
5. at most 5 stuck (P = 0.85): yes.
6. rule 2 in 12 or more (P = 0.45): no (11).
7. inserted / attempts between 0.75 and 0.95 in the median seed (P = 0.60): no (0.73).
8. epsilon check moves at least one seed by more than 0.02 (P = 0.25): no.
9. no seed aborts (P = 0.85): no seed of the complete run aborted; the first two starts of the whole run were killed by the hub (WHERE.md).
   JAX within 0.002 for every seed not flagged as diverged (P = 0.80): yes (0.0005).
10. projection at or below 30 h (P = 0.75): yes (24.3 h projected; actual 17.6 h).
