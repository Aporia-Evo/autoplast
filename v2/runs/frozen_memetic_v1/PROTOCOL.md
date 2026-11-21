# Pre-Registered Phase 2 Frozen Protocol (`frozen_memetic_v1`)

Written and frozen **before** running any Phase 2 seed and **before** evaluating any `v2/memetic` output on `collision3_test_s9.json` or any test suite.

## Method (Frozen)
- Binary: `v2/memetic/target/release/autoplast_memetic.exe` (source: `v2/memetic/src/main.rs`)
- Search space: exact `autoplast v1` D/E/K space (`<= 24` instructions, `NM=4, NV=6, NS=4`, 20 ops, `persist_m <= 3`, `persist_v = 0`, `persist_identity = 1`).
- Objective: threshold-free `MSE(S q, v) + 0.015 * mean(st^2) + 5e-4 * len` (strictly on `--train-dump`, final archive selection strictly on `--val-dump`).
- Archive: MAP-Elites over `(eff_len 1..24) x (5 generic (written, live) state classes) x top-4 distinct op-multisets`.
- Optimization: 3-tier funnel (Tier 0: 8-ep screen + 1D probe on modified const; Tier 1: 8-ep multi-scale coordinate search; Tier 2: exact 144-ep eval; parallel 144-ep Nelder-Mead polish on new bucket leaders).
- Fixed deterministic stopping criterion: `--max-cands 300000 --batch 1024 --threads 16 --st-l2 0.015`.

## Counted Seeds (8 completely fresh seeds, 2 task-seed arms)
1. **Arm A (`frozen_s1`, direct `v1` comparison on task-seed 1):**
   - `--train-dump v2/data/collision3_train_s1.json`
   - `--val-dump v2/data/collision3_val_s2001.json`
   - Search seeds: `10, 11, 12, 13` (none used during dev).
2. **Arm B (`frozen_s501`, completely unseen task-seed 501):**
   - `--train-dump v2/data/collision3_train_s501.json`
   - `--val-dump v2/data/collision3_val_s2501.json`
   - Search seeds: `100, 101, 102, 103` (neither task seed nor search seeds ever seen during dev or baseline tuning).

## Strict Post-Hoc Audit Criteria (via `v2/audit_run.py` -> `v2/strict_eval.py`)
A seed counts as a valid discovery ONLY if its compiled `best.json` passes ALL of:
1. `space_ok == True` (`<= 24` instrs, `NM=4, NV=6, NS=4`, 20 allowed ops, `persist_m <= 3`, `persist_v == 0`).
2. `jax_diff_rust <= 0.01` (exact agreement between Rust `autoplast.exe eval` and independent JAX `float64` evaluator on `v2/data/collision3_test_s9.json`).
3. `eps_shift <= 0.02` (`norm_eps=1e-6` vs `1e-9` in `float64`, plus `verify/eps_scale.py` check if triggered).
4. `stable_lt100 == True` (v3 stability bound: 64 eps x 256 write steps on both standard K=8 and collision K=8 in `float64`, all persistent entries `< 100`).
5. `rust_train - rust_test_col3 <= 0.03` (no train/test overfitting gap).
6. Comparison against fair BPTT-tuned stable baselines (`kalman_2p: 0.935`, `kalman_6p contractive: 0.940`, `kalman_6p st_l2=0.01: 0.952`, `deltanet: 0.631`, `v1: 0/128 > 0.90`, `ridge ceiling: 1.000`) including 12 paired fresh draws (`task_seed 101..112`) at `query_gap=0` and `query_gap=4`.
