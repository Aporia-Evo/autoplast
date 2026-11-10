# Search seed 14

task: regime collision3  alphabet: 19 ops  readout: fixed o = S q  add-node mutation: on  candidates: 1500020  real evaluations (after cache): 873987  time: 2901s  pop: 500  tournament: 10

commit: 21e513a  task seed: 1  train episodes: 144  persistent registers: 2 matrix, 0 vector  batch: 128

## Structural rediscovery (first candidate count at which the best rule belongs to a family)

* unclassified: 884 candidates
* decayed linear attention: 1012 candidates

## Milestones (accuracy levels: first candidate count where best train acc reached the reference rule; not rediscovery)

- linear attention (acc 0.362): 9460 candidates
- delta rule (beta=1) (acc 0.578): not reached
- delta rule (beta=0.5) (acc 0.617): not reached
- gated delta (alpha=0.9) (acc 0.519): 514548 candidates

## Best rule

```
S' = (0.646·(<(v ⊙ v), P1·(v ⊙ v)>·P1)ᵀ + (<(v ⊙ v), P1·(v ⊙ v)>·P1 - (P1 - (v)⊗(|tanh(tanh(k))|·(k + tanh(k))))))
P1' = |tanh(tanh(k))|·(P1 - (v)⊗(|tanh(tanh(k))|·(k + tanh(k))))

Effective program (17 instructions):
  V3 = Hadamard(V1, V1)
  V2 = Tanh(V0)
  V4 = MatVec(M1, V3)
  V0 = VecAdd(V0, V2)
  V2 = Tanh(V2)
  s2 = Dot(V3, V4)
  s1 = Norm(V2)
  V3 = VecScale(s1, V0)
  M0 = Outer(V1, V3)
  M2 = MatSub(M1, M0)
  M3 = MatScale(s2, M1)
  M0 = MatSub(M3, M2)
  s2 = 0.6463
  M3 = Transpose(M3)
  M3 = MatScale(s2, M3)
  M0 = MatAdd(M3, M0)
  M1 = MatScale(s1, M2)

structure: unclassified  [a=0.902 b=1.757 c=-0.002 g=0.004, erase c/a=0.003, R²=0.9826, 1408 steps]

train acc 0.515 ±0.014
test regime collision3: acc 0.515  margin -0.029  ±0.006
test d16 T12 ow0.3: acc 0.773  margin 0.144  ±0.006
test d16 T12 ow0.0: acc 0.782  margin 0.150  ±0.005
test d16 T12 ow0.6: acc 0.704  margin 0.100  ±0.009
test d32 T24 ow0.3: acc 0.856  margin 0.220  ±0.005
test d8 T6 ow0.3: acc 0.635  margin 0.028  ±0.010
test d16 T64 K8 ow0.3: acc 0.556  margin -0.012  ±0.011
test d16 T128 K8 ow0.3: acc 0.550  margin -0.028  ±0.016
```
