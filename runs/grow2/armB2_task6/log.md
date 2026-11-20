# grow v2, arm B, task seed 6, beam 4, compaction True

| round | best train fit | best train acc | best test acc | len | beam (train acc, len, last step) | Rust evals | grad passes | seconds |
|---|---|---|---|---|---|---|---|---|
| 1 | 0.4143 | 0.420 | 0.385 | 3 | 0.420, 3, at 0: M0 += eps * Outer(Tanh(V1),V0), eps +0.001; compacted 5->3; 0.000, 0, start | 65 | 61 | 6 |
| 2 | 0.6302 | 0.630 | 0.619 | 6 | 0.630, 6, at 0: V1 += eps * MatVec(M0,Tanh(V0)), eps -1; compacted 8->6; 0.627, 8, at 1: V2 += eps * MatVec(M0,Tanh(V0)), eps -1; polished; 0.528, 7, at 0: M0 += eps * MatSub(M0,M1), eps -0.1; 0.523, 6, tap V2 <- M2 V2 at 1; M2 += eps * M2 at end, eps +0.1; compacted 7->6 | 912 | 303 | 32 |
| 3 | 0.6782 | 0.675 | 0.664 | 12 | 0.675, 12, tap V0 <- M2 V0 at 1; M2 += eps * Outer(V0,Tanh(V0)) at end, eps -0.1; 0.649, 15, tap V3 <- M2 V3 at 3; M2 += eps * MatScale(Dot(V3,V3),Transpose(M2)) at end, eps +0.03; 0.646, 14, tap V1 <- M2 V1 at 2; M2 += eps * MatScale(Norm(V3),M2) at end, eps +0.01; 0.636, 12, tap V2 <- M2 V2 at 1; M2 += eps * Outer(Tanh(V0),V0) at end, eps -0.03 | 4626 | 547 | 225 |
| 4 | 0.7217 | 0.718 | 0.692 | 17 | 0.718, 17, at 8: M2 += eps * Outer(VecSub(V0,V1),V0), eps -3; polished; 0.675, 12, tap V0 <- M2 V0 at 1; M2 += eps * Outer(V0,Tanh(V0)) at end, eps -0.1; 0.653, 20, tap V0 <- M1 V0 at 2; M1 += eps * Outer(V0,V0) at end, eps -0.3; 0.649, 15, tap V3 <- M2 V3 at 3; M2 += eps * MatScale(Dot(V3,V3),Transpose(M2)) at end, eps +0.03 | 7330 | 671 | 583 |
| 5 | 0.7930 | 0.787 | 0.752 | 21 | 0.787, 21, at 10: M1 += eps * Transpose(M2), eps -0.003; polished; 0.787, 21, at 2: M2 += eps * Transpose(M2), eps +0.01; polished; 0.784, 23, at 17: M2 += eps * MatScale(Norm(V3),Transpose(M2)), eps +0.03; polished; 0.720, 21, at 9: V2 += eps * Hadamard(V1,V2), eps -0.1 | 9269 | 915 | 1007 |
| 6 | stop: beam unchanged | | | | | 9269 | 919 | 1614 |

```
S' = (S + (tanh((v - S·tanh(k))))⊗(P2·k))
P1' = -0.036·(P2·k)⊗(tanh(P2·k))
P2' = ((P2 + -6.599·(((P2·k - tanh(P2·k)))⊗(P2·k) + -0.003·(P2)ᵀ)) + -0.036·(P2·k)⊗(tanh(P2·k)))

Effective program (21 instructions):
  V2 = Tanh(V0)
  V0 = MatVec(M2, V0)
  V3 = MatVec(M0, V2)
  V1 = VecSub(V1, V3)
  V2 = Tanh(V1)
  M1 = Outer(V2, V0)
  M0 = MatAdd(M0, M1)
  V1 = Tanh(V0)
  V2 = VecSub(V0, V1)
  M1 = Outer(V2, V0)
  M3 = Transpose(M2)
  s0 = -0.0032
  M3 = MatScale(s0, M3)
  M1 = MatAdd(M1, M3)
  s0 = -6.5990
  M1 = MatScale(s0, M1)
  M2 = MatAdd(M2, M1)
  M1 = Outer(V0, V1)
  s0 = -0.0357
  M1 = MatScale(s0, M1)
  M2 = MatAdd(M2, M1)

structure: unclassified  [a=0.995 b=0.662 c=-0.581 g=0.038, erase c/a=0.584, R²=0.7662, 1408 steps]

train acc 0.787 ±0.012
test regime collision3: acc 0.752  margin 0.157  ±0.005
test d16 T12 ow0.3: acc 0.928  margin 0.300  ±0.004
test d16 T12 ow0.0: acc 0.937  margin 0.300  ±0.003
test d16 T12 ow0.6: acc 0.890  margin 0.255  ±0.006
test d32 T24 ow0.3: acc 0.964  margin 0.379  ±0.003
test d8 T6 ow0.3: acc 0.736  margin 0.072  ±0.009
test d16 T64 K8 ow0.3: acc 0.000  margin 0.000  ±0.000
test d16 T128 K8 ow0.3: acc 0.000  margin 0.000  ±0.000


```
