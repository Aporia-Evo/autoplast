# Search seed 1

task: v2  alphabet: 19 ops  readout: fixed o = S q  add-node mutation: on  candidates: 1500020  real evaluations (after cache): 595862  time: 502s  pop: 500  tournament: 10

commit: 6c2f60a  task seed: 1  train episodes: 96  persistent registers: 1 matrix, 0 vector, start zero  batch: 128

search: regularized evolution  tune-consts: 0  select: downsample (rate 0.1)  residual-insert: off

## Structural rediscovery (first candidate count at which the best rule belongs to a family)

* unclassified: 1652 candidates
* decayed linear attention: 2036 candidates
* linear, not error-correcting: 3060 candidates
* linear attention: 8052 candidates
* delta rule: 478068 candidates

## Milestones (accuracy levels: first candidate count where best train acc reached the reference rule; not rediscovery)

- linear attention (acc 0.772): 8052 candidates
- delta rule (beta=1) (acc 0.858): 478068 candidates
- delta rule (beta=0.5) (acc 0.932): 482676 candidates
- gated delta (alpha=0.9) (acc 0.729): 8052 candidates

## Best rule

```
S' = (<(|S·k| + |S·k|)·(tanh(k) - k), tanh(k)>·(|S·k|·0.563·(tanh(S·k))⊗(k) - S) + ((v)⊗(k) - (|S·k|·0.563·(tanh(S·k))⊗(k) - S)))

Effective program (17 instructions):
  V5 = MatVec(M0, V0)
  V3 = Tanh(V5)
  M2 = Outer(V3, V0)
  s2 = 0.5632
  M1 = MatScale(s2, M2)
  s1 = Norm(V5)
  M3 = MatScale(s1, M1)
  M2 = MatSub(M3, M0)
  s2 = SAdd(s1, s1)
  V5 = Tanh(V0)
  M0 = Outer(V1, V0)
  V3 = VecSub(V5, V0)
  M0 = MatSub(M0, M2)
  V1 = VecScale(s2, V3)
  s3 = Dot(V1, V5)
  M1 = MatScale(s3, M2)
  M0 = MatAdd(M1, M0)

structure: unclassified  [a=1.074 b=1.000 c=-0.605 g=0.022, erase c/a=0.563, R²=0.9809, 384 steps]

train acc 0.978 ±0.005
test d16 T12 ow0.3: acc 0.967  margin 0.289  ±0.003
test d16 T12 ow0.0: acc 0.957  margin 0.262  ±0.003
test d16 T12 ow0.6: acc 0.966  margin 0.290  ±0.003
test d32 T24 ow0.3: acc 0.998  margin 0.384  ±0.001
test d8 T6 ow0.3: acc 0.823  margin 0.127  ±0.008
test d16 T64 K8 ow0.3: acc 0.000  margin 0.000  ±0.000
test d16 T128 K8 ow0.3: acc 0.000  margin 0.000  ±0.000
```
