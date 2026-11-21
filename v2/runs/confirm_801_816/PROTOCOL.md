# Pre-Registered Confirmatory Protocol (`confirm_801_816`, Frozen `no_const_tune` v3.1)

Written and frozen **before** generating any data dumps or running any seed on `task_seed` `801..816`.

## Frozen Method (`frozen` = `v3.1` with `--no-const-tune`)
Selected based on the exploratory `701..708` ablation (`ablations_v31`), where dropping inner-loop constant tuning eliminated `T=64 -> T=256` stability over-tuning (`8/8` valid, `5/8` valid `> 0.90`). All `701..708` seeds are excluded from confirmation; `801..816` are 16 completely fresh, unseen task seeds.

- Binary: `v2/memetic/target/release/autoplast_memetic` (`Memetic MAP-Elites v3.1`, bit-deterministic and thread-count invariant; zero code modifications since `ablations_v31`).
- Search space: exact `autoplast v1` D/E/K space (`<= 24` instructions, `NM=4, NV=6, NS=4`, 20 ops, `persist_m <= 3`, `persist_v = 0`, `persist_identity = 1`).
- Common flags across all 3 arms: `--no-const-tune --max-ep-evals 22000000 --batch 1024 --st-l2 0.015` (strictly equal episode-evaluation compute).
- Paired unseen task seeds ($N = 16$ per arm, 48 runs total): $t \in \{801, 802, \dots, 816\}$, where `801..808` aligns 1:1 with epyc Package M (`v1` evolution):
  - `--train-dump`: `autoplast dump --regime collision3 --split train --task-seed {t}`
  - `--val-dump`: `autoplast dump --regime collision3 --split train --task-seed {2000+t} --train-episodes 192`
  - `--seed`: `{t}`

## Three Pre-Registered Arms (Frozen Reference + 2 Single-Component Knockouts)
1. **`frozen`** *(frozen primary method)*: `--no-const-tune` (`fitness=mse`, `const_tune=false`, `archive=map_elites`, `mutations=full`).
2. **`frozen_basic_mut`** *(mutation knockout)*: `--no-const-tune --basic-mut` (disables liveness-aware register selection, residual/2-op-chain/wrap-input mutations, and length bloat shedding).
3. **`frozen_no_archive`** *(archive knockout)*: `--no-const-tune --no-archive` (replaces `(eff_len 1..24) x 5 (written, live)` MAP-Elites archive with a flat top-K archive).

## Strict Post-Hoc Audit & Statistical Decision Rule
Every seed is audited via `v2/audit_run.py` -> `v2/strict_eval.py` (exact matching `--train-task-seed t`, `space_ok`, `jax_diff_rust <= 0.01`, `eps_shift <= 0.02` in `float64` `norm_eps=1e-9`, 9-draw `T=256 < 100` stability on `K=8` plus diagnostic `K=16`, `rust_train - rust_test_col3 <= 0.03`, and 12 paired fresh draws at `gap=0` and `gap=4`).

- A seed **counts** iff `VALID == True` and `rust_test_col3 > 0.90`.
- **Pre-registered hypothesis tests (one-sided Fisher exact test, $\alpha = 0.05$, $N = 16$ per arm):**
  1. `frozen` > `frozen_basic_mut` (tests necessity of liveness-safe structural mutations).
  2. `frozen` > `frozen_no_archive` (tests necessity of the structured `(written, live)` MAP-Elites archive).
- Both full `801..816` ($N = 16$) and the Package-M overlap subset `801..808` ($N = 8$) are reported transparently.
