# grow v2, arm B, task seed 5, beam 4, compaction True

| round | best train fit | best train acc | best test acc | len | beam (train acc, len, last step) | Rust evals | grad passes | seconds |
|---|---|---|---|---|---|---|---|---|
| 1 | 0.3848 | 0.390 | 0.385 | 2 | 0.390, 2, at 0: M0 += eps * Outer(V1,V0), eps +0.001; compacted 4->2; 0.000, 0, start | 62 | 61 | 6 |
| 2 | 0.6334 | 0.631 | 0.633 | 6 | 0.631, 6, at 0: V1 += eps * MatVec(M0,V0), eps -0.3; polished; 0.525, 6, at 0: M0 += eps * MatSub(M0,M1), eps -0.1; 0.525, 7, tap V1 <- M2 V1 at 0; M2 += eps * MatSub(M1,M2) at end, eps -0.1; 0.523, 4, at 0: M0 += eps * M0, eps -0.1; compacted 5->4 | 634 | 303 | 29 |
| 3 | 0.6566 | 0.655 | 0.642 | 9 | 0.655, 9, at 3: V0 += eps * VecScale(Dot(V1,V2),V0), eps +1; compacted 11->9; 0.651, 12, tap V2 <- M2 V2 at 1; M2 += eps * MatScale(Norm(V2),M2) at end, eps +0.03; 0.649, 12, tap V1 <- M2 V1 at 4; M2 += eps * MatScale(Norm(V2),M2) at end, eps +0.03; 0.644, 11, tap V0 <- M2 V0 at 1; M2 += eps * Outer(V0,V0) at end, eps -0.003; polished | 4286 | 547 | 200 |
