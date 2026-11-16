# Search seed 20

task: v2  alphabet: 19 ops  readout: fixed o = S q  add-node mutation: on  candidates: 4000116  real evaluations (after cache): 1062059  time: 500s  pop: 500  tournament: 10

commit: 50c2d10  task seed: 1  train episodes: 96  persistent registers: 1 matrix, 0 vector, start zero  batch: 128

search: regularized evolution  tune-consts: 0  select: fitness

## Structural rediscovery (first candidate count at which the best rule belongs to a family)

* decayed linear attention: 1268 candidates
* linear, not error-correcting: 2036 candidates
* unclassified: 3572 candidates
* linear attention: 20596 candidates
* delta rule: 2946804 candidates
* gated delta rule: 2947316 candidates

## Milestones (accuracy levels: first candidate count where best train acc reached the reference rule; not rediscovery)

- linear attention (acc 0.772): 20596 candidates
- delta rule (beta=1) (acc 0.858): 2946804 candidates
- delta rule (beta=0.5) (acc 0.932): 2947060 candidates
- gated delta (alpha=0.9) (acc 0.729): 20596 candidates

## Best rule

```
S' = (1.104·S - ((σ(|tanh(tanh(S·k))|)·S·k - v))⊗(k))

Effective program (11 instructions):
  s2 = 1.1040
  V4 = MatVec(M0, V0)
  V2 = Tanh(V4)
  V3 = Tanh(V2)
  s3 = Norm(V3)
  s0 = Sigmoid(s3)
  V5 = VecScale(s0, V4)
  M0 = MatScale(s2, M0)
  V1 = VecSub(V5, V1)
  M3 = Outer(V1, V0)
  M0 = MatSub(M0, M3)

structure: gated delta rule  [a=1.104 b=1.000 c=-0.735 g=0.010, erase c/a=0.665, R²=0.9982, 384 steps]

train acc 0.976 ±0.005
test d16 T12 ow0.3: acc 0.970  margin 0.306  ±0.003
test d16 T12 ow0.0: acc 0.957  margin 0.280  ±0.003
test d16 T12 ow0.6: acc 0.964  margin 0.300  ±0.004
test d32 T24 ow0.3: acc 0.987  margin 0.363  ±0.002
test d8 T6 ow0.3: acc 0.843  margin 0.139  ±0.008
test d16 T64 K8 ow0.3: acc 0.119  margin -0.446  ±0.007
test d16 T128 K8 ow0.3: acc 0.000  margin 0.000  ±0.000
```
