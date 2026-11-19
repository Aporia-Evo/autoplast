# Search seed 31

task: regime collision3  alphabet: 20 ops, with Recip  readout: fixed o = S q  add-node mutation: on  candidates: 1500020  real evaluations (after cache): 886468  time: 2559s  pop: 500  tournament: 10

commit: 50c2d10  task seed: 1  train episodes: 144  persistent registers: 3 matrix, 0 vector, start identity  batch: 128

search: regularized evolution  tune-consts: 0  select: share (radius 0.05)

validation level (val > 0.651, T128 K8 val >= 0.838, train - val <= 0.03; checked every 50000 candidates): 200052 candidates

## Structural rediscovery (first candidate count at which the best rule belongs to a family)

* decayed linear attention: 2164 candidates
* linear attention: 3316 candidates
* unclassified: 5108 candidates
* linear, not error-correcting: 8308 candidates
* delta rule: 22644 candidates

## Milestones (accuracy levels: first candidate count where best train acc reached the reference rule; not rediscovery)

- linear attention (acc 0.362): 3316 candidates
- delta rule (beta=1) (acc 0.578): 7284 candidates
- delta rule (beta=0.5) (acc 0.617): 98420 candidates
- gated delta (alpha=0.9) (acc 0.519): 7156 candidates

## Best rule

```
S' = ((σ(0)·((((S - P1) + P1))ᵀ)ᵀ + (S - P1)) + (((((P1)ᵀ - (P1)ᵀ) - (S - P1))·k + (v - norm(0))))⊗(k))
P1' = σ(0)·((((S - P1) + P1))ᵀ)ᵀ
P2' = (((((P1)ᵀ - (P1)ᵀ) - (S - P1))·k + (v - norm(0))))⊗(k)

Effective program (16 instructions):
  M0 = MatSub(M0, M1)
  M3 = Transpose(M1)
  s1 = Sigmoid(s1)
  V5 = Normalize(V3)
  M1 = MatAdd(M0, M1)
  V3 = VecSub(V1, V5)
  M2 = Transpose(M1)
  M3 = MatSub(M3, M3)
  M1 = MatSub(M3, M0)
  V2 = MatVec(M1, V0)
  V5 = VecAdd(V2, V3)
  M1 = Transpose(M2)
  M1 = MatScale(s1, M1)
  M3 = MatAdd(M1, M0)
  M2 = Outer(V5, V0)
  M0 = MatAdd(M3, M2)

structure: unclassified  [a=1.020 b=1.000 c=-0.520 g=0.000, erase c/a=0.510, R²=0.6238, 1408 steps]

train acc 0.633 ±0.014
test regime collision3: acc 0.640  margin 0.037  ±0.006
test d16 T12 ow0.3: acc 0.873  margin 0.235  ±0.005
test d16 T12 ow0.0: acc 0.808  margin 0.179  ±0.005
test d16 T12 ow0.6: acc 0.914  margin 0.263  ±0.005
test d32 T24 ow0.3: acc 0.944  margin 0.324  ±0.003
test d8 T6 ow0.3: acc 0.720  margin 0.079  ±0.009
test d16 T64 K8 ow0.3: acc 0.866  margin 0.223  ±0.008
test d16 T128 K8 ow0.3: acc 0.879  margin 0.223  ±0.010
```
