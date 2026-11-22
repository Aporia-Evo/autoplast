# m-plain (package M): results as measured

collision3, --recip --persist-m 3 --persist-init identity, add-node on, plain selection (`select: fitness`), --val-log --level-acc 0.651 --level-long 0.838,
task seeds 801 to 808 (search seed = task seed, --task-seed-from-seed), 1,500,000 candidates, --parallel 2 --threads 8 (batch 128), commit dce11aa,
all seeds on epyc, started 2026-11-21T21:35:22Z, wall 7660 s (2.13 h). No seed failed or was rerun. Facts only; the interpretation is left to the research agent.

## Counts (reading of README, "Memetic search: confirmation on 16 fresh task seeds")

Count = test > 0.90 with T128 K8 >= 0.838, train - test <= 0.03, long probe below 100 in all nine draws, epsilon check within 0.02.

| tag | count (test > 0.90 with the conditions) | test >= 0.99 | rule 2 (test > 0.651, T128 K8 >= 0.838, train - test <= 0.03) | below 0.53 on test | median test | best test | mean train - test | mean real evals | mean minutes |
|---|---|---|---|---|---|---|---|---|---|
| m-plain | 0/8 | 0/8 | 0/8 | 5/8 (801, 802, 804, 805, 806) | 0.5210 | 0.643 | +0.0179 | 780,548 | 31.4 |

For reference (README, same task seeds): the frozen memetic search counted 5 of 8 (802, 803, 804, 805, 806).

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
| 801 | 4.96 | 4.6 | 4.1 | 4.83 | 4.08 | 4.67 | 5.87 | 4.65 | 4.66 |
| 802 | 2.39 | 2.64 | 2.21 | 2.7 | 2.33 | 2.63 | 3.02 | 2.51 | 2.41 |
| 803 | 2.6 | 3.23 | 3.15 | 2.66 | 2.62 | 2.75 | 2.98 | 3.1 | 2.97 |
| 804 | 4.52 | 4.93 | 4.36 | 5.2 | 4.96 | 5.3 | 6.55 | 4.62 | 5.21 |
| 805 | 1.33 | 1.39 | 1.43 | 1.45 | 1.51 | 1.43 | 1.54 | 1.38 | 1.44 |
| 806 | 0.669 | 0.815 | 0.683 | 0.83 | 0.798 | 0.815 | 1.02 | 0.76 | 0.797 |
| 807 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 |
| 808 | 47 | 51.9 | 46.6 | 43 | 48.7 | 47.3 | 47 | 52.5 | 51 |

## Per seed

| task seed | train | collision3 test | JAX on dump | JAX float64, eps 1e-9 | T64 K8 | T128 K8 | train - test | long probe, largest of nine (draw) | family | S' reads | instr | real evals | min |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 801 | 0.510 | 0.514 | 0.5144 | 0.5144 | 0.581 | 0.557 | -0.004 | 5.87 (6) | unclassified | P1 | 17 | 834,511 | 23 |
| 802 | 0.580 | 0.517 | 0.5175 | 0.5175 | 0.573 | 0.564 | +0.063 | 3.02 (6) | unclassified | P1 | 12 | 611,236 | 19 |
| 803 | 0.642 | 0.643 | 0.6426 | 0.6426 | 0.812 | 0.808 | -0.001 | 3.23 (1) | unclassified | P1 | 17 | 818,846 | 29 |
| 804 | 0.537 | 0.521 | 0.5208 | 0.5208 | 0.578 | 0.560 | +0.016 | 6.55 (6) | decayed linear attention | neither | 11 | 611,943 | 19 |
| 805 | 0.547 | 0.517 | 0.5167 | 0.5167 | 0.566 | 0.552 | +0.030 | 1.54 (6) | unclassified | P1 | 18 | 863,976 | 83 |
| 806 | 0.529 | 0.521 | 0.5208 | 0.5208 | 0.577 | 0.556 | +0.008 | 1.02 (6) | decayed linear attention | neither | 14 | 700,853 | 19 |
| 807 | 0.642 | 0.640 | 0.6403 | 0.6403 | 0.820 | 0.802 | +0.002 | 1 (807) | unclassified | neither | 17 | 903,468 | 32 |
| 808 | 0.666 | 0.637 | 0.6371 | 0.6371 | 0.827 | 0.814 | +0.029 | 52.5 (7) | unclassified | P2 | 22 | 899,550 | 29 |

## Predictions against outcome (runs/m-plain/M_VORHERSAGE.md, committed in be1b18b before any M run)

Research agent: m-plain 0/8 above 0.90 (P = 0.85): yes (0/8).
Executing agent:
1. m-plain 0/8 above 0.90 under the conditions (P = 0.88): yes.
3. any seed of either arm with test >= 0.99 (P = 0.03): m-plain 0/8 (m-lexicase in its report).
4. m-plain 2 or more of 8 below 0.53 (P = 0.60): yes (5/8).
8. JAX within 0.002 for every seed not flagged (P = 0.80): yes.
11. both self-checks reproduce the Linux rows on epyc (P = 0.95): yes.
The remaining items (2, 5, 6, 7, 9, 10) concern m-lexicase or both arms and are answered in runs/m-lexicase/m_report.md.
