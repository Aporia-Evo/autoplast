# Pre-Registered Compute-Fair Component Ablation Protocol (`ablations_v31`)

Written and frozen **before** generating any data dumps or running any ablation seed for `task_seed` `701..708`.

## Goal
Quantify the causal contribution of each of the four core design components of `Memetic MAP-Elites v3.1` under **strictly equal episode-evaluation compute** (`--max-ep-evals 22000000`, matching the `21.17M` median compute of `frozen_16seeds`), paired across 8 completely fresh unseen task seeds.

## Fixed Setup (`Memetic MAP-Elites v3.1`)
- Binary: `v2/memetic/target/release/autoplast_memetic` (`v3.1`, thread-count bit-deterministic).
- Search space: exact `autoplast v1` D/E/K space (`<= 24` instructions, `NM=4, NV=6, NS=4`, 20 ops, `persist_m <= 3`, `persist_v = 0`, `persist_identity = 1`).
- Common flags across all 5 arms: `--max-ep-evals 22000000 --batch 1024 --st-l2 0.015`.
- Paired unseen task seeds ($N = 8$ per arm, 40 runs total): $t \in \{701, 702, 703, 704, 705, 706, 707, 708\}$, each with:
  - `--train-dump`: `autoplast dump --regime collision3 --split train --task-seed {t}`
  - `--val-dump`: `autoplast dump --regime collision3 --split train --task-seed {2000+t} --train-episodes 192`
  - `--seed`: `{t}`

## Five Counted Arms (Single-Component Knockouts vs. Paired `full`)
1. **`full`** *(baseline `v3.1`)*: default flags (`fitness=mse`, `const_tune=true`, `archive=map_elites`, `mutations=full`).
2. **`no_const_tune`**: `--no-const-tune` (disables Tier-0 1D probe, Tier-1 coordinate search, and leader Nelder-Mead; spends the full `22M ep_evals` on structural search).
3. **`acc_fitness`**: `--fitness acc` (discrete accuracy objective instead of smooth MSE + `st_l2`).
4. **`no_archive`**: `--no-archive` (flat top-K archive instead of `(eff_len 1..24) x 5 (written, live)` MAP-Elites buckets).
5. **`basic_mut`**: `--basic-mut` (unconstrained basic point mutations instead of liveness-safe residual / 2-op chain / split-edge mutations).

## Strict Post-Hoc Audit (Identical Across All 5 Arms)
Every arm is audited via `v2/audit_run.py` -> `v2/strict_eval.py` with exact matching `--train-task-seed t`, `space_ok`, `jax_diff_rust <= 0.01`, `eps_shift <= 0.02` (`x64`, `1e-9`), 9-draw `T=256 < 100` stability (`K=8` + diagnostic `K=16`), `rust_train - rust_test_col3 <= 0.03`, and 12 paired fresh draws (`gap=0`, `gap=4`).

## Primary Comparison Metrics (Per Arm)
- Strictly valid rate: `#VALID / 8`
- Breakthrough rate (`> 0.90`): `#(VALID and test_col3 > 0.90) / 8`
- Median `test_col3` (all 8 seeds & valid seeds), median 12-draw mean, and paired per-seed delta vs. `full`.
- Actual `total_ep_evals` and `total_cands` per arm (confirming equal episode-evaluation budget).
