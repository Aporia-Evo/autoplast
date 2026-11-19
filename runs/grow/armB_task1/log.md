# grow arm B, task seed 1

| round | step | train fit | train acc | test acc | len | Rust evals | seconds |
|---|---|---|---|---|---|---|---|
| 1 | at 0: M0 += eps * Outer(V1,V0), eps +0.001 | 0.3554 | 0.362 | 0.385 | 4 | 51 | 5 |
| 2 | at 0: M0 += eps * M0, eps -0.1 | 0.4965 | 0.500 | 0.519 | 7 | 693 | 20 |
| 3 | tap V0 <- M2 V0 at 0; M2 += eps * Outer(Tanh(V0),V0) at end, eps -0.3; constants polished | 0.5944 | 0.594 | 0.604 | 13 | 1591 | 59 |
| 4 | at 0: M0 += eps * Outer(MatVec(M0,V0),V0), eps -0.3; constants polished | 0.7694 | 0.764 | 0.776 | 18 | 2249 | 127 |
| 5 | at 6: M0 += eps * Outer(V2,Normalize(V0)), eps -0.1; constants polished | 0.8578 | 0.850 | 0.860 | 23 | 2795 | 230 |
| 6 | stop: no candidate fits | | | | | 2795 | 415 |

```
S' = ((((S + -0.243·(S·k)⊗(k)) + -0.387·(S·k)⊗(norm(P2·k))) + -0.027·((S + -0.243·(S·k)⊗(k)) + -0.387·(S·k)⊗(norm(P2·k)))) + 0.013·(v)⊗(P2·k))
P1' = -0.678·(tanh(P2·k))⊗(P2·k)
P2' = (P2 + -0.678·(tanh(P2·k))⊗(P2·k))

Effective program (23 instructions):
  V2 = MatVec(M0, V0)
  M1 = Outer(V2, V0)
  s0 = -0.2426
  M1 = MatScale(s0, M1)
  M0 = MatAdd(M0, M1)
  V0 = MatVec(M2, V0)
  V3 = Normalize(V0)
  M1 = Outer(V2, V3)
  s0 = -0.3873
  M1 = MatScale(s0, M1)
  M0 = MatAdd(M0, M1)
  s0 = -0.0267
  M1 = MatScale(s0, M0)
  M0 = MatAdd(M0, M1)
  M1 = Outer(V1, V0)
  s0 = 0.0133
  M1 = MatScale(s0, M1)
  M0 = MatAdd(M0, M1)
  V1 = Tanh(V0)
  M1 = Outer(V1, V0)
  s0 = -0.6780
  M1 = MatScale(s0, M1)
  M2 = MatAdd(M2, M1)

structure: unclassified  [a=0.975 b=0.005 c=-0.582 g=-0.017, erase c/a=0.597, R²=0.6078, 1408 steps]

train acc 0.850 ±0.010
test regime collision3: acc 0.860  margin 0.212  ±0.004
test d16 T12 ow0.3: acc 0.935  margin 0.316  ±0.004
test d16 T12 ow0.0: acc 0.993  margin 0.346  ±0.001
test d16 T12 ow0.6: acc 0.926  margin 0.271  ±0.005
test d32 T24 ow0.3: acc 0.960  margin 0.393  ±0.003
test d8 T6 ow0.3: acc 0.856  margin 0.161  ±0.007
test d16 T64 K8 ow0.3: acc 0.982  margin 0.303  ±0.003
test d16 T128 K8 ow0.3: acc 0.984  margin 0.305  ±0.004


```
