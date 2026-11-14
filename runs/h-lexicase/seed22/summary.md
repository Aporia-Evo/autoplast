# Search seed 22

task: v2  alphabet: 19 ops  readout: fixed o = S q  add-node mutation: on  candidates: 1500020  real evaluations (after cache): 843609  time: 1624s  pop: 500  tournament: 10

commit: ad31161  task seed: 1  train episodes: 96  persistent registers: 1 matrix, 0 vector, start zero  batch: 128

search: regularized evolution  tune-consts: 0  select: lexicase

## Structural rediscovery (first candidate count at which the best rule belongs to a family)

* decayed linear attention: 1140 candidates
* linear, not error-correcting: 1908 candidates
* linear attention: 4724 candidates
* unclassified: 14836 candidates
* delta rule: 57076 candidates
* gated delta rule: 795252 candidates

## Milestones (accuracy levels: first candidate count where best train acc reached the reference rule; not rediscovery)

- linear attention (acc 0.772): 5748 candidates
- delta rule (beta=1) (acc 0.858): 53620 candidates
- delta rule (beta=0.5) (acc 0.932): 58484 candidates
- gated delta (alpha=0.9) (acc 0.729): 4724 candidates

## Best rule

```
S' = (0.101·((σ(2.184)·(v)⊗(σ(2.184)·k) - (0 - S)) - (((σ(2.184)·(v)⊗(σ(2.184)·k) - (0 - S)))(((v)⊗(σ(2.184)·k))ᵀ))(σ(2.184)·(v)⊗(σ(2.184)·k))) + ((σ(2.184)·(v)⊗(σ(2.184)·k) - (0 - S)) - (((σ(2.184)·(v)⊗(σ(2.184)·k) - (0 - S)))(((v)⊗(σ(2.184)·k))ᵀ))(σ(2.184)·(v)⊗(σ(2.184)·k))))

Effective program (14 instructions):
  s2 = 2.1837
  M1 = MatSub(M2, M0)
  s2 = Sigmoid(s2)
  V3 = VecScale(s2, V0)
  M0 = Outer(V1, V3)
  M3 = MatScale(s2, M0)
  M2 = MatSub(M3, M1)
  M0 = Transpose(M0)
  s2 = 0.1008
  M1 = MatMul(M2, M0)
  M3 = MatMul(M1, M3)
  M0 = MatSub(M2, M3)
  M3 = MatScale(s2, M0)
  M0 = MatAdd(M3, M0)

structure: gated delta rule  [a=1.101 b=0.244 c=-0.799 g=-0.000, erase c/a=0.726, R²=1.0000, 384 steps]

train acc 0.971 ±0.006
test d16 T12 ow0.3: acc 0.968  margin 0.312  ±0.003
test d16 T12 ow0.0: acc 0.948  margin 0.281  ±0.003
test d16 T12 ow0.6: acc 0.963  margin 0.312  ±0.004
test d32 T24 ow0.3: acc 0.975  margin 0.361  ±0.002
test d8 T6 ow0.3: acc 0.838  margin 0.140  ±0.008
test d16 T64 K8 ow0.3: acc 0.081  margin -0.485  ±0.006
test d16 T128 K8 ow0.3: acc 0.021  margin -0.642  ±0.005
```
