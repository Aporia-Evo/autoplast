# grow v2, arm B, task seed 1, beam 4, compaction True

| round | best train fit | best train acc | best test acc | len | beam (train acc, len, last step) | Rust evals | grad passes | seconds |
|---|---|---|---|---|---|---|---|---|
| 1 | 0.3556 | 0.362 | 0.385 | 2 | 0.362, 2, at 0: M0 += eps * Outer(V1,V0), eps +0.001; compacted 4->2; 0.000, 0, start | 62 | 61 | 5 |
| 2 | 0.6061 | 0.605 | 0.625 | 6 | 0.605, 6, at 0: V1 += eps * MatVec(M0,V0), eps -0.3; polished; 0.605, 7, at 0: M0 += eps * Outer(MatVec(M0,V0),V0), eps -0.3; polished; 0.605, 7, at 1: M1 += eps * Outer(MatVec(M0,V0),V0), eps -0.3; polished; 0.505, 7, tap V1 <- M2 V1 at 0; M2 += eps * MatSub(M1,M2) at end, eps -0.1 | 582 | 303 | 21 |
| 3 | 0.7156 | 0.712 | 0.727 | 12 | 0.712, 12, tap V0 <- M2 V0 at 2; M2 += eps * Outer(V0,Tanh(V0)) at end, eps -0.3; polished; compacted 13->12; 0.624, 12, tap V2 <- M2 V2 at 1; M2 += eps * MatScale(Norm(V2),M2) at end, eps +0.03; 0.620, 12, tap V1 <- M2 V1 at 4; M2 += eps * MatScale(Dot(V2,V2),M2) at end, eps +0.03; 0.606, 11, tap V1 <- M2 V1 at 0; M2 += eps * Outer(Normalize(V1),V1) at end, eps -0.01; compacted 12->11 | 4215 | 547 | 192 |
| 4 | 0.7631 | 0.758 | 0.770 | 14 | 0.758, 14, at 8: M0 += eps * M0, eps -0.03; compacted 15->14; 0.758, 16, at 11: M0 += eps * MatSub(M0,M1), eps -0.03; 0.758, 17, at 0: M0 += eps * MatScale(Norm(V0),M0), eps -0.03; 0.754, 17, at 7: M1 += eps * MatScale(Sigmoid(S0),M0), eps -0.1 | 7446 | 791 | 473 |
| 5 | 0.7959 | 0.790 | 0.802 | 20 | 0.790, 20, at 14: M0 += eps * MatScale(Dot(V0,V1),MatMul(M0,M2)), eps +0.1; polished; 0.776, 21, at 5: M1 += eps * MatScale(Dot(V0,V0),M0), eps +0.1; polished; 0.758, 22, at 3: M2 += eps * Outer(VecScale(S1,V0),V0), eps -0.001; 0.758, 14, at 8: M0 += eps * M0, eps -0.03; compacted 15->14 | 8973 | 975 | 834 |
| 6 | 0.8169 | 0.811 | 0.814 | 24 | 0.811, 24, at 3: M2 += eps * MatMul(M2,M2), eps +0.01; polished; 0.791, 24, at 0: M2 += eps * Outer(V0,V0), eps -0.001; polished; 0.790, 20, at 14: M0 += eps * MatScale(Dot(V0,V1),MatMul(M0,M2)), eps +0.1; polished; 0.776, 21, at 5: M1 += eps * MatScale(Dot(V0,V0),M0), eps +0.1; polished | 9536 | 1099 | 1309 |
| 7 | 0.8169 | 0.811 | 0.814 | 24 | 0.811, 24, at 3: M2 += eps * MatMul(M2,M2), eps +0.01; polished; 0.791, 24, at 0: M2 += eps * Outer(V0,V0), eps -0.001; polished; 0.791, 24, at 1: M2 += eps * Outer(V0,V0), eps -0.001; polished; 0.790, 20, at 14: M0 += eps * MatScale(Dot(V0,V1),MatMul(M0,M2)), eps +0.1; polished | 9634 | 1163 | 1795 |
| 8 | stop: beam unchanged | | | | | 9698 | 1167 | 2270 |

```
S' = (0.897·((S + -0.462·(S·k)⊗(k)) + (v)⊗(P2·k)) + 0.315·<P2·k, tanh(P2·k)>·(0.897·((S + -0.462·(S·k)⊗(k)) + (v)⊗(P2·k)))(((P2 + 0.013·(P2)(P2)) + -0.462·(P2·k)⊗(tanh(P2·k)))))
P1' = (0.897·((S + -0.462·(S·k)⊗(k)) + (v)⊗(P2·k)))(((P2 + 0.013·(P2)(P2)) + -0.462·(P2·k)⊗(tanh(P2·k))))
P2' = ((P2 + 0.013·(P2)(P2)) + -0.462·(P2·k)⊗(tanh(P2·k)))

Effective program (24 instructions):
  V2 = MatVec(M0, V0)
  M1 = Outer(V2, V0)
  V0 = MatVec(M2, V0)
  M3 = MatMul(M2, M2)
  s0 = 0.0125
  M3 = MatScale(s0, M3)
  M2 = MatAdd(M2, M3)
  s0 = -0.4619
  M1 = MatScale(s0, M1)
  M0 = MatAdd(M0, M1)
  M1 = Outer(V1, V0)
  M0 = MatAdd(M0, M1)
  s1 = 0.8967
  M0 = MatScale(s1, M0)
  V1 = Tanh(V0)
  M1 = Outer(V0, V1)
  M1 = MatScale(s0, M1)
  M2 = MatAdd(M2, M1)
  s0 = Dot(V0, V1)
  M1 = MatMul(M0, M2)
  M3 = MatScale(s0, M1)
  s1 = 0.3148
  M3 = MatScale(s1, M3)
  M0 = MatAdd(M0, M3)

structure: unclassified  [a=0.979 b=0.470 c=-0.474 g=-0.005, erase c/a=0.485, R²=0.6415, 1408 steps]

train acc 0.811 ±0.011
test regime collision3: acc 0.814  margin 0.184  ±0.005
test d16 T12 ow0.3: acc 0.872  margin 0.291  ±0.005
test d16 T12 ow0.0: acc 0.995  margin 0.354  ±0.001
test d16 T12 ow0.6: acc 0.814  margin 0.218  ±0.007
test d32 T24 ow0.3: acc 0.773  margin 0.288  ±0.006
test d8 T6 ow0.3: acc 0.818  margin 0.140  ±0.008
test d16 T64 K8 ow0.3: acc 0.902  margin 0.255  ±0.007
test d16 T128 K8 ow0.3: acc 0.000  margin 0.000  ±0.000


```
