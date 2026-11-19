# grow arm A, task seed 4

| round | step | train fit | train acc | test acc | len | Rust evals | seconds |
|---|---|---|---|---|---|---|---|
| 1 | at 0: M0 += eps * Outer(V1,V0), eps +0.001 | 0.3661 | 0.373 | 0.385 | 4 | 51 | 6 |
| 2 | at 0: M0 += eps * Outer(MatVec(M0,V0),V0), eps -0.3; constants polished | 0.6361 | 0.635 | 0.635 | 9 | 549 | 19 |
| 3 | at 1: V2 += eps * VecScale(Dot(V1,V2),V1), eps +1 | 0.6472 | 0.646 | 0.642 | 14 | 1463 | 57 |
| 4 | at 12: M0 += eps * MatScale(S0,M0), eps +3 | 0.6477 | 0.647 | 0.642 | 18 | 2425 | 115 |
| 5 | stop: no candidate improves (best 0.6474 vs 0.6477) | | | | | 3241 | 186 |

```
S' = (((S + -0.353·((S·k + 1.000·<v, S·k>·v))⊗(k)) + 3.000·0.002·(S + -0.353·((S·k + 1.000·<v, S·k>·v))⊗(k))) + 0.002·(v)⊗(k))
P1' = 0.002·(v)⊗(k)
P2' = 3.000·0.002·(S + -0.353·((S·k + 1.000·<v, S·k>·v))⊗(k))

Effective program (18 instructions):
  V2 = MatVec(M0, V0)
  s0 = Dot(V1, V2)
  V3 = VecScale(s0, V1)
  s1 = 1.0000
  V3 = VecScale(s1, V3)
  V2 = VecAdd(V2, V3)
  M1 = Outer(V2, V0)
  s0 = -0.3526
  M1 = MatScale(s0, M1)
  M0 = MatAdd(M0, M1)
  M1 = Outer(V1, V0)
  s0 = 0.0021
  M2 = MatScale(s0, M0)
  s1 = 3.0000
  M2 = MatScale(s1, M2)
  M0 = MatAdd(M0, M2)
  M1 = MatScale(s0, M1)
  M0 = MatAdd(M0, M1)

structure: delta + Kronecker mix  [a=1.006 b=0.002 c=-0.355 g=-0.355, erase c/a=0.353, R²=1.0000, 1408 steps]

train acc 0.647 ±0.014
test regime collision3: acc 0.642  margin 0.044  ±0.006
test d16 T12 ow0.3: acc 0.926  margin 0.242  ±0.004
test d16 T12 ow0.0: acc 0.928  margin 0.239  ±0.003
test d16 T12 ow0.6: acc 0.919  margin 0.216  ±0.005
test d32 T24 ow0.3: acc 0.986  margin 0.325  ±0.002
test d8 T6 ow0.3: acc 0.773  margin 0.101  ±0.009
test d16 T64 K8 ow0.3: acc 0.741  margin 0.075  ±0.010
test d16 T128 K8 ow0.3: acc 0.687  margin 0.054  ±0.014


```
