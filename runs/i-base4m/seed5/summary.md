# Search seed 5

task: v2  alphabet: 19 ops  readout: fixed o = S q  add-node mutation: on  candidates: 4000116  real evaluations (after cache): 1438293  time: 602s  pop: 500  tournament: 10

commit: 50c2d10  task seed: 1  train episodes: 96  persistent registers: 1 matrix, 0 vector, start zero  batch: 128

search: regularized evolution  tune-consts: 0  select: fitness

## Structural rediscovery (first candidate count at which the best rule belongs to a family)

* unclassified: 884 candidates
* decayed linear attention: 2292 candidates
* linear attention: 32500 candidates
* delta rule: 2174196 candidates
* linear, not error-correcting: 2176372 candidates
* gated delta rule: 2212596 candidates
* delta + Kronecker mix: 2419316 candidates

## Milestones (accuracy levels: first candidate count where best train acc reached the reference rule; not rediscovery)

- linear attention (acc 0.772): 34036 candidates
- delta rule (beta=1) (acc 0.858): 2175220 candidates
- delta rule (beta=0.5) (acc 0.932): 2176884 candidates
- gated delta (alpha=0.9) (acc 0.729): 32500 candidates

## Best rule

```
S' = (σ(0.145·<(tanh(v) - S·k), (tanh(v) - S·k)>·<(tanh(v) - S·k), (tanh(v) - S·k)>) + σ(0.145·<(tanh(v) - S·k), (tanh(v) - S·k)>·<(tanh(v) - S·k), (tanh(v) - S·k)>))·(S + ((tanh(v) - S·k))⊗(σ(σ(0.145·<(tanh(v) - S·k), (tanh(v) - S·k)>·<(tanh(v) - S·k), (tanh(v) - S·k)>))·k))

Effective program (14 instructions):
  s3 = 0.1450
  V4 = MatVec(M0, V0)
  V5 = Tanh(V1)
  V1 = VecSub(V5, V4)
  s0 = Dot(V1, V1)
  s3 = SMul(s3, s0)
  s2 = SMul(s3, s0)
  s2 = Sigmoid(s2)
  s0 = Sigmoid(s2)
  V5 = VecScale(s0, V0)
  M3 = Outer(V1, V5)
  M0 = MatAdd(M0, M3)
  s1 = SAdd(s2, s2)
  M0 = MatScale(s1, M0)

structure: unclassified  [a=1.185 b=0.683 c=-0.754 g=-0.329, erase c/a=0.636, R²=0.8832, 384 steps]

train acc 0.978 ±0.005
test d16 T12 ow0.3: acc 0.972  margin 0.301  ±0.002
test d16 T12 ow0.0: acc 0.952  margin 0.277  ±0.003
test d16 T12 ow0.6: acc 0.961  margin 0.278  ±0.004
test d32 T24 ow0.3: acc 0.601  margin 0.023  ±0.007
test d8 T6 ow0.3: acc 0.827  margin 0.133  ±0.008
test d16 T64 K8 ow0.3: acc 0.000  margin 0.000  ±0.000
test d16 T128 K8 ow0.3: acc 0.000  margin 0.000  ±0.000
```
