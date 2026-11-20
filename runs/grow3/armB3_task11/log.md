# grow v3, arm B, task seed 11, beam 4, compaction, stability gate 100

| round | best train fit | best train acc | best test acc | len | beam (train acc, len, last step) | Rust evals | grad passes | gate evals | refused by gate | seconds |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | 0.3958 | 0.401 | 0.385 | 2 | 0.401, 2, at 0: M0 += eps * Outer(V1,V0), eps +0.001; compacted 4->2; 0.000, 0, start | 62 | 61 | 4 | 0 | 6 |
| 2 | 0.6338 | 0.632 | 0.633 | 7 | 0.632, 7, at 0: V1 += eps * MatVec(M0,Normalize(V0)), eps -0.3; polished; 0.632, 7, at 0: M0 += eps * Outer(MatVec(M0,V0),V0), eps -0.3; polished; 0.528, 7, at 0: M0 += eps * MatScale(Norm(V0),M0), eps -0.1; 0.439, 6, at 2: M0 += eps * MatSub(M0,M1), eps -0.03 | 454 | 303 | 14 | 4 | 23 |
