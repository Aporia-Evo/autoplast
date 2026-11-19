# grow v2, arm B, task seed 4, beam 4, compaction True

| round | best train fit | best train acc | best test acc | len | beam (train acc, len, last step) | Rust evals | grad passes | seconds |
|---|---|---|---|---|---|---|---|---|
| 1 | 0.3663 | 0.373 | 0.385 | 2 | 0.373, 2, at 0: M0 += eps * Outer(V1,V0), eps +0.001; compacted 4->2; 0.000, 0, start | 62 | 61 | 6 |
| 2 | 0.6379 | 0.636 | 0.634 | 7 | 0.636, 7, at 0: V1 += eps * MatVec(M0,Normalize(V0)), eps -0.3; polished; 0.524, 4, at 0: M0 += eps * M0, eps -0.1; compacted 5->4; 0.524, 5, at 1: M1 += eps * M0, eps -0.1; 0.524, 5, at 2: M0 += eps * MatSub(M0,M1), eps -0.1; compacted 6->5 | 640 | 303 | 24 |
| 3 | 0.6532 | 0.652 | 0.646 | 13 | 0.652, 13, tap V2 <- M2 V2 at 1; M2 += eps * MatScale(Norm(V3),M2) at end, eps +0.01; 0.652, 13, tap V3 <- M2 V3 at 2; M2 += eps * MatScale(Norm(V3),M2) at end, eps +0.01; 0.646, 13, tap V1 <- M2 V1 at 5; M2 += eps * MatScale(Dot(V3,V3),M2) at end, eps +0.01; 0.643, 13, tap V0 <- M2 V0 at 0; M2 += eps * Outer(V0,VecScale(S0,V0)) at end, eps -0.01; polished | 4035 | 547 | 165 |
