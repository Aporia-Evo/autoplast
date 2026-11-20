# grow v2, arm B, task seed 2, beam 4, compaction True

| round | best train fit | best train acc | best test acc | len | beam (train acc, len, last step) | Rust evals | grad passes | seconds |
|---|---|---|---|---|---|---|---|---|
| 1 | 0.3564 | 0.363 | 0.385 | 2 | 0.363, 2, at 0: M0 += eps * Outer(V1,V0), eps +0.001; compacted 4->2; 0.000, 0, start | 62 | 61 | 6 |
| 2 | 0.6353 | 0.634 | 0.633 | 7 | 0.634, 7, at 0: V1 += eps * MatVec(M0,Normalize(V0)), eps -0.3; polished; 0.513, 7, tap V1 <- M2 V1 at 0; M2 += eps * MatSub(M1,M2) at end, eps -0.1; 0.512, 8, at 0: M0 += eps * MatScale(Dot(V1,V1),MatSub(M0,M1)), eps -0.1; 0.511, 5, tap V0 <- M2 V0 at 0; M2 += eps * M2 at end, eps +0.1; compacted 6->5 | 605 | 303 | 30 |
| 3 | 0.6535 | 0.652 | 0.647 | 13 | 0.652, 13, tap V2 <- M2 V2 at 1; M2 += eps * MatScale(Dot(V3,V3),M2) at end, eps +0.03; 0.652, 13, tap V3 <- M2 V3 at 2; M2 += eps * MatScale(Dot(V3,V3),M2) at end, eps +0.03; 0.651, 13, tap V1 <- M2 V1 at 5; M2 += eps * MatScale(Norm(V3),M2) at end, eps +0.01; 0.641, 7, tap V0 <- M2 V0 at 0; M2 += eps * Outer(V2,V0) at end, eps +0.001; polished; compacted 12->7 | 4220 | 547 | 226 |
| 4 | 0.6548 | 0.654 | 0.648 | 17 | 0.654, 17, at 0: M2 += eps * Outer(V0,V0), eps -0.003; 0.654, 18, at 12: M1 += eps * Outer(V0,VecScale(S1,V0)), eps -0.1; 0.653, 17, at 1: V0 += eps * Hadamard(V0,V2), eps +0.3; 0.653, 18, at 0: V1 += eps * MatVec(M0,VecAdd(V0,V1)), eps -0.01 | 7751 | 791 | 574 |
| 5 | 0.6582 | 0.657 | 0.625 | 18 | 0.657, 18, at 2: V3 += eps * VecScale(Dot(V0,V3),V0), eps -1; compacted 22->18; 0.656, 21, at 1: V1 += eps * MatVec(M0,V2), eps -0.01; 0.656, 22, at 2: V0 += eps * VecScale(Dot(V0,V3),V0), eps -0.3; 0.655, 20, at 1: V2 += eps * V0, eps +0.03 | 11489 | 1035 | 1074 |
| 6 | 0.6612 | 0.661 | 0.624 | 21 | 0.661, 21, at 2: V2 += eps * V1, eps -0.1; 0.659, 22, at 1: V0 += eps * Hadamard(V0,V2), eps +0.01; 0.659, 22, at 1: V0 += eps * MatVec(M2,Hadamard(V0,V2)), eps +0.01; compacted 23->22; 0.659, 22, at 2: V3 += eps * MatVec(M0,V1), eps +0.1 | 13416 | 1279 | 1728 |
| 7 | 0.6618 | 0.661 | 0.623 | 24 | 0.661, 24, at 0: V1 += eps * V0, eps +0.01; 0.661, 21, at 2: V2 += eps * V1, eps -0.1; 0.661, 21, at 1: V2 += eps * V0, eps +0.003; compacted 24->21; 0.661, 21, at 0: V0 += eps * V0, eps +0.001; compacted 24->21 | 14067 | 1463 | 2483 |
| 8 | 0.6618 | 0.661 | 0.623 | 24 | 0.661, 24, at 0: V1 += eps * V0, eps +0.01; 0.661, 24, at 1: V1 += eps * V0, eps +0.01; 0.661, 21, at 2: V2 += eps * V1, eps -0.1; 0.661, 21, at 1: V2 += eps * V0, eps +0.003; compacted 24->21 | 15408 | 1587 | 3247 |
| 9 | 0.6618 | 0.661 | 0.623 | 24 | 0.661, 24, at 0: V1 += eps * V0, eps +0.01; 0.661, 24, at 1: V1 += eps * V0, eps +0.01; 0.661, 24, at 1: V1 += eps * V2, eps +0.01; 0.661, 21, at 2: V2 += eps * V1, eps -0.1 | 16240 | 1651 | 4021 |
| 10 | 0.6618 | 0.661 | 0.623 | 24 | 0.661, 24, at 0: V1 += eps * V0, eps +0.01; 0.661, 24, at 1: V1 += eps * V0, eps +0.01; 0.661, 24, at 1: V1 += eps * V2, eps +0.01; 0.661, 24, at 2: V1 += eps * V0, eps +0.01 | 16672 | 1715 | 4826 |
| 11 | stop: beam unchanged | | | | | 16672 | 1719 | 5659 |

```
S' = (S + (P2·((v + 0.010·k) + -0.349·S·(norm(k) + -0.100·(v + 0.010·k))))⊗((k + ((k ⊙ norm(k)) - <k, (k ⊙ norm(k))>·k))))
P1' = 0.010·|-0.349·S·(norm(k) + -0.100·(v + 0.010·k))|·P2
P2' = (P2 + 0.010·|-0.349·S·(norm(k) + -0.100·(v + 0.010·k))|·P2)

Effective program (24 instructions):
  s0 = 0.0100
  V2 = VecScale(s0, V0)
  V1 = VecAdd(V1, V2)
  V2 = Normalize(V0)
  V3 = Hadamard(V0, V2)
  s0 = -0.1000
  V4 = VecScale(s0, V1)
  V2 = VecAdd(V2, V4)
  s0 = Dot(V0, V3)
  V4 = VecScale(s0, V0)
  V3 = VecSub(V3, V4)
  V0 = VecAdd(V0, V3)
  V3 = MatVec(M0, V2)
  s0 = -0.3491
  V3 = VecScale(s0, V3)
  V1 = VecAdd(V1, V3)
  V1 = MatVec(M2, V1)
  M1 = Outer(V1, V0)
  M0 = MatAdd(M0, M1)
  s0 = Norm(V3)
  M1 = MatScale(s0, M2)
  s1 = 0.0100
  M1 = MatScale(s1, M1)
  M2 = MatAdd(M2, M1)

structure: unclassified  [a=0.993 b=1.104 c=-0.392 g=0.022, erase c/a=0.395, R²=0.8697, 1408 steps]

train acc 0.661 ±0.014
test regime collision3: acc 0.623  margin 0.034  ±0.006
test d16 T12 ow0.3: acc 0.905  margin 0.226  ±0.004
test d16 T12 ow0.0: acc 0.890  margin 0.215  ±0.004
test d16 T12 ow0.6: acc 0.885  margin 0.202  ±0.006
test d32 T24 ow0.3: acc 0.977  margin 0.314  ±0.002
test d8 T6 ow0.3: acc 0.715  margin 0.075  ±0.009
test d16 T64 K8 ow0.3: acc 0.795  margin 0.131  ±0.009
test d16 T128 K8 ow0.3: acc 0.834  margin 0.191  ±0.012


```
