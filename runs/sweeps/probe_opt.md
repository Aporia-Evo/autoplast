# Testbed 2 references, tuned on the train task of task seed 1

Objective: mean log10(f(w_T)/f(w_0)) over episodes, lower is better; div = fraction of diverged episodes.

| rule | parameters | train | train distribution | kappa 1000 | d 32 | d 8 | sigma 0.3 | T 200 | scale 10 / 0.1 |
|---|---|---|---|---|---|---|---|---|---|
| SGD | 1 | -2.013 | -2.072 | -1.437 | -1.018 (div 0.04) | -2.206 | -0.957 | -2.762 (div 0.00) | 0.927 (div 0.50) |
| momentum | 0.5, 0.6 | -2.614 | -2.638 | -1.485 | -2.012 | -2.694 | -1.009 | -2.910 | 0.869 (div 0.50) |
| RMSProp | 0.02, 0.99 | -2.717 | -2.679 | -1.588 | -2.376 | -2.726 | -1.279 | -2.634 | -2.512 |
| Adam | 0.03, 0.6, 0.99 | -3.130 | -3.073 | -1.621 | -2.980 | -3.129 | -1.208 | -3.406 | -2.814 |

Grid edges: a best value on the edge of its grid is marked in the table below if any.

Ceiling (not expressible in the space). `optimum`: w* on the quadratics, the least-squares
solution on regression. `newton`: Newton steps with the exact Hessian on the same stochastic
gradients; noise-limited, so not a ceiling, shown for reference.

```
train: newton -1.1305  optimum -5.7882
test opt train-distribution: newton -1.1274  optimum -5.8098
test opt kappa1000: newton -0.7613  optimum -5.6724
test opt d32: newton -1.1221  optimum -5.9019
test opt d8: newton -2.7590  optimum -5.7696
test opt sigma0.3: newton 1.7105  optimum -5.8058
test opt T200: newton -1.1259  optimum -5.8078
test opt scale10/0.1: newton -1.1274  optimum -5.8098
```
