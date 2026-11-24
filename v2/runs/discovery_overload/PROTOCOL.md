# Pre-Registered Protocol: Experiment 2a — Discovery on `overload` and `overload48` (`discovery_overload`)

Written and committed **before** generating any data dump or running any search on task seeds `1001..1016` (`overload`) and `1101..1116` (`overload48`). The specification, references, and counting criteria are those fixed in the main `README.md`, section **"Experiment 2a: discovery on overload and overload48 (fixed 24 Nov 2026, before any run)"** (commit `14505fe`), read together with **"Literature check of 24 Nov 2026"**. This file adds only the execution details and the predictions of the executing agent. No test suite is ever loaded by the search binary.

## Frozen Method & Code

- **Search method:** `Memetic MAP-Elites v3.1`, frozen flags `--no-const-tune --max-ep-evals 22000000 --batch 1024 --st-l2 0.015`, default memory mode (`--task mem`, the collision3 code path).
- **Code:** `v2/memetic/src/main.rs` as of `14505fe` (identical to the Testbed 2 run plus the infrastructure-only checkpoint/resume of `5774c44`). **No code change** to search, mutations, archive, fitness, or any constant for this experiment.
- **Space (as on collision3):** `<= 24` instructions, `NM=4, NV=6, NS=4`, 20 ops including `Recip`, persistent matrices `persist_m <= 3`, `persist_v = 0`, `persist_identity = 1` (exported in `best.json`).
- **Pre-flight check (done before this protocol):** `autoplast_memetic --self-test` on `v2/data/collision3_train_s1.json` still gives `tr_acc=0.9353` (Kalman-2p check) and scrambled recovery `acc=0.9353`.

### Factual note on the frozen Tier 0 micro-subset (no change made)

The frozen `Task::subset(4, 4)` takes up to 4 episodes with `<= 24` writes and up to 4 with `> 24` writes. In `overload` every episode has exactly 32 writes and in `overload48` exactly 48 (`src/main.rs`, `regime_cfg`), so on both regimes the Tier 0 micro-screen consists of the **first 4 train episodes** (on collision3 it was 4 short + 4 long = 8). This is a property of the frozen code on these regimes, recorded here before any run; nothing is adapted.

## Exact Run Specification

For `overload` with $t \in \{1001,\dots,1016\}$ and `overload48` with $t \in \{1101,\dots,1116\}$ (32 runs, search seed `--seed t`), with `R` the regime:

- **Train dump** (`dumps/R_train_s{t}.json`):
  ```bash
  ./target/release/autoplast dump --regime R --split train --task-seed {t} --out v2/runs/discovery_overload/dumps/R_train_s{t}.json
  ```
- **Validation dump** (`dumps/R_val_s{2000+t}.json`, 192 episodes):
  ```bash
  ./target/release/autoplast dump --regime R --split train --task-seed {2000+t} --train-episodes 192 --out v2/runs/discovery_overload/dumps/R_val_s{2000+t}.json
  ```
- **Search** (exact frozen flags; `--threads` does not change results, bit-determinism across thread counts verified earlier):
  ```bash
  ./v2/memetic/target/release/autoplast_memetic \
    --seed {t} --no-const-tune --max-ep-evals 22000000 --batch 1024 --st-l2 0.015 \
    --train-dump v2/runs/discovery_overload/dumps/R_train_s{t}.json \
    --val-dump v2/runs/discovery_overload/dumps/R_val_s{2000+t}.json \
    --out v2/runs/discovery_overload/R/seed{t}
  ```
  The bit-exact checkpoint/resume (`--checkpoint`, `--slice-secs`; infrastructure only, verified bit-identical in `v2/runs/testbed2_901_916/PROTOCOL.md`) is used when a run exceeds the per-command time limit of the VM.
- **Post-run output per seed** (verbatim in `R/seed{t}/eval.txt`, run inside the seed directory so no paths appear):
  ```bash
  ./target/release/autoplast eval --prog best.json --regime R --task-seed {t}
  ```
- **Delivered per seed:** `best.json`, `summary.json` (with episode-evaluation counts), `eval.txt`; plus all 64 dumps. Counting, fresh draws, JAX and the long probe are done by the owner in the repository; this run reports facts only.

## Counting Criteria (from the main `README.md`, not changed here)

A seed counts as a discovery if its rule (1) beats the best reference on the regime's test by `>= 0.02` (`overload > 0.898`, `overload48 > 0.623`); (2) beats classical reference, Kalman delta and RLS with forgetting on 12 fresh draws (task seeds `101..112`, 512 train episodes) by `>= 0.01` on the mean and in `>= 10/12` draws; (3) passes `T128 K8 >= 0.838`, `train - test <= 0.03`, long probe `< 100` in all nine draws, JAX float32/float64 at ε `1e-9` within `0.02` of Rust. Discovery is shown in a regime if `>= 3/16` seeds count.

## Predictions of the Executing Agent (Written Before Any Dump or Run)

Basis: on collision3 the frozen method reached `> 0.90` in about half of the unseen seeds (Phase 3: `8/16`; Phase 5: `8/16`), i.e. roughly the level of the tuned classical reference, and the found rules were variants of the RLS/Kalman family. On `overload`/`overload48` the classical reference already sits at `0.878` / `0.603`, with headroom to the ridge ceiling of `0.077` / `0.146`. Counting requires beating the strongest RLS-family references, which the method has so far only matched.

1. **Best test of the 16 seeds above the classical reference at all** (`overload > 0.878`): `P = 0.40`; (`overload48 > 0.603`): `P = 0.30`.
2. **Criterion 1 alone** (`overload > 0.898` / `overload48 > 0.623`): expected `0..2` of 16 per regime; `P(>= 1 seed on overload) = 0.30`, `P(>= 1 seed on overload48) = 0.20`.
3. **Median test score:** `overload` about `0.80` (most seeds between `0.72` and `0.87`); `overload48` about `0.56` (most between `0.53` and `0.60`).
4. **Discovery shown (`>= 3/16` counted):** `overload P = 0.12`; `overload48 P = 0.08`; at least one counted seed in either regime `P = 0.25`.
5. **Stability:** with `--no-const-tune` as in Phase 5 (`14/16` stable), at most `3` of 16 seeds per regime fail the long probe: `P = 0.70`.
