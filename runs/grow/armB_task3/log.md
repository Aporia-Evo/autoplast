# grow arm B, task seed 3

| round | step | train fit | train acc | test acc | len | Rust evals | seconds |
|---|---|---|---|---|---|---|---|
| 1 | at 0: M0 += eps * Outer(V1,Tanh(V0)), eps +0.001 | 0.4110 | 0.416 | 0.387 | 5 | 51 | 5 |
| 2 | at 0: M0 += eps * Outer(MatVec(M0,V0),V0), eps -1 | 0.6333 | 0.634 | 0.608 | 10 | 789 | 30 |
| 3 | tap V0 <- M2 V0 at 0; M2 += eps * Outer(V2,Normalize(V2)) at end, eps -0.03 | 0.6628 | 0.662 | 0.644 | 16 | 1703 | 91 |
| 4 | at 2: M0 += eps * MatScale(Dot(V0,V0),MatMul(M0,M2)), eps +0.003 | 0.6647 | 0.664 | 0.645 | 22 | 1945 | 178 |
| 5 | stop: no candidate fits | | | | | 1945 | 300 |

```
S' = (((S + 0.003·<P2·k, P2·k>·(S)(P2)) + -1.000·(S·P2·k)⊗(P2·k)) + 0.001·(v)⊗(tanh(P2·k)))
P1' = -0.030·(tanh(P2·k))⊗(norm(tanh(P2·k)))
P2' = (P2 + -0.030·(tanh(P2·k))⊗(norm(tanh(P2·k))))

Effective program (22 instructions):
  V0 = MatVec(M2, V0)
  V2 = MatVec(M0, V0)
  s0 = Dot(V0, V0)
  M1 = MatMul(M0, M2)
  M3 = MatScale(s0, M1)
  s1 = 0.0030
  M3 = MatScale(s1, M3)
  M0 = MatAdd(M0, M3)
  M1 = Outer(V2, V0)
  s0 = -1.0000
  M1 = MatScale(s0, M1)
  M0 = MatAdd(M0, M1)
  V2 = Tanh(V0)
  M1 = Outer(V1, V2)
  s0 = 0.0010
  M1 = MatScale(s0, M1)
  M0 = MatAdd(M0, M1)
  V0 = Normalize(V2)
  M1 = Outer(V2, V0)
  s0 = -0.0300
  M1 = MatScale(s0, M1)
  M2 = MatAdd(M2, M1)

structure: unclassified  [a=1.002 b=0.001 c=-0.728 g=-0.033, erase c/a=0.727, R²=0.9660, 1408 steps]

train acc 0.664 ±0.014
test regime collision3: acc 0.645  margin 0.036  ±0.006
test d16 T12 ow0.3: acc 0.893  margin 0.271  ±0.005
test d16 T12 ow0.0: acc 0.818  margin 0.203  ±0.005
test d16 T12 ow0.6: acc 0.945  margin 0.318  ±0.004
test d32 T24 ow0.3: acc 0.972  margin 0.369  ±0.003
test d8 T6 ow0.3: acc 0.770  margin 0.103  ±0.009
test d16 T64 K8 ow0.3: acc 0.921  margin 0.230  ±0.006
test d16 T128 K8 ow0.3: acc 0.708  margin 0.081  ±0.014


```
