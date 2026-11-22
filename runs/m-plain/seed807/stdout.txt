# Search seed 807

task: regime collision3  alphabet: 20 ops, with Recip  readout: fixed o = S q  add-node mutation: on  candidates: 1500020  real evaluations (after cache): 903468  time: 1896s  pop: 500  tournament: 10

commit: dce11aa  task seed: 807  train episodes: 144  persistent registers: 3 matrix, 0 vector, start identity  batch: 128

search: regularized evolution  tune-consts: 0  select: fitness  residual-insert: off

validation level (val > 0.651, T128 K8 val >= 0.838, train - val <= 0.03; checked every 50000 candidates): not reached

## Structural rediscovery (first candidate count at which the best rule belongs to a family)

* decayed linear attention: 628 candidates
* unclassified: 3956 candidates
* linear attention: 8308 candidates
* delta rule: 16884 candidates

## Milestones (accuracy levels: first candidate count where best train acc reached the reference rule; not rediscovery)

- linear attention (acc 0.383): 8308 candidates
- delta rule (beta=1) (acc 0.594): 16884 candidates
- delta rule (beta=0.5) (acc 0.628): 20468 candidates
- gated delta (alpha=0.9) (acc 0.516): 16884 candidates

## Best rule

```
S' = ((σ(<k, (0 - S)·k>)·((0 - S)·k + tanh(<tanh(v), tanh(v)>·tanh(tanh(v)))))⊗(tanh(norm(tanh(tanh(k))))) - (0 - S))
P2' = (σ(<k, (0 - S)·k>)·((0 - S)·k + tanh(<tanh(v), tanh(v)>·tanh(tanh(v)))))⊗(tanh(norm(tanh(tanh(k)))))

Effective program (17 instructions):
  V5 = Tanh(V1)
  M0 = MatSub(M3, M0)
  V1 = Tanh(V5)
  V3 = MatVec(M0, V0)
  V4 = Tanh(V0)
  s3 = Dot(V0, V3)
  V4 = Tanh(V4)
  V0 = Normalize(V4)
  s2 = Sigmoid(s3)
  s0 = Dot(V5, V5)
  V2 = VecScale(s0, V1)
  V4 = Tanh(V2)
  V1 = VecAdd(V3, V4)
  V5 = Tanh(V0)
  V0 = VecScale(s2, V1)
  M2 = Outer(V0, V5)
  M0 = MatSub(M2, M0)

structure: unclassified  [a=1.000 b=0.381 c=-0.477 g=-0.006, erase c/a=0.477, R²=0.9836, 1408 steps]

train acc 0.642 ±0.014
test regime collision3: acc 0.640  margin 0.045  ±0.006
test d16 T12 ow0.3: acc 0.917  margin 0.256  ±0.004
test d16 T12 ow0.0: acc 0.900  margin 0.232  ±0.004
test d16 T12 ow0.6: acc 0.935  margin 0.252  ±0.005
test d32 T24 ow0.3: acc 0.985  margin 0.346  ±0.002
test d8 T6 ow0.3: acc 0.773  margin 0.102  ±0.009
test d16 T64 K8 ow0.3: acc 0.820  margin 0.144  ±0.008
test d16 T128 K8 ow0.3: acc 0.802  margin 0.135  ±0.012
```
