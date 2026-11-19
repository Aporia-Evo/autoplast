# Search seed 32

task: regime collision3  alphabet: 20 ops, with Recip  readout: fixed o = S q  add-node mutation: on  candidates: 1500020  real evaluations (after cache): 919043  time: 2376s  pop: 500  tournament: 10

commit: 50c2d10  task seed: 1  train episodes: 144  persistent registers: 3 matrix, 0 vector, start identity  batch: 128

search: regularized evolution  tune-consts: 0  select: share (radius 0.05)

validation level (val > 0.651, T128 K8 val >= 0.838, train - val <= 0.03; checked every 50000 candidates): 100084 candidates

## Structural rediscovery (first candidate count at which the best rule belongs to a family)

* decayed linear attention: 4596 candidates
* linear, not error-correcting: 6132 candidates
* unclassified: 7028 candidates
* linear attention: 8436 candidates

## Milestones (accuracy levels: first candidate count where best train acc reached the reference rule; not rediscovery)

- linear attention (acc 0.362): 8436 candidates
- delta rule (beta=1) (acc 0.578): 57332 candidates
- delta rule (beta=0.5) (acc 0.617): 57332 candidates
- gated delta (alpha=0.9) (acc 0.519): 51060 candidates

## Best rule

```
S' = ((S + P1) + ((norm(v) - ((S + P1) + 0)·k))⊗(k))
P1' = (((((S + P1) + 0)·k + tanh(((norm(v) - ((S + P1) + 0)·k) + norm(v)))) + (v - 0·((S + P1) + 0)·k)))⊗(k)
P2' = ((norm(v) - ((S + P1) + 0)·k))⊗(k)

Effective program (14 instructions):
  M0 = MatAdd(M0, M1)
  M3 = MatAdd(M0, M3)
  V3 = MatVec(M3, V0)
  V2 = VecScale(s1, V3)
  V5 = VecSub(V1, V2)
  V4 = Normalize(V1)
  V1 = VecSub(V4, V3)
  M2 = Outer(V1, V0)
  V1 = VecAdd(V1, V4)
  V1 = Tanh(V1)
  V1 = VecAdd(V3, V1)
  M0 = MatAdd(M0, M2)
  V3 = VecAdd(V1, V5)
  M1 = Outer(V3, V0)

structure: unclassified  [a=1.030 b=1.000 c=-1.030 g=-0.000, erase c/a=1.000, R²=0.6071, 1408 steps]

train acc 0.640 ±0.014
test regime collision3: acc 0.656  margin 0.080  ±0.006
test d16 T12 ow0.3: acc 0.919  margin 0.284  ±0.004
test d16 T12 ow0.0: acc 0.882  margin 0.241  ±0.004
test d16 T12 ow0.6: acc 0.945  margin 0.305  ±0.004
test d32 T24 ow0.3: acc 0.975  margin 0.367  ±0.002
test d8 T6 ow0.3: acc 0.810  margin 0.135  ±0.008
test d16 T64 K8 ow0.3: acc 0.844  margin 0.202  ±0.008
test d16 T128 K8 ow0.3: acc 0.850  margin 0.200  ±0.011
```
