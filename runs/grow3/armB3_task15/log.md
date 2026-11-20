# grow v3, arm B, task seed 15, beam 4, compaction, stability gate 100

| round | best train fit | best train acc | best test acc | len | beam (train acc, len, last step) | Rust evals | grad passes | gate evals | refused by gate | seconds |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | 0.3914 | 0.397 | 0.385 | 2 | 0.397, 2, at 0: M0 += eps * Outer(V1,V0), eps +0.001; compacted 4->2; 0.000, 0, start | 62 | 61 | 4 | 0 | 7 |
| 2 | 0.6626 | 0.660 | 0.639 | 7 | 0.660, 7, at 0: M0 += eps * Outer(MatVec(M0,V0),V0), eps -1; polished; 0.657, 7, at 0: V1 += eps * MatVec(M0,Tanh(V0)), eps -1; polished; 0.544, 7, at 0: M0 += eps * MatScale(Norm(V0),M0), eps -0.1; 0.412, 7, at 0: V0 += eps * VecScale(Dot(V0,V1),V0), eps +0.3 | 456 | 318 | 18 | 8 | 26 |
| 3 | 0.7630 | 0.758 | 0.735 | 13 | 0.758, 13, tap V0 <- M1 V0 at 2; M1 += eps * Outer(Tanh(V0),V0) at end, eps -0.3; polished; 0.758, 13, tap V0 <- M2 V0 at 2; M2 += eps * Outer(Tanh(V0),V0) at end, eps -0.3; polished; 0.661, 13, tap V1 <- M1 V1 at 0; M1 += eps * Outer(Normalize(V1),V1) at end, eps -0.03; polished; 0.660, 7, at 0: M0 += eps * Outer(MatVec(M0,V0),V0), eps -1; polished | 3743 | 502 | 44 | 28 | 243 |
| 4 | 0.7988 | 0.793 | 0.777 | 17 | 0.793, 17, at 1: M0 += eps * MatScale(Dot(V0,V0),MatMul(M0,M1)), eps -0.03; polished; compacted 19->17; 0.791, 17, at 0: M0 += eps * MatMul(M0,M1), eps -0.03; polished; 0.773, 18, at 13: M1 += eps * MatScale(Recip(S0),MatSub(M1,M2)), eps +0.003; compacted 19->18; 0.773, 18, at 13: M2 += eps * MatScale(Recip(S0),MatSub(M1,M2)), eps -0.003; compacted 19->18 | 5877 | 746 | 54 | 28 | 549 |
| 5 | 0.8024 | 0.797 | 0.778 | 23 | 0.797, 23, tap V0 <- M2 V0 at 0; M2 += eps * MatScale(Norm(V2),MatSub(M1,M2)) at end, eps +0.001; polished; compacted 24->23; 0.795, 23, at 13: M1 += eps * MatScale(Dot(V1,V1),MatSub(M1,M2)), eps +0.01; 0.793, 17, at 1: M0 += eps * MatScale(Dot(V0,V0),MatMul(M0,M1)), eps -0.03; polished; compacted 19->17; 0.792, 22, at 4: M0 += eps * MatScale(S0,MatSub(M1,M2)), eps -0.001 | 7605 | 930 | 59 | 28 | 974 |
| 6 | 0.8024 | 0.797 | 0.778 | 23 | 0.797, 23, tap V0 <- M2 V0 at 0; M2 += eps * MatScale(Norm(V2),MatSub(M1,M2)) at end, eps +0.001; polished; compacted 24->23; 0.795, 23, at 13: M1 += eps * MatScale(Dot(V1,V1),MatSub(M1,M2)), eps +0.01; 0.793, 17, at 1: M0 += eps * MatScale(Dot(V0,V0),MatMul(M0,M1)), eps -0.03; polished; compacted 19->17; 0.793, 22, at 13: M1 += eps * MatScale(Dot(V0,V1),MatSub(M1,M2)), eps +0.003; polished; compacted 23->22 | 8148 | 994 | 62 | 28 | 1495 |
| 7 | stop: beam unchanged | | | | | 8628 | 998 | 62 | 28 | 2033 |

```
S' = (((S + -0.056·(S)(P1)) + -0.628·((S + -0.056·(S)(P1))·P2·k)⊗(P2·k)) + (v)⊗(P1·P2·k))
P1' = (P1 + -0.628·(tanh(P1·P2·k))⊗(P1·P2·k))
P2' = (P2 + 0.016·|(S + -0.056·(S)(P1))·P2·k|·((P1 + -0.628·(tanh(P1·P2·k))⊗(P1·P2·k)) - P2))

Effective program (23 instructions):
  V0 = MatVec(M2, V0)
  M3 = MatMul(M0, M1)
  s0 = -0.0562
  M3 = MatScale(s0, M3)
  M0 = MatAdd(M0, M3)
  V2 = MatVec(M0, V0)
  M3 = Outer(V2, V0)
  V0 = MatVec(M1, V0)
  s0 = -0.6275
  M3 = MatScale(s0, M3)
  M0 = MatAdd(M0, M3)
  M3 = Outer(V1, V0)
  M0 = MatAdd(M0, M3)
  V1 = Tanh(V0)
  M3 = Outer(V1, V0)
  M3 = MatScale(s0, M3)
  M1 = MatAdd(M1, M3)
  s0 = Norm(V2)
  M3 = MatSub(M1, M2)
  M3 = MatScale(s0, M3)
  s0 = 0.0156
  M3 = MatScale(s0, M3)
  M2 = MatAdd(M2, M3)

structure: unclassified  [a=0.972 b=0.361 c=-0.575 g=-0.034, erase c/a=0.592, R²=0.6218, 1408 steps]

train acc 0.797 ±0.012
test regime collision3: acc 0.778  margin 0.152  ±0.005
test d16 T12 ow0.3: acc 0.935  margin 0.305  ±0.004
test d16 T12 ow0.0: acc 0.979  margin 0.323  ±0.002
test d16 T12 ow0.6: acc 0.911  margin 0.252  ±0.005
test d32 T24 ow0.3: acc 0.963  margin 0.373  ±0.003
test d8 T6 ow0.3: acc 0.855  margin 0.154  ±0.007
test d16 T64 K8 ow0.3: acc 0.882  margin 0.168  ±0.007
test d16 T128 K8 ow0.3: acc 0.808  margin 0.115  ±0.012


```
