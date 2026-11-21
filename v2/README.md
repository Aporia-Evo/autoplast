# autoplast v2 — Memetic MAP-Elites over the Exact Register DSL

`v2/` is a self-contained search stack built alongside the untouched `v1` baseline (`0/128` seeds `> 0.90` on `collision3`). It searches the **exact same `autoplast` D/E/K program space** (`<= 24` instructions, `NM=4, NV=6, NS=4`, 20 ops, `persist_m <= 3`, `persist_v = 0`, `persist_identity = 1`) with zero hardcoded memory rules, zero target-derived thresholds, and strict train/val/test separation.

## Method (`v2/memetic`)

Zero-dependency Rust implementation (`v2/memetic/src/main.rs`) addressing five bottlenecks identified in `v1`:

1. **Smooth MSE + threshold-free state-L2 objective:** $\mathcal{L}(P) = \mathrm{MSE}(S q, v) + \lambda_{\mathrm{st}} \cdot \mathrm{mean}(\mathrm{st}^2) + 5\times 10^{-4}\cdot |P|$ with $\lambda_{\mathrm{st}} = 0.015$, evaluated strictly on exact Rust train dumps (`autoplast dump --split train`). Final selection over the archive uses only the Rust validation dump; test suites are never loaded during search.
2. **3-tier continuous constant optimization:** Tier 0 micro-screen (8 episodes + 5-point 1D probe on modified constant), Tier 1 multi-scale coordinate search on the micro-subset, Tier 2 exact 144-episode evaluation, plus parallel 144-episode Nelder-Mead simplex polish whenever a state bucket improves its leader.
3. **Dead-code compaction & liveness-safe mutations:** Every candidate is backward-liveness compacted before mutation so dead code never blocks at length 24; residual-insert, 2-op chain residual-insert, and split-edge wrap-input mutations only allocate dead scratch registers.
4. **Generic `(written, live)` MAP-Elites archive:** `24` effective lengths $\times$ `5` generic persistent-state classes (`w1l1`, `w1l+`, `w2l2`, `w2l3`, `w3l3`) $\times$ top-4 distinct op-multisets per cell, preventing read-only `MatVec(I, k)` copies from crowding out genuinely stateful updates.
5. **Deterministic budget:** Fixed `--max-cands 300000 --batch 1024 --threads 16`.

## Reproduction

```bash
# 1. Build v1 binary (for exact data dumps & Rust evaluation) and v2 memetic binary
cargo build --release
cargo build --release --manifest-path v2/memetic/Cargo.toml

# 2. Stage-Gate 1 self-test (exact Kalman check + scrambled constant recovery + speed)
./v2/memetic/target/release/autoplast_memetic --self-test

# 3. (Optional) Re-generate exact Rust dumps in v2/data/
./target/release/autoplast dump --regime collision3 --split train --task-seed 1 --out v2/data/collision3_train_s1.json
./target/release/autoplast dump --regime collision3 --split train --task-seed 2001 --train-episodes 192 --out v2/data/collision3_val_s2001.json
./target/release/autoplast dump --regime collision3 --split train --task-seed 501 --out v2/data/collision3_train_s501.json
./target/release/autoplast dump --regime collision3 --split train --task-seed 2501 --train-episodes 192 --out v2/data/collision3_val_s2501.json
./target/release/autoplast dump --regime collision3 --split test --out v2/data/collision3_test_s9.json

# 4. Run Phase 0 fair BPTT-tuned baselines
python v2/tune_baselines_bptt.py

# 5. Run pre-registered frozen Phase 2 evaluation (8 seeds across task-seed 1 and unseen task-seed 501) + strict audit
python v2/run_frozen_phase2.py

# 6. Independent float64 / norm_eps=1e-9 verification via untouched verify/verify.py
python verify/verify.py --x64 --norm-eps 1e-9 \
  v2/runs/frozen_memetic_v1/s1/seed12/best.json \
  v2/runs/frozen_memetic_v1/s501/seed100/best.json
```

## Phase 0: Fair BPTT-Tuned Known Baselines

All known families were tuned with multi-start Adam BPTT on MSE over `v2/data/collision3_train_s1.json`, exported as exact `<= 24`-instruction `autoplast` JSONs (`v2/baselines_bptt/`), and audited via `v2/strict_eval.py`:

| Family | Instrs | `train` | **`test col3`** | JAX `x64` `1e-9` | `T128 K8` | `T256` max (`< 100`) | 12 Draws | `gap=4` |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `decayed_la` | 6 | 0.500 | 0.518 | 0.518 | 0.555 | 0.75 (ok) | 0.522 | 0.285 |
| `deltanet` | 6 | 0.618 | 0.631 | 0.631 | 0.864 | 0.73 (ok) | 0.637 | 0.366 |
| `gated_deltanet` | 10 | 0.615 | 0.635 | 0.635 | 0.835 | 1.35 (ok) | 0.640 | 0.375 |
| `decoupled_ew` | 11 | 0.617 | 0.636 | 0.636 | 0.836 | 1.10 (ok) | 0.641 | 0.377 |
| `kron_delta` | 11 | 0.509 | 0.534 | 0.534 | 0.568 | 0.60 (ok) | 0.540 | 0.299 |
| `rls_2p` (unconstrained) | 14 | 0.955 | 0.945 | 0.945 | 0.000 | `1.94e+12` (FAIL) | 0.950 | 0.948 |
| `rls_5p` (unconstrained) | 20 | 0.981 | 0.976 | 0.976 | 0.000 | `9.05e+11` (FAIL) | 0.974 | 0.909 |
| `rls_5p` (`a_s, rho <= 1`) | 20 | 0.808 | **0.794** | 0.794 | 0.244 | 2.99 (ok) | 0.791 | 0.758 |
| `kalman_2p` | 15 | 0.935 | **0.935** | 0.935 | 0.950 | 2.53 (ok) | 0.936 | 0.922 |
| `kalman_6p` (unconstrained) | 23 | 0.983 | 0.978 | 0.978 | 0.971 | `9.49e+06` (FAIL) | 0.978 | 0.927 |
| `kalman_6p` (`a_s, a_p <= 1`) | 23 | 0.943 | **0.940** | 0.940 | 0.967 | 2.80 (ok) | 0.941 | 0.885 |
| `kalman_6p` (`st_l2 = 0.01`) | 23 | 0.955 | **0.952** | 0.952 | 0.966 | 46.26 (ok) | 0.953 | 0.914 |
| *Ridge ceiling (`autoplast sweep`)* | — | — | **1.000** | — | — | — | — | — |

## Phase 2: Pre-Registered Frozen Evaluation (`v2/runs/frozen_memetic_v1/`)

Protocol pre-registered in `v2/runs/frozen_memetic_v1/PROTOCOL.md` before any test evaluation. Audited via `v2/audit_run.py` (exact Rust `autoplast eval` with matching `--task-seed` for train, JAX `x64` `norm_eps=1e-9`, 9-draw v3 `T=256 < 100` stability, and 12 paired fresh draws `101..112`):

| Arm / Seed | Instrs | `train` | **`test col3`** | JAX `x64` `1e-9` | `d32` | `T128` | `T256` 9d max (`< 100`) | 12 Draws | `gap=4` | Valid |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| `s1/seed10` | 24 | 0.992 | **0.995** | 0.995 | 1.000 | 1.000 | 3.12 | 0.994 | 0.970 | **Yes** |
| `s1/seed11` | 22 | 1.000 | **0.999** | 0.999 | 1.000 | 1.000 | 3.61 | 0.999 | 0.983 | **Yes** |
| `s1/seed12` | **19** | 1.000 | **1.000** | **1.000** | 1.000 | 1.000 | 4.08 | **1.000** | **0.997** | **Yes** |
| `s1/seed13` | 24 | 0.942 | **0.945** | 0.945 | 1.000 | 0.980 | 1.63 | 0.946 | 0.865 | **Yes** |
| `s501/seed100` *(unseen task seed)* | 23 | 1.000 | **1.000** | **1.000** | 1.000 | 1.000 | 4.22 | **1.000** | **0.998** | **Yes** |
| `s501/seed101` *(unseen task seed)* | 23 | 0.842 | 0.839 | 0.839 | 0.993 | 0.965 | 1.68 | 0.845 | 0.613 | **Yes** |
| `s501/seed102` *(unseen task seed)* | 24 | 0.850 | 0.840 | 0.840 | 0.990 | 0.646 | `1.76e+123` | 0.848 | 0.469 | **No** (unstable) |
| `s501/seed103` *(unseen task seed)* | 22 | 0.736 | 0.729 | 0.729 | 0.988 | 0.958 | 1.04 | 0.736 | 0.472 | **Yes** |

- **Result:** **7/8** strictly valid, **5/8** valid & `> 0.90` (**4/4** on `task-seed 1`, **1/4** on unseen `task-seed 501`), **4/8** reaching `0.995–1.000` (vs. `0/128` in `v1`).
- **Untouched `verify/verify.py --x64 --norm-eps 1e-9`:** `s1/seed12` scores **`1.000 ± 0.000`** on 10 of 11 suites and **`0.987 ± 0.003`** on `full d16 T24` (Kalman-2p: `0.870`, DeltaNet: `0.751`).
- **Extreme OOD (`float64`, `norm_eps = 1e-12`):** `s1/seed12` and `s501/seed100` both achieve **`1.0000`** on `T=1024` collision `K=8` (`max|st| = 3.64–3.97`; `kalman_2p`: `0.832`, `kalman_6p`: `0.836`) and **`1.0000`** on `d=64, T=48` collision (`kalman_2p`: `0.979`).

### Discovered Rule (`s1/seed12`, 19 instructions, 2 constants, no `Recip`)

With persistent matrices $S = M_0$ ($S_0 = 0$) and $P = M_2$ ($P_0 = I$; $M_1$ scratch) and $c_1 \approx 0.1676$, $c_2 \approx 6.764$:

$$p = P k, \qquad u = \frac{p}{\|p\|}, \qquad e = v - S k$$
$$P' = P - (2u - p)(p - c_1 u)^\top$$
$$S' = S + e u^\top + c_2 \, (e u^\top) (P')^3$$

Along $u$ with $r = \|P k\|$, the update $r' = r - (2 - r)(r - c_1)$ has an exact attracting non-zero fixed point at $r^* = c_1 = 0.1676$ ($|\partial r'/\partial r| = 0.832 < 1$), keeping $P$ bounded for all $T$ and $\|P k\|$ bounded strictly away from zero without `Recip` or `+ q I`.

## Phase 3: 16 Fresh Unseen Task Seeds (`v2/runs/frozen_16seeds/`, `v3.1`)

Pre-registered in `v2/runs/frozen_16seeds/PROTOCOL.md` using thread-count bit-deterministic `Memetic MAP-Elites v3.1` with exact episode-evaluation accounting (`--max-cands 300000 --batch 1024 --st-l2 0.015`). Each seed $t \in \{601,\dots,616\}$ uses its own unseen `train` dump (`task-seed t`), unseen `val` dump (`task-seed 2000+t`), and search seed `t`:

| Seed (`ts=t`) | Instrs | `pm` | `ep_evals` | `train` | **`test col3`** | JAX `x64` `1e-9` | `T128` | `T256` 9d (`K=8` / `K=16`) | 12 Draws | `gap=4` | Valid |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| `seed601` | 24 | 3 | 21.7M | 0.997 | **0.996** | 0.996 | 1.000 | 3.26 / 4.49 | 0.996 | 0.961 | **Yes** |
| `seed602` | 23 | 3 | 23.7M | 0.998 | **0.997** | 0.997 | 1.000 | 3.54 / 7.45 | 0.997 | 0.980 | **Yes** |
| `seed603` | 17 | 2 | 15.5M | 0.651 | 0.646 | 0.646 | 0.860 | 0.93 / 0.93 | 0.653 | 0.388 | **Yes** |
| `seed604` | 24 | 3 | 33.8M | 0.991 | **0.989** | 0.989 | 1.000 | 2.91 / 5.27 | 0.988 | 0.959 | **Yes** |
| `seed605` | 10 | 1 | 8.5M | 0.614 | 0.634 | 0.634 | 0.857 | 0.78 / 0.90 | 0.640 | 0.372 | **Yes** |
| `seed606` | 22 | 3 | 26.4M | 0.971 | **0.973** | 0.973 | 0.998 | 2.19 / 4.19 | 0.974 | 0.931 | **Yes** |
| `seed607` | 24 | 3 | 27.7M | 0.981 | 0.985 | 0.985 | 0.998 | `inf` / `inf` | 0.984 | 0.000 | **No** (unstable) |
| `seed608` | 24 | 3 | 22.5M | 0.697 | 0.671 | 0.671 | 0.863 | 0.89 / 1.06 | 0.679 | 0.408 | **Yes** |
| `seed609` | 13 | 3 | 9.2M | 0.649 | 0.637 | 0.637 | 0.868 | 1.00 / 1.00 | 0.643 | 0.370 | **Yes** |
| `seed610` | 8 | 1 | 8.8M | 0.646 | 0.632 | 0.632 | 0.859 | 0.86 / 0.97 | 0.638 | 0.368 | **Yes** |
| `seed611` | 23 | 2 | 26.5M | 0.708 | 0.719 | 0.719 | 0.867 | 2.18 / 2.15 | 0.734 | 0.510 | **Yes** |
| `seed612` | 24 | 2 | 23.7M | 0.988 | **0.990** | 0.990 | 1.000 | 3.40 / 4.60 | 0.988 | 0.939 | **Yes** |
| `seed613` | 23 | 2 | 20.6M | 0.994 | **0.997** | 0.997 | 1.000 | 2.94 / 3.50 | 0.997 | 0.979 | **Yes** |
| `seed614` | 24 | 2 | 12.7M | 0.992 | 0.994 | 0.994 | 1.000 | `3.0e18` / `8.0e25` | 0.993 | 0.954 | **No** (unstable) |
| `seed615` | 24 | 2 | 10.4M | 0.980 | **0.982** | 0.982 | 1.000 | 2.18 / 2.88 | 0.983 | 0.954 | **Yes** |
| `seed616` | 24 | 2 | 10.7M | 0.934 | **0.941** | 0.941 | 1.000 | 1.00 / 1.20 | 0.943 | 0.851 | **Yes** |

- **Aggregate (`N = 16` unseen task seeds):**
  - **14/16 (87.5%)** strictly valid; **8/16 (50.0%)** strictly valid & `> 0.90` (vs. `0/128` in `v1`); **7/16 (43.8%)** valid & beating every stable BPTT baseline (`> 0.952`); **4/16 (25.0%)** valid & `>= 0.990`.
  - Valid median `test col3` = **0.957** (IQR `0.646–0.990`); valid median 12-draw mean = **0.959** (IQR `0.653–0.988`).
  - **Compute:** median **21.17M** total episode evaluations (range `8.55M–33.80M`, mean `18.90M`), vs. `~288M` nominal episode evaluations for `v1`'s 2M-candidate budget (`0/128`).
  - **Structure & stability:** All 8 valid `> 0.90` rules are **`Recip`-free** (`0/8` use `Recip`, `8/8` use `Normalize`), show `0.000` `eps_shift` (`1e-6` vs `1e-9`), and stay strictly bounded even at `T=256, K=16` (`1.20–7.45` across 9 draws).
  - **Untouched `verify/verify.py --x64 --norm-eps 1e-9`:** `seed613` and `seed602` score `1.000 ± 0.000` on 7/11 suites, `0.994–0.998` on `collision`/`clustered`, and `0.952–0.964` on `full d16 T24`.

## Phase 4: Compute-Fair 5-Arm Component Ablation (`v2/runs/ablations_v31/`, `v3.1`)

Pre-registered in `v2/runs/ablations_v31/PROTOCOL.md`. All 5 arms run on the exact same 8 completely fresh unseen task seeds (`701..708`) with **strictly equal episode-evaluation budget** (`--max-ep-evals 22000000`, matching the `21.17M` median of Phase 3) and undergo the identical post-hoc strict audit:

| Arm (`701..708`, `22.1M ep_evals`) | `raw > 0.90` | **Valid** | **Valid & `> 0.90`** | `Valid & >= 0.99` | Med `raw` | Med `eff` *(invalid=0)* | Med `cands` | Med `ep_evals` |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| **`no_const_tune`** (`--no-const-tune`) | **5/8** | **8/8** | **5/8 (62.5%)** | **3/8** | **0.982** | **0.982** | 2,295k | 22.14M |
| **`acc_fitness`** (`--fitness acc`) | 3/8 | **8/8** | **3/8 (37.5%)** | **3/8** | 0.704 | 0.704 | 252k | 22.17M |
| **`full`** *(v3.1 default)* | **5/8** | 3/8 *(5 unstab)* | **2/8 (25.0%)** | 2/8 | 0.970 | 0.000 | 396k | 22.15M |
| **`no_archive`** (`--no-archive`) | 3/8 | 4/8 *(4 unstab, 1 eps)* | **1/8 (12.5%)** | 0/8 | 0.659 | 0.321 | 492k | 22.03M |
| **`basic_mut`** (`--basic-mut`) | **0/8** | 8/8 | **0/8 (0.0%)** | 0/8 | 0.639 | 0.639 | 1,202k | 22.14M |

### Statistical Reading (Strictly Against Pre-Registered Reference `full`)
- **Pre-registered test (`N = 8`, one-sided Fisher exact against `full`, $\alpha = 0.05$):** **No single component reaches statistical significance on `701..708`**, largely because `full` itself was weakened by 5/8 unstable rules (`2/8` valid `> 0.90`):
  - `no_const_tune` (`5/8`) vs. `full` (`2/8`): $p = 0.16$ (n.s.)
  - `basic_mut` (`0/8`) vs. `full` (`2/8`): $p = 0.23$ (n.s.)
  - `no_archive` (`1/8`) vs. `full` (`2/8`): $p = 0.50$ (n.s.)
  - `acc_fitness` (`3/8`) vs. `full` (`2/8`): $p = 0.50$ (n.s.)
- **Post-hoc / exploratory observations (not confirmatory; task seeds `701..708` are now spent):**
  - Re-anchoring post-hoc on `no_const_tune` (`5/8` valid `> 0.90`, `8/8` stable) gives $p = 0.013$ for `basic_mut` (`0/8`) and $p = 0.059$ for `no_archive` (`1/8`, plus an epsilon-trick caught on `seed706`: `te=0.999` → `e9=0.014`).
  - Plausible hypothesis to confirm on fresh seeds (`801..816`): inner-loop constant tuning on `T=64` pushes rules across the `T=256` stability boundary (Rule 3), while liveness-safe structural mutations (and potentially the MAP-Elites archive) drive the breakthrough under equal `22M ep_evals`.
- **Descriptive note:** Across Phases 2, 3, and 4 combined, 24/24 strictly valid `> 0.90` discoveries use `Normalize` and 0/24 use `Recip`.

## Layout

- `v2/memetic/` — Zero-dependency Rust Memetic MAP-Elites search `v3.1` (`Cargo.toml`, `src/main.rs`)
- `v2/strict_eval.py` — Unified strict auditor (space check, Rust eval, JAX `x64`/`1e-9`, 9-draw v3 `T=256 < 100` + `K=16`, 12 fresh draws)
- `v2/audit_run.py` — Post-hoc batch auditor over `seed*/best.json`
- `v2/tune_baselines_bptt.py` — Phase 0 fair BPTT baseline tuner
- `v2/run_frozen_phase2.py` — Reproduces the pre-registered Phase 2 run & audit
- `v2/run_frozen_16seeds.py` — Reproduces the pre-registered Phase 3 16-seed unseen-task run & audit (`601..616`)
- `v2/run_ablations_v31.py` — Reproduces the pre-registered Phase 4 compute-fair 5-arm ablation & audit (`701..708`)
- `v2/data/` — Exact Rust `autoplast dump` JSONs (`s1`, `s2001`, `s501`, `s2501`, `s9`; `seeds_*/` auto-generated and gitignored)
- `v2/baselines_bptt/` — Compiled `<= 24`-instruction BPTT-tuned baseline JSONs and `baselines_summary.json`
- `v2/runs/frozen_memetic_v1/` — Phase 2 `PROTOCOL.md`, 8 counted `seed*/{best,summary}.json`, and `strict_audit.json`
- `v2/runs/frozen_16seeds/` — Phase 3 `PROTOCOL.md`, 16 unseen-task `seed*/{best,summary,meta}.json`, and `strict_audit.json`
- `v2/runs/ablations_v31/` — Phase 4 `PROTOCOL.md`, 5 arms × 8 unseen-task `seed*/{best,summary,meta}.json`, and per-arm `strict_audit.json`
