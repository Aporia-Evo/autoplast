# Search seed 21

task: regime collision3  alphabet: 20 ops, with Recip  readout: fixed o = S q  add-node mutation: on  candidates: 1500020  real evaluations (after cache): 663083  time: 1546s  pop: 500  tournament: 10

commit: e979a8e  task seed: 1  train episodes: 144  persistent registers: 3 matrix, 0 vector, start identity  batch: 128

## Structural rediscovery (first candidate count at which the best rule belongs to a family)

* decayed linear attention: 756 candidates
* unclassified: 5492 candidates

## Milestones (accuracy levels: first candidate count where best train acc reached the reference rule; not rediscovery)

- linear attention (acc 0.362): 9972 candidates
- delta rule (beta=1) (acc 0.578): not reached
- delta rule (beta=0.5) (acc 0.617): not reached
- gated delta (alpha=0.9) (acc 0.519): 1151860 candidates

## Best rule

```
S' = (((0.438·P2 + 1/(0.400)·(v)⊗((k)⊗(k)·tanh(k))) + (0.438·P2 + 1/(0.400)·(v)⊗((k)⊗(k)·tanh(k)))) - 0.127·1/(0.400)·(v)⊗((k)⊗(k)·tanh(k)))
P1' = 0.127·1/(0.400)·(v)⊗((k)⊗(k)·tanh(k))
P2' = ((0.438·P2 + 1/(0.400)·(v)⊗((k)⊗(k)·tanh(k))) + (0.438·P2 + 1/(0.400)·(v)⊗((k)⊗(k)·tanh(k))))

Effective program (14 instructions):
  s1 = 0.4004
  s3 = Recip(s1)
  s1 = 0.1267
  M3 = Outer(V0, V0)
  V2 = Tanh(V0)
  V2 = MatVec(M3, V2)
  M0 = Outer(V1, V2)
  M3 = MatScale(s3, M0)
  M1 = MatScale(s1, M3)
  s1 = 0.4382
  M0 = MatScale(s1, M2)
  M0 = MatAdd(M0, M3)
  M2 = MatAdd(M0, M0)
  M0 = MatSub(M2, M1)

structure: unclassified  [a=0.890 b=4.422 c=0.000 g=0.001, erase c/a=-0.000, R²=0.9764, 1408 steps]

train acc 0.515 ±0.014
test regime collision3: acc 0.520  margin -0.040  ±0.006
test d16 T12 ow0.3: acc 0.739  margin 0.128  ±0.007
test d16 T12 ow0.0: acc 0.724  margin 0.116  ±0.006
test d16 T12 ow0.6: acc 0.721  margin 0.111  ±0.009
test d32 T24 ow0.3: acc 0.642  margin 0.101  ±0.007
test d8 T6 ow0.3: acc 0.631  margin 0.032  ±0.010
test d16 T64 K8 ow0.3: acc 0.582  margin -0.008  ±0.011
test d16 T128 K8 ow0.3: acc 0.561  margin -0.028  ±0.016
```
