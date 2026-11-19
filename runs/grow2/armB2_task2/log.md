# grow v2, arm B, task seed 2, beam 4, compaction True

| round | best train fit | best train acc | best test acc | len | beam (train acc, len, last step) | Rust evals | grad passes | seconds |
|---|---|---|---|---|---|---|---|---|
| 1 | 0.3564 | 0.363 | 0.385 | 2 | 0.363, 2, at 0: M0 += eps * Outer(V1,V0), eps +0.001; compacted 4->2; 0.000, 0, start | 62 | 61 | 7 |
| 2 | 0.6353 | 0.634 | 0.633 | 7 | 0.634, 7, at 0: V1 += eps * MatVec(M0,Normalize(V0)), eps -0.3; polished; 0.513, 7, tap V1 <- M2 V1 at 0; M2 += eps * MatSub(M1,M2) at end, eps -0.1; 0.512, 8, at 0: M0 += eps * MatScale(Dot(V1,V1),MatSub(M0,M1)), eps -0.1; 0.511, 5, tap V0 <- M2 V0 at 0; M2 += eps * M2 at end, eps +0.1; compacted 6->5 | 605 | 303 | 24 |
