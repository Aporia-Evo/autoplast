# grow v2, arm B, task seed 3, beam 4, compaction True

| round | best train fit | best train acc | best test acc | len | beam (train acc, len, last step) | Rust evals | grad passes | seconds |
|---|---|---|---|---|---|---|---|---|
| 1 | 0.4112 | 0.416 | 0.387 | 3 | 0.416, 3, at 0: M0 += eps * Outer(V1,Tanh(V0)), eps +0.001; compacted 5->3; 0.000, 0, start | 65 | 61 | 7 |
| 2 | 0.6484 | 0.646 | 0.634 | 8 | 0.646, 8, at 1: V1 += eps * MatVec(M0,VecAdd(V0,V2)), eps -0.3; 0.517, 7, at 0: M0 += eps * MatSub(M0,M1), eps -0.1; 0.517, 10, tap V1 <- M2 V1 at 0; M2 += eps * MatScale(Dot(V2,V2),Transpose(M2)) at end, eps +0.1; 0.516, 8, at 0: M0 += eps * MatScale(Dot(V0,V0),M0), eps -0.1 | 943 | 303 | 35 |
