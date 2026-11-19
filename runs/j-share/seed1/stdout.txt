# Search seed 1

task: regime collision3  alphabet: 20 ops, with Recip  readout: fixed o = S q  add-node mutation: on  candidates: 1500020  real evaluations (after cache): 937470  time: 2815s  pop: 500  tournament: 10

commit: 50c2d10  task seed: 1  train episodes: 144  persistent registers: 3 matrix, 0 vector, start identity  batch: 128

search: regularized evolution  tune-consts: 0  select: share (radius 0.05)

validation level (val > 0.651, T128 K8 val >= 0.838, train - val <= 0.03; checked every 50000 candidates): 1250036 candidates

## Structural rediscovery (first candidate count at which the best rule belongs to a family)

* unclassified: 5364 candidates
* decayed linear attention: 8948 candidates
* linear, not error-correcting: 15604 candidates

## Milestones (accuracy levels: first candidate count where best train acc reached the reference rule; not rediscovery)

- linear attention (acc 0.362): 28276 candidates
- delta rule (beta=1) (acc 0.578): 84084 candidates
- delta rule (beta=0.5) (acc 0.617): 103412 candidates
- gated delta (alpha=0.9) (acc 0.519): 28276 candidates

## Best rule

```
S' = (σ(0)·S + ((((tanh(v) - P1·norm(k)))⊗(k) + P1) - P2))
P1' = ((((tanh(v) - P1·norm(k)))⊗(k) + P1) - P2)
P2' = (tanh(0))⊗((P1·norm(k) - tanh(0)))

Effective program (13 instructions):
  V4 = Tanh(V3)
  V1 = Tanh(V1)
  V5 = Normalize(V0)
  V2 = MatVec(M1, V5)
  V3 = VecSub(V1, V2)
  M3 = Outer(V3, V0)
  M1 = MatAdd(M3, M1)
  s2 = Sigmoid(s3)
  M1 = MatSub(M1, M2)
  V3 = VecSub(V2, V4)
  M3 = MatScale(s2, M0)
  M0 = MatAdd(M3, M1)
  M2 = Outer(V4, V3)

structure: unclassified  [a=1.035 b=0.949 c=-0.535 g=0.001, erase c/a=0.517, R²=0.8035, 1408 steps]

train acc 0.642 ±0.014
test regime collision3: acc 0.658  margin 0.044  ±0.006
test d16 T12 ow0.3: acc 0.912  margin 0.275  ±0.004
test d16 T12 ow0.0: acc 0.842  margin 0.215  ±0.005
test d16 T12 ow0.6: acc 0.940  margin 0.297  ±0.005
test d32 T24 ow0.3: acc 0.962  margin 0.361  ±0.003
test d8 T6 ow0.3: acc 0.788  margin 0.115  ±0.009
test d16 T64 K8 ow0.3: acc 0.861  margin 0.223  ±0.008
test d16 T128 K8 ow0.3: acc 0.881  margin 0.223  ±0.010
```
