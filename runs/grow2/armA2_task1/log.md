# grow v2, arm A, task seed 1, beam 4, compaction True

| round | best train fit | best train acc | best test acc | len | beam (train acc, len, last step) | Rust evals | grad passes | seconds |
|---|---|---|---|---|---|---|---|---|
| 1 | 0.3556 | 0.362 | 0.385 | 2 | 0.362, 2, at 0: M0 += eps * Outer(V1,V0), eps +0.001; compacted 4->2; 0.000, 0, start | 62 | 61 | 6 |
| 2 | 0.6061 | 0.605 | 0.625 | 6 | 0.605, 6, at 0: V1 += eps * MatVec(M0,V0), eps -0.3; polished; 0.605, 7, at 0: M0 += eps * Outer(MatVec(M0,V0),V0), eps -0.3; polished; 0.605, 7, at 1: M1 += eps * Outer(MatVec(M0,V0),V0), eps -0.3; polished; 0.500, 4, at 0: M0 += eps * M0, eps -0.1; compacted 5->4 | 443 | 303 | 19 |
| 3 | 0.6225 | 0.622 | 0.653 | 9 | 0.622, 9, at 2: S0 += eps * Dot(V2,V2), eps -0.3; compacted 10->9; 0.620, 11, at 4: V1 += eps * VecScale(Dot(V1,V2),V2), eps +3; 0.618, 12, at 3: S0 += eps * SMul(S0,Dot(V2,V2)), eps +0.3; 0.617, 11, at 3: V2 += eps * VecScale(Dot(V2,V2),V2), eps +3 | 3602 | 547 | 105 |
| 4 | 0.6289 | 0.628 | 0.653 | 17 | 0.628, 17, at 10: M0 += eps * MatScale(Recip(S0),M0), eps -0.01; 0.628, 17, at 11: M1 += eps * MatScale(Recip(S0),M0), eps -0.01; 0.627, 13, at 1: M0 += eps * M0, eps +0.03; compacted 14->13; 0.626, 13, at 1: M0 += eps * MatSub(M0,M1), eps -0.003 | 7273 | 791 | 287 |
| 5 | 0.6409 | 0.640 | 0.000 | 21 | 0.640, 21, at 14: S2 += eps * SMul(S1,S1), eps -0.001; polished; 0.640, 22, at 10: M0 += eps * MatScale(Recip(S2),M0), eps -0.001; 0.638, 22, at 11: M1 += eps * MatScale(Recip(S2),M0), eps -0.001; 0.631, 19, at 0: V0 += eps * V0, eps -0.01; compacted 20->19 | 10117 | 1035 | 541 |
| 6 | 0.6409 | 0.640 | 0.000 | 21 | 0.640, 21, at 14: S2 += eps * SMul(S1,S1), eps -0.001; polished; 0.640, 22, at 10: M0 += eps * MatScale(Recip(S2),M0), eps -0.001; 0.639, 17, at 14: M0 += eps * MatScale(Recip(S2),M0), eps -0.001; polished; compacted 24->17; 0.638, 22, at 11: M1 += eps * MatScale(Recip(S2),M0), eps -0.001 | 10779 | 1099 | 868 |
| 7 | 0.6497 | 0.649 | 0.667 | 23 | 0.649, 23, at 11: M0 += eps * MatScale(Recip(S0),MatSub(M0,M2)), eps +0.1; polished; 0.646, 22, at 14: M2 += eps * MatScale(Recip(S0),M0), eps +0.1; polished; 0.644, 22, at 11: M0 += eps * Outer(V1,VecScale(S0,V0)), eps -0.001; 0.641, 21, at 4: S1 += eps * Recip(S1), eps +0.001; polished | 11325 | 1343 | 1196 |
| 8 | stop: beam unchanged | | | | | 11325 | 1347 | 1578 |

```
S' = …
P1' = (v)⊗(k)
P2' = -0.002·1/(0.139·-0.336·<S·k, S·k>)·((S + (-0.336 + 0.139·-0.336·<S·k, S·k>)·(S·k)⊗(k)) + 0.214·1/(1/(0.139·-0.336·<S·k, S·k>))·((S + (-0.336 + 0.139·-0.336·<S·k, S·k>)·(S·k)⊗(k)) - P2))

Effective program (23 instructions):
  V2 = MatVec(M0, V0)
  M1 = Outer(V2, V0)
  s0 = -0.3360
  s1 = Dot(V2, V2)
  s2 = SMul(s0, s1)
  s3 = 0.1390
  s2 = SMul(s3, s2)
  s0 = SAdd(s0, s2)
  M1 = MatScale(s0, M1)
  M0 = MatAdd(M0, M1)
  s0 = Recip(s2)
  s1 = Recip(s0)
  M1 = MatSub(M0, M2)
  M3 = MatScale(s1, M1)
  s2 = 0.2143
  M3 = MatScale(s2, M3)
  M0 = MatAdd(M0, M3)
  M2 = MatScale(s0, M0)
  s1 = -0.0022
  M2 = MatScale(s1, M2)
  M0 = MatAdd(M0, M2)
  M1 = Outer(V1, V0)
  M0 = MatAdd(M0, M1)

structure: unclassified  [a=1.029 b=1.001 c=-0.502 g=0.015, erase c/a=0.488, R²=0.9141, 1408 steps]

train acc 0.649 ±0.014
test regime collision3: acc 0.667  margin 0.056  ±0.006
test d16 T12 ow0.3: acc 0.922  margin 0.226  ±0.004
test d16 T12 ow0.0: acc 0.918  margin 0.221  ±0.004
test d16 T12 ow0.6: acc 0.000  margin 0.000  ±0.000
test d32 T24 ow0.3: acc 0.951  margin 0.274  ±0.003
test d8 T6 ow0.3: acc 0.770  margin 0.101  ±0.009
test d16 T64 K8 ow0.3: acc 0.754  margin 0.091  ±0.010
test d16 T128 K8 ow0.3: acc 0.709  margin 0.079  ±0.014


```
