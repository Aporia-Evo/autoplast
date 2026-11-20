# grow v2, arm B, task seed 3, beam 4, compaction True

| round | best train fit | best train acc | best test acc | len | beam (train acc, len, last step) | Rust evals | grad passes | seconds |
|---|---|---|---|---|---|---|---|---|
| 1 | 0.4112 | 0.416 | 0.387 | 3 | 0.416, 3, at 0: M0 += eps * Outer(V1,Tanh(V0)), eps +0.001; compacted 5->3; 0.000, 0, start | 65 | 61 | 7 |
| 2 | 0.6484 | 0.646 | 0.634 | 8 | 0.646, 8, at 1: V1 += eps * MatVec(M0,VecAdd(V0,V2)), eps -0.3; 0.517, 7, at 0: M0 += eps * MatSub(M0,M1), eps -0.1; 0.517, 10, tap V1 <- M2 V1 at 0; M2 += eps * MatScale(Dot(V2,V2),Transpose(M2)) at end, eps +0.1; 0.516, 8, at 0: M0 += eps * MatScale(Dot(V0,V0),M0), eps -0.1 | 943 | 303 | 33 |
| 3 | 0.6689 | 0.667 | 0.650 | 14 | 0.667, 14, tap V2 <- M2 V2 at 2; M2 += eps * Outer(V3,Normalize(V2)) at end, eps -0.01; 0.655, 14, tap V0 <- M2 V0 at 0; M2 += eps * Outer(Tanh(V2),V0) at end, eps -0.01; 0.649, 14, tap V4 <- M2 V4 at 3; M2 += eps * MatScale(Dot(V2,V2),M2) at end, eps +0.001; 0.648, 14, tap V3 <- M2 V3 at 2; M2 += eps * Outer(Normalize(V2),V0) at end, eps -0.003 | 4732 | 547 | 268 |
| 4 | 0.6689 | 0.667 | 0.650 | 14 | 0.667, 14, tap V2 <- M2 V2 at 2; M2 += eps * Outer(V3,Normalize(V2)) at end, eps -0.01; 0.667, 14, at 13: M1 += eps * Outer(MatVec(M1,V2),V3), eps +0.01; compacted 19->14; 0.667, 14, at 13: M2 += eps * Outer(MatVec(M1,V2),V3), eps +0.01; compacted 19->14; 0.657, 19, at 11: M2 += eps * MatScale(Norm(V3),M1), eps -0.003 | 8331 | 731 | 719 |
| 5 | 0.6689 | 0.667 | 0.650 | 14 | 0.667, 14, tap V2 <- M2 V2 at 2; M2 += eps * Outer(V3,Normalize(V2)) at end, eps -0.01; 0.667, 14, at 13: M1 += eps * Outer(MatVec(M1,V2),V3), eps +0.01; compacted 19->14; 0.667, 14, at 13: M2 += eps * Outer(MatVec(M1,V2),V3), eps +0.01; compacted 19->14; 0.657, 19, at 11: M2 += eps * MatScale(Norm(V3),M1), eps -0.003 | 11216 | 855 | 1241 |
| 6 | 0.6689 | 0.667 | 0.650 | 14 | 0.667, 14, tap V2 <- M2 V2 at 2; M2 += eps * Outer(V3,Normalize(V2)) at end, eps -0.01; 0.667, 14, at 13: M1 += eps * Outer(MatVec(M1,V2),V3), eps +0.01; compacted 19->14; 0.667, 14, at 13: M2 += eps * Outer(MatVec(M1,V2),V3), eps +0.01; compacted 19->14; 0.657, 19, at 11: M2 += eps * MatScale(Norm(V3),M1), eps -0.003 | 14101 | 979 | 1758 |
| 7 | 0.6689 | 0.667 | 0.650 | 14 | 0.667, 14, tap V2 <- M2 V2 at 2; M2 += eps * Outer(V3,Normalize(V2)) at end, eps -0.01; 0.667, 14, at 13: M1 += eps * Outer(MatVec(M1,V2),V3), eps +0.01; compacted 19->14; 0.667, 14, at 13: M2 += eps * Outer(MatVec(M1,V2),V3), eps +0.01; compacted 19->14; 0.657, 19, at 11: M2 += eps * MatScale(Norm(V3),M1), eps -0.003 | 16986 | 1103 | 2275 |
| 8 | 0.6689 | 0.667 | 0.650 | 14 | 0.667, 14, tap V2 <- M2 V2 at 2; M2 += eps * Outer(V3,Normalize(V2)) at end, eps -0.01; 0.667, 14, at 13: M1 += eps * Outer(MatVec(M1,V2),V3), eps +0.01; compacted 19->14; 0.667, 14, at 13: M2 += eps * Outer(MatVec(M1,V2),V3), eps +0.01; compacted 19->14; 0.657, 19, at 11: M2 += eps * MatScale(Norm(V3),M1), eps -0.003 | 19871 | 1227 | 2775 |
| 9 | 0.6689 | 0.667 | 0.650 | 14 | 0.667, 14, tap V2 <- M2 V2 at 2; M2 += eps * Outer(V3,Normalize(V2)) at end, eps -0.01; 0.667, 14, at 13: M1 += eps * Outer(MatVec(M1,V2),V3), eps +0.01; compacted 19->14; 0.667, 14, at 13: M2 += eps * Outer(MatVec(M1,V2),V3), eps +0.01; compacted 19->14; 0.657, 19, at 11: M2 += eps * MatScale(Norm(V3),M1), eps -0.003 | 22756 | 1351 | 3272 |
| 10 | 0.6689 | 0.667 | 0.650 | 14 | 0.667, 14, tap V2 <- M2 V2 at 2; M2 += eps * Outer(V3,Normalize(V2)) at end, eps -0.01; 0.667, 14, at 13: M1 += eps * Outer(MatVec(M1,V2),V3), eps +0.01; compacted 19->14; 0.667, 14, at 13: M2 += eps * Outer(MatVec(M1,V2),V3), eps +0.01; compacted 19->14; 0.657, 19, at 11: M2 += eps * MatScale(Norm(V3),M1), eps -0.003 | 25641 | 1475 | 3798 |
| 11 | 0.6689 | 0.667 | 0.650 | 14 | 0.667, 14, tap V2 <- M2 V2 at 2; M2 += eps * Outer(V3,Normalize(V2)) at end, eps -0.01; 0.667, 14, at 13: M1 += eps * Outer(MatVec(M1,V2),V3), eps +0.01; compacted 19->14; 0.667, 14, at 13: M2 += eps * Outer(MatVec(M1,V2),V3), eps +0.01; compacted 19->14; 0.657, 19, at 11: M2 += eps * MatScale(Norm(V3),M1), eps -0.003 | 28526 | 1599 | 4317 |
| 12 | 0.6689 | 0.667 | 0.650 | 14 | 0.667, 14, tap V2 <- M2 V2 at 2; M2 += eps * Outer(V3,Normalize(V2)) at end, eps -0.01; 0.667, 14, at 13: M1 += eps * Outer(MatVec(M1,V2),V3), eps +0.01; compacted 19->14; 0.667, 14, at 13: M2 += eps * Outer(MatVec(M1,V2),V3), eps +0.01; compacted 19->14; 0.657, 19, at 11: M2 += eps * MatScale(Norm(V3),M1), eps -0.003 | 31411 | 1723 | 4835 |
| 13 | 0.6689 | 0.667 | 0.650 | 14 | 0.667, 14, tap V2 <- M2 V2 at 2; M2 += eps * Outer(V3,Normalize(V2)) at end, eps -0.01; 0.667, 14, at 13: M1 += eps * Outer(MatVec(M1,V2),V3), eps +0.01; compacted 19->14; 0.667, 14, at 13: M2 += eps * Outer(MatVec(M1,V2),V3), eps +0.01; compacted 19->14; 0.657, 19, at 11: M2 += eps * MatScale(Norm(V3),M1), eps -0.003 | 34296 | 1847 | 5377 |
| 14 | 0.6689 | 0.667 | 0.650 | 14 | 0.667, 14, tap V2 <- M2 V2 at 2; M2 += eps * Outer(V3,Normalize(V2)) at end, eps -0.01; 0.667, 14, at 13: M1 += eps * Outer(MatVec(M1,V2),V3), eps +0.01; compacted 19->14; 0.667, 14, at 13: M2 += eps * Outer(MatVec(M1,V2),V3), eps +0.01; compacted 19->14; 0.657, 19, at 11: M2 += eps * MatScale(Norm(V3),M1), eps -0.003 | 37181 | 1971 | 5886 |
| 15 | 0.6689 | 0.667 | 0.650 | 14 | 0.667, 14, tap V2 <- M2 V2 at 2; M2 += eps * Outer(V3,Normalize(V2)) at end, eps -0.01; 0.667, 14, at 13: M1 += eps * Outer(MatVec(M1,V2),V3), eps +0.01; compacted 19->14; 0.667, 14, at 13: M2 += eps * Outer(MatVec(M1,V2),V3), eps +0.01; compacted 19->14; 0.657, 19, at 11: M2 += eps * MatScale(Norm(V3),M1), eps -0.003 | 40066 | 2095 | 6387 |
| 16 | 0.6689 | 0.667 | 0.650 | 14 | 0.667, 14, tap V2 <- M2 V2 at 2; M2 += eps * Outer(V3,Normalize(V2)) at end, eps -0.01; 0.667, 14, at 13: M1 += eps * Outer(MatVec(M1,V2),V3), eps +0.01; compacted 19->14; 0.667, 14, at 13: M2 += eps * Outer(MatVec(M1,V2),V3), eps +0.01; compacted 19->14; 0.657, 19, at 11: M2 += eps * MatScale(Norm(V3),M1), eps -0.003 | 42951 | 2219 | 6892 |
| 17 | 0.6689 | 0.667 | 0.650 | 14 | 0.667, 14, tap V2 <- M2 V2 at 2; M2 += eps * Outer(V3,Normalize(V2)) at end, eps -0.01; 0.667, 14, at 13: M1 += eps * Outer(MatVec(M1,V2),V3), eps +0.01; compacted 19->14; 0.667, 14, at 13: M2 += eps * Outer(MatVec(M1,V2),V3), eps +0.01; compacted 19->14; 0.657, 19, at 11: M2 += eps * MatScale(Norm(V3),M1), eps -0.003 | 45836 | 2343 | 7392 |
| 18 | 0.6689 | 0.667 | 0.650 | 14 | 0.667, 14, tap V2 <- M2 V2 at 2; M2 += eps * Outer(V3,Normalize(V2)) at end, eps -0.01; 0.667, 14, at 13: M1 += eps * Outer(MatVec(M1,V2),V3), eps +0.01; compacted 19->14; 0.667, 14, at 13: M2 += eps * Outer(MatVec(M1,V2),V3), eps +0.01; compacted 19->14; 0.657, 19, at 11: M2 += eps * MatScale(Norm(V3),M1), eps -0.003 | 48721 | 2467 | 7902 |
| 19 | 0.6689 | 0.667 | 0.650 | 14 | 0.667, 14, tap V2 <- M2 V2 at 2; M2 += eps * Outer(V3,Normalize(V2)) at end, eps -0.01; 0.667, 14, at 13: M1 += eps * Outer(MatVec(M1,V2),V3), eps +0.01; compacted 19->14; 0.667, 14, at 13: M2 += eps * Outer(MatVec(M1,V2),V3), eps +0.01; compacted 19->14; 0.657, 19, at 11: M2 += eps * MatScale(Norm(V3),M1), eps -0.003 | 51606 | 2591 | 8398 |
| 20 | 0.6689 | 0.667 | 0.650 | 14 | 0.667, 14, tap V2 <- M2 V2 at 2; M2 += eps * Outer(V3,Normalize(V2)) at end, eps -0.01; 0.667, 14, at 13: M1 += eps * Outer(MatVec(M1,V2),V3), eps +0.01; compacted 19->14; 0.667, 14, at 13: M2 += eps * Outer(MatVec(M1,V2),V3), eps +0.01; compacted 19->14; 0.657, 19, at 11: M2 += eps * MatScale(Norm(V3),M1), eps -0.003 | 54491 | 2715 | 8898 |

```
S' = (S + ((v + -0.300·S·(k + tanh(k))))⊗(P2·tanh(k)))
P1' = -0.010·((k + tanh(k)))⊗(norm(P2·tanh(k)))
P2' = (P2 + -0.010·((k + tanh(k)))⊗(norm(P2·tanh(k))))

Effective program (14 instructions):
  V2 = Tanh(V0)
  V3 = VecAdd(V0, V2)
  V2 = MatVec(M2, V2)
  V4 = MatVec(M0, V3)
  s0 = -0.3000
  V4 = VecScale(s0, V4)
  V1 = VecAdd(V1, V4)
  M1 = Outer(V1, V2)
  M0 = MatAdd(M0, M1)
  V0 = Normalize(V2)
  M1 = Outer(V3, V0)
  s0 = -0.0100
  M1 = MatScale(s0, M1)
  M2 = MatAdd(M2, M1)

structure: unclassified  [a=1.000 b=0.846 c=-0.484 g=-0.027, erase c/a=0.484, R²=0.9828, 1408 steps]

train acc 0.667 ±0.013
test regime collision3: acc 0.650  margin 0.059  ±0.006
test d16 T12 ow0.3: acc 0.929  margin 0.271  ±0.004
test d16 T12 ow0.0: acc 0.899  margin 0.241  ±0.004
test d16 T12 ow0.6: acc 0.948  margin 0.274  ±0.004
test d32 T24 ow0.3: acc 0.987  margin 0.362  ±0.002
test d8 T6 ow0.3: acc 0.791  margin 0.116  ±0.008
test d16 T64 K8 ow0.3: acc 0.853  margin 0.154  ±0.008
test d16 T128 K8 ow0.3: acc 0.703  margin 0.076  ±0.014


```
