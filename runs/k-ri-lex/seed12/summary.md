# Search seed 12

task: regime collision3  alphabet: 20 ops, with Recip  readout: fixed o = S q  add-node mutation: on  candidates: 1500020  real evaluations (after cache): 1088422  time: 5793s  pop: 500  tournament: 10

commit: 6c2f60a  task seed: 1  train episodes: 144  persistent registers: 3 matrix, 0 vector, start identity  batch: 128

search: regularized evolution  tune-consts: 0  select: lexicase  residual-insert: on

residual insert: 357396 attempts, 111755 blocks inserted, 118577 times dead instructions removed first

validation level (val > 0.651, T128 K8 val >= 0.838, train - val <= 0.03; checked every 50000 candidates): 150004 candidates

## Structural rediscovery (first candidate count at which the best rule belongs to a family)

* unclassified: 1780 candidates
* decayed linear attention: 2932 candidates
* delta rule: 63220 candidates

## Milestones (accuracy levels: first candidate count where best train acc reached the reference rule; not rediscovery)

- linear attention (acc 0.362): 5876 candidates
- delta rule (beta=1) (acc 0.578): 63604 candidates
- delta rule (beta=0.5) (acc 0.617): 64884 candidates
- gated delta (alpha=0.9) (acc 0.519): 57332 candidates

## Best rule

```
S' = ((((P2 + ((v + -0.282·(P1·k + v)))⊗(tanh(k))))((P2 + ((v + -0.282·(P1·k + v)))⊗(tanh(k)))))(σ(0.203)·((((-0.282·(P1·k + v))⊗(k) + (-0.282·(P1·k + v))⊗(k)) + S) + 0.203·(S)ᵀ)) + (P2 + ((v + -0.282·(P1·k + v)))⊗(tanh(k))))
P1' = (((P2 + ((v + -0.282·(P1·k + v)))⊗(tanh(k))) + (P2 + ((v + -0.282·(P1·k + v)))⊗(tanh(k)))) + σ(0.203)·(((P2 + ((v + -0.282·(P1·k + v)))⊗(tanh(k))))((P2 + ((v + -0.282·(P1·k + v)))⊗(tanh(k)))))(σ(0.203)·((((-0.282·(P1·k + v))⊗(k) + (-0.282·(P1·k + v))⊗(k)) + S) + 0.203·(S)ᵀ)))
P2' = (P2 + ((v + -0.282·(P1·k + v)))⊗(tanh(k)))

Effective program (23 instructions):
  V2 = MatVec(M1, V0)
  V2 = VecAdd(V2, V1)
  s2 = -0.2822
  V2 = VecScale(s2, V2)
  V1 = VecAdd(V1, V2)
  M3 = Outer(V2, V0)
  M3 = MatAdd(M3, M3)
  M3 = MatAdd(M3, M0)
  M0 = Transpose(M0)
  s0 = 0.2028
  M0 = MatScale(s0, M0)
  M3 = MatAdd(M3, M0)
  s0 = Sigmoid(s0)
  V3 = Tanh(V0)
  M0 = Outer(V1, V3)
  M2 = MatAdd(M2, M0)
  M0 = MatScale(s0, M3)
  M1 = MatAdd(M2, M2)
  M3 = MatMul(M2, M2)
  M0 = MatMul(M3, M0)
  M3 = MatScale(s0, M0)
  M1 = MatAdd(M1, M3)
  M0 = MatAdd(M0, M2)

structure: unclassified  [a=1.020 b=0.567 c=-0.760 g=-0.003, erase c/a=0.745, R²=0.4761, 1408 steps]

train acc 0.723 ±0.013
test regime collision3: acc 0.720  margin 0.099  ±0.006
test d16 T12 ow0.3: acc 0.899  margin 0.218  ±0.005
test d16 T12 ow0.0: acc 0.810  margin 0.152  ±0.005
test d16 T12 ow0.6: acc 0.918  margin 0.234  ±0.005
test d32 T24 ow0.3: acc 0.976  margin 0.313  ±0.002
test d8 T6 ow0.3: acc 0.680  margin 0.054  ±0.010
test d16 T64 K8 ow0.3: acc 0.839  margin 0.151  ±0.008
test d16 T128 K8 ow0.3: acc 0.834  margin 0.148  ±0.012
```
