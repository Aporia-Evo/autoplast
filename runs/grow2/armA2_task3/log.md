# grow v2, arm A, task seed 3, beam 4, compaction True

| round | best train fit | best train acc | best test acc | len | beam (train acc, len, last step) | Rust evals | grad passes | seconds |
|---|---|---|---|---|---|---|---|---|
| 1 | 0.4112 | 0.416 | 0.387 | 3 | 0.416, 3, at 0: M0 += eps * Outer(V1,Tanh(V0)), eps +0.001; compacted 5->3; 0.000, 0, start | 65 | 61 | 6 |
| 2 | 0.6484 | 0.646 | 0.634 | 8 | 0.646, 8, at 1: V1 += eps * MatVec(M0,VecAdd(V0,V2)), eps -0.3; 0.517, 7, at 0: M0 += eps * MatSub(M0,M1), eps -0.1; 0.516, 8, at 0: M0 += eps * MatScale(Dot(V0,V0),M0), eps -0.1; 0.514, 8, at 2: M1 += eps * MatScale(Dot(V2,V2),M0), eps -0.1; polished | 589 | 303 | 22 |
| 3 | 0.6522 | 0.650 | 0.642 | 12 | 0.650, 12, at 5: V1 += eps * Normalize(V4), eps -0.1; 0.650, 12, at 5: V4 += eps * Normalize(V4), eps -0.1; 0.650, 11, at 5: V1 += eps * Tanh(V4), eps -0.3; compacted 12->11; 0.650, 13, at 0: V1 += eps * MatVec(M0,Normalize(V0)), eps +0.1 | 4283 | 547 | 150 |
| 4 | 0.6598 | 0.658 | 0.647 | 16 | 0.658, 16, at 6: V1 += eps * VecScale(Dot(V2,V2),V0), eps -0.1; compacted 17->16; 0.658, 16, at 3: V1 += eps * Normalize(V4), eps +0.1; 0.657, 15, at 1: V2 += eps * V0, eps -0.1; 0.656, 14, at 1: V0 += eps * V2, eps -0.3; compacted 15->14 | 8199 | 791 | 373 |
| 5 | 0.6628 | 0.662 | 0.647 | 19 | 0.662, 19, at 0: V0 += eps * V1, eps +0.03; 0.662, 19, at 4: V4 += eps * V2, eps -0.1; 0.661, 19, at 1: V2 += eps * V1, eps +0.03; 0.661, 20, at 0: M0 += eps * Outer(V0,V0), eps +0.03 | 12097 | 1035 | 693 |
| 6 | 0.6641 | 0.663 | 0.646 | 22 | 0.663, 22, at 1: V0 += eps * V1, eps -0.1; 0.663, 23, at 13: V1 += eps * VecSub(V0,V4), eps -0.01; 0.663, 23, at 13: V4 += eps * VecSub(V0,V4), eps -0.01; 0.663, 22, at 2: V2 += eps * V1, eps -0.01 | 14944 | 1279 | 1120 |
