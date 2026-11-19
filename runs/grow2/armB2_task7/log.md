# grow v2, arm B, task seed 7, beam 4, compaction True

| round | best train fit | best train acc | best test acc | len | beam (train acc, len, last step) | Rust evals | grad passes | seconds |
|---|---|---|---|---|---|---|---|---|
| 1 | 0.3891 | 0.394 | 0.385 | 2 | 0.394, 2, at 0: M0 += eps * Outer(V1,V0), eps +0.001; compacted 4->2; 0.000, 0, start | 62 | 61 | 6 |
| 2 | 0.6510 | 0.649 | 0.640 | 7 | 0.649, 7, at 0: V1 += eps * MatVec(M0,Tanh(V0)), eps -1; polished; 0.541, 7, at 0: M0 += eps * MatScale(Dot(V1,V1),M0), eps -0.1; 0.541, 7, at 1: M1 += eps * MatScale(Dot(V1,V1),M0), eps -0.1; 0.538, 5, tap V0 <- M2 V0 at 0; M2 += eps * M2 at end, eps +0.1; compacted 6->5 | 540 | 303 | 23 |
| 3 | 0.6658 | 0.664 | 0.648 | 13 | 0.664, 13, tap V2 <- M2 V2 at 1; M2 += eps * MatScale(Dot(V3,V3),M2) at end, eps +0.03; 0.664, 13, tap V3 <- M2 V3 at 2; M2 += eps * MatScale(Dot(V3,V3),M2) at end, eps +0.03; 0.655, 13, tap V0 <- M2 V0 at 0; M2 += eps * Outer(V0,Tanh(V2)) at end, eps +0.003; 0.649, 7, at 0: V1 += eps * MatVec(M0,Tanh(V0)), eps -1; polished | 4015 | 487 | 204 |
