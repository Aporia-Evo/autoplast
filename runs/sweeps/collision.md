task regime collision, tuned on 192 train episodes (task seed 1), commit 995b9f2

| family (tuned on train) | parameters | train | test regime collision | test d16 T12 ow0.3 | test d16 T12 ow0.0 | test d16 T12 ow0.6 | test d32 T24 ow0.3 | test d8 T6 ow0.3 | test d16 T64 K8 ow0.3 | test d16 T128 K8 ow0.3 |
|---|---|---|---|---|---|---|---|---|---|---|
| linear attention | – | 0.506 | 0.524 | 0.750 | 0.917 | 0.549 | 0.828 | 0.615 | 0.104 | 0.062 |
| decayed linear attention | a=0.95 | 0.544 | 0.553 | 0.790 | 0.872 | 0.648 | 0.860 | 0.637 | 0.446 | 0.429 |
| DeltaNet | e=0.30 | 0.646 | 0.658 | 0.908 | 0.927 | 0.861 | 0.975 | 0.744 | 0.643 | 0.594 |
| Gated DeltaNet | a=1.15, e=0.60 | 0.727 | 0.725 | 0.945 | 0.958 | 0.917 | 0.770 | 0.841 | 0.023 | 0.000 |
| Kronecker delta rule | β=0.95 | 0.521 | 0.530 | 0.771 | 0.928 | 0.538 | 0.839 | 0.600 | 0.022 | 0.006 |
| gated Kronecker delta rule | a=0.95, β=0.55 | 0.575 | 0.571 | 0.808 | 0.875 | 0.663 | 0.870 | 0.630 | 0.482 | 0.472 |
| RLS (2 states) | λ=0.001 | 0.837 | 0.839 | 0.836 | 1.000 | 0.624 | 0.843 | 0.813 | 0.137 | 0.069 |
| Kalman delta (2 states) | λ=0.0001, q=1 | 0.990 | 0.991 | 0.999 | 1.000 | 0.997 | 0.999 | 0.990 | 0.959 | 0.953 |
| ridge ceiling | λ=0.0001 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 |
