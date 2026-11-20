# grow v2, arm B, task seed 5, beam 4, compaction True

| round | best train fit | best train acc | best test acc | len | beam (train acc, len, last step) | Rust evals | grad passes | seconds |
|---|---|---|---|---|---|---|---|---|
| 1 | 0.3848 | 0.390 | 0.385 | 2 | 0.390, 2, at 0: M0 += eps * Outer(V1,V0), eps +0.001; compacted 4->2; 0.000, 0, start | 62 | 61 | 6 |
| 2 | 0.6334 | 0.631 | 0.633 | 6 | 0.631, 6, at 0: V1 += eps * MatVec(M0,V0), eps -0.3; polished; 0.525, 6, at 0: M0 += eps * MatSub(M0,M1), eps -0.1; 0.525, 7, tap V1 <- M2 V1 at 0; M2 += eps * MatSub(M1,M2) at end, eps -0.1; 0.523, 4, at 0: M0 += eps * M0, eps -0.1; compacted 5->4 | 634 | 303 | 29 |
| 3 | 0.6566 | 0.655 | 0.642 | 9 | 0.655, 9, at 3: V0 += eps * VecScale(Dot(V1,V2),V0), eps +1; compacted 11->9; 0.651, 12, tap V2 <- M2 V2 at 1; M2 += eps * MatScale(Norm(V2),M2) at end, eps +0.03; 0.649, 12, tap V1 <- M2 V1 at 4; M2 += eps * MatScale(Norm(V2),M2) at end, eps +0.03; 0.644, 11, tap V0 <- M2 V0 at 1; M2 += eps * Outer(V0,V0) at end, eps -0.003; polished | 4286 | 547 | 200 |
| 4 | 0.7263 | 0.721 | 0.716 | 16 | 0.721, 16, at 1: M2 += eps * MatScale(Norm(V2),M2), eps +0.01; polished; 0.714, 16, at 10: M1 += eps * MatScale(Dot(V2,V2),M2), eps +0.03; polished; 0.659, 14, at 1: M0 += eps * M0, eps +0.03; compacted 15->14; 0.658, 16, at 0: V0 += eps * MatVec(M0,V0), eps +0.1 | 7687 | 791 | 524 |
| 5 | 0.8348 | 0.827 | 0.811 | 21 | 0.827, 21, at 1: V0 += eps * MatVec(M2,Normalize(V0)), eps +0.1; polished; 0.801, 21, at 5: M0 += eps * MatScale(Recip(S1),M0), eps +0.001; polished; 0.792, 17, at 0: V0 += eps * V0, eps +0.3; polished; compacted 19->17; 0.781, 20, at 0: M0 += eps * Outer(V1,V0), eps -1; polished | 11165 | 1035 | 926 |
| 6 | 0.8348 | 0.827 | 0.811 | 21 | 0.827, 21, at 1: V0 += eps * MatVec(M2,Normalize(V0)), eps +0.1; polished; 0.802, 23, at 0: V0 += eps * V0, eps +0.003; compacted 24->23; 0.801, 21, at 5: M0 += eps * MatScale(Recip(S1),M0), eps +0.001; polished; 0.792, 17, at 0: V0 += eps * V0, eps +0.3; polished; compacted 19->17 | 11585 | 1099 | 1498 |
| 7 | 0.8348 | 0.827 | 0.811 | 21 | 0.827, 21, at 1: V0 += eps * MatVec(M2,Normalize(V0)), eps +0.1; polished; 0.802, 23, at 0: V0 += eps * V0, eps +0.003; compacted 24->23; 0.802, 23, at 0: V0 += eps * V0, eps +0.003; compacted 24->23; 0.801, 21, at 5: M0 += eps * MatScale(Recip(S1),M0), eps +0.001; polished | 11893 | 1163 | 2119 |
| 8 | 0.8348 | 0.827 | 0.811 | 21 | 0.827, 21, at 1: V0 += eps * MatVec(M2,Normalize(V0)), eps +0.1; polished; 0.802, 23, at 0: V0 += eps * V0, eps +0.003; compacted 24->23; 0.802, 23, at 0: V0 += eps * V0, eps +0.003; compacted 24->23; 0.801, 21, at 5: M0 += eps * MatScale(Recip(S1),M0), eps +0.001; polished | 11993 | 1227 | 2810 |
| 9 | 0.8348 | 0.827 | 0.811 | 21 | 0.827, 21, at 1: V0 += eps * MatVec(M2,Normalize(V0)), eps +0.1; polished; 0.802, 23, at 0: V0 += eps * V0, eps +0.003; compacted 24->23; 0.802, 23, at 0: V0 += eps * V0, eps +0.003; compacted 24->23; 0.801, 21, at 5: M0 += eps * MatScale(Recip(S1),M0), eps +0.001; polished | 12093 | 1291 | 3513 |
| 10 | 0.8348 | 0.827 | 0.811 | 21 | 0.827, 21, at 1: V0 += eps * MatVec(M2,Normalize(V0)), eps +0.1; polished; 0.802, 23, at 0: V0 += eps * V0, eps +0.003; compacted 24->23; 0.802, 23, at 0: V0 += eps * V0, eps +0.003; compacted 24->23; 0.801, 21, at 5: M0 += eps * MatScale(Recip(S1),M0), eps +0.001; polished | 12193 | 1355 | 4202 |
| 11 | 0.8348 | 0.827 | 0.811 | 21 | 0.827, 21, at 1: V0 += eps * MatVec(M2,Normalize(V0)), eps +0.1; polished; 0.802, 23, at 0: V0 += eps * V0, eps +0.003; compacted 24->23; 0.802, 23, at 0: V0 += eps * V0, eps +0.003; compacted 24->23; 0.801, 21, at 5: M0 += eps * MatScale(Recip(S1),M0), eps +0.001; polished | 12293 | 1419 | 4902 |
| 12 | 0.8348 | 0.827 | 0.811 | 21 | 0.827, 21, at 1: V0 += eps * MatVec(M2,Normalize(V0)), eps +0.1; polished; 0.802, 23, at 0: V0 += eps * V0, eps +0.003; compacted 24->23; 0.802, 23, at 0: V0 += eps * V0, eps +0.003; compacted 24->23; 0.801, 21, at 5: M0 += eps * MatScale(Recip(S1),M0), eps +0.001; polished | 12393 | 1483 | 5608 |
| 13 | 0.8348 | 0.827 | 0.811 | 21 | 0.827, 21, at 1: V0 += eps * MatVec(M2,Normalize(V0)), eps +0.1; polished; 0.802, 23, at 0: V0 += eps * V0, eps +0.003; compacted 24->23; 0.802, 23, at 0: V0 += eps * V0, eps +0.003; compacted 24->23; 0.801, 21, at 5: M0 += eps * MatScale(Recip(S1),M0), eps +0.001; polished | 12493 | 1547 | 6319 |
| 14 | 0.8348 | 0.827 | 0.811 | 21 | 0.827, 21, at 1: V0 += eps * MatVec(M2,Normalize(V0)), eps +0.1; polished; 0.802, 23, at 0: V0 += eps * V0, eps +0.003; compacted 24->23; 0.802, 23, at 0: V0 += eps * V0, eps +0.003; compacted 24->23; 0.801, 21, at 5: M0 += eps * MatScale(Recip(S1),M0), eps +0.001; polished | 12593 | 1611 | 7044 |
| 15 | 0.8348 | 0.827 | 0.811 | 21 | 0.827, 21, at 1: V0 += eps * MatVec(M2,Normalize(V0)), eps +0.1; polished; 0.802, 23, at 0: V0 += eps * V0, eps +0.003; compacted 24->23; 0.802, 23, at 0: V0 += eps * V0, eps +0.003; compacted 24->23; 0.801, 21, at 5: M0 += eps * MatScale(Recip(S1),M0), eps +0.001; polished | 12693 | 1675 | 7760 |
| 16 | 0.8348 | 0.827 | 0.811 | 21 | 0.827, 21, at 1: V0 += eps * MatVec(M2,Normalize(V0)), eps +0.1; polished; 0.802, 23, at 0: V0 += eps * V0, eps +0.003; compacted 24->23; 0.802, 23, at 0: V0 += eps * V0, eps +0.003; compacted 24->23; 0.801, 21, at 5: M0 += eps * MatScale(Recip(S1),M0), eps +0.001; polished | 12793 | 1739 | 8452 |
| 17 | 0.8348 | 0.827 | 0.811 | 21 | 0.827, 21, at 1: V0 += eps * MatVec(M2,Normalize(V0)), eps +0.1; polished; 0.802, 23, at 0: V0 += eps * V0, eps +0.003; compacted 24->23; 0.802, 23, at 0: V0 += eps * V0, eps +0.003; compacted 24->23; 0.801, 21, at 5: M0 += eps * MatScale(Recip(S1),M0), eps +0.001; polished | 12893 | 1803 | 9139 |
| 18 | 0.8348 | 0.827 | 0.811 | 21 | 0.827, 21, at 1: V0 += eps * MatVec(M2,Normalize(V0)), eps +0.1; polished; 0.802, 23, at 0: V0 += eps * V0, eps +0.003; compacted 24->23; 0.802, 23, at 0: V0 += eps * V0, eps +0.003; compacted 24->23; 0.801, 21, at 5: M0 += eps * MatScale(Recip(S1),M0), eps +0.001; polished | 12993 | 1867 | 9878 |
| 19 | 0.8348 | 0.827 | 0.811 | 21 | 0.827, 21, at 1: V0 += eps * MatVec(M2,Normalize(V0)), eps +0.1; polished; 0.802, 23, at 0: V0 += eps * V0, eps +0.003; compacted 24->23; 0.802, 23, at 0: V0 += eps * V0, eps +0.003; compacted 24->23; 0.801, 21, at 5: M0 += eps * MatScale(Recip(S1),M0), eps +0.001; polished | 13093 | 1931 | 10593 |
| 20 | 0.8348 | 0.827 | 0.811 | 21 | 0.827, 21, at 1: V0 += eps * MatVec(M2,Normalize(V0)), eps +0.1; polished; 0.802, 23, at 0: V0 += eps * V0, eps +0.003; compacted 24->23; 0.802, 23, at 0: V0 += eps * V0, eps +0.003; compacted 24->23; 0.801, 21, at 5: M0 += eps * MatScale(Recip(S1),M0), eps +0.001; polished | 13193 | 1995 | 11286 |

```
S' = (S + ((v + -1.149·S·k))⊗((P2 + 0.037·|S·k|·P2)·(k + 0.363·P2·norm(k))))
P1' = -0.286·((P2 + 0.037·|S·k|·P2)·(k + 0.363·P2·norm(k)))⊗((P2 + 0.037·|S·k|·P2)·(k + 0.363·P2·norm(k)))
P2' = ((P2 + 0.037·|S·k|·P2) + -0.286·((P2 + 0.037·|S·k|·P2)·(k + 0.363·P2·norm(k)))⊗((P2 + 0.037·|S·k|·P2)·(k + 0.363·P2·norm(k))))

Effective program (21 instructions):
  V2 = MatVec(M0, V0)
  V3 = Normalize(V0)
  V4 = MatVec(M2, V3)
  s0 = 0.3635
  V4 = VecScale(s0, V4)
  V0 = VecAdd(V0, V4)
  s0 = Norm(V2)
  M1 = MatScale(s0, M2)
  s1 = 0.0367
  M1 = MatScale(s1, M1)
  M2 = MatAdd(M2, M1)
  V0 = MatVec(M2, V0)
  s0 = -1.1491
  V2 = VecScale(s0, V2)
  V1 = VecAdd(V1, V2)
  M1 = Outer(V1, V0)
  M0 = MatAdd(M0, M1)
  M1 = Outer(V0, V0)
  s0 = -0.2861
  M1 = MatScale(s0, M1)
  M2 = MatAdd(M2, M1)

structure: unclassified  [a=0.994 b=0.686 c=-0.771 g=0.016, erase c/a=0.776, R²=0.6307, 1408 steps]

train acc 0.827 ±0.011
test regime collision3: acc 0.811  margin 0.186  ±0.005
test d16 T12 ow0.3: acc 0.914  margin 0.285  ±0.004
test d16 T12 ow0.0: acc 0.907  margin 0.261  ±0.004
test d16 T12 ow0.6: acc 0.856  margin 0.228  ±0.007
test d32 T24 ow0.3: acc 0.831  margin 0.230  ±0.006
test d8 T6 ow0.3: acc 0.846  margin 0.151  ±0.008
test d16 T64 K8 ow0.3: acc 0.955  margin 0.263  ±0.005
test d16 T128 K8 ow0.3: acc 0.000  margin 0.000  ±0.000


```
