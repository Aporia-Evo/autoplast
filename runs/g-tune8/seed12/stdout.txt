# Search seed 12

task: regime collision3  alphabet: 20 ops, with Recip  readout: fixed o = S q  add-node mutation: on  candidates: 1500196  real evaluations (after cache): 1101172  time: 1860s  pop: 500  tournament: 10

commit: ad31161  task seed: 1  train episodes: 144  persistent registers: 3 matrix, 0 vector, start identity  batch: 128

search: regularized evolution  tune-consts: 8  select: fitness

validation level (val > 0.651, T128 K8 val >= 0.838, train - val <= 0.03; checked every 50000 candidates): not reached

## Structural rediscovery (first candidate count at which the best rule belongs to a family)

* unclassified: 3572 candidates
* decayed linear attention: 4212 candidates
* gated delta rule: 9076 candidates
* delta rule: 10628 candidates
* delta + Kronecker mix: 87924 candidates

## Milestones (accuracy levels: first candidate count where best train acc reached the reference rule; not rediscovery)

- linear attention (acc 0.362): 9460 candidates
- delta rule (beta=1) (acc 0.578): 10628 candidates
- delta rule (beta=0.5) (acc 0.617): 11012 candidates
- gated delta (alpha=0.9) (acc 0.519): 10628 candidates

## Best rule

```
S' = ((0 + S) - (((S + P2)·k - v))⊗(|((S + P2)·k - v)|·0.398·k))
P1' = (0 + S)
P2' = σ(<((S + P2)·k - v), tanh((S + P2)·k)>)·((((S + P2)·k - v) + (k ⊙ k)))⊗(tanh((S + P2)·k))

Effective program (17 instructions):
  M1 = MatAdd(M3, M0)
  M2 = MatAdd(M0, M2)
  V4 = MatVec(M2, V0)
  V1 = VecSub(V4, V1)
  V3 = Tanh(V4)
  V2 = Hadamard(V0, V0)
  s3 = Dot(V1, V3)
  V4 = VecAdd(V1, V2)
  M2 = Outer(V4, V3)
  s2 = Norm(V1)
  s0 = 0.3977
  V3 = VecScale(s0, V0)
  V2 = VecScale(s2, V3)
  M0 = Outer(V1, V2)
  M0 = MatSub(M1, M0)
  s0 = Sigmoid(s3)
  M2 = MatScale(s0, M2)

structure: unclassified  [a=1.000 b=0.450 c=-0.434 g=-0.324, erase c/a=0.434, R²=0.9320, 1408 steps]

train acc 0.637 ±0.014
test regime collision3: acc 0.634  margin 0.032  ±0.006
test d16 T12 ow0.3: acc 0.905  margin 0.230  ±0.004
test d16 T12 ow0.0: acc 0.882  margin 0.210  ±0.004
test d16 T12 ow0.6: acc 0.917  margin 0.230  ±0.005
test d32 T24 ow0.3: acc 0.982  margin 0.332  ±0.002
test d8 T6 ow0.3: acc 0.697  margin 0.056  ±0.010
test d16 T64 K8 ow0.3: acc 0.821  margin 0.140  ±0.008
test d16 T128 K8 ow0.3: acc 0.798  margin 0.132  ±0.013
```
