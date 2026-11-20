# grow v2, arm A, task seed 6, beam 4, compaction True

| round | best train fit | best train acc | best test acc | len | beam (train acc, len, last step) | Rust evals | grad passes | seconds |
|---|---|---|---|---|---|---|---|---|
| 1 | 0.4143 | 0.420 | 0.385 | 3 | 0.420, 3, at 0: M0 += eps * Outer(Tanh(V1),V0), eps +0.001; compacted 5->3; 0.000, 0, start | 65 | 61 | 6 |
| 2 | 0.6302 | 0.630 | 0.619 | 6 | 0.630, 6, at 0: V1 += eps * MatVec(M0,Tanh(V0)), eps -1; compacted 8->6; 0.627, 8, at 1: V2 += eps * MatVec(M0,Tanh(V0)), eps -1; polished; 0.528, 7, at 0: M0 += eps * MatSub(M0,M1), eps -0.1; 0.520, 8, at 1: M0 += eps * MatScale(Norm(V2),M0), eps -0.1 | 602 | 303 | 23 |
| 3 | 0.6472 | 0.645 | 0.638 | 10 | 0.645, 10, at 4: V2 += eps * Normalize(V3), eps +0.3; 0.644, 11, at 5: V2 += eps * VecScale(Dot(V2,V3),V2), eps +1; compacted 13->11; 0.644, 11, at 5: V3 += eps * VecScale(Dot(V2,V3),V2), eps +1; compacted 13->11; 0.644, 13, at 3: V0 += eps * VecScale(Dot(V2,V3),V0), eps -0.3 | 4320 | 547 | 132 |
| 4 | 0.6513 | 0.649 | 0.640 | 12 | 0.649, 12, at 2: V3 += eps * V1, eps +0.3; compacted 13->12; 0.649, 14, at 0: M0 += eps * Outer(V1,V0), eps +0.03; 0.647, 13, at 1: V2 += eps * V1, eps -0.1; 0.647, 14, at 0: V0 += eps * MatVec(M0,V0), eps -0.1 | 8252 | 791 | 329 |
| 5 | 0.6525 | 0.651 | 0.638 | 16 | 0.651, 16, at 7: V2 += eps * VecSub(V1,V3), eps +0.01; 0.651, 18, at 0: M0 += eps * Outer(V1,V0), eps +0.03; 0.650, 14, at 0: V0 += eps * V0, eps +0.01; compacted 15->14; 0.650, 16, at 0: V0 += eps * Tanh(V0), eps +0.01 | 12205 | 1035 | 530 |
