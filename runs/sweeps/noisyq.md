task regime noisyq, tuned on 192 train episodes (task seed 1), commit 995b9f2

| family (tuned on train) | parameters | train | test regime noisyq | test d16 T12 ow0.3 | test d16 T12 ow0.0 | test d16 T12 ow0.6 | test d32 T24 ow0.3 | test d8 T6 ow0.3 | test d16 T64 K8 ow0.3 | test d16 T128 K8 ow0.3 |
|---|---|---|---|---|---|---|---|---|---|---|
| linear attention | – | 0.720 | 0.724 | 0.750 | 0.917 | 0.549 | 0.828 | 0.615 | 0.104 | 0.062 |
| decayed linear attention | a=0.97 | 0.750 | 0.750 | 0.780 | 0.902 | 0.612 | 0.880 | 0.631 | 0.310 | 0.287 |
| DeltaNet | e=0.50 | 0.896 | 0.899 | 0.924 | 0.900 | 0.941 | 0.987 | 0.793 | 0.840 | 0.828 |
| Gated DeltaNet | a=1.1, e=0.70 | 0.930 | 0.934 | 0.969 | 0.951 | 0.965 | 0.971 | 0.838 | 0.076 | 0.021 |
| Kronecker delta rule | β=1.30 | 0.734 | 0.738 | 0.767 | 0.915 | 0.548 | 0.836 | 0.591 | 0.041 | 0.020 |
| gated Kronecker delta rule | a=0.95, β=0.90 | 0.769 | 0.773 | 0.804 | 0.870 | 0.662 | 0.869 | 0.624 | 0.507 | 0.489 |
| RLS (2 states) | λ=0.3 | 0.823 | 0.812 | 0.835 | 1.000 | 0.626 | 0.845 | 0.811 | 0.140 | 0.069 |
| Kalman delta (2 states) | λ=0.001, q=10 | 0.967 | 0.967 | 0.998 | 0.998 | 0.996 | 1.000 | 0.980 | 0.955 | 0.960 |
| ridge ceiling | λ=0.3 | 0.993 | 0.990 | 1.000 | 1.000 | 1.000 | 1.000 | 0.987 | 1.000 | 1.000 |
