# grow v3, arm B, task seed 17, beam 4, compaction, stability gate 100

| round | best train fit | best train acc | best test acc | len | beam (train acc, len, last step) | Rust evals | grad passes | gate evals | refused by gate | seconds |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | 0.4049 | 0.410 | 0.385 | 2 | 0.410, 2, at 0: M0 += eps * Outer(V1,V0), eps +0.001; compacted 4->2; 0.000, 0, start | 62 | 61 | 4 | 0 | 7 |
| 2 | 0.6609 | 0.658 | 0.633 | 6 | 0.658, 6, at 0: V1 += eps * MatVec(M0,V0), eps -0.3; polished; 0.658, 7, at 0: M0 += eps * Outer(MatVec(M0,V0),V0), eps -0.3; polished; 0.568, 7, at 0: M0 += eps * MatScale(Norm(V0),M0), eps -0.1; 0.439, 6, at 2: M0 += eps * MatSub(M0,M1), eps -0.03; polished | 453 | 303 | 15 | 4 | 26 |
| 3 | 0.7453 | 0.740 | 0.726 | 12 | 0.740, 12, tap V0 <- M1 V0 at 2; M1 += eps * Outer(MatVec(M1,V0),V0) at end, eps -0.1; polished; compacted 13->12; 0.677, 12, tap V0 <- M1 V0 at 0; M1 += eps * MatScale(Norm(V2),M1) at end, eps +0.003; 0.677, 12, tap V0 <- M2 V0 at 0; M2 += eps * MatScale(Norm(V2),M1) at end, eps +0.003; 0.677, 13, tap V2 <- M1 V2 at 1; M1 += eps * MatScale(Norm(V2),M1) at end, eps +0.003 | 3320 | 547 | 23 | 5 | 206 |
| 4 | 0.7751 | 0.769 | 0.746 | 18 | 0.769, 18, tap V0 <- M2 V0 at 1; M2 += eps * MatScale(S0,Transpose(M1)) at end, eps -0.03; 0.766, 17, tap V0 <- M2 V0 at 0; M2 += eps * Transpose(M1) at end, eps +0.01; polished; 0.757, 17, at 1: M0 += eps * MatScale(Dot(V0,V0),M0), eps -0.01; polished; 0.755, 14, at 6: M0 += eps * M0, eps -0.01; polished; compacted 15->14 | 6477 | 791 | 31 | 5 | 518 |
| 5 | 0.8122 | 0.805 | 0.790 | 21 | 0.805, 21, at 1: M2 += eps * Outer(V0,V0), eps -0.01; polished; 0.782, 24, at 10: M2 += eps * MatScale(Dot(V0,V1),MatSub(M1,M2)), eps +0.03; polished; 0.779, 21, tap V0 <- M2 V0 at 1; M2 += eps * MatScale(Norm(V1),MatSub(M1,M2)) at end, eps +0.03; polished; 0.773, 23, at 0: M1 += eps * Outer(V0,MatVec(M2,V0)), eps -0.003 | 8443 | 1035 | 38 | 5 | 953 |
| 6 | stop: beam unchanged | | | | | 8443 | 1039 | 38 | 5 | 1487 |

```
S' = ((S + -0.418·(S·P2·k)⊗(P2·k)) + (v)⊗(P1·P2·k))
P1' = (P1 + -0.418·(P1·P1·P2·k)⊗(P1·P2·k))
P2' = ((P2 + -0.036·(P2·k)⊗(P2·k)) + 0.039·((P1 + -0.418·(P1·P1·P2·k)⊗(P1·P2·k)))ᵀ)

Effective program (21 instructions):
  V0 = MatVec(M2, V0)
  M3 = Outer(V0, V0)
  s0 = -0.0357
  M3 = MatScale(s0, M3)
  M2 = MatAdd(M2, M3)
  V2 = MatVec(M0, V0)
  M3 = Outer(V2, V0)
  V0 = MatVec(M1, V0)
  s0 = -0.4181
  M3 = MatScale(s0, M3)
  M0 = MatAdd(M0, M3)
  M3 = Outer(V1, V0)
  M0 = MatAdd(M0, M3)
  V1 = MatVec(M1, V0)
  M3 = Outer(V1, V0)
  M3 = MatScale(s0, M3)
  M1 = MatAdd(M1, M3)
  M3 = Transpose(M1)
  s0 = 0.0389
  M3 = MatScale(s0, M3)
  M2 = MatAdd(M2, M3)

structure: unclassified  [a=0.996 b=0.547 c=-0.591 g=-0.075, erase c/a=0.594, R²=0.7453, 1408 steps]

train acc 0.805 ±0.011
test regime collision3: acc 0.790  margin 0.178  ±0.005
test d16 T12 ow0.3: acc 0.921  margin 0.300  ±0.004
test d16 T12 ow0.0: acc 0.974  margin 0.322  ±0.002
test d16 T12 ow0.6: acc 0.863  margin 0.235  ±0.007
test d32 T24 ow0.3: acc 0.942  margin 0.389  ±0.004
test d8 T6 ow0.3: acc 0.801  margin 0.130  ±0.008
test d16 T64 K8 ow0.3: acc 0.971  margin 0.319  ±0.004
test d16 T128 K8 ow0.3: acc 0.989  margin 0.322  ±0.003


```
