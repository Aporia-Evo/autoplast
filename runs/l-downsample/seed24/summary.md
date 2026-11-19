# Search seed 24

task: v2  alphabet: 19 ops  readout: fixed o = S q  add-node mutation: on  candidates: 1500020  real evaluations (after cache): 595561  time: 411s  pop: 500  tournament: 10

commit: 6c2f60a  task seed: 1  train episodes: 96  persistent registers: 1 matrix, 0 vector, start zero  batch: 128

search: regularized evolution  tune-consts: 0  select: downsample (rate 0.1)  residual-insert: off

## Structural rediscovery (first candidate count at which the best rule belongs to a family)

* unclassified: 1396 candidates
* linear, not error-correcting: 1908 candidates
* decayed linear attention: 2036 candidates
* linear attention: 7668 candidates
* delta rule: 390900 candidates
* gated delta rule: 995572 candidates

## Milestones (accuracy levels: first candidate count where best train acc reached the reference rule; not rediscovery)

- linear attention (acc 0.772): 7668 candidates
- delta rule (beta=1) (acc 0.858): 391924 candidates
- delta rule (beta=0.5) (acc 0.932): 403700 candidates
- gated delta (alpha=0.9) (acc 0.729): 7668 candidates

## Best rule

```
S' = (σ((|tanh(S·k)| + 0.175)) + 0.423)·(((v - S·σ((|tanh(S·k)| + 0.175))·σ((|tanh(S·k)| + 0.175))·k))⊗(k) + S)

Effective program (15 instructions):
  V5 = MatVec(M0, V0)
  V5 = Tanh(V5)
  s0 = Norm(V5)
  s1 = 0.1751
  s2 = 0.4234
  s0 = SAdd(s0, s1)
  s0 = Sigmoid(s0)
  s1 = SMul(s0, s0)
  V2 = VecScale(s1, V0)
  V3 = MatVec(M0, V2)
  V4 = VecSub(V1, V3)
  M2 = Outer(V4, V0)
  s2 = SAdd(s0, s2)
  M0 = MatAdd(M2, M0)
  M0 = MatScale(s2, M0)

structure: unclassified  [a=1.200 b=1.139 c=-0.793 g=-0.008, erase c/a=0.661, R²=0.9647, 384 steps]

train acc 0.981 ±0.005
test d16 T12 ow0.3: acc 0.974  margin 0.302  ±0.002
test d16 T12 ow0.0: acc 0.959  margin 0.276  ±0.003
test d16 T12 ow0.6: acc 0.962  margin 0.288  ±0.004
test d32 T24 ow0.3: acc 0.783  margin 0.211  ±0.006
test d8 T6 ow0.3: acc 0.832  margin 0.134  ±0.008
test d16 T64 K8 ow0.3: acc 0.000  margin 0.000  ±0.000
test d16 T128 K8 ow0.3: acc 0.000  margin 0.000  ±0.000
```
