# grow v2, arm A, task seed 4, beam 4, compaction True

| round | best train fit | best train acc | best test acc | len | beam (train acc, len, last step) | Rust evals | grad passes | seconds |
|---|---|---|---|---|---|---|---|---|
| 1 | 0.3663 | 0.373 | 0.385 | 2 | 0.373, 2, at 0: M0 += eps * Outer(V1,V0), eps +0.001; compacted 4->2; 0.000, 0, start | 62 | 61 | 5 |
| 2 | 0.6379 | 0.636 | 0.634 | 7 | 0.636, 7, at 0: V1 += eps * MatVec(M0,Normalize(V0)), eps -0.3; polished; 0.524, 4, at 0: M0 += eps * M0, eps -0.1; compacted 5->4; 0.524, 5, at 1: M1 += eps * M0, eps -0.1; 0.524, 5, at 2: M0 += eps * MatSub(M0,M1), eps -0.1; compacted 6->5 | 448 | 303 | 17 |
| 3 | 0.6551 | 0.654 | 0.646 | 10 | 0.654, 10, at 5: V1 += eps * VecScale(Dot(V1,V3),V3), eps +1; compacted 12->10; 0.649, 10, at 4: V3 += eps * VecScale(Dot(V3,V3),V3), eps +1; compacted 12->10; 0.647, 12, at 5: V0 += eps * VecScale(Dot(V1,V3),V2), eps +0.3; 0.641, 11, at 2: V1 += eps * Normalize(V3), eps -0.03 | 3232 | 547 | 95 |
