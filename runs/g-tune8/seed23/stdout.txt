# Search seed 23

task: regime collision3  alphabet: 20 ops, with Recip  readout: fixed o = S q  add-node mutation: on  candidates: 1500084  real evaluations (after cache): 1194013  time: 3029s  pop: 500  tournament: 10

commit: ad31161  task seed: 1  train episodes: 144  persistent registers: 3 matrix, 0 vector, start identity  batch: 128

search: regularized evolution  tune-consts: 8  select: fitness

validation level (val > 0.651, T128 K8 val >= 0.838, train - val <= 0.03; checked every 50000 candidates): not reached

## Structural rediscovery (first candidate count at which the best rule belongs to a family)

* decayed linear attention: 1396 candidates
* unclassified: 6132 candidates
* linear attention: 7548 candidates

## Milestones (accuracy levels: first candidate count where best train acc reached the reference rule; not rediscovery)

- linear attention (acc 0.362): 7548 candidates
- delta rule (beta=1) (acc 0.578): not reached
- delta rule (beta=0.5) (acc 0.617): not reached
- gated delta (alpha=0.9) (acc 0.519): 508444 candidates

## Best rule

```
S' = (σ(σ(0.171))·(v)⊗((tanh(k) + tanh(((k ⊙ k) ⊙ (k ⊙ k))))) - σ(0.171)·σ(0.171)·((P2 + (0 - S)) + (0 - S)))
P1' = (v)⊗(σ(0.171)·((P2 + (0 - S)) + (0 - S))·(v ⊙ (tanh(k) + tanh(((k ⊙ k) ⊙ (k ⊙ k))))))
P2' = ((v)⊗(σ(0.171)·((P2 + (0 - S)) + (0 - S))·(v ⊙ (tanh(k) + tanh(((k ⊙ k) ⊙ (k ⊙ k)))))) - (σ(σ(0.171))·(v)⊗((tanh(k) + tanh(((k ⊙ k) ⊙ (k ⊙ k))))) - σ(0.171)·σ(0.171)·((P2 + (0 - S)) + (0 - S))))

Effective program (20 instructions):
  V3 = Tanh(V0)
  M0 = MatSub(M3, M0)
  s1 = 0.1712
  M1 = MatAdd(M2, M0)
  M3 = MatAdd(M1, M0)
  s3 = Sigmoid(s1)
  M2 = MatScale(s3, M3)
  V4 = Hadamard(V0, V0)
  V4 = Hadamard(V4, V4)
  V2 = Tanh(V4)
  V3 = VecAdd(V3, V2)
  V0 = Hadamard(V1, V3)
  M0 = Outer(V1, V3)
  M3 = MatScale(s3, M2)
  V0 = MatVec(M2, V0)
  M1 = Outer(V1, V0)
  s0 = Sigmoid(s3)
  M2 = MatScale(s0, M0)
  M0 = MatSub(M2, M3)
  M2 = MatSub(M1, M0)

structure: unclassified  [a=0.884 b=0.610 c=-0.001 g=0.000, erase c/a=0.001, R²=0.8717, 1408 steps]

train acc 0.521 ±0.014
test regime collision3: acc 0.507  margin -0.044  ±0.006
test d16 T12 ow0.3: acc 0.731  margin 0.122  ±0.007
test d16 T12 ow0.0: acc 0.713  margin 0.108  ±0.006
test d16 T12 ow0.6: acc 0.713  margin 0.099  ±0.009
test d32 T24 ow0.3: acc 0.655  margin 0.112  ±0.007
test d8 T6 ow0.3: acc 0.553  margin -0.013  ±0.010
test d16 T64 K8 ow0.3: acc 0.579  margin -0.011  ±0.011
test d16 T128 K8 ow0.3: acc 0.538  margin -0.032  ±0.016
```
