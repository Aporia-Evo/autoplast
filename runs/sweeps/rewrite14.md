task regime rewrite14, tuned on 192 train episodes (task seed 1), commit 995b9f2

| family (tuned on train) | parameters | train | test regime rewrite14 | test d16 T12 ow0.3 | test d16 T12 ow0.0 | test d16 T12 ow0.6 | test d32 T24 ow0.3 | test d8 T6 ow0.3 | test d16 T64 K8 ow0.3 | test d16 T128 K8 ow0.3 |
|---|---|---|---|---|---|---|---|---|---|---|
| linear attention | – | 0.107 | 0.106 | 0.750 | 0.917 | 0.549 | 0.828 | 0.615 | 0.104 | 0.062 |
| decayed linear attention | a=0.9 | 0.468 | 0.460 | 0.762 | 0.772 | 0.715 | 0.711 | 0.646 | 0.579 | 0.558 |
| DeltaNet | e=0.60 | 0.719 | 0.718 | 0.919 | 0.883 | 0.946 | 0.984 | 0.793 | 0.855 | 0.858 |
| Gated DeltaNet | a=1, e=0.60 | 0.719 | 0.718 | 0.919 | 0.883 | 0.946 | 0.984 | 0.793 | 0.855 | 0.858 |
| Kronecker delta rule | β=0.05 | 0.104 | 0.103 | 0.752 | 0.918 | 0.551 | 0.827 | 0.617 | 0.093 | 0.056 |
| gated Kronecker delta rule | a=0.9, β=0.85 | 0.483 | 0.470 | 0.773 | 0.769 | 0.733 | 0.707 | 0.643 | 0.604 | 0.577 |
| RLS (2 states) | λ=0.3 | 0.165 | 0.156 | 0.835 | 1.000 | 0.626 | 0.845 | 0.811 | 0.140 | 0.069 |
| Kalman delta (2 states) | λ=0.0001, q=1 | 0.844 | 0.854 | 0.999 | 1.000 | 0.997 | 0.999 | 0.990 | 0.959 | 0.953 |
| ridge ceiling | λ=0.0001 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 |
