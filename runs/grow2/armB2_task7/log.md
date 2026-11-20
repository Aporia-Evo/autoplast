# grow v2, arm B, task seed 7, beam 4, compaction True

| round | best train fit | best train acc | best test acc | len | beam (train acc, len, last step) | Rust evals | grad passes | seconds |
|---|---|---|---|---|---|---|---|---|
| 1 | 0.3891 | 0.394 | 0.385 | 2 | 0.394, 2, at 0: M0 += eps * Outer(V1,V0), eps +0.001; compacted 4->2; 0.000, 0, start | 62 | 61 | 6 |
| 2 | 0.6510 | 0.649 | 0.640 | 7 | 0.649, 7, at 0: V1 += eps * MatVec(M0,Tanh(V0)), eps -1; polished; 0.541, 7, at 0: M0 += eps * MatScale(Dot(V1,V1),M0), eps -0.1; 0.541, 7, at 1: M1 += eps * MatScale(Dot(V1,V1),M0), eps -0.1; 0.538, 5, tap V0 <- M2 V0 at 0; M2 += eps * M2 at end, eps +0.1; compacted 6->5 | 540 | 303 | 22 |
| 3 | 0.6658 | 0.664 | 0.648 | 13 | 0.664, 13, tap V2 <- M2 V2 at 1; M2 += eps * MatScale(Dot(V3,V3),M2) at end, eps +0.03; 0.664, 13, tap V3 <- M2 V3 at 2; M2 += eps * MatScale(Dot(V3,V3),M2) at end, eps +0.03; 0.655, 13, tap V0 <- M2 V0 at 0; M2 += eps * Outer(V0,Tanh(V2)) at end, eps +0.003; 0.649, 7, at 0: V1 += eps * MatVec(M0,Tanh(V0)), eps -1; polished | 4015 | 487 | 181 |
| 4 | 0.6687 | 0.667 | 0.651 | 17 | 0.667, 17, at 4: M2 += eps * Outer(VecScale(S0,V0),V0), eps +0.03; compacted 18->17; 0.664, 18, at 12: M1 += eps * Outer(V0,Tanh(V0)), eps -0.01; 0.664, 13, tap V2 <- M2 V2 at 1; M2 += eps * MatScale(Dot(V3,V3),M2) at end, eps +0.03; 0.664, 13, tap V3 <- M2 V3 at 2; M2 += eps * MatScale(Dot(V3,V3),M2) at end, eps +0.03 | 6996 | 611 | 509 |
| 5 | 0.6690 | 0.668 | 0.651 | 22 | 0.668, 22, at 5: M2 += eps * Outer(V2,Tanh(V2)), eps +0.001; 0.668, 22, at 8: M1 += eps * Outer(V2,Tanh(V2)), eps +0.001; 0.667, 17, at 4: M2 += eps * Outer(VecScale(S0,V0),V0), eps +0.03; compacted 18->17; 0.664, 18, at 12: M1 += eps * Outer(V0,Tanh(V0)), eps -0.01 | 10431 | 735 | 941 |
| 6 | 0.6690 | 0.668 | 0.651 | 22 | 0.668, 22, at 5: M2 += eps * Outer(V2,Tanh(V2)), eps +0.001; 0.668, 22, at 8: M1 += eps * Outer(V2,Tanh(V2)), eps +0.001; 0.668, 22, at 6: M2 += eps * Outer(V2,Tanh(V2)), eps +0.001; 0.668, 22, at 8: M1 += eps * Outer(V2,Tanh(V0)), eps +0.001 | 12266 | 859 | 1609 |
| 7 | stop: beam unchanged | | | | | 12266 | 863 | 2439 |

```
S' = (S + ((v + -0.394·S·P2·tanh(k)))⊗(k))
P1' = 0.030·<-0.394·S·P2·tanh(k), -0.394·S·P2·tanh(k)>·((P2 + 0.001·(-0.394·k)⊗(tanh(-0.394·k))) + 0.030·(-0.394·k)⊗(k))
P2' = (((P2 + 0.001·(-0.394·k)⊗(tanh(-0.394·k))) + 0.030·(-0.394·k)⊗(k)) + 0.030·<-0.394·S·P2·tanh(k), -0.394·S·P2·tanh(k)>·((P2 + 0.001·(-0.394·k)⊗(tanh(-0.394·k))) + 0.030·(-0.394·k)⊗(k)))

Effective program (22 instructions):
  V2 = Tanh(V0)
  V2 = MatVec(M2, V2)
  V3 = MatVec(M0, V2)
  s0 = -0.3942
  V2 = VecScale(s0, V0)
  V4 = Tanh(V2)
  M1 = Outer(V2, V4)
  s1 = 0.0010
  M1 = MatScale(s1, M1)
  M2 = MatAdd(M2, M1)
  M1 = Outer(V2, V0)
  s1 = 0.0300
  M1 = MatScale(s1, M1)
  M2 = MatAdd(M2, M1)
  V3 = VecScale(s0, V3)
  V1 = VecAdd(V1, V3)
  M1 = Outer(V1, V0)
  M0 = MatAdd(M0, M1)
  s0 = Dot(V3, V3)
  M1 = MatScale(s0, M2)
  M1 = MatScale(s1, M1)
  M2 = MatAdd(M2, M1)

structure: delta rule  [a=1.000 b=1.000 c=-0.407 g=0.002, erase c/a=0.407, R²=0.9981, 1408 steps]

train acc 0.668 ±0.014
test regime collision3: acc 0.651  margin 0.054  ±0.006
test d16 T12 ow0.3: acc 0.920  margin 0.242  ±0.004
test d16 T12 ow0.0: acc 0.920  margin 0.237  ±0.003
test d16 T12 ow0.6: acc 0.905  margin 0.220  ±0.006
test d32 T24 ow0.3: acc 0.984  margin 0.330  ±0.002
test d8 T6 ow0.3: acc 0.767  margin 0.098  ±0.009
test d16 T64 K8 ow0.3: acc 0.832  margin 0.158  ±0.008
test d16 T128 K8 ow0.3: acc 0.000  margin 0.000  ±0.000


```
