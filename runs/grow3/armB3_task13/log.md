# grow v3, arm B, task seed 13, beam 4, compaction, stability gate 100

| round | best train fit | best train acc | best test acc | len | beam (train acc, len, last step) | Rust evals | grad passes | gate evals | refused by gate | seconds |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | 0.4091 | 0.414 | 0.385 | 2 | 0.414, 2, at 0: M0 += eps * Outer(V1,V0), eps +0.001; compacted 4->2; 0.000, 0, start | 62 | 61 | 4 | 0 | 6 |
| 2 | 0.6542 | 0.652 | 0.635 | 6 | 0.652, 6, at 0: V1 += eps * MatVec(M0,V0), eps -0.3; polished; 0.652, 7, at 0: M0 += eps * Outer(MatVec(M0,V0),V0), eps -0.3; polished; 0.540, 4, at 0: M0 += eps * M0, eps -0.1; compacted 5->4; 0.434, 6, at 2: M0 += eps * MatScale(Dot(V1,V1),MatSub(M0,M1)), eps -0.03; compacted 8->6 | 477 | 303 | 18 | 5 | 24 |
| 3 | 0.7755 | 0.770 | 0.739 | 13 | 0.770, 13, tap V0 <- M1 V0 at 2; M1 += eps * Outer(VecScale(S0,V0),V0) at end, eps +0.3; polished; 0.675, 12, at 2: S0 += eps * SMul(Dot(V2,V2),Norm(V2)), eps -0.03; polished; 0.668, 13, tap V2 <- M1 V2 at 1; M1 += eps * MatScale(Norm(V2),M1) at end, eps +0.003; 0.668, 13, tap V2 <- M2 V2 at 1; M2 += eps * MatScale(Norm(V2),M1) at end, eps +0.003 | 3445 | 562 | 35 | 16 | 177 |
| 4 | 0.8028 | 0.796 | 0.774 | 17 | 0.796, 17, at 0: M0 += eps * MatMul(M0,M1), eps -0.03; polished; 0.796, 18, at 6: M0 += eps * MatScale(S0,MatMul(M0,M1)), eps +0.1; polished; 0.786, 16, at 6: M1 += eps * M2, eps +0.003; polished; 0.786, 17, at 0: M1 += eps * Transpose(M2), eps +0.003; polished | 6458 | 866 | 43 | 16 | 545 |
| 5 | 0.8063 | 0.800 | 0.773 | 23 | 0.800, 23, at 5: M1 += eps * MatScale(Norm(V2),MatSub(M1,M2)), eps -0.003; 0.799, 24, tap V0 <- M2 V0 at 0; M2 += eps * MatScale(Norm(V2),MatSub(M1,M2)) at end, eps +0.01; 0.796, 17, at 0: M0 += eps * MatMul(M0,M1), eps -0.03; polished; 0.796, 18, at 6: M0 += eps * MatScale(S0,MatMul(M0,M1)), eps +0.1; polished | 7774 | 1020 | 45 | 16 | 963 |
| 6 | 0.8063 | 0.800 | 0.773 | 23 | 0.800, 23, at 5: M1 += eps * MatScale(Norm(V2),MatSub(M1,M2)), eps -0.003; 0.800, 23, at 17: M1 += eps * MatScale(Norm(V2),MatSub(M1,M2)), eps -0.003; 0.799, 24, tap V0 <- M2 V0 at 0; M2 += eps * MatScale(Norm(V2),MatSub(M1,M2)) at end, eps +0.01; 0.799, 24, tap V0 <- M2 V0 at 1; M2 += eps * MatScale(Norm(V2),MatSub(M1,M2)) at end, eps +0.01 | 8530 | 1174 | 47 | 16 | 1448 |
| 7 | stop: beam unchanged | | | | | 8530 | 1178 | 47 | 16 | 1977 |

```
S' = (((S + -0.047·(S)(P1)) + -0.570·((S + -0.047·(S)(P1))·k)⊗(k)) + (v)⊗((P1 + -0.003·|(S + -0.047·(S)(P1))·k|·(P1 - P2))·k))
P1' = ((P1 + -0.003·|(S + -0.047·(S)(P1))·k|·(P1 - P2)) + 1.059·(-0.570·(P1 + -0.003·|(S + -0.047·(S)(P1))·k|·(P1 - P2))·k)⊗((P1 + -0.003·|(S + -0.047·(S)(P1))·k|·(P1 - P2))·k))

Effective program (23 instructions):
  M3 = MatMul(M0, M1)
  s0 = -0.0466
  M3 = MatScale(s0, M3)
  M0 = MatAdd(M0, M3)
  V2 = MatVec(M0, V0)
  s0 = Norm(V2)
  M3 = MatSub(M1, M2)
  M3 = MatScale(s0, M3)
  s0 = -0.0030
  M3 = MatScale(s0, M3)
  M1 = MatAdd(M1, M3)
  M3 = Outer(V2, V0)
  V0 = MatVec(M1, V0)
  s0 = -0.5695
  M3 = MatScale(s0, M3)
  M0 = MatAdd(M0, M3)
  M3 = Outer(V1, V0)
  M0 = MatAdd(M0, M3)
  V1 = VecScale(s0, V0)
  M3 = Outer(V1, V0)
  s1 = 1.0589
  M3 = MatScale(s1, M3)
  M1 = MatAdd(M1, M3)

structure: unclassified  [a=0.978 b=0.379 c=-0.555 g=-0.075, erase c/a=0.568, R²=0.6458, 1408 steps]

train acc 0.800 ±0.011
test regime collision3: acc 0.773  margin 0.153  ±0.005
test d16 T12 ow0.3: acc 0.915  margin 0.295  ±0.004
test d16 T12 ow0.0: acc 0.983  margin 0.324  ±0.002
test d16 T12 ow0.6: acc 0.873  margin 0.236  ±0.006
test d32 T24 ow0.3: acc 0.951  margin 0.368  ±0.003
test d8 T6 ow0.3: acc 0.819  margin 0.142  ±0.008
test d16 T64 K8 ow0.3: acc 0.899  margin 0.209  ±0.007
test d16 T128 K8 ow0.3: acc 0.907  margin 0.210  ±0.009


```
