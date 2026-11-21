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

Protocol pre-registered in `v2/runs/frozen_memetic_v1/PROTOCOL.md` before any test evaluation. Audited via `v2/audit_run.py` (exact Rust `autoplast eval`, JAX `x64` `norm_eps=1e-9`, v3 `T=256 < 100` stability, and 12 paired fresh draws `101..112`):

| Arm / Seed | Instrs | `train` | **`test col3`** | JAX `x64` `1e-9` | `d32` | `T128` | `T256` max (`< 100`) | 12 Draws | `gap=4` | Valid |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| `s1/seed10` | 24 | 0.992 | **0.995** | 0.995 | 1.000 | 1.000 | 3.01 | 0.994 | 0.970 | **Yes** |
| `s1/seed11` | 22 | 1.000 | **0.999** | 0.999 | 1.000 | 1.000 | 3.61 | 0.999 | 0.983 | **Yes** |
| `s1/seed12` | **19** | 1.000 | **1.000** | **1.000** | 1.000 | 1.000 | 3.89 | **1.000** | **0.997** | **Yes** |
| `s1/seed13` | 24 | 0.942 | **0.945** | 0.945 | 1.000 | 0.980 | 1.63 | 0.946 | 0.865 | **Yes** |
| `s501/seed100` *(unseen task seed)* | 23 | 0.999 | **1.000** | **1.000** | 1.000 | 1.000 | 4.01 | **1.000** | **0.998** | **Yes** |
| `s501/seed101` *(unseen task seed)* | 23 | 0.834 | 0.839 | 0.839 | 0.993 | 0.965 | 1.68 | 0.845 | 0.613 | **Yes** |
| `s501/seed102` *(unseen task seed)* | 24 | 0.839 | 0.840 | 0.840 | 0.990 | 0.646 | `1.72e+120` | 0.848 | 0.469 | **No** (unstable) |
| `s501/seed103` *(unseen task seed)* | 22 | 0.721 | 0.729 | 0.729 | 0.988 | 0.958 | 1.04 | 0.736 | 0.472 | **Yes** |

- **Result:** **7/8** strictly valid, **5/8** valid & `> 0.90` (**4/4** on `task-seed 1`, **1/4** on unseen `task-seed 501`), **4/8** reaching `0.995–1.000` (vs. `0/128` in `v1`).
- **Untouched `verify/verify.py --x64 --norm-eps 1e-9`:** `s1/seed12` scores **`1.000 ± 0.000`** on 10 of 11 suites and **`0.987 ± 0.003`** on `full d16 T24` (Kalman-2p: `0.870`, DeltaNet: `0.751`).
- **Extreme OOD (`float64`, `norm_eps = 1e-12`):** `s1/seed12` and `s501/seed100` both achieve **`1.0000`** on `T=1024` collision `K=8` (`max|st| = 3.64–3.97`; `kalman_2p`: `0.832`, `kalman_6p`: `0.836`) and **`1.0000`** on `d=64, T=48` collision (`kalman_2p`: `0.979`).

### Discovered Rule (`s1/seed12`, 19 instructions, 2 constants, no `Recip`)

With persistent matrices $S = M_0$ ($S_0 = 0$) and $P = M_2$ ($P_0 = I$; $M_1$ scratch) and $c_1 \approx 0.1676$, $c_2 \approx 6.764$:

$$p = P k, \qquad u = \frac{p}{\|p\|}, \qquad e = v - S k$$
$$P' = P - (2u - p)(p - c_1 u)^\top$$
$$S' = S + e u^\top + c_2 \, (e u^\top) (P')^3$$

Along $u$ with $r = \|P k\|$, the update $r' = r - (2 - r)(r - c_1)$ has an exact attracting non-zero fixed point at $r^* = c_1 = 0.1676$ ($|\partial r'/\partial r| = 0.832 < 1$), keeping $P$ bounded for all $T$ and $\|P k\|$ bounded strictly away from zero without `Recip` or `+ q I`.

## Layout

- `v2/memetic/` — Frozen zero-dependency Rust Memetic MAP-Elites search (`Cargo.toml`, `src/main.rs`)
- `v2/strict_eval.py` — Unified strict auditor (space check, Rust eval, JAX `x64`/`1e-9`, v3 `T=256 < 100`, 12 fresh draws)
- `v2/audit_run.py` — Post-hoc batch auditor over `seed*/best.json`
- `v2/tune_baselines_bptt.py` — Phase 0 fair BPTT baseline tuner
- `v2/run_frozen_phase2.py` — Reproduces the pre-registered Phase 2 run & audit
- `v2/data/` — Exact Rust `autoplast dump` JSONs (`s1`, `s2001`, `s501`, `s2501`, `s9`)
- `v2/baselines_bptt/` — Compiled `<= 24`-instruction BPTT-tuned baseline JSONs and `baselines_summary.json`
- `v2/runs/frozen_memetic_v1/` — `PROTOCOL.md`, all 8 counted `seed*/{best,summary}.json`, and `strict_audit.json`
