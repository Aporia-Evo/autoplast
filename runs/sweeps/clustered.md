task regime clustered, tuned on 192 train episodes (task seed 1), commit 995b9f2

| family (tuned on train) | parameters | train | test regime clustered | test d16 T12 ow0.3 | test d16 T12 ow0.0 | test d16 T12 ow0.6 | test d32 T24 ow0.3 | test d8 T6 ow0.3 | test d16 T64 K8 ow0.3 | test d16 T128 K8 ow0.3 |
|---|---|---|---|---|---|---|---|---|---|---|
| linear attention | – | 0.115 | 0.120 | 0.750 | 0.917 | 0.549 | 0.828 | 0.615 | 0.104 | 0.062 |
| decayed linear attention | a=0.75 | 0.164 | 0.162 | 0.558 | 0.476 | 0.690 | 0.405 | 0.620 | 0.511 | 0.497 |
| DeltaNet | e=0.30 | 0.209 | 0.205 | 0.908 | 0.927 | 0.861 | 0.975 | 0.744 | 0.643 | 0.594 |
| Gated DeltaNet | a=1.25, e=0.55 | 0.404 | 0.410 | 0.786 | 0.809 | 0.717 | 0.436 | 0.803 | 0.000 | 0.000 |
| Kronecker delta rule | β=0.05 | 0.112 | 0.120 | 0.752 | 0.918 | 0.551 | 0.827 | 0.617 | 0.093 | 0.056 |
| gated Kronecker delta rule | a=0.8, β=1.20 | 0.178 | 0.177 | 0.629 | 0.556 | 0.715 | 0.476 | 0.626 | 0.538 | 0.528 |
| RLS (2 states) | λ=0.01 | 0.839 | 0.845 | 0.835 | 1.000 | 0.628 | 0.843 | 0.812 | 0.137 | 0.069 |
| Kalman delta (2 states) | λ=0.0001, q=0.1 | 0.956 | 0.958 | 0.976 | 1.000 | 0.925 | 0.995 | 0.902 | 0.892 | 0.881 |
| ridge ceiling | λ=0.0001 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 |
