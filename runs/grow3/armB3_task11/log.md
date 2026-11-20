# grow v3, arm B, task seed 11, beam 4, compaction, stability gate 100

| round | best train fit | best train acc | best test acc | len | beam (train acc, len, last step) | Rust evals | grad passes | gate evals | refused by gate | seconds |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | 0.3958 | 0.401 | 0.385 | 2 | 0.401, 2, at 0: M0 += eps * Outer(V1,V0), eps +0.001; compacted 4->2; 0.000, 0, start | 62 | 61 | 4 | 0 | 6 |
| 2 | 0.6338 | 0.632 | 0.633 | 7 | 0.632, 7, at 0: V1 += eps * MatVec(M0,Normalize(V0)), eps -0.3; polished; 0.632, 7, at 0: M0 += eps * Outer(MatVec(M0,V0),V0), eps -0.3; polished; 0.528, 7, at 0: M0 += eps * MatScale(Norm(V0),M0), eps -0.1; 0.439, 6, at 2: M0 += eps * MatSub(M0,M1), eps -0.03 | 454 | 303 | 14 | 4 | 23 |
| 3 | 0.7365 | 0.733 | 0.720 | 12 | 0.733, 12, tap V0 <- M1 V0 at 2; M1 += eps * Outer(Tanh(V0),V0) at end, eps -0.1; polished; compacted 13->12; 0.733, 12, tap V0 <- M2 V0 at 2; M2 += eps * Outer(Tanh(V0),V0) at end, eps -0.1; polished; compacted 13->12; 0.641, 13, tap V2 <- M1 V2 at 1; M1 += eps * MatScale(Norm(V2),M1) at end, eps +0.003; 0.641, 13, tap V0 <- M2 V0 at 0; M2 += eps * MatScale(Dot(V2,V2),M1) at end, eps +0.001 | 3535 | 547 | 44 | 24 | 203 |
| 4 | 0.7753 | 0.770 | 0.770 | 17 | 0.770, 17, at 6: M0 += eps * MatScale(Sigmoid(S0),M0), eps -0.1; 0.766, 16, at 0: M0 += eps * MatMul(M0,M1), eps -0.03; polished; 0.759, 16, at 6: M1 += eps * MatSub(M1,M2), eps -0.01; polished; 0.759, 16, at 6: M2 += eps * MatSub(M1,M2), eps +0.01; polished | 5613 | 791 | 51 | 24 | 538 |
| 5 | 0.8053 | 0.800 | 0.800 | 24 | 0.800, 24, tap V0 <- M2 V0 at 1; M2 += eps * MatScale(Norm(V1),MatSub(M1,M2)) at end, eps +0.03; polished; 0.798, 22, at 10: M0 += eps * MatScale(Dot(V0,V0),MatMul(M0,M1)), eps +0.1; polished; 0.777, 23, at 17: M1 += eps * MatScale(Norm(V1),MatSub(M1,M2)), eps +0.003; 0.770, 17, at 6: M0 += eps * MatScale(Sigmoid(S0),M0), eps -0.1 | 7182 | 975 | 58 | 26 | 958 |
| 6 | 0.8061 | 0.800 | 0.800 | 24 | 0.800, 24, tap V0 <- M2 V0 at 1; M2 += eps * MatScale(Norm(V0),MatSub(M1,M2)) at end, eps +0.03; polished; 0.800, 24, tap V0 <- M2 V0 at 1; M2 += eps * MatScale(Norm(V1),MatSub(M1,M2)) at end, eps +0.03; polished; 0.798, 22, at 10: M0 += eps * MatScale(Dot(V0,V0),MatMul(M0,M1)), eps +0.1; polished; 0.777, 23, at 17: M1 += eps * MatScale(Norm(V1),MatSub(M1,M2)), eps +0.003 | 7648 | 1039 | 62 | 28 | 1477 |
| 7 | stop: beam unchanged | | | | | 7648 | 1043 | 62 | 28 | 2014 |

```
S' = (((S + -0.642·(S·k)⊗(P2·k)) + -0.157·σ(-0.642)·(S + -0.642·(S·k)⊗(P2·k))) + (v)⊗(P1·P2·k))
P1' = (P1 + -0.642·(tanh(P1·P2·k))⊗(P1·P2·k))
P2' = (P2 + 0.100·|P1·P2·k|·((P1 + -0.642·(tanh(P1·P2·k))⊗(P1·P2·k)) - P2))

Effective program (24 instructions):
  V2 = MatVec(M0, V0)
  V0 = MatVec(M2, V0)
  M3 = Outer(V2, V0)
  V0 = MatVec(M1, V0)
  s0 = -0.6423
  M3 = MatScale(s0, M3)
  M0 = MatAdd(M0, M3)
  s1 = Sigmoid(s0)
  M3 = MatScale(s1, M0)
  s1 = -0.1571
  M3 = MatScale(s1, M3)
  M0 = MatAdd(M0, M3)
  M3 = Outer(V1, V0)
  M0 = MatAdd(M0, M3)
  V1 = Tanh(V0)
  M3 = Outer(V1, V0)
  M3 = MatScale(s0, M3)
  M1 = MatAdd(M1, M3)
  s0 = Norm(V0)
  M3 = MatSub(M1, M2)
  M3 = MatScale(s0, M3)
  s0 = 0.0998
  M3 = MatScale(s0, M3)
  M2 = MatAdd(M2, M3)

structure: unclassified  [a=0.944 b=0.339 c=-0.514 g=0.013, erase c/a=0.544, R²=0.5580, 1408 steps]

train acc 0.800 ±0.011
test regime collision3: acc 0.800  margin 0.168  ±0.005
test d16 T12 ow0.3: acc 0.887  margin 0.293  ±0.005
test d16 T12 ow0.0: acc 0.989  margin 0.341  ±0.001
test d16 T12 ow0.6: acc 0.852  margin 0.226  ±0.007
test d32 T24 ow0.3: acc 0.897  margin 0.355  ±0.005
test d8 T6 ow0.3: acc 0.830  margin 0.148  ±0.008
test d16 T64 K8 ow0.3: acc 0.928  margin 0.215  ±0.006
test d16 T128 K8 ow0.3: acc 0.899  margin 0.195  ±0.009


```
