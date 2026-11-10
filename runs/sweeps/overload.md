task regime overload, tuned on 192 train episodes (task seed 1), commit 995b9f2

| family (tuned on train) | parameters | train | test regime overload | test d16 T12 ow0.3 | test d16 T12 ow0.0 | test d16 T12 ow0.6 | test d32 T24 ow0.3 | test d8 T6 ow0.3 | test d16 T64 K8 ow0.3 | test d16 T128 K8 ow0.3 |
|---|---|---|---|---|---|---|---|---|---|---|
| linear attention | – | 0.481 | 0.477 | 0.750 | 0.917 | 0.549 | 0.828 | 0.615 | 0.104 | 0.062 |
| decayed linear attention | a=0.97 | 0.528 | 0.520 | 0.780 | 0.902 | 0.612 | 0.880 | 0.631 | 0.310 | 0.287 |
| DeltaNet | e=0.40 | 0.666 | 0.663 | 0.922 | 0.915 | 0.923 | 0.987 | 0.780 | 0.781 | 0.751 |
| Gated DeltaNet | a=1.03, e=0.50 | 0.720 | 0.723 | 0.944 | 0.938 | 0.950 | 0.995 | 0.805 | 0.633 | 0.400 |
| Kronecker delta rule | β=0.70 | 0.487 | 0.493 | 0.765 | 0.930 | 0.540 | 0.837 | 0.600 | 0.027 | 0.010 |
| gated Kronecker delta rule | a=0.97, β=0.45 | 0.542 | 0.538 | 0.797 | 0.904 | 0.620 | 0.887 | 0.623 | 0.322 | 0.302 |
| RLS (2 states) | λ=0.0001 | 0.769 | 0.766 | 0.841 | 1.000 | 0.635 | 0.844 | 0.807 | 0.138 | 0.070 |
| Kalman delta (2 states) | λ=0.0001, q=0.1 | 0.818 | 0.805 | 0.976 | 1.000 | 0.925 | 0.995 | 0.902 | 0.892 | 0.881 |
| ridge ceiling | λ=0.01 | 0.961 | 0.955 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 |
