# grow v2, arm A, task seed 1, beam 4, compaction True

| round | best train fit | best train acc | best test acc | len | beam (train acc, len, last step) | Rust evals | grad passes | seconds |
|---|---|---|---|---|---|---|---|---|
| 1 | 0.3556 | 0.362 | 0.385 | 2 | 0.362, 2, at 0: M0 += eps * Outer(V1,V0), eps +0.001; compacted 4->2; 0.000, 0, start | 62 | 61 | 6 |
| 2 | 0.6061 | 0.605 | 0.625 | 6 | 0.605, 6, at 0: V1 += eps * MatVec(M0,V0), eps -0.3; polished; 0.605, 7, at 0: M0 += eps * Outer(MatVec(M0,V0),V0), eps -0.3; polished; 0.605, 7, at 1: M1 += eps * Outer(MatVec(M0,V0),V0), eps -0.3; polished; 0.500, 4, at 0: M0 += eps * M0, eps -0.1; compacted 5->4 | 443 | 303 | 19 |
| 3 | 0.6225 | 0.622 | 0.653 | 9 | 0.622, 9, at 2: S0 += eps * Dot(V2,V2), eps -0.3; compacted 10->9; 0.620, 11, at 4: V1 += eps * VecScale(Dot(V1,V2),V2), eps +3; 0.618, 12, at 3: S0 += eps * SMul(S0,Dot(V2,V2)), eps +0.3; 0.617, 11, at 3: V2 += eps * VecScale(Dot(V2,V2),V2), eps +3 | 3602 | 547 | 105 |
| 4 | 0.6289 | 0.628 | 0.653 | 17 | 0.628, 17, at 10: M0 += eps * MatScale(Recip(S0),M0), eps -0.01; 0.628, 17, at 11: M1 += eps * MatScale(Recip(S0),M0), eps -0.01; 0.627, 13, at 1: M0 += eps * M0, eps +0.03; compacted 14->13; 0.626, 13, at 1: M0 += eps * MatSub(M0,M1), eps -0.003 | 7273 | 791 | 287 |
| 5 | 0.6409 | 0.640 | 0.000 | 21 | 0.640, 21, at 14: S2 += eps * SMul(S1,S1), eps -0.001; polished; 0.640, 22, at 10: M0 += eps * MatScale(Recip(S2),M0), eps -0.001; 0.638, 22, at 11: M1 += eps * MatScale(Recip(S2),M0), eps -0.001; 0.631, 19, at 0: V0 += eps * V0, eps -0.01; compacted 20->19 | 10117 | 1035 | 541 |
| 6 | 0.6409 | 0.640 | 0.000 | 21 | 0.640, 21, at 14: S2 += eps * SMul(S1,S1), eps -0.001; polished; 0.640, 22, at 10: M0 += eps * MatScale(Recip(S2),M0), eps -0.001; 0.639, 17, at 14: M0 += eps * MatScale(Recip(S2),M0), eps -0.001; polished; compacted 24->17; 0.638, 22, at 11: M1 += eps * MatScale(Recip(S2),M0), eps -0.001 | 10779 | 1099 | 868 |
