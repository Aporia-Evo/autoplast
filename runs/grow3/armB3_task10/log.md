# grow v3, arm B, task seed 10, beam 4, compaction, stability gate 100

| round | best train fit | best train acc | best test acc | len | beam (train acc, len, last step) | Rust evals | grad passes | gate evals | refused by gate | seconds |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | 0.4114 | 0.416 | 0.385 | 2 | 0.416, 2, at 0: M0 += eps * Outer(V1,V0), eps +0.001; compacted 4->2; 0.000, 0, start | 62 | 61 | 4 | 0 | 7 |
| 2 | 0.6754 | 0.673 | 0.635 | 6 | 0.673, 6, at 0: V1 += eps * MatVec(M0,V0), eps -0.3; polished; 0.673, 7, at 0: M0 += eps * Outer(MatVec(M0,V0),V0), eps -0.3; polished; 0.565, 4, at 2: M0 += eps * M0, eps -0.1; compacted 5->4; 0.565, 7, at 0: M0 += eps * MatScale(Dot(V1,V1),M0), eps -0.1 | 457 | 303 | 11 | 0 | 26 |
| 3 | 0.7676 | 0.763 | 0.722 | 12 | 0.763, 12, tap V0 <- M1 V0 at 2; M1 += eps * Outer(V0,Tanh(V0)) at end, eps -0.1; polished; compacted 13->12; 0.763, 12, tap V0 <- M2 V0 at 2; M2 += eps * Outer(V0,Tanh(V0)) at end, eps -0.1; polished; compacted 13->12; 0.688, 12, tap V2 <- M2 V2 at 1; M2 += eps * MatScale(Norm(V2),M1) at end, eps +0.01; 0.685, 13, tap V2 <- M1 V2 at 1; M1 += eps * MatScale(Norm(V2),M1) at end, eps +0.003 | 3503 | 547 | 29 | 9 | 192 |
| 4 | 0.7976 | 0.791 | 0.768 | 14 | 0.791, 14, at 6: M0 += eps * M0, eps -0.03; polished; compacted 15->14; 0.791, 17, at 6: M0 += eps * MatScale(Sigmoid(S0),M0), eps -0.1; polished; 0.787, 17, at 6: M1 += eps * MatScale(S0,MatSub(M1,M2)), eps +0.01; 0.787, 17, at 6: M2 += eps * MatScale(S0,MatSub(M1,M2)), eps -0.01 | 6099 | 791 | 36 | 9 | 508 |
| 5 | 0.8320 | 0.825 | 0.804 | 24 | 0.825, 24, tap V0 <- M2 V0 at 1; M2 += eps * MatScale(Norm(V2),MatSub(M1,M2)) at end, eps +0.03; polished; 0.817, 20, at 7: S1 += eps * SMul(Norm(V0),Norm(V2)), eps +0.1; polished; 0.809, 19, at 3: V0 += eps * VecScale(Dot(V2,V2),V0), eps +0.3; 0.798, 20, at 1: M1 += eps * MatScale(Dot(V2,V2),MatSub(M1,M2)), eps +0.03 | 7706 | 1035 | 42 | 9 | 925 |
| 6 | 0.8320 | 0.825 | 0.804 | 24 | 0.825, 24, tap V0 <- M2 V0 at 1; M2 += eps * MatScale(Norm(V2),MatSub(M1,M2)) at end, eps +0.03; polished; 0.824, 22, at 1: V2 += eps * V2, eps +0.1; compacted 23->22; 0.819, 22, at 0: V0 += eps * V0, eps +0.01; compacted 23->22; 0.819, 24, at 0: M0 += eps * Outer(V1,V0), eps -0.01 | 8331 | 1219 | 49 | 11 | 1498 |
| 7 | stop: beam unchanged | | | | | 8331 | 1223 | 49 | 11 | 2110 |

```
S' = (((S + -0.653·(S·k)⊗(P2·k)) + -0.137·σ(-0.653)·(S + -0.653·(S·k)⊗(P2·k))) + (v)⊗(P1·P2·k))
P1' = (P1 + -0.653·(P1·P2·k)⊗(tanh(P1·P2·k)))
P2' = (P2 + 0.104·|S·k|·((P1 + -0.653·(P1·P2·k)⊗(tanh(P1·P2·k))) - P2))

Effective program (24 instructions):
  V2 = MatVec(M0, V0)
  V0 = MatVec(M2, V0)
  M3 = Outer(V2, V0)
  V0 = MatVec(M1, V0)
  s0 = -0.6527
  M3 = MatScale(s0, M3)
  M0 = MatAdd(M0, M3)
  s1 = Sigmoid(s0)
  M3 = MatScale(s1, M0)
  s1 = -0.1374
  M3 = MatScale(s1, M3)
  M0 = MatAdd(M0, M3)
  M3 = Outer(V1, V0)
  M0 = MatAdd(M0, M3)
  V1 = Tanh(V0)
  M3 = Outer(V0, V1)
  M3 = MatScale(s0, M3)
  M1 = MatAdd(M1, M3)
  s0 = Norm(V2)
  M3 = MatSub(M1, M2)
  M3 = MatScale(s0, M3)
  s0 = 0.1042
  M3 = MatScale(s0, M3)
  M2 = MatAdd(M2, M3)

structure: unclassified  [a=0.953 b=0.338 c=-0.554 g=-0.062, erase c/a=0.581, R²=0.5701, 1408 steps]

train acc 0.825 ±0.011
test regime collision3: acc 0.804  margin 0.170  ±0.005
test d16 T12 ow0.3: acc 0.927  margin 0.306  ±0.004
test d16 T12 ow0.0: acc 0.984  margin 0.336  ±0.002
test d16 T12 ow0.6: acc 0.892  margin 0.240  ±0.006
test d32 T24 ow0.3: acc 0.950  margin 0.374  ±0.003
test d8 T6 ow0.3: acc 0.853  margin 0.156  ±0.007
test d16 T64 K8 ow0.3: acc 0.924  margin 0.201  ±0.006
test d16 T128 K8 ow0.3: acc 0.897  margin 0.183  ±0.009


```
