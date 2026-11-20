# grow v3, arm B, task seed 16, beam 4, compaction, stability gate 100

| round | best train fit | best train acc | best test acc | len | beam (train acc, len, last step) | Rust evals | grad passes | gate evals | refused by gate | seconds |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | 0.3849 | 0.391 | 0.385 | 2 | 0.391, 2, at 0: M0 += eps * Outer(V1,V0), eps +0.001; compacted 4->2; 0.000, 0, start | 62 | 61 | 4 | 0 | 7 |
| 2 | 0.6558 | 0.653 | 0.641 | 7 | 0.653, 7, at 0: V1 += eps * MatVec(M0,Tanh(V0)), eps -1; polished; 0.509, 7, at 0: M0 += eps * MatScale(Dot(V0,V0),M0), eps -0.1; 0.422, 6, at 2: M0 += eps * MatSub(M0,M1), eps -0.03; polished; 0.399, 6, at 0: V0 += eps * Hadamard(V0,V1), eps +0.3 | 453 | 303 | 18 | 8 | 25 |
| 3 | 0.6563 | 0.654 | 0.641 | 11 | 0.654, 11, tap V0 <- M1 V0 at 0; M1 += eps * Outer(Tanh(V0),V0) at end, eps +0.003; compacted 13->11; 0.654, 11, tap V0 <- M2 V0 at 0; M2 += eps * Outer(Tanh(V0),V0) at end, eps +0.003; compacted 13->11; 0.653, 7, at 0: V1 += eps * MatVec(M0,Tanh(V0)), eps -1; polished; 0.649, 6, at 0: V1 += eps * MatVec(M0,V0), eps -0.3; polished; compacted 10->6 | 3565 | 487 | 52 | 24 | 212 |
| 4 | 0.6653 | 0.663 | 0.645 | 13 | 0.663, 13, tap V1 <- M1 V1 at 4; M1 += eps * MatScale(Dot(V2,V2),Transpose(M1)) at end, eps +0.01; 0.661, 12, tap V2 <- M1 V2 at 1; M1 += eps * MatScale(Dot(V2,V2),M1) at end, eps +0.01; 0.660, 13, tap V1 <- M2 V1 at 4; M2 += eps * MatScale(Norm(V2),Transpose(M1)) at end, eps +0.01; 0.656, 16, at 0: M1 += eps * Outer(Tanh(V0),V0), eps +0.003 | 6708 | 731 | 86 | 54 | 464 |
| 5 | 0.6712 | 0.669 | 0.645 | 15 | 0.669, 15, at 0: M0 += eps * Outer(V1,V0), eps +1; compacted 17->15; 0.669, 16, at 0: M2 += eps * M1, eps +0.003; 0.669, 18, at 0: M2 += eps * MatScale(Dot(V0,V0),M1), eps +0.003; 0.668, 14, at 1: V2 += eps * V1, eps -1; compacted 16->14 | 9697 | 990 | 95 | 54 | 814 |
| 6 | 0.6712 | 0.669 | 0.645 | 15 | 0.669, 15, at 0: M0 += eps * Outer(V1,V0), eps +1; compacted 17->15; 0.669, 16, at 0: M2 += eps * M1, eps +0.003; 0.669, 16, at 0: V0 += eps * V0, eps +0.001; compacted 19->16; 0.669, 18, at 0: M2 += eps * MatScale(Dot(V0,V0),M1), eps +0.003 | 12300 | 1054 | 105 | 56 | 1192 |
| 7 | 0.6712 | 0.669 | 0.645 | 15 | 0.669, 15, at 0: M0 += eps * Outer(V1,V0), eps +1; compacted 17->15; 0.669, 16, at 0: M2 += eps * M1, eps +0.003; 0.669, 16, at 0: V0 += eps * V0, eps +0.001; compacted 19->16; 0.669, 18, at 0: M2 += eps * MatScale(Dot(V0,V0),M1), eps +0.003 | 15047 | 1118 | 114 | 57 | 1604 |
| 8 | 0.6712 | 0.669 | 0.645 | 15 | 0.669, 15, at 0: M0 += eps * Outer(V1,V0), eps +1; compacted 17->15; 0.669, 16, at 0: M2 += eps * M1, eps +0.003; 0.669, 16, at 0: V0 += eps * V0, eps +0.001; compacted 19->16; 0.669, 18, at 0: M2 += eps * MatScale(Dot(V0,V0),M1), eps +0.003 | 17794 | 1182 | 123 | 58 | 1992 |
| 9 | stop: best not improved for 3 rounds | | | | | 17794 | 1182 | 123 | 58 | 1992 |

```
S' = ((S + (v)⊗(k)) + (P2·(v + -0.385·(S + (v)⊗(k))·k))⊗(k))
P2' = (P2 + 0.010·|-0.385·(S + (v)⊗(k))·k|·(P1)ᵀ)

Effective program (15 instructions):
  M3 = Outer(V1, V0)
  M0 = MatAdd(M0, M3)
  V2 = MatVec(M0, V0)
  s0 = -0.3850
  V2 = VecScale(s0, V2)
  V1 = VecAdd(V1, V2)
  V1 = MatVec(M2, V1)
  M3 = Outer(V1, V0)
  M0 = MatAdd(M0, M3)
  s0 = Norm(V2)
  M3 = Transpose(M1)
  M3 = MatScale(s0, M3)
  s0 = 0.0100
  M3 = MatScale(s0, M3)
  M2 = MatAdd(M2, M3)

structure: delta rule  [a=1.000 b=1.729 c=-0.477 g=0.001, erase c/a=0.477, R²=0.9942, 1408 steps]

train acc 0.669 ±0.014
test regime collision3: acc 0.645  margin 0.053  ±0.006
test d16 T12 ow0.3: acc 0.921  margin 0.247  ±0.004
test d16 T12 ow0.0: acc 0.912  margin 0.236  ±0.004
test d16 T12 ow0.6: acc 0.923  margin 0.234  ±0.005
test d32 T24 ow0.3: acc 0.985  margin 0.335  ±0.002
test d8 T6 ow0.3: acc 0.776  margin 0.103  ±0.009
test d16 T64 K8 ow0.3: acc 0.851  margin 0.185  ±0.008
test d16 T128 K8 ow0.3: acc 0.858  margin 0.228  ±0.011


```
