# Search seed 31

task: v2  alphabet: 19 ops  readout: fixed o = S q  add-node mutation: on  candidates: 4000116  real evaluations (after cache): 1829398  time: 2143s  pop: 500  tournament: 10

commit: 50c2d10  task seed: 1  train episodes: 96  persistent registers: 1 matrix, 0 vector, start zero  batch: 128

search: regularized evolution  tune-consts: 0  select: fitness

## Structural rediscovery (first candidate count at which the best rule belongs to a family)

* unclassified: 6388 candidates
* decayed linear attention: 10484 candidates
* linear, not error-correcting: 11764 candidates
* linear attention: 31220 candidates
* delta rule: 206580 candidates
* gated delta rule: 209396 candidates

## Milestones (accuracy levels: first candidate count where best train acc reached the reference rule; not rediscovery)

- linear attention (acc 0.772): 31220 candidates
- delta rule (beta=1) (acc 0.858): 205684 candidates
- delta rule (beta=0.5) (acc 0.932): 207348 candidates
- gated delta (alpha=0.9) (acc 0.729): 31220 candidates

## Best rule

```
S' = 1.091·((tanh(v))⊗(tanh(k)) + (S - 0.636·(S)((k)⊗(k))))

Effective program (11 instructions):
  s0 = 0.6362
  V3 = Tanh(V0)
  M1 = Outer(V0, V0)
  M3 = MatMul(M0, M1)
  M3 = MatScale(s0, M3)
  M1 = MatSub(M0, M3)
  V0 = Tanh(V1)
  M3 = Outer(V0, V3)
  s0 = 1.0915
  M1 = MatAdd(M3, M1)
  M0 = MatScale(s0, M1)

structure: gated delta rule  [a=1.092 b=0.987 c=-0.695 g=0.004, erase c/a=0.637, R²=0.9985, 384 steps]

train acc 0.973 ±0.006
test d16 T12 ow0.3: acc 0.966  margin 0.300  ±0.003
test d16 T12 ow0.0: acc 0.955  margin 0.278  ±0.003
test d16 T12 ow0.6: acc 0.963  margin 0.288  ±0.004
test d32 T24 ow0.3: acc 0.967  margin 0.343  ±0.003
test d8 T6 ow0.3: acc 0.832  margin 0.136  ±0.008
test d16 T64 K8 ow0.3: acc 0.083  margin -0.464  ±0.006
test d16 T128 K8 ow0.3: acc 0.017  margin -0.633  ±0.004
```
