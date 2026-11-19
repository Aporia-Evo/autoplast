# grow arm A, task seed 1

| round | step | train fit | train acc | test acc | len | Rust evals | seconds |
|---|---|---|---|---|---|---|---|
| 1 | at 0: M0 += eps * Outer(V1,V0), eps +0.001 | 0.3554 | 0.362 | 0.385 | 4 | 51 | 5 |
| 2 | at 0: M0 += eps * M0, eps -0.1 | 0.4965 | 0.500 | 0.519 | 7 | 549 | 18 |
| 3 | at 0: M0 += eps * M0, eps -0.03 | 0.5006 | 0.505 | 0.517 | 10 | 1447 | 41 |
| 4 | at 8: M1 += eps * MatScale(Recip(S0),Transpose(M0)), eps +0.01 | 0.5024 | 0.507 | 0.516 | 16 | 2345 | 75 |
| 5 | at 0: M0 += eps * Transpose(M0), eps +0.03 | 0.5030 | 0.508 | 0.511 | 20 | 3195 | 130 |
| 6 | at 0: M0 += eps * M0, eps +0.001 | 0.5044 | 0.509 | 0.511 | 23 | 3373 | 192 |
| 7 | stop: no candidate fits | | | | | 3373 | 277 |

```
S' = …
P1' = 0.001·((v)⊗(k) + 0.010·1/(0.001)·(((((S + 0.001·S) + 0.030·((S + 0.001·S))ᵀ) + -0.030·((S + 0.001·S) + 0.030·((S + 0.001·S))ᵀ)) + -0.100·(((S + 0.001·S) + 0.030·((S + 0.001·S))ᵀ) + -0.030·((S + 0.001·S) + 0.030·((S + 0.001·S))ᵀ))))ᵀ)
P2' = (((((S + 0.001·S) + 0.030·((S + 0.001·S))ᵀ) + -0.030·((S + 0.001·S) + 0.030·((S + 0.001·S))ᵀ)) + -0.100·(((S + 0.001·S) + 0.030·((S + 0.001·S))ᵀ) + -0.030·((S + 0.001·S) + 0.030·((S + 0.001·S))ᵀ))))ᵀ

Effective program (23 instructions):
  s0 = 0.0010
  M1 = MatScale(s0, M0)
  M0 = MatAdd(M0, M1)
  M1 = Transpose(M0)
  s0 = 0.0300
  M1 = MatScale(s0, M1)
  M0 = MatAdd(M0, M1)
  s0 = -0.0300
  M1 = MatScale(s0, M0)
  M0 = MatAdd(M0, M1)
  s0 = -0.1000
  M1 = MatScale(s0, M0)
  M0 = MatAdd(M0, M1)
  M1 = Outer(V1, V0)
  s0 = 0.0010
  s1 = Recip(s0)
  M2 = Transpose(M0)
  M3 = MatScale(s1, M2)
  s2 = 0.0100
  M3 = MatScale(s2, M3)
  M1 = MatAdd(M1, M3)
  M1 = MatScale(s0, M1)
  M0 = MatAdd(M0, M1)

structure: decayed linear attention  [a=0.883 b=0.001 c=-0.003 g=-0.000, erase c/a=0.003, R²=0.9965, 1408 steps]

train acc 0.509 ±0.014
test regime collision3: acc 0.511  margin -0.042  ±0.006
test d16 T12 ow0.3: acc 0.736  margin 0.127  ±0.007
test d16 T12 ow0.0: acc 0.723  margin 0.116  ±0.006
test d16 T12 ow0.6: acc 0.720  margin 0.109  ±0.009
test d32 T24 ow0.3: acc 0.650  margin 0.108  ±0.007
test d8 T6 ow0.3: acc 0.643  margin 0.034  ±0.010
test d16 T64 K8 ow0.3: acc 0.579  margin -0.012  ±0.011
test d16 T128 K8 ow0.3: acc 0.554  margin -0.027  ±0.016


```
