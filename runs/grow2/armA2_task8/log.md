# grow v2, arm A, task seed 8, beam 4, compaction True

| round | best train fit | best train acc | best test acc | len | beam (train acc, len, last step) | Rust evals | grad passes | seconds |
|---|---|---|---|---|---|---|---|---|
| 1 | 0.4191 | 0.424 | 0.385 | 2 | 0.424, 2, at 0: M0 += eps * Outer(V1,V0), eps +0.001; compacted 4->2; 0.000, 0, start | 62 | 61 | 6 |
| 2 | 0.6650 | 0.662 | 0.642 | 7 | 0.662, 7, at 0: V1 += eps * MatVec(M0,Tanh(V0)), eps -1; polished; 0.558, 8, at 0: M0 += eps * MatScale(Norm(V0),MatSub(M0,M1)), eps -0.1; 0.556, 5, at 1: M0 += eps * MatSub(M0,M1), eps -0.1; compacted 6->5; 0.556, 6, at 1: M1 += eps * MatSub(M0,M1), eps -0.1 | 445 | 303 | 17 |
| 3 | 0.6769 | 0.675 | 0.645 | 12 | 0.675, 12, at 2: V1 += eps * VecScale(Dot(V1,V3),V1), eps -0.3; 0.672, 11, at 0: V1 += eps * MatVec(M0,V0), eps -0.1; 0.671, 11, at 2: V1 += eps * Tanh(V3), eps -0.1; 0.670, 10, at 4: V3 += eps * VecScale(Dot(V1,V3),V1), eps +1; compacted 12->10 | 3543 | 547 | 115 |
| 4 | 0.6804 | 0.679 | 0.644 | 18 | 0.679, 18, at 5: M0 += eps * MatScale(Sigmoid(S1),MatSub(M0,M1)), eps -0.01; 0.678, 16, at 0: V1 += eps * MatVec(M0,V0), eps -0.01; 0.677, 15, at 3: V1 += eps * Normalize(V3), eps -0.03; compacted 16->15; 0.677, 15, at 2: V1 += eps * Tanh(V3), eps -0.01; compacted 16->15 | 7504 | 791 | 307 |
| 5 | 0.6812 | 0.680 | 0.644 | 18 | 0.680, 18, at 7: M0 += eps * M0, eps -0.003; compacted 19->18; 0.680, 19, at 12: V1 += eps * Normalize(V3), eps +0.01; 0.680, 19, at 12: V3 += eps * Normalize(V3), eps +0.01; 0.680, 20, at 1: M0 += eps * MatSub(M0,M1), eps -0.003 | 11401 | 1035 | 651 |
| 6 | 0.6817 | 0.680 | 0.645 | 21 | 0.680, 21, at 1: V2 += eps * V1, eps -0.01; compacted 22->21; 0.680, 22, at 0: V0 += eps * V1, eps -0.003; 0.680, 22, at 2: V3 += eps * V0, eps +0.001; 0.680, 23, at 0: M0 += eps * Outer(V1,V0), eps -0.03 | 14517 | 1279 | 1023 |
