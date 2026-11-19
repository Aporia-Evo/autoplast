# grow arm B, task seed 2

| round | step | train fit | train acc | test acc | len | Rust evals | seconds |
|---|---|---|---|---|---|---|---|
| 1 | at 0: M0 += eps * Outer(V1,V0), eps +0.001 | 0.3562 | 0.363 | 0.385 | 4 | 51 | 7 |
| 2 | tap V1 <- M2 V1 at 0; M2 += eps * MatScale(Sigmoid(S0),MatSub(M0,M2)) at end, eps -0.3 | 0.5134 | 0.517 | 0.515 | 11 | 661 | 25 |
| 3 | at 0: M0 += eps * Outer(V1,Normalize(V0)), eps +0.003 | 0.5245 | 0.527 | 0.527 | 16 | 1383 | 75 |
| 4 | stop: no candidate improves (best 0.5207 vs 0.5245) | | | | | 2295 | 158 |

```
S' = ((S + 0.003·(v)⊗(norm(k))) + 0.001·(P2·v)⊗(k))
P1' = (((S + 0.003·(v)⊗(norm(k))) + 0.001·(P2·v)⊗(k)) - P2)
P2' = (P2 + -0.300·σ(0.001)·(((S + 0.003·(v)⊗(norm(k))) + 0.001·(P2·v)⊗(k)) - P2))

Effective program (16 instructions):
  V2 = Normalize(V0)
  M1 = Outer(V1, V2)
  s0 = 0.0030
  M1 = MatScale(s0, M1)
  M0 = MatAdd(M0, M1)
  V1 = MatVec(M2, V1)
  M1 = Outer(V1, V0)
  s0 = 0.0010
  M1 = MatScale(s0, M1)
  M0 = MatAdd(M0, M1)
  s1 = Sigmoid(s0)
  M1 = MatSub(M0, M2)
  M3 = MatScale(s1, M1)
  s2 = -0.3000
  M3 = MatScale(s2, M3)
  M2 = MatAdd(M2, M3)

structure: unclassified  [a=1.000 b=0.581 c=-0.000 g=0.334, erase c/a=0.000, R²=0.1719, 1408 steps]

train acc 0.527 ±0.014
test regime collision3: acc 0.527  margin -0.025  ±0.006
test d16 T12 ow0.3: acc 0.787  margin 0.149  ±0.006
test d16 T12 ow0.0: acc 0.860  margin 0.183  ±0.004
test d16 T12 ow0.6: acc 0.663  margin 0.079  ±0.009
test d32 T24 ow0.3: acc 0.726  margin 0.159  ±0.007
test d8 T6 ow0.3: acc 0.633  margin 0.029  ±0.010
test d16 T64 K8 ow0.3: acc 0.583  margin -0.011  ±0.011
test d16 T128 K8 ow0.3: acc 0.000  margin 0.000  ±0.000


```
