# 5a result: free readout and extra ops on collision3 (written 2026-11-05 15:43 UTC)

Prediction and decision rules: 5a_VORHERSAGE.md (commit 97d2a2e, before the runs).
Additional checks: 5a_NACHTRAG_2026-11-05.md (commit b4aa8df, written during the run).
Runs on the JupyterHub, one binary for all arms (sha256 5512427..., built 06:39 UTC before A),
16 seeds x 1.5M candidates per arm, all three arms exit code 0.
A: default alphabet, fixed readout. B: `--evolve-readout --extra-ops`. C: `--evolve-readout`.
Headers checked in every summary (B: 29 ops, readout evolved; C: 19 ops, readout evolved).
JAX: every best program re-run on the exact Rust collision3 test data (verify.py --task-json);
max |JAX - Rust| 0.0005 in all three arms, i.e. rounding (verify-dump_ERGEBNIS.md).
Reference on the collision3 test: tuned DeltaNet = tuned GDN 0.631 (T128 K8 0.858);
untuned delta beta=0.5 0.640. The offline LS value 1.000 is an in-sample oracle, not reachable headroom.

## Summary
| arm | delta reached | median test | max test | seeds > 0.651 | rule 2 | non-empty read | sum of seed times (s) |
|---|---|---|---|---|---|---|---|
| A | 7/16 | 0.517 | 0.660 | [2] | 0/16 | 0/16 | 19424 |
| B | 4/16 | 0.521 | 0.640 | none | 0/16 | 8/16 | 32102 |
| C | 2/16 | 0.517 | 0.638 | none | 0/16 | 5/16 | 9921 |

## Rule 1 (pre-registered): two-sided Mann-Whitney on per-seed collision3 test accuracy
- B vs A: U = 134.5, p = 0.821. Not significant.
- C vs A: U = 120.0, p = 0.775. Not significant.

Addendum checks (not pre-registered): B vs C p = 0.160; Holm over the three pairs, smallest adjusted p 0.479.
Fisher exact on delta-reached rates: A 7/16 vs B 4/16 p = 0.458; A vs C 2/16 p = 0.113; B vs C p = 0.654.
Because B and C give part of the mutations to the read program at equal candidate budget, this answers
"is the configuration better at equal budget" (no), not "can a free readout help in principle".

## Rule 2 (pre-registered): test > 0.651 AND T128 K8 >= 0.838 AND train - test <= 0.03
No seed in any arm passes. The only seed above 0.651 is A seed 2 (Rust 0.660, JAX 0.6597, train 0.642,
T128 K8 0.777): it fails the T128 condition by 0.061. Its rule is a delta-like update with a state-dependent
step |S k| and tanh nonlinearities (summary.md). Its 0.660 is 0.020 above delta beta=0.5 (0.640),
about 3 SE under the iid-query SE; the episode-level bootstrap and the 10 fresh embedding draws from the addendum
are still open and are post hoc for this seed.

## Per-seed tables
### A (fixed readout, 19 ops)
| seed | delta reached | train | collision3 test (Rust) | JAX dump | train-test | T12 | T128 K8 | read instrs | rule 2 |
|---|---|---|---|---|---|---|---|---|---|
| 1 | no | 0.510 | 0.509 | 0.5093 | +0.001 | 0.716 | 0.542 | 0 | no |
| 2 | yes | 0.642 | 0.660 | 0.6597 | -0.018 | 0.924 | 0.777 | 0 | no |
| 3 | no | 0.512 | 0.511 | 0.5115 | +0.001 | 0.712 | 0.545 | 0 | no |
| 4 | no | 0.512 | 0.517 | 0.5175 | -0.005 | 0.754 | 0.553 | 0 | no |
| 5 | yes | 0.625 | 0.640 | 0.6397 | -0.015 | 0.922 | 0.786 | 0 | no |
| 6 | no | 0.511 | 0.517 | 0.5167 | -0.006 | 0.729 | 0.551 | 0 | no |
| 7 | no | 0.511 | 0.506 | 0.5064 | +0.005 | 0.717 | 0.555 | 0 | no |
| 8 | yes | 0.632 | 0.640 | 0.6399 | -0.008 | 0.927 | 0.796 | 0 | no |
| 9 | no | 0.509 | 0.516 | 0.5158 | -0.007 | 0.734 | 0.550 | 0 | no |
| 10 | no | 0.510 | 0.509 | 0.5093 | +0.001 | 0.716 | 0.542 | 0 | no |
| 11 | yes | 0.624 | 0.642 | 0.6417 | -0.018 | 0.929 | 0.783 | 0 | no |
| 12 | yes | 0.630 | 0.648 | 0.6482 | -0.018 | 0.938 | 0.805 | 0 | no |
| 13 | yes | 0.623 | 0.635 | 0.6348 | -0.012 | 0.921 | 0.838 | 0 | no |
| 14 | no | 0.510 | 0.509 | 0.5093 | +0.001 | 0.716 | 0.542 | 0 | no |
| 15 | yes | 0.621 | 0.634 | 0.6340 | -0.013 | 0.917 | 0.818 | 0 | no |
| 16 | no | 0.511 | 0.517 | 0.5165 | -0.006 | 0.743 | 0.550 | 0 | no |

### B (evolved readout, 29 ops)
| seed | delta reached | train | collision3 test (Rust) | JAX dump | train-test | T12 | T128 K8 | read instrs | rule 2 |
|---|---|---|---|---|---|---|---|---|---|
| 1 | no | 0.514 | 0.524 | 0.5236 | -0.010 | 0.790 | 0.557 | 0 | no |
| 2 | yes | 0.623 | 0.636 | 0.6363 | -0.013 | 0.918 | 0.826 | 0 | no |
| 3 | no | 0.520 | 0.515 | 0.5145 | +0.005 | 0.753 | 0.556 | 6 | no |
| 4 | yes | 0.624 | 0.638 | 0.6382 | -0.014 | 0.923 | 0.788 | 1 | no |
| 5 | no | 0.528 | 0.519 | 0.5188 | +0.009 | 0.795 | 0.569 | 0 | no |
| 6 | yes | 0.613 | 0.621 | 0.6211 | -0.008 | 0.897 | 0.759 | 0 | no |
| 7 | no | 0.513 | 0.521 | 0.5207 | -0.008 | 0.782 | 0.568 | 6 | no |
| 8 | no | 0.518 | 0.518 | 0.5179 | +0.000 | 0.749 | 0.566 | 0 | no |
| 9 | no | 0.519 | 0.516 | 0.5164 | +0.003 | 0.769 | 0.558 | 7 | no |
| 10 | no | 0.520 | 0.516 | 0.5161 | +0.004 | 0.768 | 0.555 | 7 | no |
| 11 | no | 0.510 | 0.521 | 0.5213 | -0.011 | 0.783 | 0.567 | 0 | no |
| 12 | yes | 0.631 | 0.640 | 0.6396 | -0.009 | 0.938 | 0.840 | 2 | no |
| 13 | no | 0.515 | 0.517 | 0.5175 | -0.002 | 0.791 | 0.544 | 0 | no |
| 14 | no | 0.520 | 0.514 | 0.5141 | +0.006 | 0.767 | 0.562 | 6 | no |
| 15 | no | 0.516 | 0.521 | 0.5207 | -0.005 | 0.784 | 0.566 | 5 | no |
| 16 | no | 0.509 | 0.521 | 0.5213 | -0.012 | 0.782 | 0.567 | 0 | no |

### C (evolved readout, 19 ops)
| seed | delta reached | train | collision3 test (Rust) | JAX dump | train-test | T12 | T128 K8 | read instrs | rule 2 |
|---|---|---|---|---|---|---|---|---|---|
| 1 | no | 0.509 | 0.517 | 0.5170 | -0.008 | 0.765 | 0.554 | 0 | no |
| 2 | no | 0.513 | 0.517 | 0.5171 | -0.004 | 0.727 | 0.560 | 7 | no |
| 3 | no | 0.515 | 0.512 | 0.5121 | +0.003 | 0.730 | 0.545 | 0 | no |
| 4 | no | 0.512 | 0.517 | 0.5165 | -0.005 | 0.728 | 0.555 | 0 | no |
| 5 | no | 0.512 | 0.518 | 0.5176 | -0.006 | 0.759 | 0.546 | 3 | no |
| 6 | no | 0.514 | 0.521 | 0.5213 | -0.007 | 0.737 | 0.558 | 8 | no |
| 7 | yes | 0.622 | 0.638 | 0.6377 | -0.016 | 0.920 | 0.815 | 4 | no |
| 8 | no | 0.509 | 0.517 | 0.5170 | -0.008 | 0.736 | 0.540 | 3 | no |
| 9 | no | 0.506 | 0.517 | 0.5168 | -0.011 | 0.734 | 0.561 | 0 | no |
| 10 | no | 0.509 | 0.516 | 0.5162 | -0.007 | 0.734 | 0.550 | 0 | no |
| 11 | no | 0.509 | 0.517 | 0.5170 | -0.008 | 0.747 | 0.556 | 0 | no |
| 12 | no | 0.510 | 0.514 | 0.5139 | -0.004 | 0.727 | 0.547 | 0 | no |
| 13 | no | 0.511 | 0.515 | 0.5150 | -0.004 | 0.732 | 0.547 | 0 | no |
| 14 | no | 0.532 | 0.537 | 0.5371 | -0.005 | 0.765 | 0.584 | 0 | no |
| 15 | no | 0.512 | 0.516 | 0.5162 | -0.004 | 0.729 | 0.551 | 0 | no |
| 16 | yes | 0.625 | 0.638 | 0.6376 | -0.013 | 0.917 | 0.794 | 0 | no |

## Prediction check (5a_VORHERSAGE.md)
- A at least one seed reaches delta (p 0.7): correct (7/16).
- A median between 0.55 and 0.64 (p 0.6): wrong (0.517; the distribution is bimodal, 9/16 stay in the decayed-LA basin near 0.51).
- No A seed beats tuned DeltaNet by rule 2 (p 0.8): correct.
- B at least one rule-2 seed (p 0.35): did not happen. C (p 0.3): did not happen.
- B significantly above A (p 0.3): did not happen. C significantly above A (p 0.25): did not happen.
- At least one best rule with a non-empty effective read program (p 0.75): correct (B 8/16, C 5/16).
- Wall time A 5 to 9 h (p 0.6): wrong, A took 10,065 s = 2.8 h. B and C wall times: still to be read from the hub runner logs.

## Meaning
Under the pre-registered rules, neither a free readout nor the extra ops improve the search on collision3 at
equal budget, and no evolved rule beats tuned DeltaNet. All delta-reaching seeds of the three arms sit at
0.621 to 0.660 on the test, around delta beta=0.5 (0.640); the non-delta seeds stay near 0.51.
Evolved read programs exist in 13 best rules, but none of them belongs to a seed above 0.640.
