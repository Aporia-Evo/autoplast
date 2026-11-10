# Search seed 2

task: regime collision3  alphabet: 19 ops  readout: fixed o = S q  add-node mutation: on  candidates: 1500020  real evaluations (after cache): 946966  time: 4405s  pop: 500  tournament: 10

commit: 21e513a  task seed: 1  train episodes: 144  persistent registers: 2 matrix, 0 vector  batch: 128

## Structural rediscovery (first candidate count at which the best rule belongs to a family)

* decayed linear attention: 3316 candidates
* linear, not error-correcting: 11124 candidates
* delta + Kronecker mix: 12020 candidates
* unclassified: 12276 candidates
* linear attention: 13684 candidates

## Milestones (accuracy levels: first candidate count where best train acc reached the reference rule; not rediscovery)

- linear attention (acc 0.362): 13428 candidates
- delta rule (beta=1) (acc 0.578): 170868 candidates
- delta rule (beta=0.5) (acc 0.617): 198644 candidates
- gated delta (alpha=0.9) (acc 0.519): 133108 candidates

## Best rule

```
S' = ((1.114·1.114·1.114·(-0.889·(0 - (P1 + (v)⊗(k))) - ((P1 + (v)⊗(k))·k)⊗(k)) + 1.114·1.114·1.114·(-0.889·(0 - (P1 + (v)⊗(k))) - ((P1 + (v)⊗(k))·k)⊗(k))) + (-0.889·(0 - (P1 + (v)⊗(k))) - 0.391·1.114·((P1 + (v)⊗(k))·k)⊗(k)))
P1' = 1.114·(-0.889·(0 - (P1 + (v)⊗(k))) - 0.391·1.114·((P1 + (v)⊗(k))·k)⊗(k))

Effective program (19 instructions):
  M0 = Outer(V1, V0)
  s1 = -0.8894
  M1 = MatAdd(M1, M0)
  s2 = 1.1141
  M2 = MatSub(M2, M1)
  V3 = MatVec(M1, V0)
  s0 = 0.3908
  M0 = Outer(V3, V0)
  M1 = MatScale(s1, M2)
  M3 = MatScale(s2, M0)
  M3 = MatScale(s0, M3)
  M0 = MatSub(M1, M0)
  M2 = MatSub(M1, M3)
  M3 = MatScale(s2, M0)
  M3 = MatScale(s2, M3)
  M1 = MatScale(s2, M3)
  M0 = MatAdd(M1, M1)
  M0 = MatAdd(M0, M2)
  M1 = MatScale(s2, M2)

structure: unclassified  [a=1.009 b=0.149 c=-0.963 g=0.000, erase c/a=0.955, R²=0.4450, 1408 steps]

train acc 0.683 ±0.013
test regime collision3: acc 0.695  margin 0.092  ±0.006
test d16 T12 ow0.3: acc 0.932  margin 0.277  ±0.004
test d16 T12 ow0.0: acc 0.906  margin 0.247  ±0.004
test d16 T12 ow0.6: acc 0.957  margin 0.280  ±0.004
test d32 T24 ow0.3: acc 0.982  margin 0.351  ±0.002
test d8 T6 ow0.3: acc 0.842  margin 0.142  ±0.008
test d16 T64 K8 ow0.3: acc 0.846  margin 0.177  ±0.008
test d16 T128 K8 ow0.3: acc 0.861  margin 0.177  ±0.011
```
