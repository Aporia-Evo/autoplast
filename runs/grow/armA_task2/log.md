# grow arm A, task seed 2

| round | step | train fit | train acc | test acc | len | Rust evals | seconds |
|---|---|---|---|---|---|---|---|
| 1 | at 0: M0 += eps * Outer(V1,V0), eps +0.001 | 0.3562 | 0.363 | 0.385 | 4 | 51 | 7 |
| 2 | at 0: M0 += eps * M0, eps -0.1 | 0.5087 | 0.511 | 0.519 | 7 | 549 | 20 |
| 3 | at 0: M0 += eps * Outer(MatVec(M0,V0),V0), eps -0.3; constants polished | 0.6308 | 0.630 | 0.638 | 12 | 1463 | 46 |
| 4 | at 10: S0 += eps * Dot(V1,V2), eps -0.3; constants polished | 0.6469 | 0.646 | 0.637 | 16 | 2377 | 89 |
| 5 | at 16: M0 += eps * MatScale(Norm(V2),M0), eps -1; constants polished | 0.6499 | 0.650 | 0.644 | 21 | 3259 | 149 |
| 6 | at 1: V2 += eps * V2, eps +0.1; constants polished | 0.6648 | 0.665 | 0.654 | 24 | 3389 | 226 |
| 7 | stop: no candidate fits | | | | | 3389 | 309 |

```
S' = ((((S + -0.313·((S·k + 0.100·S·k))⊗(k)) + 0.093·(S + -0.313·((S·k + 0.100·S·k))⊗(k))) + (0.021 + -0.377·<v, (S·k + 0.100·S·k)>)·(v)⊗(k)) + -2.990·|(S·k + 0.100·S·k)|·(((S + -0.313·((S·k + 0.100·S·k))⊗(k)) + 0.093·(S + -0.313·((S·k + 0.100·S·k))⊗(k))) + (0.021 + -0.377·<v, (S·k + 0.100·S·k)>)·(v)⊗(k)))
P1' = -2.990·|(S·k + 0.100·S·k)|·(((S + -0.313·((S·k + 0.100·S·k))⊗(k)) + 0.093·(S + -0.313·((S·k + 0.100·S·k))⊗(k))) + (0.021 + -0.377·<v, (S·k + 0.100·S·k)>)·(v)⊗(k))

Effective program (24 instructions):
  V2 = MatVec(M0, V0)
  s0 = 0.1000
  V3 = VecScale(s0, V2)
  V2 = VecAdd(V2, V3)
  M1 = Outer(V2, V0)
  s0 = -0.3129
  M1 = MatScale(s0, M1)
  M0 = MatAdd(M0, M1)
  s0 = 0.0930
  M1 = MatScale(s0, M0)
  M0 = MatAdd(M0, M1)
  M1 = Outer(V1, V0)
  s0 = 0.0206
  s1 = Dot(V1, V2)
  s2 = -0.3771
  s1 = SMul(s2, s1)
  s0 = SAdd(s0, s1)
  M1 = MatScale(s0, M1)
  M0 = MatAdd(M0, M1)
  s0 = Norm(V2)
  M1 = MatScale(s0, M0)
  s1 = -2.9900
  M1 = MatScale(s1, M1)
  M0 = MatAdd(M0, M1)

structure: delta + Kronecker mix  [a=1.009 b=0.019 c=-0.351 g=-0.390, erase c/a=0.347, R²=0.9975, 1408 steps]

train acc 0.665 ±0.014
test regime collision3: acc 0.654  margin 0.051  ±0.006
test d16 T12 ow0.3: acc 0.923  margin 0.237  ±0.004
test d16 T12 ow0.0: acc 0.962  margin 0.252  ±0.002
test d16 T12 ow0.6: acc 0.895  margin 0.199  ±0.006
test d32 T24 ow0.3: acc 0.953  margin 0.302  ±0.003
test d8 T6 ow0.3: acc 0.771  margin 0.102  ±0.009
test d16 T64 K8 ow0.3: acc 0.745  margin 0.077  ±0.010
test d16 T128 K8 ow0.3: acc 0.714  margin 0.067  ±0.014


```
