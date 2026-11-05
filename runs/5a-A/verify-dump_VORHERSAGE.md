# verify-dump prediction (written 2026-11-05 14:12 UTC, before any computation)

Question: does a JAX re-implementation give the same accuracy as Rust when it reads exactly the
Rust task data (`autoplast dump`), instead of generating its own draw? This makes the JAX step of
rule 2 in 5a_VORHERSAGE.md possible for collision3. Tooling only; search code and the hub run are untouched.

Method: new option `verify.py --task-json FILE prog.json ...`. Episodes are grouped by write length
(12 and 64 in collision3) and evaluated with the existing JAX step/read builders; accuracy = correct / queries
over all groups, divergence flag as before. Data: local release binary (same source as hub),
`autoplast dump --regime collision3 --split test` (512 standard + 256 long episodes, seed 9) and `--split train`.
Programs: verify.py references (linear attention, delta beta=0.5) and the 16 best.json of 5a-A.
Rust numbers to compare: collision3 test column in the 5a-A seed summaries and the delta beta=0.5 row.
Cost: about 5 minutes locally, no search.

Predictions:
1. delta beta=0.5 JAX on the dumped collision3 test = Rust 0.640 within 0.002. p = 0.85
2. All 16 A best programs: |JAX - Rust| <= 0.005 on collision3 test. p = 0.75
   (risk: near-ties in argmax and float32 order differences for rules with large |S|)
3. At least 14/16 within 0.002. p = 0.65
4. A seed 2 stays above 0.651 in JAX. p = 0.80
5. No A program flagged as diverged. p = 0.85

## Extension to arm B (written 2026-11-05 14:16 UTC, after the A comparison, before running B)
A matched Rust to rounding (see verify-dump_ERGEBNIS.md). B best programs carry evolved read programs.
6. All 16 B programs: |JAX - Rust| <= 0.002 on collision3 test. p = 0.80 (read path and extra ops are new risk)

## Extension to arm C (written 2026-11-05 15:29 UTC, after A and B matched, before running C)
7. All 16 C programs: |JAX - Rust| <= 0.002 on collision3 test. p = 0.90
