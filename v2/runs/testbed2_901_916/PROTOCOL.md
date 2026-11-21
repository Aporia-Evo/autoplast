# Pre-Registered Protocol: Testbed 2 Counted Run (`testbed2_901_916`)

Written and committed **before** generating any data dump or running any search on unseen task seeds `901..916`. No test suite (`seed 99`, suites 1..7) is ever loaded by the search binary.

## Frozen Method & Code Commit

- **Frozen search method:** `Memetic MAP-Elites v3.1` (`--no-const-tune --max-ep-evals 22000000 --batch 1024 --st-l2 0.015`), frozen from commit `71d7948` after confirmatory Phase 5 (`v2/runs/confirm_801_816/`).
- **Adapter commit:** `ec5c13f` (`ec5c13fd788868185964bcc877b72122ea50e8e5`) on branch `v2`. Implements exclusively the five Testbed 2 interface adaptations documented in `v2/README.md` (Testbed 2 dump loader, `V0`/`V1`/`M0`/`V2`/`V3` register convention with zero start, `VecRecip` and `VecSqrt` ops, `log10(f(w_T)/f(w_0))` objective clipped to `[-10, 3]` with `3.0` on `|w_i| >= 1e4` or non-finite plus frozen `0.015 * mean(state^2)` and `5e-4 * len`, and backward liveness from `V0` over persistent slots `M0, V2, V3`). No mutations, archive dimensions, selection weights, gates, constants, or budgets were modified or tuned on Testbed 2.
- **Stage-Gate verification completed prior to this protocol (Task-Seed 1 only):**
  - `v2/memetic` evaluator agrees to `0.000000` (requirement `<= 1e-4`) with `autoplast evalmany --task opt --opt-ops --persist-v 2 --task-seed 1` on all four ladder references (`SGD: -2.013423`, `momentum: -2.613973`, `RMSProp: -2.716799`, `Adam: -3.130259`).
  - Bit-determinism verified across `--threads 1`, `2`, and `4` on `--task opt`.
  - One uncounted trial run (`seed 1`, `val 2001`, 192 episodes, 22M `ep_evals`, no test suites evaluated) completed in `336s` (`train_raw = -3.3376`, `val_raw = -3.3742`, matching `autoplast evalmany --split train --task-seed 1` to `0.000000`).

## Exact Run Specification (`t = 901..916`)

For each unseen task seed $t \in \{901, 902, \dots, 916\}$ (16 runs total, search seed `--seed t`):

- **Train dump** (`dumps/opt_train_s{t}.json`, 128 episodes, `d=16, T=50`):
  ```bash
  ./target/release/autoplast dump --task opt --split train --task-seed {t} --out v2/runs/testbed2_901_916/dumps/opt_train_s{t}.json
  ```
- **Validation dump** (`dumps/opt_val_s{2000+t}.json`, 192 episodes, `d=16, T=50`):
  ```bash
  ./target/release/autoplast dump --task opt --split train --task-seed {2000+t} --train-episodes 192 --out v2/runs/testbed2_901_916/dumps/opt_val_s{2000+t}.json
  ```
- **Search command** (exact frozen flags):
  ```bash
  ./v2/memetic/target/release/autoplast_memetic \
    --task opt --seed {t} --no-const-tune --max-ep-evals 22000000 --batch 1024 --st-l2 0.015 \
    --train-dump v2/runs/testbed2_901_916/dumps/opt_train_s{t}.json \
    --val-dump v2/runs/testbed2_901_916/dumps/opt_val_s{2000+t}.json \
    --out v2/runs/testbed2_901_916/seed{t}
  ```
- **Post-run evaluation per seed** (recorded verbatim in `seed{t}/eval.txt` and `seed{t}/structure.txt`):
  ```bash
  ./target/release/autoplast eval --task opt --opt-ops --prog best.json --task-seed {t}
  python verify/opt_structure.py --task-json ../dumps/opt_train_s{t}.json best.json
  ```

## Counting Criteria (Pre-Registered in Main `README.md`)

Final counts are verified independently in the repository from `autoplast eval --task opt --opt-ops` and `verify/opt_structure.py`:

1. **Adam-level criterion:**
   - Suite 1 (`test opt train-distribution`) mean objective `<= -3.023` (tuned Adam `-3.073 + 0.05`);
   - `0` diverged episodes on **every** held-out suite (`train-distribution`, `kappa=1000`, `d=32`, `d=8`, `sigma=0.3`, `T=200`, `scale 10 / 0.1`);
   - `train - Suite 1 <= 0.1` (and no severe train overfitting).
2. **Structural rediscovery:** Each final `best.json` is classified on its own train dump by `verify/opt_structure.py` (`R^2 >= 0.95` to simplest of `SGD < momentum < RMSProp < Adam`, else `unclassified`).

## Pre-Run Predictions (Written Before Any `901..916` Run)

Because train and validation episodes use fixed `T = 50`, `d = 16`, `kappa in {10, 100}`, and `scale = 1.0`, reaching strong performance on Suite 1 is expected to be common, while surviving the unseen OOD `scale x10 / x0.1` and `T = 200` suites with `0%` divergence is the primary filter:

1. **Raw Suite 1 level (`Suite 1 <= -3.023`, ignoring OOD divergence):**
   - Expected median: `11` to `14` of `16` seeds.
   - `P(>= 10/16 reach Suite 1 <= -3.023) = 0.75`.
2. **Full Adam-level criterion (`Suite 1 <= -3.023`, `0` divergence on all 7 suites including `T=200` and `scale`, `train - Suite 1 <= 0.1`):**
   - Many strong rules on `scale = 1` will likely diverge on `scale x10` unless they organically incorporate scale-stabilizing operations (`Normalize`, `Tanh`, or `VecRecip(VecSqrt(...))`).
   - `P(>= 8/16 pass full Adam-level criterion) = 0.30`.
   - `P(>= 4/16 pass full Adam-level criterion) = 0.65`.
   - `P(>= 1/16 passes full Adam-level criterion) = 0.90`.
3. **Train-to-Suite-1 generalization:**
   - `P(>= 14/16 have |train - Suite 1| <= 0.1) = 0.80`.
4. **Structural rediscovery (`verify/opt_structure.py`, `R^2 >= 0.95`):**
   - At 22M episode evaluations and length up to 24 with `Normalize`, `Tanh`, `Norm`, `Dot`, `VecSqrt`, and `VecRecip` available, evolved rules tend to combine multiple nonlinearities and score below `0.95` linear `R^2` against canonical ladder forms (as in the uncounted Task-Seed 1 trial run).
   - `P(>= 10/16 classified as unclassified) = 0.70`.
   - `P(>= 2/16 classified as momentum) = 0.35`; `P(>= 1/16 RMSProp) = 0.30`; `P(>= 1/16 Adam) = 0.20`.

## Infrastructure Amendment (Checkpoint/Resume Only, Zero Search Change)

While executing `901..916` on a 2-core Linux VM with a hard ~9m50s per-command timeout, `seed901`–`seed905` completed uninterrupted (`230s`–`562s` on 2 threads), whereas `seed906` exceeded the 9m50s command deadline. Following the repository's existing precedent (`README.md`, 20 Nov amendment for `verify/grow.py`), bit-exact binary checkpoint/resume (`--checkpoint`, `--slice-secs`) was added to `v2/memetic/src/main.rs` and `v2/run_testbed2_901_916.py` to serialize and restore exact batch-boundary state (`master_rng`, `archive`, `seen_structs`, `polished_leaders`, counters, `batch_idx`, `wall_secs`).

- **Zero change to the search method, RNG stream, evaluation, mutations, archive, selection, or stopping criterion.**
- **Bit-identity test (Task-Seed 1, 500k `ep_evals`, interrupted across 2 checkpoints at `--slice-secs 3`):** `best.json` and every field of `summary.json` (except `wall_seconds`) are bit-for-bit identical to an uninterrupted run (`diff` empty).

