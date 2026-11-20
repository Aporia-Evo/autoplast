# grow v2, arm B, task seed 8, beam 4, compaction True

| round | best train fit | best train acc | best test acc | len | beam (train acc, len, last step) | Rust evals | grad passes | seconds |
|---|---|---|---|---|---|---|---|---|
| 1 | 0.4191 | 0.424 | 0.385 | 2 | 0.424, 2, at 0: M0 += eps * Outer(V1,V0), eps +0.001; compacted 4->2; 0.000, 0, start | 62 | 61 | 6 |
| 2 | 0.6650 | 0.662 | 0.642 | 7 | 0.662, 7, at 0: V1 += eps * MatVec(M0,Tanh(V0)), eps -1; polished; 0.558, 8, at 0: M0 += eps * MatScale(Norm(V0),MatSub(M0,M1)), eps -0.1; 0.556, 5, at 1: M0 += eps * MatSub(M0,M1), eps -0.1; compacted 6->5; 0.556, 6, at 1: M1 += eps * MatSub(M0,M1), eps -0.1 | 621 | 303 | 23 |
| 3 | 0.6823 | 0.680 | 0.648 | 13 | 0.680, 13, tap V3 <- M2 V3 at 2; M2 += eps * MatScale(Dot(V3,V3),M2) at end, eps +0.03; 0.680, 13, tap V2 <- M2 V2 at 1; M2 += eps * MatScale(Dot(V3,V3),M2) at end, eps +0.03; 0.680, 13, tap V0 <- M2 V0 at 0; M2 += eps * MatScale(Dot(V3,V3),M2) at end, eps +0.01; 0.675, 13, tap V1 <- M2 V1 at 5; M2 += eps * MatScale(Dot(V3,V3),M2) at end, eps +0.03 | 3886 | 547 | 181 |
| 4 | 0.6836 | 0.681 | 0.647 | 17 | 0.681, 17, at 0: M2 += eps * Transpose(M2), eps +0.001; 0.681, 17, at 0: M2 += eps * MatSub(M1,M2), eps -0.001; 0.681, 17, at 11: S1 += eps * SMul(S0,S1), eps +0.3; 0.681, 17, at 0: M2 += eps * Outer(V0,V0), eps -0.01 | 7188 | 791 | 541 |
| 5 | stop: beam unchanged | | | | | 9844 | 795 | 949 |

```
S' = (S + ((v + -0.405·(P2 + 0.001·(P2)ᵀ)·S·tanh(k)))⊗(k))
P1' = 0.030·<-0.405·(P2 + 0.001·(P2)ᵀ)·S·tanh(k), -0.405·(P2 + 0.001·(P2)ᵀ)·S·tanh(k)>·(P2 + 0.001·(P2)ᵀ)
P2' = ((P2 + 0.001·(P2)ᵀ) + 0.030·<-0.405·(P2 + 0.001·(P2)ᵀ)·S·tanh(k), -0.405·(P2 + 0.001·(P2)ᵀ)·S·tanh(k)>·(P2 + 0.001·(P2)ᵀ))

Effective program (17 instructions):
  M1 = Transpose(M2)
  s0 = 0.0010
  M1 = MatScale(s0, M1)
  M2 = MatAdd(M2, M1)
  V2 = Tanh(V0)
  V3 = MatVec(M0, V2)
  V3 = MatVec(M2, V3)
  s0 = -0.4045
  V3 = VecScale(s0, V3)
  V1 = VecAdd(V1, V3)
  M1 = Outer(V1, V0)
  M0 = MatAdd(M0, M1)
  s0 = Dot(V3, V3)
  M1 = MatScale(s0, M2)
  s1 = 0.0300
  M1 = MatScale(s1, M1)
  M2 = MatAdd(M2, M1)

structure: delta rule  [a=1.000 b=1.001 c=-0.493 g=-0.011, erase c/a=0.493, R²=0.9910, 1408 steps]

train acc 0.681 ±0.013
test regime collision3: acc 0.647  margin 0.054  ±0.006
test d16 T12 ow0.3: acc 0.922  margin 0.246  ±0.004
test d16 T12 ow0.0: acc 0.918  margin 0.237  ±0.004
test d16 T12 ow0.6: acc 0.920  margin 0.230  ±0.005
test d32 T24 ow0.3: acc 0.987  margin 0.336  ±0.002
test d8 T6 ow0.3: acc 0.772  margin 0.101  ±0.009
test d16 T64 K8 ow0.3: acc 0.841  margin 0.207  ±0.008
test d16 T128 K8 ow0.3: acc 0.000  margin 0.000  ±0.000


```
