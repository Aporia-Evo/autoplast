# grow v3, arm B, task seed 17, beam 4, compaction, stability gate 100

| round | best train fit | best train acc | best test acc | len | beam (train acc, len, last step) | Rust evals | grad passes | gate evals | refused by gate | seconds |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | 0.4049 | 0.410 | 0.385 | 2 | 0.410, 2, at 0: M0 += eps * Outer(V1,V0), eps +0.001; compacted 4->2; 0.000, 0, start | 62 | 61 | 4 | 0 | 7 |
| 2 | 0.6609 | 0.658 | 0.633 | 6 | 0.658, 6, at 0: V1 += eps * MatVec(M0,V0), eps -0.3; polished; 0.658, 7, at 0: M0 += eps * Outer(MatVec(M0,V0),V0), eps -0.3; polished; 0.568, 7, at 0: M0 += eps * MatScale(Norm(V0),M0), eps -0.1; 0.439, 6, at 2: M0 += eps * MatSub(M0,M1), eps -0.03; polished | 453 | 303 | 15 | 4 | 26 |
| 3 | 0.7453 | 0.740 | 0.726 | 12 | 0.740, 12, tap V0 <- M1 V0 at 2; M1 += eps * Outer(MatVec(M1,V0),V0) at end, eps -0.1; polished; compacted 13->12; 0.677, 12, tap V0 <- M1 V0 at 0; M1 += eps * MatScale(Norm(V2),M1) at end, eps +0.003; 0.677, 12, tap V0 <- M2 V0 at 0; M2 += eps * MatScale(Norm(V2),M1) at end, eps +0.003; 0.677, 13, tap V2 <- M1 V2 at 1; M1 += eps * MatScale(Norm(V2),M1) at end, eps +0.003 | 3320 | 547 | 23 | 5 | 206 |
| 4 | 0.7751 | 0.769 | 0.746 | 18 | 0.769, 18, tap V0 <- M2 V0 at 1; M2 += eps * MatScale(S0,Transpose(M1)) at end, eps -0.03; 0.766, 17, tap V0 <- M2 V0 at 0; M2 += eps * Transpose(M1) at end, eps +0.01; polished; 0.757, 17, at 1: M0 += eps * MatScale(Dot(V0,V0),M0), eps -0.01; polished; 0.755, 14, at 6: M0 += eps * M0, eps -0.01; polished; compacted 15->14 | 6477 | 791 | 31 | 5 | 518 |
