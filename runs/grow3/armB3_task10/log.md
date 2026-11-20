# grow v3, arm B, task seed 10, beam 4, compaction, stability gate 100

| round | best train fit | best train acc | best test acc | len | beam (train acc, len, last step) | Rust evals | grad passes | gate evals | refused by gate | seconds |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | 0.4114 | 0.416 | 0.385 | 2 | 0.416, 2, at 0: M0 += eps * Outer(V1,V0), eps +0.001; compacted 4->2; 0.000, 0, start | 62 | 61 | 4 | 0 | 7 |
| 2 | 0.6754 | 0.673 | 0.635 | 6 | 0.673, 6, at 0: V1 += eps * MatVec(M0,V0), eps -0.3; polished; 0.673, 7, at 0: M0 += eps * Outer(MatVec(M0,V0),V0), eps -0.3; polished; 0.565, 4, at 2: M0 += eps * M0, eps -0.1; compacted 5->4; 0.565, 7, at 0: M0 += eps * MatScale(Dot(V1,V1),M0), eps -0.1 | 457 | 303 | 11 | 0 | 26 |
