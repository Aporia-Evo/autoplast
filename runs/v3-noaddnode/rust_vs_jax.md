# v3-noaddnode: Rust vs JAX (verify.txt), per seed

Rust from summary.md, JAX from verify.txt (independent episodes and embeddings). a = carry coefficient of the structural fit (Rust classify.rs / JAX on real states).

| seed | family (Rust) | a Rust | a JAX | train | Rust ow0.3 | JAX ow0.3 | Rust rewrite8 T96 | JAX rewrite8 T96 | largest gap over 11 suites |
|---|---|---|---|---|---|---|---|---|---|
| 1 | linear attention | 0.958 | +0.958 | 0.814 | 0.787 | 0.778 | 0.378 | 0.407 | 0.037 (full T24) |
| 2 | gated delta rule | 1.108 | +1.108 | 0.973 | 0.967 | 0.960 | 0.023 | 0.018 | 0.026 (test d8 T6 ow0.3) |
| 3 | linear attention | 0.952 | +0.950 | 0.818 | 0.788 | 0.775 | 0.427 | 0.438 | 0.032 (full T24) |
| 4 | linear attention | 0.958 | +0.958 | 0.814 | 0.787 | 0.778 | 0.378 | 0.406 | 0.037 (full T24) |
| 5 | linear attention | 0.958 | +0.958 | 0.814 | 0.787 | 0.778 | 0.378 | 0.407 | 0.037 (full T24) |
| 6 | linear attention | 0.959 | +0.958 | 0.819 | 0.788 | 0.777 | 0.378 | 0.402 | 0.034 (full T24) |
| 7 | linear attention | 0.958 | +0.958 | 0.814 | 0.787 | 0.778 | 0.378 | 0.407 | 0.037 (full T24) |
| 8 | linear attention | 0.958 | +0.958 | 0.814 | 0.787 | 0.778 | 0.378 | 0.406 | 0.037 (full T24) |
| 9 | linear attention | 0.951 | +0.950 | 0.812 | 0.789 | 0.776 | 0.424 | 0.441 | 0.034 (full T24) |
| 10 | gated delta rule | 1.138 | +1.138 | 0.967 | 0.967 | 0.960 | 0.000 | 0.020 | 0.020 (rewrite8 T96) |
| 11 | gated delta rule | 1.134 | +1.134 | 0.965 | 0.959 | 0.954 | 0.000 | 0.020 | 0.020 (rewrite8 T96) |
| 12 | gated delta rule | 1.107 | +1.107 | 0.973 | 0.967 | 0.959 | 0.020 | 0.013 | 0.018 (full T24) |
| 13 | linear attention | 0.958 | +0.958 | 0.814 | 0.787 | 0.778 | 0.378 | 0.407 | 0.037 (full T24) |
| 14 | unclassified | 0.970 | +0.970 | 0.824 | 0.802 | 0.789 | 0.371 | 0.398 | 0.036 (full T24) |
| 15 | linear attention | 0.958 | +0.958 | 0.814 | 0.787 | 0.778 | 0.378 | 0.407 | 0.037 (full T24) |
| 16 | gated delta rule | 1.107 | +1.107 | 0.970 | 0.966 | 0.958 | 0.024 | 0.019 | 0.026 (full T24) |

Rust rewrite8 0.000 with JAX near 0.02 is the Rust overflow guard (|S| > 1e4 scores the suite 0) acting on growth factors a > 1 over 96 steps.
