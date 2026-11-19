# Search seed 10

task: regime collision3  alphabet: 20 ops, with Recip  readout: fixed o = S q  add-node mutation: on  candidates: 1500020  real evaluations (after cache): 981836  time: 4579s  pop: 500  tournament: 10

commit: 50c2d10  task seed: 1  train episodes: 144  persistent registers: 3 matrix, 0 vector, start identity  batch: 128

search: regularized evolution  tune-consts: 0  select: share (radius 0.05)

validation level (val > 0.651, T128 K8 val >= 0.838, train - val <= 0.03; checked every 50000 candidates): not reached

## Structural rediscovery (first candidate count at which the best rule belongs to a family)

* decayed linear attention: 2036 candidates
* unclassified: 4468 candidates
* linear attention: 10740 candidates
* delta rule: 186228 candidates

## Milestones (accuracy levels: first candidate count where best train acc reached the reference rule; not rediscovery)

- linear attention (acc 0.362): 10740 candidates
- delta rule (beta=1) (acc 0.578): 39156 candidates
- delta rule (beta=0.5) (acc 0.617): 52340 candidates
- gated delta (alpha=0.9) (acc 0.519): 22644 candidates

## Best rule

```
S' = (σ(0)·(((v)⊗((0 - k)) - S))((k)⊗(k)) - ((v)⊗((0 - k)) - S))
P2' = (((v)⊗((0 - k)) - S))((k)⊗(k))

Effective program (8 instructions):
  s1 = Sigmoid(s0)
  M2 = Outer(V0, V0)
  V4 = VecSub(V3, V0)
  M3 = Outer(V1, V4)
  M3 = MatSub(M3, M0)
  M2 = MatMul(M3, M2)
  M0 = MatScale(s1, M2)
  M0 = MatSub(M0, M3)

structure: delta rule  [a=1.000 b=0.500 c=-0.500 g=-0.000, erase c/a=0.500, R²=1.0000, 1408 steps]

train acc 0.617 ±0.014
test regime collision3: acc 0.640  margin 0.048  ±0.006
test d16 T12 ow0.3: acc 0.924  margin 0.262  ±0.004
test d16 T12 ow0.0: acc 0.900  margin 0.237  ±0.004
test d16 T12 ow0.6: acc 0.941  margin 0.264  ±0.005
test d32 T24 ow0.3: acc 0.987  margin 0.350  ±0.002
test d8 T6 ow0.3: acc 0.793  margin 0.113  ±0.008
test d16 T64 K8 ow0.3: acc 0.840  margin 0.161  ±0.008
test d16 T128 K8 ow0.3: acc 0.828  margin 0.154  ±0.012
```
