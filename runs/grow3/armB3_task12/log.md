# grow v3, arm B, task seed 12, beam 4, compaction, stability gate 100

| round | best train fit | best train acc | best test acc | len | beam (train acc, len, last step) | Rust evals | grad passes | gate evals | refused by gate | seconds |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | 0.3674 | 0.374 | 0.385 | 2 | 0.374, 2, at 0: M0 += eps * Outer(V1,V0), eps +0.001; compacted 4->2; 0.000, 0, start | 62 | 61 | 4 | 0 | 6 |
| 2 | 0.6217 | 0.621 | 0.633 | 7 | 0.621, 7, at 0: V1 += eps * MatVec(M0,Normalize(V0)), eps -0.3; polished; 0.621, 7, at 0: M0 += eps * Outer(MatVec(M0,V0),V0), eps -0.3; polished; 0.502, 4, at 0: M0 += eps * M0, eps -0.1; compacted 5->4; 0.421, 6, at 0: M0 += eps * MatScale(Norm(V1),MatSub(M0,M1)), eps -0.03; polished; compacted 8->6 | 478 | 303 | 17 | 3 | 25 |
| 3 | 0.7290 | 0.724 | 0.730 | 12 | 0.724, 12, tap V0 <- M1 V0 at 2; M1 += eps * Outer(V0,Tanh(V0)) at end, eps -0.3; polished; compacted 13->12; 0.724, 12, tap V0 <- M2 V0 at 2; M2 += eps * Outer(V0,Tanh(V0)) at end, eps -0.3; polished; compacted 13->12; 0.635, 13, tap V1 <- M2 V1 at 5; M2 += eps * MatScale(Norm(V2),M1) at end, eps +0.01; 0.622, 11, tap V1 <- M1 V1 at 0; M1 += eps * Outer(V1,Tanh(V1)) at end, eps -0.03; compacted 13->11 | 3764 | 547 | 55 | 30 | 198 |
| 4 | 0.7781 | 0.772 | 0.769 | 16 | 0.772, 16, at 6: M0 += eps * MatScale(S0,M0), eps +0.1; polished; 0.766, 16, at 1: M0 += eps * MatMul(M0,M1), eps -0.03; polished; 0.756, 17, at 0: M1 += eps * Outer(V0,Tanh(V0)), eps +0.03; polished; 0.756, 17, at 0: M2 += eps * Outer(V0,Tanh(V0)), eps +0.03; polished | 6275 | 791 | 63 | 30 | 504 |
| 5 | 0.8075 | 0.801 | 0.799 | 23 | 0.801, 23, tap V0 <- M2 V0 at 1; M2 += eps * MatScale(Norm(V1),MatSub(M1,M2)) at end, eps +0.03; polished; 0.795, 22, at 10: M0 += eps * MatScale(Dot(V0,V0),MatMul(M0,M1)), eps +0.1; polished; 0.774, 22, at 6: M1 += eps * MatScale(Dot(V0,V0),MatSub(M1,M2)), eps +0.003; 0.772, 16, at 6: M0 += eps * MatScale(S0,M0), eps +0.1; polished | 7874 | 975 | 69 | 31 | 953 |
| 6 | 0.8083 | 0.802 | 0.799 | 23 | 0.802, 23, tap V0 <- M2 V0 at 1; M2 += eps * MatScale(Norm(V0),MatSub(M1,M2)) at end, eps +0.03; polished; 0.801, 23, tap V0 <- M2 V0 at 1; M2 += eps * MatScale(Norm(V1),MatSub(M1,M2)) at end, eps +0.03; polished; 0.795, 22, at 10: M0 += eps * MatScale(Dot(V0,V0),MatMul(M0,M1)), eps +0.1; polished; 0.774, 22, at 6: M1 += eps * MatScale(Dot(V0,V0),MatSub(M1,M2)), eps +0.003 | 8307 | 1039 | 72 | 32 | 1471 |
| 7 | stop: beam unchanged | | | | | 8307 | 1043 | 72 | 32 | 2015 |

```
S' = (((S + -0.642·(S·k)⊗(P2·k)) + 0.080·-0.642·(S + -0.642·(S·k)⊗(P2·k))) + (v)⊗(P1·P2·k))
P1' = (P1 + -0.642·(P1·P2·k)⊗(tanh(P1·P2·k)))
P2' = (P2 + 0.098·|P1·P2·k|·((P1 + -0.642·(P1·P2·k)⊗(tanh(P1·P2·k))) - P2))

Effective program (23 instructions):
  V2 = MatVec(M0, V0)
  V0 = MatVec(M2, V0)
  M3 = Outer(V2, V0)
  V0 = MatVec(M1, V0)
  s0 = -0.6416
  M3 = MatScale(s0, M3)
  M0 = MatAdd(M0, M3)
  M3 = MatScale(s0, M0)
  s1 = 0.0800
  M3 = MatScale(s1, M3)
  M0 = MatAdd(M0, M3)
  M3 = Outer(V1, V0)
  M0 = MatAdd(M0, M3)
  V1 = Tanh(V0)
  M3 = Outer(V0, V1)
  M3 = MatScale(s0, M3)
  M1 = MatAdd(M1, M3)
  s0 = Norm(V0)
  M3 = MatSub(M1, M2)
  M3 = MatScale(s0, M3)
  s0 = 0.0981
  M3 = MatScale(s0, M3)
  M2 = MatAdd(M2, M3)

structure: unclassified  [a=0.949 b=0.334 c=-0.519 g=-0.087, erase c/a=0.547, R²=0.5604, 1408 steps]

train acc 0.802 ±0.011
test regime collision3: acc 0.799  margin 0.167  ±0.005
test d16 T12 ow0.3: acc 0.884  margin 0.292  ±0.005
test d16 T12 ow0.0: acc 0.989  margin 0.342  ±0.001
test d16 T12 ow0.6: acc 0.841  margin 0.224  ±0.007
test d32 T24 ow0.3: acc 0.893  margin 0.354  ±0.005
test d8 T6 ow0.3: acc 0.829  margin 0.147  ±0.008
test d16 T64 K8 ow0.3: acc 0.931  margin 0.209  ±0.006
test d16 T128 K8 ow0.3: acc 0.901  margin 0.189  ±0.009


```
