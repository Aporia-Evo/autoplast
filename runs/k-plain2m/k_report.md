# k-plain2m (package K, arm 2): results as measured

collision3, task seed 1, 96 + 48 train episodes, fixed readout, --recip --persist-m 3 --persist-init identity, add-node on, plain selection
(`select: fitness`, residual insertion off), --val-log --level-acc 0.651 --level-long 0.838, seeds 1-32, 2,100,000 candidates, --parallel 2 --threads 8
(batch 128), commit 6c2f60a, all seeds on epyc (owner's decision: the workstation projection was 32.4 h). Wall 62119 s (17.26 h).
No seed failed or was rerun. Baselines: the committed runs d-kalman, j-lexicase, j-share (not rerun). Facts only; the interpretation is left to the research agent.

## Same trajectory as d-kalman up to 1.5M

For all 32 seeds, every log row of k-plain2m up to 1,500,100 candidates equals the d-kalman row in candidates, real evaluations, best fitness,
best accuracy, length and pop_mean_acc (only the seconds differ; d-kalman has no val_acc/long_acc columns). So k-plain2m is d-kalman continued
by 600,000 candidates. The final best rule is the same as in d-kalman in 15/32 seeds.
The final test changed (by more than 0.0005) in 11 seeds: 2 (0.684 -> 0.683), 3 (0.639 -> 0.642), 4 (0.631 -> 0.632), 6 (0.629 -> 0.694), 13 (0.588 -> 0.684), 15 (0.663 -> 0.672), 18 (0.528 -> 0.564), 20 (0.513 -> 0.512), 21 (0.520 -> 0.589), 23 (0.516 -> 0.630), 28 (0.578 -> 0.636).

## Counts against d-kalman, j-lexicase and j-share

"under the conditions" = T128 K8 >= 0.838 and train - test <= 0.03. "stuck" = collision3 test below 0.53.

| tag | rule 2 | stuck below 0.53 | test > 0.85 under the conditions | above 0.695 under the conditions | above 0.90 under the conditions | median test | mean train - test | mean real evals | mean minutes | mean last pop_mean_acc | validation level reached |
|---|---|---|---|---|---|---|---|---|---|---|---|
| k-plain2m (2.1M) | 8/32 (2, 6, 7, 9, 13, 15, 24, 25) | 9/32 (1, 8, 11, 14, 19, 20, 22, 26, 29) | 1/32 (9) | 2/32 (7, 9) | 0/32 | 0.6350 | +0.0132 | 1,139,327 | 63.9 | 0.430 | 9/32 |
| d-kalman (1.5M) | 6/32 (2, 7, 9, 15, 24, 25) | 12/32 (1, 8, 11, 14, 18, 19, 20, 21, 22, 23, 26, 29) | 1/32 (9) | 2/32 (7, 9) | 0/32 | 0.6300 | +0.0141 | 784,926 | 42.2 | 0.418 | 0/32 |
| j-lexicase (1.5M) | 12/32 (2, 3, 4, 6, 9, 12, 17, 22, 24, 28, 30, 32) | 0/32 | 1/32 (6) | 5/32 (2, 6, 9, 12, 17) | 0/32 | 0.6815 | +0.0002 | 806,780 | 59.5 | 0.446 | 20/32 |
| j-share (1.5M) | 11/32 (1, 5, 6, 9, 12, 17, 22, 24, 26, 30, 32) | 0/32 | 0/32 | 0/32 | 0/32 | 0.6525 | -0.0123 | 962,443 | 49.4 | 0.349 | 16/32 |

Mann-Whitney (two-sided) of the 32 test accuracies: against d-kalman U = 564.0, p = 0.49;
against j-lexicase U = 225.5, p = 1.2e-04; against j-share U = 363.5, p = 0.047.
Threshold fixed in README: the effect of J stands if k-plain2m has 5/32 or more stuck. Measured: 9/32.
Train accuracy of the last log row at or below 1,500,100 candidates is below 0.53 in 11/32 seeds
(1, 8, 11, 14, 19, 20, 21, 22, 23, 26, 29), the same 11 seeds as in d-kalman at that point.
Seeds stuck on test in d-kalman but not in k-plain2m: 18, 21, 23.

## JAX and epsilon check

Dump made with the epyc binary, checked on the workstation, then deleted on both machines.
- `verify.py --task-json` (float32): largest difference to Rust 0.0005 over the 31 seeds not flagged; seed 22 is flagged as diverged
  (Rust guard 0.000, JAX 0.5153), as in d-kalman. -> verify_dump.txt
- `verify.py --x64 --norm-eps 1e-9 --task-json`: one seed moves by more than 0.02: seed 9, 0.8551 -> 0.8336 (-0.0215).
  The count changed in one more seed (20: 3331/6503 -> 3326/6503). -> verify_eps_x64.txt
- `verify/eps_scale.py` on seed 9: median max|S| 2.15 with epsilon 1e-6 and 2.01 with 1e-3, ratio 0.936. For comparison in the same call:
  d-kalman seed 9 (the same rule) ratio 0.936, j-lexicase seed 6 ratio 1e+03. -> eps_scale.txt

## Per seed

| seed | train | collision3 test | JAX on dump | T64 K8 | T128 K8 | train - test | family | S' reads | validation level at | instr | real evals | min | train at last row <= 1,500,100 | d-kalman test | rule 2 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | 0.517 | 0.520 | 0.5198 | 0.584 | 0.553 | -0.003 | decayed linear attention | P2 | not reached | 19 | 1,380,176 | 86 | 0.5168 | 0.520 | - |
| 2 | 0.676 | 0.683 | 0.6834 | 0.842 | 0.850 | -0.007 | unclassified | P1,P2 | 100,084 | 21 | 1,532,764 | 79 | 0.6757 | 0.684 | pass |
| 3 | 0.634 | 0.642 | 0.6420 | 0.798 | 0.757 | -0.008 | unclassified | P2 | not reached | 17 | 1,087,255 | 138 | 0.6314 | 0.639 | - |
| 4 | 0.628 | 0.632 | 0.6316 | 0.782 | 0.769 | -0.004 | unclassified | P1 | not reached | 17 | 1,255,460 | 50 | 0.6265 | 0.631 | - |
| 5 | 0.627 | 0.641 | 0.6406 | 0.786 | 0.771 | -0.014 | unclassified | P2 | not reached | 15 | 925,441 | 31 | 0.6257 | 0.641 | - |
| 6 | 0.689 | 0.694 | 0.6935 | 0.838 | 0.851 | -0.005 | unclassified | neither | 1,550,068 | 18 | 1,077,797 | 171 | 0.6224 | 0.629 | pass |
| 7 | 0.726 | 0.713 | 0.7131 | 0.849 | 0.851 | +0.013 | unclassified | P2 | 100,084 | 18 | 1,159,682 | 39 | 0.7265 | 0.713 | pass |
| 8 | 0.510 | 0.509 | 0.5095 | 0.574 | 0.543 | +0.001 | unclassified | neither | not reached | 8 | 745,655 | 23 | 0.5102 | 0.509 | - |
| 9 | 0.863 | 0.855 | 0.8551 | 0.940 | 0.885 | +0.008 | unclassified | P1,P2 | 600,052 | 22 | 1,431,536 | 57 | 0.8632 | 0.855 | pass |
| 10 | 0.644 | 0.644 | 0.6437 | 0.731 | 0.726 | +0.000 | unclassified | P1,P2 | not reached | 15 | 1,150,684 | 151 | 0.6437 | 0.644 | - |
| 11 | 0.518 | 0.515 | 0.5147 | 0.565 | 0.558 | +0.003 | unclassified | P1 | not reached | 12 | 949,198 | 31 | 0.5184 | 0.515 | - |
| 12 | 0.648 | 0.653 | 0.6531 | 0.827 | 0.819 | -0.005 | unclassified | P2 | not reached | 21 | 1,433,955 | 50 | 0.6478 | 0.653 | - |
| 13 | 0.668 | 0.684 | 0.6835 | 0.858 | 0.871 | -0.016 | unclassified | P1,P2 | 2,100,084 | 19 | 1,078,988 | 57 | 0.5774 | 0.588 | pass |
| 14 | 0.523 | 0.507 | 0.5075 | 0.553 | 0.538 | +0.016 | unclassified | P1,P2 | not reached | 17 | 1,111,577 | 47 | 0.5233 | 0.507 | - |
| 15 | 0.663 | 0.672 | 0.6718 | 0.865 | 0.873 | -0.009 | unclassified | P1,P2 | 1,050,100 | 14 | 1,015,759 | 47 | 0.6560 | 0.663 | pass |
| 16 | 0.635 | 0.636 | 0.6360 | 0.822 | 0.793 | -0.001 | unclassified | P2 | not reached | 18 | 1,293,434 | 36 | 0.6347 | 0.636 | - |
| 17 | 0.623 | 0.634 | 0.6337 | 0.817 | 0.818 | -0.011 | unclassified | P1,P2 | not reached | 16 | 1,102,524 | 49 | 0.6233 | 0.634 | - |
| 18 | 0.568 | 0.564 | 0.5644 | 0.593 | 0.561 | +0.004 | unclassified | P2 | not reached | 15 | 882,148 | 27 | 0.5356 | 0.528 | - |
| 19 | 0.515 | 0.518 | 0.5181 | 0.573 | 0.558 | -0.003 | decayed linear attention | neither | not reached | 14 | 1,066,680 | 27 | 0.5152 | 0.518 | - |
| 20 | 0.521 | 0.512 | 0.5122 | 0.575 | 0.549 | +0.009 | unclassified | P1,P2 | not reached | 17 | 1,149,937 | 81 | 0.5201 | 0.513 | - |
| 21 | 0.578 | 0.589 | 0.5888 | 0.627 | 0.616 | -0.011 | unclassified | P2 | not reached | 17 | 973,979 | 37 | 0.5152 | 0.520 | - |
| 22 | 0.519 | 0.000 | 0.5153 (diverged) | 0.577 | 0.561 | +0.519 | unclassified | P1,P2 | not reached | 17 | 1,190,809 | 42 | 0.5192 | 0.000 | - |
| 23 | 0.622 | 0.630 | 0.6297 | 0.809 | 0.812 | -0.008 | unclassified | P1,P2 | not reached | 15 | 803,306 | 40 | 0.5086 | 0.516 | - |
| 24 | 0.654 | 0.657 | 0.6568 | 0.860 | 0.866 | -0.003 | unclassified | P2 | 1,100,020 | 19 | 1,188,510 | 47 | 0.6536 | 0.657 | pass |
| 25 | 0.667 | 0.672 | 0.6715 | 0.859 | 0.861 | -0.005 | unclassified | P2 | 850,036 | 16 | 1,147,010 | 142 | 0.6667 | 0.672 | pass |
| 26 | 0.511 | 0.516 | 0.5156 | 0.583 | 0.553 | -0.005 | decayed linear attention | neither | not reached | 9 | 713,191 | 21 | 0.5111 | 0.516 | - |
| 27 | 0.681 | 0.687 | 0.6868 | 0.816 | 0.808 | -0.006 | unclassified | P1,P2 | 200,052 | 24 | 1,526,978 | 80 | 0.6806 | 0.687 | - |
| 28 | 0.615 | 0.636 | 0.6360 | 0.776 | 0.765 | -0.021 | unclassified | P1,P2 | not reached | 18 | 1,325,653 | 38 | 0.5725 | 0.578 | - |
| 29 | 0.512 | 0.513 | 0.5135 | 0.578 | 0.562 | -0.001 | unclassified | P1,P2 | not reached | 10 | 831,044 | 58 | 0.5119 | 0.513 | - |
| 30 | 0.642 | 0.642 | 0.6422 | 0.808 | 0.800 | +0.000 | unclassified | P2 | not reached | 22 | 1,438,576 | 93 | 0.6421 | 0.642 | - |
| 31 | 0.633 | 0.634 | 0.6336 | 0.792 | 0.784 | -0.001 | unclassified | P2 | not reached | 20 | 1,440,096 | 104 | 0.6331 | 0.634 | - |
| 32 | 0.600 | 0.603 | 0.6028 | 0.758 | 0.760 | -0.003 | unclassified | P2 | not reached | 16 | 1,048,648 | 68 | 0.5995 | 0.603 | - |

## Full formula of every seed with test above 0.72

seed 9 (test 0.855, train 0.863, T64 K8 0.940, T128 K8 0.885; structure [a=0.817 b=3.724 c=-0.024 g=-0.000, erase c/a=0.030, R²=0.4273, 1408 steps]; 22 instructions):

    S' = ((P2 + ((((norm(tanh(v)) + norm(tanh(v))) + (norm(tanh(v)) + norm(tanh(v)))) + (norm(tanh(v)) + norm(tanh(v)))))⊗(norm(σ(0)·σ(0)·(P1)ᵀ·k))) - (P1 - (P1·<norm(σ(0)·σ(0)·(P1)ᵀ·k), norm(σ(0)·σ(0)·(P1)ᵀ·k)>·k)⊗(norm(σ(0)·σ(0)·(P1)ᵀ·k))))
    P1' = (P1 - (P1·<norm(σ(0)·σ(0)·(P1)ᵀ·k), norm(σ(0)·σ(0)·(P1)ᵀ·k)>·k)⊗(norm(σ(0)·σ(0)·(P1)ᵀ·k)))
    P2' = σ(1.390)·(P2 + ((((norm(tanh(v)) + norm(tanh(v))) + (norm(tanh(v)) + norm(tanh(v)))) + (norm(tanh(v)) + norm(tanh(v)))))⊗(norm(σ(0)·σ(0)·(P1)ᵀ·k)))

The program is identical to the best rule of d-kalman seed 9 (same instruction list in best.json). Read off the formula:
S' reads P1 and P2; P1 is updated by subtracting an outer product (P1' = P1 − (P1 k)uᵀ with u = norm(P1ᵀk), as recorded for d-kalman seed 9);
no reciprocal and no gain of the form P k / (c + kᵀP k).

## Predictions against outcome (K_VORHERSAGE.md, committed in 1f4716c before any K run)

Research agent (README): 5 or more stuck (P = 0.80): yes (9). A seed above 0.90 (P = 0.03): no.
Executing agent:
11. 5 or more below 0.53 (P = 0.75): yes. Any seed above 0.90 under the conditions (P = 0.03): no.
12. projection on the workstation at or below 30 h (P = 0.50): no (32.4 h conservative, 23.8 h from the mean); the arm then ran on epyc
    (projection 24.1 h, actual 17.3 h).
13. seeds below 0.53 in train at the last row at or below 1,500,100 exactly the 11 of d-kalman (P = 0.30): yes (the whole trajectory is identical).
