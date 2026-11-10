task regime collision3, tuned on 288 train episodes (task seed 1), commit 995b9f2

| family (tuned on train) | parameters | train | test regime collision3 | test d16 T12 ow0.3 | test d16 T12 ow0.0 | test d16 T12 ow0.6 | test d32 T24 ow0.3 | test d8 T6 ow0.3 | test d16 T64 K8 ow0.3 | test d16 T128 K8 ow0.3 |
|---|---|---|---|---|---|---|---|---|---|---|
| linear attention | – | 0.374 | 0.385 | 0.750 | 0.917 | 0.549 | 0.828 | 0.615 | 0.104 | 0.062 |
| decayed linear attention | a=0.9 | 0.510 | 0.519 | 0.762 | 0.772 | 0.715 | 0.711 | 0.646 | 0.579 | 0.558 |
| DeltaNet | e=0.50 | 0.621 | 0.640 | 0.924 | 0.900 | 0.941 | 0.987 | 0.793 | 0.840 | 0.828 |
| Gated DeltaNet | a=1.01, e=0.50 | 0.622 | 0.644 | 0.931 | 0.916 | 0.944 | 0.991 | 0.797 | 0.818 | 0.771 |
| Kronecker delta rule | β=0.15 | 0.377 | 0.384 | 0.752 | 0.921 | 0.549 | 0.826 | 0.618 | 0.085 | 0.054 |
| gated Kronecker delta rule | a=0.9, β=0.40 | 0.529 | 0.530 | 0.770 | 0.772 | 0.725 | 0.711 | 0.649 | 0.596 | 0.569 |
| RLS (2 states) | λ=0.001 | 0.621 | 0.620 | 0.836 | 1.000 | 0.624 | 0.843 | 0.813 | 0.137 | 0.069 |
| Kalman delta (2 states) | λ=0.0001, q=1 | 0.938 | 0.935 | 0.999 | 1.000 | 0.997 | 0.999 | 0.990 | 0.959 | 0.953 |
| ridge ceiling | λ=0.0001 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 |
