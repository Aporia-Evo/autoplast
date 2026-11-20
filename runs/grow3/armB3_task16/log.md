# grow v3, arm B, task seed 16, beam 4, compaction, stability gate 100

| round | best train fit | best train acc | best test acc | len | beam (train acc, len, last step) | Rust evals | grad passes | gate evals | refused by gate | seconds |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | 0.3849 | 0.391 | 0.385 | 2 | 0.391, 2, at 0: M0 += eps * Outer(V1,V0), eps +0.001; compacted 4->2; 0.000, 0, start | 62 | 61 | 4 | 0 | 7 |
| 2 | 0.6558 | 0.653 | 0.641 | 7 | 0.653, 7, at 0: V1 += eps * MatVec(M0,Tanh(V0)), eps -1; polished; 0.509, 7, at 0: M0 += eps * MatScale(Dot(V0,V0),M0), eps -0.1; 0.422, 6, at 2: M0 += eps * MatSub(M0,M1), eps -0.03; polished; 0.399, 6, at 0: V0 += eps * Hadamard(V0,V1), eps +0.3 | 453 | 303 | 18 | 8 | 25 |
| 3 | 0.6563 | 0.654 | 0.641 | 11 | 0.654, 11, tap V0 <- M1 V0 at 0; M1 += eps * Outer(Tanh(V0),V0) at end, eps +0.003; compacted 13->11; 0.654, 11, tap V0 <- M2 V0 at 0; M2 += eps * Outer(Tanh(V0),V0) at end, eps +0.003; compacted 13->11; 0.653, 7, at 0: V1 += eps * MatVec(M0,Tanh(V0)), eps -1; polished; 0.649, 6, at 0: V1 += eps * MatVec(M0,V0), eps -0.3; polished; compacted 10->6 | 3565 | 487 | 52 | 24 | 212 |
| 4 | 0.6653 | 0.663 | 0.645 | 13 | 0.663, 13, tap V1 <- M1 V1 at 4; M1 += eps * MatScale(Dot(V2,V2),Transpose(M1)) at end, eps +0.01; 0.661, 12, tap V2 <- M1 V2 at 1; M1 += eps * MatScale(Dot(V2,V2),M1) at end, eps +0.01; 0.660, 13, tap V1 <- M2 V1 at 4; M2 += eps * MatScale(Norm(V2),Transpose(M1)) at end, eps +0.01; 0.656, 16, at 0: M1 += eps * Outer(Tanh(V0),V0), eps +0.003 | 6708 | 731 | 86 | 54 | 464 |
