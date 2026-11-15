# Search seed 28

task: regime collision3  alphabet: 20 ops, with Recip  readout: fixed o = S q  add-node mutation: on  candidates: 1500212  real evaluations (after cache): 918325  time: 2680s  pop: 500  tournament: 10

commit: ad31161  task seed: 1  train episodes: 144  persistent registers: 3 matrix, 0 vector, start identity  batch: 128

search: regularized evolution  tune-consts: 8  select: fitness

validation level (val > 0.651, T128 K8 val >= 0.838, train - val <= 0.03; checked every 50000 candidates): not reached

## Structural rediscovery (first candidate count at which the best rule belongs to a family)

* unclassified: 884 candidates
* decayed linear attention: 1524 candidates
* delta rule: 752996 candidates

## Milestones (accuracy levels: first candidate count where best train acc reached the reference rule; not rediscovery)

- linear attention (acc 0.362): 14588 candidates
- delta rule (beta=1) (acc 0.578): 749668 candidates
- delta rule (beta=0.5) (acc 0.617): 754164 candidates
- gated delta (alpha=0.9) (acc 0.519): 748940 candidates

## Best rule

```
S' = (σ(0)·((((v)⊗(k) + S))((0.616·((tanh(k))⊗(tanh(k)) - P1))ᵀ)·v)⊗((tanh(k) ⊙ tanh(k))) + (((v)⊗(k) + S) - (((v)⊗(k) + S))((0.616·((tanh(k))⊗(tanh(k)) - P1))ᵀ)))
P1' = σ(0)·((((v)⊗(k) + S))((0.616·((tanh(k))⊗(tanh(k)) - P1))ᵀ)·v)⊗((tanh(k) ⊙ tanh(k)))

Effective program (16 instructions):
  s3 = Sigmoid(s3)
  V2 = Tanh(V0)
  M3 = Outer(V1, V0)
  M3 = MatAdd(M3, M0)
  s0 = 0.6159
  M0 = Outer(V2, V2)
  M1 = MatSub(M0, M1)
  M1 = MatScale(s0, M1)
  V4 = Hadamard(V2, V2)
  M1 = Transpose(M1)
  M1 = MatMul(M3, M1)
  V5 = MatVec(M1, V1)
  M3 = MatSub(M3, M1)
  M1 = Outer(V5, V4)
  M1 = MatScale(s3, M1)
  M0 = MatAdd(M1, M3)

structure: unclassified  [a=1.000 b=0.471 c=-0.548 g=-0.014, erase c/a=0.548, R²=0.9534, 1408 steps]

train acc 0.631 ±0.014
test regime collision3: acc 0.636  margin 0.047  ±0.006
test d16 T12 ow0.3: acc 0.908  margin 0.259  ±0.004
test d16 T12 ow0.0: acc 0.898  margin 0.239  ±0.004
test d16 T12 ow0.6: acc 0.926  margin 0.266  ±0.005
test d32 T24 ow0.3: acc 0.976  margin 0.354  ±0.002
test d8 T6 ow0.3: acc 0.762  margin 0.099  ±0.009
test d16 T64 K8 ow0.3: acc 0.847  margin 0.179  ±0.008
test d16 T128 K8 ow0.3: acc 0.845  margin 0.173  ±0.011
```
