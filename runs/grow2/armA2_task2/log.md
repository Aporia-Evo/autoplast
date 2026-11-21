# grow v2, arm A, task seed 2, beam 4, compaction True

| round | best train fit | best train acc | best test acc | len | beam (train acc, len, last step) | Rust evals | grad passes | seconds |
|---|---|---|---|---|---|---|---|---|
| 1 | 0.3564 | 0.363 | 0.385 | 2 | 0.363, 2, at 0: M0 += eps * Outer(V1,V0), eps +0.001; compacted 4->2; 0.000, 0, start | 62 | 61 | 6 |
| 2 | 0.6353 | 0.634 | 0.633 | 7 | 0.634, 7, at 0: V1 += eps * MatVec(M0,Normalize(V0)), eps -0.3; polished; 0.512, 8, at 0: M0 += eps * MatScale(Dot(V1,V1),MatSub(M0,M1)), eps -0.1; 0.511, 4, at 0: M0 += eps * M0, eps -0.1; compacted 5->4; 0.511, 5, at 1: M1 += eps * M0, eps -0.1 | 411 | 303 | 22 |
| 3 | 0.6588 | 0.657 | 0.651 | 10 | 0.657, 10, at 0: M0 += eps * M1, eps +0.3; 0.647, 12, at 2: V0 += eps * VecScale(Dot(V1,V3),V0), eps -0.3; 0.646, 10, at 5: V1 += eps * VecScale(Dot(V1,V3),V3), eps +1; compacted 12->10; 0.644, 13, at 2: M0 += eps * MatScale(Dot(V3,V3),MatSub(M0,M1)), eps -0.01 | 3318 | 547 | 123 |
| 4 | 0.6636 | 0.662 | 0.663 | 13 | 0.662, 13, at 7: V1 += eps * VecScale(Dot(V1,V3),V1), eps +1; compacted 15->13; 0.662, 13, at 7: V3 += eps * VecScale(Dot(V1,V3),V1), eps +1; compacted 15->13; 0.662, 15, at 5: V0 += eps * VecScale(Dot(V1,V3),V2), eps -0.1; 0.661, 14, at 5: V1 += eps * Normalize(V3), eps -0.03 | 7024 | 791 | 347 |
| 5 | 0.6656 | 0.665 | 0.665 | 18 | 0.665, 18, at 6: S0 += eps * SMul(S0,Dot(V0,V2)), eps +0.03; 0.665, 19, at 6: M0 += eps * MatScale(Sigmoid(S0),MatSub(M0,M1)), eps -0.01; 0.664, 17, at 0: V1 += eps * MatVec(M0,V0), eps -0.01; 0.664, 17, at 5: V1 += eps * Tanh(V3), eps -0.01 | 10435 | 1035 | 633 |
| 6 | 0.6662 | 0.666 | 0.665 | 21 | 0.666, 21, at 5: M0 += eps * MatScale(Norm(V2),M0), eps -0.003; compacted 23->21; 0.666, 22, at 6: S0 += eps * Dot(V0,V0), eps +0.003; 0.666, 22, at 11: S0 += eps * SMul(S0,Norm(V2)), eps -0.01; compacted 23->22; 0.665, 18, at 6: S0 += eps * SMul(S0,Dot(V0,V2)), eps +0.03 | 13299 | 1219 | 963 |
