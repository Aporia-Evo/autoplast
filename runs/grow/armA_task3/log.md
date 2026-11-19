# grow arm A, task seed 3

| round | step | train fit | train acc | test acc | len | Rust evals | seconds |
|---|---|---|---|---|---|---|---|
| 1 | at 0: M0 += eps * Outer(V1,Tanh(V0)), eps +0.001 | 0.4110 | 0.416 | 0.387 | 5 | 51 | 5 |
| 2 | at 0: M0 += eps * Outer(MatVec(M0,V0),V0), eps -1 | 0.6333 | 0.634 | 0.608 | 10 | 677 | 23 |
| 3 | at 0: V0 += eps * Tanh(V0), eps -0.3 | 0.6504 | 0.649 | 0.640 | 14 | 1591 | 58 |
| 4 | at 7: M0 += eps * M0, eps +0.01 | 0.6552 | 0.654 | 0.644 | 17 | 2553 | 106 |
| 5 | stop: no candidate improves (best 0.6549 vs 0.6552) | | | | | 3513 | 169 |

```
S' = (((S + 0.010·S) + -1.000·(S·(k + -0.300·tanh(k)))⊗((k + -0.300·tanh(k)))) + 0.001·(v)⊗(tanh((k + -0.300·tanh(k)))))
P1' = 0.001·(v)⊗(tanh((k + -0.300·tanh(k))))
P2' = 0.010·S

Effective program (17 instructions):
  V2 = Tanh(V0)
  s0 = -0.3000
  V2 = VecScale(s0, V2)
  V0 = VecAdd(V0, V2)
  V2 = MatVec(M0, V0)
  M1 = Outer(V2, V0)
  s0 = -1.0000
  s1 = 0.0100
  M2 = MatScale(s1, M0)
  M0 = MatAdd(M0, M2)
  M1 = MatScale(s0, M1)
  M0 = MatAdd(M0, M1)
  V2 = Tanh(V0)
  M1 = Outer(V1, V2)
  s0 = 0.0010
  M1 = MatScale(s0, M1)
  M0 = MatAdd(M0, M1)

structure: delta rule  [a=1.010 b=0.001 c=-0.514 g=-0.000, erase c/a=0.509, R²=0.9998, 1408 steps]

train acc 0.654 ±0.014
test regime collision3: acc 0.644  margin 0.052  ±0.006
test d16 T12 ow0.3: acc 0.930  margin 0.267  ±0.004
test d16 T12 ow0.0: acc 0.915  margin 0.244  ±0.004
test d16 T12 ow0.6: acc 0.945  margin 0.265  ±0.004
test d32 T24 ow0.3: acc 0.991  margin 0.356  ±0.001
test d8 T6 ow0.3: acc 0.797  margin 0.116  ±0.008
test d16 T64 K8 ow0.3: acc 0.819  margin 0.141  ±0.009
test d16 T128 K8 ow0.3: acc 0.778  margin 0.122  ±0.013


```
