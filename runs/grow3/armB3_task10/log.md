# grow v3, arm B, task seed 10, beam 4, compaction, stability gate 100

| round | best train fit | best train acc | best test acc | len | beam (train acc, len, last step) | Rust evals | grad passes | gate evals | refused by gate | seconds |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | 0.4114 | 0.416 | 0.385 | 2 | 0.416, 2, at 0: M0 += eps * Outer(V1,V0), eps +0.001; compacted 4->2; 0.000, 0, start | 62 | 61 | 4 | 0 | 7 |
| 2 | 0.6754 | 0.673 | 0.635 | 6 | 0.673, 6, at 0: V1 += eps * MatVec(M0,V0), eps -0.3; polished; 0.673, 7, at 0: M0 += eps * Outer(MatVec(M0,V0),V0), eps -0.3; polished; 0.565, 4, at 2: M0 += eps * M0, eps -0.1; compacted 5->4; 0.565, 7, at 0: M0 += eps * MatScale(Dot(V1,V1),M0), eps -0.1 | 457 | 303 | 11 | 0 | 26 |
| 3 | 0.7676 | 0.763 | 0.722 | 12 | 0.763, 12, tap V0 <- M1 V0 at 2; M1 += eps * Outer(V0,Tanh(V0)) at end, eps -0.1; polished; compacted 13->12; 0.763, 12, tap V0 <- M2 V0 at 2; M2 += eps * Outer(V0,Tanh(V0)) at end, eps -0.1; polished; compacted 13->12; 0.688, 12, tap V2 <- M2 V2 at 1; M2 += eps * MatScale(Norm(V2),M1) at end, eps +0.01; 0.685, 13, tap V2 <- M1 V2 at 1; M1 += eps * MatScale(Norm(V2),M1) at end, eps +0.003 | 3503 | 547 | 29 | 9 | 192 |
| 4 | 0.7976 | 0.791 | 0.768 | 14 | 0.791, 14, at 6: M0 += eps * M0, eps -0.03; polished; compacted 15->14; 0.791, 17, at 6: M0 += eps * MatScale(Sigmoid(S0),M0), eps -0.1; polished; 0.787, 17, at 6: M1 += eps * MatScale(S0,MatSub(M1,M2)), eps +0.01; 0.787, 17, at 6: M2 += eps * MatScale(S0,MatSub(M1,M2)), eps -0.01 | 6099 | 791 | 36 | 9 | 508 |
