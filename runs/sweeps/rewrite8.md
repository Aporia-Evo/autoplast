task regime rewrite8, tuned on 192 train episodes (task seed 1), commit 995b9f2

| family (tuned on train) | parameters | train | test regime rewrite8 | test d16 T12 ow0.3 | test d16 T12 ow0.0 | test d16 T12 ow0.6 | test d32 T24 ow0.3 | test d8 T6 ow0.3 | test d16 T64 K8 ow0.3 | test d16 T128 K8 ow0.3 |
|---|---|---|---|---|---|---|---|---|---|---|
| linear attention | – | 0.079 | 0.068 | 0.750 | 0.917 | 0.549 | 0.828 | 0.615 | 0.104 | 0.062 |
| decayed linear attention | a=0.85 | 0.600 | 0.584 | 0.700 | 0.663 | 0.730 | 0.572 | 0.640 | 0.578 | 0.546 |
| DeltaNet | e=0.65 | 0.890 | 0.874 | 0.914 | 0.873 | 0.944 | 0.982 | 0.788 | 0.853 | 0.861 |
| Gated DeltaNet | a=1, e=0.65 | 0.890 | 0.874 | 0.914 | 0.873 | 0.944 | 0.982 | 0.788 | 0.853 | 0.861 |
| Kronecker delta rule | β=0.05 | 0.075 | 0.068 | 0.752 | 0.918 | 0.551 | 0.827 | 0.617 | 0.093 | 0.056 |
| gated Kronecker delta rule | a=0.9, β=0.75 | 0.624 | 0.607 | 0.772 | 0.770 | 0.737 | 0.708 | 0.644 | 0.604 | 0.581 |
| RLS (2 states) | λ=0.3 | 0.096 | 0.089 | 0.835 | 1.000 | 0.626 | 0.845 | 0.811 | 0.140 | 0.069 |
| Kalman delta (2 states) | λ=0.0001, q=1 | 0.961 | 0.951 | 0.999 | 1.000 | 0.997 | 0.999 | 0.990 | 0.959 | 0.953 |
| ridge ceiling | λ=0.0001 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 |
