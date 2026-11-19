# grow arm B, task seed 4

| round | step | train fit | train acc | test acc | len | Rust evals | seconds |
|---|---|---|---|---|---|---|---|
| 1 | at 0: M0 += eps * Outer(V1,V0), eps +0.001 | 0.3661 | 0.373 | 0.385 | 4 | 51 | 6 |
| 2 | at 0: M0 += eps * Outer(MatVec(M0,V0),V0), eps -0.3; constants polished | 0.6361 | 0.635 | 0.635 | 9 | 677 | 24 |
| 3 | tap V0 <- M2 V0 at 2; M2 += eps * Outer(V0,VecSub(V0,V2)) at end, eps -0.3; constants polished | 0.7643 | 0.759 | 0.735 | 15 | 1607 | 87 |
| 4 | at 6: M0 += eps * MatScale(Sigmoid(S0),MatMul(M0,M2)), eps -0.1; constants polished | 0.8052 | 0.799 | 0.771 | 21 | 2137 | 212 |
| 5 | stop: no candidate fits | | | | | 2137 | 356 |

```
S' = (((S + -0.534·(S·k)⊗(k)) + -0.176·σ(-0.534)·((S + -0.534·(S·k)⊗(k)))(P2)) + 0.002·(v)⊗(P2·k))
P1' = -0.601·(P2·k)⊗((P2·k - S·k))
P2' = (P2 + -0.601·(P2·k)⊗((P2·k - S·k)))

Effective program (21 instructions):
  V2 = MatVec(M0, V0)
  M1 = Outer(V2, V0)
  V0 = MatVec(M2, V0)
  s0 = -0.5336
  M1 = MatScale(s0, M1)
  M0 = MatAdd(M0, M1)
  s1 = Sigmoid(s0)
  M1 = MatMul(M0, M2)
  M3 = MatScale(s1, M1)
  s2 = -0.1765
  M3 = MatScale(s2, M3)
  M0 = MatAdd(M0, M3)
  M1 = Outer(V1, V0)
  s0 = 0.0019
  M1 = MatScale(s0, M1)
  M0 = MatAdd(M0, M1)
  V1 = VecSub(V0, V2)
  M1 = Outer(V0, V1)
  s0 = -0.6013
  M1 = MatScale(s0, M1)
  M2 = MatAdd(M2, M1)

structure: unclassified  [a=0.967 b=0.001 c=-0.510 g=-0.024, erase c/a=0.528, R²=0.6040, 1408 steps]

train acc 0.799 ±0.011
test regime collision3: acc 0.771  margin 0.149  ±0.005
test d16 T12 ow0.3: acc 0.900  margin 0.284  ±0.004
test d16 T12 ow0.0: acc 0.981  margin 0.318  ±0.002
test d16 T12 ow0.6: acc 0.838  margin 0.220  ±0.007
test d32 T24 ow0.3: acc 0.939  margin 0.356  ±0.004
test d8 T6 ow0.3: acc 0.804  margin 0.133  ±0.008
test d16 T64 K8 ow0.3: acc 0.904  margin 0.205  ±0.007
test d16 T128 K8 ow0.3: acc 0.895  margin 0.191  ±0.010


```
