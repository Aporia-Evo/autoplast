# Pre-Registered 16-Seed Unseen-Task Evaluation Protocol (`frozen_16seeds`, `v3.1`)

Written and frozen **before** evaluating any `task_seed` `601..616` on any test suite (a partial `v3.0` run `601..610` was discarded untested when `v3.1` added thread-independent determinism, exact `ep_evals` accounting, and opt-in ablation flags, so all 16 counted seeds come cleanly from the single frozen `v3.1` binary).

## Method (Strictly Frozen `v3.1` Default)
- Binary: `v2/memetic/target/release/autoplast_memetic` (`Memetic MAP-Elites v3.1`, source: `v2/memetic/src/main.rs`).
- Search space: exact `autoplast v1` D/E/K space (`<= 24` instructions, `NM=4, NV=6, NS=4`, 20 ops, `persist_m <= 3`, `persist_v = 0`, `persist_identity = 1`).
- Fixed flags: `--max-cands 300000 --batch 1024 --threads 16 --st-l2 0.015` (default `fitness=mse`, `const_tune=true`, `archive=map_elites`, `mutations=full`), logging exact `train_ep_evals`, `val_ep_evals`, `total_ep_evals`, and `train_write_steps` per seed.
- Strict train/val/test separation: each run reads only its own `--train-dump` and `--val-dump`; test suites are never loaded during search.

## Counted Seeds (16 Completely Fresh, Unseen Task Seeds)
For every $t \in \{601, 602, \dots, 616\}$ (16 independent task draws, never used during development, baseline tuning, or Phase 2):
- `--train-dump`: `autoplast dump --regime collision3 --split train --task-seed {t}`
- `--val-dump`: `autoplast dump --regime collision3 --split train --task-seed {2000+t} --train-episodes 192`
- `--seed`: `{t}`
- Output directory: `v2/runs/frozen_16seeds/seed{t}/` (`best.json`, `summary.json`, `meta.json`)

## Strict Post-Hoc Audit Criteria (via `v2/audit_run.py` -> `v2/strict_eval.py`)
A seed counts as a valid discovery (`VALID=True`) ONLY if its compiled `best.json` passes ALL of:
1. `space_ok == True` (`<= 24` instrs, `NM=4, NV=6, NS=4`, 20 allowed ops, `persist_m <= 3`, `persist_v == 0`).
2. `jax_diff_rust <= 0.01` (exact agreement between Rust `autoplast eval` and independent JAX `float64` evaluator on `v2/data/collision3_test_s9.json`).
3. `eps_shift <= 0.02` (`norm_eps=1e-6` vs `1e-9` in `float64`, plus `verify/eps_scale.py` check if triggered).
4. `stable_lt100 == True` (v3 stability bound across 9 independent draws: 64 eps x 256 write steps on both standard `K=8` and collision `K=8` in `float64`, every persistent entry `< 100`). Additionally logged diagnostically: 9-draw `T=256, K=16` collision max (`t256_k16_col_max`).
5. `rust_train - rust_test_col3 <= 0.03`, where `rust_train` is evaluated on the exact matching `--task-seed {t}`.
6. Paired 12 fresh draws (`task_seed 101..112`) at `query_gap=0` and `query_gap=4`, plus independent `verify/verify.py --x64 --norm-eps 1e-9` confirmation on top passing rules.

## Primary Reported Metrics
- Valid rate: `#VALID / 16`
- Breakthrough rate (`> 0.90`): `#(VALID and test_col3 > 0.90) / 16`
- Near-ceiling rate (`>= 0.99`): `#(VALID and test_col3 >= 0.99) / 16`
- Median and IQR of `test_col3` and `12-draw mean` across all 16 seeds (and across valid seeds), compared against `v1` (`0/128 > 0.90`) and stable BPTT-tuned baselines (`kalman_2p: 0.935`, `kalman_6p st_l2=0.01: 0.952`).
