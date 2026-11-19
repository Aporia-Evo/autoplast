# Search seed 8

task: v2  alphabet: 19 ops  readout: fixed o = S q  add-node mutation: on  candidates: 1500020  real evaluations (after cache): 712182  time: 407s  pop: 500  tournament: 10

commit: 6c2f60a  task seed: 1  train episodes: 96  persistent registers: 1 matrix, 0 vector, start zero  batch: 128

search: regularized evolution  tune-consts: 0  select: downsample (rate 0.1)  residual-insert: off

## Structural rediscovery (first candidate count at which the best rule belongs to a family)

* unclassified: 1268 candidates
* decayed linear attention: 2164 candidates
* linear, not error-correcting: 3444 candidates
* linear attention: 118260 candidates
* delta rule: 122484 candidates
* gated delta rule: 284532 candidates

## Milestones (accuracy levels: first candidate count where best train acc reached the reference rule; not rediscovery)

- linear attention (acc 0.772): 118260 candidates
- delta rule (beta=1) (acc 0.858): 122484 candidates
- delta rule (beta=0.5) (acc 0.932): 123252 candidates
- gated delta (alpha=0.9) (acc 0.729): 118260 candidates

## Best rule

```
S' = (σ(σ(0.938)·<S·k, S·k>) + 0.564)·((σ(σ(σ(0.938)·<S·k, S·k>))·(v - S·k))⊗(norm(tanh(k))) + S)

Effective program (16 instructions):
  s1 = 0.9382
  s0 = 0.5640
  V2 = Tanh(V0)
  s2 = Sigmoid(s1)
  V4 = MatVec(M0, V0)
  V0 = Normalize(V2)
  V1 = VecSub(V1, V4)
  s3 = Dot(V4, V4)
  s2 = SMul(s2, s3)
  s3 = Sigmoid(s2)
  s2 = Sigmoid(s3)
  V1 = VecScale(s2, V1)
  M3 = Outer(V1, V0)
  M0 = MatAdd(M3, M0)
  s2 = SAdd(s3, s0)
  M0 = MatScale(s2, M0)

structure: unclassified  [a=1.167 b=0.724 c=-0.752 g=-0.045, erase c/a=0.644, R²=0.9663, 384 steps]

train acc 0.982 ±0.005
test d16 T12 ow0.3: acc 0.975  margin 0.302  ±0.002
test d16 T12 ow0.0: acc 0.954  margin 0.279  ±0.003
test d16 T12 ow0.6: acc 0.958  margin 0.280  ±0.004
test d32 T24 ow0.3: acc 0.682  margin 0.115  ±0.007
test d8 T6 ow0.3: acc 0.839  margin 0.138  ±0.008
test d16 T64 K8 ow0.3: acc 0.000  margin 0.000  ±0.000
test d16 T128 K8 ow0.3: acc 0.000  margin 0.000  ±0.000
```
