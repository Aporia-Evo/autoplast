task regime longgap, tuned on 96 train episodes (task seed 1), commit 995b9f2

| family (tuned on train) | parameters | train | test regime longgap | test d16 T12 ow0.3 | test d16 T12 ow0.0 | test d16 T12 ow0.6 | test d32 T24 ow0.3 | test d8 T6 ow0.3 | test d16 T64 K8 ow0.3 | test d16 T128 K8 ow0.3 |
|---|---|---|---|---|---|---|---|---|---|---|
| linear attention | – | 0.065 | 0.049 | 0.750 | 0.917 | 0.549 | 0.828 | 0.615 | 0.104 | 0.062 |
| decayed linear attention | a=0.9 | 0.594 | 0.575 | 0.762 | 0.772 | 0.715 | 0.711 | 0.646 | 0.579 | 0.558 |
| DeltaNet | e=0.75 | 0.874 | 0.875 | 0.904 | 0.851 | 0.941 | 0.976 | 0.787 | 0.854 | 0.863 |
| Gated DeltaNet | a=1, e=0.75 | 0.874 | 0.875 | 0.904 | 0.851 | 0.941 | 0.976 | 0.787 | 0.854 | 0.863 |
| Kronecker delta rule | β=0.05 | 0.062 | 0.050 | 0.752 | 0.918 | 0.551 | 0.827 | 0.617 | 0.093 | 0.056 |
| gated Kronecker delta rule | a=0.9, β=0.75 | 0.621 | 0.605 | 0.772 | 0.770 | 0.737 | 0.708 | 0.644 | 0.604 | 0.581 |
| RLS (2 states) | λ=0.0001 | 0.065 | 0.071 | 0.841 | 1.000 | 0.635 | 0.844 | 0.807 | 0.138 | 0.070 |
| Kalman delta (2 states) | λ=0.0001, q=1 | 0.965 | 0.956 | 0.999 | 1.000 | 0.997 | 0.999 | 0.990 | 0.959 | 0.953 |
| ridge ceiling | λ=0.0001 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 |
