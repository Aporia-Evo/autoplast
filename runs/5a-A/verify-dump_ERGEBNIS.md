# verify-dump result (written 2026-11-05 14:17 UTC)

Prediction: verify-dump_VORHERSAGE.md (written before computing). New option `verify.py --task-json`
loads the exact Rust collision3 test data from `autoplast dump --regime collision3 --split test`
(local release binary; 768 episodes, 6,503 queries; file runs/5a-A/collision3_test.json).
Rust values are the 3-decimal numbers in the hub seed summaries, so |diff| <= 0.0005 is pure rounding.

References: delta beta=0.5 JAX 0.6402 (Rust 0.640), linear attention JAX 0.3852.

## Arm A (16 best programs)
| seed | delta reached | Rust collision3 test | JAX on dumped data | diff |
|---|---|---|---|---|
| 1 | no | 0.509 | 0.5093 | +0.0003 |
| 2 | yes | 0.660 | 0.6597 | -0.0003 |
| 3 | no | 0.511 | 0.5115 | +0.0005 |
| 4 | no | 0.517 | 0.5175 | +0.0005 |
| 5 | yes | 0.640 | 0.6397 | -0.0003 |
| 6 | no | 0.517 | 0.5167 | -0.0003 |
| 7 | no | 0.506 | 0.5064 | +0.0004 |
| 8 | yes | 0.640 | 0.6399 | -0.0001 |
| 9 | no | 0.516 | 0.5158 | -0.0002 |
| 10 | no | 0.509 | 0.5093 | +0.0003 |
| 11 | yes | 0.642 | 0.6417 | -0.0003 |
| 12 | yes | 0.648 | 0.6482 | +0.0002 |
| 13 | yes | 0.635 | 0.6348 | -0.0002 |
| 14 | no | 0.509 | 0.5093 | +0.0003 |
| 15 | yes | 0.634 | 0.6340 | +0.0000 |
| 16 | no | 0.517 | 0.5165 | -0.0005 |

Max |diff| 0.0005. No program flagged as diverged.

## Arm B (16 best programs, evolved read programs, extra ops)
| seed | delta reached | Rust collision3 test | JAX on dumped data | diff |
|---|---|---|---|---|
| 1 | no | 0.524 | 0.5236 | -0.0004 |
| 2 | yes | 0.636 | 0.6363 | +0.0003 |
| 3 | no | 0.515 | 0.5145 | -0.0005 |
| 4 | yes | 0.638 | 0.6382 | +0.0002 |
| 5 | no | 0.519 | 0.5188 | -0.0002 |
| 6 | yes | 0.621 | 0.6211 | +0.0001 |
| 7 | no | 0.521 | 0.5207 | -0.0003 |
| 8 | no | 0.518 | 0.5179 | -0.0001 |
| 9 | no | 0.516 | 0.5164 | +0.0004 |
| 10 | no | 0.516 | 0.5161 | +0.0001 |
| 11 | no | 0.521 | 0.5213 | +0.0003 |
| 12 | yes | 0.640 | 0.6396 | -0.0004 |
| 13 | no | 0.517 | 0.5175 | +0.0005 |
| 14 | no | 0.514 | 0.5141 | +0.0001 |
| 15 | no | 0.521 | 0.5207 | -0.0003 |
| 16 | no | 0.521 | 0.5213 | +0.0003 |

Max |diff| 0.0005. No program flagged as diverged.

## Predictions
1. delta beta=0.5 within 0.002 of 0.640 (p 0.85): correct (0.6402).
2. all 16 A within 0.005 (p 0.75): correct (max 0.0005).
3. at least 14/16 A within 0.002 (p 0.65): correct (16/16).
4. A seed 2 above 0.651 in JAX (p 0.80): correct (0.6597).
5. no A program diverged (p 0.85): correct.
6. all 16 B within 0.002 (p 0.80, added before running B): correct (max 0.0005).

## Meaning
On identical data the JAX interpreter reproduces Rust to rounding, including evolved read programs.
The earlier JAX deviations on collision suites (about 0.03) came from verify.py drawing its own embeddings,
not from an interpreter difference. The JAX step of rule 2 can now be done on the exact collision3 test.
The T128 K8 suite is not part of the dump (it has no regime); its JAX check stays with the standard verify.py suites.
