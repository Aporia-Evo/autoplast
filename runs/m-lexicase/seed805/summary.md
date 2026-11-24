# Search seed 805

task: regime collision3  alphabet: 20 ops, with Recip  readout: fixed o = S q  add-node mutation: on  candidates: 1500020  real evaluations (after cache): 764913  time: 1433s  pop: 500  tournament: 10

commit: dce11aa  task seed: 805  train episodes: 144  persistent registers: 3 matrix, 0 vector, start identity  batch: 128

search: regularized evolution  tune-consts: 0  select: lexicase  residual-insert: off

validation level (val > 0.651, T128 K8 val >= 0.838, train - val <= 0.03; checked every 50000 candidates): 750068 candidates

## Structural rediscovery (first candidate count at which the best rule belongs to a family)

* unclassified: 3060 candidates
* decayed linear attention: 21492 candidates
* delta rule: 187252 candidates

## Milestones (accuracy levels: first candidate count where best train acc reached the reference rule; not rediscovery)

- linear attention (acc 0.406): 14836 candidates
- delta rule (beta=1) (acc 0.620): 184564 candidates
- delta rule (beta=0.5) (acc 0.648): 187252 candidates
- gated delta (alpha=0.9) (acc 0.530): 21492 candidates

## Best rule

```
S' = (((v - ((S + P1) - ((P1)ᵀ)((S + P1)))·k))⊗(σ(0.728)·σ(0.728)·k) + ((S + P1) - ((P1)ᵀ)((S + P1))))
P1' = 0.432·P2
P2' = ((v - ((S + P1) - ((P1)ᵀ)((S + P1)))·k))⊗(σ(0.728)·σ(0.728)·k)

Effective program (14 instructions):
  M0 = MatAdd(M0, M1)
  M1 = Transpose(M1)
  M1 = MatMul(M1, M0)
  M0 = MatSub(M0, M1)
  V5 = MatVec(M0, V0)
  V1 = VecSub(V1, V5)
  s0 = 0.4322
  s1 = 0.7278
  M1 = MatScale(s0, M2)
  s2 = Sigmoid(s1)
  V5 = VecScale(s2, V0)
  V2 = VecScale(s2, V5)
  M2 = Outer(V1, V2)
  M0 = MatAdd(M2, M0)

structure: unclassified  [a=1.010 b=0.455 c=-0.453 g=-0.004, erase c/a=0.449, R²=0.7532, 1408 steps]

train acc 0.692 ±0.013
test regime collision3: acc 0.661  margin 0.047  ±0.006
test d16 T12 ow0.3: acc 0.916  margin 0.251  ±0.004
test d16 T12 ow0.0: acc 0.874  margin 0.219  ±0.004
test d16 T12 ow0.6: acc 0.916  margin 0.237  ±0.005
test d32 T24 ow0.3: acc 0.975  margin 0.343  ±0.002
test d8 T6 ow0.3: acc 0.766  margin 0.097  ±0.009
test d16 T64 K8 ow0.3: acc 0.827  margin 0.161  ±0.008
test d16 T128 K8 ow0.3: acc 0.833  margin 0.159  ±0.012
```
