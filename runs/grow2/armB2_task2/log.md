# grow v2, arm B, task seed 2, beam 4, compaction True

| round | best train fit | best train acc | best test acc | len | beam (train acc, len, last step) | Rust evals | grad passes | seconds |
|---|---|---|---|---|---|---|---|---|
| 1 | 0.3564 | 0.363 | 0.385 | 2 | 0.363, 2, at 0: M0 += eps * Outer(V1,V0), eps +0.001; compacted 4->2; 0.000, 0, start | 62 | 61 | 7 |
| 2 | 0.6353 | 0.634 | 0.633 | 7 | 0.634, 7, at 0: V1 += eps * MatVec(M0,Normalize(V0)), eps -0.3; polished; 0.513, 7, tap V1 <- M2 V1 at 0; M2 += eps * MatSub(M1,M2) at end, eps -0.1; 0.512, 8, at 0: M0 += eps * MatScale(Dot(V1,V1),MatSub(M0,M1)), eps -0.1; 0.511, 5, tap V0 <- M2 V0 at 0; M2 += eps * M2 at end, eps +0.1; compacted 6->5 | 605 | 303 | 24 |
| 3 | 0.6535 | 0.652 | 0.647 | 13 | 0.652, 13, tap V2 <- M2 V2 at 1; M2 += eps * MatScale(Dot(V3,V3),M2) at end, eps +0.03; 0.652, 13, tap V3 <- M2 V3 at 2; M2 += eps * MatScale(Dot(V3,V3),M2) at end, eps +0.03; 0.651, 13, tap V1 <- M2 V1 at 5; M2 += eps * MatScale(Norm(V3),M2) at end, eps +0.01; 0.641, 7, tap V0 <- M2 V0 at 0; M2 += eps * Outer(V2,V0) at end, eps +0.001; polished; compacted 12->7 | 4220 | 547 | 210 |
| 4 | 0.6548 | 0.654 | 0.648 | 17 | 0.654, 17, at 0: M2 += eps * Outer(V0,V0), eps -0.003; 0.654, 18, at 12: M1 += eps * Outer(V0,VecScale(S1,V0)), eps -0.1; 0.653, 17, at 1: V0 += eps * Hadamard(V0,V2), eps +0.3; 0.653, 18, at 0: V1 += eps * MatVec(M0,VecAdd(V0,V1)), eps -0.01 | 7751 | 791 | 572 |
| 5 | 0.6582 | 0.657 | 0.625 | 18 | 0.657, 18, at 2: V3 += eps * VecScale(Dot(V0,V3),V0), eps -1; compacted 22->18; 0.656, 21, at 1: V1 += eps * MatVec(M0,V2), eps -0.01; 0.656, 22, at 2: V0 += eps * VecScale(Dot(V0,V3),V0), eps -0.3; 0.655, 20, at 1: V2 += eps * V0, eps +0.03 | 11489 | 1035 | 1065 |
