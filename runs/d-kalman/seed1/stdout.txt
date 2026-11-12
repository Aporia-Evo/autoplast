# Search seed 1

task: regime collision3  alphabet: 20 ops, with Recip  readout: fixed o = S q  add-node mutation: on  candidates: 1500020  real evaluations (after cache): 976088  time: 3661s  pop: 500  tournament: 10

commit: e979a8e  task seed: 1  train episodes: 144  persistent registers: 3 matrix, 0 vector, start identity  batch: 128

## Structural rediscovery (first candidate count at which the best rule belongs to a family)

* unclassified: 5364 candidates
* decayed linear attention: 9332 candidates
* linear, not error-correcting: 11764 candidates
* linear attention: 70900 candidates

## Milestones (accuracy levels: first candidate count where best train acc reached the reference rule; not rediscovery)

- linear attention (acc 0.362): 70900 candidates
- delta rule (beta=1) (acc 0.578): not reached
- delta rule (beta=0.5) (acc 0.617): not reached
- gated delta (alpha=0.9) (acc 0.519): 147700 candidates

## Best rule

```
S' = |tanh(norm(tanh((P2·(0 + v) ⊙ k))))|·(((0 + v))⊗(tanh(k)) + |tanh((0 + v))|·S)
P2' = (<(((0 + v))⊗(tanh(k)) + |tanh((0 + v))|·S)·tanh(k), (((0 + v))⊗(tanh(k)) + |tanh((0 + v))|·S)·tanh(k)>·(|tanh((0 + v))|·S)(|tanh((0 + v))|·S) + P1)

Effective program (19 instructions):
  V3 = VecAdd(V2, V1)
  V1 = Tanh(V3)
  s1 = Norm(V1)
  V4 = MatVec(M2, V3)
  V2 = Hadamard(V4, V0)
  V5 = Tanh(V2)
  V2 = Normalize(V5)
  V4 = Tanh(V0)
  M2 = Outer(V3, V4)
  M3 = MatScale(s1, M0)
  M0 = MatAdd(M2, M3)
  V5 = Tanh(V2)
  s1 = Norm(V5)
  V3 = MatVec(M0, V4)
  s0 = Dot(V3, V3)
  M3 = MatMul(M3, M3)
  M2 = MatScale(s0, M3)
  M2 = MatAdd(M2, M1)
  M0 = MatScale(s1, M0)

structure: decayed linear attention  [a=0.868 b=0.863 c=-0.001 g=0.010, erase c/a=0.001, R²=0.9922, 1408 steps]

train acc 0.517 ±0.014
test regime collision3: acc 0.520  margin -0.045  ±0.006
test d16 T12 ow0.3: acc 0.724  margin 0.121  ±0.007
test d16 T12 ow0.0: acc 0.691  margin 0.096  ±0.006
test d16 T12 ow0.6: acc 0.729  margin 0.112  ±0.008
test d32 T24 ow0.3: acc 0.771  margin 0.182  ±0.006
test d8 T6 ow0.3: acc 0.639  margin 0.019  ±0.010
test d16 T64 K8 ow0.3: acc 0.584  margin -0.013  ±0.011
test d16 T128 K8 ow0.3: acc 0.553  margin -0.033  ±0.016
```
