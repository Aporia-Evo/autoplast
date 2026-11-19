# Search seed 26

task: v2  alphabet: 19 ops  readout: fixed o = S q  add-node mutation: on  candidates: 1500020  real evaluations (after cache): 736892  time: 456s  pop: 500  tournament: 10

commit: 6c2f60a  task seed: 1  train episodes: 96  persistent registers: 1 matrix, 0 vector, start zero  batch: 128

search: regularized evolution  tune-consts: 0  select: downsample (rate 0.1)  residual-insert: off

## Structural rediscovery (first candidate count at which the best rule belongs to a family)

* decayed linear attention: 2036 candidates
* linear, not error-correcting: 2932 candidates
* unclassified: 4468 candidates
* linear attention: 7028 candidates
* delta rule: 47604 candidates
* gated delta rule: 227444 candidates

## Milestones (accuracy levels: first candidate count where best train acc reached the reference rule; not rediscovery)

- linear attention (acc 0.772): 7028 candidates
- delta rule (beta=1) (acc 0.858): 37492 candidates
- delta rule (beta=0.5) (acc 0.932): 47604 candidates
- gated delta (alpha=0.9) (acc 0.729): 7028 candidates

## Best rule

```
S' = ((σ(|S·k|) + σ(σ(|S·k|)·σ(|S·k|)))·S + (((v - (S·k + S·k)) + ((σ(|S·k|)·σ(|S·k|)·v - σ(|S·k|)·σ(|S·k|)·k) ⊙ σ(|S·k|)·σ(|S·k|)·k)))⊗(σ(|S·k|)·σ(|S·k|)·k))

Effective program (16 instructions):
  V4 = MatVec(M0, V0)
  s3 = Norm(V4)
  s0 = Sigmoid(s3)
  s1 = SMul(s0, s0)
  s2 = Sigmoid(s1)
  V0 = VecScale(s1, V0)
  s0 = SAdd(s0, s2)
  V4 = VecAdd(V4, V4)
  V3 = VecSub(V1, V4)
  V4 = VecScale(s1, V1)
  V1 = VecSub(V4, V0)
  V1 = Hadamard(V1, V0)
  V4 = VecAdd(V3, V1)
  M3 = Outer(V4, V0)
  M0 = MatScale(s0, M0)
  M0 = MatAdd(M0, M3)

structure: unclassified  [a=1.161 b=0.312 c=-0.694 g=-0.053, erase c/a=0.598, R²=0.9745, 384 steps]

train acc 0.979 ±0.005
test d16 T12 ow0.3: acc 0.973  margin 0.293  ±0.002
test d16 T12 ow0.0: acc 0.960  margin 0.273  ±0.003
test d16 T12 ow0.6: acc 0.965  margin 0.278  ±0.004
test d32 T24 ow0.3: acc 0.849  margin 0.238  ±0.005
test d8 T6 ow0.3: acc 0.833  margin 0.134  ±0.008
test d16 T64 K8 ow0.3: acc 0.000  margin 0.000  ±0.000
test d16 T128 K8 ow0.3: acc 0.000  margin 0.000  ±0.000
```
