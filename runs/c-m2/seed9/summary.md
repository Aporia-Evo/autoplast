# Search seed 9

task: regime collision3  alphabet: 19 ops  readout: fixed o = S q  add-node mutation: on  candidates: 1500020  real evaluations (after cache): 542468  time: 3739s  pop: 500  tournament: 10

commit: 21e513a  task seed: 1  train episodes: 144  persistent registers: 2 matrix, 0 vector  batch: 128

## Structural rediscovery (first candidate count at which the best rule belongs to a family)

* decayed linear attention: 2164 candidates
* linear attention: 12020 candidates
* unclassified: 15092 candidates
* gated delta rule: 724084 candidates
* delta rule: 725108 candidates

## Milestones (accuracy levels: first candidate count where best train acc reached the reference rule; not rediscovery)

- linear attention (acc 0.362): 12020 candidates
- delta rule (beta=1) (acc 0.578): 724212 candidates
- delta rule (beta=0.5) (acc 0.617): 725108 candidates
- gated delta (alpha=0.9) (acc 0.519): 723060 candidates

## Best rule

```
S' = ((0.888·(v)⊗(k) + (0.888·0.888·(v)⊗(k) + (S + (P1)ᵀ))) - ((0.888·(v)⊗(k) + (0.888·0.888·(v)⊗(k) + (S + (P1)ᵀ))))(((0.888·(v)⊗(k))ᵀ)(0.888·(v)⊗(k))))
P1' = (0.888·(v)⊗(k))ᵀ

Effective program (12 instructions):
  M2 = Transpose(M1)
  M1 = Outer(V1, V0)
  s1 = 0.8885
  M3 = MatScale(s1, M1)
  M0 = MatAdd(M0, M2)
  M2 = MatScale(s1, M3)
  M0 = MatAdd(M2, M0)
  M0 = MatAdd(M3, M0)
  M1 = Transpose(M3)
  M3 = MatMul(M1, M3)
  M2 = MatMul(M0, M3)
  M0 = MatSub(M0, M2)

structure: unclassified  [a=1.040 b=0.354 c=-0.815 g=0.001, erase c/a=0.783, R²=0.5593, 1408 steps]

train acc 0.667 ±0.013
test regime collision3: acc 0.679  margin 0.062  ±0.006
test d16 T12 ow0.3: acc 0.923  margin 0.284  ±0.004
test d16 T12 ow0.0: acc 0.868  margin 0.233  ±0.004
test d16 T12 ow0.6: acc 0.953  margin 0.303  ±0.004
test d32 T24 ow0.3: acc 0.978  margin 0.369  ±0.002
test d8 T6 ow0.3: acc 0.829  margin 0.134  ±0.008
test d16 T64 K8 ow0.3: acc 0.870  margin 0.222  ±0.007
test d16 T128 K8 ow0.3: acc 0.885  margin 0.222  ±0.010
```
