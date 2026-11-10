task regime clustered8, tuned on 192 train episodes (task seed 1), commit 995b9f2

| family (tuned on train) | parameters | train | test regime clustered8 | test d16 T12 ow0.3 | test d16 T12 ow0.0 | test d16 T12 ow0.6 | test d32 T24 ow0.3 | test d8 T6 ow0.3 | test d16 T64 K8 ow0.3 | test d16 T128 K8 ow0.3 |
|---|---|---|---|---|---|---|---|---|---|---|
| linear attention | – | 0.046 | 0.040 | 0.750 | 0.917 | 0.549 | 0.828 | 0.615 | 0.104 | 0.062 |
| decayed linear attention | a=0.7 | 0.174 | 0.165 | 0.503 | 0.420 | 0.651 | 0.353 | 0.593 | 0.479 | 0.473 |
| DeltaNet | e=0.35 | 0.201 | 0.205 | 0.919 | 0.923 | 0.898 | 0.982 | 0.768 | 0.715 | 0.682 |
| Gated DeltaNet | a=0.99, e=0.30 | 0.203 | 0.206 | 0.904 | 0.916 | 0.870 | 0.972 | 0.743 | 0.703 | 0.683 |
| Kronecker delta rule | β=0.05 | 0.042 | 0.039 | 0.752 | 0.918 | 0.551 | 0.827 | 0.617 | 0.093 | 0.056 |
| gated Kronecker delta rule | a=0.8, β=1.20 | 0.178 | 0.181 | 0.629 | 0.556 | 0.715 | 0.476 | 0.626 | 0.538 | 0.528 |
| RLS (2 states) | λ=0.001 | 0.199 | 0.195 | 0.836 | 1.000 | 0.624 | 0.843 | 0.813 | 0.137 | 0.069 |
| Kalman delta (2 states) | λ=0.0001, q=1 | 0.676 | 0.680 | 0.999 | 1.000 | 0.997 | 0.999 | 0.990 | 0.959 | 0.953 |
| ridge ceiling | λ=0.0001 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 |
