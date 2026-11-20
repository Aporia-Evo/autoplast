# grow v2, arm B, task seed 4, beam 4, compaction True

| round | best train fit | best train acc | best test acc | len | beam (train acc, len, last step) | Rust evals | grad passes | seconds |
|---|---|---|---|---|---|---|---|---|
| 1 | 0.3663 | 0.373 | 0.385 | 2 | 0.373, 2, at 0: M0 += eps * Outer(V1,V0), eps +0.001; compacted 4->2; 0.000, 0, start | 62 | 61 | 6 |
| 2 | 0.6379 | 0.636 | 0.634 | 7 | 0.636, 7, at 0: V1 += eps * MatVec(M0,Normalize(V0)), eps -0.3; polished; 0.524, 4, at 0: M0 += eps * M0, eps -0.1; compacted 5->4; 0.524, 5, at 1: M1 += eps * M0, eps -0.1; 0.524, 5, at 2: M0 += eps * MatSub(M0,M1), eps -0.1; compacted 6->5 | 640 | 303 | 24 |
| 3 | 0.6532 | 0.652 | 0.646 | 13 | 0.652, 13, tap V2 <- M2 V2 at 1; M2 += eps * MatScale(Norm(V3),M2) at end, eps +0.01; 0.652, 13, tap V3 <- M2 V3 at 2; M2 += eps * MatScale(Norm(V3),M2) at end, eps +0.01; 0.646, 13, tap V1 <- M2 V1 at 5; M2 += eps * MatScale(Dot(V3,V3),M2) at end, eps +0.01; 0.643, 13, tap V0 <- M2 V0 at 0; M2 += eps * Outer(V0,VecScale(S0,V0)) at end, eps -0.01; polished | 4035 | 547 | 165 |
| 4 | 0.6561 | 0.655 | 0.648 | 17 | 0.655, 17, at 1: V1 += eps * MatVec(M0,V2), eps -0.01; 0.655, 17, at 2: V1 += eps * Tanh(V3), eps -0.01; 0.654, 15, at 0: V0 += eps * V0, eps +0.03; compacted 16->15; 0.654, 16, at 1: V2 += eps * V0, eps +0.03 | 7644 | 791 | 505 |
| 5 | 0.6566 | 0.656 | 0.647 | 20 | 0.656, 20, at 0: M0 += eps * Outer(V0,V0), eps -0.01; compacted 21->20; 0.656, 21, at 1: V0 += eps * MatVec(M1,V2), eps +0.3; 0.656, 21, at 0: M2 += eps * Outer(V0,V1), eps +0.01; 0.655, 17, at 1: V1 += eps * MatVec(M0,V2), eps -0.01 | 11530 | 975 | 973 |
| 6 | 0.6566 | 0.656 | 0.647 | 20 | 0.656, 20, at 0: M0 += eps * Outer(V0,V0), eps -0.01; compacted 21->20; 0.656, 20, at 0: M0 += eps * Outer(V0,V0), eps -0.01; compacted 21->20; 0.656, 21, at 1: V0 += eps * MatVec(M1,V2), eps +0.3; 0.656, 21, at 0: M2 += eps * Outer(V0,V1), eps +0.01 | 12850 | 1039 | 1453 |
| 7 | 0.6566 | 0.656 | 0.647 | 20 | 0.656, 20, at 0: M0 += eps * Outer(V0,V0), eps -0.01; compacted 21->20; 0.656, 21, at 1: V0 += eps * MatVec(M1,V2), eps +0.3; 0.656, 21, at 1: V2 += eps * V1, eps -0.003; compacted 24->21; 0.656, 21, at 0: M2 += eps * Outer(V0,V1), eps +0.01 | 13264 | 1103 | 1940 |
| 8 | 0.6566 | 0.656 | 0.647 | 20 | 0.656, 20, at 0: M0 += eps * Outer(V0,V0), eps -0.01; compacted 21->20; 0.656, 21, at 1: V0 += eps * MatVec(M1,V2), eps +0.3; 0.656, 21, at 1: V2 += eps * V1, eps -0.003; compacted 24->21; 0.656, 21, at 0: M2 += eps * Outer(V0,V1), eps +0.01 | 13806 | 1167 | 2419 |
| 9 | 0.6566 | 0.656 | 0.647 | 20 | 0.656, 20, at 0: M0 += eps * Outer(V0,V0), eps -0.01; compacted 21->20; 0.656, 21, at 1: V0 += eps * MatVec(M1,V2), eps +0.3; 0.656, 21, at 1: V2 += eps * V1, eps -0.003; compacted 24->21; 0.656, 21, at 0: M2 += eps * Outer(V0,V1), eps +0.01 | 14348 | 1231 | 2895 |
| 10 | 0.6566 | 0.656 | 0.647 | 20 | 0.656, 20, at 0: M0 += eps * Outer(V0,V0), eps -0.01; compacted 21->20; 0.656, 21, at 1: V0 += eps * MatVec(M1,V2), eps +0.3; 0.656, 21, at 1: V2 += eps * V1, eps -0.003; compacted 24->21; 0.656, 21, at 0: M2 += eps * Outer(V0,V1), eps +0.01 | 14890 | 1295 | 3376 |
| 11 | 0.6566 | 0.656 | 0.647 | 20 | 0.656, 20, at 0: M0 += eps * Outer(V0,V0), eps -0.01; compacted 21->20; 0.656, 21, at 1: V0 += eps * MatVec(M1,V2), eps +0.3; 0.656, 21, at 1: V2 += eps * V1, eps -0.003; compacted 24->21; 0.656, 21, at 0: M2 += eps * Outer(V0,V1), eps +0.01 | 15432 | 1359 | 3821 |
| 12 | 0.6566 | 0.656 | 0.647 | 20 | 0.656, 20, at 0: M0 += eps * Outer(V0,V0), eps -0.01; compacted 21->20; 0.656, 21, at 1: V0 += eps * MatVec(M1,V2), eps +0.3; 0.656, 21, at 1: V2 += eps * V1, eps -0.003; compacted 24->21; 0.656, 21, at 0: M2 += eps * Outer(V0,V1), eps +0.01 | 15974 | 1423 | 4269 |
| 13 | 0.6566 | 0.656 | 0.647 | 20 | 0.656, 20, at 0: M0 += eps * Outer(V0,V0), eps -0.01; compacted 21->20; 0.656, 21, at 1: V0 += eps * MatVec(M1,V2), eps +0.3; 0.656, 21, at 1: V2 += eps * V1, eps -0.003; compacted 24->21; 0.656, 21, at 0: M2 += eps * Outer(V0,V1), eps +0.01 | 16516 | 1487 | 4707 |
| 14 | 0.6566 | 0.656 | 0.647 | 20 | 0.656, 20, at 0: M0 += eps * Outer(V0,V0), eps -0.01; compacted 21->20; 0.656, 21, at 1: V0 += eps * MatVec(M1,V2), eps +0.3; 0.656, 21, at 1: V2 += eps * V1, eps -0.003; compacted 24->21; 0.656, 21, at 0: M2 += eps * Outer(V0,V1), eps +0.01 | 17058 | 1551 | 5157 |
| 15 | 0.6566 | 0.656 | 0.647 | 20 | 0.656, 20, at 0: M0 += eps * Outer(V0,V0), eps -0.01; compacted 21->20; 0.656, 21, at 1: V0 += eps * MatVec(M1,V2), eps +0.3; 0.656, 21, at 1: V2 += eps * V1, eps -0.003; compacted 24->21; 0.656, 21, at 0: M2 += eps * Outer(V0,V1), eps +0.01 | 17600 | 1615 | 5612 |
| 16 | 0.6566 | 0.656 | 0.647 | 20 | 0.656, 20, at 0: M0 += eps * Outer(V0,V0), eps -0.01; compacted 21->20; 0.656, 21, at 1: V0 += eps * MatVec(M1,V2), eps +0.3; 0.656, 21, at 1: V2 += eps * V1, eps -0.003; compacted 24->21; 0.656, 21, at 0: M2 += eps * Outer(V0,V1), eps +0.01 | 18142 | 1679 | 6072 |
| 17 | 0.6566 | 0.656 | 0.647 | 20 | 0.656, 20, at 0: M0 += eps * Outer(V0,V0), eps -0.01; compacted 21->20; 0.656, 21, at 1: V0 += eps * MatVec(M1,V2), eps +0.3; 0.656, 21, at 1: V2 += eps * V1, eps -0.003; compacted 24->21; 0.656, 21, at 0: M2 += eps * Outer(V0,V1), eps +0.01 | 18684 | 1743 | 6537 |
| 18 | 0.6566 | 0.656 | 0.647 | 20 | 0.656, 20, at 0: M0 += eps * Outer(V0,V0), eps -0.01; compacted 21->20; 0.656, 21, at 1: V0 += eps * MatVec(M1,V2), eps +0.3; 0.656, 21, at 1: V2 += eps * V1, eps -0.003; compacted 24->21; 0.656, 21, at 0: M2 += eps * Outer(V0,V1), eps +0.01 | 19226 | 1807 | 6985 |
| 19 | 0.6566 | 0.656 | 0.647 | 20 | 0.656, 20, at 0: M0 += eps * Outer(V0,V0), eps -0.01; compacted 21->20; 0.656, 21, at 1: V0 += eps * MatVec(M1,V2), eps +0.3; 0.656, 21, at 1: V2 += eps * V1, eps -0.003; compacted 24->21; 0.656, 21, at 0: M2 += eps * Outer(V0,V1), eps +0.01 | 19768 | 1871 | 7435 |
| 20 | 0.6566 | 0.656 | 0.647 | 20 | 0.656, 20, at 0: M0 += eps * Outer(V0,V0), eps -0.01; compacted 21->20; 0.656, 21, at 1: V0 += eps * MatVec(M1,V2), eps +0.3; 0.656, 21, at 1: V2 += eps * V1, eps -0.003; compacted 24->21; 0.656, 21, at 0: M2 += eps * Outer(V0,V1), eps +0.01 | 20310 | 1935 | 7881 |

```
S' = ((S + -0.010·(k)⊗(k)) + (((v + -0.010·(S + -0.010·(k)⊗(k))·norm(k)) + -0.352·P2·(S + -0.010·(k)⊗(k))·norm(k)))⊗(k))
P1' = 0.010·|-0.352·P2·(S + -0.010·(k)⊗(k))·norm(k)|·P2
P2' = (P2 + 0.010·|-0.352·P2·(S + -0.010·(k)⊗(k))·norm(k)|·P2)

Effective program (20 instructions):
  M1 = Outer(V0, V0)
  s0 = -0.0100
  M1 = MatScale(s0, M1)
  M0 = MatAdd(M0, M1)
  V2 = Normalize(V0)
  V3 = MatVec(M0, V2)
  V3 = VecScale(s0, V3)
  V1 = VecAdd(V1, V3)
  V3 = MatVec(M0, V2)
  V3 = MatVec(M2, V3)
  s0 = -0.3517
  V3 = VecScale(s0, V3)
  V1 = VecAdd(V1, V3)
  M1 = Outer(V1, V0)
  M0 = MatAdd(M0, M1)
  s0 = Norm(V3)
  M1 = MatScale(s0, M2)
  s1 = 0.0100
  M1 = MatScale(s1, M1)
  M2 = MatAdd(M2, M1)

structure: delta rule  [a=1.000 b=0.999 c=-0.407 g=0.003, erase c/a=0.407, R²=0.9987, 1408 steps]

train acc 0.656 ±0.014
test regime collision3: acc 0.647  margin 0.050  ±0.006
test d16 T12 ow0.3: acc 0.920  margin 0.241  ±0.004
test d16 T12 ow0.0: acc 0.921  margin 0.237  ±0.003
test d16 T12 ow0.6: acc 0.907  margin 0.219  ±0.006
test d32 T24 ow0.3: acc 0.983  margin 0.327  ±0.002
test d8 T6 ow0.3: acc 0.771  margin 0.100  ±0.009
test d16 T64 K8 ow0.3: acc 0.813  margin 0.139  ±0.009
test d16 T128 K8 ow0.3: acc 0.854  margin 0.208  ±0.011


```
