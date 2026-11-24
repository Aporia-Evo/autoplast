# m-lexicase (package M): results as measured

collision3, --recip --persist-m 3 --persist-init identity, add-node on, --select lexicase, --val-log --level-acc 0.651 --level-long 0.838,
task seeds 801 to 808 (search seed = task seed, --task-seed-from-seed), 1,500,000 candidates, --parallel 2 --threads 8 (batch 128), commit dce11aa,
all seeds on epyc, started 2026-11-21T23:43:02Z (after m-plain, same script), wall 10191 s (2.83 h). No seed failed or was rerun. Facts only; the interpretation is left to the research agent.

## Counts (reading of README, "Memetic search: confirmation on 16 fresh task seeds")

Count = test > 0.90 with T128 K8 >= 0.838, train - test <= 0.03, long probe below 100 in all nine draws, epsilon check within 0.02.

| tag | count (test > 0.90 with the conditions) | test >= 0.99 | rule 2 (test > 0.651, T128 K8 >= 0.838, train - test <= 0.03) | below 0.53 on test | median test | best test | mean train - test | mean real evals | mean minutes |
|---|---|---|---|---|---|---|---|---|---|
| m-lexicase | 0/8 | 0/8 | 4/8 (801, 804, 807, 808) | 0/8 | 0.6645 | 0.693 | +0.0134 | 751,051 | 37.0 |

For reference (README, same task seeds): the frozen memetic search counted 5 of 8 (802, 803, 804, 805, 806).

## Next to m-plain (same task seeds)

| tag | count | test >= 0.99 | rule 2 | below 0.53 | median test | best test | mean minutes |
|---|---|---|---|---|---|---|---|
| m-plain | 0/8 | 0/8 | 0/8 | 5/8 | 0.5210 | 0.643 | 31.4 |
| m-lexicase | 0/8 | 0/8 | 4/8 (801, 804, 807, 808) | 0/8 | 0.6645 | 0.693 | 37.0 |

Mann-Whitney (two-sided) of the eight test accuracies, m-lexicase against m-plain: U = 58.0, p = 0.0073.
Wall of both arms together (run_M.sh): 2026-11-21T21:35:22Z to 2026-11-22T02:32:54Z, 17,852 s (4.96 h).

## JAX and epsilon check

The test dump (`autoplast dump --regime collision3 --split test --task-seed N`) is byte-identical for the eight task seeds (same md5), so the
collision3 test suite does not depend on the task seed; the task seed changes the train task. Each best rule was checked on the dump of its own
task seed. JAX float32 against Rust: largest difference 0.0005; no seed flagged as diverged.
`verify.py --x64 --norm-eps 1e-9`: largest change 0.0000; seeds moving by more than 0.02: none, so eps_scale.py was not needed.

## Long-episode probe

`autoplast evalmany --in <best rule> --split long --regime collision3 --recip --persist-m 3 --persist-init identity --task-seed N` for N = own task seed
and 1 to 8, first column (max_state). Raw output: long_probe_raw.json.

| task seed | own draw | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 |
|---|---|---|---|---|---|---|---|---|---|
| 801 | 4.04 | 3.41 | 3.76 | 3.43 | 3.41 | 3.32 | 3.45 | 3.59 | 3.7 |
| 802 | 0.861 | 0.811 | 0.825 | 0.82 | 0.797 | 0.801 | 0.794 | 0.866 | 0.898 |
| 803 | 0.499 | 0.537 | 0.496 | 0.516 | 0.478 | 0.464 | 0.473 | 0.59 | 0.53 |
| 804 | 3.23 | 2.2 | 4.88 | 1.77 | 1.66 | 2.39 | 2.11 | 1.88 | 2.17 |
| 805 | 0.671 | 0.725 | 0.739 | 0.656 | 0.681 | 0.706 | 0.767 | 0.808 | 0.818 |
| 806 | 1.35 | 1.3 | 1.31 | 1.42 | 1.28 | 1.33 | 1.33 | 1.27 | 1.38 |
| 807 | 0.894 | 0.934 | 0.818 | 0.943 | 0.919 | 0.918 | 0.884 | 0.912 | 0.921 |
| 808 | 7.87 | 7.76 | 9.47 | 8.28 | 8.76 | 7.76 | 8.03 | 8.87 | 8.88 |

## Per seed

| task seed | train | collision3 test | JAX on dump | JAX float64, eps 1e-9 | T64 K8 | T128 K8 | train - test | long probe, largest of nine (draw) | family | S' reads | instr | real evals | min |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 801 | 0.675 | 0.674 | 0.6745 | 0.6745 | 0.870 | 0.881 | +0.001 | 4.04 (801) | unclassified | P2 | 16 | 763,131 | 78 |
| 802 | 0.697 | 0.652 | 0.6517 | 0.6517 | 0.854 | 0.851 | +0.045 | 0.898 (8) | unclassified | P1 | 14 | 685,903 | 19 |
| 803 | 0.636 | 0.631 | 0.6312 | 0.6312 | 0.795 | 0.776 | +0.005 | 0.59 (7) | unclassified | P1 | 13 | 707,819 | 26 |
| 804 | 0.667 | 0.673 | 0.6734 | 0.6734 | 0.844 | 0.872 | -0.006 | 4.88 (2) | unclassified | P1 | 17 | 817,656 | 30 |
| 805 | 0.692 | 0.661 | 0.6609 | 0.6609 | 0.827 | 0.833 | +0.031 | 0.818 (8) | unclassified | P1 | 14 | 764,913 | 24 |
| 806 | 0.581 | 0.564 | 0.5644 | 0.5644 | 0.698 | 0.696 | +0.017 | 1.42 (3) | unclassified | P2 | 19 | 690,618 | 19 |
| 807 | 0.686 | 0.693 | 0.6931 | 0.6931 | 0.853 | 0.864 | -0.007 | 0.943 (3) | unclassified | P1,P2 | 13 | 762,490 | 72 |
| 808 | 0.689 | 0.668 | 0.6677 | 0.6677 | 0.868 | 0.893 | +0.021 | 9.47 (2) | unclassified | P1,P2 | 16 | 815,878 | 27 |

## Predictions against outcome (runs/m-plain/M_VORHERSAGE.md, committed in be1b18b before any M run)

Research agent: m-lexicase 0/8 above 0.90 (P = 0.8): yes (0/8).
Executing agent:
2. m-lexicase 0/8 above 0.90 under the conditions (P = 0.85): yes.
3. any seed of either arm with test >= 0.99 (P = 0.03): no (0).
5. m-lexicase 0 of 8 below 0.53 (P = 0.75): yes (0).
6. median test of m-lexicase above that of m-plain (P = 0.75): yes (0.6645 vs 0.5210).
7. total wall of both arms between 6 and 14 h (P = 0.70): no (4.96 h).
8. JAX within 0.002 for every seed not flagged (P = 0.80): yes.
9. epsilon check moves at least one seed of the two arms by more than 0.02 (P = 0.30): no.
10. the best-test seed of each arm below 100 in all nine long-probe draws (P = 0.50): m-plain seed 803 largest 3.23,
    m-lexicase seed 807 largest 0.943: yes.
