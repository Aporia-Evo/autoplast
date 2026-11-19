# Search seed 31

task: v2  alphabet: 19 ops  readout: fixed o = S q  add-node mutation: on  candidates: 1500020  real evaluations (after cache): 475876  time: 321s  pop: 500  tournament: 10

commit: 6c2f60a  task seed: 1  train episodes: 96  persistent registers: 1 matrix, 0 vector, start zero  batch: 128

search: regularized evolution  tune-consts: 0  select: downsample (rate 0.1)  residual-insert: off

## Structural rediscovery (first candidate count at which the best rule belongs to a family)

* decayed linear attention: 2932 candidates
* linear, not error-correcting: 3572 candidates
* unclassified: 3956 candidates
* linear attention: 6388 candidates
* delta rule: 722420 candidates
* gated delta rule: 797428 candidates

## Milestones (accuracy levels: first candidate count where best train acc reached the reference rule; not rediscovery)

- linear attention (acc 0.772): 6388 candidates
- delta rule (beta=1) (acc 0.858): 724084 candidates
- delta rule (beta=0.5) (acc 0.932): 724596 candidates
- gated delta (alpha=0.9) (acc 0.729): 6388 candidates

## Best rule

```
S' = (σ(0.223)·(S + S) + (σ(<S·k, S·k>)·(v - S·k))⊗(k))

Effective program (11 instructions):
  V3 = MatVec(M0, V0)
  s0 = Dot(V3, V3)
  s2 = Sigmoid(s0)
  M1 = MatAdd(M0, M0)
  V1 = VecSub(V1, V3)
  s3 = 0.2226
  s3 = Sigmoid(s3)
  V5 = VecScale(s2, V1)
  M2 = Outer(V5, V0)
  M0 = MatScale(s3, M1)
  M0 = MatAdd(M0, M2)

structure: unclassified  [a=1.111 b=0.557 c=-0.633 g=-0.021, erase c/a=0.569, R²=0.9855, 384 steps]

train acc 0.977 ±0.005
test d16 T12 ow0.3: acc 0.971  margin 0.286  ±0.003
test d16 T12 ow0.0: acc 0.962  margin 0.269  ±0.002
test d16 T12 ow0.6: acc 0.964  margin 0.277  ±0.004
test d32 T24 ow0.3: acc 0.991  margin 0.364  ±0.001
test d8 T6 ow0.3: acc 0.826  margin 0.129  ±0.008
test d16 T64 K8 ow0.3: acc 0.180  margin -0.371  ±0.008
test d16 T128 K8 ow0.3: acc 0.000  margin 0.000  ±0.000
```
