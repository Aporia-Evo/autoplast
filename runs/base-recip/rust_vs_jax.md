# base-recip (run as v3, renamed on merge): Rust vs JAX (verify.txt), per seed

Rust from summary.md, JAX from verify.txt (independent episodes and embeddings). a = carry coefficient of the structural fit (Rust classify.rs / JAX on real states).

| seed | family (Rust) | a Rust | a JAX | train | Rust ow0.3 | JAX ow0.3 | Rust rewrite8 T96 | JAX rewrite8 T96 | largest gap over 11 suites |
|---|---|---|---|---|---|---|---|---|---|
| 1 | linear attention | 0.951 | +0.949 | 0.817 | 0.789 | 0.775 | 0.431 | 0.440 | 0.031 (full T24) |
| 2 | linear attention | 0.958 | +0.958 | 0.814 | 0.787 | 0.778 | 0.378 | 0.406 | 0.037 (full T24) |
| 3 | unclassified | 1.114 | +1.114 | 0.969 | 0.965 | 0.958 | 0.020 | 0.017 | 0.025 (test d8 T6 ow0.3) |
| 4 | gated delta rule | 1.097 | +1.098 | 0.967 | 0.961 | 0.955 | 0.018 | 0.020 | 0.057 (clustered8 T48) |
| 5 | gated delta rule | 1.125 | +1.125 | 0.971 | 0.963 | 0.952 | 0.000 | 0.011 | 0.022 (full T24) |
| 6 | linear attention | 0.956 | +0.956 | 0.821 | 0.785 | 0.769 | 0.381 | 0.408 | 0.027 (full T24) |
| 7 | linear attention | 0.951 | +0.949 | 0.817 | 0.789 | 0.775 | 0.431 | 0.440 | 0.031 (full T24) |
| 8 | linear attention | 0.952 | +0.950 | 0.817 | 0.788 | 0.775 | 0.427 | 0.439 | 0.032 (full T24) |
| 9 | gated delta rule | 1.097 | +1.097 | 0.973 | 0.967 | 0.961 | 0.026 | 0.020 | 0.030 (full T24) |
| 10 | linear attention | 0.958 | +0.958 | 0.814 | 0.787 | 0.778 | 0.378 | 0.407 | 0.037 (full T24) |
| 11 | linear attention | 0.958 | +0.958 | 0.814 | 0.787 | 0.778 | 0.378 | 0.406 | 0.037 (full T24) |
| 12 | gated delta rule | 1.100 | +1.100 | 0.975 | 0.967 | 0.961 | 0.021 | 0.018 | 0.025 (full T24) |
| 13 | linear attention | 0.951 | +0.949 | 0.817 | 0.789 | 0.775 | 0.431 | 0.440 | 0.031 (full T24) |
| 14 | linear attention | 0.951 | +0.949 | 0.817 | 0.789 | 0.775 | 0.431 | 0.440 | 0.031 (full T24) |
| 15 | linear attention | 0.958 | +0.958 | 0.814 | 0.787 | 0.778 | 0.378 | 0.407 | 0.037 (full T24) |
| 16 | linear attention | 0.951 | +0.950 | 0.829 | 0.789 | 0.772 | 0.436 | 0.444 | 0.032 (full T24) |

Rust rewrite8 0.000 with JAX near 0.02 is the Rust overflow guard (|S| > 1e4 scores the suite 0) acting on growth factors a > 1 over 96 steps.
v3 seed 4, clustered8 T48: Rust 0.034 ±0.004 vs JAX 0.091 ±0.012, beyond noise and not explained here (the rule uses the reciprocal op).
