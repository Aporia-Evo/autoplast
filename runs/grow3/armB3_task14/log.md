# grow v3, arm B, task seed 14, beam 4, compaction, stability gate 100

| round | best train fit | best train acc | best test acc | len | beam (train acc, len, last step) | Rust evals | grad passes | gate evals | refused by gate | seconds |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | 0.3923 | 0.398 | 0.385 | 3 | 0.398, 3, at 0: M0 += eps * Outer(Tanh(V1),V0), eps +0.001; compacted 5->3; 0.000, 0, start | 65 | 61 | 4 | 0 | 7 |
| 2 | 0.6521 | 0.650 | 0.639 | 8 | 0.650, 8, at 0: M0 += eps * Outer(MatVec(M0,V0),V0), eps -1; polished; 0.649, 8, at 0: V1 += eps * MatVec(M0,Tanh(V0)), eps -1; polished; 0.647, 8, at 1: V2 += eps * MatVec(M0,Tanh(V0)), eps -1; polished; 0.548, 8, at 1: M0 += eps * MatScale(Norm(V2),M0), eps -0.1 | 831 | 318 | 14 | 3 | 33 |
| 3 | 0.7673 | 0.762 | 0.734 | 13 | 0.762, 13, tap V0 <- M1 V0 at 2; M1 += eps * Outer(V0,V0) at end, eps -0.3; polished; 0.762, 13, tap V0 <- M2 V0 at 2; M2 += eps * Outer(V0,V0) at end, eps -0.3; polished; 0.665, 15, tap V2 <- M2 V2 at 1; M2 += eps * MatScale(Dot(V2,V2),Transpose(M1)) at end, eps +0.01; 0.663, 14, tap V0 <- M1 V0 at 0; M1 += eps * MatScale(Dot(V2,V2),M1) at end, eps +0.003; polished | 4523 | 562 | 60 | 42 | 297 |
| 4 | 0.7867 | 0.781 | 0.766 | 16 | 0.781, 16, at 0: M0 += eps * MatScale(Dot(V1,V1),MatMul(M0,M1)), eps -0.03; polished; compacted 19->16; 0.777, 17, at 6: M0 += eps * MatMul(M0,M1), eps -0.03; polished; 0.772, 19, at 7: M1 += eps * MatScale(Norm(V2),MatSub(M1,M2)), eps -0.003; polished; 0.772, 19, at 7: M2 += eps * MatScale(Norm(V2),MatSub(M1,M2)), eps +0.003; polished | 6391 | 806 | 72 | 42 | 660 |
| 5 | 0.7991 | 0.794 | 0.782 | 23 | 0.794, 23, tap V0 <- M2 V0 at 5; M2 += eps * MatScale(Norm(V0),MatSub(M1,M2)) at end, eps +0.01; polished; 0.785, 22, at 5: M1 += eps * MatScale(Dot(V2,V2),MatSub(M1,M2)), eps +0.01; 0.781, 16, at 0: M0 += eps * MatScale(Dot(V1,V1),MatMul(M0,M1)), eps -0.03; polished; compacted 19->16; 0.781, 21, at 17: M0 += eps * MatScale(Norm(V2),MatSub(M1,M2)), eps +0.003; compacted 23->21 | 7602 | 990 | 78 | 42 | 1108 |
| 6 | 0.7991 | 0.794 | 0.782 | 23 | 0.794, 23, tap V0 <- M2 V0 at 5; M2 += eps * MatScale(Norm(V0),MatSub(M1,M2)) at end, eps +0.01; polished; 0.785, 23, tap V0 <- M2 V0 at 0; M2 += eps * MatScale(Dot(V0,V0),MatSub(M1,M2)) at end, eps +0.001; polished; 0.785, 22, at 5: M1 += eps * MatScale(Dot(V2,V2),MatSub(M1,M2)), eps +0.01; 0.781, 16, at 0: M0 += eps * MatScale(Dot(V1,V1),MatMul(M0,M1)), eps -0.03; polished; compacted 19->16 | 8163 | 1054 | 80 | 42 | 1566 |
| 7 | 0.7991 | 0.794 | 0.782 | 23 | 0.794, 23, tap V0 <- M2 V0 at 5; M2 += eps * MatScale(Norm(V0),MatSub(M1,M2)) at end, eps +0.01; polished; 0.785, 23, tap V0 <- M2 V0 at 0; M2 += eps * MatScale(Dot(V0,V0),MatSub(M1,M2)) at end, eps +0.001; polished; 0.785, 23, tap V0 <- M2 V0 at 1; M2 += eps * MatScale(Dot(V0,V0),MatSub(M1,M2)) at end, eps +0.001; polished; 0.785, 22, at 5: M1 += eps * MatScale(Dot(V2,V2),MatSub(M1,M2)), eps +0.01 | 8724 | 1118 | 82 | 42 | 2071 |
| 8 | stop: beam unchanged | | | | | 8724 | 1122 | 82 | 42 | 2587 |

```
S' = (((S + -0.064·(S)(P1)) + -0.613·((S + -0.064·(S)(P1))·k)⊗(P2·k)) + (tanh(v))⊗(P1·P2·k))
P1' = (P1 + -0.613·(P1·P2·k)⊗(P1·P2·k))
P2' = (P2 + 0.032·|P1·P2·k|·((P1 + -0.613·(P1·P2·k)⊗(P1·P2·k)) - P2))

Effective program (23 instructions):
  M3 = MatMul(M0, M1)
  s0 = -0.0640
  M3 = MatScale(s0, M3)
  M0 = MatAdd(M0, M3)
  V2 = MatVec(M0, V0)
  V0 = MatVec(M2, V0)
  M3 = Outer(V2, V0)
  V0 = MatVec(M1, V0)
  s0 = -0.6134
  M3 = MatScale(s0, M3)
  M0 = MatAdd(M0, M3)
  V2 = Tanh(V1)
  M3 = Outer(V2, V0)
  M0 = MatAdd(M0, M3)
  M3 = Outer(V0, V0)
  M3 = MatScale(s0, M3)
  M1 = MatAdd(M1, M3)
  s0 = Norm(V0)
  M3 = MatSub(M1, M2)
  M3 = MatScale(s0, M3)
  s0 = 0.0324
  M3 = MatScale(s0, M3)
  M2 = MatAdd(M2, M3)

structure: unclassified  [a=0.969 b=0.341 c=-0.548 g=-0.016, erase c/a=0.566, R²=0.6110, 1408 steps]

train acc 0.794 ±0.012
test regime collision3: acc 0.782  margin 0.153  ±0.005
test d16 T12 ow0.3: acc 0.907  margin 0.295  ±0.004
test d16 T12 ow0.0: acc 0.982  margin 0.327  ±0.002
test d16 T12 ow0.6: acc 0.873  margin 0.234  ±0.006
test d32 T24 ow0.3: acc 0.935  margin 0.359  ±0.004
test d8 T6 ow0.3: acc 0.828  margin 0.144  ±0.008
test d16 T64 K8 ow0.3: acc 0.902  margin 0.179  ±0.007
test d16 T128 K8 ow0.3: acc 0.845  margin 0.133  ±0.011


```
